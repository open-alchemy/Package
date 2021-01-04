const domainName = 'openalchemy.io';

export const CONFIG = {
  domainName,
  api: {
    recordName: 'package.api',
    throttlingBurstLimit: 200,
    throttlingRateLimit: 100,
    additionalAllowHeaders: ['x-language'],
    defaultCredentialsId: 'default',
  },
  web: {
    recordName: 'package',
  },
  storage: {
    bucketName: `storage.package.${domainName}`,
    topicName: 'storage-package-object-created-json',
    originAccessIdentityParameterName:
      '/Package/Storage/OriginAccessIdentity/Name',
  },
  database: {
    spec: {
      tableName: 'package.specs',
      localSecondaryIndexName: 'idUpdatedAt',
    },
    credentials: {
      tableName: 'package.credentials',
      globalSecondaryIndexName: 'publicKey',
    },
  },
  security: {
    secretName: 'package-service',
  },
  index: {
    recordName: 'index.package',
  },
};
