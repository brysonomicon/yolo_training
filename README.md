# Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Get the augmented folder
unzip one of the image datasets from the SAR website
find the augmented folder. praise be to the previous team.

## Pass the path to obj.names to create_data_yaml
data.yaml is needed for yolo to train

## Split augmented images/txt into images/labels folders
Copy image/txt pairs from the augmented folder into:
- 70% to `dataset/images/train/` and `dataset/labels/train/`
- 20% to `dataset/images/val/` and `dataset/labels/val/`
- 10% to `dataset/images/test/` and `dataset/labels/test/`

there is an autosplit method in the docs but it's easy enough to do manually

## Generate data.yaml
```
python create_data_yaml.py
```

## Change experiment name in train.py
Change the main section:
```
train_class(
    data_yaml_path='data.yaml',
    experiment_name='[new_class]_detection', 
    epochs=100
)
```

### 6. Train
```
python train.py
```

### 7. Export to ONNX
```
python export_onnx.py
```

.onnx file will be output in `runs/detect/[experiment_name]/weights/best.onnx`