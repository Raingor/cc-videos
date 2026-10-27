# EP04 · 熊也来体验｜网约车司机的一天（视频 prompt）

> 栏目：**熊也来体验 EP.04** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜网约车司机打工的一天
```

**正文**
```
熊今天跑了十七单，算完流水刚够加油。

熊也来体验 EP.04｜网约车篇
人，有跑车的师傅在吗？评论区认领一下 🚗
你今天跑了几单？报个数。
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#网约车` `#网约车司机` `#打工日常` `#打工人表情包` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 熊也来体验<br>网约车司机<br>打工的一天 | 端坐、握着什么<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: sitting behind a very simple steering wheel drawn as a ring with two spokes, a rounded rectangle window behind, deep night blue background, generous negative space` | 夜蓝 / 米白 |
| **2** | 05:40 出车<br>熊比太阳早起 | 没醒、发呆<br>`3542043-health` / `1338653-5-5`<br>选用：`____` | `scene: dark pre-dawn outside a simple rounded window, one tiny crescent moon, deep blue background, flat minimal lighting` | 深蓝 / 浅灰 |
| **3** | 08:00 早高峰<br>熊看了二十分钟车尾 | 呆住、正视<br>`10689991-somehow`<br>选用：`____` | `scene: three plain rounded rectangles lined up ahead as car backs, all motionless, cool grey background, no detail` | 冷灰 / 米白 |
| **4** | 10:30 空车<br>熊等单等到<br>开始想人生 | 侧头、发呆<br>`10033892-comic`<br>选用：`____` | `scene: one completely blank rounded rectangle as an empty phone screen beside the character, misty pale blue background` | 雾蓝 / 奶油白 |
| **5** | 15:00 有人说<br>「师傅路熟」<br>熊今天有价值了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny simple heart floating beside the character, warm orange background, soft and quiet` | 暖橘 / 米白 |
| **6**<br>尾帧 | 熊今天没走错路<br>给熊记一功 | 揣手手、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: sitting with both short arms tucked in front, plain warm orange gradient background, lots of empty space at the bottom for text` | 暖橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.04`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**。夜间帧可优先翻 `1360541-winter`、`1332214-autumn`（色调更沉）
- 道具程序绘制：方向盘 = 圆环 + 两条辐条；车窗 = 圆角矩形；车尾 = 三个圆角矩形；夜景光点 = 若干小圆
- **不画真实车型、不出现任何平台 logo / 车牌 / 真人**
- 字体：细软圆润手写体，暖米白；夜色背景下保证对比度
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP04-网约车司机的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 网约车司机的一天.mp4
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

> 车内场景对 B 特别不友好：`car interior`、`driving` 会引来真实车内摄影质感和人类的手。**建议本期直接走路线 A。**

---

## 六、置顶评论（发布后 1 小时内，必做）

```
🚗 熊也来体验 EP.04｜网约车篇

熊今天的时间表：
05:40 比太阳早起
08:00 看了二十分钟车尾
10:30 空车的时候路特别顺
15:00 有人说「师傅路熟」，熊有价值了

人，有跑车的师傅在吗？评论区认领一下。
你今天跑了几单？报个数 🙋
下一期熊去体验什么职业？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 配乐用小红书站内音乐
- [ ] 标题含栏目名 +「网约车司机」+「打工」
- [ ] 7 个话题逐个点选生效
- [ ] 无真实车型 / 平台 logo / 车牌 / 真人
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| 偏男性从业者题材在本号（女 78%）的表现 | 观看数 + 观众性别比 | ≥ 600；记录性别是否偏移 |
| 「一天流水线」在该池的适配度（池内 8122 赞就是这个结构） | 点赞率 | ≥ 10% |
| 「报个数」提问 | 评论数 | ≥ 12 |
| 打工线第三期仍能涨粉 | 涨粉 | ≥ 5 |

> **若本期观看 < 400**：本号受众撑不住偏男性职业，后续打工线优先排女性从业者集中的职业（收银员 277 / 服务员 168 / 早餐店 127 / 护士 63 / 幼师 22），网约车、工地这类往后放。
