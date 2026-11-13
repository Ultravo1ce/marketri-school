"""Образцы шпона из фото книги: обрезка без бликов, выравнивание света, баланс белого по полям страницы."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

A = "/mnt/user-data/attachments/23972080-ba8e-5850-81e6-f070dcea3db4/"
OUT = "/home/claude/marketri-site/img/"
# имя файла: (исходник, участок шпона без бликов, участок белого поля страницы)
# имя: (исходник, участок шпона без бликов и краёв, целевой средний цвет готового шпона)
SPEC = {
    "veneer-sycamore": ("8ca73ba1", (205, 560, 640, 1140), (232, 220, 196)),
    "veneer-birch":    ("0a6977fb", (262, 690, 648, 1195), (222, 191, 152)),
    "veneer-oak":      ("a1347bb0", (272, 680, 640, 1170), (199, 156, 104)),
    "veneer-cherry":   ("789eda58", (305, 560, 720, 1105), (188, 118, 74)),
    "veneer-cedar":    ("fb43cefe", (292, 440, 690, 880), (160, 84, 52)),
    "veneer-wenge":    ("e684a6d1", (365, 540, 760, 1045), (72, 52, 42)),
}


def process(src, box, target):
    im = Image.open(A + src + "-image.jpg").convert("RGB")
    a = np.asarray(im).astype(np.float32)
    x0, y0, x1, y1 = box
    c = a[y0:y1, x0:x1]
    # выравнивание света и цветовых пятен по каждому каналу
    flat = np.empty_like(c)
    for k in range(3):
        ch = c[..., k]
        bl = np.asarray(Image.fromarray(np.clip(ch, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(60))).astype(np.float32)
        flat[..., k] = ch / np.maximum(bl, 1) * bl.mean()
    # приводим средний тон к реальному цвету породы, сохраняя рисунок
    m = flat.reshape(-1, 3).mean(0)
    flat = flat * (np.array(target, np.float32) / m)
    out = Image.fromarray(np.clip(flat, 0, 255).astype(np.uint8))
    W, H = out.size
    if W / H > 0.75:
        nw = int(H * 0.75); out = out.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W / 0.75); out = out.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    out = out.resize((450, 600), Image.LANCZOS)
    return ImageEnhance.Sharpness(out).enhance(1.2)


if __name__ == "__main__":
    sheet = Image.new("RGB", (6 * 230, 310), "#F6F5F2")
    for i, (name, (src, box, target)) in enumerate(SPEC.items()):
        o = process(src, box, target)
        o.save(OUT + name + ".webp", "WEBP", quality=82, method=6)
        o.save(OUT + name + ".jpg", "JPEG", quality=84, optimize=True, progressive=True)
        m = np.asarray(o).reshape(-1, 3).mean(0)
        print(name, "средний цвет", m.round(), "яркость", round(float(m.mean()), 1))
        sheet.paste(o.resize((210, 280)), (10 + i * 230, 15))
    sheet.save("/tmp/claude-0/-home-claude/23972080-ba8e-5850-81e6-f070dcea3db4/scratchpad/veneer-sheet.png")
