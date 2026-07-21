#!/bin/bash

set -a
[ -f .env ] && . .env
set +a

start=$(date +%s)

python main.py            # ← あなたのシミュレーション本体に置き換える
code=$?

elapsed=$(( $(date +%s) - start ))
python notify.py "シミュレーション" "$code" "$elapsed" "params: N=1000, seed=42"
