from pathlib import Path
import yaml
import argparse
import os

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
    
    # Make the training directories (if they do not exist) 
    directories = [
        'dataset',
        'dataset/images',
        'dataset/images/train',
        'dataset/images/val',
        'dataset/images/test',
        'dataset/labels',
        'dataset/labels/train',
        'dataset/labels/val',
        'dataset/labels/test'
    ]
    
    for directory in directories:
        try:
            os.mkdir(directory) 
        except FileExistsError:
            print(f'directory \'{directory}\' already exists')
     
    # Copy and split image / data pairs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Performs YOLO model training setup")

    parser.add_argument("--objnames-path", type=str, required=True, help='Path to the annotated data')
    parser.add_argument("--images-path", type=str, required=False, help='Path to the training images')
    parser.add_argument("--annotations-path", type=str, required=False, help="Path to the annotation files")

    args = parser.parse_args()

    create_data_yaml(args.objnames_path)