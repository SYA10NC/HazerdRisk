# 22. 生存分析・ハザードモデルの運転データ応用（time-to-event）

- 調査日: 2026-11-09
- 論点: B-09。運転データ（車両信号・テレマティクス・NDS）に生存分析・ハザードモデル（Cox、DeepSurv、DeepHit、離散時間ハザード）を適用した研究を集め、秒単位の予兆検知に使えるかを評価する
- 既存調査との関係: 09 §7-3（「見つからなかった」）と 08 §3.7（月単位の統計モデル）を前提に、その先を調べた。05 §3.4・14（CAN系予測は0.5〜1.5秒止まり）の再調査はしていない
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）27件／既出の再掲 1件（[S28]）。WebFetch は arxiv.org・pmc/ncbi・jstage・cir.nii 等で名前解決に失敗（ISSUES I-01 継続）し、本文を読めたものは無い。以下の要点はすべて検索結果の抜粋に基づく

## 2. エグゼクティブサマリー

- 運転データに生存分析を使った研究は、時間分解能で3群に分かれる。(a) 日〜年：初回事故までの時間（Cox・Weibull）、(b) 秒〜分：映像・位置入力のニューラルハザード、(c) 秒〜分：車線変更・テイクオーバー時間の統計解析
- CANのみの入力で、深層生存モデル（DeepSurv・DeepHit・離散時間NN）を事故予兆に適用した査読研究は見つからなかった（09 §7-3 の結論は維持）
- 秒スケールのニューラルハザードは NTT 系（Toda ら 2019、Takimoto ら）の映像＋位置入力のみ。入力が映像のため推論時CANのみの前提には合わない
- ドライバー単位の研究では、主な共変量は走行量（曝露）・夜間率・速度違反率・属性で、曝露量の補正が結果を大きく左右する（[S1][S2]）
- 手法面では、離散時間ハザード（Nnet-survival 型）は損失が個体ごとに独立に計算でき、ミニバッチ・打ち切りと相性が良いとされる。警告用途の第一候補とみなせる【推察】
- 校正を見るには C-index では足りず、IPCW Brier score と校正曲線が要る。警告閾値に確率を使う本構成では必須【推察】

## 3. 主要知見

凡例: 確認は全て「抜粋のみ」。時間分解能・CAN可否を明記する。

### 3.1 ドライバー単位（日〜年）

- [S1] Ayuso, Guillén, Pérez-Marín（Univ. Barcelona）, "Using GPS data to analyze the distance traveled to the first accident at fault in pay-as-you-drive insurance", Transportation Research Part C 68, 2016, 論文。https://recercat.cat/handle/2445/106566
  - 事実: 保険会社のGPSデータで、初回の過失事故までの走行距離を Weibull 回帰で推定。性別は日平均走行距離を入れると有意でなくなる
  - 分解能: 契約期間・日。時間軸は距離。入力: GPS 由来の走行パターン
  - CAN可否【推察】: 距離・日平均距離は車速積算で作れる。位置・道路種別はCAN単独では作れない
- [S2] 同グループ, "Telematics and Gender Discrimination…", Risks 4(2), 2016, 論文。https://mdpi.com/2227-9091/4/2/10（抜粋の対応は確度中）
  - 事実: 生存データ回帰で初回過失事故までの時間を推定。性差の多くは運転量の差で説明できると結論
  - 示唆【推察】: ドライバー単位ハザードでは曝露補正が必須
- [S3] Oralhan & Göktolga, Iranian J. Public Health 47(8), 2018, 論文。https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6123587/
  - 事実: 免許取得から初回事故までを Cox 回帰と生命表で分析。Kayseri の2008〜2012年の死傷事故11,671件。免許取得後の死傷事故の割合は5年30.3%、10年50.1%、25年91.7%
  - 分解能: 年。走行データなし。CAN不可
- [S4] SHRP2 系 NDS の初回事故まで Cox の検索ヒット（題名・著者・年は未特定）。https://par.nsf.gov/biblio/10205458-near-crash-characteristics-among-risky-drivers-using-shrp2-naturalistic-driving-study
  - 事実: 抜粋では、854人で初回事故までに Cox を適用し sensation-seeking 等のHRを報告とあるが、同一性は未確認。書誌の特定が必要
- [S5] 30歳未満の PAYD 契約者（約16,000人）を GPS 追跡し初回事故までを分析した研究（題名・著者・年は未特定）。https://www.pubmed.gov/25218977/
  - 事実: 夜間運転と制限速度違反の割合が高いほど初回事故までが短い（抜粋）
  - CAN可否【推察】: 速度・時刻は可。速度違反の判定は制限速度が要り、CAN単独では不可
- [S6] 韓国の初心運転者の初回違反までの Cox 研究（題名・著者未確認、2013年頃と推定）。https://koreascience.or.kr/article/JAKO201332479509850.pdf
  - 事実: 事故関与経験がある運転者は違反までの期間が短い傾向（抜粋）。月〜年。CAN不可

### 3.2 秒〜分単位の事象までの時間

- [S7] Eggert & Puphal（Honda Research Institute Europe）, "Continuous Risk Measures for Driving Support", 2018（arXiv 2023）。https://arxiv.org/abs/2303.08007
  - 事実: TTCE を一般化する「生存」型リスク指標を含む3指標を比較。抜粋では、事故検出が早く、ニアクラッシュ・非クラッシュでの偽陽性が少ないと述べる。数値は未確認
  - 分解能・入力: 未確認（軌跡状態と推定）。ニューラルモデルではない
  - 示唆【推察】: 先行車距離・相対速度（レーダ由来CAN）で近い指標を作れる可能性
- [S8] Toda, Okawa, Tanaka, Takimoto, Kurashima, Yamamoto（NTT）, "Predicting Traffic Accidents with Event Recorder Data", PredictGIS 2019, DOI 10.1145/3356995.3364535。https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi...........d90c130720cc73c91478f4f6c84d616a（図書館カタログ。入力は映像と推定、未確認）
  - 事実: 事故発生時刻を生存分析で予測し、基準手法より高精度と報告（抜粋）
- [S9] ドライブレコーダデータを用いた生存分析に基づく交通事故発生予測（CiNii 掲載。題名・著者・年は未確認）。https://cir.nii.ac.jp/crid/1050850722269275648
  - 事実: ハザード関数を前方映像用と自車位置用の2つのNNで表し、対数尤度を損失として学習。事故時刻をより正確に予測と報告（数値は未確認）。[S8] と同系統の研究と推察される
  - 示唆【推察】: 映像側をCAN時系列エンコーダに置き換える、または映像を学習時のみ補助に使う構成が候補
- [S28]（既出 20 S8）IPSJ 掲載の同系統研究（畳み込み再帰NN＋位置、負の対数尤度）。https://ipsj.ixsq.nii.ac.jp/records/209071/export/bibtex
- [S10] Lei & Ozbay（NYU C2SMART）, "Naturalistic Driving Data Analytics: Safety Evaluation With Multi-state Survival Models", IEEE ITSC。https://c2smarter.engineering.nyu.edu/wp-content/uploads/2023/10/IEEE_ITSC_YiyuanLei.pdf
  - 事実: safe／risky／near-crash の状態遷移を多状態生存モデルで扱い、悪化と回復を競合イベントとする（抜粋）。秒〜分
  - 示唆【推察】: L2〜L3 のリスク状態遷移の定式化の参考
- [S11] "Survival analysis of the unsafe behaviors leading to urban expressway crashes"（著者・年未確認）。https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9417457/
  - 事実: 事故映像から不安全行動を抽出し、生存時間解析で事故継続時間への影響を調べた（抜粋）。入力は映像由来
- [S12] Jokhio ら（Chalmers）, "Analysis of Time-to-Lane-Change-Initiation Using Realistic Driving Data", IEEE T-ITS 25(5), 2024。https://research.chalmers.se/en/publication/538666
  - 事実: ウインカー作動から車線変更開始までを事象時間として Kaplan-Meier と混合効果 Cox で分析。自車速度・前後車の有無等が有意（抜粋）。事故予兆ではない
  - 示唆【推察】: ウインカー作動はCANで観測できる時刻原点になる
- [S13] Li ら, lane-changing duration survival analysis, arXiv 2021（HighD）。https://arxiv.org/pdf/2108.05710 — 車線変更の所要時間の AFT 解析（抜粋）。軌跡データ。警告用途ではない
- [S14] 車線変更所要時間の Cox／ランダム生存森林比較、Applied Sciences 14(20):9317, 2024（著者未確認）。https://mdpi.com/2076-3417/14/20/9317 — 軌跡データ。警告用途ではない
- [S15] 深層生存モデルによるテイクオーバー時間の研究（VR、304回、SHAP）, arXiv 2402.16046。https://arxiv.org/abs/2402.16046 — シミュレータ。自動運転のテイクオーバー応答で事故予兆ではない（抜粋）
- [S16] テイクオーバー時間と事故リスクの AFT 研究（AAP 2025、Monash 記録。同一論文かは未確認）。https://research.monash.edu/en/publications/identifying-factors-affecting-driver-takeover-time-and-crash-risk/ — シミュレータ
- [S17] 前方衝突警報の注意ネットワーク, arXiv 2511.19952。https://arxiv.org/pdf/2511.19952 — ハザード型ではない。抜粋に F1 0.912、誤警報率8.2%、平均警報リードタイム2.8秒とあり、数値の参照点として記す（条件・入力は未確認）

### 3.3 他分野・手法（CANへの移植観点）

- [S18] Lee ら, DeepHit, AAAI 2018。https://ojs.aaai.org/index.php/AAAI/article/view/11842 — 生存時間分布を直接学習し、競合リスクを扱う（抜粋）。損失の詳細は未確認
- [S19] Lee ら, Dynamic-DeepHit, IEEE TBME 2020。https://read.qxmd.com/read/30951460/dynamic-deephit-a-deep-learning-approach-for-dynamic-survival-analysis-with-competing-risks-based-on-longitudinal-data — 縦断データで観測ごとに予測を更新。検証は年次の嚢胞性線維症レジストリ（5,883人）で、CANの高頻度とは桁が違う
- [S20] Katzman ら, DeepSurv, BMC Med Res Methodol 2018。https://arxiv.org/abs/1606.00931 — Cox の線形リスクをNNに置換（抜粋）
- [S21] Gensheimer & Narasimhan, Nnet-survival, PeerJ 2019。https://peerj.com/articles/6257 — 離散時間生存モデル。個体ごとに独立な負の対数尤度でミニバッチ化しやすい（抜粋）
- [S22] 保全分野の打ち切り付きRUL（arXiv 2405.01614, 2024）。https://arxiv.org/abs/2405.01614 — 打ち切りを無視すると故障リスクを過大評価と述べ、XJTU-SY で Random Survival Forest が NN 系を MAE で上回ったと報告（抜粋）
- [S23] LSTM／Transformer による打ち切り考慮RUL（PHM Society, 2024）。https://papers.phmsociety.org/index.php/phme/article/view/3974 — 性能は未確認
- [S24] バッテリRULの生存分析（arXiv 2503.13558）。https://arxiv.org/pdf/2503.13558v4 — 電圧時系列を time-to-failure 形式に変換し Cox と DeepHit・MTLR を比較（抜粋）
- [S25] 辻谷ら, RNNによるイベントヒストリー解析, 応用統計学 47(2-3), 2018（日本語）。https://www.jstage.jst.go.jp/article/jappstat/47/2-3/47_71/_article/-char/ja — 時変共変量の部分ロジスティック型RNN。医療データ
- [S26] scikit-survival 評価ガイド。https://scikit-survival.readthedocs.io/en/latest/user_guide/evaluating-survival-models.html — IPCW Brier score・時間依存AUC。C-index は順位のみ（抜粋）
- [S27] "An Introduction to Deep Survival Analysis Models for Predicting Time-to-Event Outcomes", arXiv 2410.01086。https://arxiv.org/pdf/2410.01086 — 概説（抜粋）

## 4. 統合アーキテクチャ（12）への反映点【推察】

- L3（R4 の数秒先予測）: 「Tステップ以内の事故確率」を離散時間ハザードの累積として出す設計案を追加候補とする。損失は区間ごとの尤度で、事故なし走行は打ち切りとして学習に入る。ベースラインに木ベース生存モデル（[S22] より）と、Cox／ロジスティック回帰を置く
- L3→L4: 確率出力を警告閾値に使うので、校正（IPCW Brier、校正曲線）を必須にする
- L6: 長期（日〜月）のドライバー単位ハザードは、走行距離で曝露補正した Cox 型を、車両側の集計特徴（急操作率・ADAS警報率など）で構築する案。外部の履歴（事故・違反歴）はCANに無い
- ラベル設計: 「時間ゼロ」は各窓の末尾（ランドマーク型）が警告用途に合う。評価は走行単位で分割する
- 映像を学習時のみ使う構成（[S9][S11]）は 20 の蒸留案と接続する

## 5. 課題・ギャップ

- 全27件が抜粋のみ。時間分解能・入力・偽警報率は未確認が多い
- CANのみ×深層生存×事故予兆は未発見。検索クエリ（運転CAN×生存分析、MTLR、校正）の再確認が要る
- 日本語は NTT 系ドラレコ研究（映像入力）と医療RNN [S25] のみで、運転データ×ハザードの日本語研究は未発見
- [S4][S5][S6][S9][S14] は題名・著者・年が未特定
- 事故の稀少性による打ち切り過多と校正の分散は未検討

## 6. 次のアクション提案

1. 公開データ（comma2k19 等、事故ラベルなし）では検証できないため、SHRP2 型の crash/near-crash ラベル付きデータの入手条件を B-13 とあわせて確認する
2. 離散時間ハザード（0.5秒刻み）と、ロジスティック回帰・木ベース生存の比較実験を設計する（I-11 と接続）
3. I-01 解消後に [S8][S9][S28] の本文で、入力・評価・時間分解能を確認する
4. 校正・時間依存指標を L6 の評価仕様に追加する
5. 曝露補正付きドライバー単位 Cox の特徴量表を、可観測信号で作る

## 7. 参考文献リスト

上記 [S1]〜[S28] の URL。いずれも WebSearch で実在を確認したもの（本文は未読）。
