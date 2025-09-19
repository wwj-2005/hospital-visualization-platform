import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';
import axios from 'axios';

export default function Home() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [metric, setMetric] = useState<any>(null);

  useEffect(() => {
    // 简单加载 HLS 视频
    const hlsUrl = process.env.NEXT_PUBLIC_STREAM_BASE + "/cam1/index.m3u8";
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(hlsUrl);
      hls.attachMedia(videoRef.current!);
    } else if (videoRef.current?.canPlayType('application/vnd.apple.mpegurl')) {
      videoRef.current.src = hlsUrl;
    }

    axios.get(process.env.NEXT_PUBLIC_API_BASE + "/metrics/last", {
      params: { device_id: "TEMP-001", metric: "temperature" }
    }).then(r => setMetric(r.data)).catch(()=>{});
  }, []);

  return (
    <div className="min-h-screen bg-neutral-900 text-white p-6">
      <h1 className="text-3xl font-semibold mb-4">医院运行大屏 (MVP)</h1>
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-neutral-800 p-4 rounded">
          <h2 className="text-xl mb-2">实时视频</h2>
          <video ref={videoRef} controls autoPlay style={{width:'100%', background:'#000'}} />
        </div>
        <div className="bg-neutral-800 p-4 rounded">
          <h2 className="text-xl mb-2">温度示例</h2>
            {metric ? (
              <div className="text-4xl font-bold">
                {metric.value} {metric.unit}
                <div className="text-sm mt-2 opacity-60">{metric.time}</div>
              </div>
            ) : <div>加载中...</div>}
        </div>
      </div>
    </div>
  );
}