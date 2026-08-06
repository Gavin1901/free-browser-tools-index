import urllib.request, json, asyncio, websockets, time

HN_TITLE = "InvoicePad: 0 Clicks on 1,180 Google Impressions"
HN_URL = "https://invoicepad.net"

async def hn_full():
    # Step 1: Create new target for HN
    create_payload = json.dumps({"url": "https://news.ycombinator.com/submit"})
    req = urllib.request.Request("http://localhost:9223/json/new?" + urllib.parse.urlencode({"url": "https://news.ycombinator.com/submit"}))
    
    # Use the CDP HTTP endpoint to create a new page
    pages_before = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    
    # Navigate existing browser page to HN using the browser WS endpoint
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        # Create new target
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://news.ycombinator.com/submit"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=15)
        data = json.loads(resp)
        target_id = data["result"]["targetId"]
        print(f"Created target: {target_id}")
    
    await asyncio.sleep(5)
    
    # Find the HN page
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    hn_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "ycombinator.com" in url:
            hn_ws = p["webSocketDebuggerUrl"]
            print(f"Found HN: {url[:100]}")
            break
    
    if not hn_ws:
        print("HN page not found")
        return
    
    # Step 2: Fill and submit HN form
    async with websockets.connect(hn_ws, max_size=2**24) as ws:
        # Wait for page to load
        await asyncio.sleep(3)
        
        # Check form
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let titleEl = document.querySelector('input[name="title"]');
    let urlEl = document.querySelector('input[name="url"]');
    r.hasTitle = titleEl ? "YES" : "NO";
    r.hasUrl = urlEl ? "YES" : "NO";
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
        print(f"Form check: {val}")
        
        r = json.loads(val)
        if r.get("needsLogin") == "YES":
            print("HN not logged in!")
            return
        
        if r.get("hasTitle") != "YES":
            print("No form fields - might be on wrong page")
            return
        
        # Fill title
        js2 = f'''
(function() {{
    document.querySelector('input[name="title"]').value = {json.dumps(HN_TITLE)};
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=5)
        
        # Fill URL
        js3 = f'''
(function() {{
    document.querySelector('input[name="url"]').value = {json.dumps(HN_URL)};
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=5)
        
        print("Form filled, submitting...")
        
        # Submit
        js4 = '''
(function() {
    document.querySelector('input[type="submit"]').click();
    return "SUBMITTED";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js4}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Submit: {resp[:200]}")
        
        await asyncio.sleep(5)
        
        # Check result
        js5 = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js5}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        url = data["result"]["result"]["value"]
        print(f"Final URL: {url}")

asyncio.run(hn_full())
