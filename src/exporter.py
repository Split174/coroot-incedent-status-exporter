import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import requests
import json
import enum
import os

WATCH_NS = json.loads(os.getenv('WATCH_NS'))
PROMETHEUS_DISABLE_CREATED_SERIES=True
COROOT_URL = os.getenv('COROOT_URL')

INCEDENT_STATUS = {
    "unknown": 0,
    "info": 1,
    "ok": 2,
    "warning": 3,
    "critical": 4
}


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        response = requests.get(COROOT_URL)
        if response.status_code == 200:
            g = GaugeMetricFamily("coroot_indicator_status", 'Coroot indicator status. "unknown": 0, "info": 1, "ok": 2, "warning": 3, "critical": 4', 
                labels=["app", "watchNamespace", "type"]
            )
            applications = response.json()["applications"]
            for app in applications:
                if app["labels"].get("ns") is None or app["labels"]["ns"] not in WATCH_NS: continue
                for indicator in app["indicators"]:
                    print(f"Problem in {app['id']} {indicator['message']}")
                    g.add_metric([app['id'], app["labels"]["ns"], indicator['message']], INCEDENT_STATUS[indicator['status']])
                    yield g
        else:
            print("Failed to retrieve JSON data from the URL.")

if __name__ == '__main__':
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(10)