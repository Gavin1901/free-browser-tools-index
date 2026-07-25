import concurrent.futures
import hashlib
import json
import re
import ssl
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


SITES = [
    "iworkviewer.com",
    "livephotokit.com",
    "plantingcalendar.net",
    "freetdee.com",
    "babypercent.com",
    "invoicepad.net",
    "zoneplan.net",
    "pupvax.com",
]

UA = "Mozilla/5.0 (compatible; GavinBuildsIndexAudit/1.0)"
CTX = ssl.create_default_context()


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.in_title = False
        self.meta = []
        self.links = []
        self.canonicals = []
        self.h1 = []
        self.in_h1 = False
        self.text = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        elif tag == "meta":
            self.meta.append({k.lower(): v for k, v in attrs.items()})
        elif tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        elif tag == "link" and "canonical" in (attrs.get("rel") or "").lower():
            if attrs.get("href"):
                self.canonicals.append(attrs["href"])

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_h1:
            self.h1.append(data)
        if not self.skip:
            self.text.append(data)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.geturl(), r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.geturl(), e.headers, e.read()
    except Exception as e:
        return 0, url, {}, str(e).encode("utf-8", "replace")


def normalize_url(url):
    p = urllib.parse.urlsplit(url)
    path = re.sub(r"/+", "/", p.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), path, "", ""))


def sitemap_urls(domain):
    root = f"https://{domain}/sitemap.xml"
    seen_maps, urls, queue = set(), set(), [root]
    errors = []
    while queue:
        sm = queue.pop(0)
        if sm in seen_maps:
            continue
        seen_maps.add(sm)
        status, _, _, body = fetch(sm)
        if status != 200:
            errors.append({"url": sm, "status": status})
            continue
        try:
            doc = ET.fromstring(body)
        except Exception as e:
            errors.append({"url": sm, "status": status, "parse_error": str(e)})
            continue
        locs = [x.text.strip() for x in doc.iter() if x.tag.endswith("loc") and x.text]
        if doc.tag.endswith("sitemapindex"):
            queue.extend(locs)
        else:
            urls.update(locs)
    return sorted(urls), errors


def audit_page(url, domain):
    status, final_url, headers, body = fetch(url)
    result = {
        "url": url,
        "status": status,
        "final_url": final_url,
        "redirected": normalize_url(url) != normalize_url(final_url),
        "content_type": headers.get("Content-Type", "") if hasattr(headers, "get") else "",
        "x_robots_tag": headers.get("X-Robots-Tag", "") if hasattr(headers, "get") else "",
    }
    if status != 200 or b"<html" not in body[:5000].lower():
        result["error"] = body[:300].decode("utf-8", "replace")
        return result
    html = body.decode("utf-8", "replace")
    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:
        result["parse_error"] = str(e)
    title = re.sub(r"\s+", " ", " ".join(p.title)).strip()
    h1 = re.sub(r"\s+", " ", " ".join(p.h1)).strip()
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text)
    desc = ""
    robots = []
    for m in p.meta:
        name = (m.get("name") or m.get("property") or "").lower()
        if name == "description":
            desc = m.get("content", "")
        if name in ("robots", "googlebot"):
            robots.append(m.get("content", ""))
    canon = p.canonicals[0] if p.canonicals else ""
    internal = []
    for href in p.links:
        absolute = urllib.parse.urljoin(final_url, href)
        if urllib.parse.urlsplit(absolute).netloc.lower() == domain:
            internal.append(normalize_url(absolute))
    result.update(
        {
            "title": title,
            "description": re.sub(r"\s+", " ", desc).strip(),
            "h1": h1,
            "canonical": canon,
            "canonical_matches": bool(canon) and normalize_url(canon) == normalize_url(final_url),
            "robots_meta": "; ".join(robots),
            "noindex": "noindex" in (" ".join(robots) + " " + result["x_robots_tag"]).lower(),
            "word_count": len(words),
            "text_hash": hashlib.sha1(text.lower().encode("utf-8")).hexdigest(),
            "internal_links": sorted(set(internal)),
            "internal_link_count": len(set(internal)),
        }
    )
    return result


def summarize(domain, urls, pages, sitemap_errors):
    normalized_set = {normalize_url(u) for u in urls}
    indegree = Counter()
    for p in pages:
        for link in p.get("internal_links", []):
            if link in normalized_set:
                indegree[link] += 1
    for p in pages:
        p["sitemap_indegree"] = indegree[normalize_url(p["url"])]
    titles = Counter(p.get("title", "") for p in pages if p.get("title"))
    descs = Counter(p.get("description", "") for p in pages if p.get("description"))
    hashes = Counter(p.get("text_hash", "") for p in pages if p.get("text_hash"))
    issues = {
        "non_200": [p["url"] for p in pages if p["status"] != 200],
        "redirected_in_sitemap": [p["url"] for p in pages if p.get("redirected")],
        "missing_canonical": [p["url"] for p in pages if p["status"] == 200 and not p.get("canonical")],
        "canonical_mismatch": [p["url"] for p in pages if p.get("canonical") and not p.get("canonical_matches")],
        "noindex": [p["url"] for p in pages if p.get("noindex")],
        "missing_title": [p["url"] for p in pages if p["status"] == 200 and not p.get("title")],
        "missing_description": [p["url"] for p in pages if p["status"] == 200 and not p.get("description")],
        "missing_h1": [p["url"] for p in pages if p["status"] == 200 and not p.get("h1")],
        "thin_under_200_words": [p["url"] for p in pages if p.get("word_count", 9999) < 200],
        "orphan_in_sitemap": [p["url"] for p in pages if p.get("sitemap_indegree", 0) == 0 and normalize_url(p["url"]) != normalize_url(f"https://{domain}/")],
        "duplicate_titles": {k: v for k, v in titles.items() if v > 1},
        "duplicate_descriptions": {k: v for k, v in descs.items() if v > 1},
        "duplicate_text_hashes": {k: v for k, v in hashes.items() if v > 1},
        "sitemap_errors": sitemap_errors,
    }
    return {
        "domain": domain,
        "sitemap_url_count": len(urls),
        "audited": len(pages),
        "issue_counts": {k: len(v) if not isinstance(v, dict) else sum(v.values()) for k, v in issues.items()},
        "issues": issues,
        "pages": pages,
    }


def main():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    out_dir = Path(r"D:\Tools\ai-tool-index\logs")
    daily_dir = Path(r"D:\Tools\ai-tool-index\daily")
    all_results = []
    for domain in SITES:
        urls, sm_errors = sitemap_urls(domain)
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
            pages = list(ex.map(lambda u: audit_page(u, domain), urls))
        all_results.append(summarize(domain, urls, pages, sm_errors))
        print(domain, len(urls), "URLs audited")
    json_path = out_dir / f"{date}-deep-indexability-audit.json"
    json_path.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        f"# {date} Deep Indexability Audit",
        "",
        f"Run time: {now.isoformat(timespec='seconds')}",
        "",
        "| Site | Sitemap URLs | Non-200 | Redirects | Missing canonical | Canonical mismatch | Noindex | Thin <200 | Orphan | Duplicate title count | Duplicate body count |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in all_results:
        c = r["issue_counts"]
        lines.append(
            f"| {r['domain']} | {r['sitemap_url_count']} | {c['non_200']} | {c['redirected_in_sitemap']} | "
            f"{c['missing_canonical']} | {c['canonical_mismatch']} | {c['noindex']} | "
            f"{c['thin_under_200_words']} | {c['orphan_in_sitemap']} | "
            f"{c['duplicate_titles']} | {c['duplicate_text_hashes']} |"
        )
    lines += ["", "Full page-level evidence:", f"`logs/{json_path.name}`", ""]
    md_path = daily_dir / f"{date}-deep-indexability-audit.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
