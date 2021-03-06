"""Fixtures."""

import os
import subprocess
import sys
import uuid
from urllib import request

import pytest


@pytest.fixture()
def spec_name(access_token):
    """Returns a spec id that is cleaned up at the end."""
    spec_name_value = f"IndexSpecId-{uuid.uuid4()}"

    yield spec_name_value

    delete_request = request.Request(
        f"https://package.api.openalchemy.io/v1/specs/{spec_name_value}",
        headers={"Authorization": f"Bearer {access_token}"},
        method="DELETE",
    )
    with request.urlopen(delete_request) as response:
        assert response.status == 204

    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", spec_name_value],
        cwd=os.getcwd(),
        check=False,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
