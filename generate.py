"""Gera o neofetch.svg (estilo terminal, animado). Roda sozinho via GitHub Actions."""
from datetime import date
from html import escape

BIRTH = date(2007, 3, 8)
today = date.today()
age = today.year - BIRTH.year - ((today.month, today.day) < (BIRTH.month, BIRTH.day))

USER = "EliasBronzelle"
INFO = [
    ("title", f"{USER}@github"),
    ("kv", "OS", "Windows, Android"),
    ("kv", "Uptime", f"{age} anos"),
    ("kv", "Host", "RC Equipamentos Cerâmicos"),
    ("kv", "Kernel", "TI, Marketing, Financeiro"),
    ("kv", "IDE", "VSCode, Canva, Photoshop"),
    ("gap",),
    ("kv", "Lang.Code", "Python"),
    ("kv", "Lang.Web", "HTML, CSS"),
    ("kv", "Lang.Real", "Português BR, English"),
    ("gap",),
    ("kv", "Hobby.Soft", "Modding, Automações, Smart Home"),
    ("kv", "Hobby.Hard", "PC, Manutenção de eletrônicos"),
    ("kv", "Hobby.Music", "Guitarra, Timbres"),
    ("gap",),
    ("section", "Contact"),
    ("kv", "Email", "contato.eliasbronzelle@gmail.com"),
    ("kv", "Discord", "eliasbit"),
    ("kv", "Instagram", "eliasbronzelle"),
]

art = [l for l in open("art.txt", encoding="utf-8").read().split("\n") if l.strip()]
m = min(len(l) - len(l.lstrip()) for l in art)
art = [l[m:].rstrip() for l in art]

FS, LH, CW = 15, 18, 9.0          # fonte, altura da linha, largura do caractere
PAD, BAR = 26, 34                 # margem e altura da barra de título
KEY_W = 128
art_w = max(len(l) for l in art) * CW
info_x = PAD + art_w + 30
longest = max(len(i[2]) for i in INFO if i[0] == "kv")
W = int(info_x + KEY_W + longest * CW + PAD)

top_prompt_y = BAR + PAD + 6
art_top = top_prompt_y + 26
rows = max(len(art), len(INFO))
art_bottom = art_top + len(art) * LH
bottom_prompt_y = art_bottom + 30
H = int(bottom_prompt_y + PAD)
info_top = art_top + (len(art) - len(INFO)) * LH / 2

# onda de cor: azul -> roxo -> azul, deslizando em loop contínuo
P = 240                            # período da onda (px)
DX, DY = P, P * 0.55               # direção diagonal
BLUE, PURPLE = "#4f9dff", "#b36bff"

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append(f'''<defs>
<linearGradient id="wave" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{DX}" y2="{DY}" spreadMethod="repeat">
<stop offset="0" stop-color="{BLUE}"/><stop offset="0.5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{BLUE}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{DX} {DY}" dur="5s" repeatCount="indefinite"/>
</linearGradient>
<style>
text{{font-family:'JetBrains Mono','Fira Code',Consolas,'DejaVu Sans Mono','Courier New',monospace;font-size:{FS}px;white-space:pre}}
.k{{fill:#58a6ff;font-weight:bold}}.v{{fill:#e6edf3}}.t{{fill:#ffa657;font-weight:bold}}.s{{fill:#d2a8ff;font-weight:bold}}.d{{fill:#6e7681}}.p{{fill:#7ee787;font-weight:bold}}.c{{fill:#e6edf3}}
</style></defs>''')
o.append(f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>')

# barra de título estilo janela de terminal
o.append(f'<path d="M0 12a12 12 0 0 1 12-12h{W-24}a12 12 0 0 1 12 12v{BAR-12}H0z" fill="#161b22"/>')
o.append(f'<line x1="0" y1="{BAR}" x2="{W}" y2="{BAR}" stroke="#30363d"/>')
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    o.append(f'<circle cx="{22 + i*20}" cy="{BAR/2}" r="6" fill="{c}"/>')
o.append(f'<text x="{W/2}" y="{BAR/2+5}" text-anchor="middle" class="d">{USER.lower()} — neofetch</text>')

# prompt de cima
o.append(f'<text x="{PAD}" y="{top_prompt_y}"><tspan class="p">{USER.lower()}@github</tspan><tspan class="d">:</tspan><tspan class="k">~</tspan><tspan class="c">$ neofetch</tspan></text>')

# arte (onda azul ↔ roxo)
for i, l in enumerate(art):
    y = art_top + (i + 1) * LH
    o.append(f'<text x="{PAD}" y="{y}" fill="url(#wave)" xml:space="preserve">{escape(l)}</text>')

# painel de infos
y = info_top + LH
for it in INFO:
    if it[0] == "title":
        o.append(f'<text x="{info_x}" y="{y}" class="t">{escape(it[1])}</text>')
        o.append(f'<line x1="{info_x}" y1="{y+6}" x2="{W-PAD}" y2="{y+6}" stroke="#30363d"/>')
    elif it[0] == "section":
        o.append(f'<text x="{info_x}" y="{y}" class="s">- {escape(it[1])}</text>')
        o.append(f'<line x1="{info_x+96}" y1="{y-5}" x2="{W-PAD}" y2="{y-5}" stroke="#30363d"/>')
    elif it[0] == "kv":
        o.append(f'<text x="{info_x}" y="{y}" class="k">{escape(it[1])}</text>')
        o.append(f'<text x="{info_x+KEY_W-16}" y="{y}" class="d">:</text>')
        o.append(f'<text x="{info_x+KEY_W}" y="{y}" class="v">{escape(it[2])}</text>')
    y += LH

# paleta de cores
cols = ["#ff7b72", "#ffa657", "#e3b341", "#7ee787", "#79c0ff", "#58a6ff", "#bc8cff", "#ff7eb6"]
pal_y = art_bottom - 12
for i, c in enumerate(cols):
    o.append(f'<rect x="{info_x + i*24}" y="{pal_y}" width="20" height="13" rx="3" fill="{c}"/>')

# prompt de baixo com cursor piscando
o.append(f'<text x="{PAD}" y="{bottom_prompt_y}"><tspan class="p">{USER.lower()}@github</tspan><tspan class="d">:</tspan><tspan class="k">~</tspan><tspan class="c">$ </tspan>'
         f'<tspan fill="#e6edf3">█<animate attributeName="fill-opacity" values="1;0;1" keyTimes="0;0.5;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></tspan></text>')
o.append('</svg>')
open("neofetch.svg", "w", encoding="utf-8").write("\n".join(o))
print("ok", W, H, "idade", age)
