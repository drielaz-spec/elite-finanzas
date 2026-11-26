"""Genera index.html y las escenas de compositions/ para el vídeo "estudio hipotecario".

Uso: python3 build.py words.json
words.json = [[palabra, inicio, fin], ...] en el tiempo del vídeo cortado.
"""
import json, sys, html, os

DUR = 86.42
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
.ck { color: %(g)s; font-size: 50px; line-height: 1; flex: none; }
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

SL = 'tl.fromTo("{0}", {{x: -30}}, {{x: 0, duration: 0.4, ease: "power2.out"}}, {1});'
def slide(sel, t): return f'IN("{sel}", {t}, 0); ' + SL.format(sel, t)

# 1 Gancho
S.append(("hook", 0.12, 6.1, """
    <div id="hook-out" class="wrap">
      <div id="hook-s" class="script">antes de buscar vivienda…</div>
      <div id="hook-t" class="big">¿Por qué hacer primero un <span class="ul hl">estudio hipotecario?<span id="hook-l" class="line"></span></span></div>
    </div>""", """
    IN("#hook-s", 0.0); POP("#hook-t", 0.35); DRAW("#hook-l", 4.45);""",
    [(0.35, "pop"), (4.45, "click-soft")]))

# 2 Experiencia
S.append(("exp", 6.15, 14.45, """
    <div id="exp-out" class="wrap">
      <div id="exp-s" class="script">les digo por qué</div>
      <div id="exp-b" class="badge">MI EXPERIENCIA</div>
      <div class="list">
        <div id="exp-i1" class="item"><span class="sq"></span>Inmobiliaria muy grande</div>
        <div id="exp-i2" class="item"><span class="sq"></span>Y muy reconocida</div>
      </div>
    </div>""", """
    IN("#exp-s", 0.05); POP("#exp-b", 1.6); """ + slide("#exp-i1", 3.95) + " " + slide("#exp-i2", 6.4), 
    [(1.6, "pop"), (3.95, "click-soft"), (6.4, "click-soft")]))

# 3 La regla
S.append(("regla", 14.5, 23.3, """
    <div id="regla-out" class="wrap">
      <div id="regla-s" class="script">la regla era clara</div>
      <div id="regla-t1" class="big" style="font-size:54px">No enseñábamos viviendas</div>
      <div id="regla-t2" class="big" style="font-size:54px"><span class="ul hl">sin hipoteca preaprobada<span id="regla-l" class="line"></span></span></div>
    </div>""", """
    IN("#regla-s", 0.05); IN("#regla-t1", 2.55); POP("#regla-t2", 6.8); DRAW("#regla-l", 7.6);""",
    [(2.55, "click-soft"), (6.8, "pop")]))

# 4 Cuestionario
S.append(("cuest", 23.35, 35.3, """
    <div id="cuest-out" class="wrap">
      <div id="cuest-s" class="script">antes de cada visita</div>
      <div id="cuest-b" class="badge">EL CUESTIONARIO</div>
      <div id="cuest-q" class="big" style="font-size:52px">¿Cuál será su <span class="hl">forma de pago?</span></div>
    </div>""", """
    IN("#cuest-s", 0.05); POP("#cuest-b", 4.5); POP("#cuest-q", 8.65);""",
    [(4.5, "pop"), (8.65, "click-soft")]))

# 5 Checklist hipoteca
S.append(("check", 35.35, 50.8, """
    <div id="check-out" class="wrap">
      <div id="check-b" class="badge">SI ES CON HIPOTECA</div>
      <div class="list">
        <div id="check-i1" class="item"><span class="ck">&#10003;</span>¿Consultó con su banco?</div>
        <div id="check-i2" class="item"><span class="ck">&#10003;</span>¿Ya está aprobada?</div>
        <div id="check-i3" class="item"><span class="ck">&#10003;</span><span class="hl">¿De cuánto es?</span></div>
      </div>
    </div>""", """
    POP("#check-b", 2.75); """ + slide("#check-i1", 8.05) + " " + slide("#check-i2", 11.2) + " POP(\"#check-i3\", 13.1);",
    [(2.75, "pop"), (8.05, "click-soft"), (11.2, "click-soft"), (13.1, "pop")]))

# 6 El error
S.append(("error", 50.85, 57.9, """
    <div id="error-out" class="wrap">
      <div id="error-s" class="script">el error más común</div>
      <div id="error-t" class="big" style="font-size:54px">Buscar vivienda <span class="ul">sin saber cuánto te aprueban<span id="error-l" class="line" style="background:#ff5a5a"></span></span></div>
    </div>""", """
    IN("#error-s", 0.05); POP("#error-t", 2.1); DRAW("#error-l", 5.8);""",
    [(2.1, "pop"), (5.8, "click-soft")]))

# 7 La solución
S.append(("solu", 57.95, 72.75, """
    <div id="solu-out" class="wrap">
      <div id="solu-b" class="badge">ANTES DE BUSCAR</div>
      <div style="display:flex;align-items:center;gap:18px">
        <div id="solu-f1" class="badge" style="font-size:34px">TU BANCO</div>
        <div id="solu-o" class="script" style="font-size:52px">o</div>
        <div id="solu-f2" class="badge" style="font-size:34px;background:%(g)s;color:#10261a">BRÓKER HIPOTECARIO</div>
      </div>
      <div id="solu-t" class="big" style="font-size:50px">¿Hasta cuánto te puedes <span class="hl">permitir?</span></div>
    </div>""" % {"g": GREEN}, """
    POP("#solu-b", 0.05); POP("#solu-f1", 7.0); IN("#solu-o", 7.95, 0); POP("#solu-f2", 8.45); IN("#solu-t", 10.3);""",
    [(0.05, "pop"), (7.0, "click-soft"), (8.45, "pop"), (10.3, "click-soft")]))

# 8 Cierre: pregunta
S.append(("cta1", 72.8, 79.3, """
    <div id="cta1-out" class="wrap">
      <div id="cta1-s" class="script">¿estás pensando en comprar?</div>
      <div id="cta1-t" class="big" style="font-size:54px">¿No sabes hasta cuánto <span class="hl">te pueden dar?</span></div>
    </div>""", """
    IN("#cta1-s", 0.05); POP("#cta1-t", 2.7);""",
    [(2.7, "pop")]))

# 9 Cierre: oferta
S.append(("cta2", 79.35, DUR, """
    <div id="cta2-out" class="wrap">
      <div id="cta2-s" class="script">escríbeme por mensaje &#8595;</div>
      <div id="cta2-t" class="big" style="font-size:58px">Estudio hipotecario</div>
      <div id="cta2-g" class="badge" style="font-size:38px;background:%(g)s;color:#10261a">GRATIS Y SIN COMPROMISO</div>
    </div>""" % {"g": GREEN}, """
    IN("#cta2-s", 0.05); POP("#cta2-t", 3.3); POP("#cta2-g", 4.3);""",
    [(0.05, "notification"), (3.3, "click-soft"), (4.3, "pop")]))

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
SFXDUR = {n: round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"assets/sfx/{n}.mp3"]).decode())-0.02,2) for n in ["pop","click-soft","sparkle","chime","notification"]}
VOL = {"pop": 0.35, "click-soft": 0.45, "sparkle": 0.3, "chime": 0.3, "notification": 0.35}
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
beats = [0.0, 6.15, 14.5, 23.35, 35.35, 50.85, 57.95, 72.8, DUR]
zoom_js = []
for a, b in zip(beats, beats[1:]):
    if a > 0:
        zoom_js.append(f'tl.to("#cam", {{ scale: 1.0, duration: 0.45, ease: "power2.inOut" }}, {a - 0.2:.2f});')
    zoom_js.append(f'tl.to("#cam", {{ scale: 1.045, duration: {b - a - 0.5:.2f}, ease: "sine.inOut" }}, {a + 0.25:.2f});')

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
        <video id="footage" class="clip" src="assets/footage.mp4" data-start="0" data-duration="{DUR}"
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
