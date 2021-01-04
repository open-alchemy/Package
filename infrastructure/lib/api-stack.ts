import * as fs from 'fs';
import * as crypto from 'crypto';

import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as logs from '@aws-cdk/aws-logs';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as codedeploy from '@aws-cdk/aws-codedeploy';
import * as cognito from '@aws-cdk/aws-cognito';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as route53 from '@aws-cdk/aws-route53';
import * as route53Targets from '@aws-cdk/aws-route53-targets';
import * as certificatemanager from '@aws-cdk/aws-certificatemanager';
import * as iam from '@aws-cdk/aws-iam';
import * as s3 from '@aws-cdk/aws-s3';
import * as sns from '@aws-cdk/aws-sns';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';
import * as s3Notifications from '@aws-cdk/aws-s3-notifications';

import { ENVIRONMENT } from './environment';
import { CONFIG } from './config';

export class ApiStack extends cdk.Stack {
  constructor(
    scope: cdk.Construct,
    id: string,
    props: cdk.StackProps,
    storageBucket: s3.Bucket
  ) {
    super(scope, id, props);

    // Storage for the packages
    const bucket = new s3.Bucket(this, 'PackageBucket', {
      bucketName: CONFIG.storage.bucketName,
    });

    // Grant package index distribution access to the bucket
    const originAccessIdentity = new cloudfront.OriginAccessIdentity(
      this,
      'AccessIdentity'
    );
    bucket.grantRead(originAccessIdentity);

    // Notifications for object create
    const topic = new sns.Topic(this, 'Topic', {
      displayName: CONFIG.storage.topicName,
      topicName: CONFIG.storage.topicName,
    });
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED,
      new s3Notifications.SnsDestination(topic),
      { suffix: '.json' }
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
    const deploymentPackage = 'resources/api/deployment-package.zip';
    const deploymentPackageContents = fs.readFileSync(deploymentPackage);
    const deploymentPackageHash = crypto
      .createHash('sha256')
      .update(deploymentPackageContents)
      .digest('hex');
    const func = new lambda.Function(this, 'ApiFunc', {
      functionName: 'package-service',
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(deploymentPackage),
      handler: 'api.main',
      environment: {
        STAGE: 'PROD',
        ACCESS_CONTROL_ALLOW_ORIGIN: '*',
        ACCESS_CONTROL_ALLOW_HEADERS: 'x-language',
        PACKAGE_STORAGE_BUCKET_NAME: CONFIG.storage.newBucketName,
        DEFAULT_CREDENTIALS_ID: CONFIG.api.defaultCredentialsId,
      },
      logRetention: logs.RetentionDays.ONE_WEEK,
      timeout: cdk.Duration.seconds(10),
    });
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
    const integration = new apigateway.LambdaIntegration(alias);

    // Permissions for lambda function
    bucket.grantReadWrite(func);
    storageBucket.grantReadWrite(func);
    specTable.grantReadWriteData(func);
    specTable.grant(func, 'dynamodb:DescribeTable');
    credentialsTable.grantReadWriteData(func);
    credentialsTable.grant(func, 'dynamodb:DescribeTable');
    secret.grantRead(func);

    // Certificate
    const certificateArn = ENVIRONMENT.AWS_OPEN_ALCHEMY_CERTIFICATE_ARN;
    const certificate = certificatemanager.Certificate.fromCertificateArn(
      this,
      'Certificate',
      certificateArn
    );

    // API gateway
    const api = new apigateway.RestApi(this, 'RestApi', {
      restApiName: 'Package Service',
      description: 'Micro service supporting the OpenAlchemy package service',
      deployOptions: {
        throttlingBurstLimit: CONFIG.api.throttlingBurstLimit,
        throttlingRateLimit: CONFIG.api.throttlingRateLimit,
      },
      deploy: true,
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: apigateway.Cors.DEFAULT_HEADERS.concat(
          CONFIG.api.additionalAllowHeaders
        ),
      },
      domainName: {
        certificate,
        domainName: `${CONFIG.api.recordName}.${CONFIG.domainName}`,
      },
    });
    alias.addPermission('RestApiLambdaPermission', {
      principal: new iam.ServicePrincipal('apigateway.amazonaws.com'),
      sourceArn: api.arnForExecuteApi(),
    });

    // Add Cognito authorizer
    const authorizer = new apigateway.CfnAuthorizer(this, 'Authorizer', {
      restApiId: api.restApiId,
      type: apigateway.AuthorizationType.COGNITO,
      identitySource: apigateway.IdentitySource.header('Authorization'),
      providerArns: [ENVIRONMENT.AWS_IDENTITY_PROVIDER_ARN],
      name: 'PackageAuth',
    });

    // Protect resources with cognito
    const versionResource = api.root.addResource('v1');

    // Add UI resources
    const uiResource = versionResource.addResource('ui');
    uiResource.addMethod('GET', integration);
    const openapiResource = versionResource.addResource('openapi.json');
    openapiResource.addMethod('GET', integration);
    const uiSubResources = [
      'swagger-ui-standalone-preset.js',
      'swagger-ui-bundle.js',
      'swagger-ui.css',
      'favicon-32x32.png',
      'favicon-16x16.png',
    ];
    uiSubResources.forEach((uiSubResourcePath) => {
      const uiSubResource = uiResource.addResource(uiSubResourcePath);
      uiSubResource.addMethod('GET', integration);
    });

    // Add specs endpoints
    const specsResource = versionResource.addResource('specs');
    specsResource.addMethod('GET', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.read`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    const specsSpecIdResource = specsResource.addResource('{spec_id}');
    specsSpecIdResource.addMethod('GET', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.read`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    specsSpecIdResource.addMethod('PUT', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.write`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    specsSpecIdResource.addMethod('DELETE', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.write`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    const specsIdVersionsResource = specsSpecIdResource.addResource('versions');
    specsIdVersionsResource.addMethod('GET', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.read`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    const specsIdVersionsVersionResource = specsIdVersionsResource.addResource(
      '{version}'
    );
    specsIdVersionsVersionResource.addMethod('GET', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.read`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    specsIdVersionsVersionResource.addMethod('PUT', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/spec.write`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });

    // Add credentials resource
    const credentialsResource = versionResource.addResource('credentials');
    const credentialsDefaultResource = credentialsResource.addResource(
      'default'
    );
    credentialsDefaultResource.addMethod('GET', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/credentials.read`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });
    credentialsDefaultResource.addMethod('DELETE', integration, {
      authorizationScopes: [
        `https://${CONFIG.api.recordName}.${CONFIG.domainName}/credentials.write`,
        cognito.OAuthScope.COGNITO_ADMIN.scopeName,
      ],
      authorizationType: apigateway.AuthorizationType.COGNITO,
      authorizer: {
        authorizerId: cdk.Fn.ref(authorizer.logicalId),
      },
    });

    // DNS listing
    const zone = route53.PublicHostedZone.fromLookup(this, 'PublicHostedZone', {
      domainName: CONFIG.domainName,
    });
    new route53.ARecord(this, 'NewAliasRecord', {
      zone,
      target: route53.RecordTarget.fromAlias(
        new route53Targets.ApiGateway(api)
      ),
      recordName: CONFIG.api.recordName,
    });
  }
}
