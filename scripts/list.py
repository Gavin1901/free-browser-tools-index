import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    title = p.get("title", "?")
    if p["type"] == "page":
        print(f"{title[:60]} | {url[:120]}")
