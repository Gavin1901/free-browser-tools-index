import urllib.request, json, asyncio, websockets, time

QUORA_ANSWER = "I built https://invoicepad.net — a free invoice generator with profession-specific templates (web developer, handyman, freelance writer, SEO consultant, etc). No sign-up, no watermark, instant PDF download. Takes under 60 seconds. The key insight from GSC: people search for specific templates like handyman invoice template, not generic free invoice generator. So we're building dedicated landing pages per profession."

async def quora():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to a fresh question page about invoicing
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.quora.com/What-is-the-best-free-invoicing-software-for-freelancers"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        js = "JSON.stringify({url:window.location.href, title:document.title, bodyStart:document.body.innerText.substring(0, 500)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Page: url={str(r.get('url','?'))[:100]}")
            body = str(r.get('bodyStart',''))
            if 'answer' in body.lower() or 'write' in body.lower():
                print("Can answer this question")
            print(f"Body: {body[:300]}")
        
        # Look for answer button
        js2 = '''
(function() {
    let answerBtn = [...document.querySelectorAll('button')].find(b => {
        let t = b.textContent.toLowerCase().trim();
        return (t === 'answer' || t.includes('write') || t.includes('respond')) && b.offsetParent !== null;
    });
    if (answerBtn) {
        answerBtn.click();
        return "CLICKED_ANSWER:" + answerBtn.textContent.trim();
    }
    // Try links
    let answerLink = [...document.querySelectorAll('a')].find(a => a.textContent.toLowerCase().trim() === 'answer' && a.offsetParent !== null);
    if (answerLink) {
        answerLink.click();
        return "CLICKED_LINK";
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        result = data.get("result",{}).get("result",{}).get("value","")
        print(f"Answer btn: {result}")
        
        await asyncio.sleep(4)
        
        # Check for editor
        js3 = "JSON.stringify({editors:document.querySelectorAll('[contenteditable=\"true\"], textarea').length, url:window.location.href})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"After click: editors={r.get('editors')}, url={str(r.get('url','?'))[:100]}")
            
            if r.get('editors', 0) > 0:
                # Fill and submit
                js_fill = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) ed = document.querySelector('textarea');
    if (!ed) return "NO_EDITOR";
    if (ed.contentEditable === "true") {{
        ed.focus();
        ed.innerText = {json.dumps(QUORA_ANSWER)};
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }} else {{
        let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
        ns.call(ed, {json.dumps(QUORA_ANSWER)});
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }}
    return "FILLED:" + ed.textContent.length;
}})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Fill: {resp[:150]}")
                await asyncio.sleep(2)
                
                # Submit
                js_sub = '''
(function() {
    let submit = [...document.querySelectorAll('button')].find(b => 
        (b.textContent.toLowerCase().includes('submit') || b.textContent.toLowerCase().includes('post')) &&
        b.offsetParent !== null && !b.disabled
    );
    if (submit) { submit.click(); return "CLICKED_SUBMIT"; }
    return "NO_SUBMIT";
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_sub}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                print(f"Submit: {resp[:150]}")
                await asyncio.sleep(5)
                
                js_final = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                print(f"Final URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(quora())
