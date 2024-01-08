using UnityEngine;

public class MeshAnimation : MonoBehaviour
{
    public float AnimationSpeed { get; set; } = 0.05f; // Time in seconds for each mesh to be visible
    private MeshRenderer[] meshRenderers;
    private float timer;
    private int currentIndex = 0;

    void Start()
    {
        // Get all MeshRenderer components in child objects
        meshRenderers = GetComponentsInChildren<MeshRenderer>();

        // Optionally, start with all meshes hidden
        foreach (var meshRenderer in meshRenderers)
        {
            meshRenderer.enabled = false;
        }

        // Start with the first mesh
        if (meshRenderers.Length > 0)
        {
            meshRenderers[0].enabled = true;
        }
    }

    void Update()
    {
        // Update the timer
        timer += Time.deltaTime;

        // Check if it's time to switch to the next mesh
        if (timer >= AnimationSpeed)
        {
            // Hide the current mesh
            if (currentIndex < meshRenderers.Length)
            {
                meshRenderers[currentIndex].enabled = false;
            }

            // Move to the next mesh
            int numMesh = Mathf.RoundToInt(timer / AnimationSpeed);
            currentIndex = (currentIndex + numMesh) % meshRenderers.Length;

            // Show the next mesh
            meshRenderers[currentIndex].enabled = true;

            // Reset the timer
            timer = timer - numMesh * AnimationSpeed;
        }
    }
}
