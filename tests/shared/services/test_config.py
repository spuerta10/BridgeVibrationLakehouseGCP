from shared.services.config import (
    Config,
    EmptyConfigsError
)

import pytest
from dynaconf.base import LazySettings


@pytest.fixture
def config() -> LazySettings:
    """
    Fixture to provide a LazySettings object from a configuration file.

    :return: LazySettings: LazySettings instance loaded from a configuration file.
    """
    return Config.get("src/config/config.yaml")


@pytest.fixture
def empty_file_name() -> str:
    """
    Fixture to provide the name of an empty configuration file.

    :return: str: Name of the empty configuration file.
    """
    return "empty_config.yaml"


def test_singleton(config: LazySettings):
    """
    Test to check the singleton behavior of configuration loading.

    :param config: LazySettings: LazySettings instance loaded from configuration.
    :return: None
    """
    config2: LazySettings = Config.get("src/config/config.yaml")
    assert config2 is config


def test_config_with_existent_file(config: LazySettings):
    """
    Test to ensure configuration can be retrieved from an existing file.

    :param config: LazySettings: LazySettings instance loaded from configuration.
    :return: None
    """
    assert config.to_dict()


def test_config_with_empty_file(empty_file_name: str, tmp_path):
    """
    Test to handle loading configuration from an empty file.

    :param empty_file_name: str: Name of the empty configuration file.
    :param tmp_path: fixture: Temporary directory provided by pytest.
    :return: None
    """

    empty_file = tmp_path / empty_file_name
    empty_file.touch()

    try:
        Config.get(f"{empty_file}")
    except Exception as exc_info:
        assert isinstance(exc_info, EmptyConfigsError)
    assert empty_file.stat().st_size == 0  # check if the file is actually empty


def test_config_with_nonexistent_file():
    """
    Test to handle loading configuration from a non-existent file.

    :return: None
    """
    try:
        Config.get("nonexistent_file.yaml")
    except Exception as exc_info:
        assert isinstance(exc_info, EmptyConfigsError)
