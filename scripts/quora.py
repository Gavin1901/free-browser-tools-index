import urllib.request, json, asyncio, websockets, time

async def quora():
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        msg = json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://www.quora.com/"}})
        await bws.send(msg)
        resp = await asyncio.wait_for(bws.recv(), timeout=15)
        print(f"Target: {json.loads(resp)['result']['targetId']}")
    
    await asyncio.sleep(8)
    
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "quora.com" in url:
            async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
                js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.title = document.title;
    // Check for login state
    let loggedIn = document.querySelector('[data-logged-in], .logged_in, .profile-link');
    let loginBtn = document.querySelector('a[href*="login"], button:has-text("Log In")');
    let addQuestion = document.querySelector('[aria-label*="Add question"], a[href*="/add"], button[aria-label*="question"]');
    r.loggedIn = !loginBtn || loginBtn.offsetParent === null ? "MAYBE" : "NO";
    r.hasAddBtn = addQuestion ? "YES" : "NO";
    let profileElements = document.querySelectorAll('[class*="profile"], [class*="Profile"], [class*="avatar"], [class*="Avatar"], [class*="user"]');
    r.profileCount = profileElements.length;
    return JSON.stringify(r);
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                val = data["result"]["result"]["value"]
                if isinstance(val, str):
                    r = json.loads(val)
                else:
                    r = val
                print(f"Quora: url={r.get('url')[:80]}, title={r.get('title','?')[:60]}")
                print(f"Logged in: {r.get('loggedIn')}, Add btn: {r.get('hasAddBtn')}")

asyncio.run(quora())
