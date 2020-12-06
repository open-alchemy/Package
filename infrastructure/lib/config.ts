const domainName = 'openalchemy.io';

export const CONFIG = {
  domainName,
  api: {
    recordName: 'package.api',
    throttlingBurstLimit: 200,
    throttlingRateLimit: 100,
    additionalAllowHeaders: ['x-language'],
  },
  storage: {
    bucketName: `package-storage.${domainName}`,
  },
  database: {
    tableName: 'package-storage',
    indexName: 'specIdUpdatedAt',
  },
};
