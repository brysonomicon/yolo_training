from pathlib import Path
import yaml
import argparse
import os
import shutil


class ImageLabelPair:
    def __init__(self, path_to_image: Path, path_to_label: Path, name_of_image: str, name_of_label: str):
        self.path_to_image = path_to_image
        self.path_to_label = path_to_label
        self.name_of_image = name_of_image
        self.name_of_label = name_of_label

        if not self.path_to_image.exists():
            raise FileNotFoundError(f'Images path {self.path_to_image} does not exist.')
        if not self.path_to_label.exists():
            raise FileNotFoundError(f'Label path {self.path_to_label} does not exist.')
        
    def __str__(self):
        return f'(\n{self.path_to_image},\n{self.path_to_label},\n{self.name_of_image},\n{self.name_of_label}\n)'


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
    shutil.rmtree('dataset') 
    
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
            
def valid_training_image_label_pairs(path_to_labels, path_to_images):
    '''
    Creates a list of the valid image and label pairs (ie, one exists to compliment the other)
    Uses the images list of reference.
    '''
    path_to_labels = Path(path_to_labels)
    path_to_images = Path(path_to_images)
    
    if not path_to_images.exists() or not path_to_images.is_dir():
        raise FileNotFoundError(f"training images directory does not exist or is not a directory,\n{path_to_labels}\n")
    if not path_to_labels.exists() or not path_to_labels.is_dir():
        raise FileNotFoundError(f"training labels directory does not exist or is not a directory,\n{path_to_images}")
    
    pairs = []
    images = os.listdir(path_to_images)
   
    # expect that for an image name, there is a label file as well 
    for image_name in images:
        image_path = path_to_images.joinpath(Path(image_name))
        image_name_no_ext, _ = os.path.splitext(image_name)
        label_name = f'{image_name_no_ext}.txt'
        label_path = path_to_labels.joinpath(Path(label_name))
        
        if (label_path.exists()):
            pairs.append(ImageLabelPair(
                image_path, label_path, image_name, label_name))
        
    # for imageLabel in pairs:
    #     print(imageLabel)
    
    print(f'Number of valid pairs {len(pairs)}')
    
    return pairs

def auto_split(image_label_pairs, p_train = 0.7, p_val = 0.2, p_test = 0.1):
    '''
    Splits training labels and images.
    70,20,10; training, validation, test
    '''
    npairs_total             = len(image_label_pairs)
    npairs_for_training      = round(npairs_total * p_train)
    npairs_for_validation    = round(npairs_total * p_val)
    npairs_for_testing       = round(npairs_total * p_test)
    
    pairs_for_training = image_label_pairs[
        0:\
        (npairs_for_training)]
    pairs_for_validation = image_label_pairs[
        npairs_for_training:\
        (npairs_for_training + npairs_for_validation)]
    pairs_for_test = image_label_pairs[
        (npairs_for_training + npairs_for_validation):\
        (npairs_for_training + npairs_for_validation + npairs_for_testing)]
    
    print(npairs_for_training + npairs_for_testing + npairs_for_validation)
   
    print(f'training pairs {len(pairs_for_training)}')
    print(f'validation pairs {len(pairs_for_validation)}')
    print(f'test pairs {len(pairs_for_test)}')
    print(f'total {len(pairs_for_training) + len(pairs_for_validation) + len(pairs_for_test)}')
   
    # for tpair in pairs_for_test:
    #     print(tpair) 
    
    # distribute into the appropriate directories
    
    print('... Copying training pairs ...')
    for train_pair in pairs_for_training:
        shutil.copy(train_pair.path_to_image, f'dataset/images/train/{train_pair.name_of_image}')
        shutil.copy(train_pair.path_to_label, f'dataset/labels/train/{train_pair.name_of_label}')
    
    print('... Copying validation pairs ...') 
    for val_pair in pairs_for_validation:
        shutil.copy(val_pair.path_to_image, f'dataset/images/val/{val_pair.name_of_image}')
        shutil.copy(val_pair.path_to_label, f'dataset/labels/val/{val_pair.name_of_label}')
    
    print('... Copying test pairs ...') 
    debug = 0
    for test_pair in pairs_for_test:
        shutil.copy(test_pair.path_to_image, f'dataset/images/test/{test_pair.name_of_image}')
        shutil.copy(test_pair.path_to_label, f'dataset/labels/test/{test_pair.name_of_label}')
        
        print("DEBUG", Path(f'dataset/labels/test/{test_pair.name_of_label}').exists())
        debug+=1
    print(debug)
    
    print(len(os.listdir('dataset/labels/test')))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Performs YOLO model training setup")

    parser.add_argument('--objnames-path', type=str, required=True, help='Path to the annotated data')
    parser.add_argument('--images-path', type=str, required=True, help='Path to the training images')
    parser.add_argument('--annotations-path', type=str, required=True, help="Path to the annotation files")

    args = parser.parse_args()

    create_data_yaml(args.objnames_path)
    create_training_directories()
    # auto_split(args.annotations_path, args.images_path)
    pairs = valid_training_image_label_pairs(args.annotations_path, args.images_path)
    auto_split(pairs)
    