"""Publish a Medium article through GavinBuilds Chrome using native editor events.

Do not replace Medium editor DOM or inject the whole article in one synthetic
event. Medium can render that text while rejecting the draft backend save.
This script types the title and body through keyboard events, verifies
DraftSaved after every paragraph, then publishes and prints public proof.
"""

import argparse
import asyncio
import json
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright


def cdp_endpoint(port: str) -> str:
    with urllib.request.urlopen(
        f"http://127.0.0.1:{port}/json/version", timeout=10
    ) as response:
        return json.load(response)["webSocketDebuggerUrl"]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--port", default="9223")
    parser.add_argument("--delay-ms", type=int, default=2)
    parser.add_argument("--paragraph-wait-ms", type=int, default=1800)
    args = parser.parse_args()

    body = Path(args.body_file).read_text(encoding="utf-8-sig")
    paragraphs = [paragraph.strip() for paragraph in body.split("\n\n") if paragraph.strip()]

    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(cdp_endpoint(args.port))
        context = browser.contexts[0]
        page = await context.new_page()
        failed_responses = []

        async def record_failed_response(response):
            if "medium.com" in response.url and response.status >= 400:
                failed_responses.append(
                    {"status": response.status, "url": response.url}
                )

        page.on("response", record_failed_response)
        await page.goto(
            "https://medium.com/new-story",
            wait_until="domcontentloaded",
            timeout=45_000,
        )
        await page.wait_for_timeout(5_000)

        title = page.locator("[data-testid=editorTitleParagraph]")
        editor = page.locator("[data-testid=editorParagraphText]")
        await title.click()
        await page.keyboard.type(args.title, delay=15)
        await page.wait_for_timeout(5_000)
        await editor.click()

        for index, paragraph in enumerate(paragraphs, start=1):
            await page.keyboard.type(paragraph, delay=args.delay_ms)
            await page.keyboard.press("Enter")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(args.paragraph_wait_ms)
            state = await page.locator("body").inner_text()
            if "cannot save your story" in state:
                raise RuntimeError(f"Medium rejected the draft after paragraph {index}")
            if "DraftSaved" not in state.replace(" ", ""):
                raise RuntimeError(f"DraftSaved proof missing after paragraph {index}")

        await page.wait_for_timeout(8_000)
        if failed_responses:
            raise RuntimeError(f"Medium returned failed responses: {failed_responses}")

        await page.get_by_text("Publish", exact=True).click()
        await page.wait_for_timeout(4_000)
        submission = next(
            candidate
            for candidate in context.pages
            if "/submission?" in candidate.url
        )
        publish_buttons = submission.locator("button")
        publish_index = None
        for index in range(await publish_buttons.count()):
            button = publish_buttons.nth(index)
            if (
                await button.is_visible()
                and await button.is_enabled()
                and (await button.inner_text()).strip() == "Publish"
            ):
                publish_index = index
                break
        if publish_index is None:
            raise RuntimeError("Medium final Publish button was not found")

        await publish_buttons.nth(publish_index).click()
        await submission.wait_for_timeout(12_000)
        proof = await submission.evaluate(
            """JSON.stringify({
                url: location.href,
                title: document.title,
                canonical: document.querySelector('link[rel=canonical]')?.href,
                links: [...document.querySelectorAll('a')].map(a => a.href)
            })"""
        )
        print(proof)


if __name__ == "__main__":
    asyncio.run(main())

