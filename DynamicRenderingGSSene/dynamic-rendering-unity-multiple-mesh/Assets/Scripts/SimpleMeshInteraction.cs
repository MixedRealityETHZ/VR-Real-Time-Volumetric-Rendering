using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimpleMeshInteraction : MonoBehaviour
{
    public GameObject targetObject; // The object to be controlled
    private Vector3 initialPosition;
    private Quaternion initialRotation;

    private Vector3 targetPosition;
    private Quaternion targetRotation;

    public Transform sceneCamera; // Assign your VR Camera here
    public float moveSpeed = 1.0f;
    public float rotationSpeed = 50.0f;
    private float step;

    // Start is called before the first frame update
    void Start()
    {
        if (targetObject != null)
        {
            initialPosition = targetObject.transform.position;
            initialRotation = targetObject.transform.rotation;
        }
        else
        {
            Debug.LogError("Target object not assigned.");
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Define step value for animation
        step = 5.0f * Time.deltaTime;

        if (targetObject != null)
        {
            if (OVRInput.Get(OVRInput.Button.One)) centerObject();

            if (OVRInput.Get(OVRInput.Button.Two)) resetObject();

            // if (OVRInput.Get(OVRInput.Axis1D.SecondaryHandTrigger)) centerObject();

            // if (OVRInput.Get(OVRInput.Axis1D.SecondaryIndexTrigger)) resetObject();
            
            // Move and rotate the target object with the right thumbstick
            Vector2 input = OVRInput.Get(OVRInput.Axis2D.SecondaryThumbstick);
            
            float rotationInput = OVRInput.Get(OVRInput.Axis2D.SecondaryThumbstick).x;
            
            if (OVRInput.Get(OVRInput.Axis1D.SecondaryIndexTrigger) > 0.5){
                targetObject.transform.Translate(new Vector3(input.x, 0, input.y) * moveSpeed * Time.deltaTime, Space.World);
            } else {
                targetObject.transform.Rotate(Vector3.up, rotationInput * rotationSpeed * Time.deltaTime);
            }
        }
    }

    void centerObject(){
    // Places cube smoothly at the center of the user's viewport and rotates it to face the camera
        targetPosition = sceneCamera.transform.position + sceneCamera.transform.forward * 3.0f;
        targetRotation = Quaternion.LookRotation(transform.position - sceneCamera.transform.position);

        transform.position = Vector3.Lerp(transform.position, targetPosition, step);
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, step);
    }

    void resetObject(){
        targetObject.transform.position = initialPosition;
        targetObject.transform.rotation = initialRotation;
    }
}