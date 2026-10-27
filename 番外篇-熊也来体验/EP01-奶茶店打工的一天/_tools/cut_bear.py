#!/usr/bin/env python3
"""
U2Net 抠图 v3（最终版）
- 形态学重建去掉「细连接附件」（吊牌、挂扣带）
- back 用头部左右对称做镜像修补（挂扣与头重叠，只能镜像）
- 不做全局灰度脏点清除（会误伤熊自身的暗部）
"""
import os
import cv2
import numpy as np
import onnxruntime as ort

SRC = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/jokebear_全照"
BASE = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/番外篇-熊也来体验/EP01-奶茶店打工的一天"
OUT = os.path.join(BASE, "_assets")
os.makedirs(OUT, exist_ok=True)

# u2net.onnx 有 168MB，不要放进 git 仓库。
# 解析顺序：环境变量 U2NET_PATH -> 仓库内 _tools -> 用户缓存目录
MODEL = None
for cand in (os.environ.get("U2NET_PATH"),
             os.path.join(BASE, "_tools", "u2net.onnx"),
             os.path.expanduser("~/.cache/jokebear/u2net.onnx")):
    if cand and os.path.exists(cand):
        MODEL = cand
        break
if MODEL is None:
    raise SystemExit(
        "缺少 u2net.onnx，先下载：\n"
        "  mkdir -p ~/.cache/jokebear && "
        "curl -L -o ~/.cache/jokebear/u2net.onnx "
        "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx\n"
        "（国内网络需带代理，例：export HTTPS_PROXY=http://127.0.0.1:7897）")
print("模型:", MODEL)

MEAN = np.array([0.485, 0.456, 0.406], np.float32)
STD = np.array([0.229, 0.224, 0.225], np.float32)
sess = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
IN_NAME = sess.get_inputs()[0].name
FILES = {"front": "正面.jpeg", "left": "左边.jpeg", "right": "右侧.jpeg", "back": "背面.jpeg"}


def coarse_bbox(gray):
    h, w = gray.shape
    for th in (150, 160, 170, 180, 190):
        m = (gray > th).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((35, 35), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
        best = None
        for i in range(1, n):
            x, y, bw, bh, area = stats[i]
            if x <= 2 or x + bw >= w - 2 or y + bh >= h - 2:
                continue
            if 0.25 * w < x + bw / 2 < 0.75 * w and y + bh / 2 > 0.5 * h and area > 0.02 * w * h:
                if best is None or area > best[0]:
                    best = (area, x, y, bw, bh)
        if best:
            return best[1:]
    return None


def predict(rgb):
    im = cv2.resize(rgb, (320, 320), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    im = im / max(im.max(), 1.0)
    t = np.zeros_like(im)
    for c in range(3):
        t[:, :, c] = (im[:, :, c] - MEAN[c]) / STD[c]
    out = sess.run(None, {IN_NAME: t.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    lo, hi = float(out.min()), float(out.max())
    return (out - lo) / max(hi - lo, 1e-6)


def largest(m):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        return m
    return np.where(lab == 1 + int(np.argmax(stats[1:, 4])), 255, 0).astype(np.uint8)


def reconstruct(marker, limit, iters=200):
    """测地膨胀：把 marker 在 limit 内部膨胀到不能再扩（形态学重建）"""
    k3 = np.ones((3, 3), np.uint8)
    prev = marker.copy()
    for _ in range(iters):
        dil = cv2.bitwise_and(cv2.dilate(prev, k3), limit)
        if np.array_equal(dil, prev):
            return prev
        prev = dil
    return prev


def cut(name, fn, ksize=41):
    bgr = cv2.imread(os.path.join(SRC, fn), cv2.IMREAD_COLOR)
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    x, y, bw, bh = coarse_bbox(gray)
    mx, my = int(bw * 0.45), int(bh * 0.35)
    cx0, cy0 = max(0, x - mx), max(0, y - my)
    cx1, cy1 = min(w, x + bw + mx), min(h, y + bh + my)

    sal = predict(cv2.cvtColor(bgr[cy0:cy1, cx0:cx1], cv2.COLOR_BGR2RGB))
    sal = cv2.resize(sal, (cx1 - cx0, cy1 - cy0), interpolation=cv2.INTER_LINEAR)
    full = np.zeros((h, w), np.float32)
    full[cy0:cy1, cx0:cx1] = sal

    hard = largest((full > 0.5).astype(np.uint8) * 255)
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    before = (hard > 0).sum()

    core = largest(cv2.erode(hard, np.ones((ksize, ksize), np.uint8)))
    body = reconstruct(core, hard)
    dropped = before - (body > 0).sum()
    print(f"[{name}] 形态学重建丢弃细附件 {dropped} px ({dropped/before:.1%})")

    cnts, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid = np.zeros_like(body)
    cv2.drawContours(solid, cnts, -1, 255, -1)

    bgr_clean = bgr.copy()
    if name == "back":
        # 头部左右镜像修补：去掉与头重叠的挂扣，并把轮廓补圆。
        # 轴要按熊体实际中心算（不能写死，bbox 含挂扣会偏右）
        # 注意：mask 与 RGB 必须一起镜像，否则被抹掉的挂扣像素还会透出来
        band = solid[int(y + 0.05 * bh):int(y + 0.35 * bh), :]
        xs_ = np.where(band.sum(axis=0) > 0)[0]
        ax = int((xs_.min() + xs_.max()) / 2)
        ylim = int(y + bh * 0.60)
        print(f"[{name}] 镜像轴 x={ax}  ylim={ylim}")
        src = solid.copy()
        for xx in range(ax, w):
            sx = 2 * ax - xx
            if sx < 0:
                solid[:ylim, xx] = 0
            else:
                solid[:ylim, xx] = src[:ylim, sx]
                bgr_clean[:ylim, xx] = bgr[:ylim, sx]
        solid = largest(cv2.morphologyEx(solid, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8)))

    a = np.clip((full - 0.35) / 0.30, 0, 1)
    a = np.minimum(a, (solid > 0).astype(np.float32))
    a[cv2.erode(solid, np.ones((9, 9), np.uint8)) > 0] = 1.0
    a = cv2.GaussianBlur(a, (0, 0), 1.2)

    # 注意：这里绝对不能再做「全局暗像素 inpaint」——
    # 熊的眼睛/嘴也是暗像素，一起抹掉会把脸弄没（IP 辨识度的红线）。
    # 吊牌由后续 fix_artifacts.py 按色彩/位置定向清除。
    clean = bgr_clean

    rgba = cv2.cvtColor(clean, cv2.COLOR_BGR2BGRA)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    ys, xs = np.where(a > 0.05)
    crop = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(os.path.join(OUT, f"bear_{name}.png"), crop)
    print(f"[{name}] -> {crop.shape[1]}x{crop.shape[0]}")


for kk, vv in FILES.items():
    cut(kk, vv)
print("done")
