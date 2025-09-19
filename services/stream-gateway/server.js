import express from "express";
import jwt from "jsonwebtoken";
import cors from "cors";

const app = express();
app.use(cors());

const JWT_SECRET = process.env.API_JWT_SECRET || "changeme";

app.get("/token/stream", (req, res) => {
  const { camera="cam1" } = req.query;
  const token = jwt.sign({ camera, exp: Math.floor(Date.now()/1000)+60 }, JWT_SECRET);
  res.json({ token });
});

// TODO: 在生产中校验 token 后再允许访问实际流（Nginx 层或自定义签名 URL）
app.listen(9000, () => console.log("Stream gateway on 9000"));