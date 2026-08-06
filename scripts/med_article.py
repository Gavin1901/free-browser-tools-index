import urllib.request, json, asyncio, websockets, time

async def get_article():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    # Use the submission page
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/p/" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to the article page
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://medium.com/@lg695101011/f2a75b9c5458"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        js = "JSON.stringify({url:window.location.href, title:document.title, canonical:document.querySelector('link[rel=\"canonical\"]')?.href||'NONE', hasInvoicePad:document.body.innerText.includes('invoicepad'), bodyStart:document.body.innerText.substring(0, 200)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {r.get('url','?')[:150]}")
            print(f"Canonical: {r.get('canonical','?')[:150]}")
            print(f"InvoicePad: {r.get('hasInvoicePad')}")

asyncio.run(get_article())
