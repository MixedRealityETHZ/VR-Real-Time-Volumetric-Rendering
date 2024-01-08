import pymeshlab as ml
import os
import sys
import multiprocessing

def is_selected(filename):
    # Extract the last three characters before the .ply extension
    number_str = filename[-7:-4]
    
    # Convert the string to an integer
    try:
        number = int(number_str)
    except ValueError:
        return False
    
    # Check if the number is a multiple of three
    return number <= 60

def convert_format_and_get_stats(file, input_directory, output_directory):
    input_path = os.path.join(input_directory, file)
    output_path = os.path.join(output_directory, file.replace('.ply', '.obj'))
    
    # Load the ply file
    ms = ml.MeshSet()
    ms.load_new_mesh(input_path)
    
    # Save as .obj
    ms.save_current_mesh(output_path)
    
    # Retrieve and return statistics
    current_mesh = ms.current_mesh()
    num_vertices = current_mesh.vertex_number()
    num_faces = current_mesh.face_number()
    
    print(f"Converted {file} to .obj and saved as {output_path}")
    return num_vertices, num_faces

def batch_convert_format(input_directory, output_directory, num_processes=None):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Get selected files
    selected_files = [f for f in os.listdir(input_directory) if f.endswith('.ply') and is_selected(f)]
    
    # Use multiprocessing to process files in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(convert_format_and_get_stats, [(f, input_directory, output_directory) for f in selected_files])
    
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
    default_input_directory = './basketball_meshes/it400000'
    default_output_directory = './basketball_meshes/it400000_obj'

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

    batch_convert_format(input_directory, output_directory, num_processes=2)

if __name__ == "__main__":
    main()
