using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// render mesh in sequence one by one via a coroutine
public class ShowOneByOne2 : MonoBehaviour, SequenceRendererSpeedInterface
{
    public float animationSpeed = 0.1f; // Time in seconds for each mesh to be visible
    private GameObject[] targetObjects;

    public float GetAnimationSpeed(){
        return animationSpeed;
    }
    
    public void SetAnimationSpeed(float targetSpeed){
        animationSpeed = targetSpeed;
    }

    // Start is called before the first frame update
    void Start()
    {
        // Optionally, start with all meshes hidden
        foreach (var targetObject in targetObjects)
        {
            targetObject.SetActive(false);
        }

        // Start the animation
        StartCoroutine(AnimateObjects());
    }

    IEnumerator AnimateObjects()
    {
        while (true) // Loop to keep the animation running
        {
            foreach (var targetObject in targetObjects)
            {
                // Show one mesh
                targetObject.SetActive(true);

                // Wait for the specified time
                yield return new WaitForSeconds(animationSpeed);

                // Hide the mesh again
                targetObject.SetActive(false);
            }
        }
    }

    // Update is called once per frame
    // void Update()
    // {
        
    // }
}

