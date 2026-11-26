#!/bin/bash
# Regenera las escenas y vuelve a aplicar la corrección de color cálida.
set -e
cd "$(dirname "$0")"
python3 build.py words.json
node ~/.claude/skills/hyperframes/scripts/plugin-cli.mjs media-treatment --selector "#footage" \
  --grading '{"adjust":{"exposure":0.03,"contrast":0.1,"temperature":0.06,"saturation":0.05,"blacks":-0.03}}' --apply --json >/dev/null
