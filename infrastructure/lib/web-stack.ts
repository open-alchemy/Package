import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as cloudfrontOrigins from '@aws-cdk/aws-cloudfront-origins';
import * as s3Deployment from '@aws-cdk/aws-s3-deployment';
import * as certificatemanager from '@aws-cdk/aws-certificatemanager';
import * as route53 from '@aws-cdk/aws-route53';
import * as route53Targets from '@aws-cdk/aws-route53-targets';

import { CONFIG } from './config';
import { ENVIRONMENT } from './environment';

export class WebStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    const defaultObject = 'index.html';
    const bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: `${CONFIG.web.recordName}.${CONFIG.domainName}`,
    });

    // Certificate
    const certificateArn = ENVIRONMENT.AWS_OPEN_ALCHEMY_CERTIFICATE_ARN;
    const certificate = certificatemanager.Certificate.fromCertificateArn(
      this,
      'Certificate',
      certificateArn
    );

    // CloudFront
    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new cloudfrontOrigins.S3Origin(bucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      domainNames: [`${CONFIG.web.recordName}.${CONFIG.domainName}`],
      certificate,
      defaultRootObject: defaultObject,
      errorResponses: [
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: `/${defaultObject}`,
        },
      ],
    });

    // Website deployment
    new s3Deployment.BucketDeployment(this, 'BucketDeployment', {
      sources: [s3Deployment.Source.asset('resources/web')],
      destinationBucket: bucket,
      distribution,
      distributionPaths: ['/*'],
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
      recordName: CONFIG.web.recordName,
    });
  }
}
