import glob
import inspect
import json
import os
from pathlib import Path

import pyrebase
from tracking_decorator import TrackingDecorator


#
# Main
#


class FirebaseStorageDownloader:

    @TrackingDecorator.track_time
    def run(self, logger, results_path, clean=False, reload=False):
        # Set script path
        script_path = os.path.dirname(__file__)

        # Make results path
        os.makedirs(results_path, exist_ok=True)

        # Clean results path
        if clean:
            files = glob.glob(os.path.join(results_path, "*"))
            for f in files:
                os.remove(f)

        firebase_private_key_file = "bike-path-quality-firebase-adminsdk-cgjm5-640ce5b722.json"
        config = {
            "apiKey": "apiKey",
            "authDomain": "bike-path-quality.firebaseapp.com",
            "databaseURL": "https://bike-path-quality.firebaseio.com",
            "storageBucket": "bike-path-quality.appspot.com",
            "serviceAccount": os.path.join(script_path, firebase_private_key_file)
        }

        firebase = pyrebase.initialize_app(config)

        files = firebase.storage().child("measurements").child("json").list_files()
        for file in files:
            file_name = os.path.basename(file.name)
            file_path = results_path + "/" + file_name

            if file_name.endswith(".json") and (not Path(file_path).exists() or reload):
                logger.log_line("✓️ Downloading " + file_name)
                firebase.storage().child("measurements").child("json").child(file_name).download(file_path)

                with open(file_path, 'r+') as json_file:
                    json_object = json.load(json_file)
                    json_file.seek(0)
                    json_file.truncate()
                    json_file.write(json.dumps(json_object, indent=2, sort_keys=True))

        class_name = self.__class__.__name__
        function_name = inspect.currentframe().f_code.co_name

        logger.log_line(class_name + "." + function_name + " finished")
