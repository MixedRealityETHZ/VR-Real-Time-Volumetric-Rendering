using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// render mesh in sequence one by one via update method to sync with frame
public class ShowOneByOneSyncFrame : MonoBehaviour, SequenceRendererSpeedInterface
{
    public float animationSpeed = 0.1f; // Time in seconds for each mesh to be visible
    private MeshRenderer[] meshRenderers;
    private float timer = 0f;
    private int currentIndex = 0;

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

        // Start with the first mesh
        if (meshRenderers.Length > 0)
        {
            meshRenderers[0].enabled = true;
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Update the timer
        timer = timer + Time.deltaTime;

        // Hide the current mesh
        if (currentIndex < meshRenderers.Length)
        {
            meshRenderers[currentIndex].enabled = false;
        }

        // Move to the next mesh
        // currentIndex = (currentIndex + (int) Math.Round(timer / animationSpeed)) % meshRenderers.Length;
        currentIndex = (currentIndex + (int) Math.Round(timer / animationSpeed)) % meshRenderers.Length;

        // Show the next mesh
        meshRenderers[currentIndex].enabled = true;

        timer = 0f;

    }
}
