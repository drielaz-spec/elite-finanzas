# requisitos-hipoteca — DESIGN

## Origem
- Bruto: `01-bruto/IMG_7134.MOV` (1:07, 1080×1920 após rotação, 60 fps, áudio AAC).
- Corte (`assets/source.mp4`): 34,87 s, 1080×1920, 30 fps. Removidos o silêncio de 21→40 s
  e o de 48→53 s; pausas internas > 0,35 s encurtadas para ~0,18 s.
- Transcrição: Whisper large-v3 local, espanhol, tempo por palavra (`assets/transcript.json`).

## Saída
- 9:16, 1080×1920, 30 fps, Instagram Reels.
- Margens: topo 220 px · laterais 80 px · base 420 px.

## Visual (igual a "5 motivos" e "estudio hipotecario")
- Cards no topo (y ≥ 285), Montserrat 800 branco + verde menta #3DDC84, Caveat manuscrito verde.
- Legenda amarela #FFE600 palavra por palavra, Montserrat 900 com contorno preto, na altura
  do peito (faixa y 1100–1250), uma palavra por vez.
- Cor quente (exposição +0,03, contraste +0,10, temperatura +0,06, saturação +0,05).

## Não pode ser coberto
- Rosto e boca (rosto entre y ~420 e ~1050).
- Faixa da legenda (y 1100–1250) e base de 420 px.

## Curva de intensidade (35 s)
| Faixa | Trecho | Densidade |
|---|---|---|
| Abertura | 0 – 10,4 s (gancho + situações) | alta: card novo a cada ~1–2 s |
| Corpo | 10,4 – 26 s (oferta + 3 requisitos) | média: lista que acumula (exceção legítima: lista) |
| Fecho | 26 s – fim (chamada) | sem motion novo; só uma chamada pequena e estática |

## Câmera
- Dois punch-ins rápidos (0,4 s, 100→104 %): na entrada do título (0 s) e na virada
  "Tres requisitos" (16,2 s). Entre eles, plano parado. Sem zoom lento contínuo.

## Áudio
- Voz: só ganho + limitador para chegar a −14 LUFS / −1,5 dBTP (origem: −25,7 LUFS).
- Efeitos: só 2 sopros curtos (whoosh-short), na entrada do título e na virada dos requisitos.
  Nenhum som por card, nenhum impacto seco.
- Sem trilha (não pedida).
