import getopt
import os
import sys

# Make library available in path
library_paths = [
    os.path.join(os.getcwd(), 'lib'),
    os.path.join(os.getcwd(), 'lib', 'log'),
    os.path.join(os.getcwd(), 'lib', 'data_statistics')
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from logger_facade import LoggerFacade
from input_data_statistics import InputDataStatistics


#
# Main
#

def main(argv):
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
    file_path = os.path.realpath(__file__)
    script_path = os.path.dirname(file_path)
    log_path = os.path.join(script_path, "log")
    data_path = os.path.join(script_path, "data")

    # Initialize logger
    logger = LoggerFacade(log_path, console=True, file=False)

    #
    # Statistics
    #

    surface_types = InputDataStatistics().run(
        logger=logger,
        data_path=os.path.join(data_path, "measurements", "csv"),
        measurement_speed_limit=measurement_speed_limit,
        filter_lab_conditions=True,
        filter_speed=True,
        filter_surface_types=True
    )

    log_line = "🥑 New bike activities uploaded, thereof useful"

    for bike_activity_surface_type, count in surface_types.items():
        log_line = log_line + "\n* " + bike_activity_surface_type + ": " + str(count)

    logger.log_line(log_line, telegram=True)


if __name__ == "__main__":
    main(sys.argv[1:])
