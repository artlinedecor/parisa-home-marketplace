import urllib.request
import re

req = urllib.request.Request(
    'https://t.me/s/parisa_home_esteri',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

# Search for posts by finding message wraps
posts = re.findall(r'<div class="tgme_widget_message_wrap.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
print(f"Total post blocks: {len(posts)}")

results = []
for p in posts:
    # check text inside js-message_text
    m_text = re.search(r'class="tgme_widget_message_text[^"]*">(.*?)</div>', p, re.DOTALL)
    m_img = re.search(r'background-image:url\(["\']?(https://cdn\d*\.telesco\.pe/[^"\')]+)["\']?\)', p)
    
    text = ""
    if m_text:
        text = re.sub(r'<br\s*/?>', '\n', m_text.group(1))
        text = re.sub(r'<[^>]+>', '', text).strip()
    
    img = m_img.group(1) if m_img else ""
    if text or img:
        results.append({"text": text, "image": img})

print(f"Extracted {len(results)} valid posts")
with open("channel_posts.txt", "w", encoding="utf-8") as f:
    for r in results:
        f.write(f"IMAGE: {r['image']}\nTEXT:\n{r['text']}\n" + "-"*50 + "\n\n")

print("Saved to channel_posts.txt")
