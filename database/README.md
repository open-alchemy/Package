# Database

The database has a facade exposes a series of functions that enable services to
personalize responses.

## Interface

The interface for the database is defined as the `TDatabase` class here:
[open_alchemy/package_database/types.py](open_alchemy/package_database/types.py)

It can be retrieved using:

```python
from open_alchemy import package_database

database_instance = package_database.get()
```

Note that the `STAGE` environment variable needs to be set. The possible
values are:

- `TEST`: DynamoDB is assumed to be running at <http://localhost:8000>
- `PROD`: a connection is established to the AWS hosted DynamoDB

## Tables

### Specs

Stores information about the specs for a user. The following access patterns
are expected:

- count the number of models for a user,
- create or update a spec record for a user,
- get the latest version of a spec for a user,
- list all specs for a user,
- delete a particular spec for a user,
- list all versions of a spec for a user and
- delete all specs for a user.

#### Count Models for a User

Counts the number of models a user has defined.

Input:

- `sub`: unique identifier for the user.

Output:

- The sum of the latest `model_count` for each spec for the user.

Algorithm:

1. filter by the `sub` and `updated_at_id` to start with `latest#` and
1. sum over the `model_count` of each record.

#### Create or Update a Spec

Input:

- `sub`,
- `id`: unique identifier for the spec,
- `version`: the version of the spec,
- `model_count`: the number of models in the spec,
- `title` (_optional_): the title of the spec and
- `description` (_optional_): the description of the spec.

Output:

Algorithm:

1. calculate `updated_at` based on he current EPOCH time using
   <https://docs.python.org/3/library/time.html#time.time>
   and convert to an integer represented as a string,
1. calculate the value for `updated_at_id` by joining a zero padded
   `updated_at` to 20 characters and `id` with a `#` and for `id_updated_at`
   by joining `id` and `updated_at` with a `#`,
1. save the item to the database,
1. create another item but use `latest` for `updated_at` when generating
   `updated_at_id` and `id_updated_at`

#### Get Latest Spec Version

Retrieve the latest version of a spec.

Input:

- `sub` and
- `id`.

Output:

- The latest `version` of the spec.

Algorithm:

1. Retrieve the item using the `sub` partition key and `updated_at_id` sort key
   equal to `latest#<id>` and
1. return the version of the item.

#### List Specs

Returns information about all the available specs for a user.

Input:

- `sub`.

Output:

- A list of dictionaries with the `id`, `updated_at`, `version`, `model_count`
  and `title` and `description` if they are defined.

Algorithm:

1. filter items using the `sub` partition key and `updated_at_id` starting with
   `latest#` and
1. convert the items to dictionaries.

#### Delete Spec

Delete a particular spec for a user.

Input:

- `sub` and
- `id`.

Output:

Algorithm:

1. query the `id_updated_at_index` local secondary index by filtering for `sub`
   and `id_updated_at` starting with `<id>#` and
1. delete all returned items.

#### List Spec Versions

Returns information about all the available versions of a spec for a user.

Input:

- `sub` and
- `id`.

Output:

- A list of dictionaries with the `id`, `updated_at`, `version`, `model_count`
  and `title` and `description` if they are defined.

Algorithm:

1. query the `id_updated_at_index` local secondary index by filtering for `sub`
   and `id_updated_at` starting with `<id>#`,
1. filter out any items where `updated_at_id` starts with `latest#` and
1. convert the items to dictionaries.

#### Delete All Specs for a User

Input:

- `sub`.

Output:

Algorithm:

1. Delete all entries for `sub`.

#### Spec Properties

- `sub`: A string that is the partition key of the table.
- `id`: A string.
- `updated_at`: A string.
- `version`: A string.
- `title`: An optional string.
- `description`: An optional string.
- `model_count` A number.
- `updated_at_id`: A string that is the sort key of the table.
- `id_updated_at`: A string that is the sort key of the
  `idUpdatedAt` local secondary index of the table.

### Credentials

Stores credentials for a user. The following access patterns are expected:

- list available credentials for a user,
- create or update credentials for a user,
- retrieve particular credentials for a user,
- check that a public and secret key combination exists and retrieve the `sub`
  for it,
- delete particular credentials for a user and
- delete all credentials for a user.

#### List Credentials

List all available credentials for a user.

Input:

- `sub`.

Output:

- list of dictionaries with the `id`, `public_key` and `salt` keys.

Algorithm:

1. use the `sub` partition key to retrieve all credentials for the user and
1. map the items to a dictionary.

#### Create or Update Credentials

Create or update credentials for a user.

Input:

- `sub`: unique identifier for the user,
- `id`: unique identifier for the credentials,
- `public_key`: public identifier for the credentials,
- `secret_key_hash`: a hash of the secret key for the credentials that is safe
  to store,
- `salt`: a random value used to generate the credentials.

Output:

Algorithm:

1. create and store an item based on the input.

#### Retrieve Credentials

If the credential with the id exists, return it. Otherwise, return `None`.

Input:

- `sub`: unique identifier for the user and
- `id`: unique identifier for the credential.

Output:

- `id`,
- `public_key`,
- `salt`.

Algorithm:

1. Use the `sub` partition key and `id` sort key to check whether
   an entry exists,
1. if an entry exists, return the `public_key` and `salt` and
1. return `None`.

#### Retrieve User

Check that the public key exists and retrieve the user and salt for it.

Input:

- `public_key`.

Output:

- `sub`,
- `salt` and
- `secret_key_hash`.

Algorithm:

1. check whether an entry exists using the `public_key` partition key for the
   `publicKey` global secondary index
1. if it does not exist, return `None` and
1. retrieve and return the `sub`, `salt` and `secret_key_hash`.

#### Delete a Credential for a User

Input:

- `sub` and
- `id`.

Output:

Algorithm:

1. Delete all entries for `sub` and `id`.

#### Delete All Credentials for a User

Input:

- `sub`.

Output:

Algorithm:

1. Delete all entries for `sub`.

#### Credentials Properties

- `sub`: A string that is the partition key of the table.
- `id`: A string that is the sort key of the table.
- `public_key`: A string that is the partition key of the `publicKey`
  global secondary index.
- `secret_key_hash`: Bytes.
- `salt`: Bytes.

## CI-CD

The workflow is defined here:
[../.github/workflows/ci-cd-database.yaml](../.github/workflows/ci-cd-database.yaml)

There are a few groups of jobs in the CI-CD:

- `test`: runs the tests for the package in supported python versions,
- `build`: builds the database package,
- `release-required`: determines whether a release to PyPI is required,
- `deploy`: deploys database infrastructure to AWS and
- `release`: a combination of deploying to test and production PyPI and
  executing tests on the published packages

### `test`

Executes the tests defined at [tests](tests).

### `build`

Builds the database package defined at [.](.).

### `release-required`

Has 2 outputs:

- `result`: whether a release to PyPI is required based on the latest released
  version and the version configured in the project and
- `project-version`: the version configured in the code base.

### `deploy`

Deploys the CloudFormation stack for the database defined at
[../infrastructure/lib/database-stack.ts](../infrastructure/lib/database-stack.ts)
.

### `release`

If the `result` output from `release-required` is true, the package is deployed
to both test and production PyPI.

Irrespective of whether the release was executed, the version of the package
defined in the code base is installed from both test and production PyPI and
the tests defined at [../test/database/tests](../test/database/tests) are
executed against the deployed infrastructure on AWS.

## Periodic Production Tests

The workflow is defined here:
[../.github/workflows/production-test-database.yaml](../.github/workflows/production-test-database.yaml)
.

Executes the tests defined at [../test/database/tests](../test/database/tests)
against a configured version of the package and against the currently deployed
infrastructure on AWS.
