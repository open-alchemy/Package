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
import { TestStack } from '../lib/test-stack';
import { OLD_ENVIRONMENT } from '../lib/environment';

const env = {
  account: OLD_ENVIRONMENT.AWS_ACCOUNT,
  region: OLD_ENVIRONMENT.AWS_DEFAULT_REGION,
};

const app = new cdk.App();

if (OLD_ENVIRONMENT.STACK === 'PackageApiStack') {
  new ApiStack(app, 'PackageApiStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageWebStack') {
  new WebStack(app, 'PackageWebStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageBuildStack') {
  new BuildStack(app, 'PackageBuildStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageDatabaseStack') {
  new DatabaseStack(app, 'PackageDatabaseStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageSecurityStack') {
  new SecurityStack(app, 'PackageSecurityStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageIndexStack') {
  new IndexStack(app, 'PackageIndexStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageStorageStack') {
  new StorageStack(app, 'PackageStorageStack', { env });
}
if (OLD_ENVIRONMENT.STACK === 'PackageTestStack') {
  new TestStack(app, 'PackageTestStack', { env });
}
