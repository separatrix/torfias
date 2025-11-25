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

print(f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Gallery - Torfi í Japan</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .gallery-grid img {{
            width: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 6px;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .gallery-grid img:hover {{
            transform: scale(1.02);
        }}
    </style>
</head>
<body>
    <div class="site">
        <aside class="index" aria-label="Posts index">
            <ul>
                <li><h2><a href="../">Posts</a></h2></li>
            </ul>
        </aside>

        <div id="lightbox" class="lightbox">
            <button class="lightbox-nav prev" aria-label="Previous image">&lt;</button>
            <img id="lightbox-img" src="" alt="">
            <button class="lightbox-nav next" aria-label="Next image">&gt;</button>
        </div>

        <div class="gallery-grid">
        """)

# Print out <img> lines
for f, date in files_with_dates:
    print(f'            <img src="../{folder}/{f}" loading="lazy" alt="{date.strftime("%Y-%m-%d")}">')

print(f"""
        </div>
    </div>

    <script>
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        const images = Array.from(document.querySelectorAll('.gallery-grid img'));
        let currentImageIndex = 0;

        function showImage(index) {{
            currentImageIndex = index;
            lightboxImg.src = images[index].src;
            lightboxImg.alt = images[index].alt;
            lightbox.classList.add('active');
        }}

        function nextImage() {{
            currentImageIndex = (currentImageIndex + 1) % images.length;
            showImage(currentImageIndex);
        }}

        function prevImage() {{
            currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
            showImage(currentImageIndex);
        }}

        images.forEach((img, index) => {{
            img.addEventListener('click', () => {{
                currentImageIndex = index;
                showImage(index);
            }});
        }});

        lightbox.querySelector('.next').addEventListener('click', (e) => {{
            e.stopPropagation();
            nextImage();
        }});

        lightbox.querySelector('.prev').addEventListener('click', (e) => {{
            e.stopPropagation();
            prevImage();
        }});

        lightbox.addEventListener('click', () => {{
            lightbox.classList.remove('active');
        }});

        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (!lightbox.classList.contains('active')) return;
            
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
            if (e.key === 'Escape') lightbox.classList.remove('active');
        }});
    </script>
</body>
</html>""")

