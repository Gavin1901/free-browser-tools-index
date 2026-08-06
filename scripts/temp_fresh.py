import urllib.request, json, asyncio, websockets, time

SHORT_TITLE = "What InvoicePad Taught Me About SEO"
SHORT_CONTENT = """After running Google Search Console for [InvoicePad](https://invoicepad.net), I discovered 1,180 impressions but zero clicks.

The real problem: people search for specific templates like "web development invoice" or "handyman invoice template" but the landing page is a generic form.

The tool works. The positioning does not.

[Try InvoicePad](https://invoicepad.net) — free, no sign-up, instant PDF download."""

async def fresh_publish():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "dev.to" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate fresh
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://dev.to/new"}}))
        await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        print("Page loaded")
        
        # Wait for editor to be ready
        js_wait = '''
(function() {
    let editor = document.querySelector('[contenteditable="true"]');
    return editor ? "READY" : "WAITING";
})()
'''
        for retry in range(5):
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_wait}})
            await ws.send(msg)
            resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
            val = resp.get("result",{}).get("result",{}).get("value","")
            print(f"Editor retry {retry}: {val}")
            if val == "READY":
                break
            await asyncio.sleep(2)
        
        # Fill title
        js_title = f'''
(function() {{
    let input = document.querySelector('input[aria-label*="Title"]');
    if (!input) input = document.querySelector('input[placeholder*="title" i]');
    if (!input) {{
        let inputs = [...document.querySelectorAll("input[type='text']")];
        input = inputs.find(i => i.offsetParent !== null && !i.readOnly);
    }}
    if (!input) return "NO_TITLE";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(input, {json.dumps(SHORT_TITLE)});
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Title: {resp[:150]}")
        
        await asyncio.sleep(1)
        
        # Fill content as markdown
        js_content = f'''
(function() {{
    let el = document.querySelector('[contenteditable="true"]');
    if (!el) return "NO_EDITOR";
    el.focus();
    // Try execCommand approach
    document.execCommand("selectAll");
    document.execCommand("insertText", false, {json.dumps(SHORT_CONTENT)});
    return "OK_" + el.innerText.length;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_content}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Content: {resp[:200]}")
        
        await asyncio.sleep(2)
        
        # Add tags
        for tag in ["seo", "webdev", "freelancing"]:
            js_tag = f'''
(function() {{
    let input = document.querySelector('input[placeholder*="tag" i]');
    if (!input) return "NO_TAG";
    let ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
    ns.call(input, "{tag}");
    input.dispatchEvent(new Event("input", {{bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    input.dispatchEvent(new KeyboardEvent("keyup", {{key: "Enter", code: "Enter", keyCode: 13, bubbles: true}}));
    return "OK";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_tag}})
            await ws.send(msg)
            await asyncio.wait_for(ws.recv(), timeout=5)
            await asyncio.sleep(1)
        
        print("Tags added")
        await asyncio.sleep(3)
        
        # Click Publish
        js_pub = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let pubBtn = btns.find(b => b.textContent.trim() === 'Publish' && b.offsetParent !== null && !b.disabled);
    if (pubBtn) {
        pubBtn.scrollIntoView({block: "center"});
        pubBtn.click();
        return "CLICKED";
    }
    return "NOT_FOUND_" + btns.filter(b => b.offsetParent !== null).map(b => b.textContent.trim()).join("|").substring(0, 200);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_pub}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Publish click: {resp[:200]}")
        
        await asyncio.sleep(6)
        
        # Final check
        js_final = "JSON.stringify({url: window.location.href, errors: [...document.querySelectorAll('.crayons-notice')].filter(e => e.offsetParent).map(e => e.textContent.trim().substring(0, 200))})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Final: {resp[:600]}")

asyncio.run(fresh_publish())
