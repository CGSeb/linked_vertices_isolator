import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import (
    CollectionProperty,
)

from .operators import MESH_OT_create_linked_vertices_groups, MESH_OT_isolate_vertex_group, MESH_OT_show_all_vertex_groups
from .data import LinkedVertexGroup


# --------------------------------------------------
# UI Panel
# --------------------------------------------------

class VIEW3D_PT_linked_vertices_groups(Panel):
    bl_label = "Vertex Grouped by Links"
    bl_idname = "VIEW3D_PT_linked_vertices_groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LinkedVerts'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator(MESH_OT_create_linked_vertices_groups.bl_idname, icon='GROUP_VERTEX')
        layout.operator(MESH_OT_show_all_vertex_groups.bl_idname, icon='HIDE_OFF')

        layout.separator()
        layout.label(text="(Shift click to isolate multiple)")

        for i, group in enumerate(scene.linked_vertices_groups):
            row = layout.row(align=True)
            icon = 'HIDE_OFF' if group.visible else 'HIDE_ON'
            row.operator(
                MESH_OT_isolate_vertex_group.bl_idname,
                text=group.name,
                icon=icon,
            ).index = i


# --------------------------------------------------
# Registration
# --------------------------------------------------

classes = (
    LinkedVertexGroup,
    MESH_OT_create_linked_vertices_groups,
    MESH_OT_isolate_vertex_group,
    MESH_OT_show_all_vertex_groups,
    VIEW3D_PT_linked_vertices_groups,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.linked_vertices_groups = CollectionProperty(
        type=LinkedVertexGroup
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.linked_vertices_groups

if __name__ == "__main__":
    register()
