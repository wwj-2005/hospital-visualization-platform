# 架构说明

## 数据流
摄像头 → RTSP → mediamtx → HLS → 前端 video
传感器 → MQTT → ingestion 服务 → InfluxDB → API 查询 → 前端展示

## 模块边界
- api: REST + (后续 WebSocket)
- ingestion: 统一消费 MQTT → 标准化写库
- stream-gateway: 发放临时流 Token（后期对接 WebRTC 信令）
- frontend: 可视化大屏
- 时序库: InfluxDB
- 缓存与会话: Redis
- 消息: MQTT

## 后续扩展
- 告警引擎：基于规则（阈值 / 滑动窗口）
- AI 分析：独立 microservice 产生结构化事件
- WebRTC：替换/并行 HLS 以降低延迟