# **📹 Video Session Summarization Pipeline**

### **ASR-Based Transcript + Visual Highlight Extraction + LLM Summarization**

This repository provides a **full multimodal summarization pipeline** that automatically converts a raw video into:

* **Diarized transcript** (multi-speaker ASR)
* **Key timestamps & visual highlight frames**
* **Session summary (Markdown + images)**
* **Final combined `.md` document** for distribution

The workflow is modular and consists of **four Python scripts**:

```
01_audio_splitter.py
02_asr_pipeline.py
03_llm_process.py
04_document_postprocess.py
```

---

## **📐 System Architecture**

### **1. Audio Processing**

* Extract audio from video in folder `videoDemo/XXXXXX.mp4`
* Split into chunks using silence detection
* Ensure chunks ≤ 10 minutes
* Save as `chunk_XXXX.mp3`

### **2. ASR + Diarization Pipeline**

* Run multi-speaker diarization
* Generate transcripts with timestamps
* Map local speakers → global speaker labels
* Merge everything into a unified `merged_transcript.json`

### **3. LLM Processing**

The LLM performs **all-in-one reasoning**:

* Reads transcript JSON
* Selects important timestamps (visual cues)
* Generates session summary (Markdown)
* Suggests key images to extract
* Outputs:

```json
{
  "summary_md": "...",
  "selected_timestamps": [1.61, 4.03, 23.5]
}
```

### **4. Document Post-processing**

* Extract frames from video using timestamps
* Inject images into markdown document
* Produce a final `session_summary.md`

---

# **🚀 Usage**

## **1. Prepare Environment**

```bash
pip install -r requirements.txt
```

Key libs:

* PyDub
* PyAnnote / SpeechBrain / NeMo ASR
* ffmpeg-python
* OpenAI / Typhoon LLM APIs
* Pillow
* Python-Markdown

Ensure **FFmpeg installed**:

```bash
sudo apt-get install ffmpeg
```

---

## **2. Step-by-step Run**

### **Step 1 — Audio Split**

```bash
python 01_audio_splitter.py
```

Outputs folder:

```
audioChunks/
    chunk_000.mp3
    chunk_001.mp3
    ...
```

---

### **Step 2 — Run ASR + Diarization**

```bash
python 02_asr_pipeline.py
```

Output:

```
merge_transcript.json
```

Structure includes:

* speaker
* text
* start / end
* audio file reference

---

### **Step 3 — LLM Summarization**

```bash
python 03_llm_process.py
```

Uses **SCB10X Typhoon2.1 Gemma3-12B (or your configured LLM)**
Outputs:

```
raw_llm_output.json
```

---

### **Step 4 — Final Markdown Assembly**

```bash
python 04_document_postprocess.py input.mp4
```

Outputs:

```
output/
  session_summary.md
  frames/
      frame_0004.jpg
      frame_0023.jpg
```

---

# **📁 Folder Structure**

```
.
├── 01_audio_splitter.py
├── 02_asr_pipeline.py
├── 03_llm_process.py
├── 04_document_postprocess.py
├── merge_transcript.json
├── llm_output.json
├── audioChunks/
└── frames/
```

---

# **🧠 LLM Prompting Logic**

LLM produces:

### ✔ Key timestamps

✔ Structured summary
✔ Explanation of key moments
✔ Markdown with image placeholders
✔ Final JSON for post-processing

Example expected return:

```json
{
  "summary_md": "# Session Summary...",
  "selected_timestamps": [3.5, 10.2, 40.8]
}
```

---

# **🧪 Example Final Markdown Output**

```
# Session Summary

## Executive Summary
...

## Key Visual Moments
![Image at 4s](frames/frame_0004.jpg)
![Image at 23s](frames/frame_0023.jpg)

## Detailed Timeline
...
```

---

# **🛠 Extending the Pipeline**

You can improve/add:

* [ ] Video OCR
* [ ] Slide extraction
* [ ] Speaker embedding clustering (MongoDB vector DB)
* [ ] Async streaming summarization
* [ ] Multi-language subtitles
* [ ] Whisper/Seamless M4T ASR fallback
