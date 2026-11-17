# 30. ドライバー別少数ショット適応の評価設計と、同一車両・複数ドライバーのCAN付き公開データ（B-28）

- 調査日: 2026-11-17
- 論点: B-28。同一車両・複数ドライバーでCAN／車両信号を含む公開データの信号・規模・入手条件を確認し、leave-one-driver-out（LODO）と少数ショット適応の評価に使えるかを判定する。あわせて、ドライバーまたぎ評価・個人適応の先行事例を集める。
- 既存調査との関係: 03 §2（D1〜D5、HCRL OCSLab driving dataset、PDB、KCID を含む）、21（DriveDNA の車種またぎ）、28（DG・LODO・MetaFollower 等）、23（年齢・熟練度）は扱い済みとして除外した。本稿はその先（ドライバー軸の評価手順と、新規データセットの人数・信号・ライセンス）に限る。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）14件／既出の再掲 6件。`scripts/sources_index.py --check` で照合した。
- 確認方法の注記: この実行でも arxiv.org・huggingface.co・jstage・ieee-dataport・usenix 等で WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の抜粋のみで確認し、本文は未読である。人数・信号名・数値は抜粋由来で、原文照合が必要。

## 1. エグゼクティブサマリー

- CAN／車両信号のみで、同一車両・多人数・ドライバー別少数ショット適応を事故予兆（またはそれに近いブレーキ・減速予測）で評価した公開研究は、英語・日本語の検索で見つからなかった。
- ドライバー軸の評価設計に最も近い雛形は DriveDNA（2026）である。ドライバー非重複の train/val/test（212/45/45人）と、別枠の少数ショット用53人を持つと抜粋に記載されている。少数ショット個人化の利得は小さく（5秒先・k=5 で約+0.8±0.5%）、利得が正のドライバーは55%との記載である（抜粋）。
- 同一車両・多人数の候補は、100-DrivingStyle（100人、同一車・同一ルート、操舵角・横加速度・スロットル・ブレーキ圧、1人約30分）が人数面で最有力である。ただし事故予兆ラベルも前方車情報もなく、少数ショットの支援セットが短い。
- Car Mine（Hyundai YF Sonata、4人、CAN由来51特徴量、ログイン必要）は条件は合うが規模が小さく、LODO は4分割で統計的検出力が弱い（抜粋）。
- 個人適応の他分野の数値として、車線変更の個人化モデルが一般モデルより27.8%精度向上（抜粋。相対か絶対かは未確認）。ただし入力信号は未確認で、そのままの参照値にはできない。
- 日本語では、ブレーキタイミングの個人適応（自動車技術会論文集 2020）、MPC＋個人モデル誤差補正（計測自動制御学会論文集 2026）が見つかったが、数値・被験者数は抜粋では不明である。
- 【推察】評価は「ドライバー非重複分割＋別枠の少数ショット用ドライバー」で固定し、平均値だけでなくドライバーごとの利得分布と改善した割合を報告する。想定される利得は小さく（約1%台以下）、人数が数十人規模では平均差が有意にならない可能性が高い。

## 2. 主要知見

凡例: 確認方法はすべて「抜粋のみ」。

### 2.1 評価設計の雛形・個人適応の先行事例

**[1] DriveDNA: A Large-Scale Multimodal Naturalistic Driving Dataset and Benchmark for Driving Style Identification** — HenryYHW 名義（著者未確認）、2026、データセット＋ベンチマーク。https://huggingface.co/datasets/HenryYHW/DriveDNA （論文 https://arxiv.org/pdf/2607.23822 は 21 で既出）
- 事実（抜粋）: 4,121走行・465人・975時間・10Hz、CAN＋前方映像。ドライバー非重複で train212/val45/test45、別に少数ショット用の53人。スタイルは「数分」の運転から推定。少数ショット個人化は全3シードで未見ドライバーに有効だが、5秒先・k=5 の利得は約+0.8±0.5%。尤度の利得が正のドライバーは55%、点推定誤差の利得は0付近。スタイルベクトルの FiLM 条件付けで+0.4〜1.4%、クエリへの注入は-0.7%。
- 【推察】21 の車種またぎ分割に加え、本稿ではドライバー軸の雛形として使う。CAN 単独版の入力信号は未確認。

**[2] Driver Digital Twin for Online Prediction of Personalized Lane Change Behavior** — Xishun Liao ら、2022（arXiv）／2023（IEEE IoT Journal）、論文。https://arxiv.org/abs/2211.01294
- 事実（抜粋）: 個人化モデルが一般モデルより27.8%精度向上と報告。クラウドで各ドライバーを履歴から学習。実車3台で、車線横断の平均6.08秒前（SD 1.96秒）に意図を認識。
- 【推察】ドライバー間で利得が大きく異なる点は、利得分布を報告する根拠になる。入力信号と27.8%の定義は未確認。

**[3] A comparative study on transferable driver behavior learning methods in the lane-change scenario** — BIT（北京理工大）、年未確認、比較研究。https://pure.bit.edu.cn/en/publications/a-comparative-study-on-transferable-driver-behavior-learning-meth/
- 事実（抜粋）: 転移学習で新ドライバーのモデルが少量データで高精度に達する。周辺分布と条件付き分布の両方を合わせる手法が最良。数値なし。
- 【推察】複数の適応手法を同一プロトコルで比較する設計の根拠。

**[4] Lane Change Intention Prediction of two distinct Populations using a Transformer** — ドイツ・香港のデータ、2025、プレプリント（二次要約サイト経由）。https://www.themoonlight.io/review/lane-change-intention-prediction-of-two-distinct-populations-using-a-transformer
- 事実（二次要約の抜粋）: exiD で学習したモデルは香港データで41.30%。複数集団を混ぜて学習すると大きく改善。
- 【推察】ドライバーだけでなく道路・集団をまたぐ評価が必要。28 [20] と同系統で、ID・数値は I-32 の未確定事項と同根。

**[5] 自動運転車のブレーキタイミングの個人適応（交差点）** — 自動車技術会論文集 51(3)、2020、論文（日本語）。https://www.jstage.jst.go.jp/article/jsaeronbun/51/3/51_20204209/_article/-char/en
- 事実（検索要約。題名は要約から起こしたもので未確認）: 少数パラメータのモデルで交差点のブレーキタイミングを個人に適応し、実車で快適性・受容性が向上。
- 【推察】少数パラメータ型は数分のデータでも過学習しにくく、低データ適応の候補。数値・被験者数は未確認。

**[6] 個人特性を反映したステアリング運転者モデル（MPC＋個人モデル誤差補正器）** — 計測自動制御学会論文集 62(1)、2026、論文（日本語）。https://www.jstage.jst.go.jp/article/sicetr/62/1/62_2/_article/-char/ja
- 事実（検索要約。題名・著者未確認）: MPC に個人モデル誤差の補正器を組み合わせ、個人の車線変更タイミングの好みをより正確に再現。
- 【推察】共通モデル＋個人の残差補正という構造の例。評価数値は不明。

**[7] PEDRA（Tian・Shi）** — 2026（年は URL 表記）、論文。https://weisongshi.org/papers/tian26-PEDRA.pdf
- 事実（検索結果の記載）: 短いセッションから個人の車間の安全エンベロープを学習し、CARLA ストリームと CAN 入力を使うとされる。会場・数値は未確認。
- 【推察】L2〜L3 の個人別しきい値の参考。内容未読のため参考扱い。

**[8] Generative car-following model conditioned on driving styles** — 2021、論文。https://arxiv.org/pdf/2112.05399
- 事実（検索結果の記載）: 200人のドライバーごとの車間RMSEが平均0.0581で IDM の0.0991より小さい。
- 【推察】これは各ドライバーへの当てはめの比較で、未見ドライバーへの適応ではない。評価と混同しないための対照例。

### 2.2 同一車両・複数ドライバーの公開データ

| データ | ドライバー数・車両 | 信号（抜粋の記載） | 入手・ライセンス | LODO 適性（【推察】） |
|---|---|---|---|---|
| 100-DrivingStyle [9] | 100人、同一車・同一ルート、1人約30分、計2200km | 操舵角、横加速度、スロットル、ブレーキ圧 | GitHub 公開とされるが未確認 | 人数は最有力。支援セットが短く、事故ラベル・前方車情報なし |
| This Car is Mine [10] | 4人、Hyundai YF Sonata、走行数 A8/B8/C5/D9 | CAN由来51特徴量 | IEEE DataPort、ログイン必要 | 条件は合うが4分割で検出力が弱い。個人内の時系列分割向き |
| UAH-DriveSet [11] | 6人・6車両（1対1）、500分超 | スマホ由来が主。CAN/OBD信号一覧は未確認 | リーダは CC BY-NC 4.0 | 車両とドライバーが交絡。CAN限定前提に合わない |
| comma2k19 [12] | 33時間超・2019セグメント | GNSS・全CAN | MIT（HF メタデータ由来。公式未確認） | ドライバーID無しの可能性。LODO 不向き |
| CANdid [13] | 10台 | CAN＋動作ラベル・GPS | オープンアクセス | 車両多様性向き。ドライバー情報は未確認 |
| Islam ら [14] | 不明 | CAN＋運転スタイル（題名のみ） | IEEE DataPort | 構成は一次確認が必要 |

**[9] 100 Drivers, 2200 km: A Natural Dataset of Driving Style toward Human-centered Intelligent Driving Systems** — Zhang ら、2024、データセット論文。https://arxiv.org/pdf/2406.07894
**[10] This Car is Mine!: Driver Pattern Dataset extracted from CAN-bus** — Kyung Ho Park（高麗大）、2019頃。https://ieee-dataport.org/open-access/car-mine-driver-pattern-dataset-extracted-can-bus （1Hz という記載は別のレビュー論文による特徴づけで、DataPort 本体の記載ではない）
**[11] Need data for driver behaviour analysis? Presenting the public UAH-DriveSet** — Romera・Bergasa・Arroyo、2016 ITSC。https://portalcientifico.uah.es/documentos/6276b52c2c3d9944cd36c9c4?lang=en （ドライバー6は電気自動車で、二次道路では normal と drowsy のみ）
**[12] A Commute in Data: The comma2k19 Dataset** — comma.ai、2018。https://arxiv.org/pdf/1812.05752
**[13] CANdid - An Open-Access Annotated Dataset of Vehicle CAN Bus Traffic** — Howson ら（アデレード大）、2025 USENIX VehicleSec。https://www.usenix.org/conference/vehiclesec25/presentation/howson
**[14] Real-time detection of aggressive driving using CAN data (differentiating drivers' styles)** — Islam ら、2023〜2024、データセット（題名のみ確認）。https://ieee-dataport.org/documents/real-time-detection-aggressive-driving-using-can-data-differentiating-drivers-styles-and

### 2.3 既出の再掲（本稿の論点に関わる新しい点のみ）

- 既出（01・05）: Fugiglando ら（Audi A3 10台・64人・55日、信号はアクセル・ブレーキ圧・操舵・加速度等、4Hz）。arXiv 1710.04133。データ非公開とみられ、車両差とドライバー差が交絡する。【推察】
- 既出（21）: Lestyán ら 1902.08956、既出（01）: Remeli ら 1911.09508。33人で再識別75〜85%（抜粋）。CAN からドライバー固有性が取り出せる根拠。
- 既出（09）: Continual Learning for Behavior-based Driver Identification（arXiv 2412.10780）。新データのみの微調整は破滅的忘却を起こし、リプレイ法は性能低下を11%に抑えるとの抜粋。【推察】個人適応後は元の母集団でも再評価する。
- 既出（01）: Kwak ら 1704.05223。OCSLab データの人数・信号名は HCRL 公式ページ（03 既出）で直接確認が必要。

## 3. 統合アーキテクチャ（12）への反映点

- L2（DRV・ドライバー特性）: 共通モデル＋ドライバー固有の小さな適応部（FiLM・残差補正・少数パラメータ）という構造を [1][5][6] が支持する。
- L6（評価・検証）: 評価プロトコルを追加する。
  1. ドライバー非重複の train/val/test ＋ 別枠の少数ショット用ドライバー（[1] の構成）。
  2. 支援セットは k 回または数分とし、k を振る。
  3. 指標は誤差と尤度の両方、ドライバーごとの利得分布、改善したドライバーの割合、複数シード。
  4. 適応後に元の母集団で再評価する（忘却確認）。
  5. 道路・集団まで広げた held-out を別に置く（[4]）。
- L4: 個人別しきい値は、適応でどれだけ警報率が動くかを 29 の校正評価と組み合わせて確認する。【推察】

## 4. 課題・ギャップ

- CANのみ・同一車両・事故予兆ラベル付き・数十人規模以上の公開データは確認できなかった。100-DrivingStyle は人数は十分だが信号4種・約30分で、事故予兆ラベルなし。
- 少数ショット適応の利得は DriveDNA で約1%以下と小さく、人数に対する検出力設計が必要である。
- 全ソースが抜粋のみ。ライセンス、人数、信号名、27.8%の定義は一次確認が必要。
- 日本語で数値つきのドライバーまたぎ評価は見つからなかった。サブエージェントの検索（J-STAGE・自動車技術会・情報処理学会向け）でも該当なし。

## 5. 次のアクション提案

1. 100-DrivingStyle の GitHub・Car Mine の DataPort で、信号名・ライセンス・ドライバーごとの時間を一次確認する（I-01 解消後）。
2. 上記 L6 評価プロトコルを、サンプルサイズ計算（ドライバー数・利得分布）つきで 12 の設計タスク（I-11 系）に落とす。
3. [2] [5] [6] の入力信号・被験者数・数値を本文で確認する。
4. B-27（日本語予稿の直接検索）で、ブレーキ意図・減速予測のドライバー個人差を検索する。
5. 事故予兆ラベルを持つ同一車両・多人数データの有無を、国内（JARI・東京農工大）への問い合わせ前提で整理する（26 と連携）。

## 6. 参考文献リスト

新規（抜粋のみ）:
1. https://huggingface.co/datasets/HenryYHW/DriveDNA
2. https://arxiv.org/abs/2211.01294
3. https://pure.bit.edu.cn/en/publications/a-comparative-study-on-transferable-driver-behavior-learning-meth/
4. https://www.themoonlight.io/review/lane-change-intention-prediction-of-two-distinct-populations-using-a-transformer
5. https://www.jstage.jst.go.jp/article/jsaeronbun/51/3/51_20204209/_article/-char/en
6. https://www.jstage.jst.go.jp/article/sicetr/62/1/62_2/_article/-char/ja
7. https://weisongshi.org/papers/tian26-PEDRA.pdf
8. https://arxiv.org/pdf/2112.05399
9. https://arxiv.org/pdf/2406.07894
10. https://ieee-dataport.org/open-access/car-mine-driver-pattern-dataset-extracted-can-bus
11. https://portalcientifico.uah.es/documentos/6276b52c2c3d9944cd36c9c4?lang=en
12. https://arxiv.org/pdf/1812.05752
13. https://www.usenix.org/conference/vehiclesec25/presentation/howson
14. https://ieee-dataport.org/documents/real-time-detection-aggressive-driving-using-can-data-differentiating-drivers-styles-and

既出の再掲:
- https://arxiv.org/pdf/2607.23822 （21）
- https://www.arxiv.org/pdf/2412.10780 （09）
- https://arxiv.org/pdf/1710.04133 （01・05）
- https://arxiv.org/pdf/1704.05223 （01）
- https://arxiv.org/pdf/1902.08956 （21）
- https://arxiv.org/pdf/1911.09508 （01）
