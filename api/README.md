# Package API

API interface for OpenAlchemy packages. Used to manage packages and specs.

## Package Name

Python places constraints on what the name of a package can be, see here:
<https://www.python.org/dev/peps/pep-0426/#name>.

Python also has a concept of a canonical identifier for a package, see here:
<https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>.
Pip uses the canonical id when requesting a package.

The following implementation will be done:

1. packages will be uniquely identified by their canonical name as defined by
   <https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>,
1. packages can have a name that is different to the canonical id which needs
   to comply with <https://www.python.org/dev/peps/pep-0426/#name> but the
   characters are retained for storage (e.g. case sensitivity is retained).

The `id` of a spec will be the canonical id. The name of the spec will be a
package name compliant value.

## Package Version

Python places constraints on what the version of a package can be, see here:
<https://www.python.org/dev/peps/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions>.
It can be checked using:
<https://packaging.pypa.io/en/latest/version.html#packaging.version.Version>.

## Storage Facade

The storage facade abstracts the interface to store specs on S3. It has the
following use cases:

- create or update a spec,
- get the value of a spec,
- delete a spec and
- get all available versions of a spec.

### Create or Update a Spec

Creates or updates the value of a spec.

Input:

- `user`: the user to create the spec for,
- `name`: the display name of a spec,
- `version`: the version of the spec,
- `value`: the value of the spec.

Output:

Algorithm:

1. calculate the `id` of the spec using
   <https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>,
1. map the `user`, `id` and `version` to the object `key` using
   `{user}/{id}/{version}-spec.json` and
1. write the `value` to the storage layer at the `key`.

### Get the Value of a Spec

Retrieves the value of a spec.

Input:

- `user` and,
- `name`.

Output:

- `value`.

Algorithm:

1. calculate the `id` of the spec using
   <https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>,
1. map the `user`, `id` and `version` to the object `key` using
   `{user}/{id}/{version}-spec.json` and
1. retrieve the `value` from the storage layer at the `key`.

### Delete Spec

Deletes all versions of the spec and any other related items.

Input:

- `user` and,
- `name`.

Output:

Algorithm:

1. calculate the `id` of the spec using
   <https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>,
1. map the `user` and `id` to a prefix using `{user}/{id}/` and
1. delete all objects that match.

### Get Spec Versions

Retrieves all versions available for the spec.

Input:

- `user` and,
- `name`.

Output:

- a list of `version` available for the spec.

Algorithm:

1. calculate the `id` of the spec using
   <https://packaging.pypa.io/en/latest/utils.html#packaging.utils.canonicalize_name>,
1. map the `user` and `id` to a prefix using `{user}/{id}/`,
1. define a suffix of `-spec.json`,
1. retrieve all `key`s that match the prefix and suffix and
1. retrieve the `version` from the `key` by removing the prefix and suffix.

## Endpoints

### `/credentials/default

#### Get

Retrieve the default credential from the database for the user.

Algorithm:

1. check whether credentials with the id of `default` exist in the database,
1. if the credentials exist, use the security module to calculate the
   `secret_key` and return the credentials,
1. use the security module to create credentials,
1. store the credentials in the database and
1. return the credentials.

#### Delete

Delete the default credential from the database for the user.

Algorithm:

1. delete the credentials from the database.
