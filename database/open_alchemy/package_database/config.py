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
class TConfig:
    """
    The configuration variables.

    Attrs:
        stage: The stage the application is running in
        specs_table_name: The name of the specs table
        specs_local_secondary_index_name: The name of the specs local secondary index
        credentials_table_name: The name of the credentials table
        credentials_local_secondary_index_name: The name of the credentials global
            secondary index
        free_tier_model_count: The number of models included in the free tier

    """

    stage: Stage
    specs_table_name: str
    specs_local_secondary_index_name: str
    credentials_table_name: str
    credentials_global_secondary_index_name: str
    free_tier_model_count: int


def _get() -> TConfig:
    """Read the configuration variables."""
    stage_key = "STAGE"
    stage_str = os.getenv(stage_key, Stage.TEST.value)
    assert isinstance(stage_str, str), f"{stage_key} environment variable must be set"
    assert (
        stage_str in _STAGES
    ), f"{stage_key} environment variable must be one of {_STAGES=}, {stage_str=}"
    stage = Stage[stage_str]

    specs_table_name = "package.specs"
    specs_local_secondary_index_name = "idUpdatedAt"

    credentials_table_name = "package.credentials"
    credentials_global_secondary_index_name = "publicKey"

    free_tier_model_count = 10

    return TConfig(
        stage=stage,
        specs_table_name=specs_table_name,
        specs_local_secondary_index_name=specs_local_secondary_index_name,
        credentials_table_name=credentials_table_name,
        credentials_global_secondary_index_name=credentials_global_secondary_index_name,
        free_tier_model_count=free_tier_model_count,
    )


_CONFIG = _get()


def get() -> TConfig:
    """
    Get the value of configuration variables.

    Returns:
        The configuration variables.

    """
    return _CONFIG
