import urllib.request
import json
import re

url = "https://bigmodel.cn/glm-coding"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)
except Exception as e:
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(str(e))
