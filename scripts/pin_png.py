import urllib.request, json, asyncio, websockets, base64, time, struct, zlib

# Create a minimal 200x200 red PNG
def create_png():
    width, height = 200, 200
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc
    
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr = chunk(b"IHDR", ihdr_data)
    
    raw = b""
    for y in range(height):
        raw += b"\x00"  # filter none
        for x in range(width):
            raw += bytes([66, 133, 244, 255])  # Blue-ish color
    
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    
    return header + ihdr + idat + iend

png_data = create_png()
png_b64 = base64.b64encode(png_data).decode()
print(f"PNG created: {len(png_data)} bytes")

async def upload():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "pinterest" in p.get("url", "").lower():
            ws_url = p["webSocketDebuggerUrl"]
            break
    
    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Upload PNG via fetch + File
        js_upload = f'''
(async function() {{
    let fileInput = document.querySelector('input[type="file"]');
    if (!fileInput) return "NO_FILE_INPUT";
    
    let binaryStr = atob("{png_b64}");
    let bytes = new Uint8Array(binaryStr.length);
    for (let i = 0; i < binaryStr.length; i++) {{
        bytes[i] = binaryStr.charCodeAt(i);
    }}
    let blob = new Blob([bytes], {{type: "image/png"}});
    let file = new File([blob], "invoicepad-pin.png", {{type: "image/png"}});
    
    let dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event("change", {{bubbles: true}}));
    
    return "UPLOADED:" + file.size;
}})()
'''
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js_upload, "awaitPromise": True}})
        await ws.send(msg)
        resp = await asyncio.wait_for(ws.recv(), timeout=15)
        print(f"Upload: {resp[:200]}")
        await asyncio.sleep(5)
        
        # Check for Save/Publish button
        js_save = '''
(function() {
    let btns = [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null && !b.disabled);
    let texts = btns.map(b => b.textContent.trim()).filter(t => t.length > 0 && t.length < 20);
    // Try clicking Publish/Save
    for (let b of btns) {
        let t = b.textContent.trim();
        if (t.includes('Publish') || t.includes('Save') || t === 'Done') {
            b.click();
            return "CLICKED:" + t;
        }
    }
    return "BTNS:" + [...new Set(texts)].join("|");
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

asyncio.run(upload())
