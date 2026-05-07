import json
import os

def get_custom_metadata(info, audio):
    path = info["path"]
    
    # Try to find JSON file in the same directory as the audio file
    json_path = os.path.splitext(path)[0] + ".json"
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            metadata = json.load(f)
        return metadata
    
    # Fallback: check if the path is relative to the current directory
    # (Sometimes paths are relative to the dataset root, but we're running from the project root)
    if not os.path.isabs(json_path):
        # We can try to search for the file if needed, but for now we'll just return empty
        pass

    return {}

