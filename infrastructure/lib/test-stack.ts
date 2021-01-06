import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as logs from '@aws-cdk/aws-logs';

export class TestStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda function
    new lambda.Function(this, 'Func', {
      functionName: 'test-service',
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromInline(`
def main(event, context):
    raise AssertionError('error')
      `),
      handler: 'index.main',
      logRetention: logs.RetentionDays.ONE_WEEK,
      timeout: cdk.Duration.seconds(5),
    });
  }
}
