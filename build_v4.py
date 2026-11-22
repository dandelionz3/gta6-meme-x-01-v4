#!/usr/bin/env python3
"""Build GTA 6 meme v4 — 'FINAL NOTICE' (1600x1600) for make.fun gta6-meme-x-01.
Revision 2 (user direction 03:53 WIB): the ticket is depicted AS ON A MOBILE
PHONE — the whole meme is a phone screenshot: status bar (9:41, Dynamic
Island, battery), a VICE CITY PD push notification ("FINAL NOTICE — Your
$13,587 ticket is now $510,445"), then the citation as the app screen below,
with an iMessage-style "Tap to pay" bar and a home indicator.

Kept from revision 1 (commit 087aaba): Vice City PD citation format, all
amounts (total $510,445), itemized joke labels, "47 HEISTS" payment plan,
"FAILURE TO PAY WILL RESULT IN A SEQUEL.", suspects photo with OVERDUE stamp,
and the magenta make.fun banner cropped pixel-for-pixel from v3's meme.png
(y 1300-1552) pasted at the identical coordinates. Background: v2 neon art,
darkened. All text rendered with PIL so every word is spelled correctly.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

V2 = "/home/hatch/workspace/makefun/gta6-meme-x-01-v2"
V3 = "/home/hatch/workspace/makefun/gta6-meme-x-01-v3"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01-v4"
W = H = 1600
CARD = (64, 93, 1536, 1552)          # x0, y0, x1, y1 (same as v2/v3)
BANNER = (64, 1300, 1536, 1552)      # exact banner strip in v3

BLACK = (17, 17, 17)
RED = (176, 0, 0)
DARKRED = (128, 16, 16)
PAPER = (244, 233, 203)
GRAY = (96, 84, 62)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 188, 160)
PHONE = (16, 16, 18)

F_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center_text(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


# ---------- 1. background: v2 neon art, darkened ----------
bg = Image.open(f"{V2}/media-generation-bg-chase-0-8e4031e3-de7a-4ba5-a05d-c134645e9f77.webp").convert("RGB")
bw, bh = bg.size
scale = max(W / bw, H / bh)
bg = bg.resize((int(bw * scale + 0.5), int(bh * scale + 0.5)), Image.LANCZOS)
x0 = (bg.width - W) // 2
y0 = (bg.height - H) // 2
bg = bg.crop((x0, y0, x0 + W, y0 + H))
bg = ImageEnhance.Brightness(bg).enhance(0.52)
bg = bg.filter(ImageFilter.GaussianBlur(2))

canvas = bg.copy()

# ---------- 2. phone body + screen (card-sized layer) ----------
card_w = CARD[2] - CARD[0]          # 1472
card_h = CARD[3] - CARD[1]          # 1459
layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
mask = Image.new("L", (card_w, card_h), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=64, fill=255)
card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
card.putalpha(mask)
d = ImageDraw.Draw(card)

# phone bezel (dark, rounded) — fills the card down to the banner
d.rounded_rectangle([0, 0, card_w - 1, 1206], radius=64, fill=PHONE + (255,))
# screen (cream paper) inside the bezel; bottom edge meets the banner
d.rounded_rectangle([16, 16, 1455, 1206], radius=48, fill=PAPER + (255,))
# side buttons (left: silent switch + volume, right: power)
d.rounded_rectangle([-4, 210, 4, 250], radius=4, fill=(60, 60, 64, 255))
d.rounded_rectangle([-4, 280, 4, 360], radius=4, fill=(60, 60, 64, 255))
d.rounded_rectangle([card_w - 4, 300, card_w + 4, 380], radius=4, fill=(60, 60, 64, 255))

SX0, SX1 = 16, 1455               # screen x-range
SCX = (SX0 + SX1) / 2              # screen center x = 735.5

# ---------- 3. status bar: 9:41, Dynamic Island, signal/wifi/battery ----------
d.text((60, 26), "9:41", font=font(F_BOLD, 30), fill=BLACK)
d.rounded_rectangle([651, 28, 821, 60], radius=16, fill=BLACK + (255,))  # island
# cellular bars
for i, hgt in enumerate((10, 15, 20, 25)):
    x = 1245 + i * 12
    d.rectangle([x, 56 - hgt, x + 8, 56], fill=BLACK)
# wifi fan (3 arcs + dot)
for r in (8, 14, 20):
    d.arc([1318 - r, 56 - r, 1318 + r, 56 + r], start=205, end=335,
          fill=BLACK, width=3)
d.ellipse([1315, 50, 1321, 56], fill=BLACK)
# battery: outline + 75% fill + nub
d.rounded_rectangle([1352, 34, 1396, 54], radius=5, outline=BLACK, width=3)
d.rectangle([1356, 38, 1385, 50], fill=BLACK)
d.rectangle([1399, 40, 1404, 48], fill=BLACK)

# ---------- 4. app header: VICE CITY POLICE DEPARTMENT ----------
d.rectangle([SX0, 70, SX1, 134], fill=DARKRED)
center_text(d, SCX, 82, "\u2605  VICE CITY POLICE DEPARTMENT  \u2605",
            font(F_BOLD, 44), WHITE)

# ---------- 5. push notification card (the hook) ----------
shadow = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([56, 164, 1416, 334], radius=28, fill=(0, 0, 0, 70))
shadow = shadow.filter(ImageFilter.GaussianBlur(6))
card.alpha_composite(shadow)
d = ImageDraw.Draw(card)
d.rounded_rectangle([56, 156, 1416, 326], radius=28, fill=WHITE + (255,))
# app icon: dark-red square, white star
d.rounded_rectangle([84, 184, 156, 256], radius=16, fill=DARKRED + (255,))
center_text(d, 120, 196, "\u2605", font(F_BOLD, 44), WHITE)
d.text((176, 180), "VICE CITY PD", font=font(F_BOLD, 28), fill=BLACK)
now = "now"
nw = d.textlength(now, font=font(F_REG, 24))
d.text((1388 - nw, 182), now, font=font(F_REG, 24), fill=GRAY)
d.text((176, 212), "FINAL NOTICE", font=font(F_BOLD, 36), fill=BLACK)
d.text((176, 254), "Your $13,587 ticket is now $510,445.",
       font=font(F_REG, 30), fill=BLACK)
d.text((176, 290), "Payment plan: 47 heists.",
       font=font(F_REG, 28), fill=GRAY)

# ---------- 6. citation body on the "app screen" ----------
info_x = 90
d.text((info_x, 356), "TO:  JASON DUVAL & LUCIA CAMINOS", font=font(F_BOLD, 30), fill=BLACK)
d.text((info_x, 398), "CASE NO.  LC-2026-1119", font=font(F_BOLD, 30), fill=BLACK)
d.text((info_x, 442), "DATE:  NOVEMBER 23, 2026", font=font(F_REG, 26), fill=GRAY)

# suspects photo: crop faces from v3 mugshot (watermark excluded), paste right
raw = Image.open(f"{V3}/mugshot_raw.jpg").convert("RGB")  # 991x594
photo = raw.crop((20, 55, 960, 540))       # 940x485, watermark cut
photo = photo.resize((340, 176), Image.LANCZOS)
px, py = 1020, 350
card.paste(photo, (px, py))
d = ImageDraw.Draw(card)
d.rectangle([px - 4, py - 4, px + 340 + 3, py + 176 + 3], outline=BLACK, width=4)
center_text(d, px + 170, 534, "SUSPECTS \u2014 STILL AT LARGE",
            font(F_BOLD, 20), GRAY)

# OVERDUE stamp (small, fully inside the photo, faces clear)
stamp = Image.new("RGBA", (200, 52), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.text((6, 6), "OVERDUE", font=font(F_BLACK, 28), fill=RED + (255,))
sd.rectangle([3, 4, 196, 47], outline=RED + (255,), width=4)
stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
card.alpha_composite(stamp, (px + 118, py + 88))
d = ImageDraw.Draw(card)

# ---------- 7. itemized fines ----------
d.line([90, 590, card_w - 90, 590], fill=BLACK, width=3)
center_text(d, card_w / 2, 606, "ITEMIZED FINES", font(F_BOLD, 34), BLACK)

rows = [
    ("ORIGINAL FINE \u2014 5 COUNTS", "$13,587"),
    ("LATE FEE \u2014 $100/DAY \u00d7 4,748 DAYS (YES, WE COUNTED)", "$474,800"),
    ("INTEREST \u2014 12% \u00d7 13 YEARS (BECAUSE WE CAN)", "$21,196"),
    ("TOWING \u2014 CAR STILL THERE", "$350"),
    ("PAPERWORK & STAMPS", "$12"),
    ("COLLECTION FEE \u2014 WE GOT TIRED OF ASKING", "$500"),
]
f_row = font(F_BOLD, 28)
y = 664
for label, amount in rows:
    d.text((90, y), label, font=f_row, fill=BLACK)
    aw = d.textlength(amount, font=f_row)
    d.text((card_w - 90 - aw, y), amount, font=f_row, fill=BLACK)
    y += 46
    if label != rows[-1][0]:
        d.line([90, y - 7, card_w - 90, y - 7], fill=LIGHTGRAY, width=2)

# total
d.line([90, 940, card_w - 90, 940], fill=BLACK, width=4)
f_tot = font(F_BOLD, 42)
f_amt = font(F_BLACK, 76)
d.text((90, 962), "TOTAL DUE", font=f_tot, fill=BLACK)
amt = "$510,445"
aw = d.textlength(amt, font=f_amt)
d.text((card_w - 90 - aw, 948), amt, font=f_amt, fill=RED)

# punchline — the payoff: "47 HEISTS" in red, sequel line bold black
f_pay = font(F_BOLD, 38)
pre = "PAYMENT PLAN AVAILABLE:  "
pay = "47 HEISTS"
tw = d.textlength(pre + pay, font=f_pay)
sx = card_w / 2 - tw / 2
d.text((sx, 1042), pre, font=f_pay, fill=BLACK)
d.text((sx + d.textlength(pre, font=f_pay), 1042), pay, font=f_pay, fill=RED)
center_text(d, card_w / 2, 1090, "FAILURE TO PAY WILL RESULT IN A SEQUEL.",
            font(F_BOLD, 28), BLACK)

# ---------- 8. iMessage-style "tap to pay" bar + home indicator ----------
d.rounded_rectangle([90, 1124, 1382, 1170], radius=23,
                    fill=WHITE + (255,), outline=(201, 189, 158), width=2)
d.text((120, 1136), "Tap to pay \u2014 47 heists accepted",
       font=font(F_REG, 26), fill=GRAY)
d.ellipse([1300, 1129, 1352, 1181], fill=RED + (255,))
center_text(d, 1326, 1134, "\u2191", font(F_BOLD, 30), WHITE)
d.rounded_rectangle([636, 1184, 836, 1194], radius=5, fill=(90, 80, 60, 255))

# ---------- 9. banner, pixel-for-pixel from v3 ----------
v3 = Image.open(f"{V3}/meme.png").convert("RGB")
banner = v3.crop(BANNER)  # 1472x252
card.paste(banner, (0, BANNER[1] - CARD[1]))
# NOTE: do NOT re-apply the rounded mask here — pasting the banner must leave
# its bottom corners opaque/square exactly like v3 (rev-1 verification).

# ---------- 10. composite + save ----------
canvas.paste(card, (CARD[0], CARD[1]), card)
canvas.save(f"{OUT}/meme.png")
lite = canvas.resize((720, 720), Image.LANCZOS)
lite.save(f"{OUT}/meme-lite.png", optimize=True)
print("saved", f"{OUT}/meme.png", canvas.size, "lite", lite.size)
