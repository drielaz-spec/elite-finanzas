"""Genera index.html y las escenas de compositions/ para el vídeo "requisitos hipoteca".

Uso: python3 build.py words.json
words.json = [[palabra, inicio, fin], ...] en el tiempo del vídeo cortado.
"""
import json, sys, html, os

DUR = 34.86
W, H = 1080, 1920
GREEN = "#3DDC84"
GREEN_SCRIPT = "#7CF0B4"
YELLOW = "#FFE600"

words = json.load(open(sys.argv[1]))

FONTFACE = """
@font-face { font-family: 'Caveat'; src: url('assets/fonts/caveat-500.woff2') format('woff2'); font-weight: 500; }
"""

BASE_CSS = """
#root { position: absolute; inset: 0; }
.wrap { position: absolute; left: 0; right: 0; top: 285px; display: flex; flex-direction: column;
        align-items: center; gap: 12px; text-align: center; }
.script { font-family: 'Caveat'; font-weight: 500; color: %(gs)s; font-size: 60px; line-height: 1;
          text-shadow: 0 2px 6px rgba(0,0,0,.85), 0 0 18px rgba(0,0,0,.5); }
.big { font-family: 'Montserrat'; font-weight: 800; color: #fff; font-size: 60px; line-height: 1.08;
       text-transform: uppercase; letter-spacing: .01em; text-shadow: 0 3px 14px rgba(0,0,0,.55); max-width: 800px; }
.badge { font-family: 'Montserrat'; font-weight: 800; color: #fff; font-size: 40px; letter-spacing: .04em;
         border: 4px solid %(g)s; border-radius: 12px; padding: 6px 22px; background: rgba(0,0,0,.25); }
.list { display: flex; flex-direction: column; align-items: flex-start; gap: 12px; }
.item { display: flex; align-items: center; gap: 18px; font-family: 'Montserrat'; font-weight: 800;
        color: #fff; font-size: 44px; text-transform: uppercase; text-shadow: 0 3px 12px rgba(0,0,0,.55); }
.sq { width: 24px; height: 24px; border-radius: 6px; background: %(g)s; flex: none; }
.ck { color: %(g)s; font-size: 50px; line-height: 1; flex: none; text-shadow: 0 2px 6px rgba(0,0,0,.95), 0 0 14px rgba(0,0,0,.8); }
.hl { color: %(g)s; text-shadow: 0 2px 6px rgba(0,0,0,.9), 0 0 16px rgba(0,0,0,.6); }
.ul { position: relative; display: inline-block; }
.line { position: absolute; left: 0; right: 0; bottom: -10px; height: 8px; border-radius: 4px; background: %(g)s;
        transform-origin: left center; }
""" % {"g": GREEN, "gs": GREEN_SCRIPT}


def scene(sid, dur, body, script_js):
    return f"""<template>
  <style>{FONTFACE}{BASE_CSS}</style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const IN = (sel, t, y = 24) => tl.fromTo(sel, {{ opacity: 0, y }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, t);
    const POP = (sel, t) => tl.fromTo(sel, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, t);
    const DRAW = (sel, t) => tl.fromTo(sel, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, t);
{script_js}
    tl.to("#{sid}-out", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {dur - 0.32:.2f});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


# (id, inicio, fin, cuerpo html, animaciones js, [(tiempo_local, sfx)])
S = []

SL = 'tl.fromTo("{0}", {{x: -30}}, {{x: 0, duration: 0.35, ease: "power2.out"}}, {1});'
def slide(sel, t): return f'IN("{sel}", {t}, 0); ' + SL.format(sel, t)

# 01 Gancho (âncoras: ahorros 0.72, comprarte 2.02)
S.append(("hook", 1.2, 5.3, """
    <div id="hook-out" class="wrap">
      <div id="hook-s" class="script">si no tienes ahorros</div>
      <div id="hook-t" class="big">Y quieres comprarte <span class="ul hl">un piso<span id="hook-l" class="line"></span></span></div>
    </div>""", """
    IN("#hook-s", 0.0); POP("#hook-t", 1.3); DRAW("#hook-l", 1.9);""",
    [(1.3, "whoosh-short")]))

# 02 Situações (âncoras: alquiler 5.14, padres 6.82, personas 9.28)
S.append(("sit", 5.6, 10.4, """
    <div id="sit-out" class="wrap">
      <div class="list">
        <div id="sit-i1" class="item"><span class="sq"></span>Vives de alquiler</div>
        <div id="sit-i2" class="item"><span class="sq"></span>Vives con tus padres</div>
        <div id="sit-i3" class="item"><span class="sq"></span>Compartes piso</div>
      </div>
    </div>""", """
    """ + slide("#sit-i1", 0.0) + " " + slide("#sit-i2", 1.7) + " " + slide("#sit-i3", 4.0),
    []))

# 03 Oferta (âncoras: viabilidad 13.00, gratuito 15.20)
S.append(("oferta", 13.5, 16.9, """
    <div id="oferta-out" class="wrap">
      <div id="oferta-t" class="big" style="font-size:54px">Estudio de viabilidad hipotecaria</div>
      <div id="oferta-g" class="badge" style="font-size:40px;background:%(g)s;color:#10261a">GRATUITO</div>
    </div>""" % {"g": GREEN}, """
    POP("#oferta-t", 0.0); POP("#oferta-g", 2.1);""",
    []))

# 04 Três requisitos (âncoras: requisitos 16.58, documento 19.26, trabajando 21.66, sobreendeudado 24.44)
S.append(("req", 17.0, 26.7, """
    <div id="req-out" class="wrap">
      <div id="req-b" class="badge">TRES REQUISITOS</div>
      <div class="list">
        <div id="req-i1" class="item"><span class="ck">&#10003;</span>Documento en regla</div>
        <div id="req-i2" class="item"><span class="ck">&#10003;</span>Estar trabajando</div>
        <div id="req-i3" class="item"><span class="ck">&#10003;</span>No estar sobreendeudado</div>
      </div>
    </div>""", """
    POP("#req-b", 0.0); """ + slide("#req-i1", 2.7) + " " + slide("#req-i2", 5.1) + " " + slide("#req-i3", 7.9),
    [(0.0, "whoosh-short")]))

# 05 Chamada estática (âncora: mándame 28.56)
S.append(("cta", 29.0, DUR, """
    <div id="cta-out" class="wrap">
      <div id="cta-s" class="script">mándame un mensaje &#8595;</div>
    </div>""", """
    IN("#cta-s", 0.0);""",
    []))

os.makedirs("compositions", exist_ok=True)
hosts, sfx_tags, motivo_starts = [], [], []
for sid, st, en, body, js, sfx in S:
    en = min(en, DUR)
    dur = round(en - st, 2)
    open(f"compositions/{sid}.html", "w").write(scene(sid, dur, body, js))
    hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                 f'data-start="{st}" data-duration="{dur}" data-track-index="2" data-track-kind="graphics" '
                 f'data-width="{W}" data-height="{H}" style="z-index:4"></div>')
    for t, name in sfx:
        sfx_tags.append((round(st + t, 2), name))

sfx_tags.sort()
import subprocess
SFXDUR = {n: round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"assets/sfx/{n}.mp3"]).decode())-0.02,2) for n in ["whoosh-short"]}
VOL = {"whoosh-short": 0.22}
audio_html = []
lane_end = [0.0, 0.0]
for i, (t, name) in enumerate(sfx_tags):
    lane = 5 if t >= lane_end[0] else 6
    lane_end[lane - 5] = t + SFXDUR[name]
    audio_html.append(f'      <audio id="sfx{i}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}" '
                      f'data-duration="{SFXDUR[name]}" data-track-index="{lane}" data-volume="{VOL[name]}"></audio>')

# --- Subtítulos palabra por palabra ---
cap_words = []
for i, (t, s, e) in enumerate(words):
    s = max(0.12, s)
    nxt = words[i + 1][1] if i + 1 < len(words) else DUR
    end = min(nxt, max(e, s + 0.25) + 0.35, DUR - 0.05)
    end = max(end, s + 0.12)
    cap_words.append((html.escape(t.upper()), round(s, 3), round(end, 3)))

cap_body = "\n".join(f'    <div id="cw{i}" class="cw"><span class="cwt">{t}</span></div>' for i, (t, s, e) in enumerate(cap_words))
cap_js = "\n".join(
    f'    tl.set("#cw{i}", {{ visibility: "visible", opacity: 1 }}, {s}); '
    f'tl.fromTo("#cw{i} .cwt", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.09, ease: "power2.out" }}, {s}); '
    f'tl.set("#cw{i}", {{ opacity: 0, visibility: "hidden" }}, {e});'
    for i, (t, s, e) in enumerate(cap_words))
captions = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .cw {{ position: absolute; left: 0; right: 0; top: 1100px; height: 150px; display: flex; align-items: center;
           justify-content: center; text-align: center; opacity: 0; visibility: hidden; overflow: visible; }}
    .cwt {{ display: inline-block; font-family: 'Montserrat'; font-weight: 900; font-size: 112px; color: {YELLOW};
            text-transform: uppercase; -webkit-text-stroke: 14px #000; paint-order: stroke fill;
            text-shadow: 0 6px 0 rgba(0,0,0,.55); white-space: nowrap; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{cap_body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    document.querySelectorAll("#root .cwt").forEach((el) => {{
      const fit = window.__hyperframes && window.__hyperframes.fitTextFontSize
        ? window.__hyperframes.fitTextFontSize(el.textContent, {{ fontFamily: "Montserrat", fontWeight: 900, maxWidth: 800, baseFontSize: 112, minFontSize: 60 }})
        : null;
      if (fit && fit.fontSize) el.style.fontSize = fit.fontSize + "px";
    }});
{cap_js}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open("compositions/captions.html", "w").write(captions)

# --- Zoom suave: empuje lento en cada motivo, vuelta rápida al cambiar ---
# Câmera: só dois punch-ins rápidos (0,4 s), plano parado no resto.
zoom_js = [
    'tl.to("#cam", { scale: 1.04, duration: 0.4, ease: "power2.out" }, 0.05);',
    'tl.to("#cam", { scale: 1.0, duration: 0.4, ease: "power2.out" }, 16.25);',
]

index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
      #footage {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      #scrim {{ position: absolute; left: 0; top: 0; width: {W}px; height: 760px; z-index: 3;
                background: linear-gradient(to bottom, rgba(20,12,5,.74) 0%, rgba(20,12,5,.55) 50%, rgba(24,14,6,0) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <div id="cam">
        <video id="footage" class="clip" src="assets/source.mp4" data-start="0" data-duration="{DUR}"
               data-track-index="0" playsinline data-has-audio="true" data-volume="1"></video>
      </div>
      <div id="scrim" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore></div>
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
           data-start="0" data-duration="{DUR}" data-track-index="3" data-track-kind="captions"
           data-width="{W}" data-height="{H}" style="z-index:5"></div>
{chr(10).join(audio_html)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#cam", {{ scale: 1.0 }}, 0);
      {chr(10) + '      '.join(zoom_js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(index)
print("escenas:", len(S), "| sfx:", len(sfx_tags), "| palabras:", len(cap_words))
