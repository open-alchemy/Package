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
