import urllib.request
import re

url = "https://t.me/s/parisa_home_esteri"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

# Search for any text within message bubbles or js-message_text
texts = re.findall(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
print("Found texts count:", len(texts))
for i, t in enumerate(texts):
    clean = re.sub(r'<br\s*/?>', '\n', t)
    clean = re.sub(r'<[^>]+>', '', clean).strip()
    print(f"[{i}] {clean}\n" + "="*40)

# Check if there are captions for photos
captions = re.findall(r'<div class="tgme_widget_message_photo_wrap.*?<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
print("Captions count:", len(captions))
