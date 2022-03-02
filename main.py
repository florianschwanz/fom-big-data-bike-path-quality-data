import getopt
import os
import sys

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Make library available in path
library_paths = [
    os.path.join(script_path, 'lib'),
    os.path.join(script_path, 'lib', 'log'),
    os.path.join(script_path, 'lib', 'plotters'),
    os.path.join(script_path, 'lib', 'data_download'),
    os.path.join(script_path, 'lib', 'data_pre_processing'),
    os.path.join(script_path, 'lib', 'data_preparation'),
    os.path.join(script_path, 'lib', 'data_statistics'),
    os.path.join(script_path, 'lib', 'data_transformation')
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from logger_facade import LoggerFacade
from data_downloader_firebase_firestore import FirebaseFirestoreDownloader
from data_downloader_firebase_storage import FirebaseStorageDownloader
from data_loader import DataLoader
from data_filterer import DataFilterer
from bike_activity_surface_type_plotter import BikeActivitySurfaceTypePlotter
from input_data_statistics import InputDataStatistics
from data_transformer_csv import DataTransformerCsv
from data_transformer_geojson import DataTransformerGeoJson
from sliding_window_data_splitter import SlidingWindowDataSplitter


#
# Main
#

def main(argv):
    # Set default values
    reload_data = True
    reconvert_data = True
    clean_data = True

    slicing_configurations = [
        (500, 500),
        # (500, 50),
        # (250, 25),
        # (100, 10),
    ]
    measurement_interval = 0.05

    # Set default values
    measurement_speed_limit = 5.0

    # Read command line arguments
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        print(
            "main.py --help")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("message.py")
            print("--help                           show this help")
            sys.exit()

    # Set paths
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

    for slice_width, window_step in slicing_configurations:
        SlidingWindowDataSplitter().run(
            logger=logger,
            data_path=os.path.join(data_path, "measurements", "csv"),
            results_path=os.path.join(data_path, "measurements", "slices",
                                      "width" + str(slice_width) + "_step" + str(window_step)),
            slice_width=slice_width,
            window_step=window_step,
            measurement_interval=measurement_interval,
            clean=clean_data
        )

    #
    # Statistics
    #

    dataframes = DataLoader().run(
        logger=logger,
        data_path=os.path.join(data_path, "measurements", "slices", "width" + str(500) + "_step" + str(500)),
        limit=None,
        quiet=False
    )

    filtered_dataframes = DataFilterer().run(
        logger=logger,
        dataframes=dataframes,
        slice_width=500,
        measurement_speed_limit=measurement_speed_limit,
        keep_unflagged_lab_conditions=False,
        quiet=True
    )

    BikeActivitySurfaceTypePlotter().run(
        logger=logger,
        dataframes=filtered_dataframes,
        slice_width=500,
        results_path=data_path,
        file_name="surface_type_raw",
        title="Surface type distribution (raw)",
        description="Distribution of surface types in raw data",
        xlabel="surface type",
        clean=True,
        quiet=True
    )

    surface_types = InputDataStatistics().run(
        logger=logger,
        data_path=os.path.join(data_path, "measurements", "csv"),
        measurement_speed_limit=measurement_speed_limit,
        filter_lab_conditions=False,
        filter_speed=False,
        filter_surface_types=True
    )

    BikeActivitySurfaceTypePlotter().run_bar(
        logger=logger,
        data=surface_types,
        results_path=data_path,
        file_name="surface_type_raw",
        title="Surface type distribution (raw)",
        description="Distribution of surface types in raw data",
        xlabel="surface type",
        clean=True,
        quiet=True
    )


if __name__ == "__main__":
    main(sys.argv[1:])
