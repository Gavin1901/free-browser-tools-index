import urllib.request, json, asyncio, websockets

async def check():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    
    for p in pages:
        url = p.get("url", "")
        if p["type"] != "page":
            continue
        
        label = ""
        if "pinterest" in url.lower():
            label = "PINTEREST"
        elif "producthunt" in url.lower():
            label = "PH"
        else:
            continue
        
        async with websockets.connect(p["webSocketDebuggerUrl"], max_size=2**24) as ws:
            js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.title = document.title;
    
    // Check for login indicators
    let loginBtn = document.querySelector('a[href*="login"], button:has-text("Log in"), [data-testid="login"]');
    r.loginBtn = loginBtn ? (loginBtn.offsetParent !== null ? "VISIBLE" : "HIDDEN") : "NONE";
    
    // Check for user menu / profile
    let profileEl = document.querySelector('[data-testid="header-profile"], [aria-label*="profile"], [class*="avatar"], [class*="Avatar"]');
    r.profileEl = profileEl ? "FOUND" : "NONE";
    
    // Body snippet
    r.bodyStart = document.body.innerText.substring(0, 500);
    
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
                loggedIn = r.get('loginBtn') in ('NONE', 'HIDDEN') and r.get('profileEl') == 'FOUND'
                print(f"{label}: logged_in={loggedIn}")
                print(f"  url={str(r.get('url','?'))[:100]}")
                print(f"  loginBtn={r.get('loginBtn')}, profileEl={r.get('profileEl')}")
                print(f"  body={str(r.get('bodyStart',''))[:200]}")

asyncio.run(check())
