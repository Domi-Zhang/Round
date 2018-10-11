import os

import time
from urllib.parse import quote

import requests

from utils import properties

server_url = properties.Properties.default_instance().get("server", "url")
file = properties.Properties.default_instance().get("file", "monitor")


def run():
    if not os.path.exists(file):
        print("file " + file + " not exists.")
        return

    last_time = None
    while True:
        if last_time is None or os.path.getmtime(file) > last_time:
            last_time = os.path.getmtime(file)
            for line in open(file):
                line = line.strip()
                resp = requests.get(server_url.format(quote(line)))
                if resp.status_code != 200:
                    print("got error status code: " + str(resp.status_code))
                else:
                    print(resp.text)
        else:
            print("file not change.")
            time.sleep(5)


if __name__ == "__main__":
    run()
