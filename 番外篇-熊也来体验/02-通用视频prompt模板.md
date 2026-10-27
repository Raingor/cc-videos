# 番外篇 · 通用视频 prompt 模板

> 用途：开新一期番外篇视频时，复制本文件改成 `EPnn-<职业>的一天/视频prompt.md`。
> 依据：[00-番外篇总企划.md](00-番外篇总企划.md) 第六节制作路线
> 素材：[jokebear-ref/README.md](../jokebear-ref/README.md)（1202 静态贴图 + 3229 动画帧）

---

## 先决定走哪条路线

| | 路线 A：官方贴图合成 | 路线 B：AI 图生视频 |
|---|---|---|
| 熊的还原度 | **100%**，本体就是官方原图 | 中等，脸部有走形风险 |
| 动效 | 静帧切换 / 动画帧序列 | 真动效（呼吸、眨眼、摆动） |
| 用在哪 | **默认主力**，所有期 | 需要动感的期，或封面首帧动效 |
| 前置条件 | 需要 ffmpeg（**已装好**） | 需要 AI 视频工具额度 |

**默认走 A。** 上一轮已确认：AI 生成的熊脸（无眉 + 两个黑点眼 + 紧凑 ω 嘴）必然走形，这是本系列还原度的唯一红线。

### ffmpeg 安装状态（2026-09-03 完成）

```
~/.local/bin/ffmpeg    ffmpeg 9.0.1-tessus（静态二进制）
~/.local/bin/ffprobe   ffprobe 9.0.1-tessus
```

**不是用 brew 装的。** `brew install ffmpeg` 在本机会在 `sdl3` 依赖处失败（Command Line Tools 版本过旧，需要 Xcode 26.3 CLT 才能从源编译）。改用 evermeet.cx 的静态构建，无需编译、无需 sudo。

重装方式（换机器或文件丢了时）：
```bash
curl -sL -o /tmp/ffmpeg.zip https://evermeet.cx/ffmpeg/getrelease/zip
unzip -o -q /tmp/ffmpeg.zip -d /tmp/ffmpeg_bin
mkdir -p ~/.local/bin && cp /tmp/ffmpeg_bin/ffmpeg ~/.local/bin/
chmod +x ~/.local/bin/ffmpeg && xattr -d com.apple.quarantine ~/.local/bin/ffmpeg 2>/dev/null
ffmpeg -version | head -1
```

**端到端已实测通过**：取 6 张官方贴图（`10033892-comic`）→ 1080×1440 贴图帧 → 合成得到 **13.20 秒** mp4，与本文档的 6 帧 × 2.2 秒规格完全对得上。

---

## 路线 A：官方贴图合成（主力）

### A1. 每帧的三件事

一帧 = 官方贴图熊（不动）+ 纯色/极简背景（程序画）+ 一句文字（程序画）。
**不要让任何 AI 参与熊本体的生成。**

### A2. 帧序列规格

| 项 | 值 |
|---|---|
| 尺寸 | 1080×1440（3:4，与九宫格素材管线共用） |
| 帧数 | 6–7 帧（封面 1 + 时间节点 4–5 + 尾帧 1） |
| 每帧时长 | 2.2–2.4 秒 |
| 总时长 | **≥ 12 秒**（本号 5–6 秒的视频涨粉最差，7.9 秒那条涨了 7 粉） |
| 命名 | `01.png` … `07.png` |
| 声音 | **导出无声**，配乐在小红书发布器内选站内音乐（规避版权 + 吃音乐流量） |

### A3. 合成命令

```bash
cd 番外篇-熊也来体验/EPnn-<职业>的一天
# 2.2 秒/帧；帧数改了记得同步 -framerate
ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart <职业>的一天.mp4
```

想让静帧有一点呼吸感（轻微缩放，成本几乎为零）：
```bash
ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1188:1584,zoompan=z='min(zoom+0.0006,1.06)':d=66:s=1080x1440,fps=30" \
  -c:v libx264 -pix_fmt yuv420p <职业>的一天.mp4
```

### A4. 用动画帧做真动效（比静帧更好，仍是官方素材）

`frames/` 里 3229 帧是官方动画贴图逐帧拆出来的，同一个 sticker 的连续帧可以直接当动画播：

```bash
# 例：把某个动画贴图的所有帧按 12fps 播 → 得到官方原版动效
cd jokebear-ref
ls frames/8874-keeps-moving/ | head -3     # 看命名：<stickerid>_f00.png ...
ffmpeg -y -framerate 12 -i 'frames/8874-keeps-moving/14406085_f%02d.png' \
  -vf "scale=540:-1" -c:v png /tmp/bear_loop.mov
```
再把这个 loop 叠到背景+文字上，就是 100% 还原 + 有动效。**这是本系列最优解。**

### A5. 贴图检索 prompt（给出图脚本 / 给自己看）

不是给 AI 的 prompt，是挑图条件。写成这样，谁来做都不会挑错：

```
帧 2  | 需要：站着、身体前倾、看起来还没醒
       候选包：10033892-comic / 3542043-health
       实际选用：<pack>/<id>.png
帧 3  | 需要：双手在忙、低头
       候选包：1007666-pack / 10689991-somehow
帧 6  | 需要：轻微开心、被安慰的样子（回血格）
       候选包：1310872-s-love / 1438683-s-love2
```

挑图方式：打开 `jokebear-ref/contact_all.png`（1202 张总览）肉眼找，记下 id。

---

## 路线 B：AI 图生视频（补充）

### B1. 铁律：必须用官方贴图当首帧

**只用图生视频（image-to-video），绝不用文生视频（text-to-video）。**
首帧喂官方贴图 → 模型只负责让它动，不负责画它的脸。这是把走形风险压到最低的唯一办法。

### B2. 形象锁定 prompt（每次都要带，不要省）

**正面（英文效果通常更稳，中文工具用中文版）**
```
a simple flat 2D cartoon white bear mascot, wide rounded oval head,
small round body, short stubby oval limbs with no visible fingers or toes,
two tiny black dot eyes, small black nose, tiny closed omega-shaped mouth,
no eyebrows, no blush, no teeth, clean thin dark outline, flat minimal shading,
solid pastel background, generous negative space, centered composition
```

**中文版**
```
极简扁平二维卡通白熊：横向椭圆大头，小圆身体，短椭圆四肢无手指脚趾，
两个小黑点眼睛，小黑鼻，紧闭的小 ω 形嘴，无眉毛，无腮红，无牙齿，
细深色描边，平涂极简阴影，纯色浅底，大量留白，居中构图
```

**负面 prompt（走形都是这些造成的，必须全带）**
```
realistic bear, fur, fur texture, brown bear, grizzly, teddy bear,
eyebrows, blush, rosy cheeks, big shiny eyes, sparkle eyes, eyelashes,
open mouth, teeth, tongue, human hands, fingers, toes, claws,
3D render, glossy, plastic, metallic, depth of field, bokeh,
complex background, cluttered scene, text, letters, watermark, logo, signature,
extra limbs, deformed face, multiple bears, anime girl, human character,
mascot costume, photo, photorealistic
```

### B3. 动效 prompt（只要微动，不要镜头运动）

```
subtle idle animation only: gentle body bob, slight head tilt, occasional blink,
tiny arm sway. camera completely static, no zoom, no pan, no dolly.
character stays centered and fully in frame. loop-friendly. 2 seconds.
```

**踩坑提醒**
- 不要写 "cinematic"、"dynamic camera"、"dramatic lighting" —— 一写熊就开始变形、长毛、镜头乱飞
- 不要让 AI 画文字（`text, letters` 已进负面词），**文字一律后期程序叠加**
- 不要一次生成超过 3 秒，越长越容易崩脸
- 每帧生成 2–3 个候选，挑脸没崩的那个

### B4. 单帧 prompt 模板（复制改场景那一句）

```
[首帧图片：jokebear-ref/<pack>/<id>.png]

<形象锁定 prompt B2 正面>
scene: <一句场景描述，只写背景与道具，不描述熊的长相>
<动效 prompt B3>

negative: <B2 负面 prompt 全文>
```

场景句示例（只写背景道具，不碰熊本体）：
- `behind a simple milk tea shop counter, a few plain cups and a sealing machine, warm cream background`
- `at a plain office desk with a headset and a monitor showing simple chat bubbles, cool grey-blue background`
- `inside a simple car at night, dashboard glow, city lights as soft bokeh-free dots`
- `in a plain dorm room, bunk bed frame outline, dim warm night light`

### B5. 出片后必查（还原度验收）

- [ ] 眼睛是**两个纯黑小圆点**，没有高光、没有眼白、没有睫毛
- [ ] 嘴是**紧闭的小 ω**，没张开、没牙
- [ ] **没有眉毛、没有腮红**
- [ ] 四肢是**光滑椭圆**，没有手指脚趾
- [ ] 白色是**平涂**，没有毛发质感
- [ ] 全程一只熊，没有多出来的肢体
- [ ] 画面里没有 AI 生成的文字

**任一项不过 → 弃用该帧，回退到路线 A 的静帧。** 不要将就，走形的熊会直接砸掉 IP 辨识度。

---

## 文档模板（复制以下全文）

> 注：模板里的 `../` 链接是按 **EP 子目录** 写的（复制到 `EPnn-xxx/` 后即可解析），在本文件位置看是断的，属正常。

```markdown
# EPnn · 熊也来体验｜<职业>打工的一天（视频 prompt）

> 栏目：**熊也来体验 EP.nn** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：<周几> 07:30（早八通勤窗口）
> 制作路线：A 官方贴图合成（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md)

## 一、发布信息
<标题 / 正文 / 话题，与图文版同源但正文更短>

## 二、分镜表

| 帧 | 画面文字 | 贴图选择（路线 A） | 场景 prompt（路线 B 备用） | 配色 |
|:-:|---|---|---|---|
| 1（首帧/封面） | ... | 需要：xxx；候选包：xxx；选用：`<pack>/<id>.png` | `scene: ...` | ... |
| 2–5 | ... | | | |
| 6（尾帧） | ... | | | |

## 三、合成
<ffmpeg 命令，帧数与 framerate 对应>

## 四、置顶评论
<含「下一期点单」>

## 五、发布前核对
<含还原度七项验收 + 时长 ≥12s + 站内配乐>

## 六、本期要验证的假设
```

---

## 与图文版的关系

同一职业**做一份素材、出两条内容**：
1. 先出视频（07:30 发）→ 探量，看哪几句评论区反应最好
2. 3–4 天后出九宫格图文（20:30 发）→ 用验证过的句子，补齐搜索长尾

两者走不同流量池（视频池曝光 ~8000 / 图文池 ~1200–3900），不互相抢量。
