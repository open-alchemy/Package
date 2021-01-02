"""Helper for securityfor package service."""

import base64
import hashlib
import hmac
import secrets

from . import config, types


def _generate_salt() -> types.TSalt:
    """Generate the salt."""
    return secrets.token_bytes()


def _generate_public_key(*, sub: types.TSub) -> types.TPublicKey:
    """Generate the public key."""
    sha256 = hashlib.sha256()
    sha256.update(sub.encode())

    random_token = _generate_salt()
    sha256.update(random_token)

    raw_public_key = sha256.digest()
    b64_raw_public_key = base64.urlsafe_b64encode(raw_public_key)

    return f"pk_{b64_raw_public_key.decode()}"


def _generate_secret_key(*, sub: types.TSub, salt: types.TSalt) -> types.TSecretKey:
    """Generate the secret key."""
    service_secret = config.get().service_secret

    sha256 = hashlib.sha256()
    sha256.update(sub.encode())
    sha256.update(salt)
    sha256.update(service_secret)

    raw_secret_key = sha256.digest()
    b64_raw_secret_key = base64.urlsafe_b64encode(raw_secret_key)

    return f"sk_{b64_raw_secret_key.decode()}"


def calculate_secret_key_hash(
    *, secret_key: types.TSecretKey, salt: types.TSalt
) -> types.TSecretKeyHash:
    """Generate the secret key hash."""
    return hashlib.scrypt(secret_key.encode(), salt=salt, n=2 ** 14, r=9, p=1)


def create(*, sub: types.TSub) -> types.Credentials:
    """
    Create credentials for the user.

    Args:
        sub: Unique identifier for the user.

    Returns:
        Credentials for the user.

    """
    public_key = _generate_public_key(sub=sub)
    salt = _generate_salt()
    secret_key = _generate_secret_key(sub=sub, salt=salt)
    secret_key_hash = calculate_secret_key_hash(secret_key=secret_key, salt=salt)

    return types.Credentials(
        public_key=public_key,
        secret_key=secret_key,
        secret_key_hash=secret_key_hash,
        salt=salt,
    )


def retrieve(*, sub: types.TSub, salt: types.TSalt) -> types.TSecretKey:
    """
    Retrieve the secret from existing credentials.

    Args:
        sub: Unique identifier for the customer.
        salt: Random value used to generate the credentials.

    Returns:
        The secret key for the credentials.

    """
    return _generate_secret_key(sub=sub, salt=salt)


def compare_secret_key_hashes(
    left: types.TSecretKeyHash, right: types.TSecretKeyHash
) -> bool:
    """
    Safe comparison of two secret key hashes, computes left == right.

    Args:
        left: The left side of the comparison.
        right: The right side of the comparison.

    Returns:
        Whether left == right.

    """
    return hmac.compare_digest(left, right)
