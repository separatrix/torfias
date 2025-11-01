import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_date_taken(image_path):
    try:
        image = Image.open(image_path)
        exif = image.getexif()
        if exif is None:
            return None
        
        for tag_id in exif:
            tag = TAGS.get(tag_id, tag_id)
            data = exif.get(tag_id)
            if tag == 'DateTime':
                # Parse the date string into a datetime object
                return datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
        return None
    except Exception:
        return None

# Folder containing images (relative or absolute path)
folder = "img"

# Valid image extensions
extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Get files with their dates
files_with_dates = []
for f in os.listdir(folder):
    if os.path.splitext(f)[1].lower() in extensions:
        full_path = os.path.join(folder, f)
        date_taken = get_date_taken(full_path)
        files_with_dates.append((f, date_taken or datetime.fromtimestamp(os.path.getmtime(full_path))))

# Sort files by date, newest first
files_with_dates.sort(key=lambda x: x[1], reverse=True)

# Print out <img> lines
for f, date in files_with_dates:
    print(f'            <img src="../{folder}/{f}" alt="{date.strftime("%Y-%m-%d")}">')
