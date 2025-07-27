import json
import nltk
import re

# Download required NLTK resources (first time only)
nltk.download('punkt')

# 1. Load raw transcript
with open('raw_transcript.json') as f:
    data = json.load(f)

raw_text = data['results']['transcripts'][0]['transcript']

# 2. Remove filler words
filler_words = ['um', 'uh', 'like', 'you know', 'I mean']

def clean_filler(text):
    words = nltk.word_tokenize(text)
    clean_words = [w for w in words if w.lower() not in filler_words]
    return ' '.join(clean_words)

cleaned_text = clean_filler(raw_text)

# 3. Format into paragraph and bullets
sentences = nltk.sent_tokenize(cleaned_text)
paragraph = ' '.join(sentences)
bullets = '\n'.join(f'- {s}' for s in sentences)

# 4. Extract speaker labels and timestamps (if available)
if 'speaker_labels' in data['results']:
    print("\n🎙️ Speaker Segments:")
    segments = data['results']['speaker_labels']['segments']
    for seg in segments:
        speaker = seg['speaker_label']
        start = seg['start_time']
        end = seg['end_time']
        print(f"{speaker} [{start}s - {end}s]")

# 5. Save cleaned output
output = {
    "cleaned_transcript": paragraph,
    "bulleted_summary": bullets
}

with open('clean_transcript.json', 'w') as f:
    json.dump(output, f, indent=4)

with open('clean_transcript.txt', 'w') as f:
    f.write(paragraph)

print("\n✅ Cleaned transcript saved as JSON and TXT.")
