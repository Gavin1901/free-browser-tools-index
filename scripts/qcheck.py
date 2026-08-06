import urllib.request, json, asyncio, websockets

async def check():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
                js = "JSON.stringify({url:window.location.href, title:document.title, bodySnippet:document.body.innerText.substring(0, 400)})"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                val = data.get("result",{}).get("result",{}).get("value","")
                if val:
                    r = json.loads(val) if isinstance(val, str) else val
                    print(f"URL: {r.get('url','?')[:80]}")
                    print(f"Title: {r.get('title','?')[:80]}")
                    body = r.get('bodySnippet','')
                    if 'log' in body.lower() and ('in' in body.lower() or 'sign' in body.lower()):
                        print("LOGIN PAGE DETECTED")
                    elif 'add question' in body.lower() or 'answer' in body.lower():
                        print("LOGGED IN - can post")
                    else:
                        print(f"Body: {body[:300]}")
            return

asyncio.run(check())
