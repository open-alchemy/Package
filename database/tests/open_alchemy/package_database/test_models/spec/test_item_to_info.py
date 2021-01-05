"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models


@pytest.mark.parametrize(
    "title, description, expected_spec_info",
    [
        pytest.param(None, None, {}, id="title description not defined"),
        pytest.param(
            "title 1",
            "description 1",
            {
                "title": "title 1",
                "description": "description 1",
            },
            id="title description defined",
        ),
    ],
)
@pytest.mark.models
def test_item_to_info(title, description, expected_spec_info):
    """
    GIVEN title and description
    WHEN Spec is constructed with the title and description
    THEN the expected spec info is returned.
    """
    item = factory.SpecFactory(title=title, description=description)
    expected_spec_info["name"] = item.name
    expected_spec_info["id"] = item.id
    expected_spec_info["version"] = item.version
    expected_spec_info["model_count"] = item.model_count
    expected_spec_info["updated_at"] = int(item.updated_at)

    spec_info = models.Spec.item_to_info(item)

    assert spec_info == expected_spec_info
