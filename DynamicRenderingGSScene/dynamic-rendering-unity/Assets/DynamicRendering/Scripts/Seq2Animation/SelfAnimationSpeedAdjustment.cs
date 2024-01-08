using UnityEngine;

public class SelfAnimationSpeedAdjustment : MonoBehaviour
{
    // public GameObject animatedObject; // Assign the animated object with the mesh animation script
    private MeshAnimation meshAnimator; // Assuming your animation script is named VRMeshAnimator

    public float speedChangeFactor = 1.1f; // Factor by which the speed changes
    public float normalSpeed = 0.01f; // Normal animation speed

    void Start()
    {
        meshAnimator = GetComponent<MeshAnimation>();
        if (meshAnimator == null)
        {
            Debug.LogError("VRMeshAnimator script not found on the animated object.");
        }
    }

    void Update()
    {
        if (meshAnimator != null)
        {
            // Increase speed with Y button
            if (OVRInput.GetDown(OVRInput.RawButton.Y))
            {
                meshAnimator.AnimationSpeed /= speedChangeFactor;
            }

            // Decrease speed with X button
            if (OVRInput.GetDown(OVRInput.RawButton.X))
            {
                meshAnimator.AnimationSpeed *= speedChangeFactor;
            }

            // Reset speed with left index trigger
            if (OVRInput.Get(OVRInput.RawButton.LHandTrigger))
            {
                meshAnimator.AnimationSpeed = normalSpeed;
            }
        }
    }
}
