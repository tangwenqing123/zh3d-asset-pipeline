# 场景渲染配方 — 单件棚拍/主题场景/组合场景 + 坑册

## 单件白底棚拍（item_render.py 已固化）

三点布灯：key 500W左前上38°/fill 200W右前/rim 350W正后上，功率全按 `×(r/0.5m)²` 自适应（r=包围球半径）；世界光0+透明底PIL压白；包围球自动取景60mm边距1.14。
已知特性：白色系材质在纯白底下发虚——此类资产改浅灰底(0.92)。

## 主题场景配方（一生肖一场景已验证12例）

每场景=配置不写死代码：
```python
CONFIGS = {
  "tiger": dict(main="虎",            # 主GLB按名glob解析（勿写死编号文件名）
                prop="啸天岩台",       # 道具GLB（同库）
                ground="stone",       # grass/dirt/stone/moon 四档地面色
                sky="dusk",           # warm/day/gold/dusk/moon 五档渐变天空
                platform="mound",     # mound=山岩丘/flat=平地
                size=2.0)}             # 主件目标尺寸(米)
```
- 道具摆位按**机位视线反推**（放东北三机位全出画，西北角三机位同见——多机位道具摆位本质是视线交集）
- **平地场景不放雾球**（与地面穿插出悬浮切面），雾球只配山丘
- 大气透视="远山压暗+贴地雾球"三件套（EEVEE体积雾核显上是米色墙，禁用）

## 组合场景毒件二分定位法（多件必崩时）

症状：单件渲染正常、多件组合C++ Exception崩、隔天同款正常（平台批次差异）。
定位：逐件注释二分（4件→去1件测→2轮定位毒件）。
根治：**resolve()全量repair缓存**——所有入景GLB先过glb_repair重导出，缓存到 `_repair_cache/` 幂等复用。

## Blender 5.2 无头坑册

| 坑 | 解法 |
|---|---|
| `read_factory_settings`后scene引用失效 | 重取 `scene = bpy.context.scene` |
| `shade_smooth`删了 | `for p in mesh.polygons: p.use_smooth=True` |
| NISHITA天空没了 | `sky_type='SINGLE_SCATTERING'` 或程序化渐变 |
| 世界输出节点 | 叫 `World Output` 不是 `WorldOutput` |
| 相机look-at | `rot=(atan2(hypot(dx,dy),-dz),0,atan2(-dx,dy))` |
| 渲染列表路径 | **必须绝对路径**——相对路径解析到C盘根 |
| C++ Exception偶现 | 以`[OUT]`输出为准；连续复现才是真崩 |
| 体积雾 | EEVEE Next@核显=米色墙，整条禁用 |

## 概念场景叙事化（可选进阶）

给组合场景一个叙事主题能翻倍传播力（实例：白昼岛三区=游戏企划《最后一座会消失的岛》的白昼村暖晨/被遗忘森林冷雾/消失边缘初雪）。配方：主题→三区情绪（灯光+地面+天空三档联动）→每区3机位→拼图QC。
