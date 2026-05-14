bl_info = {
    "name": "Batch Icon Renderer (Stable)",
    "author": "Copilot & Hideki",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N Panel > Icon Render",
    "description": "Render multiple icon sizes (Windows common) reliably without skipping",
    "category": "Render",
}

import bpy
import os
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, PointerProperty


# ==========================================================
# Global state for rendering process
# ==========================================================

class IconRenderState:
    sizes = []
    index = 0
    running = False
    prefix = ""
    save_dir = ""


# ==========================================================
# Render complete handler
# ==========================================================

def iconrender_on_complete(scene):
    """Handle the next size when rendering is complete"""
    if not IconRenderState.running:
        return

    IconRenderState.index += 1

    if IconRenderState.index >= len(IconRenderState.sizes):
        # Complete
        IconRenderState.running = False
        if iconrender_on_complete in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(iconrender_on_complete)
        print("All icon renders complete")
        return

    # Proceed to the next render
    bpy.ops.iconrender.render_next()


# ==========================================================
# Properties
# ==========================================================

class ICONRENDER_Properties(PropertyGroup):
    prefix: StringProperty(
        name="File name prefix",
        default="icon",
    )

    save_dir: StringProperty(
        name="Save location",
        default="//tmp",
        subtype='DIR_PATH',
    )

    # Common sizes for Windows icons
    size_512: BoolProperty(name="512 x 512", default=True)
    size_256: BoolProperty(name="256 x 256", default=True)
    size_128: BoolProperty(name="128 x 128", default=True)
    size_96:  BoolProperty(name="96 x 96",  default=False)
    size_64:  BoolProperty(name="64 x 64",  default=True)
    size_48:  BoolProperty(name="48 x 48",  default=True)
    size_40:  BoolProperty(name="40 x 40",  default=False)
    size_32:  BoolProperty(name="32 x 32",  default=True)
    size_24:  BoolProperty(name="24 x 24",  default=False)
    size_20:  BoolProperty(name="20 x 20",  default=False)
    size_16:  BoolProperty(name="16 x 16",  default=True)


# ==========================================================
# Initial render start
# ==========================================================

class ICONRENDER_OT_batch_render(Operator):
    bl_idname = "iconrender.batch_render"
    bl_label = "Render Icons"

    def execute(self, context):
        props = context.scene.iconrender_props

        # Collect sizes
        IconRenderState.sizes = []
        if props.size_512: IconRenderState.sizes.append(512)
        if props.size_256: IconRenderState.sizes.append(256)
        if props.size_128: IconRenderState.sizes.append(128)
        if props.size_96:  IconRenderState.sizes.append(96)
        if props.size_64:  IconRenderState.sizes.append(64)
        if props.size_48:  IconRenderState.sizes.append(48)
        if props.size_40:  IconRenderState.sizes.append(40)
        if props.size_32:  IconRenderState.sizes.append(32)
        if props.size_24:  IconRenderState.sizes.append(24)
        if props.size_20:  IconRenderState.sizes.append(20)
        if props.size_16:  IconRenderState.sizes.append(16)

        if not IconRenderState.sizes:
            self.report({'WARNING'}, "No sizes selected")
            return {'CANCELLED'}

        IconRenderState.index = 0
        IconRenderState.running = True
        IconRenderState.prefix = props.prefix
        IconRenderState.save_dir = bpy.path.abspath(props.save_dir)

        os.makedirs(IconRenderState.save_dir, exist_ok=True)

        # Register handler (prevent duplicate registration)
        if iconrender_on_complete not in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.append(iconrender_on_complete)

        # Start the first render
        bpy.ops.iconrender.render_next()

        return {'FINISHED'}


# ==========================================================
# Execute the next render
# ==========================================================

class ICONRENDER_OT_render_next(Operator):
    bl_idname = "iconrender.render_next"
    bl_label = "Render Next Icon"

    def execute(self, context):
        scene = context.scene

        size = IconRenderState.sizes[IconRenderState.index]

        scene.render.resolution_x = size
        scene.render.resolution_y = size

        filepath = os.path.join(
            IconRenderState.save_dir,
            f"{IconRenderState.prefix}{size}.png"
        )

        scene.render.filepath = filepath
        scene.render.image_settings.file_format = 'PNG'

        print(f"Rendering {size}x{size} → {filepath}")

        bpy.ops.render.render(write_still=True)

        return {'FINISHED'}


# ==========================================================
# UI Panel
# ==========================================================

class ICONRENDER_PT_panel(Panel):
    bl_label = "Icon Render"
    bl_idname = "ICONRENDER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Icon Render"

    def draw(self, context):
        layout = self.layout
        props = context.scene.iconrender_props

        layout.prop(props, "prefix")
        layout.prop(props, "save_dir")

        layout.label(text="Sizes (Windows common):")
        col = layout.column(align=True)
        col.prop(props, "size_512")
        col.prop(props, "size_256")
        col.prop(props, "size_128")
        col.prop(props, "size_96")
        col.prop(props, "size_64")
        col.prop(props, "size_48")
        col.prop(props, "size_40")
        col.prop(props, "size_32")
        col.prop(props, "size_24")
        col.prop(props, "size_20")
        col.prop(props, "size_16")

        layout.separator()
        layout.operator("iconrender.batch_render", icon='RENDER_STILL')


# ==========================================================
# Registration
# ==========================================================

classes = (
    ICONRENDER_Properties,
    ICONRENDER_OT_batch_render,
    ICONRENDER_OT_render_next,
    ICONRENDER_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.iconrender_props = PointerProperty(type=ICONRENDER_Properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.iconrender_props


if __name__ == "__main__":
    register()
