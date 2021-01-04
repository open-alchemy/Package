import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as sns from '@aws-cdk/aws-sns';
import * as ssm from '@aws-cdk/aws-ssm';
import * as s3Notifications from '@aws-cdk/aws-s3-notifications';

import { CONFIG } from './config';

export class StorageStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
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
    new ssm.StringParameter(this, 'Parameter', {
      stringValue: originAccessIdentity.originAccessIdentityName,
      parameterName: CONFIG.storage.originAccessIdentityParameterName,
    });

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
  }
}
