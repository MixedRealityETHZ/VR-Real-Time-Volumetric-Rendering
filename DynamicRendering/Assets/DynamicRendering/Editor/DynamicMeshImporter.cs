using UnityEngine;
using UnityEditor;
using System.IO;

public class DynamicMeshImporter : EditorWindow
{
    private string folderPath = "Meshes/Basketball/it400000_low_poly"; // Default path, change it as needed
    private GameObject targetGameObject;

    [MenuItem("Tools/Dynamic Mesh Sequence Import and Apply Textures")]
    private static void ShowWindow()
    {
        var window = GetWindow<DynamicMeshImporter>();
        window.titleContent = new GUIContent("Dynamic Mesh Importer");
        window.Show();
    }

    private void OnGUI()
    {
        GUILayout.Label("Dynamic Mesh Importer Settings", EditorStyles.boldLabel);
        
        folderPath = EditorGUILayout.TextField("Folder Path", folderPath);
        targetGameObject = EditorGUILayout.ObjectField("Target GameObject", targetGameObject, typeof(GameObject), true) as GameObject;

        if (GUILayout.Button("Import Meshes and Apply Textures"))
        {
            ImportMeshes();
        }
    }

    private void ImportMeshes()
    {
        if (targetGameObject == null)
        {
            Debug.LogError("Target GameObject is not set.");
            return;
        }

        // Application.dataPath ends with Assets
        string fullPath = Path.Combine(Application.dataPath, folderPath);
        if (!Directory.Exists(fullPath))
        {
            Debug.LogError("The specified folder path does not exist.");
            Debug.LogError(fullPath);
            return;
        }

        var directories = Directory.GetDirectories(fullPath);
        foreach (var dir in directories)
        {
            string meshName = Path.GetFileName(dir);
            string objPath = Path.Combine("Assets", folderPath, meshName, meshName + "_low_poly.obj");

            GameObject meshObj = AssetDatabase.LoadAssetAtPath<GameObject>(objPath);
            if (meshObj != null)
            {
                GameObject instance = PrefabUtility.InstantiatePrefab(meshObj) as GameObject;
                if (instance != null)
                {
                    instance.transform.SetParent(targetGameObject.transform);

                    // Load and apply textures
                    ApplyTextures(instance, dir);
                }
            }
            else
            {
                Debug.LogWarning($"Failed to load mesh: {meshName}");
                Debug.LogWarning(objPath);
            }
        }
    }

    private void ApplyTextures(GameObject obj, string directory)
    {
        // Find the child GameObject named "default"
        Transform defaultChild = obj.transform.Find("default");
        if (defaultChild == null)
        {
            Debug.LogWarning("No 'default' child found in " + obj.name);
            return;
        }

        Renderer renderer = defaultChild.GetComponent<Renderer>();
        if (renderer == null)
        {
            Debug.LogWarning("No Renderer found on 'default' child of " + obj.name);
            return;
        }

        Material mat = new Material(Shader.Find("Standard")); // Use appropriate shader
        renderer.material = mat;

        string relativeDir = Path.Combine(folderPath, Path.GetFileName(directory));
        string normalMapPath = Path.Combine("Assets", relativeDir, "normal_map.png"); // Adjust the file name as necessary
        string diffuseMapPath = Path.Combine("Assets", relativeDir, "diffuse_map.png"); // Adjust the file name as necessary

        // Texture2D normalMap = AssetDatabase.LoadAssetAtPath<Texture2D>(normalMapPath);
        // if (normalMap != null)
        //     mat.SetTexture("_BumpMap", normalMap);

        // Set normal map
        SetNormalMap(normalMapPath, mat);

        // Set diffuse map
        Texture2D diffuseMap = AssetDatabase.LoadAssetAtPath<Texture2D>(diffuseMapPath);
        if (diffuseMap != null)
            mat.SetTexture("_MainTex", diffuseMap);
    }

    private void SetNormalMap(string path, Material mat, float bumpScale = 0.0f)
    {
        // Import the texture as a normal map
        TextureImporter ti = AssetImporter.GetAtPath(path) as TextureImporter;
        if (ti != null)
        {
            ti.textureType = TextureImporterType.NormalMap;
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
        }

        Texture2D normalMap = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
        if (normalMap != null)
        {
            mat.SetTexture("_BumpMap", normalMap);
            mat.SetFloat("_BumpScale", bumpScale); // Set the bump scale
        }

    }
}