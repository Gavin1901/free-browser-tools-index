"""Publish Dev.to article via CDP - invoicepad"""
import json, time, asyncio, websockets, sys, urllib.request

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

*This is part of my AI工具出海 project — running 8 English tool sites and learning SEO from real GSC data.*"""

async def get_devto_ws():
    resp = urllib.request.urlopen("http://localhost:9223/json")
    pages = json.loads(resp.read())
    for p in pages:
        if p.get('type') == 'page' and 'dev.to' in p.get('url', ''):
            return p['webSocketDebuggerUrl']
    return None

async def main():
    ws_url = await get_devto_ws()
    if not ws_url:
        # Navigate to dev.to/new
        import subprocess
        subprocess.run([
            'python', '-c', f'''
import urllib.request, json
pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
for p in pages:
    if p["type"] == "page":
        ws = p["webSocketDebuggerUrl"]
        break
import websockets, asyncio
async def nav():
    async with websockets.connect(ws, max_size=2**24) as w:
        await w.send(json.dumps({{"id":1,"method":"Page.navigate","params":{{"url":"https://dev.to/new"}}}}))
        await asyncio.sleep(5)
asyncio.run(nav())
'''
        ], timeout=15)
        await asyncio.sleep(3)
        ws_url = await get_devto_ws()
    
    if not ws_url:
        print("ERROR: Dev.to page not found after navigation")
        return
    
    print(f"Connected to Dev.to: {ws_url[:60]}...")
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Get title element
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":"document.querySelector('input[placeholder*=\"title\"], input[name*=\"title\"], [aria-label*=\"title\"], #article-form-title') || document.querySelector('h1 + input, h1 + textarea, h1 + div[contenteditable]')"}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title element response: {resp[:200]}")
        
        # Fill title via JS
        js = f"document.querySelector('input[placeholder*=\"title\"], input[name*=\"title\"], [aria-label*=\"title\"], #article-form-title, h1 + input, h1 + textarea, h1 + div[contenteditable]').value = {json.dumps(TITLE)}; document.querySelector('input[placeholder*=\"title\"], input[name*=\"title\"], [aria-label*=\"title\"], #article-form-title, h1 + input, h1 + textarea, h1 + div[contenteditable]').dispatchEvent(new Event('input', {{bubbles: true}}))"
        msg = json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title fill: {resp[:200]}")
        
        # Fill content via JS
        content_js = f'''
(function() {{
    let el = document.querySelector('[contenteditable="true"], .crayons-editor, #article_body_markdown, textarea[name*="body"], textarea[id*="body"]');
    if (!el) {{
        let editors = document.querySelectorAll('[contenteditable]');
        el = editors.length > 0 ? editors[editors.length-1] : null;
    }}
    if (!el) return "NO_EDITOR";
    if (el.contentEditable === "true") {{
        el.innerHTML = {json.dumps(CONTENT.replace(chr(10), '<br>'))};
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
    }} else {{
        el.value = {json.dumps(CONTENT)};
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
    }}
    return "FILLED";
}})()
'''
        msg = json.dumps({"id":3,"method":"Runtime.evaluate","params":{"expression":content_js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content fill: {resp[:200]}")
        
        # Check for publish button
        pub_js = '''
(function() {
    let btns = document.querySelectorAll('button');
    for (let b of btns) {
        if (b.textContent.toLowerCase().includes('publish')) return b.textContent + '|' + (b.disabled ? 'DISABLED' : 'ENABLED');
    }
    return "NO_PUBLISH_BUTTON";
})()
'''
        msg = json.dumps({"id":4,"method":"Runtime.evaluate","params":{"expression":pub_js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish button: {resp[:300]}")
        
        print("DONE - check browser")

asyncio.run(main())
