"""Common fixtures."""

import pytest
from library import config
from library.facades import storage


def preset_config():
    """Preset configuration values."""
    config_instance = config.get()

    config_instance.stage = config.Stage.TEST
    config_instance.package_storage_bucket_name = "bucket1"
    config_instance.access_control_allow_origin = "*"
    config_instance.access_control_allow_headers = "x-language"
    config_instance.default_credentials_id = "default"


@pytest.fixture(autouse=True)
def clean_storage():
    """Delete all objects from the storage."""
    yield

    keys = storage.get_storage().list()

    storage.get_storage().delete_all(keys=keys)


@pytest.fixture(autouse=True)
def use_service_secret(_service_secret):
    """Always uses the _service_secret open-alchemy.package-security fixture."""


preset_config()
