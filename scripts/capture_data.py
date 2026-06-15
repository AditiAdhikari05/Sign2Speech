"""
Record your own sign images for each letter.
Press the letter key (a-z) to start recording that class.
Press SPACE to record a "space" sign sample.
Press S to save the current frame manually.
Press Q to quit.
Auto-saves 30 frames per class when you hold the key.
"""

import cv2
import os
import time

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "train")
FRAMES_PER_CLASS = 30
DELAY_BETWEEN_FRAMES = 0.1  # seconds

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
print("Press a letter key to record that sign class.")
print("Press SPACE to record 'space' class. Press Q to quit.")

recording = False
current_class = None
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()

    if recording:
        class_dir = os.path.join(OUTPUT_DIR, current_class)
        os.makedirs(class_dir, exist_ok=True)
        existing = len(os.listdir(class_dir))
        filename = os.path.join(class_dir, f"{existing + 1:05d}.jpg")
        cv2.imwrite(filename, frame)
        frame_count += 1

        cv2.putText(display, f"Recording: {current_class} ({frame_count}/{FRAMES_PER_CLASS})",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if frame_count >= FRAMES_PER_CLASS:
            print(f"Done recording {current_class}. Total: {len(os.listdir(class_dir))} images.")
            recording = False
            current_class = None
            frame_count = 0

        time.sleep(DELAY_BETWEEN_FRAMES)
    else:
        cv2.putText(display, "Press a-z or SPACE to record. Q to quit.",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Data Capture", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord(" ") and not recording:
        current_class = "space"
        frame_count = 0
        recording = True
        print(f"Recording: space")
    elif ord("a") <= key <= ord("z") and not recording:
        current_class = chr(key).upper()
        frame_count = 0
        recording = True
        print(f"Recording: {current_class}")

cap.release()
cv2.destroyAllWindows()
