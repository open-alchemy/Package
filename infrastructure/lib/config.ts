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
      uiSubResources: [
        'swagger-ui-standalone-preset.js',
        'swagger-ui-bundle.js',
        'swagger-ui.css',
        'favicon-32x32.png',
        'favicon-16x16.png',
      ],
      specs: {
        pathPart: 'specs',
        specsId: {
          pathPart: '{spec_id}',
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
  },
  storage: {
    bucketName: `package-storage.${domainName}`,
  },
};
