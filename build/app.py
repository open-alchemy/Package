"""Main function for lambda."""

import pathlib
import shutil


def setup(directory: str) -> pathlib.Path:
    """
    Prepare the environment for execution.

    Args:
        directory: The base directory for execution.

    Returns:
        The directory that can be used to execute.

    """
    path = pathlib.Path(directory)
    build_path = path / "build"
    if build_path.exists():
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if build_path.is_file():
            build_path.unlink()

    assert not build_path.exists()
    build_path.mkdir()
    return build_path


def main(event, context):
    """Handle request."""
    print({"event": event, "context": context})  # allow-print
