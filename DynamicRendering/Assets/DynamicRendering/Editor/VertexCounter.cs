using UnityEngine;
using UnityEditor;

public class VertexCounter : EditorWindow
{
    private int totalVertices = 0;
    private int totalFaces = 0;
    private string selectedTag = "Untagged";
    private int meshCount = 0;

    [MenuItem("Tools/Vertex and Face Counter")]
    public static void ShowWindow()
    {
        GetWindow<VertexCounter>("Vertex Counter");
    }

    private void OnGUI()
    {
        EditorGUILayout.LabelField("Select Tag:");
        selectedTag = EditorGUILayout.TagField(selectedTag);

        if (GUILayout.Button("Count Vertices and Faces"))
        {
            CountVerticesAndFaces();
        }

        if (meshCount > 0)
        {
            EditorGUILayout.LabelField("Total Meshes: ", meshCount.ToString());
            EditorGUILayout.LabelField("Total Vertices: ", totalVertices.ToString());
            EditorGUILayout.LabelField("Average Vertices: ", (totalVertices / meshCount).ToString());
            EditorGUILayout.LabelField("Total Faces: ", totalFaces.ToString());
            EditorGUILayout.LabelField("Average Faces: ", (totalFaces / meshCount).ToString());
        }
        else
        {
            EditorGUILayout.LabelField("No meshes found for the selected tag.");
        }
    }

    private void CountVerticesAndFaces()
    {
        totalVertices = 0;
        totalFaces = 0;
        meshCount = 0;

        GameObject[] allObjects = GameObject.FindGameObjectsWithTag(selectedTag);
        foreach (GameObject obj in allObjects)
        {
            MeshFilter meshFilter = obj.GetComponent<MeshFilter>();
            if (meshFilter != null && meshFilter.sharedMesh != null)
            {
                Mesh mesh = meshFilter.sharedMesh;
                totalVertices += mesh.vertexCount;
                totalFaces += mesh.triangles.Length / 3;
                meshCount++;
            }
        }

        Debug.Log("Total Meshes: " + meshCount + 
                  ", Total Vertices: " + totalVertices + ", Average Vertices: " + (meshCount > 0 ? (totalVertices / meshCount).ToString() : "N/A") +
                  ", Total Faces: " + totalFaces + ", Average Faces: " + (meshCount > 0 ? (totalFaces / meshCount).ToString() : "N/A"));
    }
}
