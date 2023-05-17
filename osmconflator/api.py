import io
import json
import time
import zipfile

import requests


class RawDataAPI:
    BASE_API_URL = "https://raw-data-api0.hotosm.org/v1"

    def request_snapshot(self, geometry):
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        payload = {"geometry": json.loads(geometry)}
        response = requests.post(
            f"{self.BASE_API_URL}/snapshot/", data=json.dumps(payload), headers=headers
        )
        response.raise_for_status()
        return response.json()

    def poll_task_status(self, task_link):
        stop_loop = False
        while not stop_loop:
            check_result = requests.get(url=f"{self.BASE_API_URL}{task_link}")
            check_result.raise_for_status()
            res = check_result.json()
            if res["status"] == "SUCCESS" or res["status"] == "FAILED":
                stop_loop = True
            time.sleep(1)
        return res

    def download_snapshot(self, download_url):
        response = requests.get(download_url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
            with zip_ref.open("Export.geojson") as file:
                return json.load(file)
