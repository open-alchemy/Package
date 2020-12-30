"""Fixtures for the application."""

import app
import pytest
from botocore import stub


@pytest.fixture
def stubbed_s3_client():
    """Stubs the S3 client."""
    stubber = stub.Stubber(app.S3_CLIENT)

    yield stubber

    stubber.deactivate()
