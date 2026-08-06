import urllib.request, json, asyncio, websockets, time

async def quora_post_now():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "quora.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Find the post creation textarea/editor
        js = "JSON.stringify({editables:[...document.querySelectorAll('[contenteditable=\"true\"], textarea')].map(e=>({tag:e.tagName,placeholder:e.placeholder||'',visible:e.offsetParent!==null,text:e.textContent?.substring(0,30)||''})),url:window.location.href})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        val = data.get("result",{}).get("result",{}).get("value","")
        if val:
            r = json.loads(val) if isinstance(val, str) else val
            print(f"Editables: {r.get('editables',[])}")
        
        # Click into the post editor
        js_click = '''
(function() {
    // Find the "What do you want to talk about" area
    let editables = [...document.querySelectorAll('[contenteditable="true"], textarea')];
    let target = editables.find(e => e.offsetParent !== null);
    if (target) {
        target.focus();
        target.click();
        return "FOCUSED:" + target.tagName;
    }
    return "NO_EDITOR";
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_click}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Focus: {resp[:150]}")
        await asyncio.sleep(2)
        
        # Type content
        content = "I analyzed GSC for my free invoice generator https://invoicepad.net and found 1,180 impressions with zero clicks. People search for handyman invoice template and web development invoice, not free invoice generator. Search intent mismatch is the real bottleneck. Building dedicated landing pages now. Free tool, no sign-up, no watermark."
        
        for char in content:
            await ws.send(json.dumps({"id":1,"method":"Input.dispatchKeyEvent","params":{"type":"char","text":char,"unmodifiedText":char}}))
            await asyncio.sleep(0.01)
        print("Content typed")
        await asyncio.sleep(3)
        
        # Find Post/Submit button
        js_post = '''
(function() {
    let btns = [...document.querySelectorAll('button')];
    let post = btns.find(b => {
        let t = b.textContent.toLowerCase().trim();
        return (t === 'post' || t === 'submit' || t === 'share') && b.offsetParent !== null && !b.disabled;
    });
    if (post) { post.click(); return "CLICKED:" + post.textContent.trim().substring(0,20); }
    return "NO_POST:" + btns.filter(b=>b.offsetParent!==null&&!b.disabled).map(b=>b.textContent.trim()).filter(t=>t.length>0&&t.length<15).join(",");
})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_post}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        print(f"Post btn: {resp[:200]}")
        await asyncio.sleep(5)
        
        js_url = "window.location.href"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_url}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=10)
        data = json.loads(resp)
        print(f"URL: {data.get('result',{}).get('result',{}).get('value','?')[:150]}")

asyncio.run(quora_post_now())
