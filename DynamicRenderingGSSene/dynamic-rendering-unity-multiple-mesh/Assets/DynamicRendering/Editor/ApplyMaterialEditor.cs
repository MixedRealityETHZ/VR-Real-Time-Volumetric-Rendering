using UnityEngine;
using UnityEditor;

public class ApplyMaterialEditor : EditorWindow
{
    private Material customMaterial;

    [MenuItem("Tools/Apply Custom Material")]
    private static void ShowWindow()
    {
        var window = GetWindow<ApplyMaterialEditor>();
        window.titleContent = new GUIContent("Apply Material");
        window.Show();
    }

    private void OnGUI()
    {
        GUILayout.Label("Apply Custom Material to Selected Meshes", EditorStyles.boldLabel);
        customMaterial = EditorGUILayout.ObjectField("Material", customMaterial, typeof(Material), false) as Material;

        if (GUILayout.Button("Apply Material"))
        {
            ApplyMaterialToSelected();
        }
    }

    private void ApplyMaterialToSelected()
    {
        if (customMaterial == null)
        {
            Debug.LogError("No material selected.");
            return;
        }

        foreach (GameObject obj in Selection.gameObjects)
        {
            MeshRenderer[] meshRenderers = obj.GetComponentsInChildren<MeshRenderer>();
            foreach (MeshRenderer renderer in meshRenderers)
            {
                Undo.RecordObject(renderer, "Apply Material");
                renderer.material = customMaterial;
            }
        }
    }
}
