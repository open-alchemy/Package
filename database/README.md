# Database

The database has a facade exposes a series of functions that enable services to
personalize responses.

## Tables

### Specs

Stores information about the specs for a user. The following access patterns
are expected:

- count the number of models for a user,
- create or update a spec record for a user,
- get the latest version of a spec for a user,
- list all specs for a user,
- delete a particular spec for a user and
- list all versions of a spec for a user.

#### Count Models for a User

Counts the number of models a user has defined.

Input:

- `sub`: unique identifier for the user.

Output:

- The sum of the latest `model_count` for each spec for the user.

Algorithm:

1. filter by the `sub` and `updated_at_spec_id` to start with `latest#` and
1. sum over the `model_count` of each record.

#### Create or Update a Spec

Input:

- `sub`,
- `spec_id`: unique identifier for the spec,
- `version`: the version of the spec,
- `model_count`: the number of models in the spec,
- `title` (_optional_): the title of the spec and
- `description` (_optional_): the description of the spec.

Output:

Algorithm:

1. calculate `updated_at` based on he current EPOCH time using
   <https://docs.python.org/3/library/time.html#time.time>
   and convert to an integer represented as a string,
1. calculate the value for `updated_at_spec_id` by joining a zero padded
   `updated_at` to 20 characters and `spec_id` with a `#` and for
   `spec_id_updated_at` by joining `spec_id` and
   `updated_at` with a `#`,
1. save the item to the database,
1. create another item but use `latest` for `updated_at` when generating
   `updated_at_spec_id` and `spec_id_updated_at`

#### Get Latest Spec Version

Retrieve the latest version of a spec.

Input:

- `sub` and
- `spec_id`.

Output:

- The latest `version` of the spec.

Algorithm:

1. Retrieve the item using the `sub` partition key and `updated_at_spec_id`
   sort key equal to `latest#<spec_id>` and
1. return the version of the item.

#### List Specs

Returns information about all the available specs for a user.

Input:

- `sub`.

Output:

- A list of dictionaries with the `spec_id`, `updated_at`, `version`,
  `model_count` and `title` and `description` if they are defined.

Algorithm:

1. filter items using the `sub` partition key and `updated_at_spec_id` starting
   with `latest#` and
1. convert the items to dictionaries.

#### Delete Spec

Delete a particular spec for a user.

Input:

- `sub` and
- `spec_id`.

Output:

Algorithm:

1. query the `spec_id_updated_at_index` local secondary index by filtering for
   `sub` and `spec_id_updated_at` starting with `<spec_id>#` and
1. delete all returned items.

#### List Spec Versions

Returns information about all the available versions of a spec for a user.

Input:

- `sub` and
- `spec_id`.

Output:

- A list of dictionaries with the `spec_id`, `updated_at`, `version`,
  `model_count` and `title` and `description` if they are defined.

Algorithm:

1. query the `spec_id_updated_at_index` local secondary index by filtering for
   `sub` and `spec_id_updated_at` starting with `<spec_id>#`,
1. filter out any items where `updated_at_spec_id` starts with `latest#` and
1. convert the items to dictionaries.

#### Spec Properties

- `sub`: A string that is the partition key of the table.
- `spec_id`: A string.
- `updated_at`: A string.
- `version`: A string.
- `title`: An optional string.
- `description`: An optional string.
- `model_count` A number.
- `updated_at_spec_id`: A string that is the sort key of the table.
- `spec_id_updated_at`: A string that is the sort key of the
  `specIdUpdatedAt` local secondary index of the table.

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
   `publicKeySecretKeyHash` global secondary index
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
- `public_key`: A string that is the partition key of the `publicSecretKey`
  global secondary index.
- `secret_key_hash`: Bytes.
- `salt`: Bytes.
