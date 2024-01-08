import bpy
import os
import math

def mesh_downsample(file_path):
  # Clear existing objects in the scene by selecting and deleting them
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.delete()  # Delete the selected objects

  # Load the object from the specified file path
  bpy.ops.import_mesh.ply(filepath=file_path)

  # Correct the orientation of the original object
  bpy.context.object.rotation_euler[0] += math.radians(90)  # 90 degrees in radians

  # Duplicate the object
  bpy.ops.object.duplicate()

  # Get the duplicated object (assuming it's the active one now)
  duplicated_object = bpy.context.active_object

  # Add a Decimate modifier with collapse method and ratio 1/200 to the duplicated object
  duplicated_object.modifiers.new(name='DecimateMod', type='DECIMATE')
  duplicated_object.modifiers['DecimateMod'].ratio = 0.1*0.1*0.5
  duplicated_object.modifiers['DecimateMod'].decimate_type = 'COLLAPSE'

  # Apply the modifier to the duplicated object
  bpy.ops.object.modifier_apply(modifier='DecimateMod')

  # Add a second Decimate modifier with planar method and 15 degrees angle limit
  duplicated_object.modifiers.new(name='DecimateModPlanar', type='DECIMATE')
  duplicated_object.modifiers['DecimateModPlanar'].angle_limit = math.radians(12) # 12 degrees in radians
  duplicated_object.modifiers['DecimateModPlanar'].decimate_type = 'DISSOLVE'

  # Apply the planar modifier
  bpy.ops.object.modifier_apply(modifier='DecimateModPlanar')

  # Perform Smart UV Project unwrapping on the duplicated object
  bpy.context.view_layer.objects.active = duplicated_object
  bpy.ops.object.editmode_toggle()
  bpy.ops.uv.smart_project(island_margin=0.02)
  bpy.ops.object.editmode_toggle()

  # Construct the output path based on the input path
  parent_dir, mesh_name_with_ext = os.path.split(file_path)
  mesh_name = os.path.splitext(mesh_name_with_ext)[0]
  output_dir = os.path.join(parent_dir + "_low_poly", mesh_name)
  os.makedirs(output_dir, exist_ok=True)
  output_path = os.path.join(output_dir, mesh_name + "_low_poly.obj")

  # Export the low-poly mesh as an .obj file
  bpy.ops.object.select_all(action='DESELECT')
  duplicated_object.select_set(True)
  bpy.ops.export_scene.obj(filepath=output_path, use_selection=True)

def process_directory(directory_path):
  # Loop over all files in the given directory
  for file_name in os.listdir(directory_path):
    # Check if the file is a .ply file
    if file_name.endswith('.ply'):
      # Extract the numerical part of the file name
      file_number = int(os.path.splitext(file_name)[0])

      # Check if process this file
      if file_number % 20 == 0:
        # Construct the full file path
        full_file_path = os.path.join(directory_path, file_name)

        # Process the file
        mesh_downsample(full_file_path)

if __name__ == "__main__":
  # Path to the directory containing the .ply files
  directory_path = r".\basketball_color\it400000"

  # Process all .ply files in the directory
  process_directory(directory_path)