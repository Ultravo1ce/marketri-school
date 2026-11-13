"""Схема «Как добраться»: метро «Пролетарская», выход № 2 → Брошевский переулок, 4.
Координаты сняты со скриншота Яндекс Карт (2032×1144), схема — в его системе координат."""

OUT = "/home/claude/marketri-site/img/"

L = {
    "ru": {
        "abel": "Абельмановская ул.", "marks": "Марксистская ул.", "volg": "Волгоградский просп.",
        "morev": "Моревский пр.", "brosh": "Брошевский пер.", "stroy": "Стройковская ул.", "tal": "ул. Талалихина",
        "sq": "Крестьянский сквер", "zastava": "пл. Крестьянская Застава", "theatre": "Театр марионеток",
        "metro": "Пролетарская", "exit": "выход 2", "school1": "Школа маркетри", "school2": "Брошевский пер., 4",
        "north": "С",
    },
    "en": {
        "abel": "Abelmanovskaya St", "marks": "Marksistskaya St", "volg": "Volgogradsky Ave",
        "morev": "Morevsky Pr", "brosh": "Broshevsky Ln", "stroy": "Stroykovskaya St", "tal": "Talalikhina St",
        "sq": "Krestyansky Square", "zastava": "Krestyanskaya Zastava Sq", "theatre": "Puppet Theatre",
        "metro": "Proletarskaya", "exit": "exit 2", "school1": "School of Marquetry", "school2": "4 Broshevsky Ln",
        "north": "N",
    },
}

BG, BLOCK, PARK, ROAD, EDGE = "#F1EDE6", "#E6DFD3", "#D9E3CF", "#FFFFFF", "#D6CDBF"
INK, MUTED, ROUTE, ACCENT = "#26211C", "#6E655C", "#A65F3C", "#3F4A3A"
FONT = "'Golos Text', 'Segoe UI', Arial, sans-serif"

ROADS = [  # (точки, ширина)
    ([(-50, 870), (300, 755), (560, 640), (1000, 420), (1250, 250), (1480, 85), (1600, -20)], 78),   # Абельмановская
    ([(430, -20), (500, 300), (560, 600)], 44),                                                     # Марксистская
    ([(575, 640), (618, 900), (660, 1180)], 54),                                                    # Волгоградский
    ([(1015, 430), (1110, 690), (1160, 1180)], 18),                                                 # Моревский
    ([(1205, 262), (1255, 350), (1300, 430), (1500, 386), (1745, 380), (2080, 432)], 20),           # Брошевский
    ([(680, 1180), (1300, 1050), (2080, 910)], 24),                                                 # Стройковская
    ([(2000, 380), (1975, 1180)], 24),                                                              # Талалихина
    ([(-50, 1050), (380, 960), (560, 900)], 30),                                                    # к югу от площади
]

ROUTE_PTS = [(302, 798), (405, 748), (520, 693), (556, 676), (590, 652), (700, 600), (790, 556),
             (880, 510), (1010, 440), (1120, 362), (1200, 290), (1222, 300), (1258, 362), (1300, 432),
             (1420, 396), (1500, 380), (1745, 378), (1782, 352)]

STEPS = [(302, 798), (585, 655), (1205, 292), (1782, 352)]


def path(pts):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)


def label(x, y, text, rot=0, size=26, color=MUTED, weight=400, anchor="middle", italic=False, halo=True):
    st = ' font-style="italic"' if italic else ""
    t = (f'<text x="{x}" y="{y}" transform="rotate({rot} {x} {y})" font-family="{FONT}" font-size="{size}" '
         f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" dominant-baseline="middle"{st}')
    h = f'{t} stroke="{BG}" stroke-width="7" stroke-linejoin="round" paint-order="stroke">{text}</text>' if halo else f"{t}>{text}</text>"
    return h


def build(lang):
    t = L[lang]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="120 110 1912 900" width="1912" height="900" role="img">',
         f'<rect x="0" y="0" width="2200" height="1300" fill="{BG}"/>']
    # кварталы-подложки и парки
    for (x, y, w, h) in [(620, 40, 280, 220), (940, 40, 260, 170), (640, 560, 330, 300), (1090, 470, 420, 330),
                         (1540, 440, 380, 400), (1350, 120, 520, 210), (700, 900, 400, 120), (1200, 860, 600, 140),
                         (150, 380, 280, 230), (330, 820, 230, 120)]:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{BLOCK}"/>')
    o.append(f'<path d="M190 690 C260 640 420 630 520 690 L470 770 C380 800 250 790 190 760Z" fill="{PARK}"/>')
    o.append(f'<path d="M640 520 L1180 250 L1230 290 L700 560Z" fill="{PARK}" opacity=".8"/>')
    o.append(f'<path d="M1560 520 C1640 500 1700 560 1680 640 C1660 700 1580 700 1560 640Z" fill="{PARK}"/>')
    # дороги: подложка-кромка и полотно
    for pts, w in ROADS:
        o.append(f'<path d="{path(pts)}" fill="none" stroke="{EDGE}" stroke-width="{w+6}" stroke-linecap="round" stroke-linejoin="round"/>')
    for pts, w in ROADS:
        o.append(f'<path d="{path(pts)}" fill="none" stroke="{ROAD}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    # переход через Волгоградский
    o.append('<g opacity=".55">' + "".join(
        f'<rect x="{560+i*9}" y="{640+i*-3}" width="5" height="34" fill="{EDGE}" transform="rotate(-58 {575} {655})"/>' for i in range(7)) + '</g>')
    # подписи улиц
    o += [label(860, 470, t["abel"], -27, 30, INK, 500), label(492, 270, t["marks"], 77, 24),
          label(612, 860, t["volg"], 81, 24), label(1105, 640, t["morev"], 70, 20),
          label(1640, 405, t["brosh"], 1, 22, INK, 500), label(1750, 962, t["stroy"], -10, 22),
          label(1985, 760, t["tal"], -88, 20), label(330, 710, t["sq"], -8, 22, "#5d7154", italic=True),
          label(420, 905, t["zastava"], -18, 20)]
    # ориентир: театр
    o.append(f'<circle cx="905" cy="520" r="9" fill="{ACCENT}"/>')
    o.append(label(925, 548, t["theatre"], 0, 22, ACCENT, 500, "start"))
    # маршрут: белая подложка + пунктир
    o.append(f'<path d="{path(ROUTE_PTS)}" fill="none" stroke="#fff" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    o.append(f'<path d="{path(ROUTE_PTS)}" fill="none" stroke="{ROUTE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 18"/>')
    o.append(f'<path d="{path(ROUTE_PTS)}" fill="none" stroke="{ROUTE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 20" opacity="0"/>')
    # номера этапов (2 и 3 — на маршруте)
    for n, (x, y) in enumerate(STEPS[1:3], start=2):
        o.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{ROUTE}" stroke="#fff" stroke-width="5"/>')
        o.append(f'<text x="{x}" y="{y+1}" font-family="{FONT}" font-size="24" font-weight="600" fill="#fff" text-anchor="middle" dominant-baseline="middle">{n}</text>')
    # старт: метро, выход 2
    x, y = STEPS[0]
    o.append(f'<circle cx="{x}" cy="{y}" r="34" fill="#943E90" stroke="#fff" stroke-width="6"/>')
    o.append(f'<text x="{x}" y="{y+2}" font-family="{FONT}" font-size="34" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">{"M" if lang == "en" else "М"}</text>')
    o.append(f'<circle cx="{x+30}" cy="{y-28}" r="17" fill="{ROUTE}" stroke="#fff" stroke-width="4"/>')
    o.append(f'<text x="{x+30}" y="{y-27}" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">1</text>')
    o.append(label(x - 6, y + 64, t["metro"], 0, 28, INK, 600))
    o.append(label(x - 6, y + 96, t["exit"], 0, 22, MUTED))
    # финиш: мастерская
    x, y = STEPS[3]
    o.append(f'<path d="M{x} {y+8} C{x-38} {y-40} {x-38} {y-92} {x} {y-92} C{x+38} {y-92} {x+38} {y-40} {x} {y+8}Z" fill="{INK}" stroke="#fff" stroke-width="5"/>')
    o.append(f'<g transform="translate({x-19} {y-79}) scale(1.2)"><polygon points="16,1 31,16 16,16" fill="#E3CFAE"/><polygon points="31,16 16,31 16,16" fill="#5A3E2B"/>'
             f'<polygon points="16,31 1,16 16,16" fill="#E3CFAE"/><polygon points="1,16 16,1 16,16" fill="#A9805A"/></g>')
    o.append(f'<circle cx="{x+28}" cy="{y-82}" r="17" fill="{ROUTE}" stroke="#fff" stroke-width="4"/>')
    o.append(f'<text x="{x+28}" y="{y-81}" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle" dominant-baseline="middle">4</text>')
    o.append(label(x, y - 130, t["school1"], 0, 28, INK, 600))
    o.append(label(x, y - 162, t["school2"], 0, 22, MUTED))
    # стрелка севера
    o.append(f'<g transform="translate(1960 190)"><circle r="34" fill="#fff" stroke="{EDGE}" stroke-width="3"/>'
             f'<path d="M0 -22 L11 10 L0 4 L-11 10Z" fill="{INK}"/>'
             f'<text y="-46" font-family="{FONT}" font-size="22" font-weight="600" fill="{INK}" text-anchor="middle">{t["north"]}</text></g>')
    o.append("</svg>")
    open(OUT + f"route-{lang}.svg", "w", encoding="utf-8").write("".join(o))


if __name__ == "__main__":
    build("ru"); build("en")
    print("ok")
