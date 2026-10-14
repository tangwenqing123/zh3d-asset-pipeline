# 混元3D平台SOP — 额度/批量/清单API/候选挑选

平台：https://3d.hunyuan.tencent.com （免费额度每日20次生成，当日刷新）

## 生产节奏

- **每日20额度排产**：单批≤10条×2批 + 留机动。风格未锁的新族首批≤4条目检
- **单次批量贴词≤10个**（平台硬限）：超发**静默丢弃**不报错——每贴完一批清点创作中心计数再贴下一批
- 生成完用户说一声→agent扫描下载，用户零操作

## 清单API（登录态浏览器内fetch）

```js
// IAB/浏览器登录态下，页面上下文里：
const r = await fetch("/api/3d/creations/list", {
  method: "POST", credentials: "include",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ offset: 0, limit: 20 })
});
// GET=405；limit>20 整页被拒返回空体（易误判为翻页结束）
// 翻页：offset+=20，直到 creations 空
```

关键返回字段：
- `creations[].prompt` — **完整提示词原文**（文生3D条目）
- `creations[].imageList[0]` — 输入图URL（图生3D条目，**title为空靠它辨认**）
- `creations[].businessType` — text3d / image3d
- `creations[].result[]` — 4候选，`urlResult.glb` 直链（COS带签名，pathname里 `{u1}/{u2}.glb`）

## 判新规则（防重复下载）

**每个creation含最多4候选GLB，本地manifest只存过其中1个**——判新必须"该creation的**所有候选u2都不在**旧集合"，any命中即跳过。用any命中判新会把全库当成新增（实战踩过：240条全误判）。

## 图生3D条目辨认（aHash配对法）

```python
# 拉imageList[0]输入图 vs 本地已知定妆图，aHash(16px)汉明距离
# 距离0=同一张图→直接命名；阈值≤20才配，其余人工看图
# 大阈值（如96-120）会把相近异图误配——必须逐条记距离
```

## 候选挑选标准（4选1）

1. 形状完整优先于贴图精致（碎件/缺件一票否决）
2. 细节件（翎羽/蒸汽/流苏）检查碎裂——收敛或无怪刺的优先
3. 姿态与提示词吻合（盘踞≠站立）
4. 不满意换seed重抽，**单件最多2次额度**（超出记台账次日补）

## 下载

GLB直链 = `https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/hunyuan3d/default/{u1}/{u2}.glb`（免签名）。
批量下载器读 manifest.tsv（格式见SKILL.md③），幂等跳过已存在，单文件流式落盘防憋内存。
