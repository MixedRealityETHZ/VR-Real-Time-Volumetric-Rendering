import bpy
import os
import sys

def is_selected(filename):
    # Extract the last three characters before the .ply extension
    number_str = filename[-7:-4]
    
    # Convert the string to an integer
    try:
        number = int(number_str)
    except ValueError:
        return False
    
    # Check if the number is a multiple of three
    return number % 100 == 0

def convert_format_and_get_stats(file, input_directory, output_directory):
    input_path = os.path.join(input_directory, file)
    output_path = os.path.join(output_directory, file.lower().replace('.ply', '.fbx'))
    
    num_vertices = 0
    num_faces = 0
    # Delete all existing objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import the PLY file
    bpy.ops.import_mesh.ply(filepath=input_path)

    # Gather statistics
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            # mesh_count += 1
            num_vertices += len(obj.data.vertices)
            num_faces += len(obj.data.polygons)
            # obj.rotation_euler = (0,0,0)
    
    # Export the scene to an FBX file
    bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)

    return num_vertices, num_faces

def batch_convert_format(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Get selected files
    selected_files = [f for f in os.listdir(input_directory) if f.endswith('.ply') and is_selected(f)]
    
    results = [convert_format_and_get_stats(f, input_directory, output_directory) for f in selected_files]
    
    # Calculate average vertices and faces
    total_vertices = sum([res[0] for res in results])
    total_faces = sum([res[1] for res in results])
    average_vertices = total_vertices / len(results) if results else 0
    average_faces = total_faces / len(results) if results else 0
    
    print(f"Average vertices: {average_vertices}")
    print(f"Average faces: {average_faces}")
    return average_vertices, average_faces

def main():
    # Default values
    default_input_directory = ''
    default_output_directory =  ''

    # Check command line arguments
    if len(sys.argv) == 3:
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
    elif len(sys.argv) == 1:
        input_directory = default_input_directory
        output_directory = default_output_directory
    else:
        print("Usage: script_name.py [input_directory] [output_directory]")
        sys.exit(1)

    batch_convert_format(input_directory, output_directory)

if __name__ == "__main__":
    main()
