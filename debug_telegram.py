import urllib.request
import re

url = "https://t.me/s/parisa_home_esteri"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

print("Fetched HTML length:", len(html))

# Let's inspect the tags around posts
posts = re.findall(r'<div class="tgme_widget_message[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
print("Posts matching count:", len(posts))

with open("sample_html_segment.html", "w", encoding="utf-8") as f:
    f.write(html[:10000])

# Find all text inside js-message_text or any class containing message
matches = re.findall(r'<div class="([^"]*message[^"]*)">(.*?)</div>', html, re.DOTALL)
print("Message classes found:", len(matches))
for cls, content in matches[:5]:
    print("Class:", cls)
    print("Content preview:", content[:100])
    print("-" * 30)
