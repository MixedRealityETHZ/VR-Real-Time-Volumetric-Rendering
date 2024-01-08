using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimpleSpeedAdjustment : MonoBehaviour
{
    public GameObject animatedObject; // Assign the animated object with the mesh animation script
    private SequenceRendererSpeedInterface meshAnimator; 

    public float speedChangeFactor = 1.1f; // Factor by which the speed changes
    public float normalSpeed = 0.05f; // Normal animation speed
    // Start is called before the first frame update
    void Start()
    {
        if (animatedObject != null)
            {
                meshAnimator = animatedObject.GetComponent<SequenceRendererSpeedInterface>();
                if (meshAnimator == null)
                {
                    Debug.LogError("SequenceRendererSpeedInterface script not found on the animated object.");
                }
                meshAnimator.SetAnimationSpeed(normalSpeed);
            }
            else
            {
                Debug.LogError("Animated object not assigned.");
            }
    }

    // Update is called once per frame
    void Update()
    {
        if (meshAnimator != null)
        {
            // Increase speed with Y button
            if (OVRInput.GetDown(OVRInput.Button.Four))
            {
                meshAnimator.SetAnimationSpeed(meshAnimator.GetAnimationSpeed() / speedChangeFactor);
            }

            // Decrease speed with X button
            if (OVRInput.GetDown(OVRInput.Button.Three))
            {
                meshAnimator.SetAnimationSpeed(meshAnimator.GetAnimationSpeed() * speedChangeFactor);
            }

            // Reset speed with left index trigger
            if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger))
            {
                meshAnimator.SetAnimationSpeed(normalSpeed);
            }
        }
    }
}
