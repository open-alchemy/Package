# Package Build

App that accepts notifications that a new `JSON` file with an OpenAPI spec was
created and creates and uploads Python packages based on that spec alongside
the `JSON` file.

## Input

The application expects 2 pieces of input, the name of a JSON file that was
created in storage and a path where that file can be found on the local disk.

### Name of the JSON file

The application receives a notification that a `JSON` file was created. The
name of the file is:

`{sub}/{specId}/{version}-spec.json`

Where:

- `sub` is a unique identifier for the user,
- `specId` is a unique identifier for the spec and
- `version` is the version of the spec.

### Path to the file

This is expected to be a file that can be read. The package output files will
be generated in the same folder in the `dist` sub directory.

## Generating the packages

OpenAlchemy is used to generate the package. In particular, the `build_json`
interface is used:
<https://openapi-sqlalchemy.readthedocs.io/en/latest/#build-json>

This is how the input to the application is mapped to the arguments of
`build_json`:

- `spec_filename`: the path to the file,
- `package_name`: the `specId`,
- `dist_path`: a folder called `dist` in the same directory as the path to the
  file and
- `format_`: `PackageFormat.SDIST|PackageFormat.WHEEL`.

## Output

The application returns a list of data classes with the following properties:

- `storage_location`: the location where the package needs to be stored and
- `path`: the path where the package can be read from the local disk.

## AWS

When hosted on AWS, the notifications are delivered via SNS to a lambda
function in the `event` argument. An example of the notification (with only the
important components) is:

```python
{
    'Records': [
        {
            'Sns': {
                'Message': (
                    '{"Records":[{"s3":{'
                    '"bucket":{"name":"package-storage.openalchemy.io"},'
                    '"object":{"key":"<file name>"}'
                    '}}]}'
                )
            }
        }
    ]
}
```

Note that, in the above example, the object key is URL encoded (e.g. a `+`
instead of a space character).

### Setup

The first step is that a folder is created in `tmp` called `build` is deleted
if it exists and then created. This is to ensure that no data is leaked from
any previous invocations if a lambda container is re-used.

### JSON spec retrieval

The spec is retrieved from s3 using
<https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file>
where `Bucket` and `Key` is retrieved from the SNS notification and the
`Filename` is set to `tmp/build/spec.json`.

### Calling the Application

The object key, after URL decoding, is passed as the name of the JSON file and
the filename is passed as the filename used to retrieve the spec from S3.

### Uploading the generated files

All generated files are uploaded to S3 using
<https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file>
where `Bucket` is retrieved from the SNS notification and the `Key` and
`Filename` are read from the application output.

### Check for spec deletion

After the upload is complete, a check is performed whether the spec still exists
on S3. If not, the package files are also deleted. This is to avoid retaining
package files when the spec is been deleted.

The check is performed using
<https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2>
where `Bucket` is taken from the SNS notification and the `Prefix` is set
to the object key from the SNS notification.

If an empty result is returned, then the package files are deleted using:
<https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_objects>
where `Bucket` is taken from the SNS notification and `Delete` is built using
the application output.

### Cleanup

To avoid leaking data between invocations, the `build` folder in `tmp` is
deleted.

## Infrastructure

The CloudFormation stack is defined here:
[../infrastructure/lib/build-stack.ts](../infrastructure/lib/build-stack.ts).

## CI-CD

The workflow for the CI-CD is defined here:
[../.github/workflows/ci-cd-build.yaml](../.github/workflows/ci-cd-build.yaml).

## Production Tests

The production tests are shared with the index service defined here:
[../build/](../build/).

The tests against the deployed build service are defined here:
[../test/index/](../test/index/).

The workflow that periodically executes the tests is defined here:
[../.github/workflows/production-test-index.yaml](../.github/workflows/production-test-index.yaml).
