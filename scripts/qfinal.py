import urllib.request, json, asyncio, websockets

async def check():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    // Check for success/toast
    r.bodyStart = document.body.innerText.substring(0, 500);
    // Check if invoicepad link is visible
    r.hasInvoicePad = document.body.innerText.includes("invoicepad.net");
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {r.get('url','?')[:120]}")
            print(f"InvoicePad visible: {r.get('hasInvoicePad')}")
            print(f"Body: {r.get('bodyStart','')[:400]}")

asyncio.run(check())
