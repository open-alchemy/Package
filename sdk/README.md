# OpenAlchemy Package SDK

An SDK for interacting with the OpenAlchemy package service.

For API based interactions check here:
<https://package.api.openalchemy.io/v1/ui/>

## Getting Started

To list all available specs:

```typescript
import { specs } from '@open-alchemy/package-sdk';

const allSpecs = await specs.list({ accessToken });
```

To interact with a particular spec:

```typescript
import { spec } from '@open-alchemy/package-sdk';

// Get the value of a spec
const employeeSpec = await spec.get({ accessToken, id: 'employee' });
// Get the value of a particular version of a spec
const employeeSpec = await spec.get({
  accessToken,
  id: 'employee',
  version: 'version 1',
});
// Create or update a spec
await spec.put({
  accessToken,
  id: 'employee',
  specValue: '<an OpenAlchemy OpenAPI Spec>',
});
// Create or update specific version of a spec
await spec.put({
  accessToken,
  id: 'employee',
  specValue: '<an OpenAlchemy OpenAPI Spec>',
  version: 'version 1',
});
// Delete a spec
await spec.delete({ accessToken, id: 'employee' });
// List the versions of a spec
const specVersions = await spec.getVersions({
  accessToken,
  id: 'employee',
});
```
