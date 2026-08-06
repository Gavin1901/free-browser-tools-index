import urllib.request, json, asyncio, websockets

async def verify():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "ycombinator.com/item" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = "JSON.stringify({hasInvoicePad:document.body.innerText.includes('invoicepad'), snippet:document.body.innerText.substring(document.body.innerText.indexOf('invoicepad')-30, document.body.innerText.indexOf('invoicepad')+100)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            has = r.get('hasInvoicePad', False)
            print(f"HN comment visible: {has}")
            if has:
                print(f"  Context: {r.get('snippet','?')}")

asyncio.run(verify())
