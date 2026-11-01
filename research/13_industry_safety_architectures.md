# 13 自動運転・ADAS企業／OSSの安全アーキテクチャ比較 — CANのみ構成への転用要素

- 調査日: 2026-11-01
- 論点: Waymo・Tesla・Mobileye・Wayve・Woven by Toyota／Toyota・Baidu Apollo・Autoware・openpilot の公開資料から、予兆検知・安全監視・フォールバックの層構成を比較し、CANのみの有人運転向け構成（12）に転用できる要素を抽出する

## 2. エグゼクティブサマリー

1. 今回の調査環境ではWebFetchが多くのホストで名前解決に失敗した。本文を読めたのはGitHub上のREADME 5件程度で、残りは検索結果の抜粋のみで確認した。各ソースに【本文】【抜粋】を付した。数値は版依存・自己申告が多く、設計根拠には一次資料での再確認が要る
2. OSS勢（Apollo・Autoware・openpilot）は、「入力監視 → 健全性の集約 → 判断 → 縮退行動 → 最終ゲート」という共通の層構成を公開している。これは12のL1（信号健全性）〜L5（出力）と対応づけられる
3. 3者とも最終縮退は停止・制御遮断である。警告のみの本プロジェクトでは、相当物は「警告の縮退と、警告不能であることの通知」である【推察】
4. Apollo Guardianは、状態メッセージの途絶（2.5秒）などで出力を遮断する単純なゲートである。CAN欠落時の警告抑制・縮退通知に同型の構造を置ける【推察】
5. Autowareは「可用性（何が使えるか）を入力にMRMを選ぶ」設計と、診断グラフ（DAG）・ラッチ・一方向エスカレートを持つ。入力健全性→検知器有効性→警告可否のDAG化と、警告のチャタリング防止に転用できる【推察】
6. openpilot/pandaは「デフォルト無音・許可は運転者操作で即解除」という送信経路の最終ゲートである。本プロジェクトでは受信専用（listen-only）の担保に相当する【推察】
7. MobileyeのRSS縦方向式は、先行車距離・相対速度がCANにあれば、学習モデルと独立したルールベース安全層として計算できる【推察】。式は本文未確認
8. Tesla Safety ScoreはFCW頻度・急制動などイベント率をスコア化する。これらはCANで再現可能で、L3のドライバーリスクスコアの設計参考になる【推察】
9. WaymoのSafety Caseは危険を「アーキテクチャ／挙動／運用中」に分ける。運用中監視は、CAN信号の分布ドリフト・欠損検知（L1・L6）に対応づけられる【推察】
10. 企業側（Waymo・Tesla・Wayve）の効果数値は自己申告・二次報道であり、本プロジェクトの根拠には使えない

## 3. 主要知見

凡例: 【本文】=本文を読んだ、【抜粋】=検索結果の要約のみ、【推察】=本稿の推論。

### 3.1 オープンソース（Apollo・Autoware・openpilot）

**S1. Apollo Guardian** — Baidu/Apollo、master、公式README【本文】 https://github.com/ApolloAuto/apollo/tree/master/modules/guardian
- 入力はChassis・ControlCommand・SystemStatus、出力はGuardianCommand。異常時に制御出力を遮断してブレーキを作動させる。10ms周期で、制御指令に最大10msの遅延が入る
- トリガは、ステータス途絶が2.5秒超、またはステータスに safety_mode_trigger_time がある場合
- 示唆: 【推察】L5の前段に、入力ストリーム途絶を検知して警告を抑制／縮退通知するゲートを置ける。ただし本プロジェクトの出力は警告であり制動ではない

**S2. Apollo Monitor** — 同、Apollo 5.5時点、README【本文】 https://github.com/ApolloAuto/apollo/tree/master/modules/monitor
- ハードウェア（CANカード等）とソフトウェア（Process・Topic）を監視し、Summary monitorがOK/WARN/ERROR/FATALに集約。データの完全性・周期・CPU/メモリ・遅延を見る。CANチェックの詳細はREADMEに無い
- 示唆: 【推察】L1で信号ごとの周期・欠損・値域・カウンタ/チェックサムを監視し、4段階の健全性へ集約する構成の参考になる

**S3. Apollo Guardian/Monitor ソース解説** — 個人ブロガー、年不明、非公式、中国語【抜粋】 https://blog.csdn.net/qq_32378713/article/details/128126473
- ERRORかFATALのモジュールが required_for_safety（既定true）ならsafety modeに入り、約10秒回復しなければ緊急停止を要求する、と要約されている。版差あり
- 示唆: 【推察】「警告→強警告」を継続時間でエスカレートさせる設計の参考。数値は公式コードで再確認が必要

**S4. Autoware MRM handler** — Autoware Foundation、main、README【本文・一部のみ】 https://github.com/autowarefoundation/autoware_universe/tree/main/system/autoware_mrm_handler
- 動作モードの可用性に基づきMRM（緊急停止・快適停止・路肩退避）を選択する。状態遷移・優先度の詳細はREADMEに無い
- 示唆: 【推察】検知器・入力の「可用性ベクトル」を明示し、利用不能時に警告ロジックを縮退させる

**S5. Autoware Fail-safe AD API** — 同、公式設計文書【抜粋】 https://docs.autoware.org/main/design/autoware-architecture-v1/interfaces/ad-api/features/fail-safe/
- 通常指令と異常時指令の切替ゲート。既定MRMは COMFORTABLE_STOP・EMERGENCY_STOP・PULL_OVER。快適停止から緊急停止へは遷移するが逆は戻らない
- 示唆: 【推察】警告段階を一方向のみエスカレートさせ、ヒステリシス／ラッチでチャタリングを防ぐ

**S6. Autoware System diagnostic graph** — 同、パッケージ文書【抜粋】 https://autowarefoundation.github.io/autoware.universe_planning/main/system/system_diagnostic_graph
- 診断メッセージを機能単位を含むDAGに集約。一部レベルはラッチされ、リセットAPIで復帰する
- 示唆: 【推察】入力健全性→特徴量有効性→検知器有効性→警告可否をDAGで宣言的に表現できる

**S7. Autoware.Auto 旧監視設計（Error Monitor/Emergency Handler 提案）** — GitLab issue、年不明【抜粋】 https://gitlab.com/autowarefoundation/autoware.auto/AutowareAuto/-/issues/1233
- State Monitor・Error Monitor・Emergency Handlerの構成案。現行と異なる可能性がある旧設計
- 示唆: S6の前身。監視→能力判定→ハンドラの系譜確認用

**S8. openpilot SAFETY.md** — comma.ai、master【本文】 https://github.com/commaai/openpilot/blob/master/docs/SAFETY.md
- ACC+ALCのレベル2支援。運転者がいつでもオーバーライド可能。ISO 26262のガイドラインに沿い、MISRA C:2012、SIL/HIL/実車試験、ハザード分析とFMEAを実施。ドライバーモニタは注意散漫を検知して警告する
- 示唆: 【推察】警告のみの本構成でも、HARA/FMEAと「誤警告が運転者に与える影響」の分析は参考になる。映像DMSは推論時に使えないため、操舵・ペダル・ウインカー由来の代理推定が要る

**S9. opendbc / panda 安全モデル** — comma.ai、master、README【本文】＋ブログ【抜粋】 https://github.com/commaai/opendbc ／ https://blog.comma.ai/understanding-the-openpilot-safety-model
- 起動時はSAFETY_SILENTでCANバスが無音。一部モードは controls_allowed で送信可能メッセージを制限し、ブレーキ操作で即解除する（ブログ要約）。cppcheck＋MISRA、車種ごとの単体テストで100%行カバレッジ
- 示唆: 【推察】CANは受信専用・デフォルト無音とし、読み取り経路が書き込みを起こさないことをHW/SWで担保する。車種別DBCの検証ゲートにも応用できる

### 3.2 Waymo・Mobileye・Wayve

**S10. Building a Credible Case for Safety** — Waymo、2023、論文【抜粋】 https://arxiv.org/pdf/2306.01917
- 「不合理なリスクの不在」を層で分解し、ハザードを architectural / behavioral / in-service operational に分類。評価は継続的で、新都市・新プラットフォームで再評価する
- 示唆: 【推察】3分類をCAN構成の監視設計の枠組みに使える。車種変更時の再評価はDBC差異対応に対応する

**S11. A Blueprint for AV Safety** — Waymo、2023-03、ブログ【抜粋】 https://blog.waymo.com/blog/2023/03/a-blueprint-for-av-safety-waymos — S10の紹介。追加の示唆は確認できていない

**S12. Collision Avoidance Testing of the Waymo ADS** — Waymo（Kusano ら）、論文、年はarXiv IDから2022年12月と推定（未確認）【抜粋】 https://arxiv.org/pdf/2212.08148
- 他の交通参加者の緊急・予期しない行動に対する応答をシナリオベースで評価する手法
- 示唆: 【推察】ヒヤリハット評価シナリオ設計の参考

**S13. Collision avoidance effectiveness… human driver behavior reference model** — Waymo/Scanlon ら、2026、SAE 2026-01-0520【抜粋】 https://saemobilus.sae.org/papers/collision-avoidance-effectiveness-automated-driving-system-using-a-human-driver-behavior-reference-model-reconstructed-fatal-collisions-2026-01-0520
- 16件の衝突シナリオのうち、Waymo Driverは12件（75%）、NIEONモデルは10件（62.5%）を回避したとの要約（Waymo研究ページの抜粋）
- 示唆: 【推察】「注意深い人間」の参照モデルとの比較は、CAN警告の効果評価の基準線設計に使える

**S14. Waymo Safety Impact Hub** — Waymo、2025〜26、自己申告データ【抜粋】 https://waymo.com/safety/impact
- 走行距離あたり事故率をNHTSA SGO報告に基づき人間基準と比較。数値の日付が不明で、設計根拠には使えない
- 示唆: 【推察】走行距離あたり率を効果指標に使う設計の参考に留める

**S15. Responsibility-Sensitive Safety** — Mobileye、2017〜、公式解説【抜粋】 https://www.mobileye.com/responsibility-sensitive-safety/
- 縦方向の最小安全距離d_minは、前方車の急ブレーキ時に停止できる距離で、速度・応答時間・制動能力に依存する。距離がd_minを下回ると制動して回復する。式の具体形は本文未確認
- 示唆: 【推察】CANの前方車距離・相対速度からd_minを計算し、学習モデルと独立したルールベース安全層にできる（12のR1「縦RSS」の裏付け）。パラメータは車両・運転者ごとに調整が必要

**S16. On a Formal Model of Safe and Scalable Self-driving Cars** — Shalev-Shwartz ら、論文【抜粋】 https://pdf.arxiv.org/pdf/1911.01207 — 検索で実在確認。S15と同系統。補足資料 https://static.mobileye.com/website/corporate/rss/rss_on_nhtsa.pdf（本文未確認）

**S17. AV Safety Demands True Redundancy** — Mobileye、2020、ブログ【抜粋】 https://www.mobileye.com/blog/av-safety-demands-true-redundancy/
- カメラ系を主系、レーダ／LiDAR系を独立な冗長系とする
- 示唆: 【推察】CANのみでは独立2系統の認識は持てない。代替として「CAN上のADAS ECU警報」と「自前モデル」を独立2系統とし、不一致を監視対象にする

**S18. Mobileye AEB TÜV SÜD検査証明書** — Mobileye/TÜV SÜD、2026-10、ニュース【抜粋】 https://autonews.gasgoo.com/articles/icv/mobileye-receives-tv-sds-first-aeb-development-and-testing-certificate-2115032298189369345
- AEB開発プロセスをISO 21448（SOTIF）に照らして監査した初の証明書とされる
- 示唆: 【推察】SOTIFの観点で「検知できない条件」「誤警報」を整理する枠組みに使える

**S19. EE Times Japan RSS解説記事（日本語）** — 2020-10（URLから推定）【抜粋・見出しのみ】 https://eetimes.itmedia.co.jp/ee/articles/2010/22/news071_2.html — 本文未読のため示唆は挙げない

**S20. GAIA-1 Technical Report** — Wayve、2023-10、PDF【抜粋】 https://s24.q4cdn.com/622300748/files/doc_news/Wayve-Releases-GAIA-1-Technical-Report-to-Advance-World-Models-for-Autonomy-2023.pdf
- 動画・テキスト・行動を入力とする生成型世界モデル（9Bパラメータ、約4,700時間の英国走行データとの報道）
- 示唆: 【推察】推論時に映像を使えないため直接は転用できない。学習時のみ使う特権情報学習（BACKLOG 8）の文脈で再検討する。なおWayveの安全アーキテクチャの一次資料（公式ブログ・論文）は特定できなかった。求人票は一次情報として弱いため載せない

### 3.3 Tesla・Toyota／Woven

**S21. Tesla Safety Score Beta** — Tesla、2021〜、公式サポートページ（カナダ版）【抜粋】 https://www.tesla.com/en_CA/support/safety-score
- FCW頻度・急制動などを予測衝突頻度（PCF）モデルで組み合わせる。FCWは運転者の感度設定に関わらずMedium相当で計算。急制動は旧版で後方向0.3g超。係数・上限は版により異なり確定できない
- 示唆: 【推察】FCW・急制動・縦GはADASフラグと車速・加速度からCANで再現でき、L3/L5のスコア設計に使える。感度設定を正規化する考え方は車種間差の吸収に有用

**S22. Tesla Q1 2024 Vehicle Safety Report 解説** — Drive Tesla Canada、2024、二次報道【抜粋】 https://driveteslacanada.ca/news/tesla-q1-2024-vehicle-safety-report/
- 2018年Q3から任意公開。Autopilot使用時7.63百万マイル/件（2024Q1）と報じられる。一次資料（tesla.com）は取得失敗
- 示唆: 【推察】Autopilot使用有無で層別する考え方は、手動運転限定の評価の層別に使える

**S23. Tesla クラッシュ過少計上の可能性** — The Autopian、年不明、二次報道【抜粋】 https://www.theautopian.com/is-tesla-may-miscounting-crashes-to-make-autopilot-seem-safer-new-study-suggests-it-might-be/
- Traffic Safety Research誌の研究が過少計上の可能性を指摘したと報じる。研究本体は未確認
- 示唆: 【推察】CAN由来イベントをラベルにする場合、定義で見かけの率が変わる。ラベル定義の透明化と検知漏れ評価が要る

**S24. Toyota Guardian / Chauffeur** — TRI/Toyota、2017〜2019、プレスリリース【抜粋】 https://pressroom.toyota.com/?p=16679
- 運転者が常に権限を持ち、衝突等を予測したときのみ介入する。量産未搭載とされる。居眠り検知デモはドライバーモニタ入力に依存
- 示唆: 【推察】リスク予測→警告→限定介入の段階構成と許容エンベロープの概念をL4・L5の警告段階設計に転用する

**S25. Arene Debuts in Toyota's All-New RAV4** — Woven by Toyota、2025-05【抜粋】 https://www.woven.toyota/en/news/20250521
- AreneのSDKが新型RAV4のToyota Safety Senseソフトに使われた
- 示唆: 【推察】予兆検知モデルがADASと同じ基盤にデプロイされうる。OTAを前提に機能安全上の分離・監視が要る

**S26. Apex.AI × Woven Planet 事例** — Apex.AI、年不明、ベンダー紹介（宣伝性あり）【抜粋】 https://apex.ai/toyota-woven-planet
- Arene OSはISO 26262 ASIL D対応の安全成果物に言及
- 示唆: 【推察】予兆検知はQMレベルの助言機能として、ASIL要求の制御系と分離する

**S27. トヨタ プリクラッシュセーフティ解説（日本語）** — トヨタ自動車、2017、公式記事【抜粋】 https://global.toyota/jp/detail/18795024
- 警告（ブザー・表示）→ブレーキ補助→自動ブレーキの3段階
- 示唆: 【推察】CAN上のPCS状態フラグを段階ラベルに使い、それより早い段階の予兆スコアをL4/L5の出力に置く

**S28. 直近ニュース（Waymo×Toyota）** — TechCrunch、2026-10-30【抜粋】 https://techcrunch.com/2026/10/30/waymos-next-robotaxi-will-be-a-toyota-bz4x-destined-for-japan-and-the-uk — 本稿の設計には直接関係せず、ニュース節（news/2026-11.md）で扱う

## 4. 統合アーキテクチャ（12）への反映点

| 層 | 足す・変える点 | 根拠 |
|---|---|---|
| L1 信号健全性 | 周期・欠損・値域・カウンタ/チェックサムをOK/WARN/ERROR/FATALに集約。信号ごとの健全性を「可用性ベクトル」として下流へ渡す | S2, S4 |
| L1→L4 | 入力健全性→特徴量有効性→検知器有効性→警告可否をDAGで宣言（ラッチ＋明示リセット） | S6 |
| L3 R1 | 縦RSS（d_min）を学習モデルと独立の安全層として維持。式は一次資料（arXiv 1708.06374）で要照合 | S15 |
| L4 | CAN上のADAS ECU警報と自前モデルを独立2系統として扱い、不一致を監視 | S17 |
| L5 | 警告段階は一方向エスカレート＋ヒステリシス。推論パイプライン自体のハートビート途絶時は「警告不能」を運転者に通知 | S1, S3, S5 |
| L5 スコア | FCW頻度・急制動率などイベント率ベースのドライバースコア。感度設定の正規化 | S21 |
| L0 | listen-only・デフォルト無音をHW/SWで担保（送信経路を持たない） | S9 |
| L6 | 運用中監視（分布ドリフト・欠損）、「注意深い人間」参照モデルとの比較、SOTIF観点の限界条件整理 | S10, S13, S18 |

【推察】上表はいずれも公開資料からの転用案であり、車種・ECU実装での検証は未実施。

## 5. 課題・ギャップ

- 本文を読めなかったソースが多い（特にTesla・Toyota・Waymo・Mobileye・Autoware公式、commaブログ）。許可ドメイン追加後の再取得が必要
- Wayveの安全アーキテクチャの一次資料は特定できなかった。Baidu Apollo ControlのSafety check、openpilotのdmonitoringd／panda ハートビートも未確認
- Tesla Safety Scoreの係数・上限は版により資料間で食い違う
- Apolloの閾値（2.5秒・約10秒）は版依存で、公式コードでの確認が要る
- 日本語の一次資料が少ない（トヨタ1件、EE Times Japan見出しのみ）
- 企業の安全成績（Waymo 等）は自己申告で、日付・定義が不確か

## 6. 次のアクション提案

1. Apollo guardian/monitorの実装コードで閾値と required_for_safety の扱いを確認する
2. RSS縦方向式を一次資料（arXiv 1708.06374）で照合し、CAN信号での実装可否（車種別）をBACKLOG 4と合わせて整理する
3. 12に「入力健全性DAG＋可用性ベクトル」「警告の単調エスカレート／ラッチ」を設計要素として追記する
4. Tesla Safety Scoreの版別定義を一次ページで確定し、CAN再現可能なイベント率の対応表を作る
5. Wayve・Waymoの一次資料（公式安全報告）を、ドメイン許可のある環境で再確認する

## 7. 参考文献リスト（本文の S1〜S28 のURL）

S1 https://github.com/ApolloAuto/apollo/tree/master/modules/guardian
S2 https://github.com/ApolloAuto/apollo/tree/master/modules/monitor
S3 https://blog.csdn.net/qq_32378713/article/details/128126473
S4 https://github.com/autowarefoundation/autoware_universe/tree/main/system/autoware_mrm_handler
S5 https://docs.autoware.org/main/design/autoware-architecture-v1/interfaces/ad-api/features/fail-safe/
S6 https://autowarefoundation.github.io/autoware.universe_planning/main/system/system_diagnostic_graph
S7 https://gitlab.com/autowarefoundation/autoware.auto/AutowareAuto/-/issues/1233
S8 https://github.com/commaai/openpilot/blob/master/docs/SAFETY.md
S9 https://github.com/commaai/opendbc
S10 https://arxiv.org/pdf/2306.01917
S11 https://blog.waymo.com/blog/2023/03/a-blueprint-for-av-safety-waymos
S12 https://arxiv.org/pdf/2212.08148
S13 https://saemobilus.sae.org/papers/collision-avoidance-effectiveness-automated-driving-system-using-a-human-driver-behavior-reference-model-reconstructed-fatal-collisions-2026-01-0520
S14 https://waymo.com/safety/impact
S15 https://www.mobileye.com/responsibility-sensitive-safety/
S16 https://pdf.arxiv.org/pdf/1911.01207
S17 https://www.mobileye.com/blog/av-safety-demands-true-redundancy/
S18 https://autonews.gasgoo.com/articles/icv/mobileye-receives-tv-sds-first-aeb-development-and-testing-certificate-2115032298189369345
S19 https://eetimes.itmedia.co.jp/ee/articles/2010/22/news071_2.html
S20 https://s24.q4cdn.com/622300748/files/doc_news/Wayve-Releases-GAIA-1-Technical-Report-to-Advance-World-Models-for-Autonomy-2023.pdf
S21 https://www.tesla.com/en_CA/support/safety-score
S22 https://driveteslacanada.ca/news/tesla-q1-2024-vehicle-safety-report/
S23 https://www.theautopian.com/is-tesla-may-miscounting-crashes-to-make-autopilot-seem-safer-new-study-suggests-it-might-be/
S24 https://pressroom.toyota.com/?p=16679
S25 https://www.woven.toyota/en/news/20250521
S26 https://apex.ai/toyota-woven-planet
S27 https://global.toyota/jp/detail/18795024
S28 https://techcrunch.com/2026/10/30/waymos-next-robotaxi-will-be-a-toyota-bz4x-destined-for-japan-and-the-uk
