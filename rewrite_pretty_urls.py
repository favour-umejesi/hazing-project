#!/usr/bin/env python3
"""Rewrite WordPress-style index.html?p=ID links to folder paths across the static site."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent / "cloned_site" / "endhazing.sl.ua.edu"

# Home page (front page)
HOME_PAGE_ID = "6"

SKIP_PARTS = {"/feed/", "wp-json", "/search/"}

def should_process(path: Path) -> bool:
    rel = path.as_posix()
    if not rel.endswith(".html"):
        return False
    return not any(part in rel for part in SKIP_PARTS)


def entity_id_from_html(head: str) -> str | None:
    post_m = re.search(r"\bpostid-(\d+)\b", head)
    if post_m:
        return post_m.group(1)
    page_m = re.search(r"\bpage-id-(\d+)\b", head)
    return page_m.group(1) if page_m else None


def folder_to_path(folder: Path, root: Path) -> str:
    rel = folder.relative_to(root).as_posix()
    return "" if rel == "." else f"{rel}/"


def should_skip_for_id_map(html_file: Path, root: Path) -> bool:
    """Skip duplicate mirrors that share page IDs with canonical section folders."""
    rel = html_file.relative_to(root).as_posix()
    if rel == "violations/index.html":
        return True
    return False


def build_id_map(root: Path) -> dict[str, str]:
    """Map WordPress page/post IDs to site paths (trailing slash, no index.html)."""
    id_map: dict[str, str] = {HOME_PAGE_ID: ""}

    def scan(files: list[Path], *, only_if_missing: bool = False) -> None:
        for html_file in files:
            if not should_process(html_file) or should_skip_for_id_map(html_file, root):
                continue
            try:
                text = html_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            body_m = re.search(r"<body\b", text, re.I)
            snippet = text[body_m.start() : body_m.start() + 4000] if body_m else text[:8000]
            entity_id = entity_id_from_html(snippet)
            if not entity_id:
                continue
            if only_if_missing and entity_id in id_map:
                continue
            id_map[entity_id] = folder_to_path(html_file.parent, root)

    all_html = sorted(root.rglob("*.html"))
    # Prefer real section folders over root-level index.html?p= mirrors
    scan([f for f in all_html if f.name == "index.html"])
    scan([f for f in all_html if f.name.startswith("index.html?p=")], only_if_missing=True)

    return id_map


def link_to(from_file: Path, root: Path, target_path: str, fragment: str = "") -> str:
    if target_path == "":
        depth = len(from_file.parent.relative_to(root).parts)
        href = "./" if depth == 0 else "../" * depth
    else:
        target_dir = root / target_path.rstrip("/")
        href = os.path.relpath(target_dir, from_file.parent).replace("\\", "/")
        if not href.endswith("/"):
            href += "/"
    if fragment:
        href += f"#{fragment}"
    return href


def rewrite_content(html: str, from_file: Path, root: Path, id_map: dict[str, str]) -> tuple[str, int]:
    count = 0

    # Include optional ../ prefix from mirror paths so we do not double-up (../../../../ + target/)
    pattern = re.compile(
        r"(?:\.\./)*index\.html(?:%3F|\?)p=(\d+)\.html(?:#([^\s\"']+))?",
        re.IGNORECASE,
    )

    def sub(m: re.Match[str]) -> str:
        nonlocal count
        entity_id = m.group(1)
        fragment = m.group(2) or ""
        target = id_map.get(entity_id)
        if target is None:
            return m.group(0)
        count += 1
        return link_to(from_file, root, target, fragment)

    html = pattern.sub(sub, html)
    return html, count


# Anchor text -> folder path (used when href is only a chain of ../ with no target folder)
NAV_LABEL_TO_PATH: dict[str, str] = {
    "About": "about/",
    "What is Hazing": "what-is-hazing/",
    "What is hazing?": "what-is-hazing/",
    "Hazing Statistics": "what-is-hazing/hazing-statistics/",
    "FAQ": "what-is-hazing/faq/",
    "GSU Hazing Policy": "what-is-hazing/ua-hazing-policy/",
    "GSU Code of Student Conduct": "what-is-hazing/ua-code-of-student-conduct/",
    "State Law": "what-is-hazing/state-law/",
    "Prevent It": "prevent-it/",
    "How to Prevent": "prevent-it/how-to-prevent/",
    "Hazing Prevention Team": "hazing-prevention-team/",
    "Report It": "report-it/",
    "report It": "report-it/",
    "Campus Support Services": "report-it/campus-support-services/",
    "Parents and Family": "parents-and-family/",
    "Hazing Transparency Report": "hazing-transparency-report/",
    "Report Hazing Here": "report-it/",
}


def resolve_internal_path(root: Path, path_suffix: str) -> str | None:
    """Map a partial path (e.g. 2024/2024/foo/) to its folder under site root."""
    path_suffix = path_suffix.strip("/")
    if not path_suffix:
        return ""
    candidates = [
        p.parent
        for p in root.glob(f"**/{path_suffix}/index.html")
        if should_process(p)
    ]
    if not candidates:
        return None
    best = min(candidates, key=lambda p: len(p.relative_to(root).parts))
    return folder_to_path(best, root)


def repair_path_suffix_links(
    html: str, from_file: Path, root: Path
) -> tuple[str, int]:
    """Fix href='../../…/partial/path/' when too many ../ are present."""
    count = 0
    pattern = re.compile(
        r'href="((?:\.\./)+)([^"#?]+/?)"',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        suffix = m.group(2).lstrip("/")
        if suffix.startswith(("http:", "https:", "mailto:", "tel:", "javascript:")):
            return m.group(0)
        target = resolve_internal_path(root, suffix)
        if target is None:
            return m.group(0)
        correct = link_to(from_file, root, target)
        if m.group(0) == f'href="{correct}"':
            return m.group(0)
        count += 1
        return f'href="{correct}"'

    html = pattern.sub(repl, html)
    return html, count


def repair_orphan_relative_links(
    html: str, from_file: Path, root: Path
) -> tuple[str, int]:
    """Fix href='../../…/' with no folder name (broken prior rewrites)."""
    count = 0
    orphan = re.compile(
        r'href="((?:\.\./)+)"([^>]*>)([^<]+)</a>',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        label = m.group(3).strip()
        target: str | None = NAV_LABEL_TO_PATH.get(label)
        if target is None and re.fullmatch(r"\d{4}", label):
            year_path = f"posts/category/{label}/"
            if (root / year_path).is_dir():
                target = year_path
        if target is None:
            return m.group(0)
        count += 1
        return f'href="{link_to(from_file, root, target)}"{m.group(2)}{label}</a>'

    html = orphan.sub(repl, html)

    self_path = folder_to_path(from_file.parent, root)
    self_href = link_to(from_file, root, self_path)
    canon = re.compile(r'<link rel="canonical" href="(?:\.\./)+" */>', re.I)
    html, n = canon.subn(f'<link rel="canonical" href="{self_href}" />', html)
    count += n

    skip = re.compile(
        r'(<a class="screen-reader-text skip-link" href=")(?:\.\./)+(#[^"]+)"',
        re.I,
    )
    html, n = skip.subn(rf"\1{self_href}\2\"", html)
    count += n

    return html, count


def resolve_href_target(
    from_file: Path, root: Path, prefix: str, dir_part: str
) -> str | None:
    """Resolve a relative href (without index.html) to a site folder path."""
    raw = f"{prefix}{dir_part}".rstrip("/")
    if not raw:
        return ""
    target = (from_file.parent / raw).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    if target.is_dir() and (target / "index.html").is_file():
        return folder_to_path(target, root)
    return resolve_internal_path(root, raw)


def repair_index_html_hrefs(
    html: str, from_file: Path, root: Path
) -> tuple[str, int]:
    """Replace index.html in internal navigation and content links."""
    count = 0
    home = link_to(from_file, root, "")

    bar = re.compile(
        r'(<a href=")(?:\.\./)*index\.html(" class="ua_title-bar_name">)',
        re.I,
    )
    html, n = bar.subn(rf"\1{home}\2", html)
    count += n

    html, n = re.subn(r'href="index\.html(#[^"]+)"', r'href="./\1"', html)
    count += n

    html, n = re.subn(
        r'action="(?:\.\./)*search/index\.html"',
        f'action="{link_to(from_file, root, "search/")}"',
        html,
        flags=re.I,
    )
    count += n

    html, n = re.subn(
        r"<link rel=['\"]shortlink['\"] href=['\"]index\.html['\"]",
        f'<link rel="shortlink" href="{home}"',
        html,
        flags=re.I,
    )
    count += n

    href_pat = re.compile(
        r'href="((?:\.\./)*)([^"#?]*?)index\.html([^"#]*)"', re.I
    )

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        prefix, dir_part, tail = m.group(1), m.group(2), m.group(3)
        if "wp-json" in dir_part or "wp-json" in prefix:
            return m.group(0)
        if not dir_part and not prefix.replace("../", "").replace("./", ""):
            count += 1
            return f'href="{home}{tail}"'
        if not dir_part and prefix:
            count += 1
            return f'href="{home}{tail}"'
        target = resolve_href_target(from_file, root, prefix, dir_part)
        if target is None:
            return m.group(0)
        count += 1
        return f'href="{link_to(from_file, root, target)}{tail}"'

    html = href_pat.sub(repl, html)
    return html, count


def repair_internal_links(
    html: str, from_file: Path, root: Path, id_map: dict[str, str]
) -> tuple[str, int]:
    """Normalize internal folder links (fixes doubled ../ from prior rewrites)."""
    count = 0
    paths = sorted({p for p in id_map.values() if p}, key=len, reverse=True)

    for target_path in paths:
        correct = link_to(from_file, root, target_path)
        correct_no_slash = correct.rstrip("/")
        pattern = re.compile(
            rf'href="(?:\.\./)*{re.escape(target_path)}(?:#([^"\']+))?"',
            re.IGNORECASE,
        )

        def repl(m: re.Match[str], c: str = correct, cns: str = correct_no_slash) -> str:
            nonlocal count
            count += 1
            if m.group(1):
                return f'href="{cns}#{m.group(1)}"'
            return f'href="{c}"'

        html = pattern.sub(repl, html)

    home = link_to(from_file, root, "")
    html, n = re.subn(r'href="(?:\.\./)*index\.html"', f'href="{home}"', html)
    count += n

    return html, count


def write_redirects(root: Path, id_map: dict[str, str]) -> None:
    lines = [
        "/index.html / 301",
        "/index.html/ / 301",
    ]
    for entity_id, path in sorted(id_map.items(), key=lambda x: int(x[0])):
        dest = "/" if not path else f"/{path}"
        lines.append(f"/index.html%3Fp={entity_id}.html {dest} 301")
        lines.append(f"/index.html?p={entity_id}.html {dest} 301")
    (root / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / ".htaccess").write_text(build_htaccess(id_map), encoding="utf-8")


def build_htaccess(id_map: dict[str, str]) -> str:
    rules = [
        "# Pretty URLs for Grambling End Hazing static site",
        "DirectoryIndex index.html",
        "",
        "<IfModule mod_rewrite.c>",
        "RewriteEngine On",
        "",
    ]
    for entity_id, path in sorted(id_map.items(), key=lambda x: int(x[0])):
        dest = "/" + path if path else "/"
        rules.append(
            f"RewriteRule ^index\\.html%3Fp={entity_id}\\.html$ {dest} [R=301,L,NE]"
        )
        rules.append(
            f"RewriteRule ^index\\.html\\?p={entity_id}(?:\\.html)?$ {dest} [R=301,L,NC]"
        )
    rules.extend(
        [
            "RewriteRule ^index\\.html$ / [R=301,L,NC]",
            "",
            "# Serve directory URLs without showing index.html",
            "RewriteCond %{REQUEST_FILENAME} -d",
            "RewriteCond %{REQUEST_FILENAME}/index.html -f",
            "RewriteRule ^(.+[^/])$ $1/ [R=301,L]",
            "</IfModule>",
            "",
        ]
    )
    return "\n".join(rules)


def main() -> int:
    root = SITE_ROOT
    if not root.is_dir():
        print(f"Site root not found: {root}", file=sys.stderr)
        return 1

    id_map = build_id_map(root)
    print(f"Mapped {len(id_map)} page/post IDs to folder paths")

    total_files = 0
    total_replacements = 0
    for html_file in sorted(root.rglob("*.html")):
        if not should_process(html_file):
            continue
        try:
            original = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        updated, n = rewrite_content(original, html_file, root, id_map)
        updated, n2 = repair_internal_links(updated, html_file, root, id_map)
        updated, n3 = repair_orphan_relative_links(updated, html_file, root)
        updated, n4 = repair_path_suffix_links(updated, html_file, root)
        updated, n5 = repair_index_html_hrefs(updated, html_file, root)
        if updated != original:
            html_file.write_text(updated, encoding="utf-8")
            total_files += 1
            total_replacements += n + n2 + n3 + n4 + n5

    write_redirects(root, id_map)
    print(f"Updated {total_files} files ({total_replacements} link rewrites)")
    print(f"Wrote {root / '_redirects'} and {root / '.htaccess'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
