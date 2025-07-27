import json

with open('clean_transcript.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

with open('clean_transcript.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(data['transcript'])
