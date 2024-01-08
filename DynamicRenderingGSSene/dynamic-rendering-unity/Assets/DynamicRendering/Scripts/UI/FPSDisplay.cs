using UnityEngine;
using TMPro;

public class FPSDisplay : MonoBehaviour
{
    public TMP_Text infoText; // Assign your TextMeshPro text component here

    private float[] frameTimes;
    private int frameCount;

    void Start()
    {
        frameTimes = new float[32];
    }

    void Update()
    {
        // Update the array with the latest frame time
        frameTimes[frameCount % frameTimes.Length] = Time.unscaledDeltaTime;
        frameCount++;

        // Calculate the average of the stored frame times
        float sum = 0.0f;
        int count = Mathf.Min(frameCount, frameTimes.Length);
        for (int i = 0; i < count; i++)
        {
            sum += frameTimes[i];
        }
        float averageFrameTime = sum / count;
        float averageFps = 1.0f / averageFrameTime;

        // Update text
        infoText.text = $"FPS: {Mathf.Round(averageFps)}";
    }
}
