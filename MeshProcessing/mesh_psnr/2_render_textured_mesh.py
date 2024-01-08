import bpy
import os
import math

# Clear all objects in the scene
def clear_scene():
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.delete()

# Function to load a mesh from a obj file
def load_mesh(file_path):
  bpy.context.scene.render.engine = 'CYCLES'
  bpy.context.scene.cycles.device = 'GPU'
  bpy.ops.import_scene.obj(filepath=file_path)
  bpy.ops.object.shade_smooth(use_auto_smooth = False)
  bpy.ops.object.shade_flat()
  

def create_material_with_textures(diffuse_path, normal_path):
  material_name = "DiffuseNormalMaterial"
  # Delete the material if it already exists
  if material_name in bpy.data.materials:
    bpy.data.materials.remove(bpy.data.materials[material_name])
  
  # Create a new material
  material = bpy.data.materials.new(name=material_name)
  material.use_nodes = True
  nodes = material.node_tree.nodes
  links = material.node_tree.links

  # Clear default nodes
  for node in nodes:
    nodes.remove(node)

  # Create nodes: Diffuse Texture, Normal Map, BSDF, and Output
  diffuse_texture = nodes.new(type='ShaderNodeTexImage')
  diffuse_texture.image = bpy.data.images.load(diffuse_path)

  normal_map = nodes.new(type='ShaderNodeNormalMap')
  normal_texture = nodes.new(type='ShaderNodeTexImage')
  normal_texture.image = bpy.data.images.load(normal_path)
  normal_texture.image.colorspace_settings.name = 'Non-Color'  # Set color space to Non-Color

  bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
  material_output = nodes.new(type='ShaderNodeOutputMaterial')

  # Link nodes
  links.new(diffuse_texture.outputs['Color'], bsdf.inputs['Base Color'])
  links.new(normal_texture.outputs['Color'], normal_map.inputs['Color'])
  links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
  links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])

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
directory = r'.\basketball_color\it400000_low_poly_10x_12\000000'  # Replace with the directory containing your mesh and textures
output_path = r'.\mesh_psnr\basketball\textured_mesh_10x.png'  # Replace with your desired output file path
mesh_name = os.path.basename(os.path.normpath(directory))

file_path = os.path.join(directory, f"{mesh_name}_low_poly.obj")
diffuse_path = os.path.join(directory, "diffuse_map.png")
normal_path = os.path.join(directory, "normal_map.png")

# Initialize a flag to track if the light has been added
light_added = False

clear_scene()
load_mesh(file_path)

# Get the imported object
imported_object = bpy.context.selected_objects[0]
# Rotate the object 90 degrees around the X-axis
imported_object.rotation_euler[0] -= math.radians(90)

material = create_material_with_textures(diffuse_path, normal_path)
assign_material_to_mesh(imported_object, material)
setup_camera()
add_directional_light()
# Modify the output path based on whether the light was added
output_path = modify_output_path(output_path, light_added)
render_scene(output_path)

