from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

app = FastAPI(title="Hospital Visualization API", version="0.1.0")

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

class MeasurementIn(BaseModel):
    device_id: str
    metric: str
    value: float
    unit: str

@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time()}

@app.post("/measurements")
def ingest(m: MeasurementIn):
    p = Point("measurement") \
        .tag("device_id", m.device_id) \
        .tag("metric", m.metric) \
        .field("value", m.value) \
        .tag("unit", m.unit)
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
    return {"status": "stored"}

@app.get("/metrics/last")
def last_metric(device_id: str, metric: str):
    q = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -30m)
      |> filter(fn: (r) => r["device_id"] == "{device_id}" and r["metric"] == "{metric}")
      |> last()
    '''
    tables = query_api.query(q)
    out = []
    for table in tables:
        for record in table.records:
            out.append({
                "time": record.get_time().isoformat(),
                "value": record.get_value(),
                "unit": record.values.get("unit")
            })
    if not out:
        raise HTTPException(404, "No data")
    return out[0]