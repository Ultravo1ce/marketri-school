"""Сборка страниц сайта школы маркетри: общая шапка, подвал и SEO-разметка."""
import json
from articles_content import ARTICLES

OUT = "/home/claude/marketri-site"
SITE = "https://example.ru"          # заменить на настоящий домен
NAME = "Школа маркетри Татьяны Гориной"
PHONE, PHONE_HREF = "+7 (900) 000-00-00", "+79000000000"
EMAIL = "info@example.ru"
TG = "https://t.me/username"
MAX = "https://max.ru/username"
WA = "https://wa.me/79000000000"
CITY = "Москва"
ADDRESS = "Москва, Брошевский переулок, дом 4"
STREET = "Брошевский переулок, 4"
MAP = "https://yandex.ru/map-widget/v1/?text=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D0%91%D1%80%D0%BE%D1%88%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BF%D0%B5%D1%80%D0%B5%D1%83%D0%BB%D0%BE%D0%BA%2C%204&z=16"
TODAY = "2026-11-09"
# Режим показа клиенту: сайт скрыт от поисковиков. Перед запуском поставить False.
PREVIEW = True

NAV = [("obuchenie.html", "Обучение"), ("master.html", "О мастере"), ("galereya.html", "Галерея"),
       ("zhurnal.html", "Журнал"), ("kontakty.html", "Контакты")]

LOGO = '''<svg viewBox="0 0 32 32" aria-hidden="true"><polygon points="16,1 31,16 16,16" fill="#E3CFAE"/><polygon points="31,16 16,31 16,16" fill="#5A3E2B"/><polygon points="16,31 1,16 16,16" fill="#E3CFAE"/><polygon points="1,16 16,1 16,16" fill="#A9805A"/></svg>'''

ORG = {
    "@context": "https://schema.org", "@type": "EducationalOrganization", "@id": SITE + "/#school",
    "name": NAME, "url": SITE + "/", "logo": SITE + "/icon-512.png", "image": SITE + "/img/og.jpg",
    "description": "Обучение технике маркетри — наборной мозаике из натурального шпона.",
    "telephone": PHONE_HREF, "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressCountry": "RU"},
    "founder": {"@type": "Person", "name": "Татьяна Горина", "jobTitle": "Мастер маркетри"},
    "sameAs": [TG, MAX, WA],
}


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (u, n) in enumerate(items)]}


def crumbs_html(items):
    lis = "".join(f'<li><a href="{u or "index.html"}">{n}</a></li>' for u, n in items[:-1])
    lis += f'<li aria-current="page">{items[-1][1]}</li>'
    back = ('<a class="back" href="index.html" data-back><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">'
            '<path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>Назад</a>')
    return f'<div class="crumbs-row">{back}<nav class="crumbs" aria-label="Навигация по разделам"><ol>{lis}</ol></nav></div>'


def page(file, title, desc, body, schema=(), og_type="website", noindex=False):
    path = "" if file == "index.html" else file
    url = SITE + "/" + path
    nav = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if u == file else ""}>{n}</a></li>' for u, n in NAV)
    robots = '<meta name="robots" content="noindex, follow">' if (noindex or PREVIEW) else '<meta name="robots" content="index, follow">'
    html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ru" href="{SITE}/{path}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{path}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F5F2">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<!-- Подтверждение прав в Яндекс Вебмастере: <meta name="yandex-verification" content="КОД"> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500&family=Spectral:ital,wght@0,300;0,400;1,300&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{"".join(ld(s) for s in schema)}
<!-- Яндекс Метрика: вставить код счётчика сюда (см. README) -->
</head>
<body>
<a class="skip" href="#main">Перейти к содержанию</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="{NAME}, на главную">{LOGO}<div><b>Школа маркетри</b><span>Татьяны Гориной</span></div></a>
    <p class="aegis">под эгидой <span>ТАГАНСКОГО МОЛОДЁЖНОГО СОЮЗА</span></p>
    <nav id="nav" class="nav" aria-label="Основное меню"><ul>{nav}</ul></nav>
    <div class="lang-switch" aria-label="Язык сайта"><span aria-current="true">RU</span><a href="en/{file}" hreflang="en" lang="en">EN</a></div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Меню</button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <p style="margin:0 0 6px;color:var(--ink)">{NAME}</p>
      <p style="margin:0"><a href="tel:{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <nav aria-label="Меню в подвале"><ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for u, n in NAV)}<li><a href="politika.html">Конфиденциальность</a></li></ul></nav>
    <p style="margin:0;width:100%">© 2026 {NAME}. Под эгидой ТАГАНСКОГО МОЛОДЁЖНОГО СОЮЗА.</p>
  </div>
</footer>
<div class="cookie" id="cookie" hidden>
  <p>Сайт использует cookie и Яндекс Метрику, чтобы понимать, какие страницы полезны. <a href="politika.html">Подробнее</a></p>
  <button type="button">Понятно</button>
</div>
<button class="to-top" type="button" aria-label="Наверх" hidden><svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true"><path d="M3 10l5-5 5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''
    with open(f"{OUT}/{file}", "w", encoding="utf-8") as f:
        f.write(html)
    return url


def img(src, alt, w, h, extra=""):
    return f'<img src="img/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"{extra}>'


GAL_SIZES = {"g01": (800, 1000), "g02": (800, 600), "g03": (800, 800), "g04": (800, 1100), "g05": (800, 640),
             "g06": (800, 900), "g07": (800, 1000), "g08": (800, 600), "g09": (800, 800),
             "s01": (800, 800), "s02": (800, 1100), "s03": (800, 640), "s04": (800, 900), "s05": (800, 1000),
             "s06": (800, 600)}


def fig(key, caption=True):
    w, h = 800, 1000
    cap = '<figcaption><b>Название работы</b>Породы шпона, размер</figcaption>' if caption else ""
    return f'<figure>{img(key + ".svg", "Работа в технике маркетри", w, h)}{cap}</figure>'


def sfig(key):
    w, h = 800, 1000
    return f'<figure>{img(key + ".svg", "Работа ученика школы маркетри", w, h)}<figcaption><b>Имя ученика</b>Этап курса, название работы</figcaption></figure>'


CONTACTS_DL = f'''<dl class="contacts">
  <div><dt>Телефон</dt><dd><a href="tel:{PHONE_HREF}">{PHONE}</a></dd></div>
  <div><dt>Telegram</dt><dd><a href="{TG}" rel="noopener" target="_blank">Написать в Telegram</a></dd></div>
  <div><dt>WhatsApp</dt><dd><a href="{WA}" rel="noopener" target="_blank">Написать в WhatsApp</a></dd></div>
  <div><dt>MAX</dt><dd><a href="{MAX}" rel="noopener" target="_blank">Написать в MAX</a></dd></div>
  <div><dt>Почта</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
  <div><dt>Мастерская</dt><dd>{ADDRESS}</dd></div>
</dl>'''

FAQ = [
    ("Нужен ли опыт работы с деревом?",
     "Нет. Первый этап курса рассчитан на тех, кто ни разу не работал со шпоном. Мастер показывает каждый приём и помогает на всех этапах."),
    ("Нужно ли покупать инструменты и материалы?",
     "Нет, всё необходимое для занятий есть в мастерской. Если решите заниматься дома, мастер подскажет, какие инструменты купить."),
    ("Можно ли пройти только один этап?",
     "Курс построен так, что каждый следующий этап опирается на предыдущий. Если у вас уже есть опыт, мастер подскажет, с какого этапа можно начать."),
    ("Сколько длится курс?",
     "Три месяца: занятия два раза в неделю по два часа. Даты ближайшего набора уточняйте у мастера по телефону или в мессенджере."),
    ("Можно ли заниматься, если я живу в другом городе?",
     "Да. Для учеников из других городов мастер составляет индивидуальный график."),
    ("Можно ли забрать свою работу?",
     "Да, работы, сделанные на занятиях, остаются у вас."),
    ("Можно ли подарить обучение?",
     "Да, курс можно подарить. Подробности уточняйте у мастера."),
    ("Чем маркетри отличается от интарсии?",
     "В интарсии детали врезают в массив дерева, а в маркетри изображение целиком набирают из тонкого шпона и наклеивают на основу. Сегодня эти слова часто используют как синонимы."),
]

FAQ_HTML = '<div class="faq">' + "".join(
    f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ) + "</div>"
FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


STAGES = [
    ("stage-1", "Основы", "Знакомство с инструментами и материалом.",
     ["инструменты и породы шпона", "перевод эскиза и разметку", "резку ножом и первый простой набор"],
     "небольшой орнамент из нескольких пород"),
    ("stage-2", "Картина из шпона", "Работа с цветом, волокном и объёмом.",
     ["многоцветный набор по готовому эскизу", "подбор шпона по цвету и направлению волокон", "тонирование горячим песком"],
     "панно по готовому эскизу"),
    ("stage-3", "Собственная работа", "Полный цикл, от идеи до готового изделия.",
     ["подготовку собственного эскиза", "наклейку набора на основу", "шлифовку и отделку маслом или лаком"],
     "законченное панно или вставка для мебели по вашей идее"),
]

RUBRICS = [
    ("panno", "Панно и картины", "Пейзажи, натюрморты и орнаменты из шпона — самый известный жанр маркетри. Панно украшают гостиные, кабинеты и спальни."),
    ("mebel", "Мебель и столешницы", "Наборные вставки на столешницах, дверцах шкафов, комодах и спинках кроватей превращают мебель в штучный предмет."),
    ("shkatulki", "Шкатулки и подарки", "Шкатулки, футляры и коробки с наборной крышкой — подарок, который хранят поколениями."),
    ("shahmaty", "Шахматные доски и игры", "Шахматные и нардовые доски из контрастных пород — классика, где геометрия набора особенно точна."),
    ("interer", "Двери и стеновые панели", "Маркетри в отделке интерьера: наборные двери, стеновые панели, вставки в потолки и паркет."),
    ("portrety", "Портреты", "Портреты из шпона по фотографии — один из самых сложных жанров: оттенки кожи и света передают подбором пород и волокна."),
    ("dekor", "Часы, подносы и декор", "Настенные часы, подносы, рамки и другие предметы, в которых маркетри становится частью повседневной жизни."),
]

WOODS = [
    ("veneer-sycamore", "Клён-явор", "Acer pseudoplatanus", "Почти белый, с шелковистым блеском и волнистым рисунком. Из этого клёна делают скрипки, а в маркетри — фон, небо и блики."),
    ("veneer-birch", "Берёза жёлтая", "Betula alleghaniensis", "Светлая, с тёплым медовым оттенком и мягким рисунком «арками». Хороша для светлых тёплых деталей."),
    ("veneer-oak", "Дуб", "Quercus robur, Quercus petraea", "Золотисто-коричневый, с отчётливыми порами и прямыми линиями волокон. Прочный и выразительный."),
    ("veneer-cherry", "Черешня", "Prunus avium", "Тёплая, розовато-оранжевая, с ровным мягким рисунком. На свету со временем темнеет и становится глубже."),
    ("veneer-cedar", "Кедр", "Cedrus", "Насыщенный красновато-коричневый, с ровным прямым волокном. Подходит для тёплых теней и осенних мотивов."),
    ("veneer-wenge", "Венге", "Millettia laurentii", "Тёмно-коричневый, почти чёрный, с контрастными прожилками. Порода из тропической Африки: контуры, тени, графика."),
]
WOODS_HTML = '<ul class="woods">' + "".join(
    f'<li><picture><source srcset="img/{f}.webp" type="image/webp"><img class="swatch" src="img/{f}.jpg" alt="Шпон: {n.lower() if n != "Клён-явор" else "клён-явор"}" width="450" height="600" loading="lazy" decoding="async"></picture>'
    f'<h3>{n}</h3><p class="latin">{l}</p><p>{d}</p></li>' for f, n, l, d in WOODS) + "</ul>"

ARTICLE_FILE = "marketri-istoriya-i-tehnika.html"
ARTICLE_TITLE = "Маркетри: история и техника наборной мозаики из дерева"
ALL_POSTS = [{"file": ARTICLE_FILE, "short": "Маркетри: история и техника", "img": "art-history",
              "excerpt": "Откуда пришла наборная мозаика из дерева, как создаётся работа и чем маркетри отличается от интарсии и паркетри."}] + ARTICLES


def pic(name, alt, lazy=True, w=1200, h=800):
    extra = ' loading="lazy" decoding="async"' if lazy else ""
    return (f'<picture><source srcset="img/{name}.webp" type="image/webp">'
            f'<img src="img/{name}.jpg" alt="{alt}" width="{w}" height="{h}"{extra}></picture>')


def post_li(a):
    thumb = (f'<a class="post-thumb" href="{a["file"]}" tabindex="-1" aria-hidden="true">{pic(a["img"], "")}</a>'
             if a.get("img") else "")
    return f'<li class="post">{thumb}<div><h3><a href="{a["file"]}">{a["short"]}</a></h3><p>{a["excerpt"]}</p></div></li>'


def related(current):
    others = [a for a in ALL_POSTS if a["file"] != current][:3]
    return f'''
<section class="section" aria-labelledby="related">
  <div class="wrap">
    <h2 id="related">Читайте также</h2>
    <ul class="posts" style="margin-top:32px">{"".join(post_li(a) for a in others)}</ul>
  </div>
</section>
<section class="section section--tint" aria-labelledby="cta">
  <div class="wrap split">
    <h2 id="cta">Попробуйте сами</h2>
    <div>
      <p class="lead">На курсе маркетри вы за три этапа пройдёте путь от первого набора до собственного панно. Опыт не нужен, все материалы есть в мастерской.</p>
      <div class="actions" style="margin-top:24px"><a class="btn" href="obuchenie.html">О курсе</a><a class="text-link" href="kontakty.html">Связаться с мастером</a></div>
    </div>
  </div>
</section>'''



# ======================= Главная =======================
home = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Школа маркетри Татьяны Гориной</h1>
      <p class="lead">Учим собирать картины и орнаменты из натурального шпона: от первого простого набора до панно и вставок в мебель. Занятия проходят в мастерской в Москве.</p>
      <div class="actions">
        <a class="btn" href="obuchenie.html">О курсе</a>
        <a class="text-link" href="kontakty.html">Как связаться</a>
      </div>
    </div>
    <figure class="inlay"><picture><source srcset="img/hero.webp" type="image/webp"><img src="img/hero.jpg" alt="Работы в технике маркетри: панно с розой ветров, пейзаж из шпона, шкатулка с цветком и шахматная доска" width="1200" height="1500" fetchpriority="high"></picture></figure>
  </div>
</section>

<section class="section" aria-labelledby="what">
  <div class="wrap split">
    <h2 id="what">Что такое маркетри?</h2>
    <div>
      <p>Маркетри — техника наборной мозаики из дерева. Изображение собирают из тонких листов шпона разных пород: каждая порода даёт свой цвет и рисунок волокон, а мастер подбирает их, как художник краски.</p>
      <p>Расцвет техники пришёлся на Францию XVII–XVIII веков, где ею украшали дворцовую мебель. Сегодня маркетри — редкое ремесло. В нём важны терпение, точность ножа и чувство материала, а не дорогие станки.</p>
      <p><a href="{ARTICLE_FILE}">Подробнее об истории и технике</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="woods">
  <div class="wrap">
    <h2 id="woods">Палитра мастера</h2>
    <p class="lead lead--wide">В маркетри нет красок: цвет даёт сама древесина. Здесь лишь несколько пород для примера, а на курсе вы познакомитесь с десятками других — от редких капов и экзотики до цветного шпона, превращающего дерево в настоящую палитру.</p>
    {WOODS_HTML}
  </div>
</section>

<section class="section" aria-labelledby="master">
  <div class="wrap split split--media">
    <figure class="inlay portrait"><picture><source srcset="img/tatyana-gorina.webp" type="image/webp"><img src="img/tatyana-gorina.jpg" alt="Татьяна Горина, мастер и преподаватель маркетри" width="682" height="852" loading="lazy" decoding="async"></picture></figure>
    <div>
      <h2 id="master">Татьяна Горина</h2>
      <p class="lead">Мастер и преподаватель маркетри.</p>
      <blockquote class="quote"><p>Я взяла резец в руки в сорок лет. До этого шила, вязала и копала грядки, а потом брат-краснодеревщик показал мне маркетри. Я много работала на заказ, долгие годы — в реставрационных мастерских на Чистых прудах. Сейчас в основном учу. И творчество у нас с учениками совместное: я учусь у них, а они у меня.</p></blockquote>
      <p><a href="master.html">История мастера</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="learn">
  <div class="wrap">
    <h2 id="learn">Курс маркетри</h2>
    <p class="lead">Один курс из трёх этапов за три месяца: от первого движения ножом до собственного панно. Подходит и тем, кто никогда не работал с деревом.</p>
    <ol class="stages">{"".join(f'<li><h3><a href="obuchenie.html">{n}</a></h3><p>{d}</p><p class="result">Результат: {r}</p></li>' for sid, n, d, _l, r in STAGES)}</ol>
    <a class="text-link" href="obuchenie.html">Подробнее о курсе</a>
  </div>
</section>

<section class="section" aria-labelledby="steps">
  <div class="wrap">
    <h2 id="steps">Как рождается работа</h2>
    <p class="lead">На занятиях вы пройдёте все этапы, которые проходит мастер.</p>
    <ol class="steps">
      <li><h3>Эскиз</h3><p>Рисунок переводят на кальку и делят на фрагменты.</p></li>
      <li><h3>Подбор шпона</h3><p>Для каждого фрагмента выбирают породу по цвету и направлению волокон.</p></li>
      <li><h3>Резка</h3><p>Фрагменты вырезают ножом по линиям эскиза.</p></li>
      <li><h3>Набор</h3><p>Детали собирают вместе и фиксируют бумажной лентой.</p></li>
      <li><h3>Отделка</h3><p>Набор приклеивают на основу, шлифуют и покрывают маслом или лаком.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="gal">
  <div class="wrap">
    <div class="section-head"><h2 id="gal">Где живёт маркетри</h2><a class="text-link" href="galereya.html">Вся галерея</a></div>
    <p class="lead" style="margin-bottom:40px">Техника маркетри подходит для картин, мебели, подарков и целых интерьеров. Работы мастера по рубрикам.</p>
    <div class="gallery">{"".join(f'<a class="rubric" href="galereya.html?r={rid}"><figure>{img(f"{rid}-1.svg", rname, 800, 1000)}<figcaption><b>{rname}</b></figcaption></figure></a>' for rid, rname, _ in RUBRICS[:6])}</div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="students">
  <div class="wrap">
    <div class="section-head"><h2 id="students">Работы учеников</h2><a class="text-link" href="galereya.html?r=students">Все работы учеников</a></div>
    <p class="lead" style="margin-bottom:40px">Эти панно сделаны на курсе. Каждое — результат одного из трёх этапов.</p>
    <div class="gallery">{"".join(sfig(k) for k in ["s01", "s02", "s03", "s04", "s05", "s06"])}</div>
  </div>
</section>

<section class="section" aria-labelledby="blog">
  <div class="wrap">
    <div class="section-head"><h2 id="blog">Журнал</h2><a class="text-link" href="zhurnal.html">Все статьи</a></div>
    <ul class="posts">{"".join(post_li(a) for a in ALL_POSTS[:3])}</ul>
  </div>
</section>

<section class="section" aria-labelledby="faq">
  <div class="wrap split">
    <h2 id="faq">Частые вопросы</h2>
    {FAQ_HTML}
  </div>
</section>

<section class="section" aria-labelledby="contacts">
  <div class="wrap">
    <div class="section-head"><h2 id="contacts">Контакты</h2><a class="text-link" href="kontakty.html">Как добраться</a></div>
    <p class="lead" style="margin-bottom:36px">Чтобы записаться на занятие или задать вопрос, позвоните или напишите в мессенджер.</p>
    {CONTACTS_DL}
  </div>
</section>
'''
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/", "inLanguage": "ru"}
page("index.html", "Школа маркетри Татьяны Гориной — обучение мозаике из шпона",
     "Школа маркетри Татьяны Гориной в Москве: курс наборной мозаики из натурального шпона в три этапа, от основ до собственного панно. Опыт не нужен.",
     home, [ORG, WEBSITE, FAQ_LD])

# ======================= Обучение =======================
prog_html = ""
for n, (pid, name, intro, learn, result) in enumerate(STAGES, 1):
    prog_html += f'''
<section class="program" id="{pid}" aria-labelledby="{pid}-t">
  <div class="wrap split">
    <div><p class="stage-num">Этап {n}</p><h2 id="{pid}-t">{name}</h2></div>
    <dl>
      <dt>О чём этап</dt><dd>{intro}</dd>
      <dt>Что освоите</dt><dd><ul>{"".join(f"<li>{x}</li>" for x in learn)}</ul></dd>
      <dt>Результат</dt><dd>{result[0].upper() + result[1:]}</dd>
    </dl>
  </div>
</section>'''
courses_ld = [{"@context": "https://schema.org", "@type": "Course", "name": "Курс маркетри",
               "description": "Курс наборной мозаики из шпона в три этапа: основы, картина из шпона, собственная работа.",
               "inLanguage": "ru", "timeRequired": "P3M", "syllabusSections": [{"@type": "Syllabus", "name": f"Этап {k}. {st[1]}", "description": st[2]} for k, st in enumerate(STAGES, 1)],
               "provider": {"@type": "EducationalOrganization", "name": NAME, "url": SITE + "/"}}]

c = [("", "Главная"), ("obuchenie.html", "Обучение")]
learn_page = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>Курс маркетри</h1>
  <p class="lead">Курс состоит из трёх этапов. На каждом вы делаете законченную работу, а к концу курса — собственное панно по своему эскизу. Все материалы и инструменты есть в мастерской.</p>
  <dl class="facts"><div><dt>Длительность</dt><dd>3 месяца</dd></div><div><dt>Занятия</dt><dd>2 раза в неделю по 2 часа</dd></div><div><dt>Опыт</dt><dd>Не нужен</dd></div><div><dt>Стоимость</dt><dd>Уточняется</dd></div></dl>
</div></div>
{prog_html}
<section class="section" aria-labelledby="enrol">
  <div class="wrap split">
    <h2 id="enrol">Как записаться</h2>
    <div>
      <p>Позвоните или напишите мастеру: он расскажет о ближайшем наборе и ответит на вопросы.</p>
      <p><a href="tel:{PHONE_HREF}">{PHONE}</a> или <a href="kontakty.html">другие способы связи</a></p>
    </div>
  </div>
</section>
'''
learn_page = learn_page.replace("индивидальной", "индивидуальной")
page("obuchenie.html", "Курс маркетри в Москве — Школа Татьяны Гориной",
     "Курс маркетри из трёх этапов: основы, картина из шпона и собственная работа. Научитесь собирать панно из натурального шпона в мастерской в Москве.",
     learn_page, [crumbs_ld(c)] + courses_ld)

# ======================= О мастере =======================
c = [("", "Главная"), ("master.html", "О мастере")]
master_page = f'''
<div class="page-head" style="padding-bottom:0"><div class="wrap">
  {crumbs_html(c)}
</div></div>
<section class="master">
  <div class="wrap master-grid">
    <figure class="inlay portrait master-photo"><picture><source srcset="img/tatyana-gorina.webp" type="image/webp"><img src="img/tatyana-gorina.jpg" alt="Татьяна Горина, мастер и преподаватель маркетри" width="682" height="852" fetchpriority="high"></picture></figure>
    <div class="master-text">
      <h1>Татьяна Горина</h1>
      <p class="lead">Мастер и преподаватель маркетри. Студия на Брошевском переулке в Москве.</p>
      <blockquote class="quote quote--big"><p>Я взяла резец в руки в сорок лет.</p></blockquote>

      <h2>Как я пришла в маркетри</h2>
      <p>Я всем говорю, что пришла в маркетри по глупости. Никакого специального образования у меня не было: по специальности я портной, шила, вязала, копала грядки. А потом мой брат, краснодеревщик, начал учить своему делу падчерицу. Я посмотрела на это и спрашиваю: «А что ты меня не научишь?» С этого всё и началось.</p>
      <p>Сначала набивала руку на простых вещах: собачки, гербы, цветочки. Первую объёмную работу сделала по мотивам Сальвадора Дали, он меня тогда очень вдохновил.</p>
      <p>Потом брат сломал руку, ему нужна была помощь, и я пошла к нему маркетристом. Работала уже над настоящими заказными изделиями. Через некоторое время он закрыл производство, и я ушла в реставрационные мастерские на Чистых прудах. Там я проработала очень долго.</p>
      <p>Художественного образования у меня тоже нет. Думаю, у меня просто склонность к этому. В детстве я очень любила аппликацию, а это почти то же самое: вырезаешь и приклеиваешь, только техника чуть-чуть другая.</p>

      <h2>Работы и заказы</h2>
      <p>В своё время я много делала на заказ, и для послов, и для промышленных магнатов. Для мебели сделала много «рубашек», наборных покрытий. Даже купила промышленный лазер, чтобы не бить руки на повторяющихся деталях: орнаментах, рамках, вензелях.</p>
      <p>Меня вдохновляет природа, мне нравится передавать её в дереве. Это сложно: чтобы показать объём, приходится основательно потрудиться. Грушу в одном натюрморте я переделывала пять раз, пока не добилась результата, который меня устроил.</p>
      <p>Некоторые мастера не любят яркие, неестественные для дерева цвета и работают только с морёным шпоном. А я, наоборот, и крашу шпон, и затемняю его горячим песком. В общем, использую все возможные приёмы.</p>

      <h2>О шпоне</h2>
      <p>Дешёвым маркетри не может быть по определению. Во-первых, это большой и сложный технологический процесс. Во-вторых, породы дерева мы используем в основном дорогие. И чтобы успешно работать, нужна большая коллекция материала.</p>
      <p>У меня, наверное, самая большая коллекция шпона, ни у кого такой нет. Храню его в пластиковых контейнерах: это самый грамотный способ. Меня спрашивают, как я помню столько разных пород. Отвечаю: когда купите сами, тоже запомните. Дерево ведь проходит не только через руки, но и через карманы.</p>

      <h2>Как я учу</h2>
      <p>Я думаю, кто-то обязательно должен показать основы. А дальше всё зависит только от вас. Научить я не могу: человек может только сам научиться. Я могу показать, рассказать, правильно направить. Успех ученика — в усердии и терпении. Сосредоточьтесь, и всё придёт.</p>
      <p>Очень важно правильно исправлять ошибки. Ошибаются все, но как выйти из такой ситуации с минимальными потерями, знают только мастера.</p>
      <p>Сейчас я упростила обучение: мы занимаемся два раза в неделю по два часа в течение трёх месяцев. После этого у учеников уже вполне приличный уровень. Но нельзя сказать, что они выходят мастерами. Мастера учатся всю жизнь.</p>
      <p>Ко мне приезжают и из других городов, с ними мы составляем индивидуальный график. Даже из Франции была девочка. Некоторые ученики задерживаются надолго: один человек ходит ко мне уже двенадцать лет. Сейчас мы с ним занимаемся реставрацией: сначала отреставрировали стол, теперь работаем над комодом.</p>
      <p>Сейчас я сама делаю мало работ и в основном занимаюсь обучением. Мы работаем вместе с учениками, а у них всё время разные запросы, поэтому приходится изучать все стили. Бывает, ставят меня в тупик: смотрят на вещи по-другому, не так, как я. Я с той стороны не смотрела, а они смотрят. Поэтому творчество у нас совместное: я учусь у них, а они у меня.</p>
      <p>Раньше мы закупали шпон на несколько тысяч долларов. Сейчас я учу по-другому: задумали работу — поезжайте с эскизом в магазин и уже под него подбирайте шпон.</p>

      <h2>Выставки и гости</h2>
      <p>Я участвую в выставках вместе с учениками. Моя выставка была и в Нижнем Новгороде.</p>
      <p>Я человек общительный, и в студии у меня в гостях кого только не было. Приезжали даже из Эрмитажа. Был художник Сергей Андрияка: он пригласил меня на выставку, посвящённую открытию Академии акварели и изящных искусств, и мы три месяца выставлялись там с учениками.</p>

      <h2>Если вы ищете, чем заняться</h2>
      <p>Тем, кто ищет для себя возможность творить, я говорю: маркетри — хорошее занятие. Это очень красиво. Дерево — материал тёплый, живой, с ним приятно работать.</p>
      <p>А ещё у вас будет прекрасная возможность оставить потомкам отличную вещь, которая будет передаваться из рук в руки. Можно, как моя ученица, взять столетнюю бабушкину швейную машинку «Зингер» и не только привести её в порядок, но и добавить что-то от себя.</p>
      <div class="actions" style="margin-top:36px"><a class="btn" href="obuchenie.html">О курсе</a><a class="text-link" href="galereya.html">Галерея работ</a></div>
    </div>
  </div>
</section>
'''
PERSON = {"@context": "https://schema.org", "@type": "Person", "name": "Татьяна Горина",
          "jobTitle": "Мастер и преподаватель маркетри", "image": SITE + "/img/tatyana-gorina.jpg",
          "description": "Мастер и преподаватель маркетри. Работала на заказ и в реставрационных мастерских на Чистых прудах, сейчас ведёт обучение в студии на Брошевском переулке.", "worksFor": {"@id": SITE + "/#school"}, "url": SITE + "/master.html"}
page("master.html", "Татьяна Горина — мастер и преподаватель маркетри",
     "Татьяна Горина о себе: как пришла в маркетри в сорок лет, работа на заказ и в реставрационных мастерских, коллекция шпона и подход к обучению.",
     master_page, [crumbs_ld(c), PERSON], og_type="profile")

# ======================= Галерея =======================
c = [("", "Главная"), ("galereya.html", "Галерея")]
rub_sections = ""
for rid, rname, rdesc in RUBRICS:
    figs = "".join(f'<figure>{img(f"{rid}-{k}.svg", f"{rname}: работа в технике маркетри", 800, 1000)}<figcaption><b>Название работы</b>Породы шпона, размер</figcaption></figure>' for k in range(1, 4))
    rub_sections += f'''
<section class="section" id="{rid}" data-rubric="{rid}" aria-labelledby="{rid}-t">
  <div class="wrap">
    <div class="split" style="margin-bottom:36px"><h2 id="{rid}-t">{rname}</h2><p class="lead" style="margin:0">{rdesc}</p></div>
    <div class="gallery">{figs}</div>
  </div>
</section>'''
rub_nav = '<li><a href="galereya.html" data-r="all" aria-current="true">Все работы</a></li>' + "".join(f'<li><a href="galereya.html?r={rid}" data-r="{rid}">{rname}</a></li>' for rid, rname, _ in RUBRICS) + '<li><a href="galereya.html?r=students" data-r="students">Работы учеников</a></li>'
gal_page = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>Галерея</h1>
  <p class="lead">Где живёт маркетри: от панно и шкатулок до мебели и отделки интерьера. Работы мастера и учеников школы.</p>
  <nav aria-label="Рубрики галереи"><ul class="rubrics">{rub_nav}</ul></nav>
</div></div>
{rub_sections}
<section class="section section--tint" id="by-students" data-rubric="students" aria-labelledby="by-students-t">
  <div class="wrap">
    <div class="split" style="margin-bottom:36px"><h2 id="by-students-t">Работы учеников</h2><p class="lead" style="margin:0">Панно, сделанные на курсе маркетри. Каждое — результат одного из трёх этапов.</p></div>
    <div class="gallery">{"".join(sfig(f"s{i:02d}") for i in range(1, 7))}</div>
  </div>
</section>
'''
page("galereya.html", "Галерея маркетри: панно, мебель, шкатулки, портреты — Школа Татьяны Гориной",
     "Работы в технике маркетри по рубрикам: панно и картины, мебель, шкатулки, шахматные доски, двери и стеновые панели, портреты из шпона, декор.",
     gal_page, [crumbs_ld(c)])

# ======================= Журнал =======================
c = [("", "Главная"), ("zhurnal.html", "Журнал")]
blog_page = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>Журнал</h1>
  <p class="lead">Статьи о технике маркетри, породах дерева и уходе за изделиями из шпона.</p>
</div></div>
<section style="padding-bottom:clamp(56px,8vw,112px)">
  <div class="wrap">
    <ul class="posts">{"".join(post_li(a) for a in ALL_POSTS)}</ul>
  </div>
</section>
'''
page("zhurnal.html", "Журнал о маркетри — статьи Школы Татьяны Гориной",
     "Статьи о технике маркетри: история, породы шпона, инструменты и уход за изделиями.", blog_page, [crumbs_ld(c)])

# ======================= Статья =======================
c = [("", "Главная"), ("zhurnal.html", "Журнал"), (ARTICLE_FILE, "Маркетри: история и техника")]
article = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>{ARTICLE_TITLE}</h1>
  <p class="meta">Школа маркетри Татьяны Гориной, 9 ноября 2026</p>
</div></div>
<article class="wrap"><div class="prose">
<p class="lead">Маркетри — одна из самых тонких техник декоративной работы с деревом. Рассказываем, откуда она появилась, как устроена и чем отличается от похожих ремёсел.</p>

<h2>Что такое маркетри?</h2>
<p>Маркетри — это изображение или орнамент, набранный из кусочков шпона разных пород дерева и наклеенный на основу. Шпон — тонкий лист древесины толщиной обычно 0,6–0,8 мм.</p>
<p>Цвет в такой работе дают не краски, а сама древесина: светлые клён и берёза, золотистый дуб, красноватая вишня, тёмный орех. Рисунок волокон работает как мазок кисти: им передают блеск воды, складки ткани или фактуру листвы.</p>
<p>Слово пришло из французского: marqueterie происходит от глагола marqueter — «размечать, испещрять».</p>

<h2>Откуда пришла техника</h2>
<p>Украшать предметы вставками из дерева, кости и камня умели ещё в Древнем Египте. В Италии эпохи Возрождения расцвела интарсия — наборные картины из дерева на стенах кабинетов и спинках церковных скамей. Самый известный пример — кабинет герцога Федерико да Монтефельтро в Урбино.</p>
<p>Расцвет маркетри пришёлся на Францию XVII–XVIII веков. Мебельщик Андре-Шарль Буль прославился наборами из латуни и черепахового панциря. В XVIII веке Жан-Франсуа Обен и Жан-Анри Ризенер создавали для королевского двора мебель с цветочными и пейзажными наборами из десятков пород дерева.</p>
<p>В России наборное дерево ценили в XVIII–XIX веках: им украшали мебель и паркеты дворцов. Знаменитые наборные полы сохранились, например, в Останкинском дворце. Новая волна интереса пришла в эпоху модерна, когда к маркетри обратились Эмиль Галле и мастера школы Нанси.</p>

<figure class="inlay">{pic("art-history", "Панно в технике маркетри: букет цветов в вазе, обрамлённый наборной окантовкой")}</figure>

<h2>Как создаётся работа</h2>
<ol>
  <li><strong>Эскиз.</strong> Рисунок переводят на кальку и делят на фрагменты: каждый станет отдельной деталью.</li>
  <li><strong>Подбор шпона.</strong> Для каждой детали выбирают породу по цвету, текстуре и направлению волокон.</li>
  <li><strong>Резка.</strong> Детали вырезают ножом или тонким лобзиком. При пакетной резке несколько листов разных пород режут одновременно, и детали точно совпадают по контуру.</li>
  <li><strong>Набор.</strong> Детали собирают с лицевой стороны и фиксируют бумажной лентой.</li>
  <li><strong>Наклейка и отделка.</strong> Набор приклеивают на основу под прессом, затем шлифуют и покрывают маслом или лаком.</li>
</ol>

<h2>Приёмы, которые дают глубину</h2>
<p><strong>Тонирование горячим песком.</strong> Край детали погружают в нагретый песок, и он темнеет. Так получают объём и тень без красителей.</p>
<p><strong>Направление волокон.</strong> Один и тот же шпон, повёрнутый под разным углом, по-разному отражает свет. Мастера используют это, чтобы выделить детали изображения.</p>

<h2>Маркетри, интарсия и паркетри</h2>
<ul>
  <li><strong>Интарсия</strong> — детали врезают в углубления в массиве дерева.</li>
  <li><strong>Маркетри</strong> — изображение целиком набирают из шпона и наклеивают на основу.</li>
  <li><strong>Паркетри</strong> — тот же принцип, но узор геометрический: кубики, ромбы, шахматная клетка.</li>
</ul>
<p>Сегодня слова «маркетри» и «интарсия» часто используют как синонимы.</p>

<h2>Где маркетри применяют сегодня</h2>
<p>Техникой украшают панно, шкатулки, шахматные доски, столешницы, дверцы шкафов и стены кабинетов. Это штучная работа: на одно панно у мастера уходят недели.</p>
<p>Попробовать технику своими руками можно на <a href="obuchenie.html">курсе</a> в нашей школе. А если хотите начать с теории, прочитайте, <a href="kak-nauchitsya-marketri.html">как научиться маркетри с нуля</a>.</p>
</div></article>
{related(ARTICLE_FILE)}
'''
ARTICLE_LD = {"@context": "https://schema.org", "@type": "Article", "headline": ARTICLE_TITLE,
              "description": "История маркетри, этапы создания работы и отличия от интарсии и паркетри.",
              "image": SITE + "/img/og.jpg", "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ru",
              "author": {"@id": SITE + "/#school"},
              "publisher": {"@id": SITE + "/#school"}, "mainEntityOfPage": SITE + "/" + ARTICLE_FILE}
page(ARTICLE_FILE, "Маркетри: история и техника наборной мозаики из дерева",
     "Что такое маркетри, откуда пришла техника, как создаётся работа из шпона и чем маркетри отличается от интарсии и паркетри.",
     article, [crumbs_ld(c), ARTICLE_LD], og_type="article")


for a in ARTICLES:
    c = [("", "Главная"), ("zhurnal.html", "Журнал"), (a["file"], a["short"])]
    body = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>{a["title"]}</h1>
  <p class="meta">Школа маркетри Татьяны Гориной, 9 ноября 2026</p>
</div></div>
<article class="wrap"><div class="prose">
<p class="lead">{a["lead"]}</p>
<figure class="inlay">{pic(a["img"], a["img_alt"], lazy=False)}</figure>
{a["body"]}
</div></article>
{related(a["file"])}
'''
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
              "image": SITE + "/img/og.jpg", "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ru",
              "author": {"@id": SITE + "/#school"}, "publisher": {"@id": SITE + "/#school"},
              "mainEntityOfPage": SITE + "/" + a["file"]}
    page(a["file"], a["title"], a["desc"], body, [crumbs_ld(c), art_ld], og_type="article")

# ======================= Контакты =======================
c = [("", "Главная"), ("kontakty.html", "Контакты")]
contacts_page = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>Контакты</h1>
  <p class="lead">Чтобы записаться на занятие или задать вопрос, позвоните или напишите в мессенджер.</p>
</div></div>
<section style="padding-bottom:clamp(56px,8vw,112px)">
  <div class="wrap">
    {CONTACTS_DL}
    <iframe class="map" src="{MAP}" title="Мастерская на карте: {ADDRESS}" loading="lazy" allowfullscreen></iframe>
    <h2 id="route" style="margin-top:64px">Как добраться?</h2>
    <p class="lead">От метро «Пролетарская» до мастерской можно дойти пешком.</p>
    <figure class="route-map"><a href="img/route-ru.svg" target="_blank" rel="noopener"><img src="img/route-ru.svg" alt="Схема пешеходного маршрута от метро «Пролетарская», выход № 2, до Брошевского переулка, 4" width="1912" height="900" loading="lazy"></a></figure>
    <p class="route-zoom"><a href="img/route-ru.svg" target="_blank" rel="noopener">Открыть схему крупнее</a></p>
    <ol class="route-steps">
      <li>Выйдите из метро «Пролетарская» через выход № 2.</li>
      <li>Идите вдоль Абельмановской улицы и перейдите Волгоградский проспект по пешеходному переходу.</li>
      <li>Продолжайте путь по Абельмановской улице мимо Театра марионеток. Сразу после дома 9 с10 поверните направо.</li>
      <li>Дойдите до Брошевского переулка и поверните налево. Мастерская — в доме 4, по левой стороне.</li>
    </ol>
    <div class="entry">
      <h3>Как войти</h3>
      <dl>
        <div><dt>Подъезд</dt><dd>№ 1</dd></div>
        <div><dt>Домофон</dt><dd>01#902</dd></div>
        <div><dt>Этаж</dt><dd>первый, чёрная дверь слева</dd></div>
      </dl>
    </div>
  </div>
</section>
'''
page("kontakty.html", "Контакты — Школа маркетри Татьяны Гориной",
     f"Телефон, WhatsApp, Telegram, MAX и адрес мастерской: Москва, Брошевский переулок, 4. Запись на курс маркетри.",
     contacts_page, [crumbs_ld(c), ORG])

# ======================= Политика =======================
c = [("", "Главная"), ("politika.html", "Конфиденциальность")]
privacy = f'''
<div class="page-head"><div class="wrap">
  {crumbs_html(c)}
  <h1>Политика конфиденциальности</h1>
  <p class="meta">Редакция от 9 ноября 2026</p>
</div></div>
<div class="wrap"><div class="prose">
<p>Сайт носит информационный характер и не содержит форм для ввода персональных данных.</p>
<h2>Какие данные собираются</h2>
<p>При посещении сайта сервис Яндекс Метрика автоматически получает обезличенные технические данные: тип устройства и браузера, страницы, которые вы открывали, примерное местоположение по IP-адресу. Для этого используются файлы cookie.</p>
<h2>Зачем</h2>
<p>Эти данные нужны, чтобы понимать, какие материалы сайта полезны посетителям, и улучшать сайт. Мы не используем их, чтобы установить вашу личность.</p>
<h2>Как отказаться</h2>
<p>Вы можете отключить cookie в настройках браузера. Сайт продолжит работать.</p>
<h2>Если вы пишете нам</h2>
<p>Когда вы звоните или пишете в мессенджер или на почту, ваши имя и контакты используются только для ответа и записи на занятие и не передаются третьим лицам.</p>
<h2>Владелец сайта</h2>
<p class="placeholder">ФИО или название организации, ИНН и контакты владельца сайта.</p>
<p>Вопросы по этой политике: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div>
'''
page("politika.html", "Политика конфиденциальности — Школа маркетри Татьяны Гориной",
     "Какие данные собирает сайт школы маркетри и как они используются.", privacy, [crumbs_ld(c)])

# ======================= 404 =======================
nf = '''
<section class="page-head" style="padding-bottom:clamp(56px,8vw,112px)"><div class="wrap">
  <h1>Такой страницы нет</h1>
  <p class="lead">Возможно, ссылка устарела или в адресе опечатка. Начните с главной или посмотрите программу курса.</p>
  <div class="actions"><a class="btn" href="index.html">На главную</a><a class="text-link" href="obuchenie.html">Обучение</a></div>
</div></section>
'''
page("404.html", "Страница не найдена — Школа маркетри Татьяны Гориной",
     "Страница не найдена.", nf, noindex=True)

# ======================= Служебные файлы =======================
urls = [("", "1.0", "monthly"), ("obuchenie.html", "0.9", "monthly"), ("master.html", "0.7", "yearly"),
        ("galereya.html", "0.7", "monthly"), ("zhurnal.html", "0.6", "weekly"), (ARTICLE_FILE, "0.6", "yearly"),
        *[(a["file"], "0.6", "yearly") for a in ARTICLES],
        ("kontakty.html", "0.8", "yearly"), ("politika.html", "0.2", "yearly")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, p, f in urls:
    sm += f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>\n"
sm += "</urlset>\n"
open(OUT + "/sitemap.xml", "w").write(sm)
open(OUT + "/robots.txt", "w").write("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n")
open(OUT + "/site.webmanifest", "w").write(json.dumps({
    "name": NAME, "short_name": "Маркетри", "icons": [{"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": "#F6F5F2", "background_color": "#F6F5F2", "display": "browser"}, ensure_ascii=False, indent=2))
open(OUT + "/.htaccess", "w").write('''# Для хостингов на Apache (Beget, Timeweb и др.)
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8

<IfModule mod_rewrite.c>
  RewriteEngine On
  # Принудительный HTTPS
  RewriteCond %{HTTPS} off
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  # Без www
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
  # /index.html -> /
  RewriteRule ^index\\.html$ / [R=301,L]
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType image/jpeg "access plus 6 months"
  ExpiresByType image/png "access plus 6 months"
  ExpiresByType image/webp "access plus 6 months"
</IfModule>
''')
print("pages ok")
