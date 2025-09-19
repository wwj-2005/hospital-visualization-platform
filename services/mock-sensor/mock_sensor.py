import os, time, json, random
import paho.mqtt.client as mqtt

INTERVAL = int(os.getenv("INTERVAL","5"))
COUNT = int(os.getenv("COUNT","3"))
BUILDING = os.getenv("BUILDING","A")
FLOOR = os.getenv("FLOOR","3")
HOST = os.getenv("MQTT_HOST","mqtt-broker")
PORT = int(os.getenv("MQTT_PORT","1883"))

METRICS = [
    ("temperature","C", 22, 28),
    ("humidity","%", 40, 65),
    ("pm25","ug/m3", 10, 80),
    ("energy","kWh", 3, 20),
    ("heart_rate","bpm", 55, 120)
]

def main():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    device_ids = [f"MOCK-{i:03d}" for i in range(1, COUNT+1)]
    print(f"[mock-sensor] started interval={INTERVAL}s devices={device_ids}")
    while True:
        for dev in device_ids:
            metric, unit, lo, hi = random.choice(METRICS)
            value = round(random.uniform(lo, hi), 2)
            topic = f"hospital/{BUILDING}/{FLOOR}/{metric}/{dev}/metrics"
            payload = {
                "metric": metric,
                "value": value,
                "unit": unit,
                "device_id": dev,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            client.publish(topic, json.dumps(payload))
        print(f"[mock-sensor] published batch at {time.strftime('%H:%M:%S')}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()