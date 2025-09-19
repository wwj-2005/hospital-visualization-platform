# API 概要 (MVP)

GET /health
POST /measurements
  body: { device_id, metric, value, unit }
GET /metrics/last?device_id=...&metric=...

后续：
GET /devices
POST /devices
GET /metrics/range
WS /realtime (推送告警/最新值)