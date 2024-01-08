import bpy
import math

# Clear all objects in the scene
def clear_scene():
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.delete()

# Function to load a mesh from a PLY file
def load_mesh(file_path):
  bpy.context.scene.render.engine = 'CYCLES'
  bpy.context.scene.cycles.device = 'GPU'
  bpy.ops.import_mesh.ply(filepath=file_path)
  bpy.ops.object.shade_smooth(use_auto_smooth = False)
  bpy.ops.object.shade_flat()

# Function to create a material using vertex color
def create_vertex_color_material():
  material_name = "VertexColorMaterial"
  # Delete the material if it already exists
  if material_name in bpy.data.materials:
    bpy.data.materials.remove(bpy.data.materials[material_name])
  
  material = bpy.data.materials.new(name=material_name)
  material.use_nodes = True
  bsdf = material.node_tree.nodes.get("Principled BSDF")
  color_attr = material.node_tree.nodes.new('ShaderNodeAttribute')
  color_attr.attribute_name = 'Col'  # Use 'Col' for vertex color
  material.node_tree.links.new(bsdf.inputs['Base Color'], color_attr.outputs['Color'])
  return material

# Function to assign material to the mesh
def assign_material_to_mesh(mesh, material):
  if mesh.data.materials:
    mesh.data.materials[0] = material
  else:
    mesh.data.materials.append(material)

# Function to set up and position the camera
def setup_camera():
  # Create a new camera if not already existing
  if "Camera" not in bpy.data.objects:
    bpy.ops.object.camera_add(location=(0, 0, -3))
  camera = bpy.context.object
  camera.data.type = 'PERSP'

  # Point the camera towards positive Z-axis (0,0,0)
  camera.rotation_euler[0] = math.radians(180)  # Rotate X
  camera.rotation_euler[1] = 0.0  # Rotate Y
  camera.rotation_euler[2] = math.radians(180)  # Rotate Z

  # Set the camera as the active camera
  bpy.context.scene.camera = camera

# Function to add directional light
def add_directional_light():
  global light_added
  # Create a new sun light if not already existing
  if "Sun" not in bpy.data.objects:
      bpy.ops.object.light_add(type='SUN', location=(0, 0, -10))
  light = bpy.context.object
  light.data.energy = 1.0  # Adjust the light strength as needed

  # Point the light towards positive Z-axis
  light.rotation_euler[0] = math.radians(180)  # Rotate X by 90 degrees
  light.rotation_euler[1] = 0.0
  light.rotation_euler[2] = 0.0

  light_added = True

# Function to modify the output path
def modify_output_path(base_path, light_added):
  if light_added:
    path_without_extension = base_path.rsplit('.', 1)[0]
    extension = base_path.split('.')[-1]
    return f"{path_without_extension}_with_light.{extension}"
  else:
    return base_path

# Function to render the scene
def render_scene(output_path):
  # Set render resolution
  bpy.context.scene.render.resolution_x = 1080
  bpy.context.scene.render.resolution_y = 1080
  bpy.context.scene.render.filepath = output_path
  bpy.context.scene.render.image_settings.file_format = 'PNG'

  # Render the scene
  bpy.ops.render.render(write_still=True)

# Example usage
file_path = r'.\basketball_color\it400000_000000_downsample\5x.ply'  # Replace with your mesh file path
output_path = r'.\mesh_psnr\basketball\downsample_5x.png'  # Replace with your desired output file path

# Initialize a flag to track if the light has been added
light_added = False

clear_scene()
load_mesh(file_path)
material = create_vertex_color_material()
assign_material_to_mesh(bpy.context.object, material)
setup_camera()
add_directional_light()
# Modify the output path based on whether the light was added
output_path = modify_output_path(output_path, light_added)
render_scene(output_path)

