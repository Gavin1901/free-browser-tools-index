import urllib.request, json, asyncio, websockets, time

PH_TITLE = "0 clicks on 1,180 impressions: an invoice generator SEO lesson"
PH_BODY = """After checking GSC for my free invoice generator (https://invoicepad.net), I found 1,180 impressions but zero clicks. The tool works. But people search for specific templates like "handyman invoice template" and "web development invoice" — not "free invoice generator." The landing page doesn't match search intent. Building dedicated template pages now. Free tool, no sign-up, no watermark."""

async def ph_submit():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "producthunt.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Fill title
        js = f'''
(function() {{
    let inp = document.querySelector('input[name="title"]');
    if (!inp) inp = document.querySelector('input[placeholder*="Title"]');
    if (!inp) return "NO_TITLE";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(inp, {json.dumps(PH_TITLE)});
    inp.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        print("Title filled")
        
        # Fill content
        js2 = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) return "NO_EDITOR";
    ed.focus();
    ed.click();
    ed.innerHTML = {json.dumps(PH_BODY.replace(chr(10), '<br>'))};
    ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "OK:" + ed.textContent.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:150]}")
        await asyncio.sleep(2)
        
        # Submit
        js3 = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let submit = btns.find(b => b.textContent.trim() === 'Submit' && b.offsetParent !== null && !b.disabled);
    if (!submit) submit = btns.find(b => (b.textContent.includes('Submit') || b.textContent.includes('Post') || b.textContent.includes('Create')) && b.offsetParent !== null && !b.disabled);
    if (submit) { submit.click(); return "CLICKED:" + submit.textContent.trim(); }
    return "NO_SUBMIT";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js3}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Submit: {resp[:150]}")
        await asyncio.sleep(6)
        
        # Check
        js4 = "JSON.stringify({url:window.location.href, title:document.title, errors:[...document.querySelectorAll('[class*=\"error\"], [role=\"alert\"]')].filter(e=>e.offsetParent!==null).map(e=>e.textContent.trim())})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js4}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Final: url={str(r.get('url','?'))[:120]}, errors={r.get('errors',[])}")

asyncio.run(ph_submit())
