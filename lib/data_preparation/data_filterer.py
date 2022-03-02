import inspect

from tqdm import tqdm
from tracking_decorator import TrackingDecorator


#
# Main
#

class DataFilterer:

    @TrackingDecorator.track_time
    def run(self, logger, dataframes, slice_width, measurement_speed_limit, keep_unflagged_lab_conditions=False,
            quiet=False):

        copied_dataframes = dataframes.copy()
        filtered_dataframes = {}

        dataframes_count = len(copied_dataframes.items())

        progress_bar = tqdm(iterable=copied_dataframes.items(), unit="dataframe", desc="Filter data frames")
        for name, dataframe in progress_bar:

            # Exclude dataframes which contain surface type 'mixed'
            if any(value in dataframe.bike_activity_surface_type.values for value in [
                "gravel",
                "paved",
                "concrete",
                "concrete lanes",
                "unhewn cobblestone",
                "cobblestone",
                "metal",
                "wood",
                "stepping_stones",
                "unpaved",
                "rock",
                "pebblestone",
                "ground",
                "dirt",
                "earth",
                "grass",
                "mud",
                "sand",
                "woodchips",
                "snow",
                "ice",
                "salt",
                "mixed"
            ]):
                if not quiet:
                    logger.log_line("✗️ Filtering out " + name + " (containing unsupported surface type)",
                                    console=False,
                                    file=True)
                continue

            filtered_dataframes[name] = dataframe

            if not quiet:
                logger.log_line("✓️ Keeping " + name, console=False, file=True)

        filtered_dataframes_count = len(filtered_dataframes.items())

        if not quiet:
            class_name = self.__class__.__name__
            function_name = inspect.currentframe().f_code.co_name

            logger.log_line(
                class_name + "." + function_name + " kept " + str(filtered_dataframes_count) + "/"
                + str(dataframes_count) + " dataframes ("
                + str(round(filtered_dataframes_count / dataframes_count, 2) * 100) + "%)")

        return filtered_dataframes
