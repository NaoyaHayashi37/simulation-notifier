"""シミュレーション終了を Slack に通知するスクリプト。

使い方:
    python notify.py "タイトル" <exit_code> [elapsed_sec] [detail]

例:
    python notify.py "シミュレーション" 0 3600 "params: N=1000, seed=42"
"""
import sys
import os
import time
import socket

import requests


def get_webhook_url() -> str:
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        sys.exit("環境変数 SLACK_WEBHOOK_URL が設定されていません")
    return url


def notify(title: str, exit_code: int, elapsed_sec: float | None = None, detail: str = "") -> None:
    ok = exit_code == 0
    color = "#36a64f" if ok else "#d00000"  # 緑 / 赤
    emoji = "✅" if ok else "❌"

    fields = [
        {"title": "ステータス", "value": "成功" if ok else f"異常終了 (code {exit_code})", "short": True},
        {"title": "ホスト", "value": socket.gethostname(), "short": True},
    ]
    if elapsed_sec is not None:
        h, rem = divmod(int(elapsed_sec), 3600)
        m, s = divmod(rem, 60)
        fields.append({"title": "実行時間", "value": f"{h}時間{m}分{s}秒", "short": True})
    if detail:
        fields.append({"title": "詳細", "value": detail, "short": False})

    payload = {
        "attachments": [
            {
                "color": color,
                "title": f"{emoji} {title}",
                "fields": fields,
                "footer": "simulation-notifier",
                "ts": int(time.time()),
            }
        ]
    }

    url = get_webhook_url()
    for attempt in range(3):  # 失敗時は最大3回リトライ
        try:
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(2 ** attempt)  # 1s, 2s, 4s と待って再試行
    print("通知の送信に失敗しました", file=sys.stderr)


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "シミュレーション終了"
    exit_code = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    elapsed = float(sys.argv[3]) if len(sys.argv) > 3 else None
    detail = sys.argv[4] if len(sys.argv) > 4 else ""
    notify(title, exit_code, elapsed, detail)
