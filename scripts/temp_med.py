import urllib.request, json, asyncio, websockets, time

TITLE = "0 Clicks, 1180 Impressions: An Invoice Generator SEO Lesson"
CONTENT = """After checking Google Search Console for InvoicePad, I found something surprising: 1,180 search impressions but zero clicks.

The free invoice generator at https://invoicepad.net works perfectly. You pick a template, fill in your details, and download a clean PDF in under a minute. No sign-up, no watermark.

But here is the problem.

People are not searching for "free invoice generator." They are searching for very specific templates:

- "web development invoice" — 88 impressions
- "handyman invoice template" — 33 impressions
- "makeup artist invoice template" — 27 impressions
- "SEO service invoice template" — 26 impressions
- "freelance writer invoice template" — 24 impressions

When someone searches "handyman invoice template," they want to see a handyman-specific preview — with labor hours, materials line items, and service descriptions already filled in.

The tool is right. The landing page is wrong for that intent.

## What We Are Doing About It

We are building dedicated landing pages for each profession template. Each page will preview an industry-specific invoice before you even click "generate."

Same free tool. Better entry points for search intent.

## Try It Yourself

Visit InvoicePad at https://invoicepad.net and generate a PDF invoice in under 60 seconds.

---

This is part of my project running 8 English tool sites and learning SEO from real Google Search Console data. Follow along for real numbers and honest lessons."""

async def fill_medium():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "medium.com/new-story" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR: Medium page not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Wait for page to fully load
        await asyncio.sleep(3)
        
        # Check if logged in
        js_check = '''
(function() {
    let r = {};
    r.url = window.location.href;
    let titleEl = document.querySelector('h3[data-testid="storyTitle"], [data-testid="editorTitle"]');
    r.hasTitle = titleEl ? "YES" : "NO";
    let contentEl = document.querySelector('[data-testid="editorBody"], article section p');
    r.hasContent = contentEl ? "YES" : "NO";
    // Check all editable elements
    let editables = document.querySelectorAll('[contenteditable="true"]');
    r.editables = editables.length;
    // Check for login wall
    let paywall = document.querySelector('[data-testid="paywall"]');
    r.paywall = paywall ? "YES" : "NO";
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_check}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Page state: {resp[:400]}")
        
        # Click the title area first
        js_click_title = '''
(function() {
    let h3 = document.querySelector('h3[data-testid="storyTitle"]');
    if (h3) { h3.click(); return "CLICKED_H3"; }
    let titleDiv = document.querySelector('[data-testid="editorTitle"]');
    if (titleDiv) { titleDiv.click(); return "CLICKED_TITLE_DIV"; }
    // Try clicking in the general editor area
    let editor = document.querySelector('article, [role="textbox"]');
    if (editor) { editor.click(); return "CLICKED_EDITOR"; }
    return "NO_TITLE_AREA";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title click: {resp[:200]}")
        
        await asyncio.sleep(1)
        
        # Type title using Input.dispatchKeyEvent
        for char in TITLE:
            ke = json.dumps({
                "id":1,
                "method":"Input.dispatchKeyEvent",
                "params":{
                    "type": "char",
                    "text": char,
                    "unmodifiedText": char
                }
            })
            await ws.send(ke)
            await asyncio.sleep(0.01)
        
        print("Title typed")
        await asyncio.sleep(1)
        
        # Press Enter to move to content area
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyDown","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(0.5)
        await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"keyUp","key":"Enter","code":"Enter","keyCode":13}}))
        await asyncio.sleep(1)
        
        # Fill content using execCommand
        js_content = f'''
(function() {{
    // Try multiple approaches to fill content
    let content = {json.dumps(CONTENT)};
    
    // Approach 1: Find the content area
    let el = document.querySelector('[data-testid="editorBody"], section[data-testid="editorContent"] p, article section');
    if (el && el.contentEditable === "true") {{
        el.focus();
        document.execCommand("selectAll", false, null);
        document.execCommand("insertText", false, content);
        return "APPROACH1:" + el.innerText.length;
    }}
    
    // Approach 2: Any contenteditable
    let editables = document.querySelectorAll('[contenteditable="true"]');
    for (let e of editables) {{
        if (e.offsetParent !== null && !e.innerText.includes("Title")) {{
            e.focus();
            document.execCommand("selectAll", false, null);
            document.execCommand("insertText", false, content);
            return "APPROACH2:" + e.innerText.length;
        }}
    }}
    
    // Approach 3: Type into the focused element
    // Already handled by CDP key events above
    
    return "NO_EDITOR_FOUND";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_content}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content fill: {resp[:300]}")
        
        await asyncio.sleep(2)
        
        # Check if content is visible
        js_verify = '''
(function() {
    let body = document.body.innerText;
    let hasInvoicePad = body.includes("invoicepad");
    let length = body.length;
    return JSON.stringify({hasInvoicePad: hasInvoicePad, bodyLength: length, firstChars: body.substring(0, 200)});
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_verify}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Verify: {resp[:500]}")
        
        print("DONE - check browser")

asyncio.run(fill_medium())
