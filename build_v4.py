#!/usr/bin/env python3
"""Build GTA 6 meme v4 — 'FINAL NOTICE' (1600x1600) for make.fun gta6-meme-x-01.
Back to v2's winning format (Vice City PD paperwork): the $13,587 ticket was
never paid, so 13 years of late fees + interest + admin blew it up to
$510,445. Pattern: v2 neon art background (darkened) + PIL text overlay.
The magenta make.fun banner is cropped pixel-for-pixel from v3's meme.png
(y 1300-1552) and pasted at the identical coordinates. Suspects photo is
cropped from v3's mugshot art (Lucia cyan + Jason magenta; watermark cut).
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

# ---------- 2. ticket card (rounded) on its own layer ----------
card_w = CARD[2] - CARD[0]
card_h = CARD[3] - CARD[1]
layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
mask = Image.new("L", (card_w, card_h), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=40, fill=255)
card = Image.new("RGBA", (card_w, card_h), PAPER + (255,))
card.putalpha(mask)
d = ImageDraw.Draw(card)

# inner thin double border (classic official-form frame)
d.rectangle([26, 26, card_w - 27, card_h - 27], outline=BLACK, width=3)
d.rectangle([36, 36, card_w - 37, card_h - 37], outline=BLACK, width=1)

# top band: dark red, full card width (clipped by rounded mask)
d.rectangle([0, 0, card_w - 1, 89], fill=DARKRED)
center_text(d, card_w / 2, 18, "\u2605  VICE CITY POLICE DEPARTMENT  \u2605",
            font(F_BOLD, 52), WHITE)

# headline
center_text(d, card_w / 2, 108, "FINAL NOTICE", font(F_BLACK, 140), BLACK)
center_text(d, card_w / 2, 268, "13 YEARS OVERDUE \u2014 THIS IS YOUR LAST WARNING",
            font(F_BOLD, 34), RED)

# ---------- 3. info block (left) + suspects photo (right) ----------
info_x = 90
d.text((info_x, 340), "TO:  JASON DUVAL & LUCIA CAMINOS", font=font(F_BOLD, 30), fill=BLACK)
d.text((info_x, 384), "CASE NO.  LC-2026-1119", font=font(F_BOLD, 30), fill=BLACK)
d.text((info_x, 428), "DATE:  NOVEMBER 23, 2026", font=font(F_REG, 28), fill=GRAY)
d.text((info_x, 468), "RE:  TICKET #1337 \u2014 NEVER PAID", font=font(F_REG, 28), fill=GRAY)

# suspects photo: crop faces from v3 mugshot (watermark excluded), paste right
raw = Image.open(f"{V3}/mugshot_raw.jpg").convert("RGB")  # 991x594
photo = raw.crop((20, 55, 960, 540))       # 940x485, watermark cut
photo = photo.resize((420, 217), Image.LANCZOS)
px, py = 970, 330
card.paste(photo, (px, py))
d.rectangle([px - 5, py - 5, px + 420 + 4, py + 217 + 4], outline=BLACK, width=4)
center_text(d, px + 210, 556, "SUSPECTS \u2014 STILL AT LARGE",
            font(F_BOLD, 22), GRAY)

# ---------- 4. itemized fines ----------
d.line([90, 610, card_w - 90, 610], fill=BLACK, width=3)
center_text(d, card_w / 2, 628, "ITEMIZED FINES", font(F_BOLD, 36), BLACK)

rows = [
    ("ORIGINAL FINE \u2014 5 COUNTS", "$13,587"),
    ("LATE FEE \u2014 $100/DAY \u00d7 4,748 DAYS", "$474,800"),
    ("INTEREST \u2014 12% \u00d7 13 YEARS", "$21,196"),
    ("TOWING \u2014 CAR STILL THERE", "$350"),
    ("PAPERWORK & STAMPS", "$12"),
    ("COLLECTION FEE \u2014 WE GOT TIRED OF ASKING", "$500"),
]
f_row = font(F_BOLD, 30)
y = 684
for label, amount in rows:
    d.text((90, y), label, font=f_row, fill=BLACK)
    aw = d.textlength(amount, font=f_row)
    d.text((card_w - 90 - aw, y), amount, font=f_row, fill=BLACK)
    y += 52
    if label != rows[-1][0]:
        d.line([90, y - 8, card_w - 90, y - 8], fill=LIGHTGRAY, width=2)

# total
d.line([90, 1002, card_w - 90, 1002], fill=BLACK, width=4)
f_tot = font(F_BOLD, 44)
f_amt = font(F_BLACK, 84)
d.text((90, 1024), "TOTAL DUE", font=f_tot, fill=BLACK)
amt = "$510,445"
aw = d.textlength(amt, font=f_amt)
d.text((card_w - 90 - aw, 1006), amt, font=f_amt, fill=RED)

# punchline
center_text(d, card_w / 2, 1118, "PAYMENT PLAN AVAILABLE:  47 HEISTS",
            font(F_BOLD, 34), BLACK)
center_text(d, card_w / 2, 1162, "FAILURE TO PAY WILL RESULT IN A SEQUEL.",
            font(F_REG, 26), GRAY)

# ---------- 5. OVERDUE stamp (rotated, over the photo, clear of caption) ----------
stamp = Image.new("RGBA", (340, 95), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.text((12, 12), "OVERDUE", font=font(F_BLACK, 52), fill=RED + (255,))
sd.rectangle([4, 8, 335, 86], outline=RED + (255,), width=5)
stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
card.alpha_composite(stamp, (px + 30, py + 30))

# ---------- 6. banner, pixel-for-pixel from v3 ----------
v3 = Image.open(f"{V3}/meme.png").convert("RGB")
banner = v3.crop(BANNER)  # 1472x252
card.paste(banner, (0, BANNER[1] - CARD[1]))

# ---------- 7. composite + save ----------
canvas.paste(card, (CARD[0], CARD[1]), card)
canvas.save(f"{OUT}/meme.png")
lite = canvas.resize((720, 720), Image.LANCZOS)
lite.save(f"{OUT}/meme-lite.png", optimize=True)
print("saved", f"{OUT}/meme.png", canvas.size, "lite", lite.size)
