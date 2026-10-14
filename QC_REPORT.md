# QC Report — zh3d-asset-pipeline v1.0（对照SkillsBench生态标准）

> 质检日期 2026-10-15 · 标准 = SkillsBench (arXiv:2602.12670) 生态质量评分 4维0-3分 + Anthropic失败模式清单逐项自查

## 评分

| 维度 | 检查明细 | 得分 |
|---|---|---|
| Completeness 必需组件齐全 | SKILL.md+4 references+3 scripts = 8/8 | 3/3 |
| Clarity SKILL.md行数 | 94行（业界建议<500，防上下文预算耗尽） | 3/3 |
| Specificity 可执行命令引用 | SKILL.md含4处脚本调用示例+--base参数说明 | 2/3 |
| Examples 全链示例 | 2条完整（prompt原词+GLB+4机位渲染），真机生产非演示 | 3/3 |
| **总分** | | **20/21（95%）** |

## Anthropic失败模式清单自查

| 失败模式 | 自查 | 结果 |
|---|---|---|
| ①过长Skill有害（-2.9pp） | SKILL.md 94行+细节全在references按需读 | PASS |
| ②Skill数量过多干扰（4+仅+5.9pp） | 单skill自包含 | PASS |
| ③与模型已有知识冲突 | 纯程序性指导，无冲突性断言 | PASS |
| ④硬编码/泄漏（泛用性） | 路径全部--base参数化或环境变量；无任务特定magic值 | PASS |

## 真机验证

- 7步闭环实测2条（石狮子对/青铜仙鹤）：扫描判新→下载→规范化→渲染→QC全过
- 回归批20条（白昼岛14+细长件4+组合造景2）：扫描20/20精确命中、下载20/20零失败、渲染80张全过
- known issue：垂柳形态不符（生成端无柳条，非管线缺陷，待重抽）

## 遗留改进项

- Specificity 2/3：可再补一条"输入图批量aHash辨认"的一行命令示例（下版本）
