import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    if p["type"] == "page" and "pinterest" in url.lower():
        published = "pin-builder" not in url
        print(f"PINTEREST: {url[:150]} | Published: {published}")
        if published:
            print(f">>> PIN URL: {url}")
