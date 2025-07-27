from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from fpdf import FPDF
from datetime import datetime
import json

# Step 1: Load transcript text
with open("clean_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# Step 2: Generate summary using TextRank (Sumy)
parser = PlaintextParser.from_string(transcript, Tokenizer("english"))
summarizer = TextRankSummarizer()
summary_sentences = summarizer(parser.document, 5)  # top 5 sentences

summary = "\n".join(str(sentence) for sentence in summary_sentences)

# Step 3: Extract action items (optional, rule-based)
actions = [line for line in transcript.split('\n') if line.lower().startswith(('action', 'decision', 'task'))]

# Step 4: Add metadata
metadata = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "duration": "25 mins",
    "speakers": ["spk_0", "spk_1", "spk_2"]
}

# Step 5: Save as TXT
with open("meeting_summary.txt", "w", encoding="utf-8") as f:
    f.write("📋 Meeting Summary:\n\n")
    f.write(summary + "\n\n")

    if actions:
        f.write("📌 Action Items / Decisions:\n")
        f.write("\n".join(actions) + "\n\n")

    f.write("🕒 Metadata:\n")
    for key, value in metadata.items():
        f.write(f"{key.capitalize()}: {value}\n")

# Step 6: Save as PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "📋 Meeting Summary:\n\n" + summary)

if actions:
    pdf.multi_cell(0, 10, "\n📌 Action Items / Decisions:\n" + "\n".join(actions))

pdf.multi_cell(0, 10, f"\n🕒 Metadata:\n")
for key, value in metadata.items():
    pdf.multi_cell(0, 10, f"{key.capitalize()}: {value}")

pdf.output("meeting_summary.pdf")
