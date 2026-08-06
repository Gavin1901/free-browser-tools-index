import urllib.request, json, asyncio, websockets, time

QUORA_ANSWER = "I built https://invoicepad.net — a free invoice generator with profession-specific templates (web developer, handyman, freelance writer, SEO consultant). No sign-up, no watermark, instant PDF download. Takes 60 seconds. The GSC insight: people search for specific templates like handyman invoice template, not generic free invoice generator."

async def answer():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Click on "Answer" in the page
        js = '''
(function() {
    // Find any clickable "Answer" element
    let all = [...document.querySelectorAll('a, button, span, div')];
    let answerEls = all.filter(el => {
        let t = el.textContent.trim();
        return t === 'Answer' && el.offsetParent !== null;
    });
    // Sort by position (click the one closest to top, usually the main nav)
    if (answerEls.length > 0) {
        answerEls[0].click();
        return "CLICKED:" + answerEls.length + "_EL_" + answerEls[0].tagName;
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        result = data.get("result",{}).get("result",{}).get("value","")
        print(f"Click answer: {result}")
        
        await asyncio.sleep(5)
        
        # Check for editor
        js2 = "JSON.stringify({editors:document.querySelectorAll('[contenteditable=\"true\"], textarea').length, url:window.location.href, bodyStart:document.body.innerText.substring(0, 400)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Editors: {r.get('editors')}")
            print(f"URL: {str(r.get('url','?'))[:100]}")
            
            if r.get('editors', 0) > 0:
                # Fill answer
                js_fill = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) ed = document.querySelector('textarea');
    if (!ed) return "NO";
    if (ed.contentEditable === "true") {{
        ed.focus();
        ed.innerText = {json.dumps(QUORA_ANSWER)};
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }} else {{
        let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
        ns.call(ed, {json.dumps(QUORA_ANSWER)});
        ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    }}
    return "FILLED";
}})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_fill}})
                await ws.send(msg)
                await asyncio.wait_for(ws.recv(), timeout=10)
                await asyncio.sleep(2)
                
                # Find and click Post/Submit
                js_post = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let post = btns.find(b => {
        let t = b.textContent.toLowerCase().trim();
        return (t === 'post' || t === 'submit') && b.offsetParent !== null && !b.disabled;
    });
    if (post) { post.click(); return "CLICKED_POST"; }
    return "NO_POST:" + btns.filter(b=>b.offsetParent!==null).map(b=>b.textContent.trim()).filter(t=>t.length>0&&t.length<20).join(",");
})()
'''
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_post}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                print(f"Post: {data.get('result',{}).get('result',{}).get('value','?')}")
                await asyncio.sleep(5)
                
                js_final = "window.location.href"
                msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
                await ws.send(msg)
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(resp)
                print(f"Final: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")
            else:
                print(f"Body: {str(r.get('bodyStart',''))[:300]}")

asyncio.run(answer())
