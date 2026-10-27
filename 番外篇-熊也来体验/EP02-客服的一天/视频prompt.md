# EP02 · 熊也来体验｜客服的一天（视频 prompt）

> 栏目：**熊也来体验 EP.02** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜客服打工的一天
```

**正文**
```
熊今天说了八十次「亲」，一次都不是对自己说的。

熊也来体验 EP.02｜客服篇
人，有客服在吗？评论区认领一下 ☕
你今天说了多少次「亲」？报个数。
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#客服` `#客服日常` `#打工日常` `#打工人表情包` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

取图文版九格里最强的 6 格。

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 熊也来体验<br>客服打工的一天 | 端坐、耳机感<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: at a very plain office desk, a thin curved headset and a simple monitor showing three empty rounded chat bubbles, cool grey-blue background, generous negative space` | 灰蓝 / 米白 |
| **2** | 10:30 被挂了电话<br>熊的心也被挂了 | 呆住、静止<br>`3542043-health`<br>选用：`____` | `scene: holding a simple handset, one thin disconnected line beside it, pale misty blue background, flat lighting` | 雾蓝 / 浅灰 |
| **3** | 12:00 有人骂了<br>熊说「非常抱歉给您<br>带来不好的体验」 | 鞠躬、道歉<br>**`6959173-honorifics-etc`**<br>选用：`____` | `scene: leaning slightly forward with head lowered, a dense block of tiny grey rectangles on a simple screen behind, grey-blue background` | 灰蓝 / 米白 |
| **4** | 14:00 熊今天<br>说了八十次「亲」 | 无表情、正视<br>`10033892-comic`<br>选用：`____` | `scene: facing forward, eight very small speech bubbles floating above the head, plain light grey background` | 浅灰 / 奶油白 |
| **5** | 15:30 有人说了谢谢<br>熊差点哭了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny simple heart floating beside the character, warm orange background, soft and quiet` | 暖橘 / 米白 |
| **6**<br>尾帧 | 熊今天一次都没发火<br>给熊记一功 | 揣手手、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: standing with both short arms tucked in front, plain warm orange gradient background, lots of empty space at the bottom for text` | 暖橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.02`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**。第 3 帧优先翻 `6959173-honorifics-etc`（敬语/鞠躬包）
- 道具程序绘制：耳麦 = 一条弧线 + 两个小圆；对话气泡 = 圆角矩形 + 小尖角；屏幕文字用小色块代替，**绝不写真实句子**（避免像平台截图）
- 不出现任何真实平台界面、品牌、真人
- 字体：细软圆润手写体，一帧一句，字号大、留白多
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP02-客服的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 客服打工的一天.mp4
```

带呼吸感版本与动画帧升级方案见 [02-通用视频prompt模板.md](../02-通用视频prompt模板.md) A3–A4。
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

> 客服篇尤其容易崩：`headset`、`microphone` 这类词会让模型给熊加上人类耳朵和手指。**建议本期直接走路线 A，不用 B。**

---

## 六、置顶评论（发布后 1 小时内，必做）

```
☕ 熊也来体验 EP.02｜客服篇

熊今天的时间表：
10:30 被挂了电话，心也被挂了
12:00 道歉了，其中零次是熊的错
14:00 说了八十次「亲」
15:30 有人说了谢谢，熊差点哭了

人，有客服在吗？评论区认领一下，熊给你倒杯水。
你今天说了多少次「亲」？报个数 🙋
下一期熊去体验什么职业？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 屏幕内容全部色块，无真实平台界面 / 品牌 / 真人
- [ ] 配乐用小红书站内音乐
- [ ] 标题含栏目名 +「客服」+「打工」
- [ ] 7 个话题逐个点选生效
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| 蓝海组合（高池 + 无同类）能否超过 EP.01 | 观看数 | ≥ EP.01 观看数 |
| 「报个数」是最低门槛的评论钩子 | 评论数 | ≥ 15 |
| 客服群体认领欲 | 明确自称客服的评论条数 | ≥ 5 |
| 13 秒时长的完播质量 | 平均观看时长 | ≥ 8 秒 |
| 系列第二期延续涨粉 | 涨粉 | ≥ 5 |
