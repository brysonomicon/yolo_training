import torch
from ultralytics import YOLO
from pathlib import Path
import yaml
import argparse

"""
Train YOLO model with augmented data 
"""
def train_class(data_yaml_path, 
                experiment_name,
                epochs=100,
                model_size='n',
                imgsz=640,
                batch_size='auto',
                patience=10,
                device='auto',
                resume=False):
    
    if not Path(data_yaml_path).exists():
        raise FileNotFoundError(f"Data file not found: {data_yaml_path}")
    
    if device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    if batch_size == 'auto':
        batch_size = 16 if device == 'cuda' else 4
    
    with open(data_yaml_path, 'r') as f:
        dataset_config = yaml.safe_load(f)
    
    try:
        model_name = f'yolov8{model_size}.pt'
        model = YOLO(model_name)
        
        results = model.train(
            data=data_yaml_path,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch_size,
            name=experiment_name,
            project='runs/detect',
            device=device,
            save=True,
            plots=True,
            patience=patience,
            workers=4 if device == 'cuda' else 2,
            resume=resume
        )
        
        weights_path = f'runs/detect/{experiment_name}/weights'
        
        return results
        
    except Exception as e:
        print(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Starts the training of a YOLO model.') 
    
    args.add_argument('--data-path', type=str, required=True, help='Path to the data.yaml file.')
    args.add_argument('--experiment-name', type=str, required=True, help='Name of the model to train')
    args.add_argument('--epochs', type=int, required=False, default=100, help='Number of epochs')
    args.add_argument('--patience', type=int, required=False, default=10, help='Epocs to wait before not improvement')
    
    parsed = args.parse_args()
    
    train_class(
        data_yaml_path=parsed.data_path,
        experiment_name=parsed.experiment_name,
        epochs=parsed.epochs,
        patience=parsed.patience,
        resume=True
    )
