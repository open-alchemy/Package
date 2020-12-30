"""Tests for the app."""

import pathlib

import app
import pytest


def no_directory(_: pathlib.Path) -> None:
    """Does nothing."""


def directory_empty(path: pathlib.Path) -> None:
    """Creates empty directory."""
    (path / "build").mkdir()


def directory_with_single_file(path: pathlib.Path) -> None:
    """Creates empty directory."""
    directory_empty(path)
    (path / "build" / "test.txt").write_text("file 1")


def directory_with_multiple_file(path: pathlib.Path) -> None:
    """Creates empty directory."""
    directory_with_single_file(path)
    (path / "build" / "test.json").write_text("'value 1")


def file(path: pathlib.Path) -> None:
    """Creates a file."""
    (path / "build").write_text("file 1")


@pytest.mark.parametrize(
    "setup_steps",
    [
        pytest.param(no_directory, id="no directory"),
        pytest.param(directory_empty, id="directory exists"),
        pytest.param(
            directory_with_single_file,
            id="directory exists with single file",
        ),
        pytest.param(
            directory_with_multiple_file,
            id="directory exists with multiple file",
        ),
        pytest.param(file, id="file"),
    ],
)
def test_setup_not_exists(tmp_path, setup_steps):
    """
    GIVEN
    WHEN setup is called
    THEN the build folder is created and empty.
    """
    setup_steps(tmp_path)

    returned_path = app.setup(str(tmp_path))

    assert str(returned_path) == str(tmp_path / "build")
    assert returned_path.exists()
    assert next(returned_path.glob("**/*"), None) is None
