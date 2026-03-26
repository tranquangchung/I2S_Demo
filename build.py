"""
Run once to generate index.html with transcripts embedded:
    python build.py

Then open index.html directly in any browser (file://) — no server needed.
"""

import os, json, re

def load_transcript(path):
    data = {}
    if not os.path.exists(path):
        print(f"  [WARN] Not found: {path}")
        return data
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '|' in line:
                id_, text = line.split('|', 1)
                data[id_.strip()] = text.strip()
    print(f"  Loaded {len(data)} entries from {path}")
    return data

print("Loading transcripts...")
en = load_transcript('images/SpokenCoco_English/transcript_ars_whisper_large_v3.txt')
ja = load_transcript('images/Stair_Japanese/transcript_whisper_kanji.txt')
vi = load_transcript('images/Flickr8k_Vietnamese/transcript_whisper.txt')

# Read the template
with open('index_template.html', encoding='utf-8') as f:
    html = f.read()

# Inject as JS variables
injection = f"""<script id="transcript-data">
  window.TRANSCRIPTS = {{
    en: {json.dumps(en, ensure_ascii=False, indent=2)},
    ja: {json.dumps(ja, ensure_ascii=False, indent=2)},
    vi: {json.dumps(vi, ensure_ascii=False, indent=2)}
  }};
</script>"""

html = html.replace('<!-- TRANSCRIPT_DATA -->', injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Open index.html in your browser.")