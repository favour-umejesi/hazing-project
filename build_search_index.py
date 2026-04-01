#!/usr/bin/env python3
"""Build search-index.json for static End Hazing mirror + fix UA_TitleSearch form actions."""

import html as html_module
import json
import os
import re
import glob

SITE_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cloned_site",
    "endhazing.sl.ua.edu",
)


def depth_from_root(rel_path: str) -> int:
    d = os.path.dirname(rel_path.replace("\\", "/"))
    if not d or d == ".":
        return 0
    return len([x for x in d.split("/") if x])


def search_form_action_for_file(rel_path: str) -> str:
    d = depth_from_root(rel_path)
    return ("../" * d) + "search/index.html"


def strip_html_for_text(raw: str) -> str:
    raw = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"\s+", " ", raw)
    return html_module.unescape(raw).strip()


def should_index(rel: str) -> bool:
    if "/feed/" in rel or rel.startswith("wp-json"):
        return False
    if rel.replace("\\", "/").startswith("search/"):
        return False
    if not rel.lower().endswith(".html"):
        return False
    return True


def main():
    all_html = glob.glob(os.path.join(SITE_ROOT, "**", "*.html"), recursive=True)
    entries = []
    for filepath in sorted(all_html):
        rel = os.path.relpath(filepath, SITE_ROOT).replace("\\", "/")
        if not should_index(rel):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError:
            continue
        m = re.search(r"<title[^>]*>([\s\S]*?)</title>", content, re.I)
        title = strip_html_for_text(m.group(1)) if m else rel
        body_m = re.search(r"<body[^>]*>([\s\S]*)</body>", content, re.I)
        body = body_m.group(1) if body_m else content
        text = strip_html_for_text(body)[:8000]
        entries.append({"path": rel, "title": title, "text": text})

    out_json = os.path.join(SITE_ROOT, "search-index.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=0)
    print(f"Wrote {len(entries)} entries to {out_json}")

    # Fix search form action on every page
    updated = 0
    for filepath in all_html:
        rel = os.path.relpath(filepath, SITE_ROOT).replace("\\", "/")
        if not rel.lower().endswith(".html"):
            continue
        if "/feed/" in rel or rel.startswith("wp-json"):
            continue
        new_action = search_form_action_for_file(rel)
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            c = f.read()
        orig = c
        c = re.sub(
            r'(id="UA_TitleSearch"\s*\n\s*action=")[^"]*(")',
            rf"\1{new_action}\2",
            c,
            count=1,
        )
        if c != orig:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(c)
            updated += 1
    print(f"Updated UA_TitleSearch form action in {updated} files")


if __name__ == "__main__":
    main()
