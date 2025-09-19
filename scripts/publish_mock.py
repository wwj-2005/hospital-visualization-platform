#!/usr/bin/env python3
import os, time, json, random, argparse
import paho.mqtt.client as mqtt

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=int(os.getenv("MOCK_INTERVAL_SECONDS", "5")))
    ap.add_argument("--count", type=int, default=int(os.getenv("MOCK_DEVICE_COUNT", "3")))
    ap.add_argument("--building", default=os.getenv("MOCK_BUILDING", "A"))
    ap.add_argument("--floor", default=os.getenv("MOCK_FLOOR", "3"))
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", type=int, default=1883)
    return ap.parse_args()

METRICS = [
    ("temperature","C", 22, 28),
    ("humidity","%", 40, 65),
    ("pm25","ug/m3", 10, 80),
    ("energy","kWh", 3, 20),
    ("heart_rate","bpm", 55, 120)
]

def main():
    args = parse_args()
    client = mqtt.Client()
    client.connect(args.host, args.port, 60)
    print(f"Mock publisher started interval={args.interval}s count={args.count}")
    dev_ids = [f"DEV-{i:03d}" for i in range(1, args.count+1)]
    while True:
        for dev in dev_ids:
            metric, unit, lo, hi = random.choice(METRICS)
            value = round(random.uniform(lo, hi), 2)
            topic = f"hospital/{args.building}/{args.floor}/{metric}/{dev}/metrics"
            payload = {
                "metric": metric,
                "value": value,
                "unit": unit,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "device_id": dev
            }
            client.publish(topic, json.dumps(payload))
        print(f"[Batch published {len(dev_ids)}] {time.strftime('%H:%M:%S')}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()