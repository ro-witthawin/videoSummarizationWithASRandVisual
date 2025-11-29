import json
import os
import cv2

def postprocess(video_path: str, raw: str) -> tuple[str, list[tuple[float, str]]]:
    result = json.load(open(raw, "r"))

    selected_ts = result["selected_timestamps"]
    summary_md = result["summary_md"]

    # ===========================
    # STEP 1 — Extract frames for selected timestamps
    # ===========================
    os.makedirs("frames", exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    extracted = []

    for ts in selected_ts:
        cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
        ok, frame = cap.read()
        if ok:
            fpath = f"frames/frame_{int(ts)}.jpg"
            cv2.imwrite(fpath, frame)
            extracted.append((ts, fpath))

    # ===========================
    # STEP 2 — Inject image paths into markdown
    # ===========================
    for ts, path in extracted:
        summary_md = summary_md.replace(
            f"(frames/frame_{ts}.jpg)",
            f"({path})"
        )
    
    md_text = summary_md

    # write file
    with open("session_summary.md", "w", encoding="utf-8") as f:
        f.write(md_text)

    return summary_md, extracted

raw_summary_md = open("raw_llm_output.json", "r", encoding="utf-8").read()
postprocess(video_path="videoDemo/MultimodalRAG.mp4", raw="raw_llm_output.json")