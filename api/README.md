# Package API

API interface for OpenAlchemy packages. Used to manage packages and specs.

## Database

The database has a facade that is defined in the following file:
[library/facades/database](library/facades/database). It exposes a series of
functions that enable the API to personalize responses.

### Tables

#### Credentials Table

Stores credentials for a user. The following access patterns are expected:

- list available credentials for a user,
- retrieve or create particular credentials for a user,
- check that a public and secret key combination exists and retrieve the `sub`
  for it,
- delete particular credentials for a user and
- delete all credentials for a user.

##### List Credentials

List all available credentials for a user.

Input:

- `sub`: unique identifier for the user

Output:

- list of dictionaries with the `credential_id` key.

Algorithm:

1. use the `sub` partition key to retrieve all credentials for the user and
1. map the items to a dictionary.

##### Retrieve or Create Credentials

If the credential with the id exists, return it. Otherwise, create it.

Input:

- `sub`: unique identifier for the user and
- `credential_id`: unique identifier for the credential.

Output:

- `public_key`: public unique identifier for the key and
- `secret_key`: secret value.

Algorithm:

1. Use the `sub` partition key and `credential_id` sort key to check whether
   an entry exists,
1. if an entry exists, retrieve the `public_key` and `salt` and use the
   credential helper to calculate the `secret_key` and return,
1. use the credential helper to generate the `public_key`, `secret_key`, `salt`
   and `secret_key_hash`,
1. store the `public_key`, `salt` and `secret_key_hash` against `sub` and
   `credential_id` and
1. return the `public_key` and `secret_key`.

##### Check Credential and Retrieve User

Check that a credential is valid and retrieve the `sub` associated with the
credential.

Input:

- `public_key` and
- `secret_key`.

Output:

- `sub`.

Algorithm:

1. calculate the `secret_key_hash` using the credential helper,
1. check whether an entry exists using the `public_key` partition key and
   `secret_key_hash` sort key for the `publicSecretKey` global secondary index
1. if it does not exist, return `None` and
1. retrieve and return the `sub`.

##### Delete a Credential for a User

Input:

- `sub` and
- `credential_id`.

Output:

Algorithm:

1. Delete all entries for `sub` and `credential_id`.

##### Delete All Credentials for a User

Input:

- `sub`.

Output:

Algorithm:

1. Delete all entries for `sub`.

##### Properties

- `sub`: A string that is the partition key of the table.
- `credential_id`: A string that is the sort key of the table.
- `public_key`: A string that is the partition key of the `publicSecretKey`
  global secondary index.
- `secret_key_hash`: A string that is the sort key of the `publicSecretKey`
  global secondary index.
- `salt`: A byte.

## Helpers

### Credentials Helper

Performs calculations for creating pubic and secret keys. A credential is made
up of a public and secret key, a salt and a hash of the secret key that is safe
to store.

#### Create

Create a new credential.

Input:

- `sub`: unique identifier for the user and
- `service_secret`: a secret for the service.

Output:

- `public_key`: a unique public identifier for the key,
- `secret_key`: a secret key for the public key,
- `salt`: a random value used to create the credential and
- `secret_key_hash`: a value derived from the secret key that is safe to store.

#### Retrieve Secret

Re-calculates the secret key based on known values.

Input:

- `sub`,
- `service_secret` and
- `salt`.

Output:

- `secret_key`.

#### Calculate Secret Hash

Calculate the secret key has for a secret.

Input:

- `secret_key` and
- `salt`.

Output:

- `secret_key_hash`.

#### Salt

A salt is a random string generated using
<https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe>
.

#### Public Key

The public key is a hash based on the `sub` of the user and a salt. The
following algorithm is used:

1. create a message by combining the `sub` and `salt`,
1. digest the message using `sha256` using
   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>
   and
1. convert to string using
   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>
   decoding and and pre-pending it with `pk_`.

#### Secret Key

The secret key is a hash based on the `sub`, same salt as the public key and a
secret associated with the package service. The following algorithm is used:

1. create a message by combining `sub`, `salt` and the package service secret,
1. digest the message using `sha256` using
   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>
   and
1. convert to string using
   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>
   decoding and and pre-pending it with `sk_`.

#### Secret Key Hash

The secret key itself is not stored but a value that is derived from it but
hard to reverse is. The following function is used to calculate it:
<https://docs.python.org/3/library/hashlib.html#hashlib.scrypt>
where:

- `password` is the `secret_key`,
- `salt` is the credential salt,
- `n` is `2 ** 14`,
- `r` is 8 and
- `p` is 1.

## Endpoints

### `/credentials/default

#### Get

Retrieve the default credential from the database for the user.

#### Delete

Delete the default credential from the database for the user.
