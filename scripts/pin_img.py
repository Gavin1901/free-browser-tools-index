import urllib.request, json, asyncio, websockets, base64, time

async def screenshot_and_upload():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    
    # Find any page to use for screenshot
    ws_url = None
    for p in pages:
        if p["type"] == "page":
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    # Navigate to invoicepad for screenshot
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://invoicepad.net"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(4)
        
        # Set viewport to a reasonable size
        await ws.send(json.dumps({"id":2,"method":"Emulation.setDeviceMetricsOverride","params":{"width":1200,"height":800,"deviceScaleFactor":1,"mobile":False}}))
        await asyncio.sleep(1)
        
        # Take screenshot
        await ws.send(json.dumps({"id":3,"method":"Page.captureScreenshot","params":{"format":"png"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        data = json.loads(resp)
        img_data = base64.b64decode(data["result"]["data"])
        img_path = "D:/Tools/ai-tool-index/logs/2026-08-06-invoicepad-pin-image.png"
        with open(img_path, "wb") as f:
            f.write(img_data)
        print(f"Screenshot saved: {len(img_data)} bytes to {img_path}")
    
    # Now upload to Pinterest pin builder
    pin_ws = None
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            pin_ws = p["webSocketDebuggerUrl"]
            break
    
    if pin_ws:
        async with websockets.connect(pin_ws, max_size=2**24) as ws:
            # Use DOM to set file input
            js_upload = f'''
(async function() {{
    let fileInput = document.querySelector('input[type="file"]');
    if (!fileInput) return "NO_FILE_INPUT";
    
    // Fetch the image and create a File
    let resp = await fetch("file:///{img_path.replace(chr(92), '/')}");
    let blob = await resp.blob();
    let file = new File([blob], "invoicepad.png", {{type: "image/png"}});
    
    // Set file via DataTransfer
    let dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event("change", {{bubbles: true}}));
    fileInput.dispatchEvent(new Event("input", {{bubbles: true}}));
    
    return "UPLOADED";
}})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_upload, "awaitPromise": True}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=15)
            print(f"Upload: {resp[:200]}")
            
            await asyncio.sleep(5)
            
            # Check for buttons now
            js_btns = '''
(function() {
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null);
    return JSON.stringify(btns.map(b => b.textContent.trim().substring(0, 30)));
})()
'''
            msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_btns}})
            await ws.send(msg)
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"Buttons: {resp[:400]}")

asyncio.run(screenshot_and_upload())
