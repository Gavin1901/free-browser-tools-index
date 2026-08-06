import urllib.request, json, asyncio, websockets, time

HN_COMMENT = "I had a similar experience with my invoice generator (https://invoicepad.net). 1,180 Google impressions, zero clicks. The tool works fine but the landing page doesn't match what people search for (specific templates like handyman invoice, not generic invoice generator). Search intent mismatch kills CTR even with decent impressions."

async def hn_comment():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "ycombinator.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    if not ws_url:
        # Create new HN page
        browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
        async with websockets.connect(browser_ws, max_size=2**24) as bws:
            await bws.send(json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://news.ycombinator.com/"}}))
            await asyncio.wait_for(bws.recv(), timeout=10)
        await asyncio.sleep(5)
        pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
        for p in pages:
            if p["type"] == "page" and "ycombinator.com" in p.get("url", ""):
                ws_url = p["webSocketDebuggerUrl"]
                break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check if we're on a usable page or still on the blocked page
        js = "JSON.stringify({url:window.location.href, title:document.title, loginLink:!!document.querySelector('a[href*=\"login\"]'), bodyStart:document.body.innerText.substring(0, 400)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {str(r.get('url','?'))[:120]}")
            print(f"Login needed: {r.get('loginLink')}")
        
        # Search for invoicing/freelancing posts
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://news.ycombinator.com/item?id=49031869"}}))
        await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(4)
        
        js2 = "JSON.stringify({url:window.location.href, title:document.title, textarea:!!document.querySelector('textarea'), bodyStart:document.body.innerText.substring(0, 300)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Post: {str(r.get('url','?'))[:120]}")
            print(f"Textarea: {r.get('textarea')}")
            
            if r.get('textarea'):
                # Fill and submit comment
                js_fill = f'''
(function() {{
    let ta = document.querySelector('textarea');
    if (!ta) return "NO_TA";
    ta.value = {json.dumps(HN_COMMENT)};
    ta.dispatchEvent(new Event("input", {{bubbles: true}}));
    let submit = document.querySelector('input[type="submit"]');
    if (submit) {{ submit.click(); return "SUBMITTED"; }}
    return "NO_SUBMIT";
}})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Comment: {resp[:200]}")
                await asyncio.sleep(5)
                
                js_url = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                print(f"Final URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(hn_comment())
