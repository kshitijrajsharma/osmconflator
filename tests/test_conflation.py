import json
from unittest import mock

import pytest

from osmconflator import conflate_geojson


@pytest.fixture
def valid_geojson():
    return """
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [0, 0]
                    },
                    "properties": {
                        "name": "Point A"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [1, 1]
                    },
                    "properties": {
                        "name": "Point B"
                    }
                }
            ]
        }
    """


@mock.patch("osmconflator.api.RawDataAPI")
def test_conflate_geojson(mock_raw_data_api, valid_geojson):
    # Mock the API responses
    task_result = {
        "status": "SUCCESS",
        "result": {"download_url": "https://example.com/download"},
    }
    mock_raw_data_api.return_value.poll_task_status.return_value = task_result
    mock_raw_data_api.return_value.download_snapshot.return_value = {
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {
                    "name": "Point A",
                },
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1, 1]},
                "properties": {
                    "name": "Point B",
                },
            },
        ]
    }
    updated_geojson_str = conflate_geojson(valid_geojson)
    updated_geojson = json.loads(updated_geojson_str)
    assert len(updated_geojson["features"]) == 1
    assert updated_geojson["features"][0]["properties"]["duplicate"] == True
    assert updated_geojson["features"][0]["properties"]["name"] == "Point A"


def test_conflate_geojson_invalid_geojson():
    invalid_geojson = "This is not a valid GeoJSON"
    with pytest.raises(ValueError):
        conflate_geojson(invalid_geojson)
