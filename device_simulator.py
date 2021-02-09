#!/usr/bin/python
import random
import requests
import sys, getopt
import time
from datetime import datetime
from threading import Thread

SERVER_URL = "http://localhost:5000"
DEVICE_STATUS = ["ON", "OFF", "ACTIVE", "INACTIVE"]

def device_worker(id):
    """
    Send a randomized payload to devicedata endpoint every 1-5 seconds.
    """
    while True:
        data = {
            "deviceId": "device_{}".format(id),
            "timestamp": datetime.now().isoformat(),
            "status": random.choice(DEVICE_STATUS),
            "pressure": round(random.uniform(0.0, 25.0), 2),
            "temperature": round(random.uniform(0.0, 200.0), 2),
        }
        resp = requests.post(url="{}/devicedata".format(SERVER_URL), json=data)
        if resp:
            print(resp.json())

        # randomize interval between 1-10 seconds
        time.sleep(random.randint(1,10))

def simulate_devices(argv):
    """
    Starts a daemon thread for each simulated devices (default 10).
    """
    num_devices = 10
    try:
        opts, args = getopt.getopt(argv,"hn:",["num_devices="])
    except getopt.GetoptError:
        print('Usage: device_simulator.py -n <num_devices>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: device_simulator.py -n <num_devices>')
            sys.exit()
        elif opt in ("-n", "--num_devices"):
            num_devices = int(arg)

    threads = []
    for i in range(1, num_devices+1):
        t = Thread(target=device_worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    # keep main thread alive until interrupt
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    simulate_devices(sys.argv[1:])
