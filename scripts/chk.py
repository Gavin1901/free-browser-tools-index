import urllib.request, json
pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    ptype = p["type"]
    url = p.get("url", "?")
    print(f"{ptype:6s} {url[:130]}")
print(f"\nTotal: {len(pages)} pages")
