"""Database production tests."""

from open_alchemy import package_security


def test_security():
    """
    GIVEN sub
    WHEN credentials are created, the secret key hash is calculated, the secret key is
        retrieved and the secret key hash is compared with itself
    THEN the secret key hash of the credentials is returned, the secret key of the
        credentials is returned and True is returned.
    """
    sub = "sub 1"

    credentials = package_security.create(sub=sub)

    assert credentials.public_key is not None
    assert credentials.secret_key is not None
    assert credentials.secret_key_hash is not None
    assert credentials.salt is not None

    returned_secret_key_hash = package_security.calculate_secret_key_hash(
        secret_key=credentials.secret_key, salt=credentials.salt
    )
    assert returned_secret_key_hash == credentials.secret_key_hash

    returned_secret_key = package_security.retrieve_secret_key(
        sub=sub, salt=credentials.salt
    )
    assert returned_secret_key == credentials.secret_key

    assert (
        package_security.compare_secret_key_hashes(
            left=credentials.secret_key_hash, right=credentials.secret_key_hash
        )
        is True
    )


def test_access_token(access_token):
    """
    GIVEN TEST_USERNAME and TEST_PASSWORD environment variables are set
    WHEN the access_token fixture is requested
    THEN an access token is returned.
    """
    assert access_token
