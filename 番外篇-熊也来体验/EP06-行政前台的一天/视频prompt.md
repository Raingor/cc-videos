# EP06 · 熊也来体验｜行政前台的一天（视频 prompt）

> 栏目：**熊也来体验 EP.06** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）
>
> 前台池方差 8.2x（23 个池最低）= 最稳的一期。**标题必须带数字**（池内头部全是"月薪7000+双休 | 朝10晚6"这类模式）。

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜朝十晚六·双休：行政前台打工的一天
```

**正文**
```
熊今天笑了一百次，其中九十次不是因为开心。

熊也来体验 EP.06｜行政前台篇
人，有前台在吗？评论区认领一下 ☕
你今天指了几次洗手间？报个数。
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#行政前台` `#前台日常` `#行政` `#打工日常` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 朝十晚六·双休<br>行政前台<br>打工的一天 | 端坐、规矩<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: sitting behind a very simple reception counter drawn as one long horizontal bar, one pen and one notepad on top, off-white background, generous negative space` | 米白 / 浅青 |
| **2** | 10:00 今天第一件事<br>是给饮水机换水 | 搬东西、吃力<br>`3542043-health`<br>选用：`____` | `scene: holding one round barrel larger than the head, pale mint background, flat lighting` | 浅青 / 米白 |
| **3** | 11:00 有人问洗手间<br>熊指了第八次 | 抬手指、无表情<br>`1007666-pack` / `10033892-comic`<br>选用：`____` | `scene: one short arm raised pointing off-frame, eight very small dots above the head, plain light grey background` | 浅灰 / 奶油白 |
| **4** | 13:00 收快递<br>熊的桌子看不见了 | 被压住、仰头<br>`3542043-health`<br>选用：`____` | `scene: surrounded by a pile of plain rectangular boxes, only the head visible, warm yellow background` | 暖黄 / 米白 |
| **5** | 16:30 有人说<br>「谢谢你帮我拿快递」<br>熊回血了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny simple heart floating beside the character, warm orange background, soft and quiet` | 暖橘 / 奶油白 |
| **6**<br>尾帧 | 熊今天笑了一百次<br>给熊记一功 | 揣手手、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: standing with both short arms tucked in front, plain warm orange gradient background, lots of empty space at the bottom for text` | 暖橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.06`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**
- 道具程序绘制：前台 = 长横条 + 台面；水桶 = 圆角梯形；快递 = 若干方块；本子 = 矩形 + 三条横线
- **不出现真实公司名、门禁品牌、真人**
- 字体：细软圆润手写体，浅墨绿或暖灰；一帧一句
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP06-行政前台的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 行政前台的一天.mp4
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

> `office`、`reception` 容易引来真实办公摄影质感。本期道具都极简，**建议直接走路线 A**。

---

## 六、置顶评论（发布后 1 小时内，必做）

```
☕ 熊也来体验 EP.06｜行政前台篇

熊今天的数字：
指了 8 次洗手间
收了 17 个快递
改了 4 次会议室时间
笑了 100 次（其中 90 次不是因为开心）

人，有前台在吗？评论区认领一下。
你今天指了几次洗手间？报个数 🙋
下一期熊去体验什么职业？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] **标题带数字**（朝十晚六 · 双休）
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 配乐用小红书站内音乐
- [ ] 无真实公司名 / 门禁品牌 / 真人
- [ ] 7 个话题逐个点选生效
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| **最低方差池（8.2x）能否稳定出量** | 观看数 | ≥ 600，**且不低于 400** |
| 标题带数字是否提升点击 | 封面点击率 | ≥ 12% |
| 「报个数」评论钩子 | 评论数 | ≥ 12 |
| 时间轴 vs EP05 荒诞规则 | 与 EP05 观看对比 | 记录 |
| 涨粉 | 涨粉 | ≥ 5 |

> **保底期**：连方差最低的池都跑不到 400，说明问题在出图/发布时段而不是选题，回头查素材质量与封面点击率。
