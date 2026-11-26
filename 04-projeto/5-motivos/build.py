"""Genera index.html y las escenas de compositions/ para el vídeo "5 motivos".

Uso: python3 build.py words.json
words.json = [[palabra, inicio, fin], ...] en el tiempo del vídeo cortado.
"""
import json, sys, html, os

DUR = 82.23
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

# Gancho
S.append(("hook", 0.15, 6.45, """
    <div id="hook-out" class="wrap">
      <div id="hook-s" class="script">hoy te doy</div>
      <div id="hook-t" class="big">5 motivos para salir del <span class="ul hl">alquiler<span id="hook-l" class="line"></span></span></div>
    </div>""", """
    IN("#hook-s", 0.0); POP("#hook-t", 0.5); DRAW("#hook-l", 5.25);""",
    [(0.5, "pop"), (5.25, "click-soft")]))

# Motivo 1
S.append(("m1", 6.45, 20.6, """
    <div id="m1-out" class="wrap">
      <div id="m1-b" class="badge">MOTIVO 1</div>
      <div class="list">
        <div id="m1-i1" class="item"><span class="sq"></span>Reforma a tu gusto</div>
        <div id="m1-i2" class="item"><span class="sq"></span>+ valor para tu propiedad <span class="hl">&#8593;</span></div>
      </div>
    </div>""", """
    POP("#m1-b", 0.08); IN("#m1-i1", 2.1, 0); tl.fromTo("#m1-i1", {x: -30}, {x: 0, duration: 0.4, ease: "power2.out"}, 2.1);
    IN("#m1-i2", 8.85, 0); tl.fromTo("#m1-i2", {x: -30}, {x: 0, duration: 0.4, ease: "power2.out"}, 8.85);""",
    [(0.08, "pop"), (2.1, "click-soft"), (8.85, "sparkle")]))

# Motivo 2: barras cuota vs alquiler
S.append(("m2", 20.6, 27.55, """
    <div id="m2-out" class="wrap">
      <div id="m2-b" class="badge">MOTIVO 2</div>
      <div style="display:flex;flex-direction:column;gap:14px;align-items:flex-start;width:760px">
        <div id="m2-r1" style="display:flex;align-items:center;gap:18px">
          <div class="item" style="width:250px">Cuota</div>
          <div id="m2-bar1" style="width:200px;height:34px;border-radius:8px;background:%(g)s;transform-origin:left center"></div>
        </div>
        <div id="m2-r2" style="display:flex;align-items:center;gap:18px">
          <div class="item" style="width:250px">Alquiler</div>
          <div id="m2-bar2" style="width:480px;height:34px;border-radius:8px;border:4px solid #fff;background:rgba(255,255,255,.12);transform-origin:left center"></div>
        </div>
      </div>
    </div>""" % {"g": GREEN}, """
    POP("#m2-b", 0.05);
    IN("#m2-r1", 2.55, 0); DRAW("#m2-bar1", 2.62);
    IN("#m2-r2", 4.62, 0); DRAW("#m2-bar2", 4.72);""",
    [(0.05, "pop"), (2.62, "click-soft"), (4.72, "click-soft")]))

# Motivo 3: checklist
S.append(("m3", 27.55, 45.25, """
    <div id="m3-out" class="wrap">
      <div id="m3-b" class="badge">MOTIVO 3 · PAZ MENTAL</div>
      <div class="list">
        <div id="m3-i1" class="item"><span class="ck">&#10003;</span>Tu comida en la nevera</div>
        <div id="m3-i2" class="item"><span class="ck">&#10003;</span>Tu piso limpio</div>
        <div id="m3-i3" class="item"><span class="ck">&#10003;</span><span class="hl">Sin visitas indeseadas</span></div>
      </div>
    </div>""", """
    POP("#m3-b", 0.05);
    IN("#m3-i1", 3.27, 0); tl.fromTo("#m3-i1", {x: -30}, {x: 0, duration: 0.4, ease: "power2.out"}, 3.27);
    IN("#m3-i2", 14.43, 0); tl.fromTo("#m3-i2", {x: -30}, {x: 0, duration: 0.4, ease: "power2.out"}, 14.43);
    POP("#m3-i3", 15.65);""",
    [(0.05, "pop"), (3.27, "click-soft"), (14.43, "click-soft"), (15.65, "pop")]))

# Motivo 4a: inversión + flujo
S.append(("m4", 45.25, 57.55, """
    <div id="m4-out" class="wrap">
      <div id="m4-b" class="badge">MOTIVO 4</div>
      <div id="m4-t" class="big" style="font-size:52px">Inversión patrimonial</div>
      <div style="display:flex;align-items:center;gap:18px">
        <div id="m4-f1" class="badge" style="font-size:36px">VENDES</div>
        <div id="m4-ar" class="hl" style="font-family:Montserrat;font-weight:800;font-size:48px">&#8594;</div>
        <div id="m4-f2" class="badge" style="font-size:36px;background:%(g)s;color:#10261a">COMPRAS OTRA</div>
      </div>
    </div>""" % {"g": GREEN}, """
    POP("#m4-b", 0.05); IN("#m4-t", 2.2);
    POP("#m4-f1", 7.23); tl.fromTo("#m4-ar", {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: 0.35, ease: "power2.out"}, 9.9);
    POP("#m4-f2", 10.27);""",
    [(0.05, "pop"), (2.2, "click-soft"), (7.23, "click-soft"), (10.27, "pop")]))

# Motivo 4b: el alquiler nunca vuelve
S.append(("m4b", 57.6, 62.3, """
    <div id="m4b-out" class="wrap">
      <div id="m4b-s" class="script">en cambio, el alquiler…</div>
      <div id="m4b-t" class="big" style="font-size:72px"><span class="ul">nunca vuelve<span id="m4b-l" class="line" style="background:#ff5a5a"></span></span></div>
    </div>""", """
    IN("#m4b-s", 0.05); POP("#m4b-t", 3.36); DRAW("#m4b-l", 3.76);""",
    [(3.36, "chime")]))

# Motivo 5
S.append(("m5", 62.3, 77.25, """
    <div id="m5-out" class="wrap">
      <div id="m5-b" class="badge">MOTIVO 5</div>
      <div id="m5-t" class="big" style="font-size:54px">Tranquilidad en tu <span class="hl">jubilación</span></div>
      <div id="m5-s" class="script">sin miedo a que algún día te echen</div>
    </div>""", """
    POP("#m5-b", 0.4); IN("#m5-t", 2.82); IN("#m5-s", 7.92);""",
    [(0.4, "pop"), (2.82, "click-soft"), (7.92, "click-soft")]))

# Llamada a la acción
S.append(("cta", 77.25, DUR, """
    <div id="cta-out" class="wrap">
      <div id="cta-s" class="script">cuéntame &#8595;</div>
      <div id="cta-t" class="big" style="font-size:56px">¿Qué otro beneficio <span class="hl">añadirías?</span></div>
    </div>""", """
    IN("#cta-s", 0.05); POP("#cta-t", 0.45);""",
    [(0.45, "notification")]))

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
beats = [0.0, 6.45, 20.6, 27.55, 45.25, 62.3, 77.25, DUR]
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
