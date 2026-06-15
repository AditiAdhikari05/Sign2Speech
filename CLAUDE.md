# Sign2Speech — Claude Code Context

## Project Vision (What Makes This Different)

This is NOT another letter-speller. It's the **first bidirectional, sentence-level, personalized ASL communication app** on a plain phone camera — no gloves, no headsets, no special hardware.

**The gap we're bridging:**
- Deaf person signs → phone speaks full sentences (not just letters)
- Hearing person speaks → phone shows sign language videos on screen
- Users can fine-tune the model to their own signing style
- Emergency one-tap phrases (doctor, 911, allergies) — no signing needed
- Works offline, in public, with dignity

**Stack:** Python 3.8+ | Ultralytics YOLO11 | OpenCV | pyttsx3 | Whisper | Anthropic Claude API

**Ultralytics library path:** `C:\Users\ASUS\Desktop\project\ultralytics`
**This project path:** `C:\Users\ASUS\Desktop\sign-language-speech\`

---

## Final Architecture (What We're Building Toward)

```
DEAF PERSON'S SIDE                    HEARING PERSON'S SIDE
──────────────────                    ─────────────────────
Camera → YOLO11 letter detection      Microphone → Whisper STT
  → Letter buffer                       → English text
  → Claude API NLP cleanup              → Sign video lookup
  → Natural sentence                    → Pre-recorded clip plays on screen
  → pyttsx3 speaks aloud
```

One phone. Two people. No accessories. No internet required (after Claude API step is swapped offline).

---

## BUILD WORKFLOW — Checkpoints (Follow in Order)

Each checkpoint ends with something that WORKS and you can show someone.
Do not skip ahead. Complete one, feel good, move to next.

---

### CHECKPOINT 1 — Letters Detected Live
**Goal:** YOLO reads your hand signs and shows the letter on screen.

**Steps:**
1. Download ASL Alphabet dataset from Kaggle (search: "ASL Alphabet akash8992") → save to `data/raw/`
2. Organize into `data/processed/train/` and `data/processed/val/` — one folder per letter (A–Z + space, del, nothing)
3. Run `python scripts/train.py` — takes 30–60 min, leave it running
4. Copy `runs/classify/train/weights/best.pt` → `models/best.pt`
5. Run `python scripts/sign_to_speech.py` — hold up a letter sign and see it detected

**WIN:** Camera detects your hand sign and shows the letter. That's a working AI model you trained.

---

### CHECKPOINT 2 — Letters Become Words (Buffer)
**Goal:** System collects detected letters and assembles them into words automatically.

**Steps:**
1. Ask Claude to add a letter-buffer to `sign_to_speech.py`
2. Logic: hold a letter for 1.5s → it gets added to the buffer → space sign clears and speaks the word
3. Test: sign H-E-L-L-O → hear "HELLO" spoken aloud

**WIN:** You can spell a word and the phone says it. First real communication.
**No new tools needed — pure Python list logic inside the existing script.**

---

### CHECKPOINT 3 — Emergency Phrase Mode (One-Tap Speaking)
**Goal:** Press a number key → phone immediately speaks a critical phrase.

**Steps:**
1. Ask Claude to add hotkeys to `sign_to_speech.py`:
   - Key `1` → speaks "I need a doctor"
   - Key `2` → speaks "Call 911"
   - Key `3` → speaks "I am deaf"
   - Key `4` → speaks "I am allergic to..."
   - Key `5` → speaks "Please write it down"
2. Display the hotkey list on screen at all times

**WIN:** This is already useful. A deaf person at a hospital could use this TODAY.
**Effort: 30 minutes. Claude writes all the code.**

---

### CHECKPOINT 4 — Letters → Full Sentences (NLP Cleanup)
**Goal:** Instead of spelling out "W-H-E-R-E B-A-T-H-R-O-O-M", the phone says "Where is the bathroom?"

**Steps:**
1. Get a Claude API key from console.anthropic.com (free tier available)
2. Ask Claude to add an API call after the word buffer is full
3. Buffer feeds raw letters/words → Claude API fixes grammar → pyttsx3 speaks clean sentence
4. Add `anthropic` to `requirements.txt`

**Example:**
```
Signed: "I STORE GO WANT"
Spoken: "I want to go to the store"
```

**WIN:** First full-sentence output. This is what no other ASL project does.
**Note:** Needs internet for this step. We swap it offline in a later checkpoint if needed.**

---

### CHECKPOINT 5 — Hearing Person's Speech Appears as Text
**Goal:** The hearing person speaks, their words appear as large text on screen for the deaf person to read.

**Steps:**
1. Run `pip install openai-whisper` (fully offline, no OpenAI account needed)
2. Ask Claude to add a second thread to `sign_to_speech.py` that listens via microphone
3. Whisper converts speech → text → display on screen in large font
4. This runs simultaneously with the sign detection

**WIN:** Now both sides of the conversation work. Truly bidirectional.
**Whisper runs 100% offline on CPU — no internet, no API key.**

---

### CHECKPOINT 6 — Hearing Person's Speech → Sign Videos on Screen
**Goal:** When the hearing person speaks, the phone shows sign language videos so the deaf person can understand.

**Steps:**
1. Download pre-recorded ASL word videos for top 200 common words (free from ASLU / Handspeak)
2. Organize into `data/signs/` folder — one MP4 per word
3. Ask Claude to add video playback: Whisper detects word → look up MP4 → play on screen
4. Words with no video: just show the text in large font as fallback

**WIN:** Full bidirectional communication. Deaf person signs → phone speaks. Hearing person speaks → phone shows signs.

---

### CHECKPOINT 7 — Personalized Training (Your Unique Feature)
**Goal:** Users teach the app THEIR version of each sign. The model adapts to them.

**How it works:**
- Base model (trained by us) = 60% of the intelligence
- User records 10 examples of each sign → fine-tunes last layer only → 40% personalized
- Takes 2–3 minutes on a laptop, stored locally as `models/user_best.pt`

**Steps:**
1. Ask Claude to write `scripts/personalize.py`
2. Script: shows each letter on screen → user signs it 10 times → saves clips
3. Fine-tune only the last classification layer of the existing YOLO model
4. At inference time: if `models/user_best.pt` exists, use it; else use base model

**WIN:** The app literally learns the user's hands. No other sign language app does this.

---

### CHECKPOINT 8 — Package as a Simple App UI
**Goal:** Replace the raw OpenCV window with a clean, presentable interface.

**Steps:**
1. Ask Claude to build a simple Kivy or Tkinter UI
2. Left side: camera feed with sign detection
3. Right side: conversation history (what was signed, what was spoken)
4. Bottom: emergency phrase buttons (tap, not keyboard)
5. Top bar: mode toggle (Sign Mode / Listen Mode)

**WIN:** Looks like a real app. Showable to anyone.

---

## YOLO vs MediaPipe — Decision

**Stick with YOLO for now.** No MediaPipe needed until Checkpoint 7+.

- YOLO11-cls handles letter and word classification on plain images — it's enough for Checkpoints 1–4
- MediaPipe (hand keypoints) becomes useful if accuracy is bad in real lighting — we add it ONLY if needed
- YOLO11-pose is the YOLO-native way to get keypoints if we ever need them — same ecosystem, no new library

**Rule:** Don't switch tools unless the current tool fails. YOLO is not failing yet.

---

## IMPORTANT Rules (Never Violate)

- **NEVER** modify anything under `C:\Users\ASUS\Desktop\project\ultralytics\` — it is a third-party library
- **NEVER** hardcode file paths; always use `os.path.join` and `os.path.dirname(__file__)`
- **NEVER** add internet-dependent TTS (no gTTS, no cloud APIs) — pyttsx3 must remain offline
- **NEVER** commit `models/best.pt` or any `.pt`/`.onnx` file to git — they are large binaries
- **YOU MUST** keep scripts independent — no shared module imports between them

---

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Record your own sign data
python scripts/capture_data.py

# Train the model
python scripts/train.py

# Copy best weights after training
cp runs/classify/train/weights/best.pt models/best.pt

# Run live demo
python scripts/sign_to_speech.py

# Personalized fine-tuning (Checkpoint 7)
python scripts/personalize.py

# Export to ONNX (faster CPU inference)
python -c "from ultralytics import YOLO; YOLO('models/best.pt').export(format='onnx')"
```

---

## Dataset

| Property | Value |
|---|---|
| Phase 1 dataset | ASL Alphabet (Kaggle, akash8992) — 87,000 images, 29 classes |
| Phase 6 sign videos | ASLU / Handspeak — pre-recorded MP4s per word |
| Train/val split | 80/20 |
| Format | One subfolder per class under `train/` and `val/` |

```
data/processed/
  train/
    A/  B/  C/ ... Z/  space/  del/  nothing/
  val/
    A/  B/  C/ ... Z/  space/  del/  nothing/
data/signs/
  hello.mp4  thankyou.mp4  doctor.mp4  ...
```

---

## Model Configuration

| Setting | Value | Reason |
|---|---|---|
| Base model | `yolo11n-cls.pt` | Fastest; real-time on CPU |
| Image size | 224 | Standard for classification |
| Epochs | 50 | Sufficient for ASL fine-tuning |
| Batch size | 64 | Reduce to 32 if OOM |
| Confidence threshold | 0.85 | Reduces false positives |
| Hold duration | 1.5s | Prevents accidental registration |

---

## Key Files

| File | Purpose |
|---|---|
| `scripts/sign_to_speech.py` | Main entry point — sign detection + TTS + emergency phrases |
| `scripts/train.py` | Training script |
| `scripts/capture_data.py` | Data collection |
| `scripts/personalize.py` | User fine-tuning (Checkpoint 7) |
| `models/best.pt` | Base trained weights |
| `models/user_best.pt` | User-personalized weights (generated, not committed) |
| `data/signs/` | Pre-recorded sign videos for hearing→deaf direction |
| `requirements.txt` | All dependencies |

---

## Current Status

- [x] Scripts written (capture_data, train, sign_to_speech)
- [x] Git repo live at github.com/AditiAdhikari05/Sign2Speech
- [ ] CHECKPOINT 1 — Download dataset + train + see letters live
- [ ] CHECKPOINT 2 — Letter buffer → word assembly
- [ ] CHECKPOINT 3 — Emergency phrase hotkeys
- [ ] CHECKPOINT 4 — NLP sentence cleanup via Claude API
- [ ] CHECKPOINT 5 — Whisper STT for hearing person's speech
- [ ] CHECKPOINT 6 — Sign videos displayed for hearing→deaf direction
- [ ] CHECKPOINT 7 — Personalized fine-tuning
- [ ] CHECKPOINT 8 — Clean app UI

---

## Do Not Touch

- `runs/` — auto-managed by Ultralytics
- `C:\Users\ASUS\Desktop\project\ultralytics\` — third-party library, read-only
- `data/raw/` — original downloaded data; never overwrite or delete
