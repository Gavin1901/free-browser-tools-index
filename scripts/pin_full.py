import urllib.request, json, asyncio, websockets, time, base64, struct, zlib

def create_png():
    width, height = 200, 200
    def chunk(ct, data):
        c = ct + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr = chunk(b"IHDR", ihdr_data)
    raw = b""
    for y in range(height):
        raw += b"\x00"
        for x in range(width):
            raw += bytes([66, 133, 244, 255])
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return header + ihdr + idat + iend

png_data = create_png()
png_b64 = base64.b64encode(png_data).decode()

async def pin_full_flow():
    # Navigate fresh
    browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
    async with websockets.connect(browser_ws, max_size=2**24) as bws:
        await bws.send(json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://www.pinterest.com/pin-builder/"}}))
        await asyncio.wait_for(bws.recv(), timeout=10)
    await asyncio.sleep(6)
    
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        await asyncio.sleep(3)
        
        # Upload image
        js_img = f'''
(async function() {{
    let fi = document.querySelector('input[type="file"]');
    if (!fi) return "NO_FILE";
    let bs = atob("{png_b64}");
    let bytes = new Uint8Array(bs.length);
    for (let i = 0; i < bs.length; i++) bytes[i] = bs.charCodeAt(i);
    let blob = new Blob([bytes], {{type: "image/png"}});
    let file = new File([blob], "pin.png", {{type: "image/png"}});
    let dt = new DataTransfer();
    dt.items.add(file);
    fi.files = dt.files;
    fi.dispatchEvent(new Event("change", {{bubbles: true}}));
    return "OK";
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_img, "awaitPromise": True}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        print("Image uploaded")
        await asyncio.sleep(5)
        
        # Fill title
        js_t = '''
(function() {
    let tas = document.querySelectorAll('textarea');
    let t = null;
    for (let ta of tas) { if (ta.id && ta.id.includes('title')) { t = ta; break; } }
    if (!t) t = tas[0];
    if (!t) return "NO";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(t, "InvoicePad: Free Invoice Generator with Profession Templates");
    t.dispatchEvent(new Event("input", {bubbles: true}));
    return "OK";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_t}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        
        # Fill link
        js_l = '''
(function() {
    let tas = document.querySelectorAll('textarea');
    let l = null;
    for (let ta of tas) { if (ta.id && ta.id.includes('link')) { l = ta; break; } }
    if (!l) l = tas[tas.length - 1];
    if (!l) return "NO";
    let ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    ns.call(l, "https://invoicepad.net");
    l.dispatchEvent(new Event("input", {bubbles: true}));
    l.dispatchEvent(new Event("blur", {bubbles: true}));
    return "OK";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_l}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        
        # Fill description
        js_d = '''
(function() {
    let ed = document.querySelector('[contenteditable="true"]');
    if (ed) {
        ed.focus();
        ed.innerText = "Free invoice generator. No sign-up, no watermark, instant PDF download.";
        ed.dispatchEvent(new Event("input", {bubbles: true}));
        return "OK";
    }
    return "NO";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_d}})
        await ws.send(msg)
        await asyncio.wait_for(ws.recv(), timeout=10)
        print("Fields filled")
        await asyncio.sleep(3)
        
        # Now click ALL buttons systematically from right to left, bottom to top
        for attempt in range(8):
            js_click = '''
(function() {
    let all = [...document.querySelectorAll('button, [role="button"], div[tabindex="0"]')].filter(el => el.offsetParent !== null && !el.disabled);
    if (all.length === 0) return "NO_BTNS";
    // Sort by x descending (rightmost first), then y descending (bottom first)
    all.sort((a, b) => {
        let ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
        if (Math.abs(ra.x - rb.x) > 100) return rb.x - ra.x;
        return rb.y - ra.y;
    });
    let btn = all[0];
    let rect = btn.getBoundingClientRect();
    btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, clientX: rect.x+rect.width/2, clientY: rect.y+rect.height/2}));
    btn.click();
    return "CLICKED:" + (btn.textContent?.trim()?.substring(0,20) || btn.getAttribute('aria-label') || '') + "@" + Math.round(rect.x) + "," + Math.round(rect.y);
})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            result = data.get("result",{}).get("result",{}).get("value","")
            print(f"  Click {attempt}: {result}")
            await asyncio.sleep(4)
            
            js_url = "window.location.href"
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(resp)
            url = data.get("result",{}).get("result",{}).get("value","")
            
            if "pin-builder" not in url:
                print(f">>> PUBLISHED! {url}")
                return
            if "published" in url or "/pin/" in url:
                print(f">>> PUBLISHED! {url}")
                return

asyncio.run(pin_full_flow())
