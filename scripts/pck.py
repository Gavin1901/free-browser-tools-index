import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    if p["type"] == "page" and "pinterest" in url.lower():
        published = "pin-builder" not in url
        pin_id = ""
        if "/pin/" in url:
            import re
            m = re.search(r'/pin/(\d+)', url)
            if m: pin_id = m.group(1)
        print(f"PINTEREST url={url[:150]} published={published} pin_id={pin_id}")
