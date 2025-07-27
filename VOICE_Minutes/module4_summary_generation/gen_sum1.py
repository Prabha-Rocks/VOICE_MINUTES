from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from datetime import datetime

# 1. Load transcript text
with open("cleaned_output1.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# 2. Generate summary using TextRank
parser = PlaintextParser.from_string(transcript, Tokenizer("english"))
summarizer = TextRankSummarizer()
summary_sentences = summarizer(parser.document, 5)  # top 5

summary = "\n".join(str(sentence) for sentence in summary_sentences)

# 3. Extract action items (optional, rule-based)
actions = [
    line for line in transcript.split('\n')
    if line.lower().startswith(('action', 'decision', 'task'))
]

# 4. Add metadata
metadata = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "duration": "25 mins",
    "speakers": ["spk_0", "spk_1", "spk_2"]
}

# 5. Save to TXT
with open("summary_out1.txt", "w", encoding="utf-8") as f:
    f.write("📋 Meeting Summary:\n\n")
    f.write(summary + "\n\n")

    if actions:
        f.write("📌 Action Items / Decisions:\n")
        f.write("\n".join(actions) + "\n\n")

    f.write("🕒 Metadata:\n")
    f.write(f"Date: {metadata['date']}\n")
    f.write(f"Duration: {metadata['duration']}\n")
    f.write(f"Speakers: {metadata['speakers']}\n")

print("✅ Summary generated and saved as summary_out1.txt")
