import bpy
import bmesh
import math

# Specify the path to your .ply file
# file_path = r'path\mesh.ply'
# plane_size = 12
# xmin, xmax = -plane_size, plane_size
# zmin, zmax = -plane_size, plane_size
# ymin, ymax = -3, 10

file_path = r'path\mesh.ply'
xmin, xmax = -7, 7
zmin, zmax = -0.5, 3
ymin, ymax = -2, 3

# Clear existing objects in the scene by selecting and deleting them
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()  # Delete the selected objects

# Load the object from the specified file path
bpy.ops.import_mesh.ply(filepath=file_path)

# Get the imported object
imported_object = bpy.context.selected_objects[0]

# Rotate the object 90 degrees around the X-axis
# imported_object.rotation_euler[0] += math.radians(90)

# Ensure we are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Create a BMesh from the object
bm = bmesh.new()
bm.from_mesh(imported_object.data)

# Iterate over the vertices and mark those outside the specified region
verts_to_delete = [v for v in bm.verts if not (xmin <= v.co.x <= xmax and ymin <= v.co.y <= ymax and zmin <= v.co.z <= zmax)]

# Delete the marked vertices
bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')

# Update the mesh from the BMesh
bm.to_mesh(imported_object.data)
bm.free()

# Update the scene
# bpy.context.view_layer.update()
