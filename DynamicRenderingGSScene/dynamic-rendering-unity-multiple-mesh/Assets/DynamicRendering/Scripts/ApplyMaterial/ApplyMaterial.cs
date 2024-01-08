using UnityEngine;

public class ApplyMaterial : MonoBehaviour
{
    public Material customMaterial; // Assign this in the inspector

    void Start()
    {
        MeshRenderer[] meshRenderers = GetComponentsInChildren<MeshRenderer>();

        foreach (MeshRenderer renderer in meshRenderers)
        {
            renderer.material = customMaterial;
        }
    }
}
