import urllib.request, json, asyncio, websockets

TITLE = "0 Clicks on 1,180 Impressions: What InvoicePad Taught Me About Search Intent"
CONTENT = """After running Google Search Console for InvoicePad (https://invoicepad.net), I discovered something uncomfortable: 1,180 impressions, zero clicks.

The site works. The invoice generator is free, fast, and produces clean PDFs. But here is what people are actually searching for:

- **"web development invoice"** — 88 impressions
- **"handyman invoice template"** — 33 impressions  
- **"makeup artist invoice template"** — 27 impressions
- **"SEO service invoice template"** — 26 impressions
- **"freelance writer invoice template"** — 24 impressions

## The Real Problem

Someone searching "handyman invoice template" does not want a generic form with empty fields. They want to see a handyman-specific invoice — with labor hours, materials line items, and service descriptions pre-filled.

The tool is correct. The positioning is wrong.

## What InvoicePad Does

- Free, no sign-up
- No watermark on PDFs
- Instant download
- Multiple profession templates
- Clean, professional output

## The Fix

Dedicated landing pages per profession template. Each page will show a preview with industry-standard line items and terminology. Same free tool, better entry point for search intent.

## Try It

Visit [InvoicePad](https://invoicepad.net) — pick a template, fill your details, download a PDF invoice in under a minute.

---

*This is part of my AI tool出海 project — running 8 English tool sites and learning SEO from real GSC data.*"""

async def fill():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    if not ws_url:
        print("ERROR: Dev.to page not found")
        return
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Fill title
        js_title = f'''
(function() {{
    let titleEl = document.querySelector('input[aria-label*="Title"], input[placeholder*="Title"], #article_published_at + input, input.crayons-textfield, form input[type="text"]');
    if (!titleEl) {{
        let inputs = document.querySelectorAll('input');
        for (let i of inputs) {{
            if (i.offsetParent !== null && (i.type === "text" || !i.type)) {{
                titleEl = i;
                break;
            }}
        }}
    }}
    if (!titleEl) return "NO_TITLE_INPUT";
    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    nativeSetter.call(titleEl, {json.dumps(TITLE)});
    titleEl.dispatchEvent(new Event("input", {{bubbles: true}}));
    titleEl.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "TITLE_FILLED: " + titleEl.value.substring(0, 40);
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:300]}")
        
        # Fill content
        content_html = CONTENT.replace("\n", "\\n").replace('"', '\\"')
        js_content = f'''
(function() {{
    let el = document.querySelector('[contenteditable="true"]');
    if (!el) {{
        let textareas = document.querySelectorAll('textarea');
        el = textareas.length > 0 ? textareas[0] : null;
    }}
    if (!el) return "NO_EDITOR_FOUND";
    if (el.contentEditable === "true") {{
        el.focus();
        document.execCommand("selectAll", false, null);
        document.execCommand("insertText", false, {json.dumps(CONTENT)});
    }} else {{
        el.value = {json.dumps(CONTENT)};
        el.dispatchEvent(new Event("input", {{bubbles: true}}));
    }}
    return "CONTENT_FILLED";
}})()
'''
        msg = json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression":js_content}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:300]}")
        
        print("DONE - please check browser and click Publish")

asyncio.run(fill())
