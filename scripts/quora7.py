import urllib.request, json, asyncio, websockets, time

QUORA_POST_TITLE = "InvoicePad: 0 Clicks on 1,180 Google Impressions — What I Learned"
QUORA_POST_BODY = """I built https://invoicepad.net, a free invoice generator with profession-specific templates for web developers, handyman services, freelance writers, and SEO consultants. No sign-up, no watermark, instant PDF download.

After checking Google Search Console, I found 1,180 impressions but zero clicks. The tool works perfectly. But people search for specific templates like "handyman invoice template" (33 impressions) and "web development invoice" (88 impressions), not "free invoice generator."

The lesson: your free tool can work perfectly and still get zero traction if your landing page doesn't match what people are actually searching for. Search intent mismatch is the real bottleneck.

We're building dedicated landing pages for each profession now. Same free tool, better entry points."""

async def quora_post():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to create a post
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.quora.com/"}}))
        await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        # Check if there's a "Create Post" or "What do you want to talk about?" area
        js = "JSON.stringify({url:window.location.href, bodyStart:document.body.innerText.substring(0, 800)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            body = str(r.get('bodyStart',''))
            # Look for the "What do you want to..." or post creation prompt
            if 'what do you want' in body.lower() or 'create post' in body.lower() or 'share your thoughts' in body.lower():
                print("Post creation area found!")
            print(f"Body: {body[:500]}")

asyncio.run(quora_post())
