# Package Index

The package index customers use to install their package. For example, using
the following command:

<!-- markdownlint-disable line-length -->

```bash
pip install --index-url https://{public_key}:{secret_key}@index.package.openalchemy.io --extra-index-url https://pypi.org/simple "{specId}=={version}"
```

<!-- markdownlint-enable line-length -->

## Components

- storage: the packages are stored in an S3 bucket under the key
  `{sub}/{specId}/{specId}-{version}.tar.gz`,
- distribution: the packages are distributed using CloudFront and
- function: authenticates and translates the HTTP request issued by `pip` to
  the key to retrieve from S3.

### Function

#### Input

The function receives requests from CloudFront, examples are below where only
the relevant pieces are shown.

##### List Request

The first step is that pip issues a request to list all available versions of a
package:

```python
{
    "Records": [
        {
            "cf": {
                "request": {
                    "headers": {
                        "authorization": [
                            {"key": "Authorization", "value": "Basic <token>"}
                        ]
                    },
                    "uri": "/{specId}/",
                }
            }
        }
    ]
}
```

#### Output

Either unauthorized or the path to retrieve from S3 by returning, for example:

#### Algorithm

1. extracts the `public_key` and `secret_key` from the request,
1. use `open-alchemy.package-database` to retrieve the `sub`, `salt` and
   `secret_key_hash` based on the `public_key`,
1. return unauthorized if the user retrieval fails,
1. use `open-alchemy.package-security` to calculate the `secret_key_hash` based
   on the `secret_key` and `salt`,
1. use `open-alchemy.package-security` to compare the `secret_key_hash`
   retrieved from the database and calculated based on the received
   `secret_key`,
1. return unauthorized of the comparison fails,
1. if it is a list request, retrieve the versions of the requested spec from
   the database, construct the response and return it and
1. rewrite the request path to include `sub`.

## Infrastructure

The CloudFormation stack is defined here:
[../infrastructure/lib/index-stack.ts](../infrastructure/lib/index-stack.ts).

## CI-CD

The workflow for the CI-CD is defined here:
[../.github/workflows/ci-cd-index.yaml](../.github/workflows/ci-cd-index.yaml).

## Production Tests

The tests against the deployed index service are defined here:
[../test/index/](../test/index/).

The workflow that periodically executes the tests is defined here:
[../.github/workflows/production-test-index.yaml](../.github/workflows/production-test-index.yaml).
