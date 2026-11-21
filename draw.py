#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws one uncaptioned open passport spread (1024x1024) for the invented
island republic of Solmara, capital Meridia, and writes it to
/output/entry.png (or $OUTPUT_PATH).

Drawn in code with PIL; the holder's ID photograph (a generated
portrait asset shipped beside this script) is pasted into its frame.
No network, no clock, no randomness -- the output is deterministic.

Country: REPUBLIC OF SOLMARA (island republic, seafaring/fishing nation)
Capital: Meridia.  Language column: English / Solmaran.
Holder: ELENA MARIS VELAS, born 14 MAR 1994 in Meridia, Solmara.
Passport No. SM 482 917, issued 12 FEB 2024, expires 11 FEB 2034.

Travel chain (all after issue, before expiry, in order):
  03 MAR 2024  DEPARTED Solmara, Meridia Intl
  03 MAR 2024  ARRIVED  Dalmara, Port Lume   (ferry, same day)
  10 MAR 2024  DEPARTED Dalmara, Port Lume
  11 MAR 2024  ARRIVED  Ostara, Kestrel Gate
  25 MAR 2024  DEPARTED Ostara, Kestrel Gate
  25 MAR 2024  ARRIVED  Solmara, Meridia Intl (ferry, same day)
Telling detail: a Dalmara visitor visa (issued 28 FEB 2024, Meridia)
with the condition "NOT VALID FOR EMPLOYMENT - FISHING PORTS
EXCLUDED" and a "FEE 25 DM PAID" stamp -- plus the holder's seafarer
endorsement on the data page.  Solmara is a fishing-island nation.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")


def font(size, bold=False, mono=False):
    path = MONO_B if (mono and bold) else MONO if mono else SANS_B if bold else SANS
    return ImageFont.truetype(path, size)


SCRIPT = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-BoldItalic.ttf"
PORTRAIT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "media-generation-solmara-portrait-0-"
                        "2df743f3-b18c-4be1-bd91-8b05c4ef65e8.webp")


def script_font(size):
    return ImageFont.truetype(SCRIPT, size)


# ---------------------------------------------------------------- colours
PAPER = (246, 241, 227)      # off-white passport paper
PAPER_DARK = (238, 232, 212)
INK = (31, 42, 58)           # near-black ink
NAVY = (31, 58, 95)
NAVY_DARK = (22, 42, 70)
BURGUNDY = (122, 46, 46)
GREY = (96, 96, 90)
RULE = (150, 146, 130)
STAMP_BLUE = (43, 74, 122)
STAMP_RED = (163, 51, 39)
STAMP_GREEN = (34, 92, 62)
STAMP_PLUM = (120, 40, 58)
SKIN = (217, 169, 134)
SKIN_DARK = (198, 148, 112)
HAIR = (74, 50, 38)
JACKET = (46, 74, 107)
PHOTO_BG_TOP = (207, 224, 234)
PHOTO_BG_BOT = (184, 205, 217)

W, H = 1024, 1024
PAGE_W = 512


# ---------------------------------------------------------------- helpers
def tracked(draw, xy, text, fnt, fill, tracking=0):
    """Draw text with fixed extra letter spacing (tracking in px)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def tracked_width(draw, text, fnt, tracking=0):
    return sum(draw.textlength(c, font=fnt) + tracking for c in text) - tracking


def center_tracked(draw, cx, y, text, fnt, fill, tracking=0):
    w = tracked_width(draw, text, fnt, tracking)
    tracked(draw, (cx - w / 2, y), text, fnt, fill, tracking)


def mrz_check(field):
    """ICAO 9303 check digit: weights 7,3,1; A-Z=10-35, '<'=0."""
    total = 0
    for i, ch in enumerate(field):
        if ch.isdigit():
            v = int(ch)
        elif ch == "<":
            v = 0
        else:
            v = ord(ch) - 55  # A=10
        total += v * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<SMRVELAS<<ELENA<MARIS"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "SM482917<"
    dob = "940314"
    exp = "340211"
    opt = "<" * 14
    body = (
        doc + mrz_check(doc)
        + "SMR"
        + dob + mrz_check(dob)
        + "F"
        + exp + mrz_check(exp)
        + opt + mrz_check(opt)
    )
    line2 = body + mrz_check(body)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


def draw_arms(draw, cx, cy, s, color=NAVY, alpha=255):
    """Small coat of arms: shield with three sea-waves and a star."""
    # shield outline
    pts = [
        (cx - 0.55 * s, cy - 0.5 * s), (cx + 0.55 * s, cy - 0.5 * s),
        (cx + 0.55 * s, cy + 0.05 * s), (cx, cy + 0.6 * s),
        (cx - 0.55 * s, cy + 0.05 * s),
    ]
    draw.polygon(pts, outline=color, width=max(2, int(s * 0.06)))
    # star above shield
    r = 0.14 * s
    star = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((cx + rr * math.cos(ang), cy - 0.72 * s + rr * math.sin(ang)))
    draw.polygon(star, fill=color)
    # three waves inside shield
    for k, wy in enumerate((-0.18, 0.02, 0.22)):
        y = cy + wy * s
        xs = [cx - 0.42 * s + i * 0.12 * s for i in range(8)]
        wave = []
        for i, x in enumerate(xs):
            wave.append((x, y + (6 if i % 2 == 0 else -6) * s / 100))
        draw.line(wave, fill=color, width=max(2, int(s * 0.05)))


def guilloche_overlay():
    """Faint wavy-line security pattern across both pages."""
    import math
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ink = (90, 110, 140, 26)
    for row in range(14, H - 8, 13):
        pts = []
        for x in range(8, W - 8, 6):
            y = row + 4.5 * math.sin(x / 46.0 + row / 29.0)
            pts.append((x, y))
        d.line(pts, fill=ink, width=1)
    return ov


def paste_portrait(img, x0, y0, x1, y1):
    """Paste the holder's ID photograph into its frame."""
    src = Image.open(PORTRAIT).convert("RGB")
    tw, th = x1 - x0, y1 - y0
    # crop a tw:th window: head and shoulders, face centred upper-middle
    cw = int(src.width * 0.62)
    ch = int(cw * th / tw)
    cx0 = (src.width - cw) // 2
    cy0 = int(src.height * 0.055)
    photo = src.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((tw, th),
                                                            Image.LANCZOS)
    img.paste(photo, (x0, y0))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], outline=(120, 118, 108), width=2)


def draw_portrait(draw, x0, y0, x1, y1):
    """Stylised bust portrait, drawn with PIL shapes only."""
    # photo background: soft vertical bands
    bands = 12
    for i in range(bands):
        t = i / (bands - 1)
        c = tuple(int(PHOTO_BG_TOP[j] + (PHOTO_BG_BOT[j] - PHOTO_BG_TOP[j]) * t)
                  for j in range(3))
        yy0 = y0 + (y1 - y0) * i / bands
        yy1 = y0 + (y1 - y0) * (i + 1) / bands
        draw.rectangle([x0, yy0, x1, yy1], fill=c)
    cx = (x0 + x1) / 2
    # shoulders / jacket
    shoulder_y = y1 - 6
    draw.polygon([
        (x0 + 4, shoulder_y), (x0 + 4, y0 + 138),
        (cx - 26, y0 + 118), (cx - 20, y0 + 104),
        (cx + 20, y0 + 104), (cx + 26, y0 + 118),
        (x1 - 4, y0 + 138), (x1 - 4, shoulder_y),
    ], fill=JACKET)
    # shirt V + collar
    draw.polygon([(cx - 20, y0 + 104), (cx, y0 + 140), (cx + 20, y0 + 104)],
                 fill=(244, 244, 238))
    draw.polygon([(cx - 20, y0 + 104), (cx - 8, y0 + 116), (cx, y0 + 106),
                  (cx + 8, y0 + 116), (cx + 20, y0 + 104)],
                 fill=(232, 232, 224))
    # neck
    draw.rectangle([cx - 13, y0 + 88, cx + 13, y0 + 110], fill=SKIN_DARK)
    # ears
    draw.ellipse([cx - 40, y0 + 52, cx - 30, y0 + 74], fill=SKIN)
    draw.ellipse([cx + 30, y0 + 52, cx + 40, y0 + 74], fill=SKIN)
    # head
    draw.ellipse([cx - 34, y0 + 18, cx + 34, y0 + 96], fill=SKIN)
    # hair: cap over the top of the head, side strands to the jaw
    draw.pieslice([cx - 36, y0 + 12, cx + 36, y0 + 78], 180, 360, fill=HAIR)
    draw.polygon([(cx - 36, y0 + 40), (cx - 30, y0 + 40), (cx - 32, y0 + 82),
                  (cx - 38, y0 + 82)], fill=HAIR)
    draw.polygon([(cx + 36, y0 + 40), (cx + 30, y0 + 40), (cx + 32, y0 + 82),
                  (cx + 38, y0 + 82)], fill=HAIR)
    draw.ellipse([cx - 34, y0 + 16, cx + 34, y0 + 52], fill=HAIR)
    draw.ellipse([cx - 30, y0 + 34, cx + 30, y0 + 62], fill=SKIN)
    # brows, eyes, nose, mouth -- kept minimal and symmetrical
    draw.line([(cx - 20, y0 + 56), (cx - 9, y0 + 54)], fill=HAIR, width=2)
    draw.line([(cx + 9, y0 + 54), (cx + 20, y0 + 56)], fill=HAIR, width=2)
    draw.ellipse([cx - 18, y0 + 60, cx - 12, y0 + 64], fill=INK)
    draw.ellipse([cx + 12, y0 + 60, cx + 18, y0 + 64], fill=INK)
    draw.line([(cx, y0 + 64), (cx - 2, y0 + 76), (cx + 2, y0 + 78)],
              fill=SKIN_DARK, width=2)
    draw.line([(cx - 8, y0 + 86), (cx + 8, y0 + 86)], fill=(150, 80, 70), width=2)
    # frame
    draw.rectangle([x0, y0, x1, y1], outline=(120, 118, 108), width=2)


def field(draw, x, y, label, label2, value, value_size=16, width=280):
    """One labelled data field: small caps label, bold value, ruled line."""
    draw.text((x, y), label, font=font(10), fill=GREY)
    if label2:
        draw.text((x, y + 12), label2, font=font(9), fill=GREY)
    draw.text((x, y + 24), value, font=font(value_size, bold=True), fill=INK)
    draw.line([(x, y + 24 + value_size + 6), (x + width, y + 24 + value_size + 6)],
              fill=RULE, width=1)


def stamp(base, cx, cy, w, h, country, action, place, date, angle, color,
          alpha=215):
    """One ink entry/exit stamp, slightly rotated, stamped onto base."""
    pad = 24
    layer = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ink = color + (alpha,)
    # double border
    d.rounded_rectangle([6, 6, w + 2 * pad - 6, h + 2 * pad - 6], radius=9,
                        outline=ink, width=3)
    d.rounded_rectangle([12, 12, w + 2 * pad - 12, h + 2 * pad - 12], radius=6,
                        outline=ink, width=1)
    # country
    f = font(14, bold=True)
    tw = d.textlength(country, font=f)
    d.text(((w + 2 * pad - tw) / 2, 14), country, font=f, fill=ink)
    # action
    f2 = font(18, bold=True)
    tw = d.textlength(action, font=f2)
    d.text(((w + 2 * pad - tw) / 2, 34), action, font=f2, fill=ink)
    # rule
    d.line([(20, 60), (w + 2 * pad - 20, 60)], fill=ink, width=1)
    # place
    f3 = font(11)
    tw = d.textlength(place, font=f3)
    d.text(((w + 2 * pad - tw) / 2, 65), place, font=f3, fill=ink)
    # date
    f4 = font(15, bold=True)
    tw = d.textlength(date, font=f4)
    d.text(((w + 2 * pad - tw) / 2, 82), date, font=f4, fill=ink)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), (34, 38, 52))
    draw = ImageDraw.Draw(img)
    # paper: two pages with a centre gutter
    draw.rectangle([8, 8, 512, H - 8], fill=PAPER)
    draw.rectangle([512, 8, W - 8, H - 8], fill=PAPER)
    draw.line([(512, 8), (512, H - 8)], fill=(120, 114, 98), width=2)
    draw.line([(512, 8), (512, H - 8)], fill=(200, 192, 172), width=1)
    # security guilloche + a soft shadow down the spine
    img = img.convert("RGBA")
    img.alpha_composite(guilloche_overlay())
    spine = Image.new("RGBA", (72, H), (0, 0, 0, 0))
    for i in range(72):
        a = int(64 * (1 - abs(i - 36) / 36) ** 2)
        ImageDraw.Draw(spine).line([(i, 0), (i, H)], fill=(20, 18, 12, a))
    img.alpha_composite(spine, (512 - 36, 0))
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ================================================= LEFT PAGE: data page
    draw_arms(draw, 256, 52, 44)
    center_tracked(draw, 256, 92, "REPUBLIC OF SOLMARA", font(23, bold=True),
                   NAVY_DARK, tracking=2)
    center_tracked(draw, 256, 122, "PASSPORT", font(14, bold=True), NAVY, tracking=8)
    draw.line([(36, 148), (476, 148)], fill=NAVY, width=2)
    draw.line([(36, 152), (476, 152)], fill=NAVY, width=1)

    # portrait: the holder's ID photograph
    paste_portrait(img, 36, 170, 186, 360)
    draw.text((36, 366), "PHOTOGRAPH", font=font(9), fill=GREY)

    # fields right of portrait
    fx, fw = 206, 270
    field(draw, fx, 170, "TYPE / VRSTA", None, "P", width=fw)
    field(draw, fx, 222, "CODE / KODA", None, "SMR", width=fw)
    field(draw, fx, 274, "PASSPORT No. / PUTOVNICA BR.", None, "SM 482 917",
          width=fw)
    field(draw, fx, 326, "SURNAME / PREZIME", None, "VELAS", width=fw)

    # full-width fields
    field(draw, 36, 412, "GIVEN NAMES / IME", None, "ELENA MARIS", width=440)
    field(draw, 36, 474, "NATIONALITY / DRZAVLJANSTVO", None, "SOLMARAN",
          width=200)
    field(draw, 276, 474, "SEX / SPOL", None, "F", width=200)
    field(draw, 36, 536, "DATE OF BIRTH / DATUM RODENJA", None,
          "14 MAR 1994", width=200)
    field(draw, 276, 536, "PLACE OF BIRTH / MJESTO RODENJA", None,
          "MERIDIA, SOLMARA", width=200)
    field(draw, 36, 598, "DATE OF ISSUE / DATUM IZDAVANJA", None,
          "12 FEB 2024", width=200)
    field(draw, 276, 598, "DATE OF EXPIRY / DATUM ISTEKA", None,
          "11 FEB 2034", width=200)
    field(draw, 36, 660, "AUTHORITY / TIJELO", None,
          "MERIDIA PASSPORT OFFICE", width=440)

    # holder's signature, in ink script on a slightly tilted layer
    sig_layer = Image.new("RGBA", (300, 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sig_layer)
    sd.text((6, 8), "Elena M. Velas", font=script_font(34),
            fill=NAVY_DARK + (235,))
    sig_layer = sig_layer.rotate(2, expand=True, resample=Image.BICUBIC)
    img = img.convert("RGBA")
    img.alpha_composite(sig_layer, (40, 712))
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.line([(36, 768), (270, 768)], fill=RULE, width=1)
    draw.text((36, 774), "HOLDER'S SIGNATURE / POTPIS", font=font(9), fill=GREY)

    # seafarer endorsement -- the telling detail on the data page
    draw.rectangle([36, 812, 476, 872], outline=NAVY, width=1, fill=PAPER_DARK)
    draw.text((48, 820), "ENDORSEMENT", font=font(10, bold=True), fill=NAVY_DARK)
    draw.text((48, 836),
              "Holder is a registered seafarer of the Solmaran deep-sea",
              font=font(11), fill=INK)
    draw.text((48, 852),
              "fleet. Seaman's Book No. 1187 - Harbour Master, Meridia.",
              font=font(11), fill=INK)

    # machine-readable zone (16px mono: 44 chars fit the 440px column)
    line1, line2 = mrz_lines()
    draw.text((36, 902), line1, font=font(16, mono=True), fill=INK)
    draw.text((36, 926), line2, font=font(16, mono=True), fill=INK)
    draw.text((36, 956),
              "This passport remains the property of the Republic of Solmara.",
              font=font(9), fill=GREY)

    # =============================================== RIGHT PAGE: visas/stamps
    center_tracked(draw, 768, 36, "VISAS", font(20, bold=True), NAVY_DARK,
                   tracking=6)
    center_tracked(draw, 768, 64, "VIZAT  ·  ENTRIES AND EXITS", font(10),
                   GREY, tracking=2)
    draw.line([(548, 88), (988, 88)], fill=NAVY, width=2)

    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # six stamps: one coherent trip, 03-25 MAR 2024; each country inks
    # in its own colour, with the uneven density of real border ink
    stamp(base, 650, 160, 185, 105, "SOLMARA", "DEPARTED",
          "MERIDIA INT'L", "03 MAR 2024", -5, STAMP_BLUE, alpha=228)
    stamp(base, 886, 160, 185, 105, "DALMARA", "ARRIVED",
          "PORT LUME", "03 MAR 2024", 4, STAMP_GREEN, alpha=205)
    stamp(base, 650, 300, 185, 105, "DALMARA", "DEPARTED",
          "PORT LUME", "10 MAR 2024", 6, STAMP_GREEN, alpha=222)
    stamp(base, 886, 300, 185, 105, "OSTARA", "ARRIVED",
          "KESTREL GATE", "11 MAR 2024", -3, STAMP_PLUM, alpha=212)
    stamp(base, 650, 440, 185, 105, "OSTARA", "DEPARTED",
          "KESTREL GATE", "25 MAR 2024", 3, STAMP_PLUM, alpha=230)
    stamp(base, 886, 440, 185, 105, "SOLMARA", "ARRIVED",
          "MERIDIA INT'L", "25 MAR 2024", -6, STAMP_BLUE, alpha=208)

    img = img.convert("RGBA")
    img.alpha_composite(base)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Dalmara visitor visa -- the telling paperwork detail
    draw.rectangle([548, 545, 988, 800], outline=BURGUNDY, width=2)
    draw.rectangle([554, 551, 982, 794], outline=BURGUNDY, width=1)
    center_tracked(draw, 768, 566, "VISITOR VISA", font(17, bold=True),
                   BURGUNDY, tracking=4)
    center_tracked(draw, 768, 592, "REPUBLIC OF DALMARA", font(12, bold=True),
                   NAVY_DARK, tracking=2)
    draw.line([(570, 620), (966, 620)], fill=RULE, width=1)
    visa_lines = [
        ("Issued:", "28 FEB 2024 - Consulate of Dalmara, Meridia"),
        ("Valid:", "14 days from first entry - single entry"),
        ("Conditions:", "NOT VALID FOR EMPLOYMENT"),
        ("", "FISHING PORTS EXCLUDED"),
    ]
    y = 634
    for k, v in visa_lines:
        if k:
            draw.text((570, y), k, font=font(12, bold=True), fill=INK)
        draw.text((668, y), v, font=font(12), fill=INK)
        y += 26
    draw.text((570, 742), "Visa No. DV-2024-0318-7",
              font=font(11), fill=GREY)

    # fee stamp, overlapping the visa box corner (date line kept clear
    # of the box's bottom border)
    fee = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fee)
    red = STAMP_RED + (225,)
    fd.ellipse([8, 8, 152, 152], outline=red, width=3)
    fd.ellipse([18, 18, 142, 142], outline=red, width=1)
    for txt, yy, fnt in (("FEE PAID", 42, font(14, bold=True)),
                         ("25 DM", 64, font(18, bold=True)),
                         ("28 FEB 2024", 90, font(10, bold=True))):
        tw = fd.textlength(txt, font=fnt)
        fd.text(((160 - tw) / 2, yy), txt, font=fnt, fill=red)
    fee = fee.rotate(12, expand=True, resample=Image.BICUBIC)
    img = img.convert("RGBA")
    img.alpha_composite(fee, (820, 655))
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.text((548, 830),
              "Holder's Seaman's Book No. 1187 - see endorsement, page 1.",
              font=font(11), fill=GREY)
    draw.text((548, 852),
              "Solmara - Meridia Harbour Authority",
              font=font(11), fill=GREY)
    draw.text((960, 976), "2", font=font(12), fill=GREY)

    out = os.environ.get("OUTPUT_PATH", "/output/entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
