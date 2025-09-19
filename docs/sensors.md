# 传感器数据模型与主题

## Topic 结构
hospital/{building}/{floor}/{deviceType}/{deviceId}/metrics

## 示例
Topic:
hospital/A/2/temperature/TEMP-001/metrics
Payload:
{
  "metric":"temperature",
  "value":23.6,
  "unit":"C",
  "ts":"2025-09-19T02:30:11Z"
}

## 告警规则（预留）
格式（草案）：
{
  "id": "rule-high-temp",
  "metric": "temperature",
  "op": ">",
  "threshold": 30,
  "duration": "5m",
  "level": "warning"
}