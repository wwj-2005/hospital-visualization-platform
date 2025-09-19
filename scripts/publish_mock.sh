#!/usr/bin/env bash
# 简易循环模拟传感器数据推送 (需要安装 mosquitto-clients)
# 用法: ./scripts/publish_mock.sh [间隔秒] (默认 5)
INTERVAL=${1:-5}

BUILDING=${MOCK_BUILDING:-A}
FLOOR=${MOCK_FLOOR:-3}

echo "Starting mock publisher: interval=${INTERVAL}s building=${BUILDING} floor=${FLOOR}"
echo "Press Ctrl+C to stop."

while true; do
  # 温度
  VALUE_T=$(awk -v min=22 -v max=27 'BEGIN{srand(); print min+rand()*(max-min)}')
  mosquitto_pub -h localhost -t hospital/${BUILDING}/${FLOOR}/temperature/TEMP-001/metrics \
    -m "{\"metric\":\"temperature\",\"value\":${VALUE_T},\"unit\":\"C\"}"

  # 湿度
  VALUE_H=$(awk -v min=40 -v max=60 'BEGIN{srand(); print min+rand()*(max-min)}')
  mosquitto_pub -h localhost -t hospital/${BUILDING}/${FLOOR}/humidity/HUM-201/metrics \
    -m "{\"metric\":\"humidity\",\"value\":${VALUE_H},\"unit\":\"%\"}"

  # PM2.5
  VALUE_PM=$(awk -v min=15 -v max=55 'BEGIN{srand(); print min+rand()*(max-min)}')
  mosquitto_pub -h localhost -t hospital/${BUILDING}/${FLOOR}/pm25/AIR-301/metrics \
    -m "{\"metric\":\"pm25\",\"value\":${VALUE_PM},\"unit\":\"ug/m3\"}"

  # 能耗 (kWh)
  VALUE_EN=$(awk -v min=5 -v max=15 'BEGIN{srand(); print min+rand()*(max-min)}')
  mosquitto_pub -h localhost -t hospital/${BUILDING}/${FLOOR}/energy/EN-401/metrics \
    -m "{\"metric\":\"energy\",\"value\":${VALUE_EN},\"unit\":\"kWh\"}"

  # 心率 (bpm)
  VALUE_HR=$(awk -v min=60 -v max=110 'BEGIN{srand(); print min+rand()*(max-min)}')
  mosquitto_pub -h localhost -t hospital/${BUILDING}/${FLOOR}/heartrate/HR-501/metrics \
    -m "{\"metric\":\"heart_rate\",\"value\":${VALUE_HR},\"unit\":\"bpm\"}"

  echo "[Mock Published] $(date '+%H:%M:%S')"
  sleep ${INTERVAL}
done