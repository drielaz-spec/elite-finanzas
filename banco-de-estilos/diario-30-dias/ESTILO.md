# Estilo «Diario 30 días» (diario con pruebas)

Referencia: `referencia.mp4` (reel de Instagram, 1:26, 720×1280, 30 fps, en portugués).
Hoja de contactos: `hoja-de-contactos.png` · Fotogramas: `fotogramas/` · Transcripción: `transcripcion.json`.

## Cuándo usarlo
Historias de resultado contadas en el tiempo: «en X días pasó esto», casos de clientes,
el antes y después de un proceso (por ejemplo: «de cero ahorros a las llaves en 60 días»).
Necesita **pruebas visuales** (capturas, mensajes, cifras). Sin pruebas pierde la fuerza.

## Estructura del guion
| Bloque | Tiempo | Qué hace | En la referencia |
|---|---|---|---|
| Gancho de contraste | 0–7 s | situación mala → resultado grande, en una frase | «En septiembre estaba preocupada por el dinero… y el sábado di una charla sobre haber hecho 1 millón» |
| Curiosidad | 7–10 s | un detalle raro que obliga a quedarse | «alguien me pagó por un link vacío» |
| Promesa de formato | 10–13 s | anuncia el formato | «30 días en 30 segundos» |
| Diario | 13–51 s | un «Día N» por hito, cada uno con su prueba | Día 1, 2, 3, 4, 10, 13, 17, 25, 27 |
| Resultado | 48–56 s | la cifra grande | «335 alumnas y 670 mil reales» |
| Oferta | 56–81 s | lista de lo que incluye, con emojis | producto, lanzar, herramientas, central |
| Llamada | 81–86 s | palabra clave para comentar | «Comenta "BLACK"» |

## Elementos visuales
1. **Título serif fino (gancho).** Blanco, serif condensada (fuente: *Instrument Serif*),
   ~64 px en 1080, dos líneas centradas en el tercio superior, sombra suave. Sin caja.
2. **Línea de máquina de escribir.** Debajo del título, blanca, *Courier Prime* negrita cursiva,
   ~40 px, se escribe letra a letra siguiendo la voz y termina con «…».
3. **Cabecera «Día N» (capítulo).** *Poppins* 800 cursiva, blanca, ~64 px, arriba y centrada.
   Se queda fija mientras dura ese día y cambia de golpe al siguiente. Es el hilo del vídeo.
   Variantes: frase corta en la misma fuente («29 horas después del primer vídeo…»,
   «Finalmente decidí qué vender!!!»), con emoji al final cuando suma.
4. **Tarjetas de prueba.** Capturas reales (perfil, mensajes, comentarios, panel) sobre tarjeta
   blanca con esquinas redondeadas, debajo de la cabecera y encima de la cabeza. Entran con
   un pop corto. A veces dos a la vez (arriba y abajo).
5. **Círculo rojo a mano.** Elipse roja de trazo irregular que se dibuja sobre el dato clave de
   la captura (seguidores, nº de alumnas).
6. **Tarjeta de cifras.** Blanca, cifra principal en **verde oscuro** (#14532D) muy grande
   («R$ 670 mil»), subtítulo pequeño gris y tres métricas debajo («335 · 1.728 · 19 %»).
7. **Palabra lateral (subtítulo).** Una sola palabra a la vez, serif fina blanca (*Instrument Serif*),
   ~44 px, **a la derecha del cuerpo** (x ≈ 75 %, y ≈ 52 %), sin contorno, sombra suave.
   Discreta: acompaña, no protagoniza.
8. **Palabra gigante.** En el momento de marca, una palabra enorme (*Poppins* 800 cursiva,
   ~180 px) en el tercio superior, con subtítulo y emoji ✅ («Yap / Validado ✅»).
9. **Lista que acumula con emojis.** Ítems en *Poppins* 800 cursiva, uno debajo del otro,
   cada uno con su emoji delante (📱 🚀 🛠️), entran al ritmo de la voz.
10. **Imagen en imagen.** Un recorte pequeño de un vídeo anterior en la esquina superior
    derecha, para «el primer vídeo».

## Ritmo y cámara
- Plano fijo, casi sin movimiento. Algún corte en seco entre frases (7,4 · 13,2 · 16,4 · 39,4 s).
- La cabecera cambia cada 2–5 s en el diario: el ritmo lo marcan los textos, no la cámara.
- Siempre hay texto arriba; la parte central (rostro) queda libre.

## Paleta
- Blanco #FFFFFF para todo el texto sobre el vídeo.
- Verde oscuro #14532D en cifras; rojo #D62828 en círculos y marcos.
- Tarjetas blancas #FFFFFF, radio ~14 px, sombra suave.

## Adaptación a nuestros vídeos (español, hipotecas)
- Mantener nuestra **legenda amarilla** solo si el vídeo no lleva la palabra lateral: no usar las dos.
- Ejemplos de «Día N»: «Día 1 · sin ahorros», «Día 12 · estudio de viabilidad», «Día 45 · hipoteca aprobada ✅»,
  con capturas reales (simulador, aprobación del banco, mensajes de clientes, siempre con
  permiso y datos personales tapados).
- Cumplir la skill `animacao-talking-head`: cada texto entra 0,3–0,5 s después de su palabra,
  densidad alta solo al principio y sin animación nueva en los últimos ~20 s salvo la llamada.

## Plantilla
`plantilla/` es un proyecto de Hyperframes con todos los elementos ya montados y sus textos
como variables, sobre 10 s de vídeo de muestra. Para usarla: copiar la carpeta, cambiar
`assets/demo.mp4` por el vídeo cortado y editar los textos y tiempos en `index.html`.
