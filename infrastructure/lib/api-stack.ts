import * as fs from 'fs';
import * as crypto from 'crypto';

import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as codedeploy from '@aws-cdk/aws-codedeploy';
import * as route53 from '@aws-cdk/aws-route53';
import * as route53Targets from '@aws-cdk/aws-route53-targets';
import * as certificatemanager from '@aws-cdk/aws-certificatemanager';
import * as iam from '@aws-cdk/aws-iam';
import * as s3 from '@aws-cdk/aws-s3';

import { ENVIRONMENT } from './environment';
import { CONFIG } from './config';

export class ApiStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Storage for the packages
    const bucket = new s3.Bucket(this, 'PackageBucket', {
      bucketName: CONFIG.storage.bucketName,
    });

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
        SPECS_BUCKET_NAME: CONFIG.storage.bucketName,
      },
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
    const integration = new apigateway.LambdaIntegration(alias);

    // Certificate
    const certificateArn = ENVIRONMENT.AWS_OPEN_ALCHEMY_API_CERTIFICATE_ARN;
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
    // const authorizer = new apigateway.CfnAuthorizer(this, 'Authorizer', {
    //   restApiId: api.restApiId,
    //   type: apigateway.AuthorizationType.COGNITO,
    //   identitySource: apigateway.IdentitySource.header('Authorization'),
    //   providerArns: [ENVIRONMENT.AWS_IDENTITY_PROVIDER_ARN],
    //   name: 'PackageAuth',
    // });

    // // Protect resources with cognito
    // const versionResource = api.root.addResource(CONFIG.api.resources.version);
    // const specsResource = versionResource.addResource(
    //   CONFIG.api.resources.specs.pathPart
    // );
    // specsResource.addMethod('PUT', integration, {
    //   authorizationType: apigateway.AuthorizationType.COGNITO,
    //   authorizationScopes:
    //     CONFIG.api.resources.specs.methods.put.authorizationScopes,
    //   authorizer: {
    //     authorizerId: authorizer.logicalId,
    //   },
    // });

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
