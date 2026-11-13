"""Иллюстрации к статьям журнала в стиле картинки на главной (вид сверху на ореховый стол)."""
import math, os, subprocess, random

HERE = os.path.dirname(os.path.abspath(__file__))
g = {}
exec(open(os.path.join(HERE, "hero_art.py"), encoding="utf-8").read(), g)   # текстуры, фильтры и помощники
T, defs, poly, pol, JOINT = g["T"], g["defs"], g["poly"], g["pol"], g["JOINT"]
box, chess, coaster, knife, banding, rect_band = g["box"], g["chess"], g["coaster"], g["knife"], g["banding"], g["rect_band"]

W, H = 1200, 800
OUT = os.path.join(HERE, "art")
os.makedirs(OUT, exist_ok=True)

extra_defs = '''
<pattern id="mat" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect width="40" height="40" fill="#3f5a4a"/><path d="M40 0H0V40" fill="none" stroke="#6f8a78" stroke-width="1"/>
  <path d="M20 0V40M0 20H40" fill="none" stroke="#567262" stroke-width=".5"/></pattern>
<filter id="sand" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .28  0 0 0 1.1 -.35"/></filter>
<radialGradient id="pan" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#9aa0a6"/><stop offset=".85" stop-color="#5d6268"/><stop offset="1" stop-color="#3b3f44"/></radialGradient>
<radialGradient id="sandfill" cx=".45" cy=".45" r=".6"><stop offset="0" stop-color="#e3c891"/><stop offset="1" stop-color="#b99a62"/></radialGradient>
<linearGradient id="tone" x1="0" x2="1"><stop offset="0" stop-color="#2a170b" stop-opacity=".85"/><stop offset=".55" stop-color="#2a170b" stop-opacity=".25"/><stop offset="1" stop-color="#2a170b" stop-opacity="0"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4efe4"/><stop offset="1" stop-color="#e2dccd"/></linearGradient>
<linearGradient id="tape" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9c08a"/><stop offset="1" stop-color="#c7aa6e"/></linearGradient>
<linearGradient id="glass" x1="0" x2="1"><stop offset="0" stop-color="#c9a24a"/><stop offset=".5" stop-color="#e8c873"/><stop offset="1" stop-color="#b38a35"/></linearGradient>
'''


def svg(name, body):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{"".join(defs)}{extra_defs}</defs>'
         f'<rect width="{W}" height="{H}" fill="{T["table"]}"/>{body}<rect width="{W}" height="{H}" fill="url(#vignette)"/></svg>')
    p = os.path.join(OUT, name + ".svg")
    open(p, "w", encoding="utf-8").write(s)
    return p


def tape(x, y, w, h, rot):
    return f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#tape)" opacity=".92"/></g>'


def leaf_path(cx, cy, L, ang, wdt=.34):
    a = math.radians(ang); n = (-math.sin(a), math.cos(a))
    tip = (cx + L * math.cos(a), cy + L * math.sin(a)); m = (cx + L * .5 * math.cos(a), cy + L * .5 * math.sin(a))
    full = f"M{cx:.1f} {cy:.1f} Q{m[0]+n[0]*L*wdt:.1f} {m[1]+n[1]*L*wdt:.1f} {tip[0]:.1f} {tip[1]:.1f} Q{m[0]-n[0]*L*wdt:.1f} {m[1]-n[1]*L*wdt:.1f} {cx:.1f} {cy:.1f}Z"
    half = f"M{cx:.1f} {cy:.1f} Q{m[0]+n[0]*L*wdt:.1f} {m[1]+n[1]*L*wdt:.1f} {tip[0]:.1f} {tip[1]:.1f}Z"
    return full, half


# ---------------- 1. История: классическое панно с букетом ----------------
def art_history():
    b = []
    x, y, w, h = 300, 70, 600, 660
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["wenge90"]}" filter="url(#shadow)"/>')
    b.append(rect_band(x + 22, y + 22, w - 44, h - 44, 16, 20, [T["maple0"], T["walnut0"], T["oak0"]]))
    b.append(f'<rect x="{x+42}" y="{y+42}" width="{w-84}" height="{h-84}" fill="{T["burl"]}" stroke="{JOINT}" stroke-width="2"/>')
    cx = x + w / 2
    b.append(f'<ellipse cx="{cx}" cy="{y+h/2}" rx="{w*.36}" ry="{h*.39}" fill="{T["wenge0"]}" stroke="{JOINT}" stroke-width="2"/>')
    b.append(f'<ellipse cx="{cx}" cy="{y+h/2}" rx="{w*.34}" ry="{h*.37}" fill="{T["maple90"]}" stroke="{JOINT}" stroke-width="2"/>')
    # ваза
    vy = y + h * .62
    b.append(f'<path d="M{cx-70} {vy} C{cx-95} {vy+80} {cx-60} {vy+150} {cx-40} {vy+165} L{cx+40} {vy+165} C{cx+60} {vy+150} {cx+95} {vy+80} {cx+70} {vy}Z" fill="{T["walnut90"]}" stroke="{JOINT}" stroke-width="2"/>')
    b.append(f'<path d="M{cx} {vy} L{cx+70} {vy} C{cx+95} {vy+80} {cx+60} {vy+150} {cx+40} {vy+165} L{cx} {vy+165}Z" fill="url(#sandR)"/>')
    b.append(f'<rect x="{cx-80}" y="{vy-14}" width="160" height="18" fill="{T["oak0"]}" stroke="{JOINT}" stroke-width="1.6"/>')
    # стебли и листья
    for (dx, dy, ang, L, t) in [(-120, -40, 200, 90, "olive30"), (110, -60, -20, 95, "olive150"), (-60, -150, 230, 80, "olive60"),
                                (80, -170, -50, 85, "olive120"), (-150, -120, 170, 70, "olive0"), (150, -130, 10, 70, "olive30")]:
        f, hf = leaf_path(cx + dx * .4, vy + dy * .5, L, ang)
        b.append(f'<path d="{f}" fill="{T[t]}" stroke="{JOINT}" stroke-width="1.5"/><path d="{hf}" fill="#1a0d06" opacity=".3"/>')
    # цветы
    def flower(fx, fy, r, n, t1, t2, centre):
        out = []
        for i in range(n):
            a = 2 * math.pi * i / n
            f, hf = leaf_path(fx, fy, r, math.degrees(a), .45)
            out.append(f'<path d="{f}" fill="{T[t1 if i % 2 else t2]}" stroke="{JOINT}" stroke-width="1.5"/><path d="{hf}" fill="#1a0d06" opacity=".28"/>')
        out.append(f'<circle cx="{fx}" cy="{fy}" r="{r*.28}" fill="{T[centre]}" stroke="{JOINT}" stroke-width="1.6"/><circle cx="{fx}" cy="{fy}" r="{r*.28}" fill="url(#sandC)"/>')
        return "".join(out)
    b.append(flower(cx, vy - 170, 64, 10, "padauk60", "cherry120", "oak0"))
    b.append(flower(cx - 110, vy - 95, 50, 8, "maple30", "ash60", "padauk0"))
    b.append(flower(cx + 115, vy - 110, 52, 8, "maple60", "ash30", "cherry0"))
    b.append(flower(cx - 40, vy - 260, 40, 7, "padauk0", "cherry60", "maple0"))
    b.append(flower(cx + 60, vy - 250, 36, 7, "ash30", "maple30", "walnut0"))
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/>')
    b.append(knife(80, 720, 360, 600))
    b.append(coaster(1040, 640, 95, 12))
    return svg("history", "".join(b))


# ---------------- 2. Как научиться: звезда-орнамент в процессе ----------------
def art_learn():
    b = []
    # калька с эскизом
    b.append(f'<g transform="rotate(-6 330 400)" filter="url(#soft)"><rect x="80" y="130" width="500" height="540" fill="url(#paper)" opacity=".95"/>'
             f'<g fill="none" stroke="#7d746a" stroke-width="2">')
    cx, cy, R = 330, 400, 200
    pts = [pol(cx, cy, R if i % 2 == 0 else R * .42, -math.pi / 2 + i * math.pi / 8) for i in range(16)]
    b.append('<polygon points="' + " ".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + '"/>')
    for p in pts[::2]:
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{p[0]:.0f}" y2="{p[1]:.0f}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R*1.12}"/></g></g>')
    # собранная наполовину звезда из шпона
    cx, cy, R = 820, 380, 230
    b.append(f'<rect x="{cx-R-40}" y="{cy-R-40}" width="{2*R+80}" height="{2*R+80}" fill="{T["walnut0"]}" filter="url(#shadow)"/>')
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        tip = pol(cx, cy, R, a); l = pol(cx, cy, R * .42, a - math.pi / 8); r = pol(cx, cy, R * .42, a + math.pi / 8)
        if i < 5:
            b.append(poly([(cx, cy), tip, l], T["maple45"]) + poly([(cx, cy), tip, r], T["oak-45"]))
    # недостающие лучи лежат рядом
    for k, (dx, dy, rot) in enumerate([(-130, 330, 30), (-30, 360, -20), (120, 340, 60)]):
        px, py = cx + dx, cy + dy
        b.append(f'<g transform="rotate({rot} {px} {py})" filter="url(#soft)">' +
                 poly([(px - 40, py), (px + 40, py), (px, py - 120)], T["maple45" if k % 2 == 0 else "oak-45"]) + '</g>')
    for (x, y, w, h, r) in [(650, 250, 160, 26, -35), (780, 470, 150, 26, 40), (860, 230, 140, 26, 70)]:
        b.append(tape(x, y, w, h, r))
    b.append(knife(120, 760, 620, 700))
    return svg("learn", "".join(b))


# ---------------- 4. Инструменты: раскладка на коврике ----------------
def art_tools():
    b = [f'<g filter="url(#shadow)"><rect x="120" y="90" width="960" height="620" rx="10" fill="url(#mat)"/></g>']
    # линейка
    b.append('<g transform="rotate(-8 600 170)" filter="url(#soft)"><rect x="200" y="150" width="760" height="44" fill="#c9ccd1"/>' +
             "".join(f'<line x1="{200+i*19}" y1="150" x2="{200+i*19}" y2="{168 if i%5 else 176}" stroke="#4b4f55" stroke-width="2"/>' for i in range(40)) + '</g>')
    # нож и лезвия
    b.append(knife(220, 300, 700, 260))
    for i in range(4):
        x = 780 + i * 45
        b.append(f'<g transform="rotate(15 {x} 300)" filter="url(#soft)"><path d="M{x} 270 L{x+14} 330 L{x-6} 330 Z" fill="url(#blade)"/></g>')
    # лобзик
    b.append('<g filter="url(#soft)" fill="none" stroke="#3a3d42" stroke-width="10" stroke-linecap="round">'
             '<path d="M240 420 H560 V600"/></g>'
             '<line x1="240" y1="420" x2="240" y2="600" stroke="#c9ccd1" stroke-width="3"/>'
             f'<rect x="220" y="600" width="40" height="110" rx="14" fill="{T["oak90"]}" stroke="{JOINT}" stroke-width="1.5" filter="url(#soft)"/>')
    # рулон ленты
    b.append('<g filter="url(#soft)"><circle cx="740" cy="520" r="78" fill="url(#tape)"/><circle cx="740" cy="520" r="44" fill="#3f5a4a"/>'
             '<circle cx="740" cy="520" r="44" fill="none" stroke="#a88d55" stroke-width="3"/></g>')
    # клей
    b.append('<g filter="url(#soft)"><rect x="880" y="430" width="90" height="190" rx="20" fill="#f2f0ea"/><rect x="905" y="400" width="40" height="40" rx="6" fill="#e2702f"/>'
             '<rect x="880" y="490" width="90" height="70" fill="#2f6aa8"/></g>')
    # карандаш и струбцина
    b.append('<g transform="rotate(-25 480 640)" filter="url(#soft)"><rect x="380" y="628" width="200" height="22" fill="#d9a441"/><path d="M580 628 L620 639 L580 650Z" fill="#e9c99a"/><path d="M606 635 L620 639 L606 643Z" fill="#333"/></g>')
    b.append('<g filter="url(#soft)" fill="none" stroke="#4a4e54" stroke-width="16" stroke-linejoin="round"><path d="M1010 140 H1080 V320 H1010"/></g>'
             '<line x1="1040" y1="140" x2="1040" y2="330" stroke="#8c9096" stroke-width="8"/>'
             f'<rect x="1025" y="320" width="30" height="60" rx="6" fill="{T["walnut0"]}" filter="url(#soft)"/>')
    # пачка шпона в углу
    for i, t in enumerate(["maple0", "cherry0", "oak0", "wenge0"]):
        b.append(f'<g transform="rotate({-4+i*3} 1000 640)" filter="url(#soft)"><rect x="900" y="{600+i*10}" width="250" height="90" fill="{T[t]}" stroke="{JOINT}" stroke-width="1"/></g>')
    return svg("tools", "".join(b))


# ---------------- 5. Уход: шкатулка, ткань, воск ----------------
def art_care():
    b = [box(120, 160, 620, 470, -3)]
    # мягкая ткань со складками
    b.append('<g filter="url(#soft)"><path d="M800 420 C860 380 980 400 1080 360 L1130 520 C1060 560 950 540 850 600 Z" fill="#c9c2b6"/>'
             '<path d="M820 470 C900 440 990 450 1090 420" fill="none" stroke="#a9a196" stroke-width="6"/>'
             '<path d="M840 530 C920 500 1010 505 1105 475" fill="none" stroke="#b3ab9f" stroke-width="5"/></g>')
    # банка воска
    b.append('<g filter="url(#shadow)"><circle cx="960" cy="230" r="95" fill="url(#glass)"/><circle cx="960" cy="230" r="70" fill="#d7b25c"/>'
             '<circle cx="960" cy="230" r="70" fill="none" stroke="#a9862f" stroke-width="3"/></g>')
    b.append(coaster(980, 690, 80, -10))
    return svg("care", "".join(b))


# ---------------- 6. Своими руками: эскиз → детали → готовый лист ----------------
def art_diy():
    b = []
    # 1. эскиз
    b.append('<g transform="rotate(-5 230 400)" filter="url(#soft)"><rect x="70" y="200" width="320" height="400" fill="url(#paper)"/></g>')
    f, _ = leaf_path(230, 560, 300, -90, .38)
    b.append(f'<path d="{f}" fill="none" stroke="#7d746a" stroke-width="3" transform="rotate(-5 230 400)"/>')
    b.append('<path d="M230 560 L230 270" stroke="#7d746a" stroke-width="2" fill="none" transform="rotate(-5 230 400)"/>')
    # 2. вырезанные детали россыпью
    for (x, y, ang, L, t) in [(480, 520, -70, 210, "olive30"), (560, 330, -100, 160, "olive150"), (650, 560, -60, 150, "oak30")]:
        f, hf = leaf_path(x, y, L, ang, .36)
        b.append(f'<g filter="url(#soft)"><path d="{f}" fill="{T[t]}" stroke="{JOINT}" stroke-width="1.5"/></g>')
    # 3. готовая работа в рамке
    x, y, w, h = 760, 150, 360, 480
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["wenge0"]}" filter="url(#shadow)"/>')
    b.append(rect_band(x + 16, y + 16, w - 32, h - 32, 12, 16, [T["maple0"], T["walnut0"]]))
    b.append(f'<rect x="{x+32}" y="{y+32}" width="{w-64}" height="{h-64}" fill="{T["maple90"]}" stroke="{JOINT}" stroke-width="2"/>')
    cx, cy = x + w / 2, y + h - 70
    f, hf = leaf_path(cx, cy, 330, -90, .38)
    b.append(f'<path d="{f}" fill="{T["olive90"]}" stroke="{JOINT}" stroke-width="1.6"/><path d="{hf}" fill="#1a0d06" opacity=".32"/>')
    b.append(f'<path d="M{cx} {cy} L{cx} {cy-300}" stroke="{JOINT}" stroke-width="5"/><path d="M{cx} {cy} L{cx} {cy-300}" stroke="#c6b98b" stroke-width="2.5"/>')
    for k in range(5):
        yy = cy - 60 - k * 50
        b.append(f'<path d="M{cx} {yy} l{-60+k*6} -36 M{cx} {yy} l{60-k*6} -36" stroke="{JOINT}" stroke-width="2" opacity=".55"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/>')
    # стрелки-этапы точками
    for xx in (420, 715):
        b.append("".join(f'<circle cx="{xx+i*14}" cy="400" r="3.5" fill="#d8c7a6" opacity=".7"/>' for i in range(3)))
    b.append(knife(80, 740, 520, 690))
    return svg("diy", "".join(b))


# ---------------- 7. Тонирование песком: сковорода и затемнённые лепестки ----------------
def art_sand():
    rnd = random.Random(7)
    b = []
    b.append('<rect x="640" y="372" width="330" height="56" rx="26" fill="#2f3236" transform="rotate(-8 660 400)" filter="url(#soft)"/>')
    b.append('<g filter="url(#shadow)"><circle cx="400" cy="400" r="290" fill="url(#pan)"/></g>')
    b.append('<circle cx="400" cy="400" r="250" fill="url(#sandfill)"/>')
    # песчинки
    dots = []
    for _ in range(2600):
        r = 250 * math.sqrt(rnd.random()); a = rnd.random() * 2 * math.pi
        x, y = 400 + r * math.cos(a), 400 + r * math.sin(a)
        c = rnd.choice(["#c9a96c", "#f0dcae", "#a8874d", "#e6cf98", "#b8975c"])
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1,2.4):.1f}" fill="{c}"/>')
    b.append("".join(dots))
    b.append('<circle cx="400" cy="400" r="250" fill="none" stroke="#2b2e32" stroke-width="6"/>')
    # лепесток: кончик торчит из песка, у погружённого края — тонировка
    f, hf = leaf_path(380, 430, 260, -45, .42)
    b.append('<defs><linearGradient id="dip" gradientUnits="userSpaceOnUse" x1="380" y1="430" x2="564" y2="246">'
             '<stop offset="0" stop-color="#2a1408" stop-opacity=".9"/><stop offset=".45" stop-color="#2a1408" stop-opacity=".3"/><stop offset=".8" stop-color="#2a1408" stop-opacity="0"/></linearGradient>'
             '<clipPath id="out"><rect x="0" y="0" width="1200" height="800"/></clipPath></defs>')
    b.append(f'<g filter="url(#soft)"><path d="{f}" fill="{T["maple30"]}" stroke="{JOINT}" stroke-width="1.6"/></g><path d="{f}" fill="url(#dip)"/>')
    # песок, присыпавший основание
    mound = []
    for _ in range(700):
        r = 70 * math.sqrt(rnd.random()); a = rnd.random() * 2 * math.pi
        x, y = 395 + r * math.cos(a) * 1.25, 430 + r * math.sin(a)
        mound.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.2,2.6):.1f}" fill="{rnd.choice(["#d9bf87","#f0dcae","#b8975c","#c9a96c"])}"/>')
    b.append('<ellipse cx="395" cy="430" rx="88" ry="70" fill="#d7bc84"/>' + "".join(mound))
    # пинцет держит лепесток
    b.append('<g filter="url(#soft)" stroke-linecap="round"><line x1="520" y1="300" x2="820" y2="90" stroke="#8d939a" stroke-width="16"/>'
             '<line x1="535" y1="318" x2="838" y2="110" stroke="#b4b9bf" stroke-width="16"/></g>')
    # готовые тонированные лепестки на столе
    for i, (x, y, ang, t) in enumerate([(820, 600, -30, "maple0"), (930, 660, -70, "ash0"), (1040, 600, -110, "maple60"), (880, 500, -5, "ash30")]):
        f, hf = leaf_path(x, y, 170, ang, .45)
        tid = f"tn{i}"
        x2, y2 = x + 170 * math.cos(math.radians(ang)), y + 170 * math.sin(math.radians(ang))
        b.append(f'<defs><linearGradient id="{tid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="{y}" x2="{x2:.0f}" y2="{y2:.0f}">'
                 f'<stop offset="0" stop-color="#3a1f0e" stop-opacity=".85"/><stop offset=".5" stop-color="#3a1f0e" stop-opacity=".25"/><stop offset="1" stop-color="#3a1f0e" stop-opacity="0"/></linearGradient></defs>')
        b.append(f'<g filter="url(#soft)"><path d="{f}" fill="{T[t]}" stroke="{JOINT}" stroke-width="1.5"/></g><path d="{f}" fill="url(#{tid})"/>')
    return svg("sand", "".join(b))


def art_table_only():
    return svg("table", "")


def render(paths):
    js = os.path.join(HERE, "render_many.js")
    open(js, "w").write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 800 } });
for (const f of process.argv.slice(2)) { await p.goto('file://' + f); await p.waitForTimeout(800); await p.screenshot({ path: f.replace('.svg', '.png') }); }
await b.close(); })();''')
    subprocess.run(["node", js] + paths, check=True)


if __name__ == "__main__":
    ps = [art_history(), art_learn(), art_tools(), art_care(), art_diy(), art_sand(), art_table_only()]
    render(ps)
    print("ok", len(ps))
