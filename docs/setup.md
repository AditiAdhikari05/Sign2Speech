# Setup Guide

## 1. Prerequisites
- Python 3.8 or newer
- Webcam
- ~5GB disk space for dataset + model

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Download Dataset (Checkpoint 1)
1. Go to Kaggle: https://www.kaggle.com/datasets/grassknoted/asl-alphabet
   - Alternative: search "ASL Alphabet akash8992" on Kaggle
2. Download and extract to `data/raw/`
3. Run the organize script (ask Claude to generate if needed)
4. Dataset should land in `data/processed/train/A/`, `data/processed/train/B/`, etc.

## 4. Train
```bash
make train
# or
python scripts/train.py
```

## 5. Promote weights
```bash
make promote
# copies runs/classify/train/weights/best.pt → models/base/best.pt
```

## 6. Run live demo
```bash
make demo
# or
python scripts/sign_to_speech.py
```

## 7. Claude API setup (Checkpoint 4)
1. Get key from https://console.anthropic.com
2. Copy `.env.example` to `.env`
3. Set `ANTHROPIC_API_KEY=your_key`
4. Set `use_claude_api: true` in `configs/inference.yaml`
