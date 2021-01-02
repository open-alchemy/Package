"""Configuration."""

import dataclasses
import typing

import boto3

_SECRETS_MANAGER_CLIENT = boto3.client("secretsmanager")


@dataclasses.dataclass
class TConfig:
    """
    The configuration variables.

    Attrs:
        service_secret: Secret used to generate secret keys

    """

    service_secret_name = "package-service"
    _service_secret: typing.Optional[bytes] = None

    @property
    def service_secret(self) -> bytes:
        """Retrieve the service secret if not defined else return it."""
        if self._service_secret is None:
            # Retrieve from AWS
            response = _SECRETS_MANAGER_CLIENT.get_secret_value(
                SecretId=self.service_secret_name
            )

            assert isinstance(
                response, dict
            ), f"secrets manager response not dict, {response=}"

            secret_binary_key = "SecretBinary"
            assert (
                secret_binary_key in response
            ), f"{secret_binary_key} not in secrets manager response, {response=}"
            secret_binary = response[secret_binary_key]
            assert isinstance(secret_binary, bytes), (
                f"secrets manager response.{secret_binary_key} not string, "
                f"{secret_binary=}, {response=}"
            )

            self._service_secret = secret_binary

        return self._service_secret

    @service_secret.setter
    def service_secret(self, value: bytes):
        """Set the service secret."""
        self._service_secret = value


def _get() -> TConfig:
    """Read the configuration variables."""
    return TConfig()


_CONFIG = _get()


def get() -> TConfig:
    """
    Get the value of configuration variables.

    Returns:
        The configuration variables.

    """
    return _CONFIG
