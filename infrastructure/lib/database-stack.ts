import * as cdk from '@aws-cdk/core';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

import { CONFIG } from './config';

export class DatabaseStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Shared properties
    const sub = { name: 'sub', type: dynamodb.AttributeType.STRING };

    // // Database for the specs
    // const specsTable = new dynamodb.Table(this, 'SpecsTable', {
    //   partitionKey: { ...sub },
    //   tableName: CONFIG.database.specs.tableName,
    //   sortKey: {
    //     name: 'updated_at_id',
    //     type: dynamodb.AttributeType.STRING,
    //   },
    //   billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    // });
    // specsTable.addLocalSecondaryIndex({
    //   indexName: CONFIG.database.specs.localSecondaryIndexName,
    //   sortKey: {
    //     name: 'id_updated_at',
    //     type: dynamodb.AttributeType.STRING,
    //   },
    //   projectionType: dynamodb.ProjectionType.ALL,
    // });

    // Database for the credentials
    const credentialsTable = new dynamodb.Table(this, 'CredentialsTable', {
      partitionKey: { ...sub },
      tableName: CONFIG.database.credentials.tableName,
      sortKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });
    credentialsTable.addGlobalSecondaryIndex({
      indexName: CONFIG.database.credentials.globalSecondaryIndexName,
      partitionKey: { name: 'public_key', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });
  }
}
