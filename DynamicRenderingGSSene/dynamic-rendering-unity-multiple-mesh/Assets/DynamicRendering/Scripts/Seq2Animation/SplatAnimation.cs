using UnityEngine;
using GaussianSplatting.Runtime; // Add the correct namespace for GaussianSplatRenderer

public class SplatAnimation : MonoBehaviour
{
    public float AnimationSpeed { get; set; } = 0.01f;
    private GaussianSplatRenderer[] splatRenderers; // Use GaussianSplatRenderer instead of GaussianMeshRenderer
    private float timer;
    private int currentIndex = 0;

    void Start()
    {
        splatRenderers = GetComponentsInChildren<GaussianSplatRenderer>();

        foreach (var splatRenderer in splatRenderers)
        {
            splatRenderer.enabled = false;
        }

        if (splatRenderers.Length > 0)
        {
            splatRenderers[0].enabled = true;
        }
    }

    void Update()
    {
        timer += Time.deltaTime;

        if (timer >= AnimationSpeed)
        {
            if (currentIndex < splatRenderers.Length)
            {
                splatRenderers[currentIndex].enabled = false;
            }

            int numSplats = Mathf.RoundToInt(timer / AnimationSpeed);
            currentIndex = (currentIndex + numSplats) % splatRenderers.Length;

            splatRenderers[currentIndex].enabled = true;

            timer = timer - numSplats * AnimationSpeed;
        }
    }
}
