# 医院可视化大屏平台 (Hospital Visualization Platform)

(此处保留之前 README 原内容)

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
查看日志：
```
docker logs -f mock-sensor
```

### 2. 使用脚本 (需要本机安装 mosquitto-clients 或 Python)
Shell 版本：
```
chmod +x scripts/publish_mock.sh
./scripts/publish_mock.sh 5
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
编辑 `scripts/publish_mock.py` 或 `services/mock-sensor/mock_sensor.py` 中的 `METRICS` 列表即可。
