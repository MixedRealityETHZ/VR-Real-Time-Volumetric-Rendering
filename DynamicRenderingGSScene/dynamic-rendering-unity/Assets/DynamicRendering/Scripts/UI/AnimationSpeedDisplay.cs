using UnityEngine;
using TMPro; // Make sure to import the TextMeshPro namespace

public class AnimationSpeedDisplay : MonoBehaviour
{
    public GameObject animatedObject;
    private MeshAnimation meshAnimator; // Replace with your mesh animation script's class name
    public TMP_Text speedDisplayText; // Assign your TextMeshPro text component here

    void Start()
    {
        if (animatedObject != null)
            {
                meshAnimator = animatedObject.GetComponent<MeshAnimation>();
                if (meshAnimator == null)
                {
                    Debug.LogError("SequenceRendererSpeedInterface script not found on the animated object.");
                }
            }
            else
            {
                Debug.LogError("Animated object not assigned.");
            }
    }

    // Update is called once per frame
    void Update()
    {
        if (meshAnimator != null && speedDisplayText != null)
        {
            speedDisplayText.text = $"Animation Speed: {1f/meshAnimator.AnimationSpeed:F0} Meshes/s";
        }
    }
}
