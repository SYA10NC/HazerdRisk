# HazerdRisk

有人運転（手動運転）車両で、**CANバスから取得できるデータのみ**を用いて事故を未然に防ぐ（危険の予兆検知・警告）ための調査リポジトリ。

論文・記事・公式発表・自動運転の実技術といったオープンソース情報を収集し、Markdown で蓄積する。調査は Claude Code のクラウドルーチンで毎日自動実行され、このリポジトリに追記される。

## 構成

- `research/` — テーマ別の調査レポート（深掘り）
  - [research/README.md](research/README.md) — 索引とテーマ横断の要点
  - [research/12_integrated_architecture.md](research/12_integrated_architecture.md) — 統合参照アーキテクチャ（現時点の結論）
  - [research/BACKLOG.md](research/BACKLOG.md) — 未調査テーマのキュー（自動ループが上から消化する）
  - [research/LOG.md](research/LOG.md) — 自動ループの実行ログ
- `news/` — 月別の最新動向（新着論文・公式発表・自動運転技術ニュース）
- `docs/LOOP.md` — 自動調査ループの手順書（クラウドエージェントが毎回読む）
- `CLAUDE.md` — エージェント向けの記述ルール

## 自動調査ループ

- 実行: Claude Code クラウドルーチン（毎日 06:00 JST）
- 1回の実行でやること
  1. `research/BACKLOG.md` の先頭テーマを1件深掘りし、`research/NN_<slug>.md` を追加する
  2. 直近の新着情報を `news/YYYY-MM.md` に追記する
  3. 索引・バックログ・ログを更新する
  4. main に commit・push する
- 手順の詳細は [docs/LOOP.md](docs/LOOP.md) を参照
- テーマを追加したいときは、`research/BACKLOG.md` の「未着手」に1行足せばよい。上にあるものほど先に処理される

## 記述ルール（要約）

- すべてのソースに URL を付け、実在を確認したものだけを載せる
- 事実（ソースの記載）と推察を分け、推察には「【推察】」を付ける
- 原文の長文転載はしない
