import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "?")
    title = p.get("title", "?")[:60]
    if p["type"] == "page":
        if "quora.com" in url:
            print(f"QUORA: {url[:120]} | {title}")
        elif "medium.com" in url:
            print(f"MEDIUM: {url[:120]} | {title}")
        elif "dev.to" in url:
            print(f"DEVTO: {url[:120]} | {title}")
        elif "ycombinator" in url:
            print(f"HN: {url[:120]} | {title}")
        else:
            print(f"OTHER: {url[:100]} | {title}")
