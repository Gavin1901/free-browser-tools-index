import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "")
    if p["type"] == "page" and "medium.com" in url:
        published = "/new-story" not in url
        print(f"Medium: {url[:150]}")
        print(f"  Published: {published}")
        if published:
            print(f"  >>> SUCCESS! Published URL: {url}")
