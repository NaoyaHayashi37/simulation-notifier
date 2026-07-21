# simulation-notifier

数日かかる長時間シミュレーションの終了を、**Slack に自動通知**するツール。

大学の共用サーバーで計算を回していると「終わったかどうか」を確認するために
何度もログインし直す必要があった。この手間を解消するために作った。

## 特徴

- ✅ 成功 / ❌ 異常終了 を色分けして通知（終了コードで判定）
- ⏱ 実行時間を自動計測して表示
- 🖥 実行ホスト名を表示（どのサーバーのジョブか分かる）
- 🔁 送信失敗時は自動リトライ
- 🔒 Webhook URL は環境変数で管理（リポジトリに秘密情報を含めない）

## セットアップ

```bash
pip install -r requirements.txt
cp .env.example .env      # .env に Slack Webhook URL を記入
```

Slack の Incoming Webhook URL は
[Slack API のアプリ設定](https://api.slack.com/apps) から発行する。

## 使い方

`run_sim.sh` の `python main.py` を自分のシミュレーション本体に置き換えて実行する。

```bash
bash run_sim.sh
```

開始時刻を記録 → 本体を実行 → 経過時間つきで成功/失敗を Slack に通知する。

通知だけ単体で試す場合:

```bash
python notify.py "テスト" 0 3600 "params: N=1000"
```

## 構成

```
simulation-notifier/
├── notify.py        通知本体（Slack へ POST）
├── run_sim.sh       シミュを包んで実行時間を計測するラッパー
├── requirements.txt 依存パッケージ
├── .env.example     設定の見本（実際の .env は Git 管理外）
└── README.md
```
