import io

from setuptools import find_packages, setup

with io.open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="osmconflator",
    version="0.0.7",
    url="https://github.com/kshitijrajsharma/osmconflator",
    author="Kshitij Raj Sharma",
    author_email="skshitizraj@gmail.com",
    description="A package for conflation of GeoJSON features with OSM data",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "shapely",
        "requests",
    ],
)
