import os, json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

MQTT_HOST = os.getenv("MQTT_BROKER_URL","mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT","1883"))

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    print("MQTT connected", rc)
    client.subscribe("hospital/+/+/+/+/metrics")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload.get("device_id") or msg.topic.split("/")[4]
        metric = payload["metric"]
        value = float(payload["value"])
        unit = payload.get("unit","")
        p = Point("measurement").tag("device_id", device_id).tag("metric", metric).tag("unit", unit).field("value", value)
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
    except Exception as e:
        print("Ingestion error:", e)

def main():
    c = mqtt.Client()
    c.on_connect = on_connect
    c.on_message = on_message
    c.connect(MQTT_HOST, MQTT_PORT, 60)
    c.loop_forever()

if __name__ == "__main__":
    main()