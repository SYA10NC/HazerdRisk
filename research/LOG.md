# 調査ログ

書式: `- YYYY-MM-DD | ファイル | ソース件数 | news件数 | メモ`

- 2026-11-01 | 01〜06 | 約190件 | - | 第1弾。ローカルの Claude Code セッションで、サブエージェント6体で並列調査
- 2026-11-02 | 07〜12 | 163件 | - | 第2弾。未然防止アーキテクチャを5論点に分解して調査し、12で統合（【訂正 2026-11-01】日付は 2026-11-01 が正しい）
- 2026-11-01 | 13_industry_safety_architectures.md | ソース28件（本文確認は一部、多くは検索抜粋） | news 4件 | WebFetchが多くのホストで不可。OSS3者の層構成を比較
- 2026-11-01 | ISSUES.md・COVERAGE.md・SOURCES.md 新設 | - | - | 調査の棚卸し。問題点を I-01〜I-11 にタスク化、BACKLOG をゴールプロンプト形式に改め、重複チェック手順（scripts/sources_index.py）を LOOP に追加。既出URL 424件、ファイル間重複 29件
- 2026-11-01 | 14_can_only_multisecond_prediction.md | ソース38件（0/38/0＝新規本文/新規抜粋/既出。全て検索抜粋） | news 3件 | B-01。CANのみ・実車・2秒以上先・偽警報率つきの研究は未発見。CAN系は0.5〜1.5秒、横は約1秒（誤警報約3.1%）止まり
- 2026-11-02 | 15_adas_false_alarm_field_data.md | ソース34件（0/31/3＝新規本文/新規抜粋/既出） | news 4件 | B-02。誤警報率の公的実測は未発見。無効化率はLDWが最大。WebFetch不可(I-01)で本文確認0
- 2026-11-03 | 16_lead_vehicle_signals_by_vehicle.md | ソース30件（24/6/0＝新規本文/新規抜粋/既出） | news 2件 | B-03。距離・相対速度の物理量は Toyota/GM/Mazda/Ford/Hyundai/Honda Nidec。OBD 可視性の車種別一次資料は未発見。J1939 ACC1=PGN 65135
- 2026-11-04 | 17_shrp2_triggers_and_can_reproduction.md | ソース24件（0/21/3＝新規本文/新規抜粋/既出再掲） | news 4件 | B-04。12行のトリガ表は一次未確認。CAN再現の注意5点（微分ノイズ・車輪スリップ・取付軸ずれ・記録周期・段差誤検知）
- 2026-11-05 | 18_pedal_misapplication_low_speed.md | ソース24件（0/24/0＝新規本文/新規抜粋/既出） | news 2件 | B-05。R175 ACPE と国交省2026-01改正を追加。判定入力はアクセル開度・操作速度・車速・シフトに収束。閾値の数値は原文未確認
- 2026-11-06 | 19_intersection_precursors_can_only.md | ソース18件（0/18/0＝新規本文/新規抜粋/既出） | news 4件 | B-06。CANのみで交差点を判定した研究は未発見。SHRP2 衝突時速度は低め（抜粋）。全て抜粋のみ(I-17)
- 2026-11-07 | 20_world_model_and_distillation_for_can_only.md | ソース34件（0/34/0＝新規本文/新規抜粋/既出） | news 3件 | B-07。映像→CAN蒸留で運転リスクを扱う直接研究は未発見。COMODO型蒸留・予測誤差=危険度・ego動力学残差が転用候補。全て抜粋のみ(I-19)
