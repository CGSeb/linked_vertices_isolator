import bpy
import bmesh
from bpy.types import Operator
from bpy.props import (
    IntProperty,
)

class MESH_OT_create_linked_vertices_groups(Operator):
    bl_idname = "mesh.create_linked_vertices_groups"
    bl_label = "Create Linked Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)

        for v in bm.verts:
            v.tag = False

        groups = context.scene.linked_vertices_groups
        groups.clear()

        def collect_island(start_vert):
            stack = [start_vert]
            island = []
            start_vert.tag = True

            while stack:
                v = stack.pop()
                island.append(v.index)
                for e in v.link_edges:
                    other = e.other_vert(v)
                    if not other.tag:
                        other.tag = True
                        stack.append(other)
            return island

        for v in bm.verts:
            if not v.tag:
                island = collect_island(v)
                item = groups.add()
                item.name = f"Group {len(groups)}"
                item.visible = True
                item.verts = ",".join(map(str, island))

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


class MESH_OT_isolate_vertex_group(Operator):
    bl_idname = "mesh.isolate_vertex_group"
    bl_label = "Isolate Group"

    index: IntProperty()

    def invoke(self, context, event):
        self.shift = event.shift
        return self.execute(context)

    def execute(self, context):
        obj = context.object
        scene = context.scene
        groups = scene.linked_vertices_groups

        bpy.ops.object.mode_set(mode='EDIT')

        ts = context.tool_settings

        # --- STORE PREVIOUS SELECT MODE ---
        prev_select_mode = ts.mesh_select_mode[:]

        # Force vertex select
        ts.mesh_select_mode = (True, False, False)

        bm = bmesh.from_edit_mesh(obj.data)

        # Reveal everything first
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')

        if self.shift:
            # MULTI-ISOLATE
            groups[self.index].visible = not groups[self.index].visible
        else:
            # EXCLUSIVE ISOLATE
            for i, g in enumerate(groups):
                g.visible = (i == self.index)

        # Collect all visible vertices
        visible_indices = set()
        for g in groups:
            if g.visible:
                visible_indices.update(int(i) for i in g.verts.split(","))

        # Select visible vertices
        for v in bm.verts:
            v.select = (v.index in visible_indices)

        bmesh.update_edit_mesh(obj.data, destructive=False)

        # Hide everything else
        bpy.ops.mesh.hide(unselected=True)

        # --- RESTORE PREVIOUS SELECT MODE ---
        ts.mesh_select_mode = prev_select_mode
        bpy.ops.view3d.view_selected()

        bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}


class MESH_OT_show_all_vertex_groups(Operator):
    bl_idname = "mesh.show_all_vertex_groups"
    bl_label = "Show All Groups"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()

        for g in context.scene.linked_vertices_groups:
            g.visible = True

        return {'FINISHED'}