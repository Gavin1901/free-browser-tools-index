import urllib.request, json, asyncio, websockets, time

PIN_LINK = "https://invoicepad.net"
PIN_TITLE = "InvoicePad: Free Invoice Generator with Profession Templates"
PIN_DESC = "Free invoice generator for web developers, handyman, freelance writers, SEO consultants. No sign-up, no watermark, instant PDF download."

async def pin():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Step 1: Fill the link field - this often triggers OG image fetch
        js_link = f'''
(function() {{
    let linkTA = document.querySelector('textarea[id*="link"]');
    if (!linkTA) linkTA = document.querySelector('textarea[placeholder*="link" i]');
    if (!linkTA) {{
        let tas = document.querySelectorAll('textarea');
        linkTA = tas[tas.length - 1]; // last textarea is usually the link
    }}
    if (!linkTA) return "NO_LINK_TA";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(linkTA, {json.dumps(PIN_LINK)});
    linkTA.dispatchEvent(new Event("input", {{bubbles: true}}));
    linkTA.dispatchEvent(new Event("change", {{bubbles: true}}));
    linkTA.dispatchEvent(new Event("blur", {{bubbles: true}}));
    return "FILLED_LINK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_link}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Link: {resp[:150]}")
        await asyncio.sleep(5)  # Wait for OG image fetch
        
        # Step 2: Fill title
        js_title = f'''
(function() {{
    let ta = document.querySelector('textarea[id*="title"]');
    if (!ta) ta = document.querySelectorAll('textarea')[0];
    if (!ta) return "NO_TITLE_TA";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(ta, {json.dumps(PIN_TITLE)});
    ta.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "FILLED_TITLE";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        print("Title filled")
        
        # Step 3: Fill description (contenteditable div)
        js_desc = f'''
(function() {{
    let ed = document.querySelector('[contenteditable="true"]');
    if (!ed) return "NO_EDITOR";
    ed.focus();
    ed.innerText = {json.dumps(PIN_DESC)};
    ed.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "FILLED_DESC";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_desc}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        print("Desc filled")
        await asyncio.sleep(2)
        
        # Step 4: Check for Save/Publish button
        js_check = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let save = btns.find(b => {
        let t = b.textContent.toLowerCase();
        return (t.includes('save') || t.includes('publish') || t.includes('create')) && b.offsetParent !== null && !b.disabled;
    });
    if (save) {
        save.click();
        return "CLICKED:" + save.textContent.trim().substring(0, 20);
    }
    return "NO_SAVE_BTN:" + btns.filter(b=>b.offsetParent!==null).map(b=>b.textContent.trim()).filter(t=>t).join(",");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_check}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Save btn: {resp[:200]}")
        await asyncio.sleep(5)
        
        js_final = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_final}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"Final URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(pin())
