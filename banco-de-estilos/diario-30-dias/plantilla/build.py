"""Plantilla «Diario 30 días» para HyperFrames (1080x1920).

Edita solo el bloque CONFIG y ejecuta:  python3 build.py
Genera index.html y compositions/*.html. Cada texto entra ~0,4 s después de su palabra.
"""
import html, json, os

# ===================== CONFIG =====================
VIDEO = "assets/demo.mp4"      # vídeo ya cortado
DUR = 12.0                     # duración del vídeo (ffprobe)
WORDS = "words-demo.json"      # [[palabra, inicio, fin], ...] del Whisper

ESCENAS = [
    # Gancho: título serif + línea de máquina de escribir
    {"tipo": "gancho", "id": "gancho", "inicio": 0.4, "fin": 5.1,
     "titulo": "Sin ahorros y viviendo<br>de alquiler", "linea": "y quieres comprarte un piso…",
     "linea_en": 1.9},
    # Día N + tarjeta de prueba con círculo rojo
    {"tipo": "dia_prueba", "id": "dia1", "inicio": 5.3, "fin": 8.4,
     "dia": "Día 1", "prueba_titulo": "Simulador hipotecario", "prueba_dato": "180.000 €",
     "prueba_nota": "precio de la vivienda", "prueba_en": 0.3},
    # Día N + tarjeta de cifras (verde)
    {"tipo": "dia_cifras", "id": "dia12", "inicio": 8.5, "fin": DUR,
     "dia": "Día 12 ✅", "cifra": "Aprobada", "sub": "hipoteca en 12 días",
     "metricas": [["90 %", "financiación"], ["30", "años"], ["0 €", "de ahorros"]], "cifras_en": 0.3},
]
# ==================================================

W, H = 1080, 1920
FONTS = """
@font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/instrument-serif.woff2') format('woff2'); }
@font-face { font-family: 'Poppins Italic'; src: url('assets/fonts/poppins-800-italic.woff2') format('woff2'); font-weight: 800; font-style: italic; }
@font-face { font-family: 'Courier Prime'; src: url('assets/fonts/courier-prime-700-italic.woff2') format('woff2'); font-weight: 700; font-style: italic; }
"""
CSS = FONTS + """
#root { position: absolute; inset: 0; }
.top { position: absolute; left: 80px; right: 80px; top: 250px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center; }
.serif { font-family: 'Instrument Serif'; color: #fff; font-size: 74px; line-height: 1.0; letter-spacing: -0.01em;
         text-shadow: 0 2px 10px rgba(0,0,0,.45); }
.tipo { font-family: 'Courier Prime'; font-weight: 700; font-style: italic; color: #fff; font-size: 42px;
        text-shadow: 0 2px 4px rgba(0,0,0,.95), 0 0 16px rgba(0,0,0,.75); align-self: flex-start; margin-left: 40px; }
.dia { font-family: 'Poppins Italic'; font-weight: 800; font-style: italic; color: #fff; font-size: 72px; line-height: 1;
       text-shadow: 0 3px 12px rgba(0,0,0,.45); }
.card { background: #fff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.25); padding: 26px 36px; min-width: 620px;
        font-family: 'Inter', sans-serif; color: #111; position: relative; }
.card .t { font-size: 30px; font-weight: 700; color: #333; }
.card .d { font-size: 76px; font-weight: 900; margin-top: 4px; position: relative; display: inline-block; }
.card .n { font-size: 30px; margin-top: 10px; color: #666; }
.circ { position: absolute; left: -46px; top: -12px; width: calc(100% + 92px); height: calc(100% + 24px); overflow: visible; }
.circ path { fill: none; stroke: #D62828; stroke-width: 6; stroke-linecap: round; }
.cifra { font-size: 104px; font-weight: 900; color: #14532D; line-height: 1; }
.met { display: flex; justify-content: space-between; gap: 30px; margin-top: 16px; }
.met b { display: block; font-size: 52px; font-weight: 900; color: #111; }
.met span { font-size: 28px; color: #666; }
"""

def scene(sid, dur, body, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const POP = (s, t) => tl.fromTo(s, {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }}, t);
    const FADE = (s, t) => tl.fromTo(s, {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, t);
{js}
    tl.to("#{sid}-out", {{ opacity: 0, duration: 0.15, ease: "power2.in" }}, {dur - 0.17:.2f});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

CIRCLE = '<svg class="circ" viewBox="0 0 100 40" preserveAspectRatio="none"><path id="{id}" d="M 40 3 C 75 0, 99 7, 98 20 C 97 34, 62 39, 34 38 C 8 37, 0 28, 2 19 C 4 8, 22 2, 52 2" pathLength="1" style="stroke-dasharray:1;stroke-dashoffset:1"/></svg>'

os.makedirs("compositions", exist_ok=True)
hosts = []
for e in ESCENAS:
    sid, st, en = e["id"], e["inicio"], min(e["fin"], DUR)
    dur = round(en - st, 2)
    if e["tipo"] == "gancho":
        chars = "".join(f'<span class="ch" style="opacity:0">{html.escape(c)}</span>' for c in e["linea"])
        body = f"""    <div id="{sid}-out" class="top">
      <div id="{sid}-t" class="serif">{e['titulo']}</div>
      <div id="{sid}-l" class="tipo">{chars}</div>
    </div>"""
        n = len(e["linea"]); step = min(0.06, 1.6 / max(n, 1))
        js = f'    FADE("#{sid}-t", 0.0);\n' + \
             f'    document.querySelectorAll("#{sid}-l .ch").forEach((c, i) => tl.set(c, {{ opacity: 1 }}, {e["linea_en"]} + i * {step:.3f}));'
    elif e["tipo"] == "dia_prueba":
        body = f"""    <div id="{sid}-out" class="top">
      <div id="{sid}-d" class="dia">{e['dia']}</div>
      <div id="{sid}-c" class="card"><div class="t">{e['prueba_titulo']}</div>
        <div class="d">{e['prueba_dato']}{CIRCLE.format(id=sid + '-o')}</div><div class="n">{e['prueba_nota']}</div></div>
    </div>"""
        js = f'    tl.set("#{sid}-d", {{ opacity: 1 }}, 0);\n    POP("#{sid}-c", {e["prueba_en"]});\n' + \
             f'    tl.to("#{sid}-o", {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut" }}, {e["prueba_en"] + 0.45});'
    elif e["tipo"] == "dia_cifras":
        mets = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in e["metricas"])
        body = f"""    <div id="{sid}-out" class="top">
      <div id="{sid}-d" class="dia">{e['dia']}</div>
      <div id="{sid}-c" class="card"><div class="cifra">{e['cifra']}</div><div class="n">{e['sub']}</div>
        <div class="met">{mets}</div></div>
    </div>"""
        js = f'    tl.set("#{sid}-d", {{ opacity: 1 }}, 0);\n    POP("#{sid}-c", {e["cifras_en"]});'
    open(f"compositions/{sid}.html", "w").write(scene(sid, dur, body, js))
    hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" '
                 f'data-duration="{dur}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:3"></div>')

# Palabra lateral (subtítulo discreto a la derecha del cuerpo)
words = json.load(open(WORDS))
items, sets = [], []
for i, (t, s, e) in enumerate(words):
    s = max(0.12, s); nxt = words[i + 1][1] if i + 1 < len(words) else DUR
    end = max(min(nxt, max(e, s + 0.25) + 0.3, DUR - 0.05), s + 0.12)
    items.append(f'    <div id="pw{i}" class="pw">{html.escape(t)}</div>')
    sets.append(f'    tl.set("#pw{i}", {{ visibility: "visible", opacity: 1 }}, {s:.3f}); tl.set("#pw{i}", {{ opacity: 0, visibility: "hidden" }}, {end:.3f});')
open("compositions/palabras.html", "w").write(f"""<template>
  <style>{FONTS}
    #root {{ position: absolute; inset: 0; }}
    .pw {{ position: absolute; left: 640px; width: 360px; top: 960px; text-align: center; font-family: 'Instrument Serif';
           font-size: 50px; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.6); opacity: 0; visibility: hidden; }}
  </style>
  <div id="root" data-composition-id="palabras" data-width="{W}" data-height="{H}">
{chr(10).join(items)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(sets)}
    window.__timelines["palabras"] = tl;
  </script>
</template>
""")

open("index.html", "w").write(f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #footage {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      #scrim {{ position: absolute; left: 0; top: 0; width: {W}px; height: 820px; z-index: 2;
                background: linear-gradient(to bottom, rgba(0,0,0,.42) 0%, rgba(0,0,0,.22) 55%, rgba(0,0,0,0) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <video id="footage" class="clip" src="{VIDEO}" data-start="0" data-duration="{DUR}" data-track-index="0"
             playsinline data-has-audio="true" data-volume="1"></video>
      <div id="scrim" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore></div>
{chr(10).join(hosts)}
      <div id="palabras" data-composition-id="palabras" data-composition-src="compositions/palabras.html" data-start="0"
           data-duration="{DUR}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:4"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("escenas:", len(ESCENAS), "| palabras:", len(words))
