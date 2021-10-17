import os
import sys

# Make library available in path
library_paths = [
    os.path.join(os.getcwd(), 'lib'),
    os.path.join(os.getcwd(), 'lib', 'log'),
    os.path.join(os.getcwd(), 'lib', 'data_download'),
    os.path.join(os.getcwd(), 'lib', 'data_transformation'),
    os.path.join(os.getcwd(), 'lib', 'data_statistics'),
    os.path.join(os.getcwd(), 'lib', 'data_pre_processing'),
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from logger_facade import LoggerFacade
from data_downloader_firebase_firestore import FirebaseFirestoreDownloader
from data_downloader_firebase_storage import FirebaseStorageDownloader
from data_transformer_csv import DataTransformerCsv
from data_transformer_geojson import DataTransformerGeoJson
from input_data_statistics import InputDataStatistics
from sliding_window_data_splitter import SlidingWindowDataSplitter

# Configuration
reload_data = True
reconvert_data = True
clean_data = True

slice_width = 500
window_step = 20
measurement_speed_limit = 5.0

# Set paths
file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)
log_path = os.path.join(script_path, "log")
data_path = os.path.join(script_path, "data")

# Initialize logger
logger = LoggerFacade(log_path, console=True, file=False)

#
# Download
#

FirebaseStorageDownloader().run(
    logger=logger,
    results_path=os.path.join(data_path, "measurements", "json"),
    clean=clean_data,
    reload=reload_data
)

FirebaseFirestoreDownloader().run(
    logger=logger,
    results_path=os.path.join(data_path, "metadata", "json"),
    clean=clean_data,
    reload=reload_data
)

#
# Transformation
#

DataTransformerGeoJson().run(
    logger=logger,
    data_path=os.path.join(data_path, "measurements", "json"),
    results_path=os.path.join(data_path, "measurements", "geojson"),
    clean=clean_data,
    reconvert=reconvert_data
)

DataTransformerCsv().run(
    logger=logger,
    data_path=os.path.join(data_path, "measurements", "json"),
    results_path=os.path.join(data_path, "measurements", "csv"),
    clean=clean_data,
    reconvert=reconvert_data
)

#
# Data pre-processing
#

SlidingWindowDataSplitter().run(
    logger=logger,
    data_path=os.path.join(data_path, "measurements", "csv"),
    slice_width=slice_width,
    window_step=window_step,
    results_path=os.path.join(data_path, "measurements", "slices", "width" + str(slice_width) + "_step" + str(window_step)),
    clean=clean_data
)

#
# Statistics
#

InputDataStatistics().run(
    logger=logger,
    data_path=os.path.join(data_path, "measurements", "csv"),
    measurement_speed_limit=measurement_speed_limit
)
