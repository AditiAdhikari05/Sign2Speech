# Sign Language to Speech

A real-time tool that detects hand signs via webcam and converts them to spoken words using YOLO for classification and text-to-speech output.

## How It Works

```
Webcam → YOLO classifier (hand sign → letter) → Word buffer → Text-to-Speech
```

Hold a sign steady for 1.5 seconds to register it. When you sign "space", the current word is spoken aloud.

## Project Structure

```
sign-language-speech/
├── data/
│   ├── raw/                  # original downloaded dataset
│   ├── dataset.yaml          # YOLO dataset config
│   └── processed/
│       ├── train/images+labels/
│       └── val/images+labels/
├── models/
│   └── best.pt               # trained weights (after training)
├── scripts/
│   ├── capture_data.py       # record your own signs via webcam
│   ├── train.py              # train the YOLO model
│   └── sign_to_speech.py     # live demo: webcam → speech
└── runs/                     # auto-created by YOLO during training
```

## Setup

### 1. Install dependencies

```bash
pip install ultralytics pyttsx3 opencv-python
```

### 2. Get a dataset

**Option A — Download ASL Alphabet dataset (recommended to start)**
- Go to Kaggle and search: `ASL Alphabet` by akash8992
- Download and extract into `data/raw/`

**Option B — Record your own signs**
```bash
python scripts/capture_data.py
```
This opens your webcam and lets you record signs for each letter.

### 3. Prepare data

Your `data/processed/` folder needs one subfolder per class (letter):
```
data/processed/train/
    A/  B/  C/  D/  ...  Z/  space/  nothing/
data/processed/val/
    A/  B/  C/  D/  ...  Z/  space/  nothing/
```

Then create `data/dataset.yaml`:
```yaml
path: ./data/processed
train: train
val: val
nc: 29
names: ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
        'del','nothing','space']
```

### 4. Train the model

```bash
python scripts/train.py
```

Training takes ~30 minutes on a GPU, ~2 hours on CPU.
Best weights are saved to `runs/classify/train/weights/best.pt`.
Copy that file to `models/best.pt`.

### 5. Run the live demo

```bash
python scripts/sign_to_speech.py
```

- Hold a sign steady in front of the camera
- Wait 1.5 seconds for it to register (green text shows current letter)
- Sign **space** to speak the current word aloud
- Press **Q** to quit

## Model Details

| Setting       | Value                  |
|---------------|------------------------|
| Base model    | YOLOv11n-cls (nano)    |
| Input size    | 224x224                |
| Classes       | 29 (A-Z + space/del/nothing) |
| Framework     | Ultralytics YOLO       |

## Upgrading to Hand Pose (Advanced)

For better accuracy under varied lighting, switch to a pose-based approach:
1. Train `yolo11n-pose` on the hand-keypoints dataset (already in the ultralytics repo at `docs/en/datasets/pose/hand-keypoints.md`)
2. Extract 21 keypoint coordinates per frame
3. Feed coordinates into a small MLP classifier instead of raw image pixels

## Requirements

- Python 3.8+
- Webcam
- `ultralytics`, `pyttsx3`, `opencv-python`
- GPU optional but speeds up training significantly
