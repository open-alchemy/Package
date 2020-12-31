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
    topicName: 'package-storage-object-created-json',
  },
  database: {
    storageTableName: 'package-storage',
    storageIndexName: 'specIdUpdatedAt',
  },
};
