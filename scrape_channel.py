import urllib.request
import re
import json

req = urllib.request.Request(
    'https://t.me/s/parisa_home_esteri',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    
    # Extract images from telesco.pe
    images = re.findall(r'background-image:url\(["\']?(https://cdn\d*\.telesco\.pe/[^"\')]+)["\']?\)', html)
    print(f"Found {len(images)} images")
    with open("scraped_images.json", "w", encoding="utf-8") as f:
        json.dump(list(set(images)), f, indent=2)

    # Extract messages
    raw_texts = re.findall(r'<div class="tgme_widget_message_text[^"]*">(.*?)</div>', html, re.DOTALL)
    print(f"Found {len(raw_texts)} message texts")
    clean_texts = []
    for t in raw_texts:
        c = re.sub(r'<br\s*/?>', '\n', t)
        c = re.sub(r'<[^>]+>', '', c).strip()
        if c:
            clean_texts.append(c)
    
    with open("scraped_posts.txt", "w", encoding="utf-8") as f:
        f.write("\n\n=== POST ===\n\n".join(clean_texts))
    print("Done extraction")
except Exception as e:
    print(f"Error: {e}")
