using UnityEngine;
using UnityEditor;

public class ApplyTagEditor : MonoBehaviour
{
    [MenuItem("GameObject/Apply Tag To Children", false, 10)]
    static void ApplyTagToChildren()
    {
        GameObject selectedObject = Selection.activeGameObject;

        if (selectedObject == null)
        {
            Debug.LogWarning("No GameObject selected. Please select a GameObject to apply a tag to its children.");
            return;
        }

        string tagToApply = selectedObject.tag; // Applies the parent's tag to its children

        if (!IsTagValid(tagToApply))
        {
            Debug.LogWarning("The tag '" + tagToApply + "' does not exist. Please ensure the selected GameObject has a valid tag.");
            return;
        }

        ApplyTagRecursively(selectedObject.transform, tagToApply);
        Debug.Log("Tag '" + tagToApply + "' applied to all children of " + selectedObject.name);
    }

    static void ApplyTagRecursively(Transform currentTransform, string tag)
    {
        foreach (Transform child in currentTransform)
        {
            child.gameObject.tag = tag;
            ApplyTagRecursively(child, tag);
        }
    }

    static bool IsTagValid(string tag)
    {
        foreach (string availableTag in UnityEditorInternal.InternalEditorUtility.tags)
        {
            if (availableTag.Equals(tag))
            {
                return true;
            }
        }
        return false;
    }
}
