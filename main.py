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
from data_downloader_firebase_firestore import FirebaseFirestoreDownloader
from data_downloader_firebase_storage import FirebaseStorageDownloader
from data_transformer_csv import DataTransformerCsv
from data_transformer_geojson import DataTransformerGeoJson

# Configuration
RELOAD_DATA = True
RECONVERT_DATA = True
CLEAN_DATA = True

# Set script path
file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Download data from Firebase Storage
FirebaseStorageDownloader().run(
    results_path=script_path + "/data/measurements/json",
    clean=CLEAN_DATA,
    reload=RELOAD_DATA)

# Download data from Firebase Firestore
FirebaseFirestoreDownloader().run(
    results_path=script_path + "/data/metadata/json",
    clean=CLEAN_DATA,
    reload=RELOAD_DATA)

# Convert data into geojson
DataTransformerGeoJson().run(
    data_path=script_path + "/data/measurements/json",
    results_path=script_path + "/data/measurements/geojson",
    clean=CLEAN_DATA,
    reconvert=RECONVERT_DATA)

# Convert data into csv
DataTransformerCsv().run(
    data_path=script_path + "/data/measurements/json",
    results_path=script_path + "/data/measurements/csv",
    clean=CLEAN_DATA,
    reconvert=RECONVERT_DATA)
