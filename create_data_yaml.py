from pathlib import Path
import yaml
import argparse
import os

class ImageLabelPair:
    def __init__(self, path_to_image, path_to_label):
        self.path_to_image = path_to_image
        self.path_to_label = path_to_label
        
    def __str__(self):
        return f'({self.path_to_image}, {self.path_to_label})'


def create_data_yaml(path):     
    '''
    Pass the path to obj.names to generate the data.yaml file for yolo training
    '''
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

def create_training_directories():
    '''
    Creates the directory tree expected for model training.
    '''
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

def auto_split(path_to_labels, path_to_images):
    '''
    Splits training labels and images.
    70,20,10; training, validation, test
    '''
    path_to_labels = Path(path_to_labels)
    path_to_images = Path(path_to_images)
   
    bad_path = False
    bad_path_message = ""
    
    if not path_to_images.exists() or not path_to_images.is_dir():
        bad_path_message += f"training images directory does not exist or is not a directory,\n{path_to_labels}\n"
        bad_path = True
    if not path_to_labels.exists() or not path_to_labels.is_dir():
        bad_path_message += f"training labels directory does not exist or is not a directory,\n{path_to_images}"
        bad_path = True
        
    if (bad_path):
        raise FileNotFoundError(bad_path_message)
    
    pairs = []
    images = os.listdir(path_to_images)
    images_list = ""
    labels = os.listdir(path_to_labels)
    labels_list = ""
    
    for image, label in images, labels:
        pairs.append(ImageLabelPair(image, label))
        
    for imageLabel in pairs:
        print(imageLabel)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Performs YOLO model training setup")

    parser.add_argument('--objnames-path', type=str, required=True, help='Path to the annotated data')
    parser.add_argument('--images-path', type=str, required=True, help='Path to the training images')
    parser.add_argument('--annotations-path', type=str, required=True, help="Path to the annotation files")

    args = parser.parse_args()

    create_data_yaml(args.objnames_path)
    create_training_directories()
    auto_split(args.annotations_path, args.images_path)
    