import urllib.request
import re

url = "https://t.me/s/parisa_home_esteri"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

texts = re.findall(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
with open("telegram_posts_utf8.txt", "w", encoding="utf-8") as f:
    for i, t in enumerate(texts):
        clean = re.sub(r'<br\s*/?>', '\n', t)
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        f.write(f"--- POST {i+1} ---\n{clean}\n\n")

print(f"Successfully saved {len(texts)} posts to telegram_posts_utf8.txt")
