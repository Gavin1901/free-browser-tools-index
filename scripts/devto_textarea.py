import urllib.request, json, asyncio, websockets, time

DEVTO_TITLE = "What InvoicePad Taught Me About Search Intent"
DEVTO_CONTENT = """After running Google Search Console for [InvoicePad](https://invoicepad.net), I found 1,180 impressions but zero clicks.

The free invoice generator works. You pick a template, fill in details, download a clean PDF. No sign-up, no watermark.

But here is the problem. People search for:

- "web development invoice" - 88 impressions
- "handyman invoice template" - 33 impressions
- "makeup artist invoice template" - 27 impressions
- "SEO service invoice template" - 26 impressions
- "freelance writer invoice template" - 24 impressions

When someone searches "handyman invoice template," they want to see a handyman-specific invoice with labor hours and materials pre-filled. The tool works. The landing page doesn't match search intent.

## The Fix

We are building dedicated landing pages for each profession. Same free tool, better entry points.

Try it: [InvoicePad](https://invoicepad.net) - free, instant PDF download."""

async def devto_pub():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    dev_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "dev.to" in url:
            dev_ws = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(dev_ws, max_size=2**24) as ws:
        # Fill title textarea
        js_title = f'''
(function() {{
    let ta = document.querySelector('textarea[placeholder*="title" i]');
    if (!ta) return "NO_TITLE_TA";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(ta, {json.dumps(DEVTO_TITLE)});
    ta.dispatchEvent(new Event("input", {{bubbles: true}}));
    ta.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "FILLED_TITLE:" + ta.value.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:200]}")
        
        await asyncio.sleep(1)
        
        # Fill content textarea
        js_content = f'''
(function() {{
    let ta = document.querySelector('textarea[name="body_markdown"]');
    if (!ta) ta = document.querySelector('textarea[placeholder*="content" i]');
    if (!ta) return "NO_BODY_TA";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(ta, {json.dumps(DEVTO_CONTENT)});
    ta.dispatchEvent(new Event("input", {{bubbles: true}}));
    ta.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "FILLED_BODY:" + ta.value.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_content}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:200]}")
        
        await asyncio.sleep(2)
        
        # Add tags
        for tag in ["seo", "webdev", "freelancing", "invoice"]:
            js_tag = f'''
(function() {{
    let input = document.querySelector('input[placeholder*="tag" i]');
    if (!input) return "NO_TAG";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(input, "{tag}");
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    return "TAG";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_tag}})
            await ws.send(msg)
            await asyncio.wait_for(ws.recv(), timeout=5)
            await asyncio.sleep(1)
        
        print("Tags added")
        await asyncio.sleep(3)
        
        # Publish
        js_pub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pub = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pub) { pub.click(); return "CLICKED"; }
    pub = btns.find(b => b.textContent.includes('Publish') && b.offsetParent !== null);
    if (pub) { pub.click(); return "CLICKED2"; }
    return "NO_PUB";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish click: {resp[:200]}")
        
        await asyncio.sleep(8)
        
        # Check final
        js_final = '''
(function() {
    let r = {};
    r.url = window.location.href;
    r.title = document.title;
    let notices = [...document.querySelectorAll('.crayons-notice')].filter(n => n.offsetParent).map(n => n.textContent.trim().substring(0, 200));
    r.notices = notices;
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data["result"]["result"]["value"]
        if isinstance(val, str):
            r = json.loads(val)
        else:
            r = val
        print(f"Final: url={r.get('url')}, title={r.get('title')}, notices={r.get('notices')}")

asyncio.run(devto_pub())
