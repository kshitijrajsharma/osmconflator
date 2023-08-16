from setuptools import find_packages, setup

setup(
    name="osmconflator",
    version="0.0.2",
    author="Kshitij Raj Sharma",
    author_email="skshitizraj@gmail.com",
    description="A package for conflation of GeoJSON features with OSM data",
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
