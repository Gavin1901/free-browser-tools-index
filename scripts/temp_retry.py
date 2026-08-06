import urllib.request, json, asyncio, websockets, time

TITLE = "What InvoicePad Taught Me About Search Intent and SEO"
CONTENT = """After running Google Search Console for InvoicePad (https://invoicepad.net), I discovered something uncomfortable: 1,180 impressions, zero clicks.

The site works. The invoice generator is free, fast, and produces clean PDFs. But here is what people are actually searching for:

- "web development invoice" — 88 impressions
- "handyman invoice template" — 33 impressions  
- "makeup artist invoice template" — 27 impressions
- "SEO service invoice template" — 26 impressions
- "freelance writer invoice template" — 24 impressions

## The Real Problem

Someone searching "handyman invoice template" does not want a generic form with empty fields. They want to see a handyman-specific invoice.

The tool is correct. The positioning is wrong.

## What InvoicePad Does

- Free, no sign-up
- No watermark on PDFs
- Instant download
- Multiple profession templates
- Clean, professional output

## Try It

Visit [InvoicePad](https://invoicepad.net) — pick a template, fill your details, download a PDF invoice in under a minute.

---

*Part of my AI tool project — running 8 English tool sites and learning SEO from real GSC data.*"""

async def do_all():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Reload page
        await ws.send(json.dumps({"id":1,"method":"Page.reload","params":{}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print("Reloaded")
        await asyncio.sleep(4)
        
        # Wait for page to be ready then fill
        # Fill title
        js = f'''
(function() {{
    let titleEl = document.querySelector('input[aria-label*="Title"], input[placeholder*="Title"]');
    if (!titleEl) {{
        let inputs = document.querySelectorAll("input[type='text']");
        for (let i of inputs) {{
            if (i.offsetParent !== null && !i.readOnly) {{
                titleEl = i;
                break;
            }}
        }}
    }}
    if (!titleEl) return "NO_TITLE";
    let ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ns.call(titleEl, {json.dumps(TITLE)});
    titleEl.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "OK_" + titleEl.value.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:200]}")
        
        # Fill content
        js2 = f'''
(function() {{
    let el = document.querySelector('[contenteditable="true"]');
    if (!el) return "NO_EDITOR";
    el.focus();
    el.innerHTML = {json.dumps(CONTENT.replace(chr(10), '<br>'))};
    el.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js2}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:200]}")
        
        # Add tags
        for tag in ["seo", "webdev", "freelancing", "invoice"]:
            js_tag = f'''
(function() {{
    let input = document.querySelector('input[placeholder*="tag"]');
    if (!input) return "NO_TAG";
    let ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ns.call(input, "{tag}");
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    return "OK";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_tag}})
            await ws.send(msg)
            await asyncio.wait_for(ws.recv(), timeout=5)
            await asyncio.sleep(1)
            print(f"Tag: {tag}")
        
        await asyncio.sleep(3)
        
        # Try publish
        js_pub = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        if (b.textContent.trim() === 'Publish' && !b.disabled && b.offsetParent !== null) {
            b.click();
            return "CLICKED";
        }
    }
    return "NOT_FOUND";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish: {resp[:200]}")
        
        await asyncio.sleep(5)
        
        # Final check
        js_final = "JSON.stringify({url: window.location.href, title: document.title})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:500]}")

asyncio.run(do_all())
