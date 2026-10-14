# zh3d-asset-pipeline

**中文3D资产全链生产管线** —— 从一句中文提示词到可发布的数据集条目。

```
提示词工程 → 混元3D生成 → 批量下载 → GLB规范化+Blender渲染 → 数据集落盘 → git-lfs开源发布
```

在 [zh3d-chain 数据集](https://modelscope.cn/datasets/zuiqingfeng6/zh3d-chain)（136条精选+50组提示词变体）上完整验证过11个生产日。本仓库将整条管线沉淀为可复用的 ZCode/Claude skill。

## 它解决什么

- **提示词工程**：三风格族基准卡（青铜雕塑/写实器物/Q版黏土）+词法铁律+3D安全词（细长件碎裂防治）
- **平台生产**：混元3D每日20额度排产SOP+清单API+批量贴词限制防坑
- **资产管线**：幂等批量下载/GLB规范化修复（平台批次兼容根治）/Blender无头白底棚拍渲染
- **数据集工程**：条目目录规范+manifest schema+魔搭git-lfs发布checklist

## 结构

```
├── SKILL.md                        # 技能入口（五层流水线总览）
├── references/
│   ├── prompt-engineering.md       # 三风格族/词法铁律/安全词/变体组方法论
│   ├── hunyuan-sop.md              # 平台SOP/清单API/判新规则/aHash辨认
│   ├── scene-recipes.md            # 主题场景配方/毒件二分定位/Blender坑册
│   └── dataset-publish.md          # 条目规范/manifest/魔搭发布checklist
└── scripts/
    ├── batch_download_hunyuan.py   # 批量下载器（幂等，--base可配）
    ├── glb_repair.py               # GLB导入重导出规范化（崩溃根治）
    └── item_render.py              # Blender无头白底棚拍（4机位）
```

## 使用

ZCode/Claude Code 用户：把本目录放进 `~/.agents/skills/zh3d-asset-pipeline/` 即被发现。对模型说“做一个3D资产/3D数据集条目”即触发。

脚本独立可用：

```bash
python scripts/batch_download_hunyuan.py --base /path/to/assets
blender -b -P scripts/glb_repair.py -- --glb in.glb --out out.glb
blender -b -P scripts/item_render.py -- --glb model.glb --out renders/ --name item_id
```

## License

MIT（脚本与文档）。管线产出资产的许可由生成平台条款决定（混元3D产出：禁训练竞争模型）。
