# 医院可视化大屏平台 (Hospital Visualization Platform)

## 目标
构建一个高可扩展、低延迟（逐步实现）、高端视觉风格的医院运行状态与视频监控统一展示平台。

## 核心特性 (MVP)
- 多路摄像头实时监看（初期 HLS，预留 WebRTC）
- 传感器数据接入（MQTT）
- 大屏指标：床位使用率、环境参数（温湿度、PM2.5）、设备在线率
- 告警基础框架
- 可配置布局（后期）

## 架构概览
详见 [docs/architecture.md](docs/architecture.md)

## 快速启动
1. 复制环境变量模板：
   cp .env.example .env  (Windows PowerShell 用：Copy-Item .env.example .env)
2. 启动：
   docker compose up -d --build
3. 前端访问：
   http://localhost:3000
4. API 文档 (FastAPI):
   http://localhost:8000/docs

## 技术栈
Frontend: Next.js + TS + Tailwind + ECharts  
Backend: FastAPI + InfluxDB + Redis + MQTT  
Streaming: rtsp-simple-server (mediamtx) + FFmpeg (HLS)  
Auth: 简易 JWT（后期 Keycloak）  

## Roadmap (阶段)
1. MVP：HLS 视频 + 传感器写入 + 大屏指标
2. 增强：告警规则、角色权限、WebRTC 低延迟
3. 智能化：AI 视频分析、能耗预测
4. 集成：FHIR/HL7 接入、设备统一资产管理

## 模拟数据 (新增章节)

### 1. 使用 Docker 内置 mock-sensor
在 `.env` 中调整：
```
MOCK_INTERVAL_SECONDS=5
MOCK_DEVICE_COUNT=3
```
启动：
```
docker compose up -d mock-sensor
```
日志：
```
docker logs -f mock-sensor
```

### 2. 使用脚本 (本机需安装 mosquitto-clients 或 Python)
Shell 版本：
```
chmod +x scripts/publish_mock.sh
./scripts/publish_mock.sh 5
```
Windows PowerShell:
```
bash scripts/publish_mock.sh 5   # 在 Git Bash 或 WSL 下
```
Python 版本：
```
python scripts/publish_mock.py --interval 5 --count 5
```

### 3. 查询最新数据
```
curl "http://localhost:8000/metrics/last?device_id=DEV-001&metric=temperature"
```

### 4. 修改指标范围
编辑 `scripts/publish_mock.py` 或 `services/mock-sensor/mock_sensor.py` 内的 METRICS 列表。

## License
内部使用（按需添加）。