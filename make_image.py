# Editorial front-page image for Thursday 19 November 2026 world news.
# Drawn entirely with PIL shapes + text: no external images, no network.
# Run: python3 make_image.py  -> writes entry.png (1024x1024) beside this file.
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W = H = 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_O = FD + "DejaVuSans.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

# Palette: newsprint cream, ink, accent red/blue/gold
CREAM = (250, 246, 236)
INK = (18, 18, 22)
MUTED = (70, 70, 78)
RED = (176, 32, 40)
NAVY = (22, 48, 96)
GOLD = (184, 134, 11)
TEAL = (0, 110, 110)
GREEN = (28, 120, 60)
PURPLE = (96, 48, 140)
LINE = (40, 40, 48)
PANEL = (255, 253, 248)
DARKPANEL = (22, 28, 48)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def block(x, y, text, font, fill, maxw, leading=6):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y

def kicker(x, y, text, color):
    d.rectangle([x, y, x + 10, y + 18], fill=color)
    d.text((x + 16, y - 1), text.upper(), font=f(SANS_B, 15), fill=color)
    return y + 26

def panel(x0, y0, x1, y1, fill=PANEL, outline=LINE, width=2):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

# ---------- Masthead ----------
d.rectangle([0, 0, W, 118], fill=INK)
d.text((28, 10), "THE WORLD IN ONE DAY", font=f(SERIF_B, 52), fill=(255, 255, 255))
d.text((30, 70), "Thursday  19 November 2026  —  World News Front Page", font=f(SANS_B, 24), fill=(255, 210, 90))
d.text((W - 28, 16), "19 NOV", font=f(SANS_B, 34), fill=(255, 255, 255), anchor="ra")
d.text((W - 28, 52), "2026", font=f(SANS_B, 34), fill=(255, 210, 90), anchor="ra")
d.text((W - 28, 92), "THURSDAY", font=f(SANS, 15), fill=(200, 200, 210), anchor="ra")

# ---------- Lead story ----------
LX0, LY0, LX1, LY1 = 16, 130, 1008, 430
panel(LX0, LY0, LX1, LY1)
y = kicker(LX0 + 18, LY0 + 14, "Lead story  ·  Shenzhen, China  ·  APEC Summit", RED)
d.text((LX0 + 18, y), "Trump, Xi and Putin hold first", font=f(SERIF_B, 44), fill=INK)
d.text((LX0 + 18, y + 50), "three-way summit", font=f(SERIF_B, 44), fill=INK)
y2 = y + 112
y2 = block(LX0 + 18, y2, "The US, Chinese and Russian presidents met together for the first time on the sidelines of APEC and issued a joint \u201cpeace declaration\u201d pledging dialogue on nuclear risks, stable energy flows and UN reform. Ukraine and the Iran war topped the agenda; no major agreement was announced, with New START expired and arms control still elusive.",
           f(SANS, 19), MUTED, 600, leading=5)
# Three leader circles (flags as initials)
cx = LX0 + 660
for i, (init, col, lab) in enumerate([("US", NAVY, "TRUMP"), ("CN", RED, "XI"), ("RU", (60, 60, 160), "PUTIN")]):
    x = cx + i * 112
    d.ellipse([x, LY0 + 96, x + 92, LY0 + 188], fill=col, outline=INK, width=3)
    d.text((x + 46, LY0 + 142), init, font=f(SANS_B, 30), fill=(255, 255, 255), anchor="mm")
    d.text((x + 46, LY0 + 200), lab, font=f(SANS_B, 16), fill=INK, anchor="ma")
d.text((cx + 140, LY0 + 226), "90-minute talks  ·  19 Nov", font=f(SANS_O, 15), fill=MUTED, anchor="ma")
# handshake-ish divider
d.line([cx + 10, LY0 + 250, cx + 320, LY0 + 250], fill=GOLD, width=4)
block(cx + 6, LY0 + 262, "First-ever trilateral meeting of the three leaders.", f(SANS_O, 15), MUTED, 320, leading=4)

# ---------- Grid panels ----------
GX = [16, 352, 688]
GW = 320
GY = [442, 726]
GH = 272

stories = [
    dict(color=NAVY, kick="Justice · The Hague", head="World court: Myanmar committed genocide",
         body="The ICJ ruled 9–6 that Myanmar committed state-sponsored genocide against the Rohingya — the UN top court's first such ruling. Restitution ordered.",
         icon="scales"),
    dict(color=PURPLE, kick="Culture · Worldwide launch", head="GTA VI launches around the world",
         body="Grand Theft Auto VI released at midnight local time on PS5 and Xbox Series X|S — after two delays, the most pre-ordered game ever. A 212 GB download strained broadband worldwide.",
         icon="pad"),
    dict(color=RED, kick="War · Ukraine / Crimea", head="Ukraine strikes Crimean Bridge again",
         body="Russia said Ukraine attacked the Crimean Bridge for the third time this week, as fighting also continued in Gaza with a rare Israeli ground operation in central Gaza.",
         icon="bridge"),
    dict(color=(180, 80, 0), kick="War · Middle East", head="Iran war widens across the Gulf",
         body="US forces struck an IRGC missile site on Qeshm Island after a drone attack in Bahrain; Iran fired on Kuwait and Gulf states. A Houthi missile damaged Riyadh's PIF Tower.",
         icon="missile"),
    dict(color=TEAL, kick="Nuclear · North Korea", head="IAEA: N. Korea expanding enrichment",
         body="IAEA chief Grossi told the board North Korea is expanding uranium enrichment at Yongbyon. Seoul's President Lee renewed calls for dialogue with Pyongyang.",
         icon="atom"),
    dict(color=GREEN, kick="Climate · COP31 / India", head="Climate talks deadlock; cyclone nears India",
         body="COP31 entered its final stage split over fossil-fuel phase-out and finance. Cyclone Akvan was set to hit India's Andhra–Odisha coast Friday at 90–100 km/h.",
         icon="leaf"),
]

def draw_icon(kind, x, y, color):
    # simple pictograms in a 64x64 box at (x,y)
    if kind == "scales":
        d.line([x + 32, y + 4, x + 32, y + 44], fill=color, width=4)
        d.line([x + 8, y + 12, x + 56, y + 12], fill=color, width=4)
        for sx in (x + 8, x + 56):
            d.line([sx, y + 12, sx - 8, y + 28], fill=color, width=2)
            d.line([sx, y + 12, sx + 8, y + 28], fill=color, width=2)
            d.arc([sx - 10, y + 24, sx + 10, y + 40], 0, 180, fill=color, width=3)
        d.line([x + 20, y + 52, x + 44, y + 52], fill=color, width=5)
    elif kind == "pad":
        d.rounded_rectangle([x + 2, y + 18, x + 62, y + 48], radius=14, outline=color, width=4)
        d.line([x + 16, y + 33, x + 28, y + 33], fill=color, width=4)
        d.line([x + 22, y + 27, x + 22, y + 39], fill=color, width=4)
        for dx, dy in [(46, 28), (54, 36)]:
            d.ellipse([x + dx, y + dy, x + dx + 7, y + dy + 7], fill=color)
    elif kind == "bridge":
        d.line([x + 2, y + 40, x + 62, y + 40], fill=color, width=5)
        d.line([x + 14, y + 10, x + 14, y + 52], fill=color, width=4)
        d.line([x + 50, y + 10, x + 50, y + 52], fill=color, width=4)
        d.line([x + 14, y + 14, x + 50, y + 38], fill=color, width=2)
        d.line([x + 50, y + 14, x + 14, y + 38], fill=color, width=2)
        for wx in range(4, 60, 12):
            d.arc([x + wx, y + 50, x + wx + 10, y + 60], 0, 180, fill=NAVY, width=2)
    elif kind == "missile":
        d.polygon([(x + 44, y + 4), (x + 58, y + 18), (x + 34, y + 42), (x + 20, y + 28)], fill=color)
        d.polygon([(x + 20, y + 28), (x + 10, y + 44), (x + 24, y + 40)], fill=INK)
        d.line([x + 12, y + 48, x + 4, y + 58], fill=GOLD, width=4)
        d.line([x + 20, y + 50, x + 14, y + 60], fill=GOLD, width=4)
    elif kind == "atom":
        d.ellipse([x + 26, y + 26, x + 38, y + 38], fill=color)
        for a in (0, 60, 120):
            import math
            pts = []
            for t in range(0, 361, 10):
                r = math.radians(t); ra = math.radians(a)
                ex, ey = 28 * math.cos(r), 11 * math.sin(r)
                pts.append((x + 32 + ex * math.cos(ra) - ey * math.sin(ra),
                            y + 32 + ex * math.sin(ra) + ey * math.cos(ra)))
            d.line(pts, fill=color, width=2)
    elif kind == "leaf":
        d.ellipse([x + 8, y + 6, x + 54, y + 52], fill=color)
        d.line([x + 14, y + 50, x + 48, y + 12], fill=(255, 255, 255), width=3)
        d.line([x + 14, y + 50, x + 10, y + 60], fill=color, width=4)

for idx, s in enumerate(stories):
    x0 = GX[idx % 3]; y0 = GY[idx // 3]; x1 = x0 + GW; y1 = y0 + GH
    panel(x0, y0, x1, y1)
    yy = kicker(x0 + 14, y0 + 12, s["kick"], s["color"])
    draw_icon(s["icon"], x1 - 72, y0 + 34, s["color"])
    for ln in wrap(d, s["head"], f(SERIF_B, 24), GW - 96):
        d.text((x0 + 14, yy), ln, font=f(SERIF_B, 24), fill=INK)
        yy += 30
    yy += 4
    yy = block(x0 + 14, yy, s["body"], f(SANS, 16), MUTED, GW - 28, leading=5)

# ---------- Footer ----------
d.rectangle([0, 1006, W, H], fill=INK)
d.text((16, 1010), "Also 19 Nov: Denmark backs Greenland defence deal  ·  Japan PM Takaichi spoke with Putin  ·  Fiji El Niño disaster", font=f(SANS, 13), fill=(230, 230, 230))

img.save(os.path.join(BASE, "entry.png"), optimize=True)
print("wrote entry.png", img.size, os.path.getsize(os.path.join(BASE, "entry.png")), "bytes")
