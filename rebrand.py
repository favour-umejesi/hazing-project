#!/usr/bin/env python3
"""Rebrand the cloned End Hazing site from University of Alabama to Grambling State University."""

import os
import re
import glob

SITE_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cloned_site", "endhazing.sl.ua.edu"
)

# Pantone 124 C — official GSU gold (see grambling_marks licensing art sheet)
GSU_GOLD = "#ECAA00"

# Headings match www.gram.edu (Signika); body uses Times New Roman (Minion Pro fallback per identity sheet)
GRAMBLING_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Signika:wght@400;700&display=swap" rel="stylesheet">'''

GRAMBLING_CSS = f'''<style id="grambling-overrides">
:root {{
  /* Grambling State University brand colors (PMS 124 C gold, Process Black C) */
  --gsu-gold: {GSU_GOLD};
  --gsu-gold-rgb: 236, 170, 0;
  --gsu-black: #000000;
  --gsu-white: #ffffff;
  --gsu-gray-dark: #1a1a1a;
  --ua_color-link: var(--gsu-gold) !important;
  --ua_color-link--inverse: var(--gsu-black) !important;
  /* Headings: Signika (www.gram.edu); body: Times New Roman (identity sheet fallback) */
  --ua_font--heading: "Signika", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --ua_font--body: "Times New Roman", Times, serif;
  --ua_font--accent: "Signika", "Helvetica Neue", Helvetica, Arial, sans-serif;
}}
.ua_minerva,
.ua_minerva body,
.ua_minerva .ua_page_content,
.ua_minerva p,
.ua_minerva li,
.ua_minerva .wp-block-paragraph {{
  font-family: var(--ua_font--body);
  font-weight: 400;
  line-height: 1.42857143;
}}
.ua_minerva h1,
.ua_minerva h2,
.ua_minerva h3,
.ua_minerva h4,
.ua_minerva h5,
.ua_minerva h6,
.ua_minerva .wp-block-heading,
.ua_minerva .ua_page_title {{
  font-family: var(--ua_font--heading);
  font-weight: 400;
  line-height: 1.1;
}}
.ua_minerva .ua_title-bar_name {{
  font-family: var(--ua_font--heading);
  font-weight: 700;
}}
.ua_minerva .ua_primary-navigation a {{
  font-family: var(--ua_font--heading);
  font-weight: 400;
}}
.ua_brand-bar {{
  background-color: var(--gsu-black) !important;
}}
.ua_title-bar {{
  background-color: var(--gsu-gold) !important;
}}
.ua_title-bar_name,
.ua_title-bar a {{
  color: var(--gsu-black) !important;
}}
.ua_title-bar_expander {{
  color: var(--gsu-black) !important;
}}
.ua_primary-navigation {{
  background-color: var(--gsu-black) !important;
}}
.ua_primary-navigation a {{
  color: var(--gsu-white) !important;
}}
.ua_primary-navigation ul ul {{
  background-color: var(--gsu-gray-dark) !important;
}}
.ua_primary-navigation ul ul a {{
  color: var(--gsu-gold) !important;
}}
.ua_primary-navigation ul ul a:hover {{
  color: var(--gsu-white) !important;
  background-color: #333333 !important;
}}
.ua_primary-navigation li {{
  border-color: #333333 !important;
}}
.ua_primary-navigation button {{
  color: var(--gsu-gold) !important;
}}
:root :where(.wp-element-button, .wp-block-button__link) {{
  background-color: var(--gsu-black) !important;
  color: var(--gsu-gold) !important;
  border-color: var(--gsu-gold) !important;
}}
:root :where(.wp-element-button:hover, .wp-block-button__link:hover) {{
  background-color: var(--gsu-gold) !important;
  color: var(--gsu-black) !important;
  border-color: var(--gsu-black) !important;
}}
.ua_link-list_item {{
  background-color: var(--gsu-black) !important;
  color: var(--gsu-gold) !important;
}}
.ua_link-list_item:hover {{
  background-color: var(--gsu-gold) !important;
  color: var(--gsu-black) !important;
}}
.ua_site-footer {{
  background-color: var(--gsu-gray-dark) !important;
  color: var(--gsu-white) !important;
}}
.ua_site-footer h2,
.ua_site-footer h3,
.ua_site-footer h4 {{
  color: var(--gsu-gold) !important;
}}
.ua_site-footer p,
.ua_site-footer li:not(.wp-social-link):not(.wp-block-social-link),
.ua_site-footer span,
.ua_site-footer div {{
  color: var(--gsu-white) !important;
}}
.ua_site-footer a:where(:not(.wp-element-button)) {{
  color: var(--gsu-gold) !important;
}}
.ua_minerva .ua_site-footer .wp-block-social-links .wp-social-link,
.ua_minerva .ua_site-footer .wp-block-social-links .wp-block-social-link {{
  background: transparent !important;
  background-color: transparent !important;
  color: var(--gsu-gold) !important;
}}
.ua_minerva .ua_site-footer .wp-block-social-links .wp-social-link a,
.ua_minerva .ua_site-footer .wp-block-social-link-anchor {{
  background: transparent !important;
  background-color: transparent !important;
  color: var(--gsu-gold) !important;
}}
.ua_minerva .ua_site-footer .wp-block-social-links svg,
.ua_minerva .ua_site-footer .wp-block-social-link-anchor svg {{
  fill: var(--gsu-gold) !important;
  color: var(--gsu-gold) !important;
}}
.ua_brand-footer {{
  background-color: var(--gsu-black) !important;
}}
.ua_brand-footer a {{
  color: var(--gsu-gold) !important;
}}
.ua_brand-footer p,
.ua_brand-footer span {{
  color: var(--gsu-white) !important;
}}
a:where(:not(.wp-element-button)) {{
  color: var(--gsu-gold);
}}
.ua_page_title {{
  color: var(--gsu-black);
}}
.is-style-elevated {{
  border-top: 4px solid var(--gsu-gold);
}}
.sl-QueryLoop.is-style-elevated {{
  border-top: 4px solid var(--gsu-gold);
}}
.sl-QueryLoop.is-style-elevated:hover {{
  border-top-color: var(--gsu-black);
}}
.ua_title-bar_search button {{
  background-color: var(--gsu-black) !important;
  color: var(--gsu-gold) !important;
}}
.ua_card {{
  border-color: var(--gsu-gold) !important;
}}
.wp-block-button__link.wp-element-button {{
  border: 2px solid var(--gsu-gold) !important;
}}
.ua_cookie-banner__container .ua_cookie-banner__content button {{
  background-color: var(--gsu-gold) !important;
  color: var(--gsu-black) !important;
}}
/* Home page user-journey section */
.gram-journey {{
  background: var(--gsu-gray-dark);
  color: var(--gsu-white);
  padding: var(--wp--preset--spacing--flow-double, 3rem) var(--wp--preset--spacing--flow, 1.5rem);
  margin-top: var(--wp--preset--spacing--flow-double, 3rem);
  margin-bottom: var(--wp--preset--spacing--flow, 1.5rem);
}}
.gram-journey__heading {{
  text-align: center;
  color: var(--gsu-gold);
  margin-bottom: 0.5rem;
}}
.gram-journey__intro {{
  text-align: center;
  max-width: 42rem;
  margin: 0 auto 2rem;
}}
.gram-journey__grid {{
  display: grid;
  gap: 1rem;
  max-width: 72rem;
  margin: 0 auto;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}}
.gram-journey__card {{
  background: var(--gsu-black);
  border-top: 4px solid var(--gsu-gold);
  padding: 1.25rem;
}}
.gram-journey__card h3 {{
  color: var(--gsu-gold);
  font-size: 1.1rem;
  margin: 0 0 0.5rem;
}}
.gram-journey__card p {{
  font-size: 0.95rem;
  margin: 0 0 0.75rem;
  line-height: 1.45;
}}
.gram-journey__card a {{
  color: var(--gsu-gold);
  font-weight: 600;
  text-decoration: underline;
}}
/* Home — Anonymous Reporting (tighter section spacing; keep full QR size) */
.gram-anonymous-reporting {{
  padding-block: var(--wp--preset--spacing--50, 1.5rem);
  margin-block: 0;
}}
.gram-anonymous-reporting + .wp-block-group.is-style-elevated {{
  margin-block-start: var(--wp--preset--spacing--50, 1.5rem) !important;
  padding-top: var(--wp--preset--spacing--flow, 1.5rem);
}}
.gram-anonymous-reporting.is-layout-constrained > * {{
  margin-block-start: 0.5rem;
}}
.gram-anonymous-reporting.is-layout-constrained > :first-child {{
  margin-block-start: 0;
}}
.gram-anonymous-reporting .wp-block-media-text {{
  margin-block: 0;
}}
.gram-anonymous-reporting .wp-block-media-text__media,
.gram-anonymous-reporting .wp-block-media-text__content {{
  align-self: start;
}}
.gram-anonymous-reporting .wp-block-media-text__media img {{
  width: 100%;
  max-width: 400px;
  height: auto;
}}
.gram-anonymous-reporting .wp-block-media-text__content {{
  padding-block: 0;
}}
.gram-anonymous-reporting .wp-block-media-text__content.is-layout-flow > * {{
  margin-block-start: 1rem;
}}
.gram-anonymous-reporting .wp-block-media-text__content.is-layout-flow > :first-child {{
  margin-block-start: 0;
}}
/* Alternate Activities — semi-transparent disclosure panels (How to Prevent) */
#activities .wp-block-cover__inner-container {{
  color: #ffffff;
}}
#activities .gram-alt-activities {{
  width: 100%;
  max-width: 40rem;
  margin: 1.25rem auto 0;
  text-align: left;
}}
#activities .gram-alt-activities details {{
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(0, 0, 0, 0.5);
  margin-top: 0.65rem;
}}
#activities .gram-alt-activities summary {{
  cursor: pointer;
  list-style: none;
  padding: 0.9rem 1rem;
  font-family: var(--ua_font--heading);
  font-weight: 700;
  font-size: 1.0625rem;
  color: #ffffff;
  letter-spacing: -0.02em;
}}
#activities .gram-alt-activities summary::-webkit-details-marker {{
  display: none;
}}
#activities .gram-alt-activities details[open] summary {{
  border-bottom: 1px solid rgba(255, 255, 255, 0.28);
}}
#activities .gram-alt-activities .gram-alt-panel {{
  padding: 0.85rem 1rem 1.1rem;
  color: #e8e9eb;
  font-size: 0.95rem;
  line-height: 1.55;
}}
#activities .gram-alt-activities .gram-alt-panel a {{
  color: var(--gsu-gold) !important;
  text-decoration: underline;
}}
#activities .gram-alt-activities .gram-alt-panel a:hover,
#activities .gram-alt-activities .gram-alt-panel a:focus {{
  color: #ffffff !important;
}}
#activities .gram-alt-activities ul {{
  margin: 0.4rem 0 0;
  padding-left: 1.2rem;
}}
#activities .gram-alt-activities li {{
  margin-top: 0.35rem;
}}
</style>'''

GRAMBLING_LOGO_SVG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 450 25'%3E%3Ctext x='0' y='19' fill='white' font-family='Georgia,serif' font-size='16' font-weight='bold' letter-spacing='2.5'%3EGRAMBLING STATE UNIVERSITY%3C/text%3E%3C/svg%3E"

GRAMBLING_FOOTER_LOGO_REL_PATH = "wp-content/uploads/sites/11/grambling-assets/gsu-g-logo.png"

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
    """Inject or refresh Grambling CSS overrides before </head>."""
    if 'id="grambling-overrides"' in content:
        return re.sub(
            r'<style id="grambling-overrides">[\s\S]*?</style>',
            GRAMBLING_CSS.strip(),
            content,
            count=1,
        )
    return content.replace("</head>", GRAMBLING_CSS + "\n</head>", 1)


def inject_fonts(content):
    """Load Signika for headings (gram.edu). Body uses system Times New Roman."""
    font_block = GRAMBLING_FONTS.strip() + "\n"
    content = re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*'
        r'(?:<link href="https://fonts\.googleapis\.com/[^"]+" rel="stylesheet">\s*)+',
        font_block,
        content,
        count=1,
    )
    if "family=Signika" not in content:
        return content.replace("</head>", GRAMBLING_FONTS + "\n</head>", 1)
    return content


def nav_prefix_from_block(block: str) -> str:
    """Relative path prefix for links in a primary-nav tail section."""
    for pattern in (
        r'<a href="((?:\.\./|(?:\./)+)*)parents-and-family/">',
        r'<a href="((?:\.\./|(?:\./)+)*)report-it/campus-support-services/">',
        r'<a href="((?:\.\./|(?:\./)+)*)report-it/">',
        r'<a href="((?:\.\./|(?:\./)+)*)hazing-prevention-team/">',
    ):
        m = re.search(pattern, block)
        if m:
            return m.group(1)
    return ""


def normalize_primary_nav_tail(content: str) -> str:
    """Rebuild reporting, student support, family, and community commitment nav items."""
    pat = re.compile(
        r'(?:<li class="ua_menu-item-parent"><a href="[^"]*">Reporting Concerns</a>[\s\S]*?'
        r'|<li><a href="[^"]*">Reporting Concerns</a></li>\s*)'
        r'[\s\S]*?(?=</ul>\s*</nav>)',
        re.I,
    )

    def repl(m: re.Match[str]) -> str:
        prefix = nav_prefix_from_block(m.group(0))
        return (
            f'<li><a href="{prefix}report-it/">Reporting Concerns</a></li>\n'
            f'<li><a href="{prefix}report-it/campus-support-services/">'
            f"Student Support Resources</a></li>\n"
            f'<li><a href="{prefix}parents-and-family/">Family Engagement</a></li>\n'
            f"{community_commitment_nav_block(prefix)}\n"
        )

    return pat.sub(repl, content, count=1)


def community_commitment_nav_block(prefix: str) -> str:
    """Single Community Commitment dropdown for the primary nav."""
    return (
        f'<li class="ua_menu-item-parent"><a href="{prefix}hazing-prevention-team/">Community Commitment</a>'
        f'<button><span class="ua_primary-navigation_inactive_content">'
        f'<span class="fa fa-caret-down" title="Expand Community Commitment menu" aria-hidden="true"></span>'
        f'<span class="ua_visually-hidden">Expand Community Commitment menu</span></span>'
        f'<span class="ua_primary-navigation_active_content">'
        f'<span class="fa fa-caret-up" title="Close Community Commitment menu" aria-hidden="true"></span>'
        f'<span class="ua_visually-hidden">Close Community Commitment menu</span></span></button>'
        f'<ul><li><a href="{prefix}hazing-prevention-team/">Prevention Team</a></li>'
        f'<li><a href="{prefix}hazing-transparency-report/">Transparency Report</a></li></ul></li>'
    )


def normalize_community_commitment_nav(content: str) -> str:
    """Deprecated: use normalize_primary_nav_tail. Kept as alias for clarity."""
    return normalize_primary_nav_tail(content)


def replace_navigation(content):
    """Rename nav labels and restructure menu to match recommended user journey."""
    label_map = [
        (">About</a>", ">Our Commitment</a>"),
        (">What is Hazing</a>", ">Understanding Hazing</a>"),
        (">Prevent It</a>", ">Prevention &amp; Education</a>"),
        (">Report It</a>", ">Reporting Concerns</a>"),
        (">Campus Support Services</a>", ">Student Support Resources</a>"),
        (">Parents and Family</a>", ">Family Engagement</a>"),
        (">Hazing Transparency Report</a>", ">Transparency Report</a>"),
        ("Expand About menu", "Expand Our Commitment menu"),
        ("Close About menu", "Close Our Commitment menu"),
        ("Expand What is Hazing menu", "Expand Understanding Hazing menu"),
        ("Close What is Hazing menu", "Close Understanding Hazing menu"),
        ("Expand Prevent It menu", "Expand Prevention & Education menu"),
        ("Close Prevent It menu", "Close Prevention & Education menu"),
        ("Expand Report It menu", "Expand Reporting Concerns menu"),
        ("Close Report It menu", "Close Reporting Concerns menu"),
    ]
    for old, new in label_map:
        content = content.replace(old, new)

    content = re.sub(
        r'\s*<li><a href="[^"]*hazing-prevention-team/">Hazing Prevention Team</a></li>',
        "",
        content,
    )

    return normalize_primary_nav_tail(content)


def replace_culture_messaging(content):
    """Shift tone from compliance-only to values and campus culture."""
    replacements = [
        (
            "Join the effort to end hazing",
            "Building a campus culture of respect and leadership",
        ),
        (
            "Grambling State University and the Division of Student Affairs stand firmly against hazing and are committed to providing information and resources to help students end hazing for good. Hazing is not a challenge unique to GSU but is a common issue in student organizations across the nation. Find information on what counts as hazing, myths surrounding it, ways to prevent it and where victims of hazing can find support on campus.",
            "At Grambling State University, ending hazing is part of our commitment to leadership development, student success, and community responsibility. We promote a campus where every student belongs, grows, and leads with integrity — while providing clear policies, education, and support when concerns arise.",
        ),
        (
            "Grambling State University is committed to maintaining a supportive, educational environment that seeks to enhance the well-being of all members of its community. Hazing is a crime under Louisiana law and",
            "Grambling State University is committed to a campus culture rooted in leadership, mutual respect, and student success. Ending hazing strengthens that culture for every member of our community. Hazing is a crime under Louisiana law and",
        ),
        (
            "This website is a resource to combat hazing by, among other things, providing education and empowering victims and bystanders. For more information about reporting concerns about hazing, please visit the",
            "This site helps you understand what GSU promotes — belonging, accountability, and care for one another — as well as what we prohibit. You will find education, prevention tools, and support resources here. To report a concern, visit the",
        ),
        (
            "Thank you for working to make our community at Grambling State University hazing-free.",
            "Thank you for helping Grambling State live out our promise: where everybody is somebody.",
        ),
        (
            ">About | End Hazing</title>",
            ">Our Commitment | End Hazing</title>",
        ),
        (
            'wp-block-post-title">About</h1>',
            'wp-block-post-title">Our Commitment</h1>',
        ),
        (
            "Student Life houses whole-person recovery services for hazing victims.",
            "Student Affairs connects students with whole-person support and recovery resources.",
        ),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content


def replace_photography(content):
    """Swap dated or off-brand imagery; broaden alt text away from narrow org framing."""
    content = re.sub(
        r'((?:\.\./)*)wp-content/uploads/sites/11/2024/08/Bryce-Main[^"]*',
        r"\1wp-content/uploads/sites/11/2025/gsu-life/gsu-students-walking.png",
        content,
    )
    content = content.replace('alt="Campus building"', 'alt="Grambling State University students on campus"')
    greek_alt = (
        "Students gathered outdoors on the Grambling State University campus, "
        "representing community and student life"
    )
    content = re.sub(
        r'aria-label="[^"]*Greek-letter organization[^"]*"',
        f'aria-label="{greek_alt}"',
        content,
    )
    content = re.sub(
        r'alt="[^"]*Greek-letter organization[^"]*"',
        f'alt="{greek_alt}"',
        content,
    )
    content = re.sub(
        r'background-image:url\(([^)]*?)gsu-place-and-family\.png[^)]*\)',
        r"background-image:url(\1gsu-students-walking.png)",
        content,
    )
    return content


JOURNEY_SECTION = re.compile(
    r'<section class="gram-journey alignfull"[\s\S]*?</section>\s*',
    re.I,
)


def journey_section_html(prefix: str = "") -> str:
    return f'''
<section class="gram-journey alignfull" aria-labelledby="gram-journey-heading">
<h2 id="gram-journey-heading" class="gram-journey__heading wp-block-heading has-text-align-center">Explore End Hazing at GSU</h2>
<p class="gram-journey__intro">Move through the site by what you need — from our shared values to reporting and support.</p>
<div class="gram-journey__grid">
<article class="gram-journey__card"><h3>Our Commitment</h3><p>How GSU connects anti-hazing work to leadership and student success.</p><a href="{prefix}about/">Learn our commitment</a></article>
<article class="gram-journey__card"><h3>Understanding Hazing</h3><p>Definitions, statistics, policies, and FAQs.</p><a href="{prefix}what-is-hazing/">Understand hazing</a></article>
<article class="gram-journey__card"><h3>Prevention &amp; Education</h3><p>Practical steps and the Hazing Prevention Team.</p><a href="{prefix}prevent-it/">Prevent hazing</a></article>
<article class="gram-journey__card"><h3>Reporting Concerns</h3><p>Anonymous and direct reporting options.</p><a href="{prefix}report-it/">Report a concern</a></article>
<article class="gram-journey__card"><h3>Student Support Resources</h3><p>Campus offices ready to help.</p><a href="{prefix}report-it/campus-support-services/">Find support</a></article>
<article class="gram-journey__card"><h3>Family Engagement</h3><p>Guidance for parents and families.</p><a href="{prefix}parents-and-family/">Support your student</a></article>
<article class="gram-journey__card"><h3>Community Commitment</h3><p>Prevention team and transparency reporting.</p><a href="{prefix}hazing-prevention-team/">See our commitment</a></article>
</div>
</section>
'''


def inject_journey_section(content, rel_path: str):
    """Add a single guided journey block on the home page (dedupe if repeated)."""
    if rel_path not in ("index.html",):
        return content

    content = JOURNEY_SECTION.sub("", content)

    marker = '<div class="entry-content is-layout-flow wp-block-post-content'
    journey = journey_section_html()
    if marker in content:
        return content.replace(marker, journey + marker, 1)
    return content


def tag_home_anonymous_reporting(content, rel_path: str):
    """Mark the home Anonymous Reporting block for compact layout styles."""
    if rel_path != "index.html":
        return content
    if "gram-anonymous-reporting" in content:
        return content
    return content.replace(
        'wp-block-group-is-layout-constrained">\n<h2 class="wp-block-heading has-text-align-center">Anonymous Reporting</h2>',
        'wp-block-group-is-layout-constrained gram-anonymous-reporting">\n<h2 class="wp-block-heading has-text-align-center">Anonymous Reporting</h2>',
        1,
    )


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
        r' <span><a href="https://www.gram.edu/aboutus/contact/">Contact GSU</a></span>'
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
        <li><a href="https://www.gram.edu/aboutus/contact/">Contact Us</a></li>
        <li><a href="https://www.gram.edu/student-life/titleIX/">Title IX</a></li>
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
        "https://www.gram.edu/contact",
        "https://www.gram.edu/aboutus/contact/",
    )
    content = re.sub(
        r'<li>\s*<a href="https://www\.gram\.edu/compliance/">Compliance</a>\s*</li>\s*',
        "",
        content,
    )
    content = re.sub(
        r'<li>\s*<a href="https://www\.gram\.edu/equal-opportunity">Equal Opportunity</a>\s*</li>\s*',
        "",
        content,
    )
    content = re.sub(
        r'<li>\s*<a href="https://www\.gram\.edu/administration/legal/consumer-information/">Consumer Information</a>\s*</li>\s*',
        "",
        content,
    )
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


    return content


def clean_transparency_navigation(content: str, rel: str) -> str:
    """Remove category footers and archive sidebars that expose old UA violation posts."""
    content = re.sub(
        r'<div class="is-layout-flex">\s*'
        r'<div class="ua_post-metadata_categories">[\s\S]*?</div>\s*'
        r"</div>\s*",
        "",
        content,
    )

    if rel.startswith("posts/category/"):
        content = re.sub(
            r'<div class="ua_page_sidebar ua_layout--flow ua_layout--standard">\s*'
            r'<div class="ua_archive_tag-list[^"]*">[\s\S]*?</ul>\s*</div>\s*'
            r"</div>\s*",
            "",
            content,
        )
        content = re.sub(
            r'<div class="wp-block-archives-dropdown wp-block-archives">[\s\S]*?</script>\s*</div>\s*',
            "",
            content,
        )

    return content


def fix_stale_violations_links(content: str) -> str:
    """Point legacy violations URLs at the Grambling transparency report."""
    return re.sub(
        r'href="((?:\.\./)*)violations/"',
        r'href="\1hazing-transparency-report/"',
        content,
    )


def redirect_violations_page(content: str, rel: str) -> str:
    """Send /violations/ visitors to the canonical transparency report."""
    if rel != "violations/index.html":
        return content
    if 'http-equiv="refresh"' in content:
        return content
    redirect = (
        '<meta http-equiv="refresh" content="0; url=../hazing-transparency-report/">'
    )
    return content.replace("<head>", f"<head>\n{redirect}", 1)


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
    rel = os.path.relpath(filepath, SITE_ROOT).replace("\\", "/")

    content = inject_fonts(content)
    content = inject_css(content)
    content = replace_brand_bar(content)
    content = replace_favicons(content)
    content = replace_og_title(content)
    content = replace_footer(content, filepath)
    content = replace_footer_student_life(content)
    content = replace_gram_external_links(content)
    content = replace_text_references(content)
    content = replace_title_tags(content)
    content = replace_navigation(content)
    content = replace_culture_messaging(content)
    content = replace_photography(content)
    content = inject_journey_section(content, rel)
    content = tag_home_anonymous_reporting(content, rel)
    content = clean_transparency_navigation(content, rel)
    content = fix_stale_violations_links(content)
    content = redirect_violations_page(content, rel)

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
