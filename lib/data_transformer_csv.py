import csv
import glob
import json
import math
import os
from pathlib import Path

# Configuration
USER_UID_STEFAN = "00000000-0000-0000-0000-000000000000"


def get_average_accelerometer_data(bike_activity_measurements):
    values = []

    for bike_activity_measurement in bike_activity_measurements:
        x = bike_activity_measurement["accelerometerX"]
        y = bike_activity_measurement["accelerometerY"]
        z = bike_activity_measurement["accelerometerZ"]

        values.append(math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)))

    return sum(values) / len(values)


def write_bike_activity_samples_to_csv(results_path, results_file_name, bike_activity, bike_activity_samples_with_measurements):
    bike_activity_uid = bike_activity["uid"]
    # bike_activity_start_time = bike_activity["startTime"]
    # bike_activity_end_time = bike_activity["endTime"]
    # bike_activity_tracking_type = bike_activity["trackingType"]
    bike_activity_surface_type = bike_activity["surfaceType"]
    bike_activity_smoothness_type = bike_activity["smoothnessType"]
    bike_activity_phone_position = bike_activity["phonePosition"]
    bike_activity_bike_type = bike_activity["bikeType"]

    with open(results_path + "/" + results_file_name, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([
            # Descriptive values
            'bike_activity_uid',
            'bike_activity_sample_uid',
            'bike_activity_measurement',
            'bike_activity_measurement_timestamp',
            'bike_activity_measurement_lon',
            'bike_activity_measurement_lat',
            # Input values
            'bike_activity_measurement_speed',
            'bike_activity_measurement_accelerometer_x',
            'bike_activity_measurement_accelerometer_y',
            'bike_activity_measurement_accelerometer_z',
            'bike_activity_phone_position',
            'bike_activity_bike_type',
            # Output values
            'bike_activity_surface_type',
            'bike_activity_smoothness_type',
        ])

        for bike_activity_sample_with_measurements in bike_activity_samples_with_measurements:

            bike_activity_sample = bike_activity_sample_with_measurements["bikeActivitySample"]
            bike_activity_measurements = bike_activity_sample_with_measurements["bikeActivityMeasurements"]

            bike_activity_sample_uid = bike_activity_sample["uid"]
            # bike_activity_sample_timestamp = bike_activity_sample["timestamp"]
            # bike_activity_sample_lon = bike_activity_sample["lon"]
            # bike_activity_sample_lat = bike_activity_sample["lat"]
            # bike_activity_sample_speed = bike_activity_sample["speed"]
            bike_activity_sample_surface_type = bike_activity_sample["surfaceType"] if "surfaceType" in bike_activity_sample else None

            for bike_activity_measurement in bike_activity_measurements:
                bike_activity_measurement_uid = bike_activity_measurement["uid"]
                bike_activity_measurement_timestamp = bike_activity_measurement["timestamp"]
                bike_activity_measurement_lon = bike_activity_measurement["lon"]
                bike_activity_measurement_lat = bike_activity_measurement["lat"]
                bike_activity_measurement_speed = bike_activity_measurement["speed"]
                bike_activity_measurement_accelerometer_x = bike_activity_measurement["accelerometerX"]
                bike_activity_measurement_accelerometer_y = bike_activity_measurement["accelerometerY"]
                bike_activity_measurement_accelerometer_z = bike_activity_measurement["accelerometerZ"]

                csv_writer.writerow([
                    bike_activity_uid,
                    bike_activity_sample_uid,
                    bike_activity_measurement_uid,
                    bike_activity_measurement_timestamp,
                    bike_activity_measurement_lon,
                    bike_activity_measurement_lat,
                    # Input values
                    bike_activity_measurement_speed,
                    bike_activity_measurement_accelerometer_x,
                    bike_activity_measurement_accelerometer_y,
                    bike_activity_measurement_accelerometer_z,
                    bike_activity_phone_position,
                    bike_activity_bike_type,
                    # Output values
                    bike_activity_sample_surface_type if bike_activity_sample_surface_type is not None else bike_activity_surface_type,
                    bike_activity_smoothness_type,
                ])


def get_rider_name(user_data_uid):
    if user_data_uid == USER_UID_STEFAN:
        return "Stefan P"
    else:
        return "Florian S"


#
# Main
#


class DataTransformerCsv:

    def run(self, data_path, results_path, clean=False, reconvert=False):
        # Make results path
        os.makedirs(results_path, exist_ok=True)

        # Clean results path
        if clean:
            files = glob.glob(os.path.join(results_path, "*"))
            for f in files:
                os.remove(f)

        for file_path in glob.iglob(data_path + "/*.json"):

            file_name = os.path.basename(file_path)
            file_base_name = file_name.replace(".json", "")

            results_file_name = file_base_name + ".csv"
            results_file_path = results_path + "/" + results_file_name

            if not Path(results_file_path).exists() or reconvert:
                file = open(file_path)
                data = json.load(file)

                user_data_uid = data['userData']['uid']
                rider_name = get_rider_name(user_data_uid)

                bike_activity = data['bikeActivity']
                bike_activity_samples_with_measurements = data['bikeActivitySamplesWithMeasurements']

                print("✔️ Converting into csv " + file_name + " (" + rider_name + ")")

                write_bike_activity_samples_to_csv(
                    results_path=results_path,
                    results_file_name=file_base_name + ".csv",
                    bike_activity=bike_activity,
                    bike_activity_samples_with_measurements=bike_activity_samples_with_measurements
                )

        print("DataTransformerGeoJson finished.")
