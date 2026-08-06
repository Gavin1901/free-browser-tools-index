import urllib.request, json, asyncio, websockets, time

PIN_TITLE = "InvoicePad: Free Invoice Generator for Freelancers"
PIN_DESC = "Free invoice generator with profession-specific templates for web developers, handyman services, freelance writers, and more. No sign-up, no watermark, instant PDF download. https://invoicepad.net"
PIN_LINK = "https://invoicepad.net"

async def create_pin():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate directly to pin builder
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.pinterest.com/pin-builder/"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        js = "JSON.stringify({url:window.location.href, title:document.title})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Pin builder: {str(r.get('url','?'))[:120]}")
        
        # Check for pin creation form elements
        js2 = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // Look for all inputs
    let inputs = [...document.querySelectorAll('input, textarea, [contenteditable="true"]')];
    r.inputs = inputs.filter(i => i.offsetParent !== null).map(i => ({
        tag: i.tagName,
        type: i.type || "editable",
        placeholder: (i.placeholder||"").substring(0, 30),
        id: (i.id||"").substring(0, 30),
        name: (i.name||"").substring(0, 30)
    }));
    
    // Look for file upload
    let fileInput = document.querySelector('input[type="file"]');
    r.fileInput = fileInput ? "FOUND" : "NONE";
    
    // Look for any visible buttons
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => b.textContent.trim().substring(0, 30));
    r.buttons = [...new Set(btns)].filter(t => t.length > 0 && t.length < 25);
    
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
            print(f"Inputs: {r.get('inputs',[])}")
            print(f"File input: {r.get('fileInput')}")
            print(f"Buttons: {r.get('buttons',[])}")

asyncio.run(create_pin())
