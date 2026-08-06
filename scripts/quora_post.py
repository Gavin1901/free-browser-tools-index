import urllib.request, json, asyncio, websockets, time

QUORA_ANSWER = """I recently analyzed Google Search Console data for InvoicePad (https://invoicepad.net), a free invoice generator. The results surprised me: 1,180 search impressions but zero clicks.

The tool itself works fine — you pick a template, fill in your details, and download a clean PDF in under a minute. No sign-up, no watermark.

The problem is search intent mismatch. People search for very specific templates like "web development invoice" (88 impressions), "handyman invoice template" (33 impressions), or "SEO service invoice template" (26 impressions). But when they land on a generic invoice generator homepage, they bounce.

The lesson: your free tool can work perfectly and still get zero traction if your landing page doesn't match what people are actually searching for.

InvoicePad is now building dedicated landing pages for each profession template. Same tool, better entry points."""

async def quora_post():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to answer a question about invoicing
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.quora.com/What-is-the-best-free-invoice-generator-for-freelancers"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        js = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        url = data.get("result",{}).get("result",{}).get("value","")
        print(f"Navigated to: {url[:120]}")
        
        # Look for answer box
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    // Find answer editor
    let editor = document.querySelector('[contenteditable="true"], [role="textbox"], textarea');
    r.editor = editor ? "FOUND_" + editor.tagName : "MISSING";
    // Find answer button
    let answerBtn = [...document.querySelectorAll('button')].find(b => b.textContent.toLowerCase().includes('answer'));
    r.answerBtn = answerBtn ? "FOUND" : "MISSING";
    // Check body for question title
    r.bodyStart = document.body.innerText.substring(0, 300);
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
            print(f"Editor: {r.get('editor')}, Answer btn: {r.get('answerBtn')}")
            print(f"Body: {r.get('bodyStart','')[:200]}")
        
        # If page redirected or not found, try creating a post instead
        if "answer" not in url.lower() and "quora.com" in url:
            # Try to find the answer form on this page
            pass

asyncio.run(quora_post())
