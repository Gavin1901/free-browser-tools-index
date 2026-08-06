import urllib.request, json
pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    if p["type"] == "page" and "pinterest" in url.lower():
        print(f"PINTEREST: {url[:200]}")
        if "/pin/" in url:
            import re
            m = re.search(r'/pin/(\d+)', url)
            print(f">>> PIN ID: {m.group(1) if m else 'N/A'}")
