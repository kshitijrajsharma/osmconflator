import json

from shapely.geometry import shape
from shapely.ops import unary_union


def calculate_bbox(features):
    geometries = [shape(feature["geometry"]) for feature in features]
    union = unary_union(geometries)
    bbox = union.bounds
    return bbox


def conflate_features(input_features, osm_features):
    osm_geometries = [shape(feature["geometry"]) for feature in osm_features]
    conflated_features = []

    for input_feature in input_features:
        input_geometry = shape(input_feature["geometry"])
        duplicate = False
        intersect = False

        for osm_geometry in osm_geometries:
            if input_geometry.equals(osm_geometry):
                duplicate = True
                intersect = True  # Treat duplicates as intersecting as well
                break
            elif input_geometry.intersects(osm_geometry):
                intersect = True
                break

        if duplicate or intersect:
            input_feature["properties"]["duplicate"] = duplicate
            input_feature["properties"]["intersect"] = intersect
            conflated_features.append(input_feature)

    return conflated_features
