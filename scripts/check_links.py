#!/usr/bin/env python3
"""サイト全HTMLのリンク・広告表記の点検。

    python3 scripts/check_links.py            # 内部リンク + 表記チェックのみ(高速)
    python3 scripts/check_links.py --http     # 外部リンクのHTTP到達性も検査

検査項目:
- 内部リンク・画像パスの存在
- 外部リンク(アフィリエイト含む)のHTTPステータス(--http時)
- 商品・広告リンクの rel="sponsored" 漏れ
- アフィリエイトリンクを含むページの広告表記の有無
- affiliate-config.js の未設定項目
"""
import glob
import os
import re
import ssl
import sys
import urllib.request
from html.parser import HTMLParser

# macOSのPythonは証明書ストア未設定のことがある。certifiがあれば使い、
# なければ検証なしで到達性のみ確認する(リンク切れ検出が目的のため)。
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    try:
        SSL_CONTEXT = ssl.create_default_context()
        SSL_CONTEXT.load_default_certs()
        with urllib.request.urlopen("https://www.google.com", timeout=5, context=SSL_CONTEXT):
            pass
    except Exception:
        SSL_CONTEXT = ssl._create_unverified_context()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFFILIATE_HOSTS = (
    "amazon.co.jp",
    "amzn.to",
    "rakuten.co.jp",
    "shopping.yahoo.co.jp",
    "a8.net",
    "valuecommerce",
    "moshimo",
    "af.moshimo.com",
)
DISCLOSURE_KEYWORDS = ("広告", "PR")


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []  # (tag, attrs dict)

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "img", "script", "link"):
            d = dict(attrs)
            # preconnect/dns-prefetch はドメインルートへのヒントなので到達性検査の対象外
            if tag == "link" and d.get("rel") in ("preconnect", "dns-prefetch"):
                return
            self.links.append((tag, d))


def is_affiliate(url):
    return any(host in url for host in AFFILIATE_HOSTS)


def check_http(url, timeout=10):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (link checker)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as res:
            return res.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):  # HEAD拒否はGETで再試行
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link checker)"})
                with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as res:
                    return res.status
            except Exception as e2:
                return getattr(e2, "code", str(e2))
        return e.code
    except Exception as e:
        return str(e)


def main():
    do_http = "--http" in sys.argv
    problems = []
    external_urls = {}  # url -> [pages]

    pages = [
        p for p in
        glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "articles", "*.html"))
    ]

    for page in sorted(pages):
        rel_page = os.path.relpath(page, ROOT)
        html = open(page).read()
        parser = LinkCollector()
        parser.feed(html)

        page_has_affiliate_link = False

        for tag, attrs in parser.links:
            url = attrs.get("href") or attrs.get("src")
            if not url or url.startswith(("#", "mailto:", "data:", "javascript:")):
                continue

            if url.startswith("http"):
                external_urls.setdefault(url, []).append(rel_page)
                if tag == "a" and is_affiliate(url):
                    page_has_affiliate_link = True
                    rel = attrs.get("rel", "")
                    if "sponsored" not in rel:
                        problems.append(f'[sponsored漏れ] {rel_page}: {url[:80]} (rel="{rel}")')
            else:
                path = os.path.normpath(os.path.join(os.path.dirname(page), url.split("#")[0].split("?")[0]))
                if not os.path.exists(path):
                    problems.append(f"[内部リンク切れ] {rel_page}: {url}")

        if page_has_affiliate_link and not any(k in html for k in DISCLOSURE_KEYWORDS):
            problems.append(f"[広告表記なし] {rel_page}: アフィリエイトリンクがあるのに広告/PR表記が見つからない")

    # affiliate-config.js の未設定チェック
    config_path = os.path.join(ROOT, "js", "affiliate-config.js")
    if os.path.exists(config_path):
        config = open(config_path).read()
        unset = []
        if re.search(r'associateTag:\s*""', config):
            unset.append("amazon.associateTag")
        empty_templates = len(re.findall(r'affiliateUrlTemplate:\s*""', config))
        if empty_templates:
            unset.append(f"affiliateUrlTemplate 未設定 {empty_templates}件 (rakuten/yahoo)")
        if unset:
            problems.append(f"[未設定] js/affiliate-config.js: {', '.join(unset)}")

    # analytics.js の未設定チェック
    analytics_path = os.path.join(ROOT, "js", "analytics.js")
    if os.path.exists(analytics_path) and re.search(r'MEASUREMENT_ID = ""', open(analytics_path).read()):
        problems.append("[未設定] js/analytics.js: MEASUREMENT_ID が空(GA4未接続)")

    if do_http:
        print(f"外部リンク {len(external_urls)} 件を検査中...")
        for url, sources in sorted(external_urls.items()):
            status = check_http(url)
            if status not in (200, 301, 302, 308):
                problems.append(f"[外部リンクNG {status}] {url[:90]} (使用: {', '.join(sorted(set(sources))[:3])})")

    print(f"\n=== リンク点検レポート ({len(pages)}ページ) ===")
    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} 件の指摘")
        return 1
    print("問題なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
