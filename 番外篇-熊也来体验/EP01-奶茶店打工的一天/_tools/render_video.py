#!/usr/bin/env python3
"""
渲染带「呼吸感」的视频：把 6 张静帧按 2.2 秒/帧铺成 30fps 序列，
对每一输出帧做一次轻微缩放裁切。

相比 ffmpeg 的 zoompan 一次性写法，这里的好处是：
  - 缩放是「全片连续」的，不会每切一帧就弹回 1.0（那种跳变很显眼）
  - 帧内再叠一个周期正好等于 2.2 秒的正弦微呼吸，切帧处幅值相接，平滑
总时长严格 6 × 2.2 = 13.2 秒。
"""
import os
import subprocess
import numpy as np
from PIL import Image

BASE = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/番外篇-熊也来体验/EP01-奶茶店打工的一天"
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
W, H = 1080, 1440
FPS = 30
PER_FRAME = 66                 # 2.2s * 30fps
NFRAMES = 6
UP = 1.15                      # 先放大再裁，保证缩放后不糊

src = []
for i in range(1, NFRAMES + 1):
    im = Image.open(os.path.join(BASE, f"{i:02d}.png")).convert("RGB")
    im = im.resize((int(W * UP), int(H * UP)), Image.LANCZOS)
    src.append(np.array(im))

total = PER_FRAME * NFRAMES

cmd = [FFMPEG, "-y", "-loglevel", "error",
       "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
       os.path.join(BASE, "奶茶店打工的一天.mp4")]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

for k in range(total):
    f = min(k // PER_FRAME, NFRAMES - 1)
    local = k % PER_FRAME
    p = k / (total - 1)
    # 全片缓慢推近 1.5% -> 5%，叠一个 2.2s 周期的 ±1% 微呼吸
    s = 1.015 + 0.035 * p + 0.010 * np.sin(2 * np.pi * local / PER_FRAME)
    cw, ch = int(W * UP / s), int(H * UP / s)
    x0, y0 = (src[f].shape[1] - cw) // 2, (src[f].shape[0] - ch) // 2
    crop = Image.fromarray(src[f][y0:y0 + ch, x0:x0 + cw]).resize((W, H), Image.LANCZOS)
    proc.stdin.write(np.asarray(crop, np.uint8).tobytes())

proc.stdin.close()
proc.wait()
print("done", os.path.join(BASE, "奶茶店打工的一天.mp4"), "frames=", total)
