# Dynamic Mesh Rendering for Neural Implicit Representations
This repo contains unity rendering example of Gaussian Splatting scene. The rendering targets Meta Oculus Quest 2, Unity Version: 2022.3.10f1.
1. `UGS-package`: The existing [Unity package](https://github.com/aras-p/UnityGaussianSplatting) used to load Gaussian Splatting files.

2. `dynamic-rendering-unity`: Unity example scene and scripts. 
    - This scene integrates the animation sequence we acquired from [DynamicMeshGeneration](../DynmaicMeshGeneration/) to the Gaussian Splatting background.
    - You could use Quest Link with Unity to view the scene in Quest 2. This requires a computer running the project and could not build-into the device(so far).

3. `dynamic-rendering-unity-multiple-mesh`: Unity example scene and scripts. 
    - This scene is not shown in our project demo and report. We develop it to check the possibility of load multiple Gaussian splating files and display them through Quest Link.
    - You could use Quest Link with Unity to view the scene in Quest 2. This requires a computer running the project and could not build-into the device(so far).

You may need to re-import the Unity package. If you see the following error message
<img src="pic\Unity_Package_Manager_Error.png" alt="DemoScene" />
Clike on "continue" and enter the project

Go to `Window->packageManager`,click on the add botton at top left and choose `Add package from disk`, select the "package.json" file under the UGS-package folder, and re-open the project once the local package is imported successfully. Then you should be able to load the Gaussian Splatting files.
<img src="pic\reimport_step1.png" alt="DemoScene" />
<img src="pic\reimport_step2.png" alt="DemoScene" />
<img src="pic\reimport_step3.png" alt="DemoScene" />
<img src="pic\reimport_step4.png" alt="DemoScene" />

## dynamic-rendering-unity
The unity project to render the simplified the mesh, our target platform is Meta Oculus Quest 2. You may need to reimport the need package in your unity project([Here](dynamic-rendering-unity/Packages/manifest.json))

1. Our extracted/simplified meshes are under [Assets/DynamicRendering/DemoMeshSeq](dynamic-rendering-unity/Assets/DynamicRendering/DemoMeshSeq/), the Gaussian splating scene file are under [Assets/GaussianAssets](dynamic-rendering-unity/Assets/GaussianAssets), demo scene: [Assets/Scenes/DynamicRenderingDemo.unity](dynamic-rendering-unity/Assets/Scenes/DynamicRenderingDemo.unity)

2. Our C# scripts and custom shaders are under [Assets/DynamicRendering](dynamic-rendering-unity/Assets/DynamicRendering)
    - [Assets/DynamicRendering/Scripts](dynamic-rendering-unity/Assets/DynamicRendering/Scripts): script to animate mesh sequence, basic interaction to addjust the animation speed and basic UI display for mesh speed and FPS.
    - [Assets/DynamicRendering/Editor](dynamic-rendering-unity/Assets/DynamicRendering/Editor): Unity editor script. For scene complexity statistics, automatically import mesh sequence and apply custom material to all meshes in the sequence.
    - [Assets/DynamicRendering/Shaders](dynamic-rendering-unity/Assets/DynamicRendering/Shaders) and [Assets/dynamic-rendering-unity/Materials](dynamic-rendering-unity/Assets/DynamicRendering/Materials): Custom materials for vertex color only and shaders defined by shader graph.


<img src="pic\demo_scene_GS.png" alt="DemoScene" /> 

## dynamic-rendering-unity-multiple-mesh
This scene is not shown in our project demo and report. We develop it to check the possibility of load multiple Gaussian splating files and display them through Quest Link.

Currently, we don't have a dynamic mesh that is at suitable size for dynamic scene display. We do provide a script to translate the results obtained from [DynamicGaussian](https://github.com/JonathonLuiten/Dynamic3DGaussians) to ply files, while it lack the spherical harmonic part and hence could not be used in our project.

As a compromise solution, we use a simple GS file and rotates it to show the dynamic effect of the mesh. You could replace them with multiple GS files obtained from dynamic gaussian splatting as long as it could be loaded through the [Unity package](https://github.com/aras-p/UnityGaussianSplatting).

You could also add another Gaussian splat file as background. The file sequence and the static gaussian file should both work well in Unity and Quest 2.

1. The Gaussian Splating file we use here is under [Assets/GaussianAssets](dynamic-rendering-unity-multiple-mesh/Assets/GaussianAssets), demo scene: [Assets/Scenes/DynamicRenderingDemo.unity](dynamic-rendering-unity-multiple-mesh/Assets/Scenes/DynamicRenderingDemo.unity)

2. The script we used to transfer npz files from Dynamic Gaussian to ply files is [npz_convert](npz_convert.py)

3. Our C# scripts and custom shaders are under [Assets/DynamicRendering](dynamic-rendering-unity-multiple-mesh/Assets/DynamicRendering)
    - [Assets/DynamicRendering/Scripts](dynamic-rendering-unity-multiple-mesh/Assets/DynamicRendering/Scripts): script to animate mesh sequence and gaussian splat file sequence and basic UI display for FPS.


<img src="pic\GS_mesh_and_scene.png" alt="Multiple" /> 