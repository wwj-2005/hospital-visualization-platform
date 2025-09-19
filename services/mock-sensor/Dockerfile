FROM python:3.11-slim
WORKDIR /app
RUN pip install paho-mqtt
COPY mock_sensor.py .
ENV INTERVAL=5 COUNT=3 BUILDING=A FLOOR=3 MQTT_HOST=mqtt-broker MQTT_PORT=1883
CMD ["python","mock_sensor.py"]