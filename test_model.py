import argparse

from ultralytics import YOLO
from pathlib import Path

def test_model(model_path, test_images_dir=None):
    """Test the trained model on sample images"""
    
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    
    if test_images_dir is None:
        test_images_dir = Path('dataset/images/test')
    
    test_images = list(Path(test_images_dir).glob('*.jpg'))[:5] + \
                  list(Path(test_images_dir).glob('*.png'))[:5]
    
    if not test_images:
        print("No test images found")
        return
    
    print(f"Testing on {len(test_images)} images...")
    
    for img_path in test_images:
        print(f"Testing: {img_path.name}")
        results = model(str(img_path))
        
        for r in results:
            boxes = r.boxes
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    conf = box.conf.item()
                    cls = int(box.cls.item())
                    print(f"  Detected class {cls} with confidence {conf:.3f}")
            else:
                print("  No detections")

if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Tests a yolo trained model.") 
    
    args.add_argument('--target-model', type=str, required=True, help='Path to the trained model to test.') 
    args.add_argument('--target-images', type=str, required=False, help='Path to the images to test the model on.')
    
    parsed = args.parse_args()
    
    test_model(
        model_path=parsed.target_model,
        test_images_dir=parsed.target_images
    )
