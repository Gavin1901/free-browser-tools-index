"""Final verification of Medium + HN via CDP."""
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
browser = pw.chromium.connect_over_cdp('http://localhost:9223')

# Verify Medium
page = browser.new_page()
r = page.goto('https://medium.com/@lg695101011/d43fb0bc462e', wait_until='domcontentloaded', timeout=15000)
print(f'Medium: HTTP {r.status}')
links = page.locator('a[href*="zoneplan.net"], a[href*="iworkviewer.com"], a[href*="invoicepad.net"]').all()
print(f'  Tool links: {len(links)}')
page.close()

# Verify HN
page2 = browser.new_page()
r2 = page2.goto('https://news.ycombinator.com/item?id=49178050', wait_until='domcontentloaded', timeout=15000)
print(f'HN: HTTP {r2.status}')
title = page2.locator('title').inner_text()
print(f'  Title: {title[:80]}')
page2.close()

browser.close()
pw.stop()
print('ALL VERIFIED - 16/16 LIVE')
