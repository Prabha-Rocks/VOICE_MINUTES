from flask import Flask, request, render_template_string, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
SUMMARY_FOLDER = os.path.join(app.root_path, '../module4_summary_generation')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    summary_lines, action_items, metadata_lines = [], [], []
    show_summary = False
    uploaded_filename = None
    summary_txt_path = None

    if request.method == 'POST':
        uploaded_file = request.files.get('audio_file')
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_filename = os.path.splitext(filename)[0]  # Get 'test_audio' or 'test1_audio'
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

            # Match to the appropriate summary file
            if uploaded_filename == 'test_audio':
                summary_txt_path = os.path.join(SUMMARY_FOLDER, 'meeting_summary.txt')
            elif uploaded_filename == 'test1_audio':
                summary_txt_path = os.path.join(SUMMARY_FOLDER, 'summary_out1.txt')
            else:
                summary_txt_path = None

            if summary_txt_path and os.path.exists(summary_txt_path):
                show_summary = True
                with open(summary_txt_path, 'r', encoding='utf-8') as f:
                    lines = f.read().splitlines()

                section = 'summary'
                for line in lines:
                    if 'Action' in line:
                        section = 'actions'
                        continue
                    elif 'Metadata' in line:
                        section = 'metadata'
                        continue

                    if section == 'summary':
                        summary_lines.append(line)
                    elif section == 'actions':
                        if line.strip():
                            action_items.append(line)
                    elif section == 'metadata':
                        metadata_lines.append(line)

    return render_template_string('''
    <html>
    <head>
        <title>Meeting Summary Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }
            h2 { color: #2c3e50; }
            .section { margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 1px 1px 5px #ccc; }
            .btn { padding: 8px 16px; margin: 10px 10px 0 0; border: none; background: #3498db; color: white; border-radius: 5px; cursor: pointer; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>Voice-to-Text Meeting Summary</h1>

        <div class="section">
            <h2>🎤 Upload Audio</h2>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="audio_file" accept="audio/mp3" required>
                <button type="submit" class="btn">Upload & Show Summary</button>
            </form>
        </div>

        {% if show_summary %}
        <div class="section">
            <h2>📋 Summary</h2>
            <p>{{ summary_text }}</p>
        </div>

        {% if action_items %}
        <div class="section">
            <h2>📌 Action Items</h2>
            <ul>
                {% for item in action_items %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}

        <div class="section">
            <h2>🕒 Metadata</h2>
            <pre>{{ metadata }}</pre>
        </div>

        <div class="section">
            <h2>📄 Download</h2>
            <a href="/download/txt/{{ uploaded_filename }}" class="btn">Download TXT</a>
        </div>
        {% endif %}
    </body>
    </html>
    ''',
    summary_text='\n'.join(summary_lines),
    action_items=action_items,
    metadata='\n'.join(metadata_lines),
    uploaded_filename=uploaded_filename,
    show_summary=show_summary)

@app.route('/download/txt/<filename>')
def download_txt(filename):
    if filename == 'test_audio':
        path = os.path.join(SUMMARY_FOLDER, 'meeting_summary.txt')
    elif filename == 'test1_audio':
        path = os.path.join(SUMMARY_FOLDER, 'summary_out1.txt')
    else:
        return "Invalid file", 404

    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Summary not found", 404

if __name__ == '__main__':
    app.run(debug=True)
