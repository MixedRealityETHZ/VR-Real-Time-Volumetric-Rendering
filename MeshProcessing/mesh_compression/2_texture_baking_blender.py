import bpy
import os
import math

def create_normal_bake_material(obj, image_name, image_size=(2048, 2048)):
  # Check if an image with the given name already exists and remove it
  if image_name in bpy.data.images:
    bpy.data.images.remove(bpy.data.images[image_name])
  
  # Create a new image to bake to
  baked_img = bpy.data.images.new(image_name, width=image_size[0], height=image_size[1])

  # Check if a material with the given name already exists and remove it
  if "NormalBakeMaterial" in bpy.data.materials:
    bpy.data.materials.remove(bpy.data.materials["NormalBakeMaterial"])

  # Create a new material with nodes
  bake_mat = bpy.data.materials.new(name="NormalBakeMaterial")
  bake_mat.use_nodes = True
  nodes = bake_mat.node_tree.nodes

  # Add an Image Texture node and set its image
  img_tex_node = nodes.new(type='ShaderNodeTexImage')
  img_tex_node.image = baked_img
  img_tex_node.image.colorspace_settings.name = 'Non-Color'  # Set color space to non-color

  # Add a Normal Map node
  normal_map_node = nodes.new(type='ShaderNodeNormalMap')

  # Connect the Image Texture node to the Normal Map node
  bake_mat.node_tree.links.new(img_tex_node.outputs['Color'], normal_map_node.inputs['Color'])

  # Connect the Normal Map node to the Principled BSDF's Normal input
  bsdf = nodes.get('Principled BSDF')
  bake_mat.node_tree.links.new(normal_map_node.outputs['Normal'], bsdf.inputs['Normal'])

  # Assign the material to the object
  if obj.data.materials:
      obj.data.materials[0] = bake_mat
  else:
      obj.data.materials.append(bake_mat)

  return baked_img

def bake_normal_map(low_poly_obj, high_poly_obj, low_poly_dir, texture_size):
  # Name for the baked image
  image_name = "normal_map"

  # Create material and get the image used for baking
  baked_img = create_normal_bake_material(low_poly_obj, image_name, texture_size)

  # Setup for baking
  bpy.context.scene.render.engine = 'CYCLES'
  bpy.context.scene.cycles.device = 'GPU'
  # Adjust render settings - set max samples to 1024
  bpy.context.scene.cycles.samples = 1024

  # Select the low-poly and high-poly objects
  bpy.ops.object.select_all(action='DESELECT')
  high_poly_obj.select_set(True)
  low_poly_obj.select_set(True)
  bpy.context.view_layer.objects.active = low_poly_obj

  # Bake the normal map
  bpy.context.scene.render.bake.use_selected_to_active = True
  bpy.context.scene.render.bake.cage_extrusion = 0.02  # Set extrusion distance to 0.1 meters
  bpy.ops.object.bake(type='NORMAL')

  # Save the baked image
  baked_img.filepath_raw = os.path.join(low_poly_dir, image_name + ".png")
  baked_img.file_format = 'PNG'
  baked_img.save()

def create_diffuse_bake_material(obj, image_name, image_size=(2048, 2048)):
  # Check if an image with the given name already exists and remove it
  if image_name in bpy.data.images:
    bpy.data.images.remove(bpy.data.images[image_name])

  # Create a new image to bake to
  baked_img = bpy.data.images.new(image_name, width=image_size[0], height=image_size[1])

  # Check if a material with the given name already exists and remove it
  if "DiffuseBakeMaterial" in bpy.data.materials:
    bpy.data.materials.remove(bpy.data.materials["DiffuseBakeMaterial"])

  # Create a new material with nodes
  bake_mat = bpy.data.materials.new(name="DiffuseBakeMaterial")
  bake_mat.use_nodes = True
  nodes = bake_mat.node_tree.nodes

  # Add an Image Texture node and set its image
  img_tex_node = nodes.new(type='ShaderNodeTexImage')
  img_tex_node.image = baked_img

  # Connect the Image Texture node to the Principled BSDF's Base Color input
  bsdf = nodes.get('Principled BSDF')
  bake_mat.node_tree.links.new(img_tex_node.outputs['Color'], bsdf.inputs['Base Color'])

  # Assign the material to the object
  if obj.data.materials:
    obj.data.materials[0] = bake_mat
  else:
    obj.data.materials.append(bake_mat)

  return baked_img

def bake_diffuse_map(low_poly_obj, high_poly_obj, low_poly_dir, texture_size):
  # Name for the baked image
  image_name = "diffuse_map"

  # Create material and get the image used for baking
  baked_img = create_diffuse_bake_material(low_poly_obj, image_name, texture_size)

  # Setup for baking
  bpy.context.scene.render.engine = 'CYCLES'
  bpy.context.scene.cycles.device = 'GPU'
  # Adjust render settings - set max samples to 1024
  bpy.context.scene.cycles.samples = 1024

  # Select the low-poly and high-poly objects
  bpy.ops.object.select_all(action='DESELECT')
  high_poly_obj.select_set(True)
  low_poly_obj.select_set(True)
  bpy.context.view_layer.objects.active = low_poly_obj

  # Bake the diffuse map
  bpy.context.scene.render.bake.use_selected_to_active = True
  bpy.context.scene.render.bake.cage_extrusion = 0.02  # Set extrusion distance to 0.1 meters
  ## Set bake type to 'DIFFUSE' and disable 'Direct' and 'Indirect' contributions
  bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})

  # Save the baked image
  baked_img.filepath_raw = os.path.join(low_poly_dir, image_name + ".png")
  baked_img.file_format = 'PNG'
  baked_img.save()

def load_and_bake(high_poly_path, texture_size):
  # Construct the low-poly .obj file path based on the high-poly path
  parent_dir, mesh_name_with_ext = os.path.split(high_poly_path)
  mesh_name = os.path.splitext(mesh_name_with_ext)[0]
  low_poly_dir = os.path.join(parent_dir + "_low_poly", mesh_name)
  low_poly_path = os.path.join(low_poly_dir, mesh_name + "_low_poly.obj")

  # Check if the low-poly .obj file exists
  if os.path.exists(low_poly_path):
    # Clear existing objects in the scene by selecting and deleting them
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()  # Delete the selected objects

    # Load the high-poly .ply file
    bpy.ops.import_mesh.ply(filepath=high_poly_path)

    # Get the last imported object (high-poly mesh)
    high_poly_mesh = bpy.context.selected_objects[-1]
    high_poly_mesh.name = mesh_name

    # Correct the orientation of the high-poly object
    high_poly_mesh.rotation_euler[0] += math.radians(90) # 90 degrees in radians

    # Load the low-poly .obj file
    bpy.ops.import_scene.obj(filepath=low_poly_path)

    # Get the last imported object (low-poly mesh)
    low_poly_mesh = bpy.context.selected_objects[-1]
    low_poly_mesh.name = mesh_name + "_low_poly"

    # Turn off Auto Smooth for both high-poly and low-poly meshes
    high_poly_mesh = bpy.data.objects.get(mesh_name)
    low_poly_mesh = bpy.data.objects.get(mesh_name + "_low_poly")

    for mesh in [high_poly_mesh, low_poly_mesh]:
      bpy.ops.object.select_all(action='DESELECT')
      # Apply Shade Flat
      mesh.select_set(True)
      bpy.context.view_layer.objects.active = mesh
      bpy.ops.object.shade_smooth(use_auto_smooth = False)
      bpy.ops.object.shade_flat()

    # Assign material to high-poly mesh
    # Check if a material with the given name already exists and remove it
    if "HighPolyMaterial" in bpy.data.materials:
      bpy.data.materials.remove(bpy.data.materials["HighPolyMaterial"])
    # Create a new material
    high_poly_material = bpy.data.materials.new(name="HighPolyMaterial")
    high_poly_material.use_nodes = True

    # Get the material nodes
    nodes = high_poly_material.node_tree.nodes

    # Use vertex color for the base color
    if 'Col' in high_poly_mesh.data.vertex_colors:
      vertex_color_node = nodes.new(type='ShaderNodeVertexColor')
      vertex_color_node.layer_name = 'Col'
      bsdf = nodes.get('Principled BSDF')

      # Connect the vertex color to the base color of the Principled BSDF
      high_poly_material.node_tree.links.new(bsdf.inputs['Base Color'], vertex_color_node.outputs['Color'])

    # Assign the material to the high-poly mesh
    if high_poly_mesh.data.materials:
      high_poly_mesh.data.materials[0] = high_poly_material
    else:
      high_poly_mesh.data.materials.append(high_poly_material)

    # Perform normal map baking
    bake_normal_map(low_poly_mesh, high_poly_mesh, low_poly_dir, texture_size)

    # Perform diffuse map baking
    bake_diffuse_map(low_poly_mesh, high_poly_mesh, low_poly_dir, texture_size)
  else:
    pass

def process_directory(directory_path, texture_size):
  # Loop over all files in the given directory
  for file_name in os.listdir(directory_path):
    # Check if the file is a .ply file
    if file_name.endswith('.ply'):
      # Extract the numerical part of the file name
      file_number = int(os.path.splitext(file_name)[0])

      # Check if the file number is a multiple of 25
      if file_number % 20 == 0:
        # Construct the full file path for the high-poly mesh
        high_poly_path = os.path.join(directory_path, file_name)

        # Load the high-poly and corresponding low-poly models, and perform baking if possible
        load_and_bake(high_poly_path, texture_size)

if __name__ == "__main__":
  texture_size=(1024, 1024)

  # Path to the directory containing the .ply files
  directory_path = r".\basketball_color\it400000"

  # Process all .ply files in the directory
  process_directory(directory_path, texture_size)
