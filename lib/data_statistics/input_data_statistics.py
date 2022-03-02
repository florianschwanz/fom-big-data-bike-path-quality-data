import csv
import glob

from tracking_decorator import TrackingDecorator


def get_bike_activity_measurement_speed_min(slice):
    bike_activity_measurement_speed_min = None

    for row in slice:
        bike_activity_measurement_speed = float(row["bike_activity_measurement_speed"])

        if bike_activity_measurement_speed_min == None or bike_activity_measurement_speed < bike_activity_measurement_speed_min:
            bike_activity_measurement_speed_min = bike_activity_measurement_speed

    return bike_activity_measurement_speed_min


#
# Main
#

class InputDataStatistics:

    @TrackingDecorator.track_time
    def run(self, logger, data_path, measurement_speed_limit, filter_lab_conditions=False, filter_speed=False,
            filter_surface_types=False):

        slices = {}
        surface_types = {}

        for file_path in glob.iglob(data_path + "/*.csv"):

            with open(file_path) as csv_file:

                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:

                    # Determine bike activity UID and bike activity sample UID
                    bike_activity_uid = row["bike_activity_uid"]
                    bike_activity_sample_uid = row["bike_activity_sample_uid"]

                    # Create result file if not yet existing
                    if bike_activity_sample_uid not in slices:
                        slices[bike_activity_sample_uid] = []

                    # Append row
                    slices[bike_activity_sample_uid].append(row)

        valid_surface_types = [
            "asphalt",
            # "concrete lanes",
            "concrete plates",
            "paving stones",
            "sett",
            # "compacted",
            "fine gravel",
            # "gravel"
        ]

        for bike_activity_sample_uid, slice in slices.items():
            bike_activity_flagged_lab_conditions = slice[0]["bike_activity_flagged_lab_conditions"]
            bike_activity_surface_type = slice[0]["bike_activity_surface_type"]
            bike_activity_measurement_speed_min = get_bike_activity_measurement_speed_min(slice)

            if (not filter_lab_conditions or bike_activity_flagged_lab_conditions == "True") \
                    and (not filter_speed or bike_activity_measurement_speed_min * 3.6 >= measurement_speed_limit) \
                    and (not filter_surface_types or bike_activity_surface_type in valid_surface_types):

                if bike_activity_surface_type not in surface_types:
                    surface_types[bike_activity_surface_type] = 0

                surface_types[bike_activity_surface_type] += 1

        for surface_type, value in surface_types.items():
            logger.log_line(f"{surface_type}: {value}")
        logger.log_line(f"total: {len(slices.items())}")

        return surface_types
