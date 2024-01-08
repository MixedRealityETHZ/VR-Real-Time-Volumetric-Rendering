using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface SequenceRendererSpeedInterface
{
    public float GetAnimationSpeed();
    public void SetAnimationSpeed(float targetSpeed); // Time in seconds for each mesh to be visible
}

// render mesh in sequence one by one via a coroutine
public class ShowOneByOne : MonoBehaviour, SequenceRendererSpeedInterface
{
    public float animationSpeed = 0.1f; // Time in seconds for each mesh to be visible
    private MeshRenderer[] meshRenderers;

    public float GetAnimationSpeed(){
        return animationSpeed;
    }
    
    public void SetAnimationSpeed(float targetSpeed){
        animationSpeed = targetSpeed;
    }

    // Start is called before the first frame update
    void Start()
    {
        // Get all MeshRenderer components in child objects
        meshRenderers = GetComponentsInChildren<MeshRenderer>();

        // Optionally, start with all meshes hidden
        foreach (var meshRenderer in meshRenderers)
        {
            meshRenderer.enabled = false;
        }

        // Start the animation
        StartCoroutine(AnimateMeshes());
    }

    IEnumerator AnimateMeshes()
    {
        while (true) // Loop to keep the animation running
        {
            foreach (var meshRenderer in meshRenderers)
            {
                // Show one mesh
                meshRenderer.enabled = true;

                // Wait for the specified time
                yield return new WaitForSeconds(animationSpeed);

                // Hide the mesh again
                meshRenderer.enabled = false;
            }
        }
    }

    // Update is called once per frame
    // void Update()
    // {
        
    // }
}

