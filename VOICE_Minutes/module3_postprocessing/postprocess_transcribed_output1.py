import json
import nltk
import re

# Download NLTK resources (only once)
nltk.download('punkt')

# 1. Load new raw transcript
with open('raw_Transcribed_output1.json') as f:
    data = json.load(f)

raw_text = data['results']['transcripts'][0]['transcript']

# 2. Remove filler words
filler_words = ['um', 'uh', 'like', 'you know', 'I mean']

def clean_filler(text):
    words = nltk.word_tokenize(text)
    return ' '.join([w for w in words if w.lower() not in filler_words])

cleaned_text = clean_filler(raw_text)

# 3. Format into paragraph and bullets
sentences = nltk.sent_tokenize(cleaned_text)
paragraph = ' '.join(sentences)
bullets = '\n'.join(f'- {s}' for s in sentences)

# 4. Extract speaker labels and timestamps (if any)
if 'speaker_labels' in data['results']:
    print("\n🎙️ Speaker Segments:")
    for seg in data['results']['speaker_labels']['segments']:
        speaker = seg['speaker_label']
        start = seg['start_time']
        end = seg['end_time']
        print(f"{speaker} [{start}s - {end}s]")

# 5. Save output
output = {
    "cleaned_transcript": paragraph,
    "bulleted_summary": bullets
}

with open('cleaned_output1.json', 'w') as f:
    json.dump(output, f, indent=4)

with open('cleaned_output1.txt', 'w') as f:
    f.write(paragraph)

print("\n✅ Cleaned output saved as cleaned_output1.json and cleaned_output1.txt")
