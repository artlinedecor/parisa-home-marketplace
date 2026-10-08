import urllib.request
import re

url = "https://t.me/s/parisa_home_esteri"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

# Split by tgme_widget_message text
items = re.findall(r'<div class="tgme_widget_message_wrap.*?<div class="tgme_widget_message_text[^"]*">(.*?)</div>', html, re.DOTALL)
print(f"Items found: {len(items)}")

with open("real_extracted_posts.txt", "w", encoding="utf-8") as f:
    for idx, item in enumerate(items):
        clean = re.sub(r'<br\s*/?>', '\n', item)
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        f.write(f"=== POST {idx+1} ===\n{clean}\n\n")

print("Saved to real_extracted_posts.txt")
