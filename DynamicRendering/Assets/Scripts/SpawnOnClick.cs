using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimpleInteraction : MonoBehaviour
{
    public Rigidbody Box;
    bool fire = false;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float triggerLeft = OVRInput.Get(OVRInput.RawAxis1D.LIndexTrigger);
        float triggerRight = OVRInput.Get(OVRInput.RawAxis1D.RIndexTrigger);

        if(triggerRight > 0.9f && !fire){
            fire = true;
            Instantiate(Box, new Vector3(Random.Range(-3,3),Random.Range(1,4),Random.Range(-3,3)), Quaternion.identity);
        }

        if(triggerRight < 0.1f && fire){
            fire = false;
        }
    }
}
