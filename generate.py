"""Gera o neofetch.svg colorido. Roda sozinho via GitHub Actions (idade atualiza automática)."""
from datetime import date
from html import escape

BIRTH = date(2007, 3, 8)
today = date.today()
age = today.year - BIRTH.year - ((today.month, today.day) < (BIRTH.month, BIRTH.day))

INFO = [
    ("title", "EliasBronzelle@github"),
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

FS, LH, CW = 13, 16, 7.8          # fonte, altura da linha, largura aprox. do caractere
PAD = 28
art_w = max(len(l) for l in art) * CW
info_x = PAD + art_w + 40
KEY_W = 118
rows = max(len(art), len(INFO))
H = int(rows * LH + PAD * 2 + 26)
W = int(info_x + KEY_W + 330 + PAD)
info_top = PAD + 12 + (len(art) - len(INFO)) * LH / 2

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('''<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="%d">
<stop offset="0" stop-color="#58a6ff"/><stop offset="0.5" stop-color="#bc8cff"/><stop offset="1" stop-color="#ff7eb6"/>
</linearGradient>
<style>
text{font-family:'JetBrains Mono','Fira Code',Consolas,'DejaVu Sans Mono','Courier New',monospace;font-size:%dpx;white-space:pre}
.k{fill:#58a6ff;font-weight:bold}.v{fill:#e6edf3}.t{fill:#ffa657;font-weight:bold}.s{fill:#d2a8ff;font-weight:bold}.d{fill:#484f58}
</style></defs>''' % (H, FS))
o.append(f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>')

for i, l in enumerate(art):
    y = PAD + 12 + i * LH
    o.append(f'<text x="{PAD}" y="{y}" fill="url(#g)" xml:space="preserve">{escape(l)}</text>')

y = info_top
for it in INFO:
    if it[0] == "title":
        o.append(f'<text x="{info_x}" y="{y}" class="t">{escape(it[1])}</text>')
        o.append(f'<line x1="{info_x}" y1="{y+5}" x2="{W-PAD}" y2="{y+5}" stroke="#30363d"/>')
    elif it[0] == "section":
        o.append(f'<text x="{info_x}" y="{y}" class="s">- {escape(it[1])}</text>')
        o.append(f'<line x1="{info_x+90}" y1="{y-4}" x2="{W-PAD}" y2="{y-4}" stroke="#30363d"/>')
    elif it[0] == "kv":
        o.append(f'<text x="{info_x}" y="{y}" class="k">{escape(it[1])}</text>')
        o.append(f'<text x="{info_x+KEY_W-14}" y="{y}" class="d">:</text>')
        o.append(f'<text x="{info_x+KEY_W}" y="{y}" class="v">{escape(it[2])}</text>')
    y += LH

# paleta de cores estilo neofetch
cols = ["#ff7b72", "#ffa657", "#e3b341", "#7ee787", "#79c0ff", "#58a6ff", "#bc8cff", "#ff7eb6"]
for i, c in enumerate(cols):
    o.append(f'<rect x="{info_x + i*22}" y="{H-PAD-6}" width="18" height="12" rx="3" fill="{c}"/>')
o.append('</svg>')
open("neofetch.svg", "w", encoding="utf-8").write("\n".join(o))
print("ok", W, H, "idade", age)
