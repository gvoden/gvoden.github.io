import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
import html2text

# Input and output folders
INPUT_DIR = "articles"    # folder with Medium .html files
OUTPUT_DIR = "_posts"     # Jekyll posts folder
IMAGE_DIR = "assets/images"  # local image storage

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Configure html2text
h2t = html2text.HTML2Text()
h2t.ignore_links = False   # keep links
h2t.ignore_images = False  # keep images
h2t.body_width = 0         # no line wrapping

def slugify(title):
    """Convert title to URL-friendly slug"""
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def download_image(url, slug, idx):
    """Download image to assets/images and return local path"""
    try:
        ext = os.path.splitext(url.split("?")[0])[1]
        if not ext or len(ext) > 5:
            ext = ".jpg"  # fallback
        filename = f"{slug}-{idx}{ext}"
        filepath = os.path.join(IMAGE_DIR, filename)
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            return f"/{IMAGE_DIR}/{filename}"
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
    return url  # fallback to original

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(INPUT_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

            # Extract title
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else "Untitled"

            # Extract article body
            article_tag = soup.find("article")
            if not article_tag:
                continue

            # Download images & rewrite src
            for idx, img in enumerate(article_tag.find_all("img")):
                if img.has_attr("src"):
                    local_path = download_image(img["src"], slugify(title), idx)
                    img["src"] = local_path

            body_html = str(article_tag)
            body_md = h2t.handle(body_html)

            # Try to get published date from Medium metadata
            date_tag = soup.find("meta", {"property": "article:published_time"})
            if date_tag and date_tag.get("content"):
                try:
                    timestamp = datetime.datetime.fromisoformat(
                        date_tag["content"].replace("Z", "+00:00")
                    )
                except Exception:
                    timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            else:
                timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))

            date_str = timestamp.strftime("%Y-%m-%d")

            # Extract Medium tags
            tag_elements = soup.find_all("meta", {"property": "article:tag"})
            tags = [tag["content"] for tag in tag_elements if tag.get("content")]

            # Build filename
            slug = slugify(title)
            md_filename = f"{date_str}-{slug}.md"
            md_path = os.path.join(OUTPUT_DIR, md_filename)

            # Write Markdown file with Jekyll front matter
            with open(md_path, "w", encoding="utf-8") as out:
                out.write(f"---\n")
                out.write(f"layout: post\n")
                out.write(f'title: "{title}"\n')
                out.write(f"date: {timestamp.isoformat()}\n")
                if tags:
                    out.write("categories:\n")
                    for tag in tags:
                        out.write(f"  - {tag}\n")
                out.write(f"---\n\n")
                out.write(body_md)

            print(f"✅ Converted: {filename} → {md_filename} (tags: {tags}, images downloaded)")
