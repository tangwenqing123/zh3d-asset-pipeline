---
name: zh3d-asset-pipeline
description: 中文3D资产全链生产管线——从一句中文提示词到可发布的数据集条目（提示词工程→混元3D生成→批量下载→GLB规范化→Blender白底渲染→数据集落盘→魔搭开源发布）。凡用户要做3D资产/3D数据集/文生3D提示词/混元3D批量生产/3D场景渲染/把3D产出发布到ModelScope，一律用本技能。触发词：3D资产、3D数据集、文生3D、混元3D、3D提示词、3D渲染、3D管线。
---

# zh3d-asset-pipeline — 中文3D资产全链生产管线

把一句中文提示词变成一条可发布的数据集条目（提示词→GLB→渲染→manifest→开源仓库）。这套管线在 zh3d-chain 数据集（136条精选+50组变体，2026-10 ModelScope 发布）上完整验证过十一个生产日。

## 总览：五层流水线

```
①提示词工程 → ②平台生成(混元3D) → ③下载入库 → ④规范化+渲染 → ⑤数据集落盘/发布
     人审闸          每日20额度      全自动         Blender无头        git-lfs到魔搭
```

**铁律：单发→质检→PASS才批量。** 任何一批新资产，先生产1条走完全链，人审通过后再放批量。

## ① 提示词工程层

先读 `references/prompt-engineering.md`（三风格族基准卡+词法铁律+3D安全词+变体组方法论）。核心：

- **三风格族**：青铜雕塑族 / 写实器物族 / Q版黏土族——同一族内不许漂，族卡直接套模板
- **3D安全词**：细长件（须/角/流苏/柳条）一律加"短粗/贴伏/成绺"——细长飘件是图生3D碎件重灾区
- **通用收尾**：`底部平整，单体完整，纯白背景，无杂物无文字，高清3D资产。`
- **图生3D输入图四自检**：纯白底/居中/全身完整/无文字水印——任一不过重抽

## ② 平台生成层（混元3D）

先读 `references/hunyuan-sop.md`（每日额度排产/批量贴词限制/清单API/候选挑选）。核心坑：

- **单次批量贴词≤10个**：超发静默丢弃不报错，贴完清点创作中心计数
- **图生3D条目无标题**：辨认靠 imageList 输入图（aHash 配对法，见SOP）
- **4候选挑形状最佳1个**，不满意换seed重抽，单件最多2次额度

## ③ 下载入库层

用户生成完说一声后，扫描平台清单→判新→追加manifest→批量下载（见 `references/hunyuan-sop.md` 的清单API段）。

```
python scripts/batch_download_hunyuan.py --base /path/to/assets   # 读 manifest.tsv，幂等跳过已存在；--base或环境变量ZH3D_ASSETS指定资产根目录
```

manifest.tsv 格式（每行一资产，第5列可选=显式归类目录）：
```
日期|条目名|u1(目录guid)|u2(文件hash)|分类目录
```

## ④ 规范化+渲染层（Blender无头）

**平台批次兼容坑**：平台某天生成的GLB可能在新版Blender里"单件正常、多件组合必崩"（C++ Exception/KERNELBASE）。根治=导入重导出规范化：

```
D:\Blender\blender.exe -b -P scripts/glb_repair.py -- --glb in.glb --out out.glb
```

白底棚拍渲染（4机位 front/quarter/side/top，1080×1920）：

```
D:\Blender\blender.exe -b -P scripts/item_render.py -- --glb model.glb --out renders/ --name item_id
# 或批量：--list jobs.json  [{"name":..,"glb":..,"out":..},...]（路径必须绝对路径）
```

多件组合场景（主题场景/概念图）参考 `references/scene-recipes.md`（一生肖一场景/白昼岛三区配方+毒件二分定位法+EEVEE核显坑册）。

## ⑤ 数据集落盘+发布层

先读 `references/dataset-publish.md`（条目目录规范/manifest.jsonl schema/魔搭发布checklist）。每条目：

```
dataset/assets/{分类}/{条目ID}/
├── prompt.md          # 中文提示词原词+风格卡+来源存档（原词必须当场落档！）
├── scene_params.json  # 渲染参数快照（可复现）
├── image/             # 输入图（图生3D条目）
├── model/model.glb
└── renders/           # 4机位白底图
```

发布= git-lfs 推魔搭。**中文路径验收必须URL编码**（curl裸UTF-8会假404）；push前先 fetch（平台会插自动提交）；StorageSize字段滞后不可作验收依据。全套坑见 dataset-publish.md。

## 快速开始（最小闭环）

1. 用户给一个物件（如"貔貅"）→ 按①写提示词（三选一风格族）
2. 文生3D直出：用户贴词到平台生成（或已生成→扫描入库）
3. 你跑③下载→④repair+渲染
4. QC：抽 front 机位目检（几何完整/无碎件/构图居中）
5. ⑤落盘成条目，登记产出

## 产出纪律

- 凡生成必登记（产出库/artifacts台账）
- 提示词原词当场落档进 prompt.md——回溯版要如实标注"回溯"
- QC不合格：白底崩→重渲染；碎件→换候选或加安全词重抽
- 计费资源：GPU实例>10分钟无任务必须提示关机
