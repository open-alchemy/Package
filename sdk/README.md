# OpenAlchemy Package SDK

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
await spec.put({
  accessToken,
  id: 'employee',
  specValue: '<an OpenAlchemy OpenAPI Spec>',
});
await spec.delete({ accessToken, id: 'employee' });
const specVersions = await spec.getVersions({
  accessToken,
  id: 'employee',
});
```
