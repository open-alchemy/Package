"""Types for security."""

import dataclasses

TSub = str
TPublicKey = str
TSecretKey = str
TSecretKeyHash = bytes
TSalt = bytes


@dataclasses.dataclass
class Credentials:
    """
    Credentials for a user.

    Attrs:
        public_key: Public identifier for the credentials.
        secret_key: Secret value for the key.
        salt: Random value used to generate the secret key.
        secret_key_hash: Derived from the secret key that is safe to store.

    """

    public_key: TPublicKey
    secret_key: TSecretKey
    secret_key_hash: TSecretKeyHash
    salt: TSalt
