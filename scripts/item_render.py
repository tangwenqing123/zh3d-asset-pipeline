# -*- coding: utf-8 -*-
# 白底产品棚拍渲染器（dataset-zh3d-chain 条目渲染用）
# 单件: blender.exe -b -P item_render.py -- --glb X.glb --out DIR --name ID
# 批量: blender.exe -b -P item_render.py -- --list items.json
#   items.json = [{"name":..,"glb":..,"out":..}, ...]  单进程循环全部条目
# 输出: {name}_{front,quarter,side,top}.png  1080x1920 白底
import bpy, sys, math, json, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

def argget(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d

VIEWS = {  # 视角: (方位角deg 0=正面-Y, 仰角deg)
    "front":   (0, 8),
    "quarter": (45, 18),
    "side":    (90, 8),
    "top":     (30, 78),
}
RES_X, RES_Y, LENS = 1080, 1920, 60


def setup_item(glb, out, name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene  # 坑#1: factory settings 后必须重取引用
    bpy.ops.import_scene.gltf(filepath=glb)
    scene = bpy.context.scene
    meshes = [o for o in scene.objects if o.type == 'MESH']
    if not meshes:
        raise RuntimeError("no mesh in " + glb)

    mins = Vector((1e9,) * 3); maxs = Vector((-1e9,) * 3)
    for o in meshes:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    center = (mins + maxs) / 2
    size = maxs - mins
    r = size.length / 2

    # 无地面：悬浮白底（资产预览标准），避免地面灯光衰减渐变带
    # 纯白世界：强度0（不参与照明），背景走透明底→后期PIL压白
    world = bpy.data.worlds.new("white"); scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (1, 1, 1, 1)
    bg.inputs[1].default_value = 0.0

    # 三点棚拍灯（功率随包围盒半径缩放；透明底无环境光，全靠灯）
    k = (r / 0.5) ** 2
    def area(nm, loc, size, pw, rot=(0, 0, 0)):
        ld = bpy.data.lights.new(nm, type='AREA')
        ld.energy = pw * k; ld.size = size
        lo = bpy.data.objects.new(nm, ld)
        lo.location = loc; lo.rotation_euler = rot
        scene.collection.objects.link(lo)
    s2 = max(size.x, size.y, size.z) * 2.0
    area("key",   (center.x - size.x * 2.0, center.y - size.y * 2.6, maxs.z + size.z * 1.4), s2, 500,
         (math.radians(38), 0, math.radians(18)))
    area("fill",  (center.x + size.x * 2.4, center.y - size.y * 1.2, maxs.z + size.z * 0.8), s2, 200)
    area("rim",   (center.x + size.x * 0.6, center.y + size.y * 2.6, maxs.z + size.z * 1.6), s2 * 0.7, 350)

    # 渲染设置
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = eng; break
        except TypeError:
            continue
    try:
        scene.eevee.taa_render_samples = 64
    except AttributeError:
        pass
    scene.view_settings.view_transform = 'Standard'
    scene.render.resolution_x = RES_X
    scene.render.resolution_y = RES_Y
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True

    cam_data = bpy.data.cameras.new("cam"); cam_data.lens = LENS
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    fov_v = 2 * math.atan(18.0 / LENS)
    fov_h = 2 * math.atan(18.0 * (RES_X / RES_Y) / LENS)
    dist = r / math.sin(min(fov_v, fov_h) / 2) * 1.14 + r * 0.2

    os.makedirs(out, exist_ok=True)
    for view, (az, el) in VIEWS.items():
        azr, elr = math.radians(az), math.radians(el)
        loc = Vector((center.x + dist * math.cos(elr) * math.sin(azr),
                      center.y - dist * math.cos(elr) * math.cos(azr),
                      center.z + dist * math.sin(elr)))
        cam.location = loc
        d = center - loc
        cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = os.path.join(out, f"{name}_{view}.png")
        bpy.ops.render.render(write_still=True)
        print("[RENDER-OK]", scene.render.filepath)


if "--list" in argv:
    items = json.load(open(argget("--list"), encoding="utf-8"))
    for it in items:
        print("[ITEM]", it["name"], flush=True)
        setup_item(it["glb"], it["out"], it["name"])
else:
    setup_item(argget("--glb"), argget("--out"), argget("--name"))
print("[ALL-DONE]")
