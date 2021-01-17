"""Configuration."""

import dataclasses
import enum
import os
import typing


class Stage(str, enum.Enum):
    """The stage the API is running in."""

    TEST = "TEST"
    PROD = "PROD"


_STAGES = {item.value for item in Stage}


@dataclasses.dataclass
class TConfig:
    """
    The application configuration.

    Attrs:
        stage: The stage the application is running in.
        package_storage_bucket_name: The name of the bucket with the specs.
        access_control_allow_origin: The CORS origin response.
        access_control_allow_headers: The CORS headers response.
        free_tier_model_count: The number of models allowed in the free tier.

    """

    _stage: typing.Optional[Stage] = None
    _package_storage_bucket_name: typing.Optional[str] = None
    _access_control_allow_origin: typing.Optional[str] = None
    _access_control_allow_headers: typing.Optional[str] = None
    _default_credentials_id: typing.Optional[str] = None
    _free_tier_model_count: typing.Optional[int] = None

    @staticmethod
    def _get_env(key: str) -> str:
        """Get the environment variable."""
        value = os.getenv(key)
        assert isinstance(value, str), (
            f"the {key} environment variable must be set and a string, " f"{value=}"
        )
        return value

    @property
    def stage(self) -> Stage:
        """Retrieve the stage configuration."""
        if self._stage is None:
            stage_key = "STAGE"
            stage_str = self._get_env(stage_key)
            assert stage_str in _STAGES, (
                f"the {stage_key} environment variable value must be one of "
                f"{_STAGES}, {stage_str=}"
            )
            self._stage = Stage[stage_str]

        return self._stage

    @stage.setter
    def stage(self, value: Stage) -> None:
        """Set the stage."""
        self._stage = value

    @property
    def package_storage_bucket_name(self) -> str:
        """Retrieve the package_storage_bucket_name configuration."""
        if self._package_storage_bucket_name is None:
            package_storage_bucket_name = self._get_env("PACKAGE_STORAGE_BUCKET_NAME")
            self._package_storage_bucket_name = package_storage_bucket_name

        return self._package_storage_bucket_name

    @package_storage_bucket_name.setter
    def package_storage_bucket_name(self, value: str) -> None:
        """Set the package_storage_bucket_name."""
        self._package_storage_bucket_name = value

    @property
    def access_control_allow_origin(self) -> str:
        """Retrieve the access_control_allow_origin configuration."""
        if self._access_control_allow_origin is None:
            access_control_allow_origin = self._get_env("ACCESS_CONTROL_ALLOW_ORIGIN")
            self._access_control_allow_origin = access_control_allow_origin

        return self._access_control_allow_origin

    @access_control_allow_origin.setter
    def access_control_allow_origin(self, value: str) -> None:
        """Set the access_control_allow_origin."""
        self._access_control_allow_origin = value

    @property
    def access_control_allow_headers(self) -> str:
        """Retrieve the access_control_allow_headers configuration."""
        if self._access_control_allow_headers is None:
            access_control_allow_headers = self._get_env("ACCESS_CONTROL_ALLOW_HEADERS")
            self._access_control_allow_headers = access_control_allow_headers

        return self._access_control_allow_headers

    @access_control_allow_headers.setter
    def access_control_allow_headers(self, value: str) -> None:
        """Set the access_control_allow_headers."""
        self._access_control_allow_headers = value

    @property
    def default_credentials_id(self) -> str:
        """Retrieve the default_credentials_id configuration."""
        if self._default_credentials_id is None:
            default_credentials_id = self._get_env("DEFAULT_CREDENTIALS_ID")
            self._default_credentials_id = default_credentials_id

        return self._default_credentials_id

    @default_credentials_id.setter
    def default_credentials_id(self, value: str) -> None:
        """Set the default_credentials_id."""
        self._default_credentials_id = value

    @property
    def free_tier_model_count(self) -> int:
        """Retrieve the free_tier_model_count configuration."""
        if self._free_tier_model_count is None:
            free_tier_model_count_key = "FREE_TIER_MODEL_COUNT"
            free_tier_model_count_str = self._get_env(free_tier_model_count_key)
            try:
                self._free_tier_model_count = int(free_tier_model_count_str)
            except ValueError as exc:
                raise AssertionError(
                    f"the {free_tier_model_count_key} environment variable value must "
                    f"be an integer, {free_tier_model_count_str=}"
                ) from exc

        return self._free_tier_model_count

    @free_tier_model_count.setter
    def free_tier_model_count(self, value: int) -> None:
        """Set the free_tier_model_count."""
        self._free_tier_model_count = value


def _construct() -> TConfig:
    """Construct the configuration."""
    return TConfig()


class TCache(typing.TypedDict, total=True):
    """Cache for configuration."""

    config: typing.Optional[TConfig]


_CACHE: TCache = {"config": None}


def get() -> TConfig:
    """Retrieve the configuration."""
    if _CACHE["config"] is None:
        _CACHE["config"] = _construct()
    assert _CACHE["config"] is not None
    return _CACHE["config"]
