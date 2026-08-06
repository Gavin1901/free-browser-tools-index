import urllib.request, json, asyncio, websockets, time

HN_TITLE = "InvoicePad: 0 Clicks on 1,180 Google Impressions"
HN_URL = "https://invoicepad.net"

async def hn():
    # Find existing HN page
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    hn_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "ycombinator.com" in url:
            hn_ws = p["webSocketDebuggerUrl"]
            print(f"Found: {url[:100]}")
            break
    
    if not hn_ws:
        print("HN not found")
        return
    
    async with websockets.connect(hn_ws, max_size=2**24) as ws:
        # Fill and submit
        js_fill = f'''
(function() {{
    document.querySelector('input[name="title"]').value = {json.dumps(HN_TITLE)};
    document.querySelector('input[name="url"]').value = {json.dumps(HN_URL)};
    let ta = document.querySelector('textarea');
    if (ta) ta.value = "GSC shows 1180 impressions but 0 clicks. Users search for specific invoice templates like web development invoice and handyman invoice template. The tool works but positioning doesn't match search intent.";
    return "FILLED";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Fill: {resp[:150]}")
        
        await asyncio.sleep(1)
        
        # Submit
        js_sub = "document.querySelector('input[type=\"submit\"]').click(); 'SUBMITTED'"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_sub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print(f"Submit: {resp[:200]}")
        
        await asyncio.sleep(8)
        
        # Check URL
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        final_url = data["result"]["result"]["value"]
        print(f"Final URL: {final_url}")
        
        # Check page title too
        js_title = "document.title"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Page title: {data['result']['result']['value']}")

asyncio.run(hn())
