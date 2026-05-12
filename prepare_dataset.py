import os
import xml.etree.ElementTree as ET
import json
import glob

def get_pickup_type(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Find the parameter named 'Pick Up'
    for param in root.findall('.//parameter'):
        name = param.find('name')
        if name is not None and name.text == 'Pick Up':
            value = param.find('value').text
            if value:
                if 'Neck' in value:
                    return 'neck'
                elif 'Bridge' in value:
                    return 'bridge'
    return None

def process_directory(base_dir):
    xml_dir = os.path.join(base_dir, 'Lists', 'NoFX')
    audio_dir = os.path.join(base_dir, 'Samples', 'NoFX')
    
    if not os.path.exists(xml_dir) or not os.path.exists(audio_dir):
        print(f"Skipping {base_dir} - directories not found.")
        return
        
    xml_files = glob.glob(os.path.join(xml_dir, '*.xml'))
    count = 0
    
    for xml_file in xml_files:
        pickup_type = get_pickup_type(xml_file)
        if not pickup_type:
            continue
            
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all audiofile fileIDs
        for audio in root.findall('.//audiofile'):
            file_id = audio.find('fileID').text
            if file_id:
                wav_path = os.path.join(audio_dir, f"{file_id}.wav")
                json_path = os.path.join(audio_dir, f"{file_id}.json")
                
                # Check if the wav file exists before creating the json
                if os.path.exists(wav_path):
                    # Determine playing style from the directory name
                    play_style = "single note" if "monophon" in base_dir else "chord"
                    
                    metadata = {
                        "prompt": f"A sustained {play_style} of an electric guitar, {pickup_type} pickup"
                    }
                    with open(json_path, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    count += 1
                    
    print(f"Created {count} JSON files in {audio_dir}")

def main():
    base_dirs = [
        "IDMT-SMT-AUDIO-EFFECTS/Gitarre monophon",
        "IDMT-SMT-AUDIO-EFFECTS/Gitarre polyphon",
        "/scratch/th3622/IDMT-SMT-AUDIO-EFFECTS/Gitarre monophon",
        "/scratch/th3622/IDMT-SMT-AUDIO-EFFECTS/Gitarre polyphon"
    ]
    
    for b_dir in base_dirs:
        process_directory(b_dir)

if __name__ == "__main__":
    main()
