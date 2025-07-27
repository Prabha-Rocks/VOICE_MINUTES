import boto3
import os
from datetime import datetime
import mimetypes

# Constants
BUCKET_NAME = "meeting-audio-upload-bucket"
ALLOWED_EXTENSIONS = ['.mp3', '.mp4']

# Create S3 client (uses default credential chain)
s3 = boto3.client('s3')

# Validate file extension
def validate_file(file_path):
    return os.path.splitext(file_path)[1].lower() in ALLOWED_EXTENSIONS

# Upload file to S3
def upload_to_s3(file_path, uploader="anonymous"):
    if not validate_file(file_path):
        raise ValueError("Only .mp3 or .mp4 files allowed!")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found!")

    file_name = os.path.basename(file_path)
    timestamp = datetime.utcnow().isoformat() + "Z"  # UTC ISO format

    # Get content type (e.g., audio/mpeg)
    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, BUCKET_NAME, file_name, ExtraArgs={
            'Metadata': {
                'uploader': uploader,
                'timestamp': timestamp
            },
            'ContentType': content_type
        })

    print(f"✅ Uploaded '{file_name}' by {uploader} at {timestamp}")

# Example usage
upload_to_s3("test_audio.mp3", uploader="Prabha")
