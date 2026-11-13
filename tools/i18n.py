"""Английская версия сайта: русские страницы -> /en/ по словарю переводов.

python3 i18n.py extract   — выписать все русские фрагменты в segments.json
python3 i18n.py build     — собрать /en/ и проверить, что кириллицы не осталось
"""
import json, re, sys, glob, os
from bs4 import BeautifulSoup, NavigableString, Comment

SITE_DIR = "/home/claude/marketri-site"
HERE = os.path.dirname(os.path.abspath(__file__))
CYR = re.compile(r"[А-Яа-яЁё]")
BLOCK = {"p", "li", "h1", "h2", "h3", "figcaption", "dt", "dd", "summary", "button", "title",
         "div", "blockquote", "span", "label", "nav", "a", "small", "b"}
ATTRS = ("alt", "aria-label", "title", "content", "placeholder")


def pages():
    return sorted(glob.glob(SITE_DIR + "/*.html"))


def segment_nodes(soup):
    cand, ids = [], set()
    for s in soup.find_all(string=CYR):
        if isinstance(s, Comment) or s.parent.name in ("script", "style"):
            continue
        n = s.parent
        while n is not None and n.name not in BLOCK:
            n = n.parent
        if n is not None and id(n) not in ids:
            cand.append(n); ids.add(id(n))
    # оставляем только внешние блоки
    out = []
    for n in cand:
        if not any(id(p) in ids for p in n.parents):
            out.append(n)
    return out


def inner(n):
    return "".join(str(c) for c in n.contents)


def walk_json(o, fn):
    if isinstance(o, dict):
        return {k: walk_json(v, fn) for k, v in o.items()}
    if isinstance(o, list):
        return [walk_json(v, fn) for v in o]
    if isinstance(o, str) and CYR.search(o):
        return fn(o)
    return o


def extract():
    segs = []
    def add(t):
        t = t.strip()
        if t and CYR.search(t) and t not in segs:
            segs.append(t)
    for f in pages():
        soup = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        for tag in soup.find_all(True):
            for a in ATTRS:
                v = tag.get(a)
                if isinstance(v, str) and CYR.search(v):
                    add(v)
        for sc in soup.find_all("script", type="application/ld+json"):
            walk_json(json.loads(sc.string), lambda s: (add(s), s)[1])
        for n in segment_nodes(soup):
            add(inner(n))
    json.dump(segs, open(HERE + "/segments.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(segs), "segments,", sum(len(s) for s in segs), "chars")


def build():
    sys.path.insert(0, HERE)
    from en_map import EN
    tr = {k.strip(): v for k, v in EN.items()}
    missing = []

    def T(t):
        k = t.strip()
        if k in tr:
            return tr[k]
        missing.append(k)
        return t

    os.makedirs(SITE_DIR + "/en", exist_ok=True)
    for f in pages():
        name = os.path.basename(f)
        soup = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        soup.html["lang"] = "en"
        # тексты
        for n in segment_nodes(soup):
            new = BeautifulSoup(T(inner(n)), "html.parser")
            n.clear()
            for c in list(new.contents):
                n.append(c)
        for tag in soup.find_all(True):
            for a in ATTRS:
                v = tag.get(a)
                if isinstance(v, str) and CYR.search(v):
                    tag[a] = T(v)
        for sc in soup.find_all("script", type="application/ld+json"):
            data = walk_json(json.loads(sc.string), T)
            sc.string = json.dumps(data, ensure_ascii=False)
        # пути к общим файлам
        for tag in soup.find_all(["link", "script", "img", "source", "a"]):
            for a in ("href", "src", "srcset"):
                v = tag.get(a)
                if not v or v.startswith(("http", "#", "mailto:", "tel:", "data:")):
                    continue
                if v.startswith(("assets/", "img/", "favicon", "apple-touch", "site.webmanifest", "icon-512")):
                    tag[a] = "../" + v
        # адреса и язык
        s = str(soup)
        s = s.replace('content="ru_RU"', 'content="en_US"')
        s = re.sub(r'(<link href="https://example\.ru/)(?!en/)([^"]*)(" rel="canonical")', r'\1en/\2\3', s)
        s = re.sub(r'(<meta content="https://example\.ru/)(?!en/)([^"]*)(" property="og:url")', r'\1en/\2\3', s)
        # переключатель языка
        s = re.sub(r'<div aria-label="[^"]*" class="lang-switch">.*?</div>',
                   f'<div aria-label="Site language" class="lang-switch"><a href="../{name}" hreflang="ru" lang="ru">RU</a><span aria-current="true">EN</span></div>', s, flags=re.S)
        # служебные строки, не попавшие в сегменты
        s = s.replace("<!-- Подтверждение прав в Яндекс Вебмастере:", "<!-- Yandex Webmaster verification:")
        s = s.replace("<!-- Яндекс Метрика: вставить код счётчика сюда (см. README) -->", "<!-- Yandex Metrica counter goes here (see README) -->")
        s = s.replace('content="КОД"', 'content="CODE"')
        open(SITE_DIR + "/en/" + name, "w", encoding="utf-8").write(s)
        left = [m for m in re.findall(r"[^<>\"]*[А-Яа-яЁё][^<>\"]*", s)]
        if left:
            print("CYRILLIC LEFT in", name, left[:5])
    if missing:
        print("MISSING", len(set(missing)))
        json.dump(sorted(set(missing)), open(HERE + "/missing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    # карта сайта: добавляем английские адреса
    sm_path = SITE_DIR + "/sitemap.xml"
    sm = open(sm_path, encoding="utf-8").read()
    if "/en/" not in sm:
        locs = re.findall(r"<url>.*?</url>", sm, flags=re.S)
        en_urls = [u.replace("https://example.ru/", "https://example.ru/en/") for u in locs]
        sm = sm.replace("</urlset>", "\n".join(en_urls) + "\n</urlset>")
        open(sm_path, "w", encoding="utf-8").write(sm)
    print("en pages:", len(pages()))


if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()
