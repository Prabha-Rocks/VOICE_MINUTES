# VOICE_MINUTES
🚀 Voice-to-Text Meeting Minutes Generator: An end-to-end pipeline that converts meeting audio into clean transcripts and concise summaries using AWS (S3, Lambda, Transcribe) and NLP (TextRank). View ,download reports via a Flask dashboard. Fast, accurate, and fully automated meeting documentation!
---

## 🔰 Project Overview

This project automates the entire pipeline of generating meeting minutes from voice recordings using cloud-native services and NLP techniques.

### 🎯 Objective:
- Convert uploaded `.mp3`/`.mp4` audio files to text.
- Clean and structure transcripts.
- Generate summaries and action points.
- Display summaries via an interactive dashboard.
- Enable downloading clean summaries in `.txt` format.

### 🛠️ Tools & Technologies:
- **AWS**: S3, Lambda, Amazon Transcribe
- **Python**: Boto3, NLTK, Sumy (TextRank), Flask
- **Frontend**: HTML templating (Jinja)
- **Others**: JSON, TXT handling, modular file structure

---

## 🧩 Module 1: Audio Upload & S3 Integration

### ✅ Features:
- CLI/Python script to upload `.mp3` or `.mp4` files.
- Validates audio file extension and naming conventions.
- Automatically stores metadata: file name, timestamp, user (optional).
- Shows status of upload in CLI/console.
  
### 🔧 AWS Service:
- Amazon S3

### 📁 S3 Bucket:
- `audio_upload1` — stores raw input audio files.

### 🗂️ Files:
- `upload_audio.py` — script to upload and validate audio files.

---

## 🧩 Module 2: AWS Transcribe Setup via Lambda

### ✅ Features:
- Automatically triggered Lambda function upon new audio upload.
- Lambda starts an **Amazon Transcribe Job** for audio → text conversion.
- Handles `.mp3` with optional speaker diarization.
- Stores **raw JSON transcript** output in another bucket.

### ⚙️ AWS Services:
- AWS Lambda (trigger & monitor)
- Amazon Transcribe (speech-to-text)
- Amazon S3

### 📁 Buckets:
- `audio_upload1` → input audio
- `transcribed_audio2` → raw transcription output

### 🗂️ Files:
- `triggerTranscribeJob.py` — Lambda code
- IAM roles + permissions configured

---

## 🧩 Module 3: Transcript Post-Processing

### ✅ Features:
- Cleans raw transcript JSON:
  - Removes filler words ("uh", "um", etc.)
  - Adds punctuation and formatting
  - Paragraph-wise segmentation
  - Retains timestamps and speaker tags
- Saves final output in `.txt` and `.json` formats.

### 🧠 NLP:
- **NLTK**: Tokenization, sentence segmentation

### 📁 Output Files:
- `clean_transcript.json`
- `clean_transcript.txt`
- (e.g., for 2nd audio: `cleaned_output1.txt`)

### 🗂️ Files:
- `postprocess_transcript.py`

---

## 🧩 Module 4: Meeting Summary Generation

### ✅ Features:
- Uses **TextRank algorithm** to extract:
  - Concise summary
  - Action items
  - Metadata: duration, speakers, date
- Saves result as `.txt`
- Works for any cleaned transcript.

### 🧠 NLP:
- **Sumy (TextRank)** for summarization
- Python `datetime` for metadata

### 📁 Output Files:
- `meeting_summary.txt` ← from `test_audio.mp3`
- `summary_out1.txt` ← from `test1_audio.mp3`

### 🗂️ Files:
- `generate_summary.py`

---

## 🧩 Module 5: Dashboard & Downloadable Reports

### ✅ Features:
- Built using **Flask** (`app.py`)
- Upload `.mp3` → Dashboard fetches and displays:
  - Clean summary
  - Action points
  - Metadata
- Dynamic linking: `test_audio.mp3` → `meeting_summary.txt`
- Allows `.txt` download of summaries
- Prevents crashes on missing files (fallback alerts)
  
### 🌐 Tech Used:
- Flask (Python backend)
- Jinja2 (HTML templating)


---

## 📦 Extra Features & Flexibility

- ✅ Modular and reusable code structure
- 🔄 Easy to swap summarization engine (e.g., GPT or HuggingFace)
- 🛡️ Can integrate authentication using Flask-Login
- 📈 Future enhancements:
  - Streamlit UI or React dashboard
  - CI/CD deployment
  - S3 lifecycle policies for cost optimization
  - Sentiment analysis
  - PDF report generation

---

## 💡 How It Works – End-to-End Flow

1. **User uploads audio** → `audio_upload1` (S3)
2. **Lambda triggers Transcribe** → stores raw transcript
3. **Post-processing script** cleans and structures transcript
4. **Summarization script** generates meeting minutes
5. **Dashboard** fetches and shows summary based on uploaded file
6. **Download .txt report** available to user

---

## 🚀 How to Run (Locally)

```bash
# 1. Upload your audio
python upload_audio.py test_audio.mp3

# 2. Post-process transcript after Transcribe finishes
python postprocess_transcript.py

# 3. Generate summary
python generate_summary.py

# 4. Launch dashboard
cd module5_dashboard
python app.py

