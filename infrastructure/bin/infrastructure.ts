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
  account: ENVIRONMENT.awsAccount,
  region: ENVIRONMENT.awsDefaultRegion,
};

const app = new cdk.App();

if (ENVIRONMENT.stack === 'PackageApiStack') {
  new ApiStack(app, 'PackageApiStack', { env });
}
if (ENVIRONMENT.stack === 'PackageWebStack') {
  new WebStack(app, 'PackageWebStack', { env });
}
if (ENVIRONMENT.stack === 'PackageBuildStack') {
  new BuildStack(app, 'PackageBuildStack', { env });
}
if (ENVIRONMENT.stack === 'PackageDatabaseStack') {
  new DatabaseStack(app, 'PackageDatabaseStack', { env });
}
if (ENVIRONMENT.stack === 'PackageSecurityStack') {
  new SecurityStack(app, 'PackageSecurityStack', { env });
}
if (ENVIRONMENT.stack === 'PackageIndexStack') {
  new IndexStack(app, 'PackageIndexStack', { env });
}
if (ENVIRONMENT.stack === 'PackageStorageStack') {
  new StorageStack(app, 'PackageStorageStack', { env });
}
