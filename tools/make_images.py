"""Заглушки фотографий (SVG в духе маркетри), иконки сайта и картинка для превью ссылок."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/claude/marketri-site"
IMG = OUT + "/img"
os.makedirs(IMG, exist_ok=True)

WOOD = {
    "maple": "#E6D3B3", "birch": "#D8C29E", "ash": "#CDBB9C", "oak": "#B48A5E",
    "cherry": "#9A5B3C", "walnut": "#5B4030", "wenge": "#3A2B22", "olive": "#7C7650",
}
PAL = [
    ("maple", "oak", "walnut"), ("birch", "cherry", "wenge"), ("ash", "olive", "walnut"),
    ("maple", "cherry", "walnut"), ("birch", "oak", "wenge"),
]


def tones(i):
    return [WOOD[k] for k in PAL[i % len(PAL)]]


def wrap(w, h, defs, body):
    label_w = 176
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>{defs}
<pattern id="grain" width="300" height="9" patternUnits="userSpaceOnUse"><path d="M0 4 Q75 2 150 4 T300 4" fill="none" stroke="#000" stroke-opacity=".07" stroke-width=".8"/></pattern>
</defs>
{body}
<rect width="{w}" height="{h}" fill="url(#grain)"/>
<rect x="20" y="{h-60}" width="{label_w}" height="38" rx="2" fill="#F6F5F2" fill-opacity=".93"/>
<text x="36" y="{h-35}" font-family="Arial, sans-serif" font-size="15" fill="#6E655C">Место для фото</text>
</svg>'''


def stripes(w, h, t, angle=60, sw=34):
    n = len(t)
    rects = "".join(f'<rect x="{i*sw}" width="{sw}" height="10" fill="{c}"/>' for i, c in enumerate(t))
    defs = f'<pattern id="p" width="{n*sw}" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate({angle})">{rects}</pattern>'
    return wrap(w, h, defs, f'<rect width="{w}" height="{h}" fill="url(#p)"/>')


def checker(w, h, t, s=70):
    a, b = t[0], t[2]
    defs = (f'<pattern id="p" width="{2*s}" height="{2*s}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="{2*s}" height="{2*s}" fill="{a}"/><rect width="{s}" height="{s}" fill="{b}"/>'
            f'<rect x="{s}" y="{s}" width="{s}" height="{s}" fill="{b}"/></pattern>')
    return wrap(w, h, defs, f'<rect width="{w}" height="{h}" fill="url(#p)"/>')


def cubes(w, h, t, s=44):
    W = s * math.sqrt(3)
    H = 3 * s

    def cube(cx, cy):
        top = f"{cx},{cy-s} {cx+W/2},{cy-s/2} {cx},{cy} {cx-W/2},{cy-s/2}"
        left = f"{cx-W/2},{cy-s/2} {cx},{cy} {cx},{cy+s} {cx-W/2},{cy+s/2}"
        right = f"{cx},{cy} {cx+W/2},{cy-s/2} {cx+W/2},{cy+s/2} {cx},{cy+s}"
        return (f'<polygon points="{top}" fill="{t[0]}"/><polygon points="{left}" fill="{t[1]}"/>'
                f'<polygon points="{right}" fill="{t[2]}"/>')

    centers = [(0, 0), (W, 0), (W / 2, 1.5 * s), (0, 3 * s), (W, 3 * s)]
    inner = "".join(cube(x, y) for x, y in centers)
    defs = f'<pattern id="p" width="{W:.2f}" height="{H}" patternUnits="userSpaceOnUse">{inner}</pattern>'
    return wrap(w, h, defs, f'<rect width="{w}" height="{h}" fill="url(#p)"/>')


def sunburst(w, h, t, n=28):
    cx, cy = w / 2, h * .55
    r = math.hypot(w, h)
    parts = [f'<rect width="{w}" height="{h}" fill="{t[0]}"/>']
    for i in range(n):
        if i % 2:
            continue
        a1, a2 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p = f"M{cx},{cy} L{cx+r*math.cos(a1):.1f},{cy+r*math.sin(a1):.1f} L{cx+r*math.cos(a2):.1f},{cy+r*math.sin(a2):.1f}Z"
        parts.append(f'<path d="{p}" fill="{t[1]}"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{min(w,h)*.09:.0f}" fill="{t[2]}"/>')
    return wrap(w, h, "", "".join(parts))


def save(name, svg):
    with open(f"{IMG}/{name}.svg", "w", encoding="utf-8") as f:
        f.write(svg)


def plain(w, h):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" fill="#E2DBD0"/>
<rect x="12" y="12" width="{w-24}" height="{h-24}" fill="none" stroke="#D2C9BB"/>
<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" letter-spacing="3" fill="#958A7C">МЕСТО ДЛЯ ФОТО</text>
</svg>'''


save("hero", plain(800, 1000))
save("master", plain(800, 1000))
save("process", plain(1200, 800))
sizes = [(800, 1000), (800, 600), (800, 800), (800, 1100), (800, 640), (800, 900)]
for i in range(9):
    save(f"g{i+1:02d}", plain(*sizes[i % len(sizes)]))
for i in range(6):
    save(f"s{i+1:02d}", plain(*sizes[(i + 2) % len(sizes)]))

# ---------- Иконки ----------
MARK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<polygon points="16,1 31,16 16,16" fill="#E3CFAE"/><polygon points="31,16 16,31 16,16" fill="#5A3E2B"/>
<polygon points="16,31 1,16 16,16" fill="#E3CFAE"/><polygon points="1,16 16,1 16,16" fill="#A9805A"/>
</svg>'''
with open(OUT + "/favicon.svg", "w") as f:
    f.write(MARK)


def mark_png(size, pad=0, bg=None):
    im = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = (size - 2 * pad) / 32

    def P(*pts):
        return [(pad + x * s, pad + y * s) for x, y in pts]
    d.polygon(P((16, 1), (31, 16), (16, 16)), fill="#E3CFAE")
    d.polygon(P((31, 16), (16, 31), (16, 16)), fill="#5A3E2B")
    d.polygon(P((16, 31), (1, 16), (16, 16)), fill="#E3CFAE")
    d.polygon(P((1, 16), (16, 1), (16, 16)), fill="#A9805A")
    return im


mark_png(32).save(OUT + "/favicon-32.png")
mark_png(180, pad=26, bg="#F6F5F2").save(OUT + "/apple-touch-icon.png")
mark_png(512, pad=72, bg="#F6F5F2").save(OUT + "/icon-512.png")

# ---------- Превью для соцсетей и мессенджеров ----------
og = Image.new("RGB", (1200, 630), "#F6F5F2")
d = ImageDraw.Draw(og)
# полоса шпона справа
for x in range(-700, 1300, 24):
    for k, c in enumerate(["#E3CFAE", "#5A3E2B", "#A9805A"]):
        x0 = x + k * 8
        d.polygon([(760 + x0, 630), (760 + x0 + 8, 630), (760 + x0 + 8 + 364, 0), (760 + x0 + 364, 0)], fill=c)
d.rectangle([0, 0, 760, 630], fill="#F6F5F2")
serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
d.text((80, 190), "Школа маркетри", font=ImageFont.truetype(serif, 66), fill="#26211C")
d.text((80, 275), "Татьяны Гориной", font=ImageFont.truetype(serif, 66), fill="#26211C")
d.text((80, 400), "Обучение наборной мозаике из шпона", font=ImageFont.truetype(sans, 30), fill="#6E655C")
og.save(OUT + "/img/og.jpg", quality=88)
print("ok")
