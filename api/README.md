# Package API

API interface for OpenAlchemy packages. Used to manage packages and specs.

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
