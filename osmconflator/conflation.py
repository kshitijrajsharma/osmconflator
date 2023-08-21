import json
import logging

from shapely.geometry import box

from .api import RawDataAPI
from .utils import calculate_bbox, conflate_features

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def validate_geojson(geojson_str):
    """
    Validates the input GeoJSON.

    Args:
        geojson_str (str): Input GeoJSON string.

    Raises:
        ValueError: If the input is not a valid GeoJSON.

    Returns:
        dict: Parsed GeoJSON dictionary.
    """
    try:
        geojson = json.loads(geojson_str)
    except json.JSONDecodeError:
        raise ValueError("Invalid GeoJSON. Please provide a valid GeoJSON string.")

    if (
        not isinstance(geojson, dict)
        or "type" not in geojson
        or "features" not in geojson
    ):
        raise ValueError("Invalid GeoJSON. Please provide a valid GeoJSON object.")

    return geojson


def conflate_geojson(geojson_str, remove_conflated=False):
    """
    Conflates the input GeoJSON with OpenStreetMap data.

    Args:
        geojson_str (str): Input GeoJSON string or JSON object.
        remove_conflated(bool) : False by default , returns geojson which are not intersected/duplicated with osm features
    Returns:
        str: Updated GeoJSON string with conflated features.
    """
    logger.info("Conflating GeoJSON...")

    if isinstance(geojson_str, str):
        geojson = validate_geojson(geojson_str)
    elif isinstance(geojson_str, dict):
        geojson = geojson_str
    else:
        raise ValueError(
            "Invalid input. Please provide a valid GeoJSON string or JSON object."
        )

    input_features = geojson["features"]
    input_bbox = calculate_bbox(input_features)
    logger.info(f"Creating bounding box for {len(input_features)} features...")
    bbox_geometry = box(*input_bbox)
    bbox_geojson_str = json.dumps(bbox_geometry.__geo_interface__)
    # with open("bbox.geojson", "w") as file:
    #     file.write(bbox_geojson_str)
    api = RawDataAPI()
    snapshot_data = api.request_snapshot(bbox_geojson_str)
    task_link = snapshot_data["track_link"]
    logger.info(f"Fetching latest OSM snapshot")
    task_result = api.poll_task_status(task_link)
    logger.info(f"Fetch Task result: {task_result['status']}")
    if task_result["status"] != "SUCCESS":
        raise RuntimeError(
            "Raw Data API did not respond correctly. Please try again later."
        )

    snapshot_url = task_result["result"]["download_url"]
    osm_features = api.download_snapshot(snapshot_url)
    # with open("osm_features.geojson", "w") as file:
    #     file.write(json.dumps(osm_features))
    logger.info(f"{len(osm_features['features'])} OSM features Found")
    logger.info("Conflating features...")
    geojson["features"] = conflate_features(
        input_features, osm_features["features"], remove_conflated
    )
    logger.info("Conflation completed.")
    return geojson
