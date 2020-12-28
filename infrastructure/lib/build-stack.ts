import * as fs from 'fs';
import * as crypto from 'crypto';

import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as codedeploy from '@aws-cdk/aws-codedeploy';

import { CONFIG } from './config';

export class BuildStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // Lambda function
    const deploymentPackage = 'resources/build/deployment-package.zip';
    const deploymentPackageContents = fs.readFileSync(deploymentPackage);
    const deploymentPackageHash = crypto
      .createHash('sha256')
      .update(deploymentPackageContents)
      .digest('hex');
    const func = new lambda.Function(this, 'BuildFunc', {
      functionName: 'package-build-service',
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(deploymentPackage),
      handler: 'app.main',
      environment: {
        STAGE: 'PROD',
        PACKAGE_STORAGE_BUCKET_NAME: CONFIG.storage.bucketName,
      },
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
  }
}
