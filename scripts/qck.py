import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    if p["type"] == "page" and "quora.com" in url:
        print(f"QUORA: {url[:150]}")
