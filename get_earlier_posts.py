import urllib.request
import re
import json

base_url = "https://t.me/s/parisa_home_esteri?before=1090"
req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

texts = re.findall(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
print(f"Earlier posts found: {len(texts)}")

with open("earlier_posts_utf8.txt", "w", encoding="utf-8") as f:
    for i, t in enumerate(texts):
        clean = re.sub(r'<br\s*/?>', '\n', t)
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        f.write(f"--- EARLIER POST {i+1} ---\n{clean}\n\n")

print("Saved to earlier_posts_utf8.txt")
