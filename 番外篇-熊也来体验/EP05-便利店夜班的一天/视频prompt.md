# EP05 · 熊也来体验｜便利店夜班的一天（视频 prompt）

> 栏目：**熊也来体验 EP.05** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）
>
> **⚠️ 本期走「荒诞规则」结构**：首帧直接抛规则，不是"XX 的一天"。依据见 [00-番外篇总企划.md](../00-番外篇总企划.md) §2.4——便利店池方差 164x，头部全靠内部规则的荒诞（27000 / 16000 / 10000）。

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜便利店夜班：报废的关东煮，熊不能吃
```

**正文**
```
熊今天扔掉了六个饭团、两份关东煮，一口都不能吃，吃了要罚钱。

熊也来体验 EP.05｜便利店夜班篇
人，有便利店的搭子在吗？评论区认领一下 🏪
你们店最离谱的规定是什么？
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#便利店` `#便利店店员` `#便利店夜班` `#打工日常` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

前 3 帧讲规则（钩子），后 3 帧才是夜班时间轴。

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 报废的关东煮<br>熊不能吃<br>吃了要罚钱 | 呆住、看着什么<br>`10689991-somehow` / `3542043-health`<br>选用：`____` | `scene: standing in front of a plain rectangular warmer tray holding three small round balls, cool grey background, generous negative space` | 冷灰 / 暖黄 |
| **2** | 要拍照、登记<br>当着监控扔 | 举着什么、端正<br>`6959173-honorifics-etc`<br>选用：`____` | `scene: holding one small rectangle like a phone, one tiny dark circle on the wall corner as a camera, cool grey-blue background` | 冷灰 / 浅蓝 |
| **3** | 员工也不能买<br>不能带回家 | 摇头、无奈<br>`10689991-somehow` / `1338653-5-5`<br>选用：`____` | `scene: one small rice ball shape with a single diagonal line crossing it, misty pale blue background, minimal` | 雾蓝 / 米白 |
| **4** | 02:00 有人进来买烟<br>熊差点感动了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny simple human silhouette outline at a doorway, one small heart beside the character, warm orange on deep blue` | 暖橘 / 夜蓝 |
| **5** | 04:00 补货<br>熊搬的箱子比自己大 | 搬东西、吃力<br>`3542043-health`<br>选用：`____` | `scene: holding one plain box larger than the character itself, grey-blue background, flat lighting` | 灰蓝 / 浅灰 |
| **6**<br>尾帧 | 熊今天一个人<br>守了一整夜<br>给熊记一功 | 揣手手、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: standing with both short arms tucked in front, dawn light gradient background, lots of empty space at the bottom for text` | 晨光橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.05`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**。夜间帧可优先翻 `1360541-winter`（色调更沉）
- 道具程序绘制：保温槽 = 圆角矩形 + 三个小圆；监控 = 小圆 + 支架线；禁止符 = 圆 + 斜线；箱子 = 大方块 + 一条封口线
- **不出现任何真实便利店品牌（7-11 / 全家 / 罗森等）、真实包装、真人**
- **首帧文字要大**——规则本身就是钩子，字号压过其他帧
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP05-便利店夜班的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 便利店夜班的一天.mp4
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

> `convenience store`、`shelves`、`night shift` 会引来真实店内摄影质感和品牌包装。**本期建议直接走路线 A。**

---

## 六、置顶评论（发布后 1 小时内，必做）

```
🏪 熊也来体验 EP.05｜便利店夜班篇

外人不知道的三条规则：
① 过期前两小时就要下架，不是过期后
② 要拍照、登记、当着监控扔
③ 员工也不能买、不能带回家

熊今天扔掉了六个饭团、两份关东煮、一盒三明治。

人，有便利店的搭子在吗？评论区认领一下。
你们店最离谱的规定是什么？熊想听 🙋
下一期熊去体验什么职业？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] **首帧是规则，不是"XX 的一天"**
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 配乐用小红书站内音乐
- [ ] 无真实便利店品牌 / 真实包装 / 真人
- [ ] 7 个话题逐个点选生效
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| **「荒诞规则」结构在高方差池优于时间轴** | 观看数 | ≥ 800 |
| 规则型首帧的点击率 | 封面点击率 | ≥ 12% |
| 「最离谱的规定」评论钩子 | 评论数 | ≥ 20 |
| 双视角共鸣（顾客也参与） | 非从业者评论占比 | ≥ 40% |
| 低中位池能否涨粉 | 涨粉 | ≥ 5 |
