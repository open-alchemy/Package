# Security

Performs calculations for creating pubic and secret keys. A credential is made
up of a public and secret key, a salt and a hash of the secret key that is safe
to store.

## Service Secret

For certain operations, such as the creation of secret keys, a service secret
is retrieved which required access to AWS secrets manager.

## Create

Create a new credential.

Input:

- `sub`: unique identifier for the user.

Output:

- `public_key`: a unique public identifier for the key,
- `secret_key`: a secret key for the public key,
- `salt`: a random value used to create the credential and
- `secret_key_hash`: a value derived from the secret key that is safe to store.

## Retrieve Secret

Re-calculates the secret key based on known values.

Input:

- `sub` and
- `salt`.

Output:

- `secret_key`.

## Calculate Secret Hash

Calculate the secret key has for a secret.

Input:

- `secret_key` and
- `salt`.

Output:

- `secret_key_hash`.

## Compare Secret Hashes

Safely compare two secret key hashes

Input:

- `left`: a `secret_key_hash` and
- `right`: a `secret_key_hash`.

Output:

- Whether `left` == `right`.

Algorithm:

1. use <https://docs.python.org/3/library/hmac.html#hmac.compare_digest> to
   compare the secret key hashes.

## Salt

A salt is a random string generated using
<https://docs.python.org/3/library/secrets.html#secrets.token_bytes>.

## Public Key

The public key is a hash based on the `sub` of the user and a salt. The
following algorithm is used:

1. create a message by combining the `sub` and a random salt created using
   <https://docs.python.org/3/library/secrets.html#secrets.token_bytes>,
1. digest the message using `sha256` using
   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>
   and
1. convert to string using
   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>
   decoding and and pre-pending it with `pk_`.

## Secret Key

The secret key is a hash based on the `sub`, `salt` and a secret associated
with the service. The following algorithm is used:

1. retrieve the service secret,
1. create a message by combining `sub`, `salt` and the service secret,
1. digest the message using `sha256` using
   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>
   and
1. convert to string using
   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>
   decoding and and pre-pending it with `sk_`.

## Secret Key Hash

The secret key itself is not stored but a value that is derived from it but
hard to reverse is. The following function is used to calculate it:
<https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac>
where:

- `hash_name` is `sha256`,
- `password` is the `secret_key`,
- `salt` is the credential salt,
- `iterations` is 10k.

## CI-CD

The workflow is defined here:
[../.github/workflows/ci-cd-security.yaml](../.github/workflows/ci-cd-security.yaml).

There are a few groups of jobs in the CI-CD:

- `test`: runs the tests for the package in supported python versions,
- `build`: builds the security package,
- `deploy`: deploys security infrastructure to AWS,
- `release-required`: determines whether a release to PyPI is required and
- `release`: a combination of deploying to test and production PyPI and
  executing tests on the published packages

### `test`

Executes the tests defined at [tests](tests).

### `build`

Builds the security package defined at [.](.).

### `release-required`

Has 2 outputs:

- `result`: whether a release to PyPI is required based on the latest released
  version and the version configured in the project and
- `project-version`: the version configured in the code base.

### `deploy`

Deploys the CloudFormation stack for the security defined at
[../infrastructure/lib/security-stack.ts](../infrastructure/lib/security-stack.ts).

### `release`

If the `result` output from `release-required` is true, the package is deployed
to both test and production PyPI.

Irrespective of whether the release was executed, the version of the package
defined in the code base is installed from both test and production PyPI and
the tests defined at [../test/security/tests](../test/security/tests) are
executed against the deployed infrastructure on AWS.

## Periodic Production Tests

The workflow is defined here:
[../.github/workflows/production-test-security.yaml](../.github/workflows/production-test-security.yaml).

Executes the tests defined at [../test/security/tests](../test/security/tests)
against a configured version of the package and against the currently deployed
infrastructure on AWS.

## Pytest Plugin

A pytest plugin is made available to make testing easier. It is defined at
[open_alchemy/package_security/pytest_plugin.py](open_alchemy/package_security/pytest_plugin.py).

### Fixtures

All fixtures that have an effect but yield `None` are prefixed with `_` so that
tools like pylint do not complain about unused arguments for test functions.

#### `service_secret`

Configures the package to use a dummy service secret and yields it.

#### `_service_secret`

The same as `service_secret` except that it is prefix with a leading `_`.
