"""Post comments on Dev.to articles via Playwright CDP"""
import json, asyncio, urllib.request
from playwright.async_api import async_playwright

COMMENTS = [
    {
        "url": "https://dev.to/atul_verma_9b425fa7292242/i-built-2-free-tools-to-learn-nextjs-16-heres-the-tech-stack-and-what-i-learned-52lg",
        "text": "Nice work! I also built a free invoice generator (Next.js + Cloudflare Pages) — invoicepad.net. Same philosophy: no sign-up, instant PDF. One thing I learned: SEO for template pages (freelance writer, web developer, etc.) works better than trying to rank the homepage. Keep building!"
    },
    {
        "url": "https://dev.to/ryancadev/i-got-tired-of-opening-5-different-sites-to-plan-my-nutrition-so-i-built-one-free-hub-4g2e",
        "text": "Great idea consolidating everything into one hub. I faced the same problem and built freetdee.com — a free TDEE + macro calculator with bodybuilding-specific activity levels. The Mifflin-St Jeor formula implementation was the trickiest part. How did you handle the activity multiplier for lifters vs regular users?"
    }
]

def cdp():
    with urllib.request.urlopen('http://127.0.0.1:9223/json/version', timeout=10) as r:
        return json.load(r)['webSocketDebuggerUrl']

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp())
        ctx = browser.contexts[0]

        for comment in COMMENTS:
            page = await ctx.new_page()
            await page.goto(comment['url'], wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(4000)
            print(f'URL: {page.url}')

            # Scroll to comments section
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight * 0.7)')
            await page.wait_for_timeout(2000)

            # Find the comment textarea
            textarea = page.locator('textarea#text-area, textarea[aria-label*="comment" i], textarea[placeholder*="comment" i]').first
            if await textarea.count() > 0:
                await textarea.click()
                await page.keyboard.type(comment['text'], delay=5)
                await page.wait_for_timeout(1000)
                print('Comment typed')

                # Find Submit button
                submit = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Post")').first
                if await submit.count() > 0 and await submit.is_enabled():
                    await submit.click()
                    print('Submit clicked')
                    await page.wait_for_timeout(5000)
                    print(f'After submit: {page.url}')
            else:
                print('No comment textarea found')

            await page.close()

asyncio.run(main())
