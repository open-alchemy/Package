"""Database production tests."""

import importlib
import json
import os
import subprocess
import sys
import time
import typing
import uuid
from urllib import request


def test_index(access_token, spec_id):
    """
    GIVEN spec
    WHEN spec is created and then installed
    THEN the spec can be imported.
    """
    # Create the spec
    version = str(uuid.uuid4())
    title = "title 1"
    description = "description 1"
    spec = {
        "info": {
            "title": title,
            "description": description,
            "version": version,
        },
        "components": {
            "schemas": {
                "Employee": {
                    "type": "object",
                    "x-tablename": "employee",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "x-primary-key": True,
                            "x-autoincrement": True,
                        },
                    },
                }
            }
        },
    }
    spec_str = json.dumps(spec)
    spec_request = request.Request(
        f"https://package.api.openalchemy.io/v1/specs/{spec_id}",
        data=spec_str.encode(),
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-LANGUAGE": "JSON",
            "Content-Type": "text/plain",
        },
        method="PUT",
    )
    with request.urlopen(spec_request) as response:
        assert response.status == 204

    # Retrieve credentials
    credentials_request = request.Request(
        "https://package.api.openalchemy.io/v1/credentials/default",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        method="GET",
    )
    with request.urlopen(credentials_request) as response:
        assert response.status == 200
        response_data = json.loads(response.read().decode())
        assert "public_key" in response_data
        public_key = response_data["public_key"]
        assert "secret_key" in response_data
        secret_key = response_data["secret_key"]

    output: typing.Any = None
    for _ in range(5):
        output = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--index-url",
                f"https://{public_key}:{secret_key}@index.package.openalchemy.io",
                "--extra-index-url",
                "https://pypi.org/simple",
                f"{spec_id}=={version}",
            ],
            cwd=os.getcwd(),
            check=False,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if output.returncode == 0:
            break
        # Wait for the package to be created
        time.sleep(30)
    assert output is not None
    assert (
        output.returncode == 0
    ), f"{output.stdout.decode()=}, {output.stderr.decode()=}"

    importlib.import_module(spec_id)
