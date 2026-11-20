"""Génère les SVG animés du profil (version claire et sombre).

GitHub sert les SVG comme des <img> : seules les animations CSS internes
fonctionnent, pas de JS ni de police externe -> pile système.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(card="#0a0c10", stroke="#21262d", text="#f0f6fc", muted="#6e7681",
                 block="#161b22", ink="#f0f6fc", accent="#7ee0b5", dot="#e6edf3"),
    "light": dict(card="#ffffff", stroke="#d0d7de", text="#1f2328", muted="#8c959f",
                  block="#f6f8fa", ink="#1f2328", accent="#1a7f5a", dot="#1f2328"),
}

LOOP = 9  # secondes


def pct(t):
    return f"{t / LOOP * 100:.2f}%"


def hero(name, c):
    W, H = 1000, 300
    lines = [("Product engineer.", c["text"]), ("AI &amp; interfaces.", c["muted"])]
    text, covers, kf = "", "", ""
    for i, (line, fill) in enumerate(lines):
        start, end = 0.9 + i * 0.9, 1.7 + i * 0.9
        y = 158 + i * 56
        text += f'<text x="56" y="{y}" class="big" fill="{fill}">{line}</text>'
        covers += f'<rect class="cv{i}" x="52" y="{y - 46}" width="440" height="60" fill="{c["card"]}"/>'
        kf += (f"@keyframes r{i}{{0%,{pct(start)}{{transform:translateX(0)}}{pct(end)},100%{{transform:translateX(450px)}}}}"
               f".cv{i}{{animation:r{i} {LOOP}s steps(5,end) infinite}}")

    # prompt IA -> l'interface demandée apparaît (un toggle qui s'allume)
    X0, W0 = 612, 332            # zone droite
    cx = X0 + W0 / 2
    iy = 70                      # haut du champ de saisie
    prompt = "make a toggle"
    t_type, t_think, t_ui, t_on = 2.7, 4.0, 4.9, 5.6
    cw = len(prompt) * 9.1       # largeur mono 15px
    sx, sy = X0 + 26, iy + 23    # étincelle
    spark = (f"M{sx},{sy - 8} C{sx + 1},{sy - 2} {sx + 2},{sy - 1} {sx + 8},{sy} "
             f"C{sx + 2},{sy + 1} {sx + 1},{sy + 2} {sx},{sy + 8} "
             f"C{sx - 1},{sy + 2} {sx - 2},{sy + 1} {sx - 8},{sy} "
             f"C{sx - 2},{sy - 1} {sx - 1},{sy - 2} {sx},{sy - 8}Z")
    ty = 196                      # centre du toggle
    dots = "".join(
        f'<circle class="think" style="animation-delay:{k * 0.15 - LOOP:.2f}s" cx="{cx - 14 + k * 14}" cy="{ty}" r="3.5" fill="{c["muted"]}"/>'
        for k in range(3))
    ui = f"""
<g class="ui in">
<rect x="{X0}" y="{iy}" width="{W0}" height="46" rx="23" fill="{c['block']}" stroke="{c['stroke']}"/>
<path d="{spark}" fill="{c['accent']}"/>
<text x="{X0 + 46}" y="{iy + 28}" font-family="{MONO}" font-size="15" fill="{c['text']}">{prompt}</text>
<rect class="typ" x="{X0 + 44}" y="{iy + 10}" width="{cw + 6}" height="26" fill="{c['block']}"/>
<circle cx="{X0 + W0 - 23}" cy="{iy + 23}" r="14" fill="{c['ink']}"/>
<path d="M{X0 + W0 - 23},{iy + 29} V{iy + 17} M{X0 + W0 - 28},{iy + 22} L{X0 + W0 - 23},{iy + 17} L{X0 + W0 - 18},{iy + 22}" stroke="{c['card']}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g class="thinkg">{dots}</g>
<g class="ui tg2" style="transform-origin:{cx}px {ty}px">
<rect class="track" x="{cx - 38}" y="{ty - 21}" width="76" height="42" rx="21"/>
<circle class="knob" cx="{cx - 17}" cy="{ty}" r="16" fill="#ffffff"/>
</g>
"""
    def p(t):
        return pct(t)
    css = f"""
.big{{font-family:{SANS};font-size:46px;font-weight:600;letter-spacing:-1.6px}}
.ui{{opacity:0}}
.in{{animation:a1 {LOOP}s cubic-bezier(.2,.8,.2,1) infinite}}
.tg2{{animation:a2 {LOOP}s cubic-bezier(.2,.8,.2,1) infinite}}
@keyframes a1{{0%,{p(0.3)}{{opacity:0;transform:scale(.96)}}{p(0.7)},90%{{opacity:1;transform:none}}96%,100%{{opacity:0}}}}
@keyframes a2{{0%,{p(t_ui)}{{opacity:0;transform:scale(.9)}}{p(t_ui + 0.35)},90%{{opacity:1;transform:none}}96%,100%{{opacity:0}}}}
.typ{{animation:typ {LOOP}s steps({len(prompt)},end) infinite}}
@keyframes typ{{0%,{p(t_type)}{{transform:translateX(0)}}{p(t_type + 1.1)},100%{{transform:translateX({cw + 8:.0f}px)}}}}
.thinkg{{opacity:0;animation:tg {LOOP}s infinite}}
@keyframes tg{{0%,{p(t_think - 0.05)}{{opacity:0}}{p(t_think)},{p(t_ui - 0.1)}{{opacity:1}}{p(t_ui)},100%{{opacity:0}}}}
.think{{animation:th .6s ease-in-out infinite alternate}}
@keyframes th{{from{{opacity:.25}}to{{opacity:1}}}}
.track{{fill:{c['stroke']};animation:tr {LOOP}s infinite}}
@keyframes tr{{0%,{p(t_on)}{{fill:{c['stroke']}}}{p(t_on + 0.25)},100%{{fill:{c['accent']}}}}}
.knob{{animation:kn {LOOP}s cubic-bezier(.3,1.4,.5,1) infinite}}
@keyframes kn{{0%,{p(t_on)}{{transform:translateX(0)}}{p(t_on + 0.35)},100%{{transform:translateX(34px)}}}}
.caret{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.fade{{animation:fa {LOOP}s infinite}}
@keyframes fa{{0%,92%{{opacity:1}}97%{{opacity:0}}100%{{opacity:1}}}}
{kf}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ui{{opacity:1}}.typ,.thinkg{{display:none}}.track{{fill:{c['accent']}}}.knob{{transform:translateX(34px)}}.cv0,.cv1{{display:none}}}}
"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Product engineer. AI and interfaces.">
<style>{css}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{c['card']}" stroke="{c['stroke']}"/>
<text x="56" y="76" font-family="{MONO}" font-size="13" fill="{c['muted']}">&gt; alex</text>
<rect class="caret" x="112" y="65" width="7" height="14" fill="{c['muted']}"/>
<g class="fade">{text}{covers}</g>
{ui}
</svg>
"""
    (OUT / f"hero-{name}.svg").write_text(svg)


def field(name, c):
    W, H = 1000, 140
    cols, rows = 72, 7
    x0, gap = 56, (W - 112) / (cols - 1)
    dots = []
    for j in range(rows):
        for i in range(cols):
            y = 34 + j * (72 / (rows - 1))
            d = (math.sin(i * 0.28) + math.cos(j * 0.6) + i * 0.06) * 0.55
            dots.append(f'<circle cx="{x0 + i * gap:.1f}" cy="{y:.1f}" r="1.6" style="animation-delay:{d - 8:.2f}s"/>')
    css = f"""
circle{{fill:{c['dot']};opacity:.07;animation:w 3.4s ease-in-out infinite}}
@keyframes w{{0%,100%{{opacity:.07}}50%{{opacity:.85}}}}
@media (prefers-reduced-motion:reduce){{circle{{animation:none;opacity:.3}}}}
"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lab">
<style>{css}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{c['card']}" stroke="{c['stroke']}"/>
<g>{''.join(dots)}</g>
<text x="56" y="126" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{c['muted']}">LAB</text>
</svg>
"""
    (OUT / f"lab-{name}.svg").write_text(svg)


for n, c in THEMES.items():
    hero(n, c)
    field(n, c)
print("ok")
