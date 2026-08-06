import urllib.request, json, asyncio, websockets, time

async def check():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    dev_ws = None
    for p in pages:
        url = p.get("url", "")
        if p["type"] == "page" and "dev.to" in url:
            dev_ws = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(dev_ws, max_size=2**24) as ws:
        # Comprehensive page scan
        js = '''
(function() {
    let r = {};
    r.url = window.location.href;
    
    // All text inputs
    r.textInputs = [...document.querySelectorAll('input[type="text"], input:not([type])')].map(i => ({
        placeholder: i.placeholder || "",
        name: i.name || "",
        aria: i.getAttribute("aria-label") || "",
        visible: i.offsetParent !== null
    }));
    
    // All textareas
    r.textareas = [...document.querySelectorAll('textarea')].map(t => ({
        placeholder: t.placeholder || "",
        name: t.name || "",
        visible: t.offsetParent !== null
    }));
    
    // All contenteditables
    r.editables = [...document.querySelectorAll('[contenteditable="true"], [role="textbox"]')].map(e => ({
        tag: e.tagName,
        role: e.getAttribute("role"),
        visible: e.offsetParent !== null,
        text: e.textContent?.trim().substring(0, 30) || ""
    }));
    
    // Look for the markdown editor area
    let bodyField = document.querySelector('#article_body_markdown, textarea[name*="body"], [data-testid="editor"]');
    r.bodyField = bodyField ? "FOUND_" + bodyField.tagName : "MISSING";
    
    // Check for Crayons editor (Dev.to's editor)
    let crayonsEditor = document.querySelector('.crayons-editor, [class*="editor"]');
    r.crayonsEditor = crayonsEditor ? "FOUND" : "MISSING";
    
    // Any element with markdown-related class
    let mdElements = document.querySelectorAll('[class*="markdown"], [class*="Markdown"], [class*="editor"], [class*="Editor"]');
    r.mdElements = [...mdElements].filter(e => e.offsetParent !== null).map(e => e.tagName + "." + (e.className?.toString() || "").substring(0, 40)).slice(0, 5);
    
    // Body HTML snippet
    r.bodySnippet = document.body.innerHTML.substring(2000, 2800);
    
    return JSON.stringify(r);
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        data = json.loads(resp)
        val = data["result"]["result"]["value"]
        if isinstance(val, str):
            r = json.loads(val)
        else:
            r = val
        print(f"Text inputs: {json.dumps(r.get('textInputs','?'), indent=2)[:500]}")
        print(f"Textareas: {r.get('textareas','?')}")
        print(f"Editables: {r.get('editables','?')}")
        print(f"Body field: {r.get('bodyField','?')}")
        print(f"Crayons editor: {r.get('crayonsEditor','?')}")
        print(f"MD elements: {r.get('mdElements','?')}")
        print(f"Body snippet: {r.get('bodySnippet','?')[:300]}")

asyncio.run(check())
