const domainName = 'openalchemy.io';

export const CONFIG = {
  domainName,
  api: {
    recordName: 'package.api',
    throttlingBurstLimit: 200,
    throttlingRateLimit: 100,
    additionalAllowHeaders: ['x-language'],
  },
  web: {
    recordName: 'package',
  },
  storage: {
    bucketName: `package-storage.${domainName}`,
    queueName: 'package-storage-object-created-json',
  },
  database: {
    tableName: 'package-storage',
    indexName: 'specIdUpdatedAt',
  },
};
