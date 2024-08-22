import json
from unittest import mock

import pytest

from osmconflator import conflate_geojson


@pytest.fixture
def valid_geojson():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [83.9797402, 28.2040093],
                            [83.9798306, 28.2039456],
                            [83.9798735, 28.2039929],
                            [83.979783, 28.2040566],
                            [83.9797402, 28.2040093],
                        ]
                    ],
                },
                "properties": {
                },
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [83.9797672, 28.2040843],
                            [83.979893, 28.2039933],
                            [83.9799483, 28.2040526],
                            [83.9798225, 28.2041437],
                            [83.9797672, 28.2040843],
                        ]
                    ],
                },
                "properties": {
                },
            },
                        {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [83.9797672, 28.3040843],
                            [83.979893, 28.2039933],
                            [83.9799483, 28.2040526],
                            [83.9798225, 28.2041437],
                            [83.9797672, 28.3040843],
                        ]
                    ],
                },
                "properties": {
                },
            },
        ],
    }

@mock.patch("osmconflator.api.RawDataAPI")
def test_conflate_geojson(mock_raw_data_api, valid_geojson):
    # Mock the API responses
    task_result = {
        "status": "SUCCESS",
        "result": {"download_url": "https://example.com/download"},
    }
    mock_raw_data_api.return_value.poll_task_status.return_value = task_result
    mock_raw_data_api.return_value.download_snapshot.return_value = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [83.9797402, 28.2040093],
                            [83.9798306, 28.2039456],
                            [83.9798735, 28.2039929],
                            [83.979783, 28.2040566],
                            [83.9797402, 28.2040093],
                        ]
                    ],
                },
                "properties": {
                    "osm_id": 417779760,
                    "version": 1,
                    "tags": {"building": "yes"},
                    "timestamp": "2016-05-13T06:26:44",
                },
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [83.9797672, 28.2040843],
                            [83.979893, 28.2039933],
                            [83.9799483, 28.2040526],
                            [83.9798225, 28.2041437],
                            [83.9797672, 28.2040843],
                        ]
                    ],
                },
                "properties": {
                    "osm_id": 417779732,
                    "version": 1,
                    "tags": {"building": "yes"},
                    "timestamp": "2016-05-13T06:26:34",
                },
            },
        ],
    }
    conflated_geojson = conflate_geojson(valid_geojson)

    assert len(conflated_geojson["features"]) == 3
    assert conflated_geojson["features"][0]["properties"]["intersect"] == True
    assert conflated_geojson["features"][0]["properties"]["duplicate"] == True
    assert conflated_geojson["features"][1]["properties"]["intersect"] == True
    assert conflated_geojson["features"][1]["properties"]["duplicate"] == True
    assert conflated_geojson["features"][2]["properties"]["duplicate"] == False
    assert conflated_geojson["features"][2]["properties"]["intersect"] == True
    conflated_removed_features = conflate_geojson(valid_geojson, remove_conflated=True)
    assert len(conflated_removed_features["features"]) == 0


def test_conflate_geojson_invalid_geojson():
    invalid_geojson = "This is not a valid GeoJSON"
    with pytest.raises(ValueError):
        conflate_geojson(invalid_geojson)
