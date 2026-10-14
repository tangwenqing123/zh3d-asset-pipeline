# -*- coding: utf-8 -*-
# GLB规范化重写器：导入→glTF重导出（修平台10/14批与Blender渲染不兼容）
# 用法: blender.exe -b -P glb_repair.py -- --glb <in.glb> [--out <out.glb>]
import bpy, sys

RAW = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
src = RAW[RAW.index("--glb")+1]
dst = RAW[RAW.index("--out")+1] if "--out" in RAW else src.replace(".glb", "_repair.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_apply=True,
                          export_texcoords=True, export_normals=True,
                          export_materials='EXPORT',
                          export_yup=True, use_selection=False)
print("[REPAIR-OK]", dst)
