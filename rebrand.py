#!/usr/bin/env python3
"""Rebrand the cloned End Hazing site from University of Alabama to Grambling State University."""

import os
import re
import glob

SITE_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cloned_site", "endhazing.sl.ua.edu"
)

GRAMBLING_CSS = '''<style id="grambling-overrides">
:root {
  --ua_color-link: #ECAA00 !important;
  --ua_color-link--inverse: #000000 !important;
}
.ua_brand-bar {
  background-color: #000000 !important;
}
.ua_title-bar {
  background-color: #ECAA00 !important;
}
.ua_title-bar_name,
.ua_title-bar a {
  color: #000000 !important;
}
.ua_title-bar_expander {
  color: #000000 !important;
}
.ua_primary-navigation {
  background-color: #000000 !important;
}
.ua_primary-navigation a {
  color: #ffffff !important;
}
.ua_primary-navigation ul ul {
  background-color: #1a1a1a !important;
}
.ua_primary-navigation ul ul a {
  color: #ECAA00 !important;
}
.ua_primary-navigation ul ul a:hover {
  color: #ffffff !important;
  background-color: #333333 !important;
}
.ua_primary-navigation li {
  border-color: #333333 !important;
}
.ua_primary-navigation button {
  color: #ECAA00 !important;
}
:root :where(.wp-element-button, .wp-block-button__link) {
  background-color: #000000 !important;
  color: #ECAA00 !important;
  border-color: #ECAA00 !important;
}
:root :where(.wp-element-button:hover, .wp-block-button__link:hover) {
  background-color: #ECAA00 !important;
  color: #000000 !important;
  border-color: #000000 !important;
}
.ua_link-list_item {
  background-color: #000000 !important;
  color: #ECAA00 !important;
}
.ua_link-list_item:hover {
  background-color: #ECAA00 !important;
  color: #000000 !important;
}
.ua_site-footer {
  background-color: #1a1a1a !important;
  color: #ffffff !important;
}
.ua_site-footer h2,
.ua_site-footer h3,
.ua_site-footer h4 {
  color: #ECAA00 !important;
}
.ua_site-footer p,
.ua_site-footer li:not(.wp-social-link):not(.wp-block-social-link),
.ua_site-footer span,
.ua_site-footer div {
  color: #ffffff !important;
}
.ua_site-footer a:where(:not(.wp-element-button)) {
  color: #ECAA00 !important;
}
/* Social icons in footer: gold logos, no chip background (overrides theme + footer li rules) */
.ua_minerva .ua_site-footer .wp-block-social-links .wp-social-link,
.ua_minerva .ua_site-footer .wp-block-social-links .wp-block-social-link {
  background: transparent !important;
  background-color: transparent !important;
  color: #ECAA00 !important;
}
.ua_minerva .ua_site-footer .wp-block-social-links .wp-social-link a,
.ua_minerva .ua_site-footer .wp-block-social-link-anchor {
  background: transparent !important;
  background-color: transparent !important;
  color: #ECAA00 !important;
}
.ua_minerva .ua_site-footer .wp-block-social-links svg,
.ua_minerva .ua_site-footer .wp-block-social-link-anchor svg {
  fill: #ECAA00 !important;
  color: #ECAA00 !important;
}
.ua_brand-footer {
  background-color: #000000 !important;
}
.ua_brand-footer a {
  color: #ECAA00 !important;
}
.ua_brand-footer p,
.ua_brand-footer span {
  color: #ffffff !important;
}
a:where(:not(.wp-element-button)) {
  color: #ECAA00;
}
.ua_page_title {
  color: #000000;
}
.is-style-elevated {
  border-top: 4px solid #ECAA00;
}
.sl-QueryLoop.is-style-elevated {
  border-top: 4px solid #ECAA00;
}
.sl-QueryLoop.is-style-elevated:hover {
  border-top-color: #000000;
}
.ua_title-bar_search button {
  background-color: #000000 !important;
  color: #ECAA00 !important;
}
.ua_card {
  border-color: #ECAA00 !important;
}
.wp-block-button__link.wp-element-button {
  border: 2px solid #ECAA00 !important;
}
.ua_cookie-banner__container .ua_cookie-banner__content button {
  background-color: #ECAA00 !important;
  color: #000000 !important;
}
</style>
'''

GRAMBLING_LOGO_SVG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 450 25'%3E%3Ctext x='0' y='19' fill='white' font-family='Georgia,serif' font-size='16' font-weight='bold' letter-spacing='2.5'%3EGRAMBLING STATE UNIVERSITY%3C/text%3E%3C/svg%3E"

GRAMBLING_FOOTER_LOGO_REL_PATH = "wp-content/uploads/sites/11/grambling-assets/gsu-g-logo-transparent.png"

UL_SYSTEM_SVG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 280 30'%3E%3Ctext x='0' y='20' fill='white' font-family='Georgia,serif' font-size='13' letter-spacing='1.5'%3EUNIVERSITY OF LOUISIANA SYSTEM%3C/text%3E%3C/svg%3E"


def find_html_files():
    """Find all HTML files in the cloned site, excluding feed/RSS and wp-json files."""
    all_html = glob.glob(os.path.join(SITE_ROOT, "**", "*.html"), recursive=True)
    filtered = []
    for f in all_html:
        rel = os.path.relpath(f, SITE_ROOT)
        if "/feed/" in rel or rel.startswith("wp-json"):
            continue
        filtered.append(f)
    return sorted(filtered)


def inject_css(content):
    """Inject the Grambling CSS overrides right before </head>."""
    if 'id="grambling-overrides"' in content:
        return content
    return content.replace("</head>", GRAMBLING_CSS + "\n</head>", 1)


def replace_brand_bar(content):
    """Replace the UA brand bar logo and link with Grambling's."""
    # Replace the UA logo image and link
    content = re.sub(
        r'<a\s+href="https://ua\.edu"\s+class="ua_brand-bar_logo">\s*'
        r'<img\s+src="[^"]*UA_Wordmark-White\.svg[^"]*"\s+alt="The University of Alabama"\s*/?\s*>\s*</a>',
        f'<a href="https://www.gram.edu/" class="ua_brand-bar_logo">'
        f' <img src="{GRAMBLING_LOGO_SVG}" alt="Grambling State University">'
        f' </a>',
        content,
        flags=re.DOTALL
    )
    # Replace myBama link
    content = re.sub(
        r'<a\s+href="http://mybama\.ua\.edu/"\s+class="ua_brand-bar_link">myBama</a>',
        '<a href="https://portal.gram.edu/" class="ua_brand-bar_link">Banner Web</a>',
        content
    )
    return content


def replace_favicons(content):
    """Replace UA favicons with Grambling's."""
    content = re.sub(
        r'<link\s+rel="icon"\s+href="https://assetfiles\.ua\.edu/brand/favicons/favicon\.ico"[^>]*>',
        '<link rel="icon" href="https://www.gram.edu/favicon.ico" sizes="32x32">',
        content
    )
    content = re.sub(
        r'\s*<link\s+rel="icon"\s+href="https://assetfiles\.ua\.edu/brand/favicons/icon\.svg"[^>]*>',
        '',
        content
    )
    content = re.sub(
        r'\s*<link\s+rel="apple-touch-icon"\s+href="https://assetfiles\.ua\.edu/brand/favicons/apple-touch-icon\.png"[^>]*>',
        '',
        content
    )
    content = re.sub(
        r'\s*<link\s+rel="manifest"\s+href="https://assetfiles\.ua\.edu/brand/favicons/manifest\.webmanifest"[^>]*>',
        '',
        content
    )
    return content


def replace_og_title(content):
    """Replace og:title meta tags that mention UA."""
    content = re.sub(
        r'(content="[^"]*)\bThe University of Alabama\b',
        r'\1Grambling State University',
        content
    )
    content = re.sub(
        r'(content="[^"]*)\bUniversity of Alabama\b',
        r'\1Grambling State University',
        content
    )
    return content


def replace_footer(content, filepath):
    """Replace UA System logo, Denny Chimes, brand footer logo, copyright, and legal links."""
    footer_logo_src = os.path.relpath(
        os.path.join(SITE_ROOT, GRAMBLING_FOOTER_LOGO_REL_PATH),
        os.path.dirname(filepath)
    ).replace("\\", "/")
    # Replace UA System link and logo
    content = re.sub(
        r'<a\s+href="https://uasystem\.edu/[^"]*"\s+target="_blank"\s+rel="noreferrer"\s+class="ua_site-footer_ua-system">\s*'
        r'<img\s+alt="[^"]*"\s+src="[^"]*UA_System\.svg[^"]*"\s*/?\s*>\s*'
        r'<span\s+class="ua_visually-hidden">[^<]*</span>\s*</a>',
        f'<a href="https://www.ulsystem.edu/" target="_blank" rel="noreferrer" class="ua_site-footer_ua-system">'
        f' <img alt="University of Louisiana System" src="{UL_SYSTEM_SVG}">'
        f' <span class="ua_visually-hidden">Part of the University of Louisiana System</span>'
        f' </a>',
        content,
        flags=re.DOTALL
    )
    # Remove Denny Chimes div
    content = re.sub(
        r'\s*<div\s+class="ua_site-footer_denny-chimes"\s+id="DennyChimes"></div>',
        '',
        content
    )
    # Replace brand footer logo
    content = re.sub(
        r'<img\s+src="[^"]*Capstone_A-White\.svg[^"]*"\s+alt="The University of Alabama Logo"\s*/?\s*>',
        f'<img src="{footer_logo_src}" alt="Grambling State University Logo" style="width:50px;height:50px;object-fit:contain;background:transparent;">',
        content
    )
    content = re.sub(
        r'<img\s+src="[^"]*"\s+alt="Grambling State University Logo"[^>]*>',
        f'<img src="{footer_logo_src}" alt="Grambling State University Logo" style="width:50px;height:50px;object-fit:contain;background:transparent;">',
        content
    )
    # Replace copyright block
    content = re.sub(
        r'<p>\s*<span>\s*<a\s+href="https://www\.ua\.edu/copyright">Copyright\s*&copy;\s*(\d+)</a>\s*'
        r'<a\s+href="https://www\.ua\.edu">\s*The University of Alabama</a>\s*</span>\s*'
        r'<span>\s*<a\s+href="tel:\+12053486010">\(205\)\s*348-6010</a>\s*</span>\s*'
        r'<span>\s*<a\s+href="https://www\.ua\.edu/contact">Contact UA</a>\s*</span>\s*</p>',
        r'<p>'
        r'<span><a href="https://www.gram.edu">Copyright &copy; \1 Grambling State University</a></span>'
        r' <span><a href="tel:+13182473811">(318) 247-3811</a></span>'
        r' <span><a href="https://www.gram.edu/contact">Contact GSU</a></span>'
        r'</p>',
        content,
        flags=re.DOTALL
    )
    # Replace legal links
    old_legal = re.compile(
        r'<nav\s+aria-label="Legal Links">\s*<ul\s+class="ua_brand-footer_link-list">.*?</ul>\s*</nav>',
        re.DOTALL
    )
    new_legal = '''<nav aria-label="Legal Links">
      <ul class="ua_brand-footer_link-list">
        <li><a href="https://www.gram.edu/compliance/">Compliance</a></li>
        <li><a href="https://www.gram.edu/administration/legal/consumer-information/">Consumer Information</a></li>
        <li><a href="https://www.gram.edu/contact">Contact Us</a></li>
        <li><a href="https://www.gram.edu/student-life/titleIX/">Title IX</a></li>
        <li><a href="https://www.gram.edu/equal-opportunity">Equal Opportunity</a></li>
      </ul>
    </nav>'''
    content = old_legal.sub(new_legal, content)
    return content


def replace_footer_student_life(content):
    """Replace Student Life footer section text and links."""
    content = re.sub(
        r'The Division of Student Life maximizes each UA student',
        'The Division of Student Affairs supports each GSU student',
        content
    )
    # Replace social media links
    content = re.sub(
        r'<a\s+href="https://%20https://www\.facebook\.com/BamaStudentLife"',
        '<a href="https://www.facebook.com/gramblingstateuniversity"',
        content
    )
    content = re.sub(
        r'<a\s+href="https://www\.facebook\.com/BamaStudentLife"',
        '<a href="https://www.facebook.com/gramblingstateuniversity"',
        content
    )
    content = re.sub(
        r'<a\s+href="https://instagram\.com/bamastudentlife/"',
        '<a href="https://www.instagram.com/grambling1901/"',
        content
    )
    content = re.sub(
        r'<a\s+href="https://www\.youtube\.com/user/bamastudentlife"',
        '<a href="https://www.youtube.com/@GramblingStateUniversity"',
        content
    )
    # Replace contact links
    content = re.sub(
        r'<a\s+href="https://sl\.ua\.edu/about/contact-us/"[^>]*>Contact Student Life</a>',
        '<a href="https://www.gram.edu/aboutus/administration/students/" target="_blank" rel="noreferrer noopener">Contact Student Affairs</a>',
        content
    )
    content = re.sub(
        r'<a\s+href="https://sl\.ua\.edu/about/contact-us/complaints-and-appeals/"[^>]*>Complaints and Appeals</a>',
        '<a href="https://www.gram.edu/aboutus/administration/students/" target="_blank" rel="noreferrer noopener">Student Affairs</a>',
        content
    )
    return content


def replace_text_references(content):
    """Replace UA text references with Grambling equivalents."""
    # Specific contextual replacements first (order matters)
    content = content.replace(
        "The University of Alabama and the Division of Student Life stand firmly against hazing",
        "Grambling State University and the Division of Student Affairs stand firmly against hazing"
    )
    content = content.replace(
        "Hazing is not a challenge unique to UA but is a common issue",
        "Hazing is not a challenge unique to GSU but is a common issue"
    )

    # Navigation link labels
    content = content.replace(">UA Hazing Policy</a>", ">GSU Hazing Policy</a>")
    content = content.replace(">UA Code of Student Conduct</a>", ">GSU Code of Student Conduct</a>")

    # Cookie banner privacy link
    content = re.sub(
        r'<a href="https://www\.ua\.edu/privacy">Privacy Statement</a>',
        '<a href="https://www.gram.edu/privacy">Privacy Statement</a>',
        content
    )

    # Generic text replacements (careful with order)
    content = content.replace(
        "The University of Alabama will maintain",
        "Grambling State University will maintain"
    )
    content = content.replace(
        "providing false information to UA officials",
        "providing false information to GSU officials"
    )

    # Replace standalone "The University of Alabama" in visible text (not in URLs or CSS class names)
    content = re.sub(
        r'(?<!ua\.)(?<!\.ua\.)(?<!//)The University of Alabama(?! System)',
        'Grambling State University',
        content
    )

    # "University of Alabama" without "The" (not in URLs or class names)
    content = re.sub(
        r'(?<!["/])(?<!ua\.)University of Alabama(?! System)',
        'Grambling State University',
        content
    )

    # Anonymous reporting through UAct section
    content = content.replace("Anonymous Reporting through UAct", "Anonymous Reporting")
    content = content.replace(
        "Text UAct",
        "Report Hazing"
    )
    content = content.replace(
        "Use the QR code to submit an anonymous report of hazing to UAct, or learn more about additional reporting options.",
        "Submit an anonymous report of hazing, or learn more about additional reporting options."
    )

    # Page-specific replacements
    content = re.sub(
        r'alt="The Grambling State University Logo"',
        'alt="Grambling State University Logo"',
        content
    )

    # Standalone "UA" (University of Alabama abbreviation) -> "GSU"
    # Word boundary avoids UA_ ids (e.g. UA_TitleSearch), lowercase ua_ classes, and words like "UAL".
    content = re.sub(r"\bUA\b", "GSU", content)

    return content


def replace_gram_external_links(content):
    """Keep Gram.edu footer / Student Life links on current official URLs."""
    content = content.replace(
        "https://www.gram.edu/student-affairs/contact",
        "https://www.gram.edu/aboutus/administration/students/",
    )
    content = content.replace(
        "https://www.gram.edu/student-affairs/",
        "https://www.gram.edu/aboutus/administration/students/",
    )
    content = content.replace(
        "https://www.gram.edu/titleix",
        "https://www.gram.edu/student-life/titleIX/",
    )
    return content


def replace_title_tags(content):
    """Update <title> and other head-level text."""
    # Add Grambling to page titles
    content = re.sub(
        r'(content="[^"]*End Hazing) \| The University of Alabama"',
        r'\1 | Grambling State University"',
        content
    )
    return content


def process_file(filepath):
    """Apply all rebranding transformations to a single HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    content = inject_css(content)
    content = replace_brand_bar(content)
    content = replace_favicons(content)
    content = replace_og_title(content)
    content = replace_footer(content, filepath)
    content = replace_footer_student_life(content)
    content = replace_gram_external_links(content)
    content = replace_text_references(content)
    content = replace_title_tags(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to process")

    modified = 0
    for filepath in html_files:
        rel = os.path.relpath(filepath, SITE_ROOT)
        changed = process_file(filepath)
        status = "MODIFIED" if changed else "unchanged"
        print(f"  [{status}] {rel}")
        if changed:
            modified += 1

    print(f"\nDone. Modified {modified}/{len(html_files)} files.")

    # Run a quick audit for any remaining UA references
    print("\n--- AUDIT: Checking for remaining 'University of Alabama' references ---")
    remaining = 0
    for filepath in html_files:
        rel = os.path.relpath(filepath, SITE_ROOT)
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        # Check for remaining UA references in visible content (skip URLs, CSS, JS, asset paths)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if 'University of Alabama' in stripped:
                if 'ua.edu' in stripped or 'assetfiles' in stripped or 'sourceURL=' in stripped:
                    continue
                if 'UA_System' in stripped or 'class="ua_' in stripped or 'id="ua_' in stripped:
                    continue
                print(f"  REMAINING: {rel}:{i}: ...{stripped[:120]}...")
                remaining += 1

    if remaining == 0:
        print("  No remaining 'University of Alabama' references found in visible content!")
    else:
        print(f"  Found {remaining} remaining reference(s) to review.")


if __name__ == "__main__":
    main()
