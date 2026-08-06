import urllib.request, json, asyncio, websockets, time

PH_TITLE = "InvoicePad: 0 clicks on 1,180 impressions — a search intent lesson"
PH_BODY = """I analyzed GSC data for my free invoice generator (https://invoicepad.net) and found 1,180 impressions with zero clicks.

The tool works perfectly — pick a template, fill details, download PDF. No sign-up, no watermark.

The problem: people search for specific templates like "handyman invoice template" (33 imp) and "web development invoice" (88 imp), but land on a generic generator page.

Lesson: your tool can work perfectly and still get zero traction if the landing page doesn't match search intent."""

async def ph_post():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "producthunt.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Navigate to new discussion
        await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.producthunt.com/discussions/new"}}))
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        await asyncio.sleep(5)
        
        # Check page
        js = "JSON.stringify({url:window.location.href, title:document.title, bodyStart:document.body.innerText.substring(0, 400)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Page: {str(r.get('url','?'))[:120]}")
            print(f"Title: {str(r.get('title','?'))[:60]}")
            print(f"Body: {str(r.get('bodyStart',''))[:300]}")
        
        # Look for form elements
        js2 = '''
(function() {
    let r = {};
    // Check all inputs
    r.inputs = [...document.querySelectorAll('input[type="text"], input:not([type]), textarea')].map(i => ({
        placeholder: (i.placeholder||"").substring(0, 50),
        name: i.name||"",
        visible: i.offsetParent !== null
    }));
    // Check contenteditable
    r.editables = document.querySelectorAll('[contenteditable="true"]').length;
    // Check TipTap editor
    r.tiptap = document.querySelector('.tiptap, .ProseMirror, [class*="editor"]') ? "FOUND" : "NONE";
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
            print(f"Editables: {r.get('editables')}, TipTap: {r.get('tiptap')}")

asyncio.run(ph_post())
