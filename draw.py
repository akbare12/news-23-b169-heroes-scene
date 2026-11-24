#!/usr/bin/env python3
"""Draw the news-23 heroes-scene front page (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (15, 42, 74)
NAVY2 = (23, 64, 110)
TEAL = (14, 90, 96)
GOLD = (198, 148, 28)
RED = (185, 28, 28)
GREEN = (22, 120, 60)
GRAY = (90, 90, 90)
LGRAY = (232, 232, 232)
INK = (20, 20, 20)
WHITE = (255, 255, 255)
ORANGE = (230, 110, 20)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

def chip(draw, x, y, text, fill):
    f = font(FB, 8)
    w = draw.textlength(text, font=f) + 8
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=3, fill=fill)
    draw.text((x + 4, y + 2), text, font=f, fill=WHITE)
    return x + w

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([10, 8, 1014, 56], fill=NAVY)
center(d, 14, "THE WORLD TODAY", font(FSB, 34), WHITE)
# date line
d.line([10, 64, 1014, 64], fill=NAVY, width=2)
center(d, 70, "MONDAY 23 NOVEMBER 2026", font(FB, 14), NAVY)
# kicker
center(d, 92, "AI rout shakes Asia  |  Guterres calls for AI rules  |  US lead over China at record low",
       font(FR, 12), INK)

# ---------- number strip (10 numbers, 5 cols x 2 rows) ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL FUND"), ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL, METS"), ("165", "MISSILES / WEEK"), ("12,000", "CLEARED MANCHESTER"),
    ("264 kg", "EXPLOSIVES, LEBANON"), ("$107.3B", "ANTHROPIC IPO"),
]
d.rectangle([10, 112, 1014, 176], fill=(245, 245, 245), outline=LGRAY)
for i, (val, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x0 = 12 + col * 200
    y0 = 114 + row * 31
    center(d, y0, val, font(FB, 15), NAVY, x0, x0 + 198)
    center(d, y0 + 17, lab, font(FB, 8), GRAY, x0, x0 + 198)

# ---------- region bar ----------
center(d, 182, "ASIA-PACIFIC 7   ·   AMERICAS 8   ·   MIDDLE EAST 6   ·   EUROPE 5   ·   AFRICA 3   ·   WORLD 2",
       font(FB, 12), INK)
d.line([10, 200, 1014, 200], fill=NAVY, width=2)
d.text((10, 206), "THE DAY'S BIG STORIES", font=font(FB, 11), fill=NAVY)

# ---------- hero scenes ----------
HX = [10, 350, 690]
HW = 324
HY = 224
SH = 140  # scene art height

def hero_frame(x):
    d.rectangle([x, HY, x + HW, HY + SH], outline=NAVY, width=2)

# --- scene 1: Kospi skyline + chart ---
x = HX[0]
hero_frame(x)
d.rectangle([x + 2, HY + 2, x + HW - 2, HY + SH - 2], fill=(10, 30, 55))
# buildings with lit windows
import random
random.seed(23)
bx = x + 12
while bx < x + HW - 40:
    bw = random.randint(26, 40)
    bh = random.randint(34, 78)
    by = HY + SH - 8 - bh
    d.rectangle([bx, by, bx + bw, HY + SH - 8], fill=(30, 60, 100))
    for wy in range(by + 6, HY + SH - 14, 12):
        for wx in range(bx + 5, bx + bw - 6, 11):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    bx += bw + 6
# chart line (kept in lower half, clear of the big number)
pts = [(x + 20, HY + 96), (x + 80, HY + 84), (x + 140, HY + 104), (x + 200, HY + 78),
       (x + 260, HY + 100), (x + 305, HY + 70)]
d.line(pts, fill=ORANGE, width=4)
d.text((x + 12, HY + 10), "-3.3%", font=font(FB, 30), fill=(255, 210, 90))
d.text((x + 130, HY + 16), "KOSPI 4,708.54", font=font(FB, 13), fill=WHITE)
d.text((x + 130, HY + 36), "-161 PTS · INTRADAY -5.8%", font=font(FB, 10), fill=(200, 210, 225))

# --- scene 2: Guterres globe + flags ---
x = HX[1]
hero_frame(x)
d.rectangle([x + 2, HY + 2, x + HW - 2, HY + SH - 2], fill=TEAL)
# flags row at very top, small, right side
flag_cols = [(255, 255, 255), (255, 200, 60), (120, 200, 255), (255, 120, 120)]
for i, fc in enumerate(flag_cols):
    fx = x + HW - 14 - (i + 1) * 26
    d.rectangle([fx, HY + 8, fx + 20, HY + 20], fill=fc, outline=WHITE)
# globe
cx, cy, r = x + 90, HY + 82, 46
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 140, 190), outline=WHITE, width=2)
d.ellipse([cx - r + 12, cy - r + 10, cx - r + 34, cy - r + 26], fill=(60, 180, 90))
d.ellipse([cx + 4, cy + 8, cx + 30, cy + 30], fill=(60, 180, 90))
d.text((x + 160, HY + 52), "150", font=font(FB, 34), fill=(255, 210, 90))
d.text((x + 160, HY + 92), "DELEGATES", font=font(FB, 13), fill=WHITE)
d.text((x + 160, HY + 110), "BRIDGETOWN", font=font(FB, 13), fill=WHITE)
d.text((x + 160, HY + 126), "BARBADOS", font=font(FB, 13), fill=WHITE)

# --- scene 3: Power Index bars ---
x = HX[2]
hero_frame(x)
d.rectangle([x + 2, HY + 2, x + HW - 2, HY + SH - 2], fill=(248, 248, 248))
bars = [("US 78.9", 78.9, (30, 90, 160)), ("CHINA 73.6", 73.6, (185, 60, 60)),
        ("INDIA 40.5", 40.5, GOLD)]
by = HY + 10
for lab, val, col in bars:
    d.text((x + 12, by), lab, font=font(FB, 12), fill=INK)
    d.rectangle([x + 12, by + 18, x + 12 + int(val * 3.4), by + 32], fill=col)
    by += 34
d.text((x + 12, HY + SH - 24), "GAP 5.3 — NARROWEST SINCE 2018", font=font(FB, 11), fill=RED)

# --- hero headlines / bodies / sources ---
heroes = [
    ("AI ROUT HITS ASIA", "Kospi sheds 161 points as Samsung -3.1% and SK Hynix -2.5% lead the sell-off.", "REUTERS"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE", "Summit backs a risk framework — a blueprint, not a treaty.", "AP"),
    ("US LEAD OVER CHINA AT RECORD LOW", "Asia Power Index: US 78.9, China 73.6; US diplomacy -6 to 76.7.", "LOWY INSTITUTE"),
]
for i, (hl, body, src) in enumerate(heroes):
    x = HX[i]
    y = HY + SH + 6
    lines = wrap(d, hl, font(FB, 13), HW)
    for ln in lines[:2]:
        d.text((x, y), ln, font=font(FB, 13), fill=INK)
        y += 16
    y = HY + SH + 40
    for ln in wrap(d, body, font(FR, 10), HW)[:2]:
        d.text((x, y), ln, font=font(FR, 10), fill=(60, 60, 60))
        y += 12
    d.text((x, HY + SH + 66), src, font=font(FB, 9), fill=GRAY)
    chip(d, x + 90, HY + SH + 65, "REPORTED", GREEN)

# ---------- cards ----------
d.line([10, 440, 1014, 440], fill=NAVY, width=2)
d.text((10, 446), "MORE OF THE DAY", font=font(FB, 11), fill=NAVY)
cards = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker.", "REUTERS", False),
    ("FBI PROBES NCIC POLICE-DATABASE HACK", "Bureau probes law-enforcement breach.", "AP", False),
    ("TRUMP: IRAN STRIKES MAY RESUME", "Strikes could return in the New Year.", "REUTERS", False),
    ("NASDAQ FUTURES +3% IN HOLIDAY WEEK", "US stocks set for strong holiday week.", "BLOOMBERG", False),
    ("SKUBAL $450M METS DEAL", "Nine years — record for a pitcher.", "ESPN", False),
    ("TOM JACKSON DIES AT 75", "NFL linebacker, broadcaster, dies.", "AP", False),
    ("STATES SUE SPACEX OVER AI SAFETY", "AGs challenge AI safety claims.", "REUTERS", False),
    ("ANTHROPIC IPO $107.3B", "Raised at $83; debut close $97.17.", "BLOOMBERG", False),
    ("POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Warsaw: Kh-101s entered its skies.", "AP", True),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "US flags orbital weapon risk.", "REUTERS", True),
]
CW, CH = 200, 58
for i, (hl, body, src, claim) in enumerate(cards):
    col, row = i % 5, i // 5
    x = 10 + col * 204
    y = 464 + row * 62
    d.rectangle([x, y, x + CW, y + CH], outline=LGRAY)
    yy = y + 4
    for ln in wrap(d, hl, font(FB, 10), CW - 8)[:2]:
        d.text((x + 4, yy), ln, font=font(FB, 10), fill=INK)
        yy += 12
    d.text((x + 4, y + CH - 24), body, font=font(FR, 8), fill=(60, 60, 60))
    d.text((x + 4, y + CH - 13), src, font=font(FB, 8), fill=GRAY)
    chip(d, x + CW - 58, y + CH - 14, "CLAIM" if claim else "REPORTED", RED if claim else GREEN)

# ---------- map + ALSO ----------
d.line([10, 596, 1014, 596], fill=NAVY, width=2)
d.text((10, 602), "THE WORLD", font=font(FB, 11), fill=NAVY)
d.text((510, 602), "ALSO ON MONDAY", font=font(FB, 11), fill=NAVY)

# map blobs
d.polygon([(60, 640), (200, 620), (235, 680), (205, 770), (120, 790), (58, 730)], fill=(210, 228, 210))
d.polygon([(285, 625), (475, 620), (485, 665), (445, 705), (300, 695), (272, 655)], fill=(210, 228, 210))
d.polygon([(330, 710), (432, 708), (442, 762), (402, 802), (340, 782), (320, 732)], fill=(210, 228, 210))
pins = [
    (440, 640), (150, 748), (140, 658), (330, 652), (315, 632),
    (296, 646), (372, 636), (398, 656), (360, 676), (384, 680),
    (410, 688), (385, 728), (360, 758),
]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=NAVY, outline=WHITE, width=1)
    t = str(i)
    tw = d.textlength(t, font=font(FB, 8))
    d.text((px - tw / 2, py - 5), t, font=font(FB, 8), fill=WHITE)
legend = [
    "1 Seoul   2 Bridgetown   3 Washington   4 Paris   5 London",
    "6 Manchester   7 Warsaw   8 Kyiv   9 Antalya   10 Gaza",
    "11 Bahrain   12 Khartoum   13 Kinshasa",
]
ly = 812
for ln in legend:
    d.text((10, ly), ln, font=font(FR, 9), fill=(60, 60, 60))
    ly += 13

also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared after substance scare",
    "Zelenskyy: 165 Russian missiles in a week",
    "COP31: the day after — Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain Sat: Iranian strike hits plant, 2 hurt",
    "Benghazi: UN demands probe of port attacks [CLAIM]",
    "Sudan: air defences down drones over Khartoum [CLAIM]",
    "DRC: fighting traps Ebola teams (11,762 cases)",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules (cuts to 80%)",
    "Seoul readies 10T-won stabilisation fund",
]
ay = 622
for i, item in enumerate(also, 1):
    d.text((510, ay), f"{i}. {item}", font=font(FR, 10), fill=INK)
    ay += 14

# ---------- DATE CHECK ----------
d.rectangle([10, 872, 1014, 990], outline=RED, width=3)
d.rectangle([10, 872, 1014, 896], fill=RED)
d.text((16, 877), "DATE CHECK — LEFT OUT (NOT 23 NOVEMBER)", font=font(FB, 12), fill=WHITE)
left_out = [
    "Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
    "El Chapo Isidro captured (22 Nov)", "EU–Indonesia pact (21 Nov)",
    "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)",
]
for i, item in enumerate(left_out):
    col, row = i % 2, i // 2
    d.text((20 + col * 500, 900 + row * 13), "✕  " + item, font=font(FR, 10), fill=RED)
d.text((16, 942), "NOT YET:", font=font(FB, 10), fill=RED)
not_yet = [
    "Dymer search continues (14 missing)", "4 House races uncalled",
    "COP32 venue not set", "WHO evacuating trapped Ebola staff",
]
for i, item in enumerate(not_yet):
    col, row = i % 2, i // 2
    d.text((20 + col * 500, 956 + row * 12), "•  " + item, font=font(FR, 10), fill=INK)

# ---------- footer ----------
d.line([10, 996, 1014, 996], fill=NAVY, width=1)
d.text((10, 1002), "Sources: Reuters · AP · Bloomberg · ESPN · Lowy Institute", font=font(FR, 9), fill=GRAY)
d.text((640, 1002), "REPORTED = confirmed by wires   CLAIM = one side's claim", font=font(FR, 9), fill=GRAY)

img.save(OUT, optimize=True)
print("saved", OUT, img.size)
