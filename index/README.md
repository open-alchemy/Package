# Package Index

The package index customers use to install their package. For example, using
the following command:

`pip install -f https://{public_key}:{secret_key}@index.package.openalchemy.io "{specId}=={version}"`

## Components

- storage: the packages are stored in an S3 bucket under the key
  `{sub}/{specId}/{specId}-{version}.tar.gz`,
- distribution: the packages are distributed using CloudFront and
- function: authenticates and translates the HTTP request issued by `pip` to
  the key to retrieve from S3.

### Function

Input:
The function receives requests from CloudFront, for example:

Output:
Either unauthorized or the path to retrieve from S3 by returning, for example:

Algorithm:

1. extracts the `public_key` and `secret_key` from the request,
1. use `open-alchemy.package-database` to retrieve the `sub`, `salt` and
   `secret_key_hash` based on the `public_key`,
1. return unauthorized if the user retrieval fails,
1. use `open-alchemy.package-security` to calculate the `secret_key_hash` based
   on the `secret_key` and `salt`,
1. use `open-alchemy.package-security` to compare the `secret_key_hash`
   retrieved from the database and calculated based on the received
   `secret_key`,
1. return unauthorized of the comparison fails and
1. calculate and return the object key/ path to list keys for based on the
   request.
