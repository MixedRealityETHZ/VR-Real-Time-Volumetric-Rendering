using UnityEngine;
using TMPro;

public class BackgroundStatsDisplay : MonoBehaviour
{
    public TMP_Text infoText; // Assign your TextMeshPro text component here

    void Update()
    {
        int totalVertices = 0;
        int totalFaces = 0;

        GameObject[] backgroundObjects = GameObject.FindGameObjectsWithTag("StatBackground");
        foreach (GameObject obj in backgroundObjects)
        {
            MeshFilter meshFilter = obj.GetComponent<MeshFilter>();
            if (meshFilter != null && meshFilter.sharedMesh != null)
            {
                totalVertices += meshFilter.sharedMesh.vertexCount;
                totalFaces += meshFilter.sharedMesh.triangles.Length / 3; // Dividing by 3 as each face is typically a triangle
            }
        }

        infoText.text = "Background Total Vertices: " + totalVertices + " Total Faces: " + totalFaces;
    }
}
