# EP07 · 熊也来体验｜超市收银员的一天（视频 prompt）

> 栏目：**熊也来体验 EP.07** · 形式：**竖版短视频 13 秒**（6 帧 × 2.2 秒）
> 建议发布时间：周一 **07:30**
> 制作路线：**A 官方贴图合成**（主力）
> 状态：📝 待出片
> 依据：[02-通用视频prompt模板.md](../02-通用视频prompt模板.md) · [图文版](图文版.md)（同源素材）
>
> 双视角最强的一期：从业者会认领，顾客人人排过队。池内 25 万赞那条走的正是顾客视角。

---

## 一、发布信息（可直接复制）

**标题**
```
熊也来体验｜超市收银员打工的一天
```

**正文**
```
熊今天扫了六百件商品，其中一件扫了十一次。

熊也来体验 EP.07｜收银员篇
人，有收银的搭子在吗？评论区认领一下 🛒
也欢迎顾客说说，你们排队时在想什么。
```

**话题**：`#自嘲熊` `#自嘲熊揣手手` `#收银员` `#超市` `#超市打工` `#打工日常` `#精神状态`

---

## 二、分镜表（6 帧 × 2.2 秒 = 13.2 秒）

| 帧 | 画面文字 | 路线 A：贴图需求 → 候选包 → 选用 | 路线 B：场景 prompt（备用） | 配色 |
|:-:|---|---|---|---|
| **1**<br>首帧/封面 | 熊也来体验<br>超市收银员<br>打工的一天 | 端坐、握着什么<br>`10033892-comic` / `1007666-pack`<br>选用：`____` | `scene: sitting behind a simple conveyor belt drawn as two parallel lines with short ticks, one trapezoid scanner emitting a thin light line, off-white background, generous negative space` | 米白 / 浅青 |
| **2** | 08:50 开机<br>扫码枪比熊清醒 | 没醒、发呆<br>`3542043-health` / `1338653-5-5`<br>选用：`____` | `scene: looking at one trapezoid scanner emitting a thin light line, pale morning beige background, flat lighting` | 晨光米 / 浅灰 |
| **3** | 12:00 有人问<br>「这个多少钱」<br>熊也想知道 | 呆住、正视<br>`10033892-comic`<br>选用：`____` | `scene: holding up one plain unlabeled rectangular product, no barcode, no text, plain light grey background` | 浅灰 / 奶油白 |
| **4** | 15:30 有个小朋友<br>说了谢谢<br>熊回血了 | **回血帧·必须暖**<br>`1310872-s-love` / `1438683-s-love2`<br>选用：`____` | `scene: one tiny heart and one very short simple silhouette outline beside the character, warm orange background, soft and quiet` | 暖橘 / 奶油白 |
| **5** | 18:00 晚高峰<br>队伍排到货架后面了 | 被压住、仰头<br>`3542043-health`<br>选用：`____` | `scene: one very long zigzag line ahead of the character reaching the frame edge, warm yellow background, nothing else` | 暖黄 / 浅灰 |
| **6**<br>尾帧 | 熊今天没算错账<br>给熊记一功 | 揣手手、轻微得意<br>`1007666-pack` / `1310872-s-love`<br>选用：`____` | `scene: standing with both short arms tucked in front, plain warm orange gradient background, lots of empty space at the bottom for text` | 暖橘渐变 / 奶油白 |

尾帧底部加小字：`点赞收藏｜熊也来体验 EP.07`

---

## 三、出片规范

- 帧尺寸 **1080×1440**，命名 `01.png` … `06.png`
- 熊本体一律官方贴图原图，**不得 AI 生成**
- 道具程序绘制：传送带 = 两条平行长线 + 短竖线；扫码枪 = 梯形 + 细光线；商品 = 素色方块；队伍 = 一条折线
- **不出现真实超市品牌、真实商品包装、条码、真人**
- 字体：细软圆润手写体；一帧一句
- **总时长 ≥ 12 秒**；**导出无声**，配乐用小红书站内音乐

---

## 四、合成命令（路线 A）

```bash
cd "番外篇-熊也来体验/EP07-超市收银员的一天"

ffmpeg -y -framerate 1/2.2 -pattern_type glob -i '0*.png' \
  -vf "scale=1080:1440,fps=30" -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart 超市收银员的一天.mp4
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

> `supermarket`、`barcode`、`products` 极易引来真实包装与品牌字样（负面词里的 `text/logo` 会被商品挤穿）。**本期直接走路线 A。**

---

## 六、置顶评论（发布后 1 小时内，必做）

```
🛒 熊也来体验 EP.07｜收银员篇

熊今天的数字：
扫了 600 件商品
其中 1 件扫了 11 次
找零差了 5 毛（自己补上了）
被问了 N 次「这个多少钱」

人，有收银的搭子在吗？评论区认领一下。
你被问过最难回答的问题是什么？
（也欢迎顾客说说，你们排队时在想什么 🙋）
下一期熊去体验什么职业？点单最多的熊就去。
```

---

## 七、发布前核对

- [ ] 选择「上传视频」，时长 ≥ 12 秒，首帧即封面
- [ ] 熊本体全部官方贴图（或通过还原度七项）
- [ ] 置顶评论同时喊从业者和顾客（双视角）
- [ ] 配乐用小红书站内音乐
- [ ] 无真实超市品牌 / 商品包装 / 条码 / 真人
- [ ] 7 个话题逐个点选生效
- [ ] 今天不再发第二篇
- [ ] 发布后 1 小时内置顶评论，回复前 10 条

---

## 八、本期要验证的假设

| 假设 | 看哪个数 | 通过线 |
|---|---|---|
| 双视角职业是否放大互动 | 评论数 | ≥ 20 |
| 顾客视角参与度 | 非从业者评论占比 | ≥ 50% |
| 中位 277 的池能否出量 | 观看数 | ≥ 600 |
| 顾客更爱转发"我也见过" | 分享 / 点赞 | ≥ 70%（本号现 59%） |
| 涨粉 | 涨粉 | ≥ 5 |
