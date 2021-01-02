import * as cdk from '@aws-cdk/core';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';

import { CONFIG } from './config';

export class SecurityStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Service secret
    new secretsmanager.Secret(this, 'Secret', {
      secretName: CONFIG.security.secretName,
    });
  }
}
