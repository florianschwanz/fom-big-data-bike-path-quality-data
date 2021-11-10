import getopt
import os
import sys

# Make library available in path
library_paths = [
    os.path.join(os.getcwd(), 'lib'),
    os.path.join(os.getcwd(), 'lib', 'log'),
    os.path.join(os.getcwd(), 'lib', 'data_download'),
    os.path.join(os.getcwd(), 'lib', 'data_transformation'),
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
        (500, 50),
        (250, 25),
        (100, 10),
    ]
    measurement_interval = 0.05

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


if __name__ == "__main__":
    main(sys.argv[1:])
