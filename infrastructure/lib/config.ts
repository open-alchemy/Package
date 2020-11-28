const domainName = 'openalchemy.io';

export const CONFIG = {
  domainName,
  api: {
    recordName: 'package.api',
    throttlingBurstLimit: 200,
    throttlingRateLimit: 100,
    additionalAllowHeaders: ['x-language'],
    resources: {
      version: 'v1',
      ui: 'ui',
      openapi: 'openapi.json',
      specs: {
        pathPart: 'specs',
        methods: {
          put: {
            authorizationScopes: [
              'https://package.api.openalchemy.io/spec.write',
            ],
          },
        },
      },
    },
  },
  storage: {
    bucketName: `package-storage.${domainName}`,
  },
};
