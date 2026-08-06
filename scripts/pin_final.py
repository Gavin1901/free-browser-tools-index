import urllib.request, json, asyncio, websockets, time

PIN_LINK = "https://invoicepad.net"
PIN_TITLE = "InvoicePad: Free Invoice Generator with Profession Templates"

async def pin_save():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    if not ws_url:
        # Navigate fresh
        browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
        async with websockets.connect(browser_ws, max_size=2**24) as bws:
            await bws.send(json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://www.pinterest.com/pin-builder/"}}))
            await asyncio.wait_for(bws.recv(), timeout=10)
        await asyncio.sleep(6)
        pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
        for p in pages:
            if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
                ws_url = p["webSocketDebuggerUrl"]
                break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        await asyncio.sleep(3)
        
        # Fill link field first
        js_link = f'''
(function() {{
    let tas = document.querySelectorAll('textarea');
    let linkTA = null;
    for (let ta of tas) {{
        if (ta.id && ta.id.includes('link')) {{ linkTA = ta; break; }}
    }}
    if (!linkTA) linkTA = tas[tas.length - 1];
    if (!linkTA) return "NO_LINK_TA";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(linkTA, {json.dumps(PIN_LINK)});
    linkTA.dispatchEvent(new Event("input", {{bubbles: true}}));
    linkTA.dispatchEvent(new Event("change", {{bubbles: true}}));
    linkTA.dispatchEvent(new Event("blur", {{bubbles: true}}));
    return "LINK_FILLED";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_link}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        await asyncio.sleep(3)
        
        # Fill title
        js_title = f'''
(function() {{
    let tas = document.querySelectorAll('textarea');
    let titleTA = null;
    for (let ta of tas) {{
        if (ta.id && ta.id.includes('title')) {{ titleTA = ta; break; }}
    }}
    if (!titleTA) titleTA = tas[0];
    if (!titleTA) return "NO";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(titleTA, {json.dumps(PIN_TITLE)});
    titleTA.dispatchEvent(new Event("input", {{bubbles: true}}));
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_title}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        
        # Fill description
        js_desc = '''
(function() {
    let ed = document.querySelector('[contenteditable="true"]');
    if (ed) {
        ed.focus();
        ed.innerText = "Free invoice generator with profession-specific templates. No sign-up, no watermark, instant PDF download.";
        ed.dispatchEvent(new Event("input", {bubbles: true}));
        return "OK";
    }
    return "NO";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_desc}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        await asyncio.sleep(2)
        
        # Look for "Save from site" button or any save button
        js_save = '''
(function() {
    // Find ALL buttons with their full text
    let allBtns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
    let texts = allBtns.map(b => b.textContent.trim());
    
    // Try clicking any button that might save/publish
    for (let b of allBtns) {
        let t = b.textContent.trim();
        // Pinterest uses specific button texts
        if (t.includes('Save') || t.includes('Publish') || t.includes('Create') || t.includes('Done')) {
            b.click();
            return "CLICKED:" + t.substring(0, 40);
        }
    }
    
    // As last resort, click the rightmost/bottom button
    if (allBtns.length > 0) {
        let last = allBtns[allBtns.length - 1];
        last.click();
        return "LAST:" + last.textContent.trim().substring(0, 40);
    }
    
    return "NO_BTNS:" + texts.join(" | ");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_save}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Save: {resp[:200]}")
        await asyncio.sleep(5)
        
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")
        
        # Check for success
        js_check = "JSON.stringify({images:document.querySelectorAll('img[src*=\"invoicepad\"], [class*=\"pin\"]').length, bodySnippet:document.body.innerText.substring(0, 300)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_check}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Check: {resp[:300]}")

asyncio.run(pin_save())
