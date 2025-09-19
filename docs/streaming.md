# 视频流策略

## MVP
RTSP → mediamtx 自动输出 HLS。延迟 2~5s 可接受。

## 升级为 WebRTC
方案：
1. 引入 LiveKit / Janus / SRS
2. ffmpeg 推流到 WebRTC SFU
3. 前端用 WebRTC 播放 (低延迟 <1s)

## Token 保护
- 访问 /token/stream 获取短期 JWT
- Nginx/网关校验 token 再代理流 (生产实现)

## FFmpeg 示例
ffmpeg -rtsp_transport tcp -i rtsp://USER:PASS@camera-ip/Streaming/Channels/101 \
-c copy -f rtsp rtsp://localhost:8554/cam1