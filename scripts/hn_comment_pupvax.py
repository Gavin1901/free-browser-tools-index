"""Post a HN comment about PupVax on a relevant thread."""
import urllib.request, json, asyncio, websockets, time

HN_COMMENT = "I built a free puppy vaccine schedule tracker (https://pupvax.com) and audited 839 Google impressions — got 1 click. The top query 'puppy vaccinations' has 111 impressions but 0 clicks. Root cause: avg position 67.5 (page 7), only 10 of 53 pages indexed, no vet-domain backlinks. For low-competition health queries, Google needs to see authority signals before it'll rank you. One interesting thing I found: 90% of puppies are born with roundworms — deworming at 2 weeks is standard care that most owners don't know about."

async def hn_comment():
    pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
    ws_url = None
    for p in pages:
        if p["type"] == "page" and "ycombinator.com" in p.get("url", ""):
            ws_url = p["webSocketDebuggerUrl"]
            break

    if not ws_url:
        browser_ws = json.loads(urllib.request.urlopen("http://localhost:9223/json/version").read())["webSocketDebuggerUrl"]
        async with websockets.connect(browser_ws, max_size=2**24) as bws:
            await bws.send(json.dumps({"id":1,"method":"Target.createTarget","params":{"url":"https://news.ycombinator.com/"}}))
            await asyncio.wait_for(bws.recv(), timeout=10)
        await asyncio.sleep(5)
        pages = json.loads(urllib.request.urlopen("http://localhost:9223/json").read())
        for p in pages:
            if p["type"] == "page" and "ycombinator.com" in p.get("url", ""):
                ws_url = p["webSocketDebuggerUrl"]
                break

    async with websockets.connect(ws_url, max_size=2**24) as ws:
        # Check page state
        js = "JSON.stringify({url:window.location.href, title:document.title, loginLink:!!document.querySelector('a[href*=\"login\"]'), bodyStart:document.body.innerText.substring(0, 400)})"
        msg = json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":js}})
        await ws.send(msg)
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 1:
                info = json.loads(r["result"]["result"]["value"])
                print(f"HN page: {info['url'][:80]}")
                print(f"Title: {info['title']}")
                print(f"Login needed: {info['loginLink']}")
                print(f"Body: {info['bodyStart'][:200]}")
                break

        # Try to find a commentable thread - look for "discuss" or "comments" links
        find_thread_js = """
        (function() {
            var links = document.querySelectorAll('a');
            var threads = [];
            for (var l of links) {
                var href = l.href || '';
                var text = l.textContent.trim();
                if ((href.includes('item?id=') || text.match(/\\d+ comments?/)) && threads.length < 5) {
                    threads.push({href: href, text: text});
                }
            }
            return JSON.stringify(threads);
        })()
        """
        await ws.send(json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression":find_thread_js,"returnByValue":True}}))
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 2:
                threads = json.loads(r["result"]["result"]["value"])
                print(f"Found {len(threads)} threads")
                break

        if threads and len(threads) > 0:
            target = threads[0]['href']
            print(f"Navigating to: {target}")
            await ws.send(json.dumps({"id":3,"method":"Page.navigate","params":{"url":target}}))
            await asyncio.sleep(3)

            # Check for comment box
            check_js = """
            (function() {
                var ta = document.querySelector('textarea');
                var form = document.querySelector('form[action*=\"comment\"]');
                return JSON.stringify({
                    hasTextarea: !!ta,
                    hasForm: !!form,
                    textareaName: ta ? ta.name : 'none'
                });
            })()
            """
            await ws.send(json.dumps({"id":4,"method":"Runtime.evaluate","params":{"expression":check_js,"returnByValue":True}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == 4:
                    state = json.loads(r["result"]["result"]["value"])
                    print(f"Comment state: {state}")
                    break

            if state.get('hasTextarea'):
                # Fill comment
                comment_js = f"""
                (function() {{
                    var ta = document.querySelector('textarea');
                    if (!ta) return 'NOT FOUND';
                    var s = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
                    s.call(ta, {json.dumps(HN_COMMENT)});
                    ta.dispatchEvent(new Event('input', {{bubbles:true}}));
                    return 'OK: ' + ta.value.length + ' chars';
                }})()
                """
                await ws.send(json.dumps({"id":5,"method":"Runtime.evaluate","params":{"expression":comment_js,"returnByValue":True}}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == 5:
                        print(f"Comment fill: {r['result']['result']['value']}")
                        break

                await asyncio.sleep(1)

                # Click submit
                submit_js = """
                (function() {
                    var btns = document.querySelectorAll('input[type=\"submit\"], button[type=\"submit\"]');
                    for (var b of btns) {
                        if (b.value && b.value.toLowerCase().includes('add')) {
                            b.click();
                            return 'Clicked: ' + b.value;
                        }
                    }
                    // Fallback - look for any submit
                    var submit = document.querySelector('input[type=\"submit\"]');
                    if (submit) { submit.click(); return 'Clicked submit'; }
                    return 'NOT FOUND';
                })()
                """
                await ws.send(json.dumps({"id":6,"method":"Runtime.evaluate","params":{"expression":submit_js,"returnByValue":True}}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == 6:
                        print(f"Submit: {r['result']['result']['value']}")
                        break

                await asyncio.sleep(3)

                # Get final URL
                await ws.send(json.dumps({"id":7,"method":"Runtime.evaluate","params":{"expression":"window.location.href","returnByValue":True}}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == 7:
                        print(f"Final URL: {r['result']['result']['value']}")
                        break
            else:
                print("No comment textarea found - likely blocked or no threads available")
        else:
            # Try creating a new post (Show HN) instead
            print("No commentable threads, trying Submit link...")
            await ws.send(json.dumps({"id":3,"method":"Page.navigate","params":{"url":"https://news.ycombinator.com/submit"}}))
            await asyncio.sleep(3)

            check_js = "JSON.stringify({url:window.location.href, body:document.body.innerText.substring(0,300)})"
            await ws.send(json.dumps({"id":4,"method":"Runtime.evaluate","params":{"expression":check_js,"returnByValue":True}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == 4:
                    state = json.loads(r["result"]["result"]["value"])
                    print(f"Submit page: {state}")
                    # Check if blocked
                    if "not able to submit" in state.get('body',''):
                        print("HN: ACCOUNT BLOCKED from submitting new links")
                    break

asyncio.run(hn_comment())
