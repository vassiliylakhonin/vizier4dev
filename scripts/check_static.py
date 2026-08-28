#!/usr/bin/env python3
"""Dependency-free checks for the two self-contained Vizier demo pages."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = (ROOT / "index.html", ROOT / "landing.html")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang") or ""
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"] or "")


def check_page(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    errors: list[str] = []

    if parser.lang != "en":
        errors.append(f"{path.name}: expected <html lang=\"en\">")
    if parser.scripts:
        errors.append(f"{path.name}: external scripts are not allowed: {parser.scripts}")
    if re.search(r"\b(fetch|XMLHttpRequest|WebSocket)\s*\(", text):
        errors.append(f"{path.name}: unexpected network API call")
    if re.search(r"<button\b[^>]*>(?:(?!</button>).)*<button\b", text, re.IGNORECASE | re.DOTALL):
        errors.append(f"{path.name}: nested buttons break click handling and accessibility")
    has_language_content = (
        ("const DICT=" in text and "const TOUR_RU=" in text and "function setLang" in text)
        if path.name == "index.html"
        else ('class="ru"' in text and 'class="en"' in text)
    )
    if "v4d_lang" not in text or not has_language_content:
        errors.append(f"{path.name}: bilingual language contract is incomplete")

    for href in parser.links:
        if href.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = href.split("#", 1)[0]
        if target and not (ROOT / target).exists():
            errors.append(f"{path.name}: missing local link target {target}")
    return errors


def main() -> int:
    errors = [error for page in PAGES for error in check_page(page)]
    headers = (ROOT / "_headers").read_text(encoding="utf-8")
    for required in (
        "Content-Security-Policy:",
        "X-Content-Type-Options: nosniff",
        "Referrer-Policy: no-referrer",
        "Permissions-Policy:",
        "X-Robots-Tag: noindex",
    ):
        if required not in headers:
            errors.append(f"_headers: missing {required}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("ok: two self-contained pages, local links, bilingual contract, and security headers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
