import urllib.request
import re

url = "https://t.me/s/parisa_home_esteri"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

# Find all messages
messages = re.findall(r'<div class="tgme_widget_message\s[^"]*" data-post="([^"]+)">(.*?)</div>\s*<!-- /tgme_widget_message -->', html, re.DOTALL)
print(f"Messages with data-post: {len(messages)}")

with open("raw_posts_deep.txt", "w", encoding="utf-8") as f:
    for post_id, content in messages:
        # text
        text_match = re.search(r'class="tgme_widget_message_text[^"]*">(.*?)</div>', content, re.DOTALL)
        text = ""
        if text_match:
            text = re.sub(r'<br\s*/?>', '\n', text_match.group(1))
            text = re.sub(r'<[^>]+>', '', text).strip()
        
        # image
        img_match = re.search(r'background-image:url\(["\']?(https://cdn\d*\.telesco\.pe/[^"\')]+)["\']?\)', content)
        img = img_match.group(1) if img_match else ""
        
        f.write(f"=== POST: {post_id} ===\nIMAGE: {img}\nTEXT:\n{text}\n\n")

print("Saved raw_posts_deep.txt")
