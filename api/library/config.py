"""Configuration."""

import dataclasses
import enum
import os


class Stage(str, enum.Enum):
    """The stage the API is running in."""

    TEST = "TEST"
    PROD = "PROD"


_STAGES = {item.value for item in Stage}


@dataclasses.dataclass
class TEnvironment:
    """The environment variables."""

    # The stage the application is running in
    stage: Stage
    # The name of the bucket with the specs
    package_storage_bucket_name: str
    # The CORS origin response
    access_control_allow_origin: str
    # The CORS headers response
    access_control_allow_headers: str
    # The name of the package storage table
    package_database_table_name: str
    # The name of the package storage index
    package_database_index_name: str


def _get_env() -> TEnvironment:
    """Read environment variables."""
    stage_str = os.getenv("STAGE", Stage.TEST.value)
    assert isinstance(stage_str, str)
    assert stage_str in _STAGES
    stage = Stage[stage_str]

    package_storage_bucket_name = os.getenv("PACKAGE_STORAGE_BUCKET_NAME", "")
    assert isinstance(package_storage_bucket_name, str)

    access_control_allow_origin = os.getenv("ACCESS_CONTROL_ALLOW_ORIGIN", "*")
    assert isinstance(access_control_allow_origin, str)

    access_control_allow_headers = os.getenv(
        "ACCESS_CONTROL_ALLOW_HEADERS", "x-language"
    )
    assert isinstance(access_control_allow_headers, str)

    package_database_table_name = os.getenv(
        "PACKAGE_DATABASE_TABLE_NAME", "package-storage"
    )
    assert isinstance(package_database_table_name, str)

    package_database_index_name = os.getenv(
        "PACKAGE_DATABASE_INDEX_NAME", "specIdUpdatedAt"
    )
    assert isinstance(package_database_index_name, str)

    return TEnvironment(
        stage=stage,
        package_storage_bucket_name=package_storage_bucket_name,
        access_control_allow_origin=access_control_allow_origin,
        access_control_allow_headers=access_control_allow_headers,
        package_database_table_name=package_database_table_name,
        package_database_index_name=package_database_index_name,
    )


_ENVIRONMENT = _get_env()


def get_env() -> TEnvironment:
    """
    Get the value of environment variables.

    Returns:
        The environment variables.

    """
    return _ENVIRONMENT
