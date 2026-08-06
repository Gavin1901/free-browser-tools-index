import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    ptype = p["type"]
    url = p.get("url", "?")
    title = p.get("title", "?")[:60]
    print(f"{ptype:6s} | {title:60s} | {url[:100]}")
