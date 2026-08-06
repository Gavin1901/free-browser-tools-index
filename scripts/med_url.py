import urllib.request, json

pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    url = p.get("url", "")
    title = p.get("title", "?")
    if p["type"] == "page" and "medium.com" in url:
        print(f"URL: {url}")
        print(f"Title: {title}")
        # Check if this is a published article URL (not new-story)
        if "/new-story" not in url:
            print(">>> PUBLISHED! <<<")
        else:
            print("Still on new-story page")
