from pathlib import Path
import yaml

'''
Pass the path to obj.names to generate the data.yaml file for yolo training
'''
def create_data_yaml(path):     
    obj_names_path = Path(path)
    
    if not obj_names_path.exists():
        raise FileNotFoundError(f"obj.names file not found: {path}")
    
    with open(obj_names_path, 'r') as f:
        class_names = [
            line.strip() 
            for line in f.readlines() 
            if line.strip()
            ]
    
    if not class_names:
        raise ValueError(f"No classes found in {path}")
    
    current_dir = Path.cwd().absolute()
    
    dataset_config = {
        'path': str(current_dir / 'dataset'),
        'train': 'images/train',
        'val': 'images/val', 
        'test': 'images/test',
        'nc': len(class_names),
        'names': class_names
    }
    
    with open('data.yaml', 'w') as f:
        yaml.dump(dataset_config, f, default_flow_style=False)

if __name__ == "__main__":
    create_data_yaml('CVAT_AircraftCrashed_YoloAnnotations/obj.names')