bl_info = {
    "name": "Blender AI Script Assistant",
    "author": "Your Name",
    "version": (1, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > BlenderAI",
    "description": "Generates Blender scripts from natural language using AI",
    "category": "3D View",
}

import bpy

# Property group
class BlenderProperties(bpy.types.PropertyGroup):
    user_prompt: bpy.props.StringProperty(
        name="Prompt",
        description="Describe what you want Blender to do",
        default="Drop a cloth onto a cube and ball"
    )
    script_output: bpy.props.StringProperty(
        name="Script Output",
        description="Generated script",
        default=""
    )

# Operator
class Blender_OT_GenerateScript(bpy.types.Operator):
    bl_idname = "Blender.generate_script"
    bl_label = "Generate and Run Script"

    def execute(self, context):
        props = context.scene.Blender_props
        prompt = props.user_prompt

        # Fake LLM script (cloth sim on cube + ball)
        fake_script = """
import bpy

# Reset to frame 1 before adding simulation
bpy.context.scene.frame_set(1)

# Delete all existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove old rigid body world if it exists
if bpy.context.scene.rigidbody_world:
    bpy.ops.rigidbody.world_remove()

# Create a new rigid body world
bpy.ops.rigidbody.world_add()

# Optional: clear cloth caches
for obj in bpy.data.objects:
    for mod in obj.modifiers:
        if mod.type == 'CLOTH':
            bpy.ops.ptcache.free_bake_all()

# --- Create Cube ---
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cube = bpy.context.active_object
cube.name = "GroundCube"
bpy.ops.rigidbody.object_add()
cube.rigid_body.type = 'PASSIVE'
cube.modifiers.new(name="Collision", type='COLLISION')

# --- Create Ball ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3))
ball = bpy.context.active_object
ball.name = "Ball"
bpy.ops.rigidbody.object_add()
ball.rigid_body.type = 'ACTIVE'
ball.rigid_body.mass = 1.0
ball.modifiers.new(name="Collision", type='COLLISION')

# --- Create Cloth ---
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 5))
cloth = bpy.context.active_object
cloth.name = "ClothPlane"

# Subdivide
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=25)
bpy.ops.object.mode_set(mode='OBJECT')

# Cloth physics
cloth_mod = cloth.modifiers.new(name="ClothSim", type='CLOTH')
cloth_mod.collision_settings.use_self_collision = True
cloth.modifiers.new(name="Collision", type='COLLISION')

# --- Materials (Optional) ---
mat_cube = bpy.data.materials.new(name="CubeMat")
mat_cube.diffuse_color = (0.2, 0.6, 1, 1)
cube.data.materials.append(mat_cube)

mat_ball = bpy.data.materials.new(name="BallMat")
mat_ball.diffuse_color = (1, 0.3, 0.3, 1)
ball.data.materials.append(mat_ball)

mat_cloth = bpy.data.materials.new(name="ClothMat")
mat_cloth.diffuse_color = (0.8, 0.8, 0.2, 1)
cloth.data.materials.append(mat_cloth)

# --- Frame Range ---
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 150
scene.rigidbody_world.point_cache.frame_start = 1
scene.rigidbody_world.point_cache.frame_end = 150
"""

        props.script_output = fake_script

        try:
            exec(fake_script, {'bpy': bpy})
            self.report({'INFO'}, "Simulation created successfully.")
        except Exception as e:
            self.report({'ERROR'}, f"Execution failed: {e}")

        return {'FINISHED'}

# UI Panel
class Blender_PT_MainPanel(bpy.types.Panel):
    bl_label = "Blender AI"
    bl_idname = "Blender_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlenderAI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.Blender_props

        layout.prop(props, "user_prompt")
        layout.operator("Blender.generate_script", text="Generate Script")

        if props.script_output:
            layout.label(text="Generated Code Preview:")
            box = layout.box()
            preview = str(props.script_output)[:200] + "..."
            box.label(text=preview)

# Registration
classes = [BlenderProperties, Blender_OT_GenerateScript, Blender_PT_MainPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.Blender_props = bpy.props.PointerProperty(type=BlenderProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.Blender_props

if __name__ == "__main__":
    register()
