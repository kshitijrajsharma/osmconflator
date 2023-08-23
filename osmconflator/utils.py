import json

from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.validation import make_valid


def calculate_bbox(features):
    geometries = [make_valid(shape(feature["geometry"])) for feature in features]
    union = unary_union(geometries)
    bbox = union.bounds
    return bbox


import logging


def conflate_features(input_features, osm_features, remove_conflated=False):
    osm_geometries = [shape(feature["geometry"]) for feature in osm_features]

    return_features = []
    for input_feature in input_features:
        input_geometry = shape(input_feature["geometry"])
        duplicate = False
        intersect = False

        for osm_geometry in osm_geometries:
            if input_geometry.equals(osm_geometry):
                duplicate = True
                intersect = True
                break
            if input_geometry.intersects(osm_geometry):
                intersect = True
                break

        input_feature["properties"]["duplicate"] = duplicate
        input_feature["properties"]["intersect"] = intersect

        if (duplicate or intersect) and remove_conflated:
            continue
        return_features.append(input_feature)

    return return_features
