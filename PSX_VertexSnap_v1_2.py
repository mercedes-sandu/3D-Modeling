bl_info = {
    "name": "PSX Style Vertex Snapping",
    "author": "Lucas Roedel",
    "version": (1, 2),
    "blender": (3, 10, 0),
    "location": "3D Viewport > Side panel",
    "description": "Adds a PSX style vertex snapping to selected objects with adjustable resolution",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy








# Adds a shrinkwrap modifier to all selected objects that snaps its nearest vertices to the grid
def add_snapmod(context):
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH' and "VertexSnap" not in obj.modifiers and "GRID" in bpy.context.scene.objects and obj.name != "GRID":
            mod = obj.modifiers.new("VertexSnap", 'SHRINKWRAP')
            mod.wrap_method = 'NEAREST_VERTEX'
            mod.target = bpy.data.objects["GRID"]


class addVertexSnap(bpy.types.Operator):
    """Adds a modifier to selected objects that snaps its vertices to the GRID"""
    bl_idname = "mod.add_vertex_snap"
    bl_label = "Add Modifier"

    def execute(self, context):
        add_snapmod(context)
        if "GRID" not in bpy.context.scene.objects:
            self.report({'ERROR'}, 'GRID object not found')
        return {'FINISHED'}
    
    
    
    
    
    
    
# Removes a shrinkwrap modifier to all selected objects that snaps its nearest vertices to the grid    
def remove_snapmod(context):
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for m in obj.modifiers:
                if m.name == "VertexSnap":
                    obj.modifiers.remove(m)


class removeVertexSnap(bpy.types.Operator):
    """Removes a modifier to selected objects that snaps its vertices to the GRID"""
    bl_idname = "mod.remove_vertex_snap"
    bl_label = "Remove Modifier"

    def execute(self, context):
        remove_snapmod(context)
        return {'FINISHED'}









# Adds a grid object named GRID with adjustable vert density   
def create_grid(context):
    if "GRID" in bpy.context.scene.objects:
        array_resolution = context.scene.array_resolution
        bpy.data.objects["GRID"].modifiers["Array X"].count = array_resolution
        bpy.data.objects["GRID"].modifiers["Array Y"].count = array_resolution
        bpy.data.objects["GRID"].modifiers["Array Z"].count = array_resolution
#        bpy.data.objects["GRID"].scale = (1/array_resolution, 1/array_resolution, 1/array_resolution)
        
    else:
        name = "GRID"
        grid_mesh = bpy.data.meshes.new(name)
        grid_obj = bpy.data.objects.new(name, grid_mesh)
        verts = []
        edges = []
        faces = []
        verts.append([0.0, 0.0, 0.0])
        grid_mesh.from_pydata(verts, edges, faces)

        my_coll = bpy.data.collections.new("GRID")
        bpy.context.scene.collection.children.link(my_coll)     
        my_coll.objects.link(grid_obj)
        grid_obj.hide_render = True
        bpy.data.objects["GRID"].display_type = 'BOUNDS'

        array_resolution = context.scene.array_resolution

        mod_array_x = grid_obj.modifiers.new('Array X', 'ARRAY')
        mod_array_x.use_relative_offset = False
        mod_array_x.use_constant_offset = True
        mod_array_x.constant_offset_displace[0] = 0.1
        mod_array_x.constant_offset_displace[1] = 0
        mod_array_x.constant_offset_displace[2] = 0
        mod_array_x.count = array_resolution

        mod_array_y = grid_obj.modifiers.new('Array Y', 'ARRAY')
        mod_array_y.use_relative_offset = False
        mod_array_y.use_constant_offset = True
        mod_array_y.constant_offset_displace[0] = 0
        mod_array_y.constant_offset_displace[1] = 0.1
        mod_array_y.constant_offset_displace[2] = 0
        mod_array_y.count = array_resolution

        mod_array_z = grid_obj.modifiers.new('Array Z', 'ARRAY')
        mod_array_z.use_relative_offset = False
        mod_array_z.use_constant_offset = True
        mod_array_z.constant_offset_displace[0] = 0
        mod_array_z.constant_offset_displace[1] = 0
        mod_array_z.constant_offset_displace[2] = 0.1
        mod_array_z.count = array_resolution
    
#        bpy.data.objects["GRID"].scale = (1/array_resolution, 1/array_resolution, 1/array_resolution)


class addGrid(bpy.types.Operator):
    """Adds a grid of vertices with adjustable density, named GRID"""
    bl_idname = "grid.add_grid"
    bl_label = "Add GRID"

    def execute(self, context):
        create_grid(context)
        return {'FINISHED'}













class PSXsnapPanel(bpy.types.Panel):
    """Creates a Panel for PSX Vertex Snap in the UI Panels"""
    bl_label = "PSX Vertex Snap"
    bl_idname = "PT_vertexsnap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PSX Vertex Snap"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
            
        # Add grid button
        layout.label(text="Add GRID for the vertices to snap")
        layout.label(text="WARNING: high density values may slow blender down")
        row = layout.row()
        row.scale_y = 1
        row.prop(context.scene, 'array_resolution')
        row = layout.row()
        row.scale_y = 1.5
        row.operator("grid.add_grid")

        # Add modifiers button
        layout.label(text="Adds or removes snap modifier to selected objects")
        row = layout.row(align = True)
        row.scale_y = 1.5
        row.operator("mod.add_vertex_snap")
        row.operator("mod.remove_vertex_snap")

        
        
        
        
        


def register():
    bpy.utils.register_class(addVertexSnap)
    bpy.utils.register_class(removeVertexSnap)
    bpy.types.Scene.array_resolution = bpy.props.IntProperty(
    name = 'GRID density', min = 1
) 
    bpy.utils.register_class(addGrid)
    bpy.utils.register_class(PSXsnapPanel)


def unregister():
    bpy.utils.unregister_class(addVertexSnap)
    bpy.utils.unregister_class(removeVertexSnap)
    del bpy.types.Scene.array_resolution
    bpy.utils.unregister_class(addGrid)
    bpy.utils.unregister_class(PSXsnapPanel)


if __name__ == "__main__":
    register()
