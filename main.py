import os
import sys

# Make library available in path
library_paths = [
    os.path.join(os.getcwd(), 'lib')
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from data_downloader_firebase_storage import FirebaseStorageDownloader
from data_transformer_geojson import DataTransformerGeoJson

# Configuration
RELOAD_DATA = True
RECONVERT_DATA = True

# Set script path
file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Download data from Firebase Storage
FirebaseStorageDownloader().run(
    results_path=script_path + "/data/measurements/json",
    reload=RELOAD_DATA)

# Convert data into geojson
DataTransformerGeoJson().run(
    data_path=script_path + "/data/measurements/json",
    results_path = script_path + "/data/measurements/geojson",
    reconvert=RECONVERT_DATA)
