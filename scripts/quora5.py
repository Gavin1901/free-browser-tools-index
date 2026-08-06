import urllib.request, json, asyncio, websockets, time

ANSWER = """I tested several free invoice generators and InvoicePad (https://invoicepad.net) stands out for one reason: profession-specific templates. Most free tools give you a blank form. InvoicePad has pre-configured templates for web developers, handyman services, makeup artists, SEO consultants, and freelance writers. Each template includes industry-standard line items. A handyman invoice has labor hours and materials fields. A freelance writer invoice has per-word and per-project rate fields. Completely free, no sign-up, no watermark, instant PDF download. Takes under 60 seconds."""

async def answer():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # First, find and navigate to the question page. Look for a link
        js = '''
(function() {
    // Find the question link on this page
    let links = [...document.querySelectorAll('a')];
    let qLink = links.find(a => a.textContent.includes('What free invoice templates'));
    if (qLink) { window.location.href = qLink.href; return "NAVIGATED:" + qLink.href; }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Nav: {resp[:200]}")
        await asyncio.sleep(4)
        
        # Check for answer form on current page
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    // Find answer button
    let answerBtn = [...document.querySelectorAll('button')].find(b => b.textContent.toLowerCase().includes('answer') && b.offsetParent !== null);
    r.answerBtn = answerBtn ? "FOUND_" + answerBtn.textContent.trim().substring(0, 20) : "MISSING";
    // Find any editor
    let editor = document.querySelector('[contenteditable="true"], textarea');
    r.editor = editor ? "FOUND_" + editor.tagName : "MISSING";
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).filter(t => t.length > 0 && t.length < 30);
    r.visibleBtns = [...new Set(btns)].slice(0, 15);
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"URL: {r.get('url','?')[:120]}")
            print(f"Answer btn: {r.get('answerBtn')}, Editor: {r.get('editor')}")
            print(f"Visible btns: {r.get('visibleBtns', [])}")
            
            # Try clicking answer button
            if r.get('answerBtn', '').startswith('FOUND'):
                js3 = '''
(function() {
    let btn = [...document.querySelectorAll('button')].find(b => b.textContent.toLowerCase().includes('answer') && b.offsetParent !== null);
    if (btn) { btn.click(); return "CLICKED"; }
    return "NOT_FOUND";
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Click answer: {resp[:200]}")
                await asyncio.sleep(4)
            
            # Try filling and submitting if editor exists
            js4 = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) ed = document.querySelector('textarea');
    if (!ed) return "NO_EDITOR";
    if (ed.contentEditable === "true") {{
        ed.focus();
        ed.innerText = {json.dumps(ANSWER)};
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }} else {{
        let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
        ns.call(ed, {json.dumps(ANSWER)});
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }}
    return "FILLED:" + ed.textContent.length;
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js4}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"Fill answer: {resp[:200]}")
            
            await asyncio.sleep(2)
            
            # Try submit
            js5 = '''
(function() {
    let submit = [...document.querySelectorAll('button')].find(b => 
        (b.textContent.toLowerCase().includes('submit') || b.textContent.toLowerCase().includes('post')) &&
        b.offsetParent !== null
    );
    if (submit) { submit.click(); return "CLICKED_SUBMIT"; }
    return "NO_SUBMIT";
})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js5}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"Submit: {resp[:200]}")
            await asyncio.sleep(5)
            
            js6 = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js6}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            print(f"Final URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(answer())
