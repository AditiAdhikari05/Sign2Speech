# Common commands — run with: make <target>
# Example: make train

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

capture:
	python scripts/capture_data.py

train:
	python scripts/train.py

demo:
	python scripts/sign_to_speech.py

personalize:
	python scripts/personalize.py

test:
	pytest tests/ -v

promote:
	copy runs\classify\train\weights\best.pt models\base\best.pt

export-onnx:
	python -c "from ultralytics import YOLO; YOLO('models/base/best.pt').export(format='onnx')"

validate:
	python -c "from ultralytics import YOLO; YOLO('models/base/best.pt').val(data='data/processed')"

clean-runs:
	rmdir /s /q runs
