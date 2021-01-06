import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as sns from '@aws-cdk/aws-sns';
import * as logs from '@aws-cdk/aws-logs';
import * as cloudwatchActions from '@aws-cdk/aws-cloudwatch-actions';
import * as snsSubscriptions from '@aws-cdk/aws-sns-subscriptions';

import { ENVIRONMENT } from './environment';

export class TestStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda function
    const func = new lambda.Function(this, 'Func', {
      functionName: 'test-service',
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromInline(
        'exports.handler = function(event, ctx, cb) { throw ("error"); }'
      ),
      handler: 'index.handler',
      logRetention: logs.RetentionDays.ONE_WEEK,
      timeout: cdk.Duration.seconds(5),
    });
    const alarm = func.metricErrors().createAlarm(this, 'Alarm', {
      threshold: 1,
      evaluationPeriods: 1,
      alarmName: 'test-service-error',
      alarmDescription: 'The test-service lambda function had an error',
    });
    const topic = new sns.Topic(this, 'Topic', {
      displayName: 'test-service-error-alarm',
      topicName: 'test-service-error-alarm',
    });
    topic.addSubscription(
      new snsSubscriptions.EmailSubscription(ENVIRONMENT.alarmEmailAddress)
    );
    alarm.addAlarmAction(new cloudwatchActions.SnsAction(topic));
  }
}
