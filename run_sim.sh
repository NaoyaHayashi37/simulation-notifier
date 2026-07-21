#!/bin/bash
# シミュレーション本体を包み、実行時間つきで終了を通知するラッパー。
#
# 使い方:
#   1. cp .env.example .env して .env に Webhook URL を書く
#   2. .env の SLACK_WEBHOOK_URL の右辺を実際の値に
#   3. bash run_sim.sh

# .env を読み込む
set -a
[ -f .env ] && . .env
set +a

start=$(date +%s)

python main.py            # ← あなたのシミュレーション本体に置き換える
code=$?                   # 直前の終了コードを保存

elapsed=$(( $(date +%s) - start ))
python notify.py "シミュレーション" "$code" "$elapsed" "params: N=1000, seed=42"
