"""Схема «Как добраться» на реальной геометрии со скриншота Яндекс Карт.
1) классифицируем пиксели: фон / дорога / сквер / дом / контур дома; подписи и значки заполняем соседями;
2) перекрашиваем в палитру сайта; 3) снимаем маршрут по фиолетовым точкам; 4) накладываем свои подписи (SVG)."""
import base64, io, math
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

SRC = "/mnt/user-data/attachments/23972080-ba8e-5850-81e6-f070dcea3db4/83d7e5ec-image.png"
OUT = "/home/claude/marketri-site/img/"
DBG = "/tmp/claude-0/-home-claude/23972080-ba8e-5850-81e6-f070dcea3db4/scratchpad/"

a = np.asarray(Image.open(SRC).convert("RGB")).astype(np.int16)
H, W, _ = a.shape

# ---------- 1. классы ----------
CENT = {  # класс: эталонные цвета Яндекса
    0: [(248, 248, 248), (240, 240, 240), (248, 248, 240), (232, 232, 232), (232, 232, 224)],   # фон
    1: [(184, 192, 208), (192, 200, 216), (208, 216, 224), (176, 184, 200), (168, 176, 192), (216, 216, 232), (200, 206, 218)],  # дорога
    2: [(200, 232, 176), (216, 240, 200), (192, 216, 176), (232, 248, 224)],                   # сквер
    3: [(224, 216, 216), (232, 224, 216), (240, 232, 232), (248, 240, 240), (224, 224, 224)],  # дом
    4: [(200, 192, 184), (208, 200, 200), (208, 200, 192)],                                    # стена/контур дома
}
labels = np.full((H, W), 255, np.uint8)
best = np.full((H, W), 1e9)
for k, cs in CENT.items():
    for c in cs:
        d = np.sqrt(((a - np.array(c)) ** 2).sum(2))
        m = d < best
        best[m] = d[m]; labels[m] = k
labels[best > 14] = 255                                  # текст, иконки, маршрут — неизвестно

# ---------- 2. заполняем неизвестное по соседям ----------
for rad in (4, 8, 16, 32):
    unk = labels == 255
    if not unk.any():
        break
    score = np.zeros((5, H, W), np.float32)
    for k in range(5):
        score[k] = cv2.blur((labels == k).astype(np.float32), (2 * rad + 1, 2 * rad + 1))
    fill = score.argmax(0).astype(np.uint8)
    has = score.max(0) > 0
    labels[unk & has] = fill[unk & has]
labels[labels == 255] = 0
# крупные «дорожные» пятна, не похожие на улицы (здание школы и т.п.), считаем домами
rl, rn = ndimage.label(labels == 1)
for i, sl in enumerate(ndimage.find_objects(rl), start=1):
    comp = rl[sl] == i
    area = comp.sum(); h, w = comp.shape
    if area > 2500 and area / (h * w) > 0.35 and max(h, w) < 400:
        labels[sl][comp] = 3
# сглаживаем мелкий шум
labels = ndimage.median_filter(labels, size=5)

# ---------- 3. палитра сайта ----------
PAL = {0: (241, 237, 230), 1: (255, 255, 255), 2: (218, 228, 205), 3: (228, 218, 203), 4: (205, 191, 170)}
rgb = np.zeros((H, W, 3), np.uint8)
for k, c in PAL.items():
    rgb[labels == k] = c
# кромка дорог — тонкая тёплая линия
road = (labels == 1).astype(np.uint8)
edge = cv2.dilate(road, np.ones((5, 5), np.uint8)) - road
rgb[(edge == 1) & (labels != 1)] = (214, 204, 189)
# мягкая тень у домов
bld = ((labels == 3) | (labels == 4)).astype(np.uint8)
sh = cv2.GaussianBlur(np.roll(np.roll(bld, 4, 0), 3, 1).astype(np.float32), (0, 0), 3)
shade = (sh * (1 - bld) * 0.18)[..., None]
rgb = (rgb.astype(np.float32) * (1 - shade)).astype(np.uint8)
base = Image.fromarray(rgb)
base.save(DBG + "route_base.png")

# ---------- 4. маршрут по фиолетовым точкам ----------
r, g, b = a[..., 0], a[..., 1], a[..., 2]
purple = (b > 180) & (r > 90) & (r < 190) & (g < 150) & (b - g > 80)
lab, n = ndimage.label(purple)
cents = ndimage.center_of_mass(purple, lab, range(1, n + 1))
sizes = ndimage.sum(purple, lab, range(1, n + 1))
pts = [(c[1], c[0]) for c, s in zip(cents, sizes) if 6 <= s <= 120]
# цепочка от старта (у выхода 2) по ближайшим соседям
start = min(pts, key=lambda p: (p[0] - 300) ** 2 + (p[1] - 805) ** 2)
chain, rest = [start], [p for p in pts if p != start]
while rest:
    last = chain[-1]
    nxt = min(rest, key=lambda p: (p[0] - last[0]) ** 2 + (p[1] - last[1]) ** 2)
    if math.dist(nxt, last) > 60:
        break
    chain.append(nxt); rest.remove(nxt)
approx = cv2.approxPolyDP(np.array(chain, np.float32).reshape(-1, 1, 2), 3, False).reshape(-1, 2)
route = [(float(x), float(y)) for x, y in approx]
print("точек маршрута:", len(pts), "в цепочке:", len(chain), "после упрощения:", len(route), "конец:", route[-1])
np.save(DBG + "route_pts.npy", np.array(route))
