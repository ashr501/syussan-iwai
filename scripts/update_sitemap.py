#!/usr/bin/env python3
"""sitemap.xml をリポジトリ内のHTMLから再生成する。

記事の追加・削除後に実行する:
    python3 scripts/update_sitemap.py
"""
import glob
import os
import sys

BASE_URL = "https://honne-catalog.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ページごとの changefreq / priority。未指定の記事は monthly / 0.6
PAGE_SETTINGS = {
    "index.html": ("weekly", "1.0"),
    "products.html": ("weekly", "0.9"),
    "onegai-list.html": ("weekly", "0.9"),
    "about.html": ("yearly", "0.3"),
    "privacy.html": ("yearly", "0.3"),
    "articles/second-child-gifts.html": ("monthly", "0.9"),
    "articles/unwanted-gifts-ranking.html": ("monthly", "0.8"),
    "articles/appreciated-gifts-ranking.html": ("monthly", "0.8"),
    "articles/older-child-gift.html": ("monthly", "0.8"),
    "articles/naoshi-guide.html": ("monthly", "0.7"),
    "articles/book-card-gift-guide.html": ("monthly", "0.7"),
    "articles/cash-gift-guide.html": ("monthly", "0.7"),
    "articles/mom-selfcare-gift.html": ("monthly", "0.7"),
}
DEFAULT_SETTING = ("monthly", "0.6")


def collect_pages():
    pages = []
    for name in ["index.html", "products.html", "onegai-list.html", "about.html", "privacy.html"]:
        if os.path.exists(os.path.join(ROOT, name)):
            pages.append(name)
    pages += sorted(
        os.path.relpath(p, ROOT)
        for p in glob.glob(os.path.join(ROOT, "articles", "*.html"))
    )
    return pages


def build_sitemap(pages):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        loc = f"{BASE_URL}/" if page == "index.html" else f"{BASE_URL}/{page}"
        changefreq, priority = PAGE_SETTINGS.get(page, DEFAULT_SETTING)
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <changefreq>{changefreq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    pages = collect_pages()
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    new_content = build_sitemap(pages)
    old_content = open(sitemap_path).read() if os.path.exists(sitemap_path) else ""
    if new_content == old_content:
        print(f"sitemap.xml は最新です ({len(pages)}ページ)")
        return 0
    with open(sitemap_path, "w") as f:
        f.write(new_content)
    print(f"sitemap.xml を更新しました ({len(pages)}ページ)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
