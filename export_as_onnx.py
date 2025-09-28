from ultralytics import YOLO
from pathlib import Path

def export_to_onnx(weights_path, output_name=None):    
    if not Path(weights_path).exists():
        raise FileNotFoundError(f"Weights file not found: {weights_path}")
    
    model = YOLO(weights_path)
    
    model.export(
        format='onnx',
        imgsz=640,
        optimize=True,
        half=False,
        int8=False
    )
    
    onnx_path = weights_path.replace('.pt', '.onnx')
    
    return onnx_path

if __name__ == "__main__":
    weights_path = 'runs/detect/aircraft_crash_detection/weights/best.pt'
    export_to_onnx(weights_path)