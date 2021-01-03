# OpenAlchemy Package SDK

An SDK for interacting with the OpenAlchemy package service.

For API based interactions check here:
<https://package.api.openalchemy.io/v1/ui/>

## Getting Started

To list all available specs:

```typescript
import { SpecsService } from '@open-alchemy/package-sdk';

const service = new SpecsService();
const allSpecs = await service.list({ accessToken });
```

To interact with a particular spec:

```typescript
import { SpecService } from '@open-alchemy/package-sdk';

const service = new SpecService();
// Get the value of a spec
const employeeSpec = await service.get({ accessToken, id: 'employee' });
// Get the value of a particular version of a spec
const employeeSpec = await service.get({
  accessToken,
  id: 'employee',
  version: 'version 1',
});
// Create or update a spec
await service.put({
  accessToken,
  id: 'employee',
  specValue: '<an OpenAlchemy OpenAPI Spec>',
});
// Create or update specific version of a spec
await service.put({
  accessToken,
  id: 'employee',
  specValue: '<an OpenAlchemy OpenAPI Spec>',
  version: 'version 1',
});
// Delete a spec
await service.delete({ accessToken, id: 'employee' });
// List the versions of a spec
const specVersions = await service.getVersions({
  accessToken,
  id: 'employee',
});
```

To retrieve credentials:

```typescript
import { CredentialsService } from '@open-alchemy/package-sdk';

const service = new CredentialsService();
// Get the value of credentials
const employeeSpec = await service.get({ accessToken });
// Delete credentials
await service.delete({ accessToken });
```
