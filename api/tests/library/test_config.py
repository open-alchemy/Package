"""Tests for the configuration."""

import pytest
from library import config


@pytest.mark.parametrize(
    "env_name, config_name",
    [
        pytest.param("STAGE", "stage", id="stage"),
        pytest.param(
            "PACKAGE_STORAGE_BUCKET_NAME",
            "package_storage_bucket_name",
            id="package_storage_bucket_name",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_ORIGIN",
            "access_control_allow_origin",
            id="access_control_allow_origin",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_HEADERS",
            "access_control_allow_headers",
            id="access_control_allow_headers",
        ),
        pytest.param(
            "DEFAULT_CREDENTIALS_ID",
            "default_credentials_id",
            id="default_credentials_id",
        ),
        pytest.param(
            "FREE_TIER_MODEL_COUNT",
            "free_tier_model_count",
            id="free_tier_model_count",
        ),
    ],
)
@pytest.mark.config
def test_config_env_missing(monkeypatch, env_name, config_name):
    """
    GIVEN environment dependent configuration where environment variable is not set
    WHEN the configuration is access
    THEN AssertError is raised.
    """
    monkeypatch.delenv(env_name, raising=False)

    with pytest.raises(AssertionError):
        getattr(config._construct(), config_name)  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "env_name, env_value, config_name",
    [
        pytest.param("STAGE", "invalid", "stage", id="stage invalid"),
        pytest.param(
            "FREE_TIER_MODEL_COUNT",
            "invalid",
            "free_tier_model_count",
            id="free_tier_model_count invalid",
        ),
    ],
)
@pytest.mark.config
def test_config_env_invalid(monkeypatch, env_name, env_value, config_name):
    """
    GIVEN environment dependent configuration where environment variable is invalid
    WHEN the configuration is access
    THEN AssertError is raised.
    """
    monkeypatch.setenv(env_name, env_value)

    with pytest.raises(AssertionError):
        getattr(config._construct(), config_name)  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "env_name, env_value, config_name, expected_value",
    [
        pytest.param("STAGE", "TEST", "stage", config.Stage.TEST, id="stage"),
        pytest.param(
            "PACKAGE_STORAGE_BUCKET_NAME",
            "bucket 1",
            "package_storage_bucket_name",
            "bucket 1",
            id="package_storage_bucket_name",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_ORIGIN",
            "origin 1",
            "access_control_allow_origin",
            "origin 1",
            id="access_control_allow_origin",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_HEADERS",
            "header 1",
            "access_control_allow_headers",
            "header 1",
            id="access_control_allow_headers",
        ),
        pytest.param(
            "DEFAULT_CREDENTIALS_ID",
            "credentials 1",
            "default_credentials_id",
            "credentials 1",
            id="default_credentials_id",
        ),
        pytest.param(
            "FREE_TIER_MODEL_COUNT",
            "1",
            "free_tier_model_count",
            1,
            id="free_tier_model_count",
        ),
    ],
)
@pytest.mark.config
def test_config_env_set(monkeypatch, env_name, env_value, config_name, expected_value):
    """
    GIVEN environment dependent configuration where environment variable is set
    WHEN the configuration is access
    THEN the expected value is returned.
    """
    monkeypatch.setenv(env_name, env_value)

    returned_value = getattr(
        config._construct(), config_name  # pylint: disable=protected-access
    )

    assert returned_value == expected_value


@pytest.mark.parametrize(
    "env_name, config_name, config_value",
    [
        pytest.param("STAGE", "stage", config.Stage.TEST, id="stage"),
        pytest.param(
            "PACKAGE_STORAGE_BUCKET_NAME",
            "package_storage_bucket_name",
            "bucket 1",
            id="package_storage_bucket_name",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_ORIGIN",
            "access_control_allow_origin",
            "origin 1",
            id="access_control_allow_origin",
        ),
        pytest.param(
            "ACCESS_CONTROL_ALLOW_HEADERS",
            "access_control_allow_headers",
            "header 1",
            id="access_control_allow_headers",
        ),
        pytest.param(
            "DEFAULT_CREDENTIALS_ID",
            "default_credentials_id",
            "credentials 1",
            id="default_credentials_id",
        ),
        pytest.param(
            "FREE_TIER_MODEL_COUNT",
            "free_tier_model_count",
            1,
            id="free_tier_model_count",
        ),
    ],
)
@pytest.mark.config
def test_config_value_set(monkeypatch, env_name, config_name, config_value):
    """
    GIVEN environment dependent configuration where environment variable is not set but
        the config value is already set
    WHEN the configuration is access
    THEN the preset value is returned.
    """
    monkeypatch.delenv(env_name, raising=False)
    config_instance = config._construct()  # pylint: disable=protected-access
    setattr(config_instance, config_name, config_value)

    returned_value = getattr(config_instance, config_name)

    assert returned_value == config_value
