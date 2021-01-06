import * as fs from 'fs';
import * as crypto from 'crypto';

import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as logs from '@aws-cdk/aws-logs';
import * as codedeploy from '@aws-cdk/aws-codedeploy';
import * as s3 from '@aws-cdk/aws-s3';
import * as sns from '@aws-cdk/aws-sns';
import * as sqs from '@aws-cdk/aws-sqs';
import * as lambdaEventSources from '@aws-cdk/aws-lambda-event-sources';
import * as snsSubscriptions from '@aws-cdk/aws-sns-subscriptions';
import * as cloudwatchActions from '@aws-cdk/aws-cloudwatch-actions';
import * as cloudwatch from '@aws-cdk/aws-cloudwatch';

import { CONFIG } from './config';
import { ENVIRONMENT } from './environment';

export class BuildStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Storage for the packages
    const bucket = s3.Bucket.fromBucketName(
      this,
      'PackageBucket',
      CONFIG.storage.bucketName
    );

    // Configuration for lambda event source
    const topicArn = cdk.Arn.format(
      { resource: CONFIG.storage.topicName, service: 'sns' },
      this
    );
    const topic = sns.Topic.fromTopicArn(this, 'Topic', topicArn);
    const deadLetterQueue = new sqs.Queue(this, 'Queue', {
      queueName: `${CONFIG.storage.topicName}-dead-letter`,
    });

    // Lambda function
    const deploymentPackage = 'resources/build/deployment-package.zip';
    const deploymentPackageContents = fs.readFileSync(deploymentPackage);
    const deploymentPackageHash = crypto
      .createHash('sha256')
      .update(deploymentPackageContents)
      .digest('hex');
    const functionName = 'package-build-service';
    const func = new lambda.Function(this, 'BuildFunc', {
      functionName,
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(deploymentPackage),
      handler: 'app.main',
      environment: {
        STAGE: 'PROD',
        PACKAGE_STORAGE_BUCKET_NAME: CONFIG.storage.bucketName,
      },
      logRetention: logs.RetentionDays.ONE_WEEK,
      timeout: cdk.Duration.minutes(1),
    });
    bucket.grantReadWrite(func);
    const version = new lambda.Version(
      this,
      `LambdaVersion-${deploymentPackageHash}`,
      {
        lambda: func,
        removalPolicy: cdk.RemovalPolicy.RETAIN,
      }
    );
    const alias = new lambda.Alias(this, 'LambdaAlias', {
      aliasName: 'prod',
      version,
    });
    new codedeploy.LambdaDeploymentGroup(this, 'DeploymentGroup', {
      alias,
      deploymentConfig: codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
    });

    // Add alarm subscription
    const alarmName = `${functionName}-error`;
    const alarm = func.metricErrors().createAlarm(this, 'Alarm', {
      threshold: 1,
      evaluationPeriods: 1,
      alarmName,
      alarmDescription: `The ${functionName} lambda function had an error`,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });
    const alarmTopic = new sns.Topic(this, 'AlarmTopic', {
      displayName: `${alarmName}-alarm`,
      topicName: `${alarmName}-alarm`,
    });
    topic.addSubscription(
      new snsSubscriptions.EmailSubscription(ENVIRONMENT.alarmEmailAddress)
    );
    alarm.addAlarmAction(new cloudwatchActions.SnsAction(alarmTopic));

    // Add lambda trigger from bucket
    func.addEventSource(
      new lambdaEventSources.SnsEventSource(topic, { deadLetterQueue })
    );
  }
}
