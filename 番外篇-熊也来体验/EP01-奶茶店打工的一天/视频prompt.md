# EP01 · 熊也来体验｜奶茶店打工的一天（视频 prompt）

> 栏目：**熊也来体验 EP.01** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**（早八通勤窗口；本号爆量篇 08:00–12:00 每小时稳定 150+ 观看）
> 制作路线：**A 官方贴图合成**（主力），B 仅在需要动效时用
> 状态：📝 待出片
> 素材目录：`番外篇-熊也来体验/EP01-奶茶店打工的一天/`
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜奶茶店打工的一天
```

**正文**
```
熊今天卖了三百杯，自己一口没喝。

熊也来体验 EP.01｜奶茶店篇
人，有奶茶店的搭子在吗？评论区认领一下 🧋
下一期熊去体验什么职业？评论区点单。
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#奶茶店` `#奶茶店店员` `#打工日常` `#打工人表情包` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

视频取图文版九格里最强的 6 格（去掉 11:00、19:00，节奏更紧）。

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 熊也来体验<br>奶茶店打工的一天 | 站着、略无奈<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: behind a very simple milk tea shop counter, two plain empty cups and a small square sealing machine on the counter, warm cream background, generous negative space` | 奶油白 / 浅棕 |
| **2** | 09:50 开店<br>熊先把封口机预热了<br>（自己还没热） | 没醒、发呆<br>`3542043-health` / `1338653-5-5`<br>选用：`____` | `scene: a small square machine with one tiny red indicator light on a plain counter, soft morning light, pale beige background` | 晨光米 / 浅灰 |
| **3** | 13:00 高峰<br>单子比熊高 | 被压住、仰头<br>`10033892-comic` / `3542043-health`<br>选用：`____` | `scene: one long narrow white receipt strip standing taller than the character, plain warm yellow background, nothing else in frame` | 暖黄 / 米白 |
| **4** | 14:30 有人说少冰<br>熊已经封好口了 | 呆住、静止<br>`10689991-somehow`<br>选用：`____` | `scene: holding one sealed plain cup, completely still, cool grey background, flat lighting` | 冷灰 / 浅棕 |
| **5** | 16:00 有人说了谢谢<br>熊今天回血了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny simple heart floating beside the character, warm orange background, soft and quiet` | 暖橘 / 奶油白 |
| **6**<br>尾帧 | 熊今天卖了三百杯<br>自己一口没喝<br>给熊记一功 | 举杯、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: holding one intact plain cup up, plain warm orange gradient background, lots of empty space at the bottom for text` | 暖橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.01`

---

## 三、出片规范

- 帧尺寸 **1080×1440**（3:4），命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**
- 道具程序绘制：封口机 = 圆角方块 + 小红点；小票 = 细长白条 + 锯齿边；杯子 = 上宽下窄梯形 + 一条封口线。不画真实品牌杯型、不出现 logo、不出现真人
- 字体：细软圆润手写体，一帧一句，字号大、留白多
- **总时长必须 ≥ 12 秒**（本号 5–6 秒的视频涨粉最差；7.9 秒那条涨了 7 粉）
- **导出无声**，配乐在小红书发布器里选站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP01-奶茶店打工的一天"

# 基础版：6 帧 × 2.2 秒 = 13.2 秒
ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 奶茶店打工的一天.mp4

# 带轻微呼吸感（缓慢放大 6%，静帧不那么死）
ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1188:1584,zoompan=z='min(zoom+0.0006,1.06)':d=66:s=1080x1440,fps=30" \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart 奶茶店打工的一天.mp4
```

> ffmpeg 已装好（`~/.local/bin/ffmpeg`，静态二进制 9.0.1）。

**升级选项（推荐，仍是 100% 官方素材）**：把某几帧换成动画帧序列，得到官方原版动效——
```bash
cd ../../jokebear-ref
ffmpeg -y -framerate 12 -i 'frames/8874-keeps-moving/<stickerid>_f%02d.png' \
  -vf "scale=540:-1" -c:v png /tmp/bear_loop.mov
```
再把 `bear_loop.mov` 叠到背景 + 文字层上。`frames/` 共 3229 帧，9 个动画包可选。

---

## 五、路线 B 用法（只在需要真动效时）

1. **首帧必须喂官方贴图**（image-to-video），绝不用文生视频
2. prompt = [形象锁定正面] + [上表 scene 句] + [动效句]，负面词全带
3. 形象锁定 / 动效 / 负面词全文见 [02-通用视频prompt模板.md](../02-通用视频prompt模板.md) B2–B3
4. 每帧生成 2–3 个候选，按下面七项验收挑

**还原度七项验收（任一不过就弃用该帧，回退静帧）**
- [ ] 眼睛是两个纯黑小圆点，无高光、无眼白、无睫毛
- [ ] 嘴是紧闭小 ω，没张开、没牙
- [ ] 没有眉毛、没有腮红
- [ ] 四肢光滑椭圆，无手指脚趾
- [ ] 白色平涂，无毛发质感
- [ ] 全程一只熊，无多余肢体
- [ ] 画面无 AI 生成的文字

---

## 六、置顶评论（发布后 1 小时内，必做）

```
🧋 熊也来体验 EP.01｜奶茶店篇

熊今天的时间表：
09:50 先给封口机预热（自己还没热）
13:00 单子比熊高
14:30 有人说少冰，熊已经封好口了
16:00 有人说了谢谢，熊回血了

人，有奶茶店的搭子在吗？评论区认领一下。
下一期熊去体验什么职业？点单最多的熊就去 🙋
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，不是「上传图文」
- [ ] 时长 ≥ 12 秒，首帧即封面帧
- [ ] 熊本体全部官方贴图（或通过还原度七项验收）
- [ ] 配乐用小红书站内音乐，不外挂本地 BGM
- [ ] 标题含栏目名 + 职业词 +「打工」
- [ ] 正文含期数 + 认领钩子 + 点单钩子
- [ ] 7 个话题逐个点选生效
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| 中位最高的职业池（857）能带量 | 观看数 | ≥ 1000（视频池上限更高） |
| 13 秒能把平均观看时长拉起来 | 平均观看时长 | ≥ 8 秒（本号现 5.1–6.5 秒） |
| 「同行认领 + 职业点单」双钩子 | 评论数 | ≥ 12 |
| 身份场景是本号唯一涨粉款 | 涨粉 | ≥ 5 |
| 视频先发、图文后发是否互不抢量 | 3–4 天后图文版曝光 | ≥ 本篇曝光 × 60% |
