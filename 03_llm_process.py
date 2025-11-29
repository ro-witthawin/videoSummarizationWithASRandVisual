import json
import os
import cv2
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer


def process_session_llm_select(transcript_path, 
                               model_name="scb10x/typhoon2.1-gemma3-12b",
                               max_images=10):

    # ===========================
    # STEP 1 — Load transcript
    # ===========================
    with open(transcript_path, "r") as f:
        transcript = json.load(f)

    transcript = sorted(transcript, key=lambda x: x["start"])

    # Convert to dialogue format
    dialogue = "\n".join(
        f"[{t['start']:.2f}s] {t['speaker']}: {t['word']}"
        for t in transcript
    )

    # ===========================
    # STEP 2 — Build prompt for LLM
    # ===========================
    prompt = f"""
You will:
1. Read the transcript
2. Select the BEST timestamps where images should be extracted from the video
   - max {max_images}
   - choose timestamps that represent KEY MOMENTS:
       * speaker changes
       * important content
       * emotional reactions
       * slide transitions
3. Produce a FINAL Markdown summary that includes:
   - Executive Summary
   - Speaker highlights
   - Timeline summary
   - Markdown placeholders for images like:

        ![Image at {{ts}}s](frames/frame_{{ts}}.jpg)
   - Final Summary

4. Output JSON ONLY in this schema:

{{
  "summary_md": ".... markdown here ...",
  "selected_timestamps": [1.23, 5.88, 28.10]
}}

--------------------------
TRANSCRIPT:
{dialogue}
--------------------------

Select timestamps + produce summary now.
"""

    # ===========================
    # STEP 3 — Load model
    # ===========================
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cpu"
    )
    print("Model loaded.")
    # print("propt :", prompt)
    with open("summary_prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    print("Inputs prepared.")
    streamer = TextStreamer(tokenizer, skip_prompt=True)
    print("Streamer created.")
    output = model.generate(
        **inputs,
        max_new_tokens=2048,
        temperature=0.5,
        top_p=0.95,
        streamer=streamer,
    )
    raw = tokenizer.decode(output[0], skip_special_tokens=True)

    # ===========================
    # STEP 4 — Parse LLM JSON
    # ===========================
    json_start = raw.find("{")
    json_end = raw.rfind("}") + 1
    json_str = raw[json_start:json_end]

    json.dump(json_str, open("raw_llm_output.json", "w"), indent=2)
    print("Raw LLM output saved to raw_llm_output.json")
    

process_session_llm_select("merged_transcript.json")