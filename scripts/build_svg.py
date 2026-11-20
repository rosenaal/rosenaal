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

    # une seule fenêtre : courbe qui se dessine + un carré plein
    X0, Y0, t0 = 600, 56, 2.9
    pts = " ".join(f"{X0 + 32 + k * 24:.1f},{Y0 + 128 - (math.sin(k * 0.7) * 16 + k * 4.2):.1f}" for k in range(11))
    ui = f"""
<rect class="ui" style="animation-delay:{t0 - LOOP:.2f}s" x="{X0}" y="{Y0}" width="344" height="188" rx="12" fill="{c['block']}"/>
<polyline class="draw" points="{pts}" fill="none" stroke="{c['accent']}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect class="ui" style="animation-delay:{t0 + 1.6 - LOOP:.2f}s;transform-origin:{X0 + 300}px {Y0 + 150}px" x="{X0 + 284}" y="{Y0 + 134}" width="32" height="32" rx="8" fill="{c['ink']}"/>
"""
    css = f"""
.big{{font-family:{SANS};font-size:46px;font-weight:600;letter-spacing:-1.6px}}
.ui{{opacity:0;animation:pop {LOOP}s cubic-bezier(.2,.8,.2,1) infinite}}
@keyframes pop{{0%{{opacity:0;transform:scale(.96)}}4%,90%{{opacity:1;transform:none}}96%,100%{{opacity:0}}}}
.draw{{stroke-dasharray:400;stroke-dashoffset:400;animation:draw {LOOP}s ease-out infinite}}
@keyframes draw{{0%,{pct(t0 + 0.3)}{{stroke-dashoffset:400}}{pct(t0 + 1.6)},90%{{stroke-dashoffset:0}}96%,100%{{stroke-dashoffset:400}}}}
.caret{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.fade{{animation:fa {LOOP}s infinite}}
@keyframes fa{{0%,92%{{opacity:1}}97%{{opacity:0}}100%{{opacity:1}}}}
{kf}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ui{{opacity:1}}.draw{{stroke-dashoffset:0}}.cv0,.cv1{{display:none}}}}
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
