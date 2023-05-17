# OSM Conflator

OSM Conflator is a Python package that allows you to conflate GeoJSON features with OpenStreetMap (OSM) data. It helps you identify and modify features in a GeoJSON dataset that intersect with OSM data, providing a convenient way to update properties or perform other actions based on the conflation results.

## Installation

You can install OSM Conflator using pip:

```shell
pip install osmconflator
```

## Usage

Here's an example of how to use OSM Conflator in your Python code:

```python
from osmconflator import conflate_geojson

geojson_str = '{"type": "FeatureCollection", "features": ... }'

conflated_geojson = conflate_geojson(geojson_str)

print(conflated_geojson)
```

In the above example, conflate_geojson is the main function provided by OSM Conflator. It takes a GeoJSON string as input, performs conflation with OSM data, and returns an  GeoJSON string with problems of duplicate and overlapping.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request. When contributing to this project, please follow the Contributing Guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.