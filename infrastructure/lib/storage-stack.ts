import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as cloudfront from '@aws-cdk/aws-cloudfront';

import { CONFIG } from './config';

export class StorageStack extends cdk.Stack {
  originAccessIdentity: cloudfront.OriginAccessIdentity;
  bucket: s3.Bucket;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Storage for the packages
    this.bucket = new s3.Bucket(this, 'PackageBucket', {
      bucketName: CONFIG.storage.newBucketName,
    });

    // Grant package index distribution access to the bucket
    this.originAccessIdentity = new cloudfront.OriginAccessIdentity(
      this,
      'AccessIdentity'
    );
    this.bucket.grantRead(this.originAccessIdentity);
  }
}
