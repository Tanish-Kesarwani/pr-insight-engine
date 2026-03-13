import json
import os
from datetime import datetime


class HistoryManager:

    def __init__(self, history_dir="analysis_history"):

        self.history_dir = history_dir

        # Ensure directory exists
        os.makedirs(self.history_dir, exist_ok=True)

    def save_run(self, result):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"run_{timestamp}.json"

        filepath = os.path.join(self.history_dir, filename)

        with open(filepath, "w") as f:
            json.dump(result, f, indent=4)

    def load_history(self):

        runs = []

        if not os.path.exists(self.history_dir):
            return runs

        for file in os.listdir(self.history_dir):

            if file.endswith(".json"):

                path = os.path.join(self.history_dir, file)

                with open(path) as f:
                    runs.append(json.load(f))

        return runs