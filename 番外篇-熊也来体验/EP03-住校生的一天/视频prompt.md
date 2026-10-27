# EP03 · 熊也来体验｜住校生的一天（视频 prompt）

> 栏目：**熊也来体验 EP.03** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**（早八窗口与学生作息重合）
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）
>
> 同类实证：「熊 的住校日常（**live动图**）」9580 赞——**这一期特别适合走动效**（同类爆款就是动图形式）。优先用 A4 的动画帧方案，不要只用静帧。

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜住校生的一天
```

**正文**
```
熊今天上完了所有课，代价是把明天的觉先睡了。

熊也来体验 EP.03｜住校篇
人，还在住校的举个手 🙋
你们宿舍熄灯后聊到几点？报个时间。
```

**话题**：`#自嘲熊` `#自嘲熊日常` `#住校日常` `#宿舍日常` `#学生党` `#早八` `#校园日常`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 熊也来体验<br>住校生的一天 | 背包、站着<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: standing with a small simple backpack, a plain bunk bed frame outline behind, soft morning blue background, generous negative space` | 晨光蓝 / 奶油白 |
| **2** | 06:50 早八<br>熊的身体先起来了<br>灵魂还在被子里 | 没醒、趴坐<br>`3542043-health` / `1338653-5-5`<br>选用：`____` | `scene: sitting on the edge of a plain bed, a rumpled blanket beside, pale dawn light through a simple window, blue-grey background` | 蓝灰 / 米白 |
| **3** | 14:00 图书馆<br>熊翻了一页<br>睡了四十分钟 | 睡着、趴着<br>`3542043-health`<br>选用：`____` | `scene: lying face down on one open plain book, quiet beige background, flat soft lighting` | 米白 / 浅棕 |
| **4** | 18:00 室友带了饭<br>熊今天被爱了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one small simple lunch box and one tiny heart beside the character, warm orange background, soft and quiet` | 暖橘 / 奶油白 |
| **5** | 20:00 洗澡<br>热水在最后五分钟来了 | 呆住、静止<br>`10689991-somehow`<br>选用：`____` | `scene: standing under three very thin vertical water lines, misty pale blue background, minimal` | 雾蓝 / 浅灰 |
| **6**<br>尾帧 | 熊今天上完了所有课<br>给熊记一功 | 举手、轻微得意<br>`1007666-pack`<br>选用：`____` | `scene: raising one short arm, plain light blue gradient background, lots of empty space at the bottom for text` | 浅蓝渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.03`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**
- 道具程序绘制线框：上下铺 = 两横四竖；书 = 两个平行四边形；水线 = 三条细竖线；饭盒 = 圆角矩形 + 一条盖线
- **不出现真实校名、校徽、真实宿舍照片、真人**
- 字体：细软圆润手写体；一帧一句；情绪轻松略社恐，**不写"青春真好"这类抒情**
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP03-住校生的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 住校生的一天.mp4
```

**本期重点：用动画帧做真动效（同类爆款是 live 动图形式）**

`frames/` 里 3229 帧全部来自官方动画贴图，同一 sticker 的连续帧直接播就是官方原版动效：

```bash
cd ../../jokebear-ref
# 1. 先找一个"没睡醒/趴着"的动画贴图，看它有多少帧
ls frames/8874-keeps-moving/ | sed 's/_f[0-9]*\.png//' | sort -u | head -20

# 2. 把该 sticker 的帧序列导成透明 loop（12fps）
ffmpeg -y -framerate 12 -i 'frames/8874-keeps-moving/<stickerid>_f%02d.png' \
  -vf "scale=540:-1" -c:v png /tmp/bear_loop.mov
```
再把 `bear_loop.mov` 叠到背景 + 文字层上。可选动画包：`8874-keeps-moving`、`10096-keeps-moving-2`、`17409-keeps-moving-3`、`1349939-move`、`3147970-move2`、四季 move 包。

> ffmpeg 已装好（`~/.local/bin/ffmpeg`，静态二进制 9.0.1）。

---

## 五、路线 B 用法

首帧必须喂官方贴图（image-to-video），prompt = [形象锁定正面] + [上表 scene 句] + [动效句]，负面词全带；全文见 [02-通用视频prompt模板.md](../02-通用视频prompt模板.md) B2–B3。

**还原度七项验收（任一不过就弃用该帧）**
- [ ] 眼睛两个纯黑小圆点，无高光/眼白/睫毛
- [ ] 嘴是紧闭小 ω，没张开没牙
- [ ] 无眉毛、无腮红
- [ ] 四肢光滑椭圆，无手指脚趾
- [ ] 白色平涂，无毛发质感
- [ ] 全程一只熊
- [ ] 无 AI 生成文字

> 本期建议直接用 A4 动画帧方案，比 B 更还原且更省额度。

---

## 六、置顶评论（发布后 1 小时内，必做）

```
🙋 熊也来体验 EP.03｜住校篇

熊今天的时间表：
06:50 身体先起来了，灵魂还在被子里
14:00 翻了一页，睡了四十分钟
18:00 室友带了饭，熊被爱了
20:00 热水在最后五分钟来了

人，还在住校的举个手。
你们宿舍熄灯后聊到几点？报个时间 🌙
下一期熊去体验什么？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 优先使用动画帧方案（同类爆款是动图形式）
- [ ] 配乐用小红书站内音乐
- [ ] 标题含栏目名 +「住校生」
- [ ] 7 个话题逐个点选生效
- [ ] 无真实校名 / 校徽 / 真人
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| 熊+住校能否复现同类 9580 赞的量级 | 观看数 | ≥ 1500 |
| 动画帧动效是否优于静帧切换 | 平均观看时长 | ≥ 9 秒（静帧期为 ≥8 秒） |
| 校园线 vs 打工线哪条更强 | 与 EP.01/02 观看对比 | 记录，决定后续配比 |
| 学生党认领欲 | 明确说自己住校的评论条数 | ≥ 8 |
| 校园线涨粉能力 | 涨粉 | ≥ 5 |
