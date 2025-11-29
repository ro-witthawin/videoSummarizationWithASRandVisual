from pydub import AudioSegment, silence
from tqdm import tqdm
import os
import math

# -----------------------------
# CONFIG
# -----------------------------
INPUT_FILE = "videoDemo/output.wav"
OUTPUT_DIR = "audioChunks"
MIN_SILENCE_LEN = 1500   # 1.5 sec of silence
SILENCE_THRESH = -60     # dBFS
MAX_CHUNK_MS = 10 * 60 * 1000  # 5 minutes
# -----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load audio/video
audio = AudioSegment.from_file(INPUT_FILE)

# Detect silence ranges
silences = silence.detect_silence(
    audio,
    min_silence_len=MIN_SILENCE_LEN,
    silence_thresh=SILENCE_THRESH
)

# Convert to simple list of silence split points
split_points = [s[0] for s in silences]
split_points.append(len(audio))  # last segment end

# -----------------------------
# First pass: split by silence
# -----------------------------
segments = []
start = 0

print("# Split by silence")
for end in tqdm(split_points):
    if end - start > 1000:  # ignore segments < 1 sec
        segments.append(audio[start:end])
    start = end

# -----------------------------
# Second pass: ensure max 5 min per chunk
# -----------------------------
final_chunks = []

for seg in segments:
    if len(seg) <= MAX_CHUNK_MS:
        final_chunks.append(seg)
    else:
        # further subdivide long segments
        parts = math.ceil(len(seg) / MAX_CHUNK_MS)
        for i in range(parts):
            sub = seg[i * MAX_CHUNK_MS : (i + 1) * MAX_CHUNK_MS]
            final_chunks.append(sub)

# -----------------------------
# Export as MP3
# -----------------------------
print("# Export as MP3")

for i, chunk in enumerate(final_chunks):
    out_path = os.path.join(OUTPUT_DIR, f"chunk_{i:03d}.mp3")
    chunk.export(out_path, format="mp3")
    print(f"Saved: {out_path}")

print("Done! Total chunks:", len(final_chunks))

