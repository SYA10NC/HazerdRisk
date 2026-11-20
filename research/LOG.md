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
- 2026-11-08 | 21_cross_vehicle_adaptation_for_can.md | ソース31件（0/31/0＝新規本文/新規抜粋/既出） | news 4件 | B-08。事故予兆のCANのみ車種間転移は未発見。IDS中心。ゼロショット困難との2026プレプリント、物理量化・信号同定・時系列UDAを整理。全て抜粋のみ(I-20)
- 2026-11-09 | 22_survival_hazard_models_for_driving.md | ソース28件（0/27/1＝新規本文/新規抜粋/既出） | news 3件 | B-09。CANのみ×深層生存×事故予兆は未発見。秒スケールはNTT系の映像入力のみ。日〜年はCox/Weibull。全て抜粋のみ(I-22)
- 2026-11-10 | 23_older_and_novice_drivers_can_detection.md | ソース36件（0/34/2＝新規本文/新規抜粋/既出） | news 2件 | B-10。CANのみで年齢層・熟練度を推定した研究は未発見。警報データでの高齢者判別・MCI判別・操作量熟練度分類が近い例。全て抜粋のみ(I-24)
- 2026-11-11 | 24_commercial_vehicle_j1939_and_fleet_safety.md | ソース29件（0/29/0＝新規本文/新規抜粋/既出） | news 3件 | B-11。AEBS1/2 の PGN は未確定（EBC1/CCVS1/EBC5・AEBS2 SPN のみ）。国内デジタコ閾値は非公開のまま。全て抜粋のみ(I-01)
- 2026-11-12 | 25_aftermarket_devices_and_unr155_r156.md | ソース28件（0/26/2＝新規本文/新規抜粋/既出） | news 3件 | B-12。後付け機器を直接扱う R155/保安基準の条項は未発見。部品承認は構想段階。全て抜粋のみ(I-01)
- 2026-11-13 | 26_japan_near_miss_db_and_dashcam_data.md | ソース36件（0/35/1＝新規本文/新規抜粋/既出） | news 3件 | B-13。公開DLの国内ヒヤリハットDBは未確認。SMRC・ITARDAとも共同研究/審査型。誤検出約70%の記述あり。全て抜粋のみ(I-01)。B-20 は I-01 のため見送り
- 2026-11-14 | 27_japanese_driving_foundation_and_distillation.md | ソース16件（0/16/0＝新規本文/新規抜粋/既出） | news 5件 | B-22。CANのみの国内資料は未発見。国内各社は映像中心。全て抜粋のみ(I-01)。I-01 のため B-14/15/16/19/20/26 は見送り
- 2026-11-15 | 28_domain_generalization_and_few_shot_adaptation.md | ソース29件（0/29/0＝新規本文/新規抜粋/既出） | news 4件 | B-23。CANのみ×未見車種DG/LODOの事故予兆研究は未発見。HAROOD等のLODO評価、MetaFollower等の少数ショット適応を整理。全て抜粋のみ(I-01)。I-01 のため B-14/15/16/19/20/26 は見送り
- 2026-11-16 | 29_hazard_calibration_and_alert_threshold_design.md | ソース24件（0/24/0＝新規本文/新規抜粋/既出） | news 2件 | B-24。ハザード確率→警報率上限つき閾値の直接研究は未発見。校正は事後補正（Platt/CSD）＋校正曲線、閾値は固定警報率・コスト比・LTT。全て抜粋のみ(I-01)。B-14/15/16/19/20/26 は I-01 のため見送り
- 2026-11-17 | 30_driver_specific_adaptation_evaluation_design.md | ソース20件（0/14/6＝新規本文/新規抜粋/既出再掲） | news 0件 | B-28。CANのみ×同一車両×多人数×事故予兆の公開評価は未発見。DriveDNA の少数ショット利得は約+0.8%と小さい。100-DrivingStyle（100人）が人数面で最有力。全て抜粋のみ(I-01)。B-14/15/16/19/20/26 は I-01 のため見送り
- 2026-11-18 | 31_health_incapacitation_can_precursors.md | ソース21件（0/21/0＝新規本文/新規抜粋/既出） | news 0件 | B-25。CANのみの操作途絶検知の定量評価は未発見。無入力→警告→停止が共通構造、閾値は未確認。全て抜粋のみ(I-01)。B-14/15/16/19/20/26 は I-01 のため見送り
- 2026-11-19 | 32_japanese_brake_intent_and_deceleration_prediction.md | ソース19件（0/18/1＝新規本文/新規抜粋/既出） | news 2件 | B-27。CANのみで1.5秒超のブレーキ意図予測の日本語文献は未発見。ペダル動特性は数百ms級、介入が早すぎると再加速（約1/4）。全て抜粋のみ(I-01)。B-14/15/16/19/20/26 は I-01 のため見送り
- 2026-11-20 | 33_japanese_alarm_fatigue_and_threshold_literature.md | ソース28件（0/27/1＝新規本文/新規抜粋/既出） | news 2件 | B-29。日本語で感度・PPV・誤報率を直接報告した文献は未発見。医療は内訳比率、プラントは EEMUA 191 系、車載は国内不要作動資料。全て抜粋のみ(I-01)。B-14/15/16/19/20/26 は I-01 のため見送り
