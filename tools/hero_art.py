"""Иллюстрация для первого экрана: композиция работ в технике маркетри (вид сверху)."""
import math

W, H = 1600, 2000
defs, body = [], []
JOINT = "#24170f"

# ---------- текстуры шпона ----------
def wood(pid, base, line, fx, fy, seed, angle=0, size=900, alpha=0.55, octaves=3):
    """Шпон: базовый цвет + волокна из шума (fx<<fy — волокна по горизонтали)."""
    defs.append(f'''
<filter id="f-{pid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{fx} {fy}" numOctaves="{octaves}" seed="{seed}" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  {2.6*alpha} 0 0 0 {-1.05*alpha}"/>
</filter>
<filter id="g-{pid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{fx*0.5} {fy*0.35}" numOctaves="2" seed="{seed+7}" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0.5 0 0 -0.22"/>
</filter>
<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" patternTransform="rotate({angle})">
  <rect width="{size}" height="{size}" fill="{base}"/>
  <rect width="{size}" height="{size}" fill="{line}" filter="url(#f-{pid})"/>
  <rect width="{size}" height="{size}" filter="url(#g-{pid})"/>
</pattern>''')
    return f"url(#{pid})"


def burl(pid, base, line, seed):
    defs.append(f'''
<filter id="f-{pid}" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022 0.016" numOctaves="5" seed="{seed}" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 1.9 0 -0.82" result="a"/>
  <feTurbulence type="turbulence" baseFrequency="0.09" numOctaves="2" seed="{seed+3}" result="m"/>
  <feColorMatrix in="m" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.9 0 0 0 -0.55" result="b"/>
  <feMerge><feMergeNode in="a"/><feMergeNode in="b"/></feMerge>
</filter>
<pattern id="{pid}" width="700" height="700" patternUnits="userSpaceOnUse">
  <rect width="700" height="700" fill="{base}"/>
  <rect width="700" height="700" fill="{line}" filter="url(#f-{pid})"/>
</pattern>''')
    return f"url(#{pid})"


T = {}
def mk(name, base, line, angle=0, fx=0.003, fy=0.16, seed=1, alpha=0.55):
    T[name] = wood(name, base, line, fx, fy, seed, angle, alpha=alpha)

# Палитра пород
for a in (0, 90, 45, -45, 30, 60, 120, 150):
    s = abs(a) + 3
    mk(f"maple{a}", "#ead9b8", "#b89a6a", a, seed=s, alpha=.35)
    mk(f"oak{a}", "#c0915d", "#7a5532", a, seed=s + 1, alpha=.6)
    mk(f"cherry{a}", "#a65f3c", "#5e2e18", a, seed=s + 2, alpha=.5)
    mk(f"walnut{a}", "#5f4332", "#2b1b12", a, seed=s + 3, alpha=.6)
    mk(f"wenge{a}", "#3a2a21", "#130b07", a, seed=s + 4, alpha=.7)
    mk(f"ash{a}", "#d8c7a6", "#9a8463", a, seed=s + 5, alpha=.45)
    mk(f"olive{a}", "#77744b", "#3e3c22", a, seed=s + 6, alpha=.5)
    mk(f"padauk{a}", "#b2492c", "#6a2414", a, seed=s + 7, alpha=.45)
T["table"] = wood("table", "#4a3427", "#20140d", 0.0012, 0.07, 41, 2, size=1800, alpha=.5, octaves=4)
T["burl"] = burl("burl", "#8a5f3f", "#3e2617", 9)

# Тени, тонирование песком
defs.append('''
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#0b0604" flood-opacity=".55"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0b0604" flood-opacity=".5"/>
</filter>
<linearGradient id="sandL" x1="0" x2="1"><stop offset="0" stop-color="#1a0d06" stop-opacity=".55"/><stop offset=".55" stop-color="#1a0d06" stop-opacity="0"/></linearGradient>
<linearGradient id="sandR" x1="1" x2="0"><stop offset="0" stop-color="#1a0d06" stop-opacity=".5"/><stop offset=".6" stop-color="#1a0d06" stop-opacity="0"/></linearGradient>
<linearGradient id="sandT" y1="0" y2="1"><stop offset="0" stop-color="#1a0d06" stop-opacity=".45"/><stop offset=".6" stop-color="#1a0d06" stop-opacity="0"/></linearGradient>
<radialGradient id="sandC"><stop offset=".55" stop-color="#1a0d06" stop-opacity="0"/><stop offset="1" stop-color="#1a0d06" stop-opacity=".55"/></radialGradient>
<radialGradient id="vignette" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>
<linearGradient id="blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9eaec"/><stop offset=".5" stop-color="#a9adb3"/><stop offset="1" stop-color="#6f737a"/></linearGradient>
''')


def poly(pts, fill, extra=""):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    sw = "" if "stroke-width" in extra else 'stroke-width="1.6"'
    st = "" if "stroke=" in extra.replace("stroke-width", "") else f'stroke="{JOINT}"'
    return f'<polygon points="{p}" fill="{fill}" {st} {sw} stroke-linejoin="round" {extra}/>'


def pol(cx, cy, r, a):
    return cx + r * math.cos(a), cy + r * math.sin(a)


def banding(cx, cy, r1, r2, n, cols):
    """Кольцевая «верёвочная» окантовка из косых сегментов."""
    out = []
    for i in range(n):
        a1, a2 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        sk = math.pi / n * .9
        pts = [pol(cx, cy, r1, a1), pol(cx, cy, r1, a2), pol(cx, cy, r2, a2 + sk), pol(cx, cy, r2, a1 + sk)]
        out.append(poly(pts, cols[i % len(cols)], 'stroke-width="1"'))
    return "".join(out)


def rect_band(x, y, w, h, t, step, cols):
    """Прямоугольная окантовка «ёлочкой» шириной t."""
    out = []
    for side in range(4):
        L = w if side % 2 == 0 else h
        k = int(L // step)
        for i in range(k):
            a, b = i * step, (i + 1) * step
            if side == 0:   pts = [(x + a, y), (x + b, y), (x + b - t, y + t), (x + a - t, y + t)]
            elif side == 1: pts = [(x + w, y + a), (x + w, y + b), (x + w - t, y + b - t), (x + w - t, y + a - t)]
            elif side == 2: pts = [(x + w - a, y + h), (x + w - b, y + h), (x + w - b + t, y + h - t), (x + w - a + t, y + h - t)]
            else:           pts = [(x, y + h - a), (x, y + h - b), (x + t, y + h - b + t), (x + t, y + h - a + t)]
            out.append(poly(pts, cols[i % len(cols)], 'stroke-width="0.8"'))
    return "".join(out)


# ---------- стол ----------
body.append(f'<rect width="{W}" height="{H}" fill="{T["table"]}"/>')

# ---------- 1. Круглое панно: роза ветров ----------
def compass(cx, cy, R):
    g = [f'<g filter="url(#shadow)"><circle cx="{cx}" cy="{cy}" r="{R}" fill="{T["wenge0"]}"/></g>']
    g.append(banding(cx, cy, R - 4, R - 34, 96, [T["maple90"], T["walnut90"], T["oak90"]]))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R-36}" fill="{T["walnut0"]}" stroke="{JOINT}" stroke-width="2"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R-52}" fill="{T["burl"]}" stroke="{JOINT}" stroke-width="2"/>')
    # тонкое кольцо клёна
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.80}" fill="none" stroke="{JOINT}" stroke-width="12"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.80}" fill="none" stroke="#e3cfa9" stroke-width="8"/>')
    # лучи: 8 коротких, 8 средних, 4+4 длинных
    def ray(a, rt, rb, w, light, dark):
        tip = pol(cx, cy, rt, a); l = pol(cx, cy, rb, a - w); r = pol(cx, cy, rb, a + w)
        c = (cx, cy)
        return poly([c, tip, l], light) + poly([c, tip, r], dark) + poly([c, tip, r], "url(#sandR)", 'stroke="none" opacity=".6"')
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8 + math.pi / 16
        g.append(ray(a, R * .58, R * .16, .34, T["cherry60"], T["walnut60"]))
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4 + math.pi / 8
        g.append(ray(a, R * .70, R * .2, .30, T["ash30"], T["oak120"]))
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        rt = R * .9 if i % 2 == 0 else R * .76
        g.append(ray(a, rt, R * .22, .26, T["maple45"], T["oak-45"]))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R*.07}" fill="{T["padauk0"]}" stroke="{JOINT}" stroke-width="2"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R*.07}" fill="url(#sandC)"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sheen)"/>')
    return "".join(g)

body.append(compass(540, 600, 440))

# ---------- 2. Пейзаж в раме ----------
def landscape(x, y, w, h, rot):
    g = [f'<g transform="rotate({rot} {x+w/2} {y+h/2})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["wenge90"]}" filter="url(#shadow)"/>']
    g.append(rect_band(x + 26, y + 26, w - 52, h - 52, 16, 20, [T["maple0"], T["walnut0"]]))
    ix, iy, iw, ih = x + 46, y + 46, w - 92, h - 92
    g.append(f'<clipPath id="clipL"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}"/></clipPath><g clip-path="url(#clipL)">')
    # небо полосами
    sky = [T["maple0"], T["ash0"], T["maple0"], T["ash0"]]
    for k in range(4):
        y0 = iy + k * ih * .12
        g.append(poly([(ix, y0), (ix + iw, y0 + 14), (ix + iw, y0 + ih * .12 + 14), (ix, y0 + ih * .12)], sky[k]))
    sx, sy = ix + iw * .68, iy + ih * .26
    g.append(f'<circle cx="{sx}" cy="{sy}" r="{iw*.11}" fill="#f1e2bf" stroke="{JOINT}" stroke-width="1.6"/><circle cx="{sx}" cy="{sy}" r="{iw*.11}" fill="url(#sandC)" opacity=".5"/>')
    # дальние горы
    g.append(poly([(ix, iy + ih * .5), (ix + iw * .2, iy + ih * .36), (ix + iw * .38, iy + ih * .44), (ix + iw * .6, iy + ih * .31),
                   (ix + iw * .85, iy + ih * .43), (ix + iw, iy + ih * .38), (ix + iw, iy + ih * .62), (ix, iy + ih * .62)], T["olive30"]))
    g.append(poly([(ix + iw * .6, iy + ih * .31), (ix + iw * .85, iy + ih * .43), (ix + iw, iy + ih * .38), (ix + iw, iy + ih * .6), (ix + iw * .55, iy + ih * .6)], "url(#sandL)", 'stroke="none"'))
    # средний план
    g.append(poly([(ix, iy + ih * .56), (ix + iw * .3, iy + ih * .49), (ix + iw * .55, iy + ih * .55), (ix + iw * .8, iy + ih * .5),
                   (ix + iw, iy + ih * .54), (ix + iw, iy + ih * .66), (ix, iy + ih * .66)], T["oak30"]))
    # озеро
    for k in range(3):
        y0 = iy + ih * (.64 + k * .045)
        g.append(poly([(ix, y0), (ix + iw, y0), (ix + iw, y0 + ih * .045), (ix, y0 + ih * .045)], [T["ash0"], T["maple0"], T["ash0"]][k]))
    # луг
    g.append(poly([(ix, iy + ih * .78), (ix + iw * .4, iy + ih * .74), (ix + iw, iy + ih * .8), (ix + iw, iy + ih), (ix, iy + ih)], T["olive0"]))
    g.append(poly([(ix, iy + ih * .88), (ix + iw * .5, iy + ih * .84), (ix + iw, iy + ih * .9), (ix + iw, iy + ih), (ix, iy + ih)], T["walnut0"]))
    # дерево
    tx, ty = ix + iw * .26, iy + ih * .86
    g.append(poly([(tx - 9, ty), (tx - 5, ty - ih * .3), (tx + 5, ty - ih * .3), (tx + 10, ty)], T["walnut90"]))
    for (dx, dy, r, t) in [(-46, -.36, 60, "olive60"), (36, -.38, 58, "olive120"), (-6, -.47, 66, "olive30"), (-60, -.27, 44, "oak60"), (52, -.28, 46, "olive150")]:
        cxx, cyy = tx + dx, ty + ih * dy
        g.append(f'<ellipse cx="{cxx}" cy="{cyy}" rx="{r}" ry="{r*.88}" fill="{T[t]}" stroke="{JOINT}" stroke-width="1.6"/>')
        g.append(f'<ellipse cx="{cxx}" cy="{cyy}" rx="{r}" ry="{r*.88}" fill="url(#sandC)"/>')
    # птицы
    for (bx, by) in [(ix + iw * .55, iy + ih * .17), (ix + iw * .62, iy + ih * .13)]:
        g.append(f'<path d="M{bx-14} {by} q7 -8 14 0 q7 -8 14 0" fill="none" stroke="{T["wenge0"]}" stroke-width="4" stroke-linecap="round"/>')
    g.append('</g>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/></g>')
    return "".join(g)

body.append(landscape(1010, 150, 520, 720, 4))

# ---------- 3. Крышка шкатулки с цветком ----------
def box(x, y, w, h, rot):
    cx, cy = x + w / 2, y + h / 2
    g = [f'<g transform="rotate({rot} {cx} {cy})">',
         f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" rx="6" fill="{T["walnut90"]}" filter="url(#shadow)"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["burl"]}" stroke="{JOINT}" stroke-width="2"/>']
    g.append(rect_band(x + 18, y + 18, w - 36, h - 36, 14, 18, [T["maple45"], T["wenge45"], T["oak45"]]))
    # веера в углах
    for (qx, qy, a0) in [(x + 32, y + 32, 0), (x + w - 32, y + 32, math.pi / 2), (x + w - 32, y + h - 32, math.pi), (x + 32, y + h - 32, 3 * math.pi / 2)]:
        n = 7
        for i in range(n):
            a1 = a0 + (math.pi / 2) * i / n; a2 = a0 + (math.pi / 2) * (i + 1) / n
            g.append(poly([(qx, qy), pol(qx, qy, 130, a1), pol(qx, qy, 130, a2)], T["maple0"] if i % 2 == 0 else T["oak90"]))
        g.append(f'<path d="M{pol(qx,qy,130,a0)[0]:.1f} {pol(qx,qy,130,a0)[1]:.1f} A130 130 0 0 1 {pol(qx,qy,130,a0+math.pi/2)[0]:.1f} {pol(qx,qy,130,a0+math.pi/2)[1]:.1f}" fill="none" stroke="{JOINT}" stroke-width="5"/>')
    # медальон
    rx, ry = w * .3, h * .36
    g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx+16}" ry="{ry+16}" fill="{T["wenge0"]}" stroke="{JOINT}" stroke-width="2"/>')
    g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{T["maple90"]}" stroke="{JOINT}" stroke-width="2"/>')
    # стебель и листья
    g.append(f'<path d="M{cx} {cy+ry*.9} C{cx-20} {cy+ry*.4} {cx+18} {cy+ry*.1} {cx} {cy-ry*.05}" fill="none" stroke="{JOINT}" stroke-width="12" stroke-linecap="round"/>')
    g.append(f'<path d="M{cx} {cy+ry*.9} C{cx-20} {cy+ry*.4} {cx+18} {cy+ry*.1} {cx} {cy-ry*.05}" fill="none" stroke="#6f6c43" stroke-width="8" stroke-linecap="round"/>')
    def leaf(px, py, ang, L, t):
        a = math.radians(ang)
        tip = (px + L * math.cos(a), py + L * math.sin(a))
        n = (-math.sin(a), math.cos(a))
        m = (px + L * .5 * math.cos(a), py + L * .5 * math.sin(a))
        d = f"M{px:.1f} {py:.1f} Q{m[0]+n[0]*L*.32:.1f} {m[1]+n[1]*L*.32:.1f} {tip[0]:.1f} {tip[1]:.1f} Q{m[0]-n[0]*L*.32:.1f} {m[1]-n[1]*L*.32:.1f} {px:.1f} {py:.1f}Z"
        half = f"M{px:.1f} {py:.1f} Q{m[0]+n[0]*L*.32:.1f} {m[1]+n[1]*L*.32:.1f} {tip[0]:.1f} {tip[1]:.1f}Z"
        return (f'<path d="{d}" fill="{T[t]}" stroke="{JOINT}" stroke-width="1.6"/>'
                f'<path d="{half}" fill="#1a0d06" opacity=".28"/>')
    g.append(leaf(cx, cy + ry * .55, 200, 120, "olive30"))
    g.append(leaf(cx, cy + ry * .35, -20, 115, "olive150"))
    g.append(leaf(cx, cy + ry * .75, -40, 90, "olive60"))
    # цветок
    fy = cy - ry * .2
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        px, py = pol(cx, fy, 48, a)
        rr = 58
        tip = pol(cx, fy, 48 + rr * 1.5, a)
        l = pol(px, py, rr * .75, a - math.pi / 2); r = pol(px, py, rr * .75, a + math.pi / 2)
        d = f"M{cx:.1f} {fy:.1f} Q{l[0]:.1f} {l[1]:.1f} {tip[0]:.1f} {tip[1]:.1f} Q{r[0]:.1f} {r[1]:.1f} {cx:.1f} {fy:.1f}Z"
        g.append(f'<path d="{d}" fill="{T["padauk60" if i % 2 else "cherry120"]}" stroke="{JOINT}" stroke-width="1.6"/>')
        g.append(f'<path d="M{cx:.1f} {fy:.1f} Q{l[0]:.1f} {l[1]:.1f} {tip[0]:.1f} {tip[1]:.1f}Z" fill="#1a0d06" opacity=".3"/>')
    g.append(f'<circle cx="{cx}" cy="{fy}" r="34" fill="{T["oak0"]}" stroke="{JOINT}" stroke-width="2"/><circle cx="{cx}" cy="{fy}" r="34" fill="url(#sandC)"/>')
    for i in range(10):
        dx, dy = pol(0, 0, 18, i * 2.4)
        g.append(f'<circle cx="{cx+dx:.1f}" cy="{fy+dy:.1f}" r="4" fill="{JOINT}" opacity=".6"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/></g>')
    return "".join(g)

body.append(box(90, 1150, 780, 600, -4))

# ---------- 4. Шахматная доска ----------
def chess(x, y, s, rot):
    n = 8; B = 46
    size = n * s + 2 * B
    cx, cy = x + size / 2, y + size / 2
    g = [f'<g transform="rotate({rot} {cx} {cy})">',
         f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{T["walnut0"]}" filter="url(#shadow)"/>']
    g.append(rect_band(x + 14, y + 14, size - 28, size - 28, 14, 16, [T["maple45"], T["wenge45"]]))
    for i in range(n):
        for j in range(n):
            light = (i + j) % 2 == 0
            t = (T["maple0"] if (i % 2) else T["maple90"]) if light else (T["wenge90"] if (j % 2) else T["wenge0"])
            sx, sy = x + B + i * s, y + B + j * s
            g.append(f'<rect x="{sx}" y="{sy}" width="{s}" height="{s}" fill="{t}" stroke="{JOINT}" stroke-width="1"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="url(#sheen)"/></g>')
    return "".join(g)

body.append(chess(960, 1020, 68, 9))

# ---------- 5. Подставки ----------
def coaster(cx, cy, R, rot):
    g = [f'<g transform="rotate({rot} {cx} {cy})"><circle cx="{cx}" cy="{cy}" r="{R}" fill="{T["walnut0"]}" filter="url(#soft)"/>']
    g.append(banding(cx, cy, R - 3, R - 18, 48, [T["maple90"], T["wenge90"]]))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R-20}" fill="{T["cherry0"]}" stroke="{JOINT}" stroke-width="1.6"/>')
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        tip = pol(cx, cy, R * .7, a); l = pol(cx, cy, R * .28, a - math.pi / 8); r = pol(cx, cy, R * .28, a + math.pi / 8)
        g.append(poly([(cx, cy), tip, l], T["maple30"]) + poly([(cx, cy), tip, r], T["oak120"]))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sheen)"/></g>')
    return "".join(g)

body.append(coaster(1100, 1830, 125, 10))
body.append(coaster(1420, 1760, 105, -15))

# ---------- 6. Нож и обрезки шпона ----------
def scraps():
    g = []
    for (x, y, w, h, r, t) in [(150, 1840, 240, 60, -12, "padauk0"), (420, 1870, 200, 50, 8, "maple0"), (640, 1835, 180, 56, -4, "olive0")]:
        g.append(f'<g transform="rotate({r} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T[t]}" filter="url(#soft)" stroke="{JOINT}" stroke-width="1"/></g>')
    return "".join(g)

def knife(x1, y1, x2, y2):
    a = math.degrees(math.atan2(y2 - y1, x2 - x1)); L = math.hypot(x2 - x1, y2 - y1)
    return (f'<g transform="translate({x1} {y1}) rotate({a})" filter="url(#soft)">'
            f'<rect x="0" y="-14" width="{L*.62}" height="28" rx="12" fill="{T["oak0"]}" stroke="{JOINT}" stroke-width="1.5"/>'
            f'<rect x="{L*.6}" y="-11" width="{L*.08}" height="22" fill="#9aa0a7"/>'
            f'<path d="M{L*.68} -8 L{L} 2 L{L*.68} 8 Z" fill="url(#blade)"/></g>')

body.append(scraps())
body.append(knife(250, 1960, 900, 1900))

body.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{"".join(defs)}</defs>{"".join(body)}</svg>'
open("hero-art.svg", "w").write(svg)
print("svg", len(svg) // 1024, "KB")
