import urllib.request, json, asyncio, websockets, time

async def hn():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://news.ycombinator.com/submit"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print(f"Nav: {resp[:100]}")
        await asyncio.sleep(4)
        
        # Check page state
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.title = document.title;
    
    // Check if logged in
    let loginLink = document.querySelector('a[href="login"]');
    r.loggedIn = loginLink ? "NO" : "MAYBE";
    
    // Check form fields
    let titleInput = document.querySelector('input[name="title"]');
    let urlInput = document.querySelector('input[name="url"]');
    let textarea = document.querySelector('textarea');
    let submitBtn = document.querySelector('input[type="submit"]');
    
    r.formFields = {
        title: titleInput ? "FOUND" : "MISSING",
        url: urlInput ? "FOUND" : "MISSING",
        text: textarea ? "FOUND" : "MISSING",
        submit: submitBtn ? "FOUND" : "MISSING"
    };
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = json.loads(data["result"]["result"]["value"])
        print(f"State: {json.dumps(val, indent=2)}")

asyncio.run(hn())
