import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "project", "ultralytics"))

from ultralytics import YOLO

model = YOLO(os.path.join(os.path.dirname(__file__), "..", "models", "best.pt"))

model.train(
    data=os.path.join(os.path.dirname(__file__), "..", "data", "processed"),
    epochs=30,
    imgsz=224,
    batch=32,
    project=os.path.join(os.path.dirname(__file__), "..", "runs"),
    name="classify",
)

print("Training done. Run: copy runs\\classify\\weights\\best.pt models\\base\\best.pt")
