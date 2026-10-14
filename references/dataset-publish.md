# 数据集落盘与魔搭发布 — 条目规范/manifest/发布checklist

## 条目目录规范

```
dataset/assets/{分类目录}/{条目ID}/
├── prompt.md          # 中文提示词原词+风格卡+来源存档
├── scene_params.json  # 渲染参数快照
├── image/             # 输入图（图生3D条目放 doubao_input.png）
├── model/model.glb
└── renders/           # 4机位：{条目ID}_{front,quarter,side,top}.png
```

**prompt.md 必须存原词**（生成当时的提示词原文，禁止事后改写美化）。原词丢失只能标"回溯版"并注明——如实记录优先于好看。

## manifest.jsonl（每行一条完整元数据）

```json
{"id": "var_46_long", "category": "22_变体组", "cn_name": "龙_Q版黏土版",
 "prompt_zh": "一条Q版黏土小龙摆件，盘绕成圆墩坐姿，……",
 "style_card": "Q版黏土族v1",
 "image_input": null, "image_tool": "无(文生3D直出)",
 "model_glb": "assets/22_变体组/var_46_long/model/model.glb",
 "model_engine": "腾讯混元3D 文生3D text2ModelV3.1",
 "model_stats": {"tri_faces": 1500000, "vertices": 800000, "file_mb": 77.1},
 "renders": ["var_46_long_front.png", "..."],
 "chain": ["prompt_zh", "model_glb", "renders+scene_params"],
 "license": {"text": "CC-BY-4.0", "renders": "CC-BY-NC-4.0+AI标识", "model": "混元3D服务条款穿透(见NOTICE)"},
 "ai_generated": true, "date": "2026-10-14", "notes": "..."}
```

## 许可分层（NOTICE.md）

| 模态 | 许可 |
|---|---|
| 提示词/风格卡/参数 | CC-BY-4.0 |
| 渲染图 | CC-BY-NC-4.0 + AI标识 |
| 3D模型 | 混元3D服务条款穿透——**禁训练竞争模型**（数据集因此定位"创作者语料+评测基准"，非训练集） |

## 魔搭发布 checklist

1. 网页建仓（SDK create_repo 或网页）→ **建仓即有初始提交，push前先 fetch+merge**
2. `.gitattributes` 锁 LFS：`*.glb/*.png filter=lfs diff=lfs merge=lfs -text`
3. README frontmatter（license/task_categories/language/tags/pretty_name）——服务端Tags靠它激活，否则黄条
4. `git lfs install && git add -A && git push`；push被拒=平台插了dataset_infos自动提交→fetch+merge再推
5. **中文路径验收必须URL编码**：`urllib.parse.quote(path)`——curl裸UTF-8对中文路径假404
6. StorageSize字段滞后数日，**不可作验收依据**；用 resolve/master 抽查 HEAD 200 + 文件树API核对
7. 大量上传断点续传安全：中断就再 push / `git lfs push origin master`
8. 元数据程序化：中文名/描述走 `PUT /api/v1/datasets/{Id}` JSON；README更新走页内 `POST /api/v1/datasets/{Id}/repo/upload`（FormData+csrf_token头）

## 拉回（本地清空后恢复）

```bash
git lfs clone https://www.modelscope.cn/datasets/{ns}/{repo}.git
```
清本地前：留 manifest+scripts+README 的小zip保底；删除动作列 trash.txt 备查。
