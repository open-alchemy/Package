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

## Salt

A salt is a random string generated using
<https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe>
.

## Public Key

The public key is a hash based on the `sub` of the user and a salt. The
following algorithm is used:

1. create a message by combining the `sub` and a random salt created using
   <https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe>,
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
<https://docs.python.org/3/library/hashlib.html#hashlib.scrypt>
where:

- `password` is the `secret_key`,
- `salt` is the credential salt,
- `n` is `2 ** 14`,
- `r` is 8 and
- `p` is 1.
