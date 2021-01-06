import * as fs from 'fs';
import * as crypto from 'crypto';

import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as logs from '@aws-cdk/aws-logs';
import * as s3 from '@aws-cdk/aws-s3';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as cloudfrontOrigins from '@aws-cdk/aws-cloudfront-origins';
import * as certificatemanager from '@aws-cdk/aws-certificatemanager';
import * as route53 from '@aws-cdk/aws-route53';
import * as route53Targets from '@aws-cdk/aws-route53-targets';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';
import * as ssm from '@aws-cdk/aws-ssm';
import * as cloudwatchActions from '@aws-cdk/aws-cloudwatch-actions';
import * as snsSubscriptions from '@aws-cdk/aws-sns-subscriptions';
import * as sns from '@aws-cdk/aws-sns';
import * as cloudwatch from '@aws-cdk/aws-cloudwatch';

import { CONFIG } from './config';
import { ENVIRONMENT } from './environment';

export class IndexStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // package storage
    const bucket = s3.Bucket.fromBucketName(
      this,
      'Bucket',
      CONFIG.storage.bucketName
    );

    // Origin access identity
    const parameter = ssm.StringParameter.fromStringParameterName(
      this,
      'Parameter',
      CONFIG.storage.originAccessIdentityParameterName
    );
    const originAccessIdentity = cloudfront.OriginAccessIdentity.fromOriginAccessIdentityName(
      this,
      'AccessIdentity',
      parameter.stringValue
    );

    // Database for the packages
    const specTable = dynamodb.Table.fromTableAttributes(this, 'SpecTable', {
      tableName: CONFIG.database.spec.tableName,
      localIndexes: [CONFIG.database.spec.localSecondaryIndexName],
    });
    const credentialsTable = dynamodb.Table.fromTableAttributes(
      this,
      'CredentialsTable',
      {
        tableName: CONFIG.database.credentials.tableName,
        globalIndexes: [CONFIG.database.credentials.globalSecondaryIndexName],
      }
    );

    // Secret for credentials
    const secret = secretsmanager.Secret.fromSecretNameV2(
      this,
      'CredentialsSecret',
      CONFIG.security.secretName
    );

    // Lambda function
    const functionName = 'package-index-service';
    const deploymentPackage = 'resources/index/deployment-package.zip';
    const deploymentPackageContents = fs.readFileSync(deploymentPackage);
    const deploymentPackageHash = crypto
      .createHash('sha256')
      .update(deploymentPackageContents)
      .digest('hex');
    const func = new lambda.Function(this, 'IndexFunc', {
      functionName,
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(deploymentPackage),
      handler: 'app.main',
      logRetention: logs.RetentionDays.ONE_WEEK,
      timeout: cdk.Duration.seconds(5),
    });
    const version = new lambda.Version(
      this,
      `LambdaVersion-${deploymentPackageHash}`,
      {
        lambda: func,
        removalPolicy: cdk.RemovalPolicy.RETAIN,
      }
    );

    // Add alarm subscription
    const alarmName = `${functionName}-error`;
    const alarm = func.metricErrors().createAlarm(this, 'Alarm', {
      threshold: 1,
      evaluationPeriods: 1,
      alarmName,
      alarmDescription: `The ${functionName} lambda function had an error`,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });
    const topic = new sns.Topic(this, 'Topic', {
      displayName: `${alarmName}-alarm`,
      topicName: `${alarmName}-alarm`,
    });
    topic.addSubscription(
      new snsSubscriptions.EmailSubscription(ENVIRONMENT.alarmEmailAddress)
    );
    alarm.addAlarmAction(new cloudwatchActions.SnsAction(topic));

    // Permissions for lambda function
    specTable.grantReadData(func);
    specTable.grant(func, 'dynamodb:DescribeTable');
    credentialsTable.grantReadData(func);
    credentialsTable.grant(func, 'dynamodb:DescribeTable');
    secret.grantRead(func);

    // Certificate
    const certificateArn = ENVIRONMENT.awsOpenAlchemyCertificateArn;
    const certificate = certificatemanager.Certificate.fromCertificateArn(
      this,
      'Certificate',
      certificateArn
    );

    // CloudFront
    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new cloudfrontOrigins.S3Origin(bucket, {
          originAccessIdentity,
        }),
        edgeLambdas: [
          {
            functionVersion: version,
            eventType: cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
          },
        ],
      },
      domainNames: [`${CONFIG.index.recordName}.${CONFIG.domainName}`],
      certificate,
    });

    // DNS listing
    const zone = route53.PublicHostedZone.fromLookup(this, 'PublicHostedZone', {
      domainName: CONFIG.domainName,
    });
    new route53.ARecord(this, 'AliasRecord', {
      zone,
      target: route53.RecordTarget.fromAlias(
        new route53Targets.CloudFrontTarget(distribution)
      ),
      recordName: CONFIG.index.recordName,
    });
  }
}
