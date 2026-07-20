"""Publish a Dev.to article via CDP (GavinBuilds Chrome) - simplified evaluate approach."""
import asyncio, json, urllib.request, time
import websockets

TITLE = "How I Built 8 Free Browser Tools With AI — First Click Milestone"
TAGS_STR = "webdev,seo,nextjs,tutorial,ai"
BODY_MD = r"""Today I hit a small milestone with my 8 free browser tools: the weakest site got its first Google click.

## What I built

Eight free browser tools, all static sites built with Next.js and deployed on Cloudflare Pages:

- [LivePhotoKit](https://livephotokit.com/) — HEIC & Live Photo converter
- [iWorkViewer](https://iworkviewer.com/) — Open Apple iWork files online
- [PlantingCalendar](https://plantingcalendar.net/) — USDA zone planting calendar
- [BabyPercent](https://babypercent.com/) — Baby growth percentile calculator
- [FreeTDEE](https://freetdee.com/) — TDEE, calorie & macro calculator
- [InvoicePad](https://invoicepad.net/) — Invoice & receipt generator
- [ZonePlan](https://zoneplan.net/) — Time zone meeting planner
- [PupVax](https://pupvax.com/) — Puppy vaccine schedule

All open source on [GitHub](https://github.com/Gavin1901).

## How I do daily maintenance

Every day I run a 7-step routine:

1. Health check: curl all 8 homepages, robots.txt and sitemaps
2. IndexNow: submit 20 URLs per site to Bing/IndexNow API
3. GSC data: scrape Google Search Console for clicks, impressions, CTR
4. Deep SEO audit: noindex, canonical, title, GA4, AdSense, schema
5. Pick the weakest site and change exactly one variable
6. Publish 3-5 backlinks on GitHub and Dev.to
7. Log everything to a public evidence repo

## Today's signal

[FreeTDEE.com](https://freetdee.com/) got its first organic click. It was 0 clicks for weeks. A GSC query check showed "tdee macro calculator" had 6 impressions at position 43 but zero clicks. So I updated the macro-calculator page title from "Macro Calculator 2026" to "TDEE Macro Calculator 2026" to match the search query exactly.

One variable. I'll check GSC in 2-3 days.

## What I learned

- Don't change five things at once. Change one. Wait for data.
- Git push is not deploy. Always verify the live domain.
- The weakest site just broke zero. The method works.

Next: PupVax (0 clicks), ZonePlan (only 4 pages indexed)."""

async def send_and_recv(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    return json.loads(await ws.recv())

async def evaluate(ws, msg_id, expression):
    return await send_and_recv(ws, msg_id, 'Runtime.evaluate', {
        'expression': expression,
        'returnByValue': True
    })

async def main():
    tabs = json.loads(urllib.request.urlopen('http://localhost:9223/json').read())
    devto_tab = None
    for t in tabs:
        if 'dev.to/new' in t.get('url', ''):
            devto_tab = t
            break
    if not devto_tab:
        print("ERROR: Dev.to new post tab not found")
        return

    ws_url = devto_tab['webSocketDebuggerUrl']
    async with websockets.connect(ws_url, max_size=10_000_000) as ws:
        await send_and_recv(ws, 1, 'Runtime.enable')
        await asyncio.sleep(2)

        # Check page state
        r = await evaluate(ws, 2, 'document.title')
        print(f"Page: {r.get('result',{}).get('result',{}).get('value','???')}")

        # Fill title
        title_expr = f"""
        (function() {{
            const ta = document.querySelector('textarea[aria-label=\"Post Title\"]');
            if (ta) {{
                const s = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
                s.call(ta, {json.dumps(TITLE)});
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return 'OK: ' + ta.value.substring(0,50);
            }}
            return 'NOT FOUND';
        }})()
        """
        r = await evaluate(ws, 10, title_expr)
        print(f"Title: {r.get('result',{}).get('result',{}).get('value','???')}")
        await asyncio.sleep(1)

        # Fill body - try textarea first (v1 markdown editor), then contenteditable
        body_expr = f"""
        (function() {{
            // Try v1 markdown textarea
            const ta = document.querySelector('textarea#article_body_markdown, textarea[aria-label*=\"body\" i]');
            if (ta) {{
                const s = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
                s.call(ta, {json.dumps(BODY_MD)});
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return 'OK(textarea v1): ' + ta.value.length + ' chars';
            }}
            // Try contenteditable
            const ed = document.querySelector('[contenteditable=\"true\"]');
            if (ed) {{
                ed.focus();
                ed.textContent = {json.dumps(BODY_MD)};
                ed.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return 'OK(contenteditable): ' + ed.textContent.length + ' chars';
            }}
            return 'NOT FOUND - check page';
        }})()
        """
        r = await evaluate(ws, 11, body_expr)
        print(f"Body: {r.get('result',{}).get('result',{}).get('value','???')}")
        await asyncio.sleep(2)

        # Fill tags
        tags_expr = f"""
        (function() {{
            const inp = document.querySelector('input[placeholder*=\"tag\" i]');
            if (!inp) return 'TAG INPUT NOT FOUND';
            const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
            const tags = {json.dumps(TAGS_STR)}.split(',');
            const results = [];
            for (const tag of tags) {{
                s.call(inp, tag.trim());
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inp.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }}));
                inp.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }}));
                results.push(tag.trim());
            }}
            return 'OK: ' + results.join(', ');
        }})()
        """
        r = await evaluate(ws, 12, tags_expr)
        print(f"Tags: {r.get('result',{}).get('result',{}).get('value','???')}")
        await asyncio.sleep(2)

        # Click Publish
        pub_expr = """
        (function() {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                const txt = b.textContent.trim().toLowerCase();
                if (txt.includes('publish') && !txt.includes('unpublish')) {
                    b.scrollIntoView();
                    b.click();
                    return 'Clicked: ' + b.textContent.trim();
                }
            }
            return 'PUBLISH BUTTON NOT FOUND';
        })()
        """
        r = await evaluate(ws, 13, pub_expr)
        print(f"Publish: {r.get('result',{}).get('result',{}).get('value','???')}")
        await asyncio.sleep(5)

        # Get final URL
        r = await evaluate(ws, 14, 'document.location.href')
        final_url = r.get('result',{}).get('result',{}).get('value','???')
        print(f"\nFinal URL: {final_url}")

asyncio.run(main())
