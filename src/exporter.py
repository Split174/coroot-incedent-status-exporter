import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import requests
import json

WATCH_NS = ["default"]
PROMETHEUS_DISABLE_CREATED_SERIES=True
URL = "https://community-demo.coroot.com/api/project/qcih204s/overview/applications"




class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        response = requests.get(URL)
        if response.status_code == 200:
            g = GaugeMetricFamily("coroot_indicator_status", 'Coroot indicator status', labels=["app", "type", "status"])
            applications = response.json()["applications"]
            for app in applications:
                if app["labels"].get("ns") is None or app["labels"]["ns"] not in WATCH_NS: continue
                for indicator in app["indicators"]:
                    print(f"Problem in {app['id']} {indicator['message']}")
                    g.add_metric([app['id'], indicator['message'], indicator['status']], 0)
                    yield g
        else:
            print("Failed to retrieve JSON data from the URL.")

if __name__ == '__main__':
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(10)