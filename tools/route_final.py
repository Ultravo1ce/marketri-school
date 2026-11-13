"""Итоговая схема: реальная подложка (webp внутри SVG) + маршрут, отметки и подписи на двух языках."""
import base64, io
import numpy as np
from PIL import Image
import route_map as RM          # подписи и стили из прежней схемы

S = "/tmp/claude-0/-home-claude/23972080-ba8e-5850-81e6-f070dcea3db4/scratchpad/"
OUT = "/home/claude/marketri-site/img/"
W, H = 2031, 1144
FONT, INK, MUTED, ROUTE, ACCENT, BG = RM.FONT, RM.INK, RM.MUTED, RM.ROUTE, RM.ACCENT, "#F1EDE6"

pts = [tuple(p) for p in np.load(S + "route_pts.npy")]
cut = next(i for i, p in enumerate(pts) if p[0] > 1730)          # отрезаем хвост к чужому значку
route = pts[:cut + 1] + [(1784, 372)]
END = (1786, 350)
STEPS = [route[0], (560, 676), (1213, 276), END]

buf = io.BytesIO()
Image.open(S + "route_base.png").convert("RGB").save(buf, "WEBP", quality=72, method=6)
b64 = base64.b64encode(buf.getvalue()).decode()


def lab(x, y, text, rot=0, size=26, color=MUTED, weight=400, anchor="middle", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" transform="rotate({rot} {x} {y})" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}" dominant-baseline="middle" stroke="#fff" stroke-width="7" stroke-linejoin="round" paint-order="stroke"{st}>{text}</text>')


def build(lang):
    t = RM.L[lang]
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in route)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
         f'<image href="data:image/webp;base64,{b64}" x="0" y="0" width="{W}" height="{H}"/>']
    # подписи улиц — по реальным осям
    o += [lab(1395, 92, t["abel"], -35, 30, INK, 500), lab(790, 455, t["abel"], -27, 28, INK, 500),
          lab(498, 150, t["marks"], 78, 24), lab(622, 870, t["volg"], 82, 24),
          lab(1098, 560, t["morev"], 66, 21), lab(1600, 396, t["brosh"], -1, 23, INK, 500),
          lab(1720, 960, t["stroy"], -11, 23), lab(1975, 900, t["tal"], -87, 21),
          lab(330, 700, t["sq"], -6, 22, "#5d7154", italic=True), lab(470, 930, t["zastava"], 0, 21)]
    # ориентиры
    o.append(f'<circle cx="944" cy="511" r="10" fill="{ACCENT}" stroke="#fff" stroke-width="4"/>')
    o.append(lab(962, 538, t["theatre"], 0, 22, ACCENT, 600, "start"))
    o.append(lab(1300, 352, "9 с10" if lang == "ru" else "9 bldg 10", 0, 19, MUTED, 500))
    # маршрут
    o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" stroke-linejoin="round" opacity=".95"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{ROUTE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 19"/>')
    for n, (x, y) in enumerate(STEPS[1:3], start=2):
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{ROUTE}" stroke="#fff" stroke-width="5"/>'
                 f'<text x="{x:.0f}" y="{y+1:.0f}" font-family="{FONT}" font-size="24" font-weight="600" fill="#fff" text-anchor="middle" dominant-baseline="middle">{n}</text>')
    # старт
    x, y = STEPS[0]
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="#943E90" stroke="#fff" stroke-width="6"/>'
             f'<text x="{x:.0f}" y="{y+2:.0f}" font-family="{FONT}" font-size="34" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">{"M" if lang == "en" else "М"}</text>'
             f'<circle cx="{x+30:.0f}" cy="{y-28:.0f}" r="17" fill="{ROUTE}" stroke="#fff" stroke-width="4"/>'
             f'<text x="{x+30:.0f}" y="{y-27:.0f}" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">1</text>')
    o.append(lab(x - 10, y + 62, t["metro"], 0, 28, INK, 600))
    o.append(lab(x - 10, y + 94, t["exit"], 0, 22, MUTED))
    # финиш
    x, y = END
    o.append(f'<path d="M{x} {y+8} C{x-38} {y-40} {x-38} {y-92} {x} {y-92} C{x+38} {y-92} {x+38} {y-40} {x} {y+8}Z" fill="{INK}" stroke="#fff" stroke-width="5"/>'
             f'<g transform="translate({x-19} {y-79}) scale(1.2)"><polygon points="16,1 31,16 16,16" fill="#E3CFAE"/><polygon points="31,16 16,31 16,16" fill="#5A3E2B"/>'
             f'<polygon points="16,31 1,16 16,16" fill="#E3CFAE"/><polygon points="1,16 16,1 16,16" fill="#A9805A"/></g>'
             f'<circle cx="{x+28}" cy="{y-82}" r="17" fill="{ROUTE}" stroke="#fff" stroke-width="4"/>'
             f'<text x="{x+28}" y="{y-81}" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">4</text>')
    o.append(lab(x, y - 130, t["school1"], 0, 28, INK, 600))
    o.append(lab(x, y - 162, t["school2"], 0, 22, MUTED))
    # север
    o.append(f'<g transform="translate(1960 80)"><circle r="34" fill="#fff" stroke="#D6CDBF" stroke-width="3"/>'
             f'<path d="M0 -22 L11 10 L0 4 L-11 10Z" fill="{INK}"/></g>'
             f'<text x="1960" y="140" font-family="{FONT}" font-size="22" font-weight="600" fill="{INK}" text-anchor="middle">{t["north"]}</text>')
    o.append("</svg>")
    open(OUT + f"route-{lang}.svg", "w", encoding="utf-8").write("".join(o))


build("ru"); build("en")
import os
print("ok", os.path.getsize(OUT + "route-ru.svg") // 1024, "KB")
