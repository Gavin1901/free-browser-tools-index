import urllib.request, json, asyncio, websockets, time

HN_TITLE = "InvoicePad: 0 Clicks on 1,180 Google Impressions — A Search Intent Case Study"
HN_URL = "https://invoicepad.net"

async def hn_submit():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "ycombinator.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("HN page not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check form state
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let titleEl = document.querySelector('input[name="title"]');
    let urlEl = document.querySelector('input[name="url"]');
    let textEl = document.querySelector('textarea');
    r.titleExists = titleEl ? "YES" : "NO";
    r.urlExists = urlEl ? "YES" : "NO";
    r.textExists = textEl ? "YES" : "NO";
    
    // Check for login wall
    let loginLink = document.querySelector('a[href*="login"]');
    r.needsLogin = loginLink ? "YES" : "NO";
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"Form: {json.dumps(val)}")
        
        if val.get("needsLogin") == "YES":
            print("HN requires login! Attempting login page...")
            await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://news.ycombinator.com/login"}}))
            await asyncio.sleep(5)
            return
        
        if val.get("titleExists") != "YES":
            print("No title field — probably not logged in")
            return
        
        # Fill title
        js_fill_title = f'''
(function() {{
    let el = document.querySelector('input[name="title"]');
    if (!el) return "NO_TITLE";
    el.value = {json.dumps(HN_TITLE)};
    el.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "FILLED";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:150]}")
        
        # Fill URL
        js_fill_url = f'''
(function() {{
    let el = document.querySelector('input[name="url"]');
    if (!el) return "NO_URL";
    el.value = {json.dumps(HN_URL)};
    el.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "FILLED";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"URL: {resp[:150]}")
        
        # Fill text if exists
        HN_TEXT = "GSC data shows 1,180 impressions with zero clicks. People search for 'web development invoice' and 'handyman invoice template' — not 'free invoice generator'. The tool works. The landing page doesn't match search intent."
        js_fill_text = f'''
(function() {{
    let el = document.querySelector('textarea');
    if (!el) return "NO_TEXT";
    el.value = {json.dumps(HN_TEXT)};
    el.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "FILLED";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill_text}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Text: {resp[:150]}")
        
        await asyncio.sleep(2)
        
        # Click submit
        js_submit = '''
(function() {
    let submit = document.querySelector('input[type="submit"]');
    if (submit) { submit.click(); return "CLICKED"; }
    return "NO_SUBMIT";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_submit}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Submit: {resp[:200]}")
        
        await asyncio.sleep(5)
        
        js_final = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final URL: {resp[:300]}")

asyncio.run(hn_submit())
