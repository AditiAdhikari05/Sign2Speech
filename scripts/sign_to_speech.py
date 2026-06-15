import cv2
import pyttsx3
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "project", "ultralytics"))

from ultralytics import YOLO

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "best.pt")
CONFIDENCE_THRESHOLD = 0.85
HOLD_SECONDS = 1.5  # seconds to hold a sign before it registers

if not os.path.exists(MODEL_PATH):
    print(f"Model not found at {MODEL_PATH}")
    print("Run scripts/train.py first, then copy best.pt to models/best.pt")
    sys.exit(1)

model = YOLO(MODEL_PATH)
engine = pyttsx3.init()
engine.setProperty("rate", 150)

cap = cv2.VideoCapture(0)
word_buffer = ""
last_letter = ""
last_sign_time = time.time()
letter_registered = False

print("Sign Language to Speech running. Press Q to quit.")
print("Hold a sign for 1.5 seconds to register it. Sign SPACE to speak the word.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    top1_idx = results[0].probs.top1
    top1_label = results[0].names[top1_idx]
    confidence = results[0].probs.top1conf.item()

    now = time.time()

    if confidence >= CONFIDENCE_THRESHOLD:
        if top1_label == last_letter:
            held_for = now - last_sign_time
            progress = min(held_for / HOLD_SECONDS, 1.0)

            if held_for >= HOLD_SECONDS and not letter_registered:
                letter_registered = True
                if top1_label == "space":
                    if word_buffer:
                        print(f"Speaking: {word_buffer}")
                        engine.say(word_buffer)
                        engine.runAndWait()
                        word_buffer = ""
                elif top1_label == "del":
                    word_buffer = word_buffer[:-1]
                elif top1_label != "nothing":
                    word_buffer += top1_label
                    print(f"Added: {top1_label} → buffer: {word_buffer}")

            bar_width = int(progress * 200)
            cv2.rectangle(frame, (10, 60), (10 + bar_width, 80), (0, 255, 0), -1)
            cv2.rectangle(frame, (10, 60), (210, 80), (255, 255, 255), 2)
        else:
            last_letter = top1_label
            last_sign_time = now
            letter_registered = False
    else:
        last_letter = ""
        last_sign_time = now
        letter_registered = False

    color = (0, 255, 0) if confidence >= CONFIDENCE_THRESHOLD else (0, 100, 255)
    cv2.putText(frame, f"Sign: {top1_label} ({confidence:.0%})", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"Word: {word_buffer}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, "Hold sign 1.5s | SPACE=speak | DEL=delete | Q=quit",
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow("Sign Language to Speech", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
