#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';

import { ApiStack } from '../lib/api-stack';
import { WebStack } from '../lib/web-stack';
import { BuildStack } from '../lib/build-stack';
import { DatabaseStack } from '../lib/database-stack';
import { SecurityStack } from '../lib/security-stack';
import { IndexStack } from '../lib/index-stack';
import { StorageStack } from '../lib/storage-stack';
import { ENVIRONMENT } from '../lib/environment';

const env = {
  account: ENVIRONMENT.AWS_ACCOUNT,
  region: ENVIRONMENT.AWS_DEFAULT_REGION,
};

const app = new cdk.App();

const storageStack = new StorageStack(app, 'PackageStorageStack', { env });
if (ENVIRONMENT.STACK === 'PackageApiStack') {
  new ApiStack(app, 'PackageApiStack', { env }, storageStack.bucket);
}
if (ENVIRONMENT.STACK === 'PackageWebStack') {
  new WebStack(app, 'PackageWebStack', { env });
}
if (ENVIRONMENT.STACK === 'PackageBuildStack') {
  new BuildStack(app, 'PackageBuildStack', { env });
}
if (ENVIRONMENT.STACK === 'PackageDatabaseStack') {
  new DatabaseStack(app, 'PackageDatabaseStack', { env });
}
if (ENVIRONMENT.STACK === 'PackageSecurityStack') {
  new SecurityStack(app, 'PackageSecurityStack', { env });
}
if (ENVIRONMENT.STACK === 'PackageIndexStack') {
  new IndexStack(app, 'PackageIndexStack', { env });
}
