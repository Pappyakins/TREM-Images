"""Build a personalized celebration card: person's photo (from the sheet's
Image/Image_wed link) with their name overlaid, plus the real TREM logo.

Usage:
    python3 make_card.py <image_url_or_path> "<Name>" <birthday|wedding> <out_path>
"""
import sys, os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "assets", "trem_logo.png")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
# Beautiful display fonts for the celebrant's name (downloaded 2026-09-27)
FONTS_DIR = os.path.join(BASE, "assets", "fonts")
NAME_FONT_SCRIPT = os.path.join(FONTS_DIR, "GreatVibes-Regular.ttf")
NAME_FONT_SERIF = os.path.join(FONTS_DIR, "CormorantGaramond-Bold.ttf")
NAME_FONT_DISPLAY = os.path.join(FONTS_DIR, "PlayfairDisplay-Bold.ttf")
# Default name font — Allura (elegant script, Pappy's pick 2026-09-27).
# Change to NAME_FONT_SCRIPT for Great Vibes, NAME_FONT_SERIF for Cormorant,
# or NAME_FONT_DISPLAY for Playfair.
NAME_FONT = os.path.join(FONTS_DIR, "Allura-Regular.ttf")
# Stroke emboldens single-weight scripts like Allura (it has no true bold).
NAME_STROKE = 0

NAVY = (22, 30, 54)
GOLD = (232, 197, 92)
WHITE = (255, 255, 255)


def load_image(src):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            tmp = "/tmp/_card_src"
            with open(tmp, "wb") as f:
                f.write(r.read())
        return Image.open(tmp).convert("RGB")
    return Image.open(src).convert("RGB")


def tracked(draw, cx, y, text, font, fill, tracking=10, stroke_width=0):
    ws = [draw.textlength(ch, font=font) for ch in text]
    total = sum(ws) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, ws):
        if stroke_width:
            draw.text((x, y), ch, font=font, fill=fill,
                      stroke_width=stroke_width, stroke_fill=fill)
        else:
            draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


def fit_font(draw, text, path, start, tracking, max_w):
    size = start
    while size > 12:
        f = ImageFont.truetype(path, size)
        ws = [draw.textlength(ch, font=f) for ch in text]
        if sum(ws) + tracking * (len(text) - 1) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, 12)


def make_card(src, name, occasion, out_path):
    im = load_image(src)
    W, H = im.size

    # Work on a copy; add a bottom gradient band for the name.
    # The source art already carries its own "HAPPY BIRTHDAY / FROM TREM TORONTO"
    # wording, so our band sits low and clear of it.
    card = im.copy()
    band_h = int(H * 0.16)
    overlay = Image.new("L", (1, band_h), 0)
    px = overlay.load()
    for y in range(band_h):
        px[0, y] = int(235 * (y / band_h) ** 1.6)
    overlay = overlay.resize((W, band_h)).filter(ImageFilter.GaussianBlur(8))
    navy = Image.new("RGB", (W, band_h), NAVY)
    card.paste(navy, (0, H - band_h), overlay)
    # thin gold rule above the band
    d = ImageDraw.Draw(card)
    d.rectangle([0, H - band_h, W, H - band_h + 4], fill=GOLD)

    cx = W / 2
    band_top = H - band_h

    # Name plate only — the artwork already says "Happy Birthday / Anniversary",
    # so we keep the band clean and center the name in it.
    name_font = NAME_FONT if os.path.exists(NAME_FONT) else SERIF_B
    # Script fonts read small: bump the size for them.
    _scripts = ("vibes", "allura", "parisienne", "alexbrush", "pinyonscript",
                "script", "tangerine", "sacramento", "arizonia")
    size_boost = 1.45 if any(s in os.path.basename(name_font).lower()
                             for s in _scripts) else 1.0
    fn = fit_font(d, name, name_font, int(W * 0.062 * size_boost), int(W * 0.003), W * 0.86)
    bbox = d.textbbox((0, 0), name, font=fn)
    th = bbox[3] - bbox[1]
    y1 = band_top + (band_h - th) / 2 - bbox[1]
    tracked(d, cx, y1, name, fn, WHITE, tracking=int(W * 0.003),
            stroke_width=NAME_STROKE)

    # small TREM logo badge, top-right corner (clear of the name)
    try:
        logo = Image.open(LOGO).convert("RGBA")
        lw = int(W * 0.075)
        lh = int(lw * logo.size[1] / logo.size[0])
        logo = logo.resize((lw, lh), Image.LANCZOS)
        card.paste(logo, (W - lw - int(W * 0.025), int(H * 0.03)), logo)
    except Exception as e:
        print("logo skipped:", e)

    card.save(out_path, quality=92)
    print("saved", out_path, card.size)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    make_card(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
