import torch
from ultralytics import YOLO
from pathlib import Path
import yaml

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
                device='auto'):
    
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
            workers=4 if device == 'cuda' else 2
        )
        
        weights_path = f'runs/detect/{experiment_name}/weights'
        
        return results
        
    except Exception as e:
        print(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    train_class(
        data_yaml_path='data.yaml',
        experiment_name='aircraft_crash_detection',
        epochs=100
    )