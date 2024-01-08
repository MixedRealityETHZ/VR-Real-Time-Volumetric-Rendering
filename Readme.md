# Dynamic Mesh Rendering for Neural Implicit Representations
This repo contains mesh generation for dynamic objects, mesh simplification and unity rendering example scene. The rendering targets Meta Oculus Quest 2, Unity Version: 2022.3.10f1.
1. `DynamicMeshGeneration`: This is a modified version of [ResFields](https://github.com/markomih/ResFields) to enable the extractin of meshes with vertex colors.

2. `MeshProcessing`: Python script for Blender. The extracted raw mesh sequence with vertex color will be processed by Blender and transformed to simplified meshes and corresponding texture maps (diffuse map and normal map).

3. `DynamicRendering`: Unity example scene and scripts. 
    - The simplified mesh sequence, static mesh and background are put into one scene. There are also custom shaders and materials. 
    - Some C# scripts are used to perform scene complexity statistics, load mesh sequence, assign custom material to object sequence, and animate mesh sequence with user tunable speed.



| <img src="demo-scene\demo_scene_1.jpg" alt="DemoScene1" style="zoom: 30%;" /> | <img src="demo-scene\demo_scene_2.jpg" alt="DemoScene2" style="zoom: 33%;" /> |
| :------------------------------------------------------------: | :------------------------------------------------------------: |

## Mesh Generation
To generate meshes of static objects or scenes, we recommend using following Neural Reconstruction methods:
- [NeuS](https://github.com/Totoro97/NeuS)
- [Neuralangelo](https://github.com/NVlabs/neuralangelo)
- [sdfstudio](https://github.com/autonomousvision/sdfstudio)

For dynamic objects, we provide a modified version of [ResFields](https://github.com/markomih/ResFields) under [DynamicMeshGeneration](DynamicMeshGeneration).
Modifications are made in the following files to enable the extraction of meshes that carry vertex color information:
- [DynamicMeshGeneration/dyrecon/models/dysdf.py](DynamicMeshGeneration/dyrecon/models/dysdf.py)
- [DynamicMeshGeneration/dyrecon/models/utils.py](DynamicMeshGeneration/dyrecon/models/utils.py)

## Mesh Processing
```
scripts with `import bpy` are run inside blender
other scripts: python3.8 and pymeshlab
```

1. [surface_reconstruction/](MeshProcessing/surface_reconstruction): scripts for surface resonstruction from point cloud

2. [format_conversion/](MeshProcessing/format_conversion): scripts for format conversion, ply -> obj -> fbx.

3. [background_edit/](MeshProcessing/background_edit): script to trunk mesh outside the given region. This is used to remove the reconstruction artifacts in the background. 

4. [mesh_compression/](MeshProcessing/mesh_compression)
    - [1_mesh_downsample_blender.py](MeshProcessing/mesh_compression/1_mesh_downsample_blender.py): step 1, apply series of decimate modifiers to the original mesh and do uv unwrapping.
    - [2_texture_baking_blender.py](MeshProcessing/mesh_compression/2_texture_baking_blender.py): step 2, perform texture baking. First create a material that use vertex color as diffuse color for the original mesh. Then, perform texture baking for diffuse map and normal map.

5. [mesh_psnr/](MeshProcessing/mesh_psnr): 
    - Render the mesh using vertex color ([1_render_vertex_color.py](MeshProcessing/mesh_psnr/1_render_vertex_color.py)) and texture maps ([2_render_textured_mesh.py](MeshProcessing/mesh_psnr/2_render_textured_mesh.py)) in Blender. Camera positions and lighting configs can be adjusted in the scripts.
    - [3_calculate_psnr_ssim.py](MeshProcessing/mesh_psnr/3_calculate_psnr_ssim.py): Calculate the PSNR and SSIM between the images(can choose to use full image or just part of the image, e.g. only the head).

| <img src="MeshProcessing\mesh_psnr\plots\psnr.png" alt="PSNR" style="zoom: 50%;" /> | <img src="MeshProcessing\mesh_psnr\plots\ssim.png" alt="SSIM" style="zoom: 50%;" /> |
| :----------------------------------------------------------: | :----------------------------------------------------------: |

## Dynamic Rendering
The unity project to render the simplified the mesh, our target platform is Meta Oculus Quest 2. You may need to reimport the need package in your unity project([Here](DynamicRendering/Packages/manifest.json))

1. Our extracted/simplified meshes are under [Assets/Meshes](DynamicRendering/Assets/Meshes), demo scene: [Assets/Scenes/DynamicRenderingDemo.unity](DynamicRendering/Assets/Scenes/DynamicRenderingDemo.unity)

2. Our C# scripts and custom shaders are under [Assets/DynamicRendering](DynamicRendering/Assets/DynamicRendering)
    - [Assets/DynamicRendering/Scripts](DynamicRendering/Assets/DynamicRendering/Scripts): script to animate mesh sequence, basic interaction to addjust the animation speed and basic UI display for mesh speed and FPS.
    - [Assets/DynamicRendering/Editor](DynamicRendering/Assets/DynamicRendering/Editor): Unity editor script. For scene complexity statistics, automatically import mesh sequence and apply custom material to all meshes in the sequence.
    - [Assets/DynamicRendering/Shaders](DynamicRendering/Assets/DynamicRendering/Shaders) and [Assets/DynamicRendering/Materials](DynamicRendering/Assets/DynamicRendering/Materials): Custom materials for vertex color only and shaders defined by shader graph.
