from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty,
    StringProperty,
)

class LinkedVertexGroup(PropertyGroup):
    name: StringProperty()
    visible: BoolProperty(default=True)
    verts: StringProperty()  # comma-separated vertex indices