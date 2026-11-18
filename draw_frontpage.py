#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024) as entry.png.

Layout: navy masthead naming the day, a generated editorial illustration
(hero.png, no text in it), four main stories in a 2x2 grid, a briefs band
and a footer. Every headline and summary below was checked against news
reports dated Wednesday 18 November 2026 before this script was written.
Only the Python standard library and Pillow are used; the output is
deterministic (same bytes on every run).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (251, 246, 236)
NAVY = (14, 42, 71)
NAVY_DARK = (10, 32, 56)
GOLD = (201, 148, 44)
RED = (180, 35, 24)
INK = (26, 26, 26)
GREY = (90, 90, 88)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "noto", "NotoSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "noto", "NotoSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "noto", "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


STORIES = [
    (
        "ASIA  ·  DIPLOMACY",
        "Quad leaders meet in Manila",
        "Trump joins the Quad to launch maritime, "
        "AI and cyber initiatives.",
    ),
    (
        "MIDDLE EAST",
        "Iran hits US radar base in Bahrain",
        "The IRGC claims a drone strike on Sheikh Isa Air Base, "
        "the third attack in five days.",
    ),
    (
        "EUROPE  ·  WAR",
        "Ukraine strikes the Crimea bridge",
        "Kyiv hits the Kerch bridge as Russia pounds "
        "Kyiv's bridges.",
    ),
    (
        "BUSINESS  ·  TECH",
        "Nvidia beats estimates",
        "First earnings without Jensen Huang; the board rules out "
        "the ex-CEO's return.",
    ),
]

BRIEFS = [
    "US loses measles-free status",
    "Russian plane crash in Siberia kills 19",
    "Dhoni retires from IPL, to mentor Chennai",
    "Cyclone Akvan nears India's east coast",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 160], fill=NAVY)
    title_f = font(SANS_BOLD, 27)
    title = "T H E   W O R L D   I N   O N E   D A Y"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 24), title, font=title_f, fill=GOLD)
    date_f = font(SERIF_BOLD, 56)
    date = "Wednesday, 18 November 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 66), date, font=date_f, fill=WHITE)
    d.rectangle([0, 160, W, 166], fill=GOLD)

    # --- Hero illustration (centre-cropped to the strip) ---------------
    hero = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    strip_h = 246
    top = (hero.height - strip_h) // 2
    hero = hero.crop((0, top, W, top + strip_h))
    img.paste(hero, (0, 172))
    d.rectangle([0, 172, W, 174], fill=GOLD)
    d.rectangle([0, 416, W, 418], fill=GOLD)

    # --- Four main stories, 2x2 grid ----------------------------------
    margin, gutter = 36, 28
    col_w = (W - 2 * margin - gutter) // 2
    grid_top, row_h, row_gap = 438, 216, 14
    kick_f = font(SANS_BOLD, 21)
    head_f = font(SANS_BOLD, 36)
    sum_f = font(SANS, 24)
    for i, (kicker, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (col_w + gutter)
        y = grid_top + row * (row_h + row_gap)
        d.rectangle([x, y, x + col_w, y + 3], fill=GOLD)
        d.text((x, y + 12), kicker, font=kick_f, fill=RED)
        head_lines = wrap(d, headline, head_f, col_w)
        hy = y + 42
        for line in head_lines:
            d.text((x, hy), line, font=head_f, fill=INK)
            hy += 44
        sum_lines = wrap(d, summary, sum_f, col_w)
        sy = hy + 6
        for line in sum_lines:
            d.text((x, sy), line, font=sum_f, fill=(58, 58, 58))
            sy += 30

    # --- Briefs band ----------------------------------------------------
    band_y = 886
    d.rectangle([0, band_y, W, 976], fill=NAVY)
    brief_title_f = font(SANS_BOLD, 21)
    d.text((margin, band_y + 8), "ALSO ON 18 NOVEMBER",
           font=brief_title_f, fill=GOLD)
    brief_f = font(SANS, 20)
    for i, brief in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = margin + col * (col_w + gutter)
        y = band_y + 36 + row * 25
        d.text((x, y), "—  " + brief, font=brief_f, fill=WHITE)

    # --- Footer ---------------------------------------------------------
    foot_f = font(SANS, 19)
    foot = "Events reported on Wednesday, 18 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 986), foot, font=foot_f, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
