# テーマ3: 公開CANデータセット・CAN信号定義・取得/解析ツールの調査

- 調査日: 2026-11-01
- テーマのゴール: 有人運転車両でCANバスのデータ"のみ"を使って事故の予兆を検知・警告するという最終目的に向け、研究開発に使える公開CANデータセット、CAN信号定義（DBC）、取得・解析ツールを網羅的に集める。事故予防モデル開発の観点（信号の種類、規模、ラベルの有無、ライセンス、入手方法）で比較・整理する。
- 表記ルール: 本文の事実記述はすべて末尾の参考文献（[番号]）に基づく。筆者の推察には「【推察】」を付ける。ライセンスや規模のうち、ソースで確認できなかった項目は「未確認」と書く。

---

## 1. エグゼクティブサマリー

1. 公開CANデータセットは「侵入検知（IDS）用」と「運転行動・自動運転研究用」の2系統に分かれる。IDS系（HCRL Car-Hacking、ROAD、SynCAN、can-train-and-test、TU/e CAN Intrusion）は攻撃ラベルを持つが、事故やヒヤリハットのラベルはない[3][5][6][7][9]。
2. 生のCANフレームと実走行を兼ね備え、事故予防の基礎研究に最も使いやすいのは comma2k19 である。約33時間、MIT、CAN全量（車速・操舵角・車輪速・レーダトラック）を含む[1]。ただしラベルはない。
3. 事故・ヒヤリハットのラベルがある車両データは、ほぼ自然運転研究（SHRP2 NDS: 衝突1,549件・ニアミス2,705件、100-Car: 公開分は衝突60件・ニアミス768件）に限られる[15][16][17]。どちらもアクセスに制約があり、10 Hz程度に加工済みの車両ネットワーク変数として提供されるため、生CANではない[16][18]。
4. 運転行動ラベル（車線変更・合流・右左折など）とCAN信号を併せ持つものに Honda HDD（104時間、非商用・大学所属者限定）[12]がある。車両バス信号を含む自動運転データセットとして nuScenes CAN bus expansion[13]と A2D2（CC BY-ND 4.0）[14]がある。
5. 信号定義の公開ソースの中心は commaai/opendbc（MIT）である[20]。DBCが手に入らない車両向けには、READ[21]、LibreCAN[22]、CAN-D[23]といった自動リバースエンジニアリング手法がある。OBD-II PID（SAE J1979）[24]や J1939（商用車）[26]は標準化されているが、取れる信号は限られる。
6. ツールはオープンソースだけで「取得（panda / CANedge / SocketCAN）→デコード（cantools / asammdf）→解析・RE（cabana / SavvyCAN）」の流れを組める[27]〜[35]。
7. 【推察】本プロジェクトで最大の障害になるのは「CANのみ」と「事故・ニアミスラベル」を両立した公開データが実質的に存在しないことである。当面は (a) comma2k19 などの実走行CANでの教師なし異常検知、(b) SHRP2系の運動学変数（速度・加速度・ヨーレート・ペダル）での教師ありニアミス予測[37][38]、を組み合わせるのが現実的である。

---

## 2. データセット一覧

### 2.1 比較サマリー表

| # | 名称 | 提供者 | 年 | 生CAN | 主な信号 | 規模 | ラベル | ライセンス/入手 | 事故予防での有用度【推察】 |
|---|---|---|---|---|---|---|---|---|---|
| D1 | comma2k19 | comma.ai | 2018頃 | ○ | CAN全量（車速・操舵角・車輪速・レーダトラック）、GNSS、IMU、前方映像 | 約33時間、2,019セグメント、約100 GB | なし | MIT（リポジトリ）、Academic Torrents | 高（実走行CANの基盤データ） |
| D2 | commaCarSegments | comma.ai | 2024〜 | 未確認 | openpilot走行セグメント | 多数（件数未確認） | 未確認 | Hugging Face | 中（多車種化の候補、要調査） |
| D3 | HCRL Car-Hacking | 高麗大 HCRL | 2018〜2020 | ○ | 生フレーム（ID, DLC, DATA） | 各30〜40分×4攻撃 | 攻撃（T/R） | 学術利用（論文引用） | 低（攻撃検知用） |
| D4 | HCRL Survival Analysis | 高麗大 HCRL | 2018 | ○ | 生フレーム、3車種 | 正常は1車種あたり60〜90秒程度との指摘あり | 攻撃 | IEEE DataPort | 低 |
| D5 | HCRL Driving Dataset (OCSLab) | 高麗大 HCRL | 2015〜 | ×（OBD由来51特徴） | エンジン・燃料・トランスミッション系の特徴量 | 約23時間、運転者10名 | 運転者ID | 学術利用 | 中（運転者特性・個人差の検討） |
| D6 | ROAD | ORNL | 2020/2024 | ○＋信号時系列CSV | 生CAN、CAN-Dでデコードした信号 | 約3.5時間（556.7 MB） | 攻撃（0/1） | CC BY 4.0、Zenodo | 中（デコード済み信号の実例として有用） |
| D7 | SynCAN | ETAS (Bosch) | 2019 | ×（合成信号） | 10 ID・20信号 | 学習4＋テスト6アーカイブ | 攻撃5種 | 非商用研究、GitHub（アーカイブ済） | 低〜中（信号レベル異常検知の手法検証） |
| D8 | can-train-and-test | Lampe & Meng | 2023/2024 | ○ | 4車両（GM、Subaru） | 236 CSV、約1.93億行、約7.5 GB | 攻撃9種 | Bitbucket（ライセンス未確認） | 低〜中（車種間汎化の検証） |
| D9 | TU/e Automotive CAN Bus Intrusion v2 | TU Eindhoven | 2019 | ○ | Opel Astra、Renault Clio、試作バス | 約102.9 MB | 攻撃5種 | CC BY-NC 4.0、4TU | 低 |
| D10 | Udacity Self-Driving Car | Udacity | 2016 | △（ROS bag内の車両レポート） | ギア・ブレーキ・スロットル・操舵・車速、画像 | 40 GB / 183 GB / 223 GB 等 | 一部アノテーション（画像） | リポジトリはアーカイブ済、ライセンス未確認 | 中（運転操作信号の時系列） |
| D11 | Honda HDD | Honda Research Institute USA | 2018 | △（CAN値。生フレームかは未確認） | CANセンサ値、GPS、カメラ等 | 104時間、137セッション | 運転行動（車線変更・合流・右左折など） | 非商用、大学メール必須 | 高（行動ラベル付き） |
| D12 | nuScenes CAN bus expansion | Motional (nuTonomy) | 2020 | △（JSON化された信号） | 操舵角100 Hz、ブレーキ・スロットル・操舵センサ約800〜970 Hz、車輪速、ウインカー等 | nuScenes各シーン | なし（シーン注釈は別） | nuScenes規約（CANデータの個別ライセンスは未確認） | 中（高頻度ペダル・操舵） |
| D13 | A2D2 | Audi | 2020 | △（車両バスデータ） | 車速・加速度・操舵角・スロットル・ブレーキ | 論文記載の規模 | 3D/セマンティック（画像・点群） | CC BY-ND 4.0（商用可、改変物の再配布不可） | 中 |
| D14 | Vehicle Energy Dataset (VED) | Univ. of Michigan | 2019/2020 | ×（OBD-II） | 車速、RPM、MAF、GPS、SOC等 | 383台、約37.4万マイル、1年間 | なし | Apache-2.0、GitHub | 中（多車両・長期の自然運転） |
| D15 | KCID (Kidmose CANid) | Kidmose ら | 2025 | ○ | 生CAN | 運転者16名×4車両 | 運転者ID・属性 | 入手条件は未確認 | 中（運転者状態の個人差の検討） |
| D16 | SHRP2 NDS | TRB / VTTI | 2010〜2013収集 | ×（10 Hzに加工された車両ネットワーク変数） | 速度、アクセル、ブレーキ、ABS、ギア、操舵角、シートベルト等 | 運転者3,400名超、トリップ540万件超 | 衝突1,549件・ニアミス2,705件・ベースライン2万件 | InSight（登録制、IRB研修。識別情報はエンクレーブ内のみ） | 最高（ただしアクセスの壁が高い） |
| D17 | 100-Car NDS | VTTI / NHTSA | 2001〜2003収集 | × | 車速、車間距離、TTC等 | 公開分: ニアミス768件・衝突60件 | 衝突・ニアミス | VTTI公開ポータル | 高（小規模だが入手容易） |
| D18 | UDRIVE | EU FP7 コンソーシアム | 2012〜2017 | ○（CAN収集） | CAN、運動学、映像5〜8視点 | 約87,871時間 | 未確認 | 法的・倫理的制約の下で外部提供予定（手続き未確認） | 高（欧州唯一の大規模NDS） |
| D19 | ヒヤリハットデータベース（東京農工大） | 東京農工大 / 自技会 | 2005〜 | ×（速度パルス・ブレーキ信号等） | 映像＋車速・ブレーキ操作 | タクシー車両の多数事例 | ヒヤリハット | 公開条件は未確認（共同研究ベースと推定） | 高（国内のニアミス事例） |
| D20 | JARI ドライブレコーダーデータ | 日本自動車研究所 | 2004〜 | × | 映像＋車両データ | タクシー200台ほか | 事故・ニアミス（自動検出＋目視） | 一般公開は確認できず | 中（国内事例、要問い合わせ） |

凡例: 生CAN ○=生フレームあり、△=デコード済み信号のみ、×=CAN以外（OBD・計測器など）または生CANなし。

### 2.2 各データセットの詳細

#### D1. comma2k19 [1]
- 提供者: comma.ai。URL: https://github.com/commaai/comma2k19
- 収録: カリフォルニア州280号線の通勤走行で、合計約33時間（1分×2,019セグメント）。grey pandaで取得したCAN全量を含み、車速、操舵角、車輪速、レーダトラックが入っている。ほかに生GNSS（Qualcomm/u-blox）、9軸IMU、前方映像（HEVC）、ECEF姿勢がある。
- 車両: RAV4（chunk 1〜2）、Honda Civic（chunk 3〜10）。
- 規模: 約100 GB（約10 GBのアーカイブ×10）。Academic Torrentsで配布。
- ラベル: なし。
- ライセンス: リポジトリはMIT。Hugging Face版のカードもMITとしている[2]。データ自体の個別条項は記載なし。
- 本プロジェクトでの用途: 生CANから信号をデコードする処理系（opendbcとの組み合わせ）の検証。正常運転の分布学習（教師なし異常検知のベースライン）。【推察】映像があるため、急ブレーキ前後の状況を目視で確認する補助ラベリングにも使える。

#### D2. commaCarSegments [2b]
- URL: https://huggingface.co/datasets/commaai/commaCarSegments
- 2024年1月に初回コミットがあり、segments/ 以下にハッシュ名のフォルダが多数並ぶ。CANデータの形式とライセンスはデータセットカードを読めておらず未確認である。【推察】openpilotの車種移植用セグメント集と考えられ、多車種の生CANを得られる可能性があるため、精査の優先度は高い。

#### D3. HCRL Car-Hacking Dataset [3][4]
- URL: https://sites.google.com/hksecurity.net/hcrl/Datasets/car-hacking-dataset
- 収録: OBD-IIポート経由で実車から記録した生フレーム（Timestamp, CAN ID, DLC, DATA[0..7], Flag T/R）。攻撃はDoS（ID 0x000を0.3 ms周期）、Fuzzy、ギア偽装、RPM偽装の4種で、各データセットに3〜5秒の注入が300回入る。各データセットは30〜40分。
- 車両: HCRLのページには車名がない。ROAD論文のサーベイでは Hyundai YF Sonata とされている[4]。
- ラベル: 攻撃フラグのみ。
- 利用条件: 学術目的で提供し、論文（Song, Woo, Kim 2020）の引用を求めている。正式なライセンス表記はない。
- 注意点: ROAD論文は「攻撃注入中に車両が実際には走行していなかった」などの問題を挙げ、テストセットとしての妥当性に疑問を示している[4]。
- 用途: 【推察】事故予防には直接使えない。ただし生CANの周期性・ID分布を扱う前処理の練習台にはなる。

#### D4. HCRL Survival Analysis Dataset [5]
- URL: https://sites.google.com/hksecurity.net/hcrl/Datasets/survival-ids
- 収録: Hyundai YF Sonata、Kia Soul、Chevrolet Spark の3車種で、Flooding、Fuzzy、Malfunction の攻撃（20秒ごとに5秒注入）。IEEE DataPortでも公開されている。
- 注意点: 正常走行のキャプチャが1車種あたり60〜90秒しかなく、学習には不十分との批判がある[4]。

#### D5. HCRL Driving Dataset（OCSLab）[6b]
- URL: https://sites.google.com/hksecurity.net/hcrl/Datasets/driving-dataset
- 収録: 運転者10名（A〜J）、約23時間。高麗大学〜ワールドカップ競技場の往復約46 km。関連論文によれば、KIA車両から取得したOBD-II由来の51特徴量（約9.4万レコード）で、生CANは含まない[6c]。
- ラベル: 運転者ID。
- 利用条件: 学術利用と論文引用。IEEE DataPort（DOI 10.21227/sg58-3392）からも入手できる。
- 用途: 【推察】運転者の個人差（同じ操作でもペダル・操舵の癖が異なる）を考慮したモデルの検討に使える。

#### D6. ROAD（Real ORNL Automotive Dynamometer）[7][4]
- URL: https://zenodo.org/records/10462796 、論文 https://arxiv.org/abs/2012.14600 （PLoS ONE 2024）
- 収録: 2010年代半ばの1車両（車種は非公開）。ダイナモと実路で記録した正常12キャプチャ（約3時間）と攻撃33キャプチャ（約30分）。攻撃はFuzzing、特定ID捏造（車輪速、最高速度表示、冷却水温、後退灯）、模擬マスカレード、アクセル攻撃。
- 形式: candump形式の生ログとJSONメタデータに加え、CAN-Dアルゴリズムでデコードした信号時系列CSV（Label, ID, Time, Signal-i-of-ID）がある。
- ライセンス: CC BY 4.0。データは車両の匿名性を保つよう難読化されている。
- 用途: 【推察】「生CANを信号時系列に変換した結果」を公開データで比べられる数少ない例であり、自前の信号抽出パイプラインの検証に使える。

#### D7. SynCAN [8]
- URL: https://github.com/etas/SynCAN
- 収録: 合成の信号レベルデータ（10 ID、計20信号）。攻撃はPlateau、Continuous、Playback、Suppress、Flooding の5種。正常テストセットもある。
- ライセンス: 学術・非学術を問わず非商用（研究・教育・出版・個人実験）に限る。フィールド使用は想定外。リポジトリはアーカイブ済み。
- 用途: 【推察】信号レベルの時系列異常検知（LSTM-AEなど）の実装確認に使える。

#### D8. can-train-and-test [9]
- URL: https://bitbucket.org/brooke-lampe/can-train-and-test 、論文 https://arxiv.org/abs/2308.04972 （Computers & Security 2024）
- 収録: GMとSubaruの4車両。攻撃はDoS、Fuzzing、各種Spoofing、Standstill、Interval など9種。236 CSV（約1.93億行、約7.5 GB）と再生可能な .log。正常:攻撃の比は36:1〜927:1。
- ライセンス: 未確認（Bitbucketページの本文を取得できなかった）。
- 用途: 【推察】「学習時に見ていない車種」での汎化テストという枠組みは、事故予防モデルの車種間汎化の評価設計に流用できる。

#### D9. TU/e Automotive CAN Bus Intrusion Dataset v2 [10]
- URL: https://data.4tu.nl/datasets/efb320d8-c189-4e54-98af-3a79cc14f421
- 収録: Opel Astra、Renault Clio、自作の試作CANバス。攻撃は診断、Fuzzing、Replay、Suspension、DoS。v2は約102.9 MB。
- ライセンス: CC BY-NC 4.0。

#### D10. Udacity Self-Driving Car Dataset [11][11b]
- URL: https://github.com/udacity/self-driving-car （2021年11月にアーカイブ済み）
- 収録: 223 GBのMountain View走行データ。画像フレームに加え、緯度経度、ギア、ブレーキ、スロットル、操舵角、車速を含む（ROS bag形式。dbw_mkzのBrakeReportやWheelSpeedReportなどのトピック）[11b]。
- ライセンス: 未確認。
- 用途: 【推察】ドライバー操作（ブレーキ・スロットル・操舵）の時系列を高頻度で得られるが、ラベルがなく、走行シーンも限られる。

#### D11. Honda Research Institute Driving Dataset（HDD）[12]
- URL: https://usa.honda-ri.com/hdd 、論文 https://arxiv.org/abs/1811.02307 （CVPR 2018）
- 収録: サンフランシスコ・ベイエリアで約104時間、137セッション。計測車両のCANセンサ値とGPS（映像にオーバーレイ）。
- ラベル: 目的指向の運転行動（車線分岐、車線変更、合流、駐車、交差点・横断歩道・踏切通過、右左折、Uターン）。論文では原因（stimulus）や注意の層もあるとされる。
- ライセンス: 非商用限定。大学所属者が大学メールで申請する必要がある。
- 用途: 【推察】CAN信号から運転行動（車線変更など）を認識する前段モデルの学習に最適である。運転者の「意図」と「操作」のずれを検知する研究の土台になる。

#### D12. nuScenes CAN bus expansion [13]
- URL: https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/can_bus/README.md
- 収録: Renault Zoe由来のIMU（100 Hz）、Pose（50 Hz）、Steer Angle Feedback（100 Hz）、Vehicle Monitor（2 Hz: 車速、ブレーキ、操舵、ギア、ウインカー等）、Zoe Sensors（約794〜973 Hz: ブレーキ・操舵・スロットルセンサ）、Zoe Vehicle Info（100 Hz: 車輪速・トルク・加速度）。2020年2月公開。
- 注意: README自身が「highly experimental（実験的）」と明記している。
- 用途: 【推察】ペダル・操舵を高サンプリングで扱える。周辺物体の注釈（カメラ・LiDAR）を、CAN特徴量の「教師信号」として使う研究に応用できる（推論時はCANのみ、学習時のみ外部センサを使う構成）。

#### D13. A2D2（Audi Autonomous Driving Dataset）[14]
- URL: https://arxiv.org/abs/2004.06320 （公式 a2d2.audi）
- 収録: 6カメラ、5 LiDARに加え、車両バスデータ（車速・加速度、操舵角、スロットル、ブレーキなど）。論文はこれを「公開データセットでこれまで不足していた」と位置づけている。
- ライセンス: CC BY-ND 4.0（商用利用可、改変物の再配布不可）。
- 用途: 【推察】商用利用できるため、製品化を視野に入れた検証データとして価値がある。

#### D14. Vehicle Energy Dataset（VED）[15b]
- URL: https://github.com/gsoh/VED 、論文 https://arxiv.org/abs/1905.02081
- 収録: ミシガン州アナーバーの一般車383台（ガソリン264、HV 92、PHV/EV 27）、2017年11月〜2018年11月、約37.4万マイル。OBD-IIロガーで車速、RPM、MAF、外気温、SOC、GPSを記録。
- ライセンス: Apache-2.0。
- 用途: 【推察】サンプリングが粗いOBD-II PIDだけでも、多数車両・長期間にわたって運転スタイル指標（急加減速頻度など）を算出できるかの検討に使える。

#### D15. KCID（Kidmose CANid Dataset）[15c]
- URL: https://arxiv.org/abs/2510.25856 （2025）
- 収録: 運転者16名×4車両の生CAN、運転者の属性情報、日常運転と固定ルート運転。既存の運転者識別データセット6種（HCRL Driving Datasetなど）のレビューも含む。
- 入手方法: 未確認。

#### D16. SHRP2 Naturalistic Driving Study（NDS）[16][17][18]
- URL: https://insight.shrp2nds.us/
- 規模: 運転者・車両3,400超、トリップ要約540万件超、衝突・ニアミス・ベースラインのイベント36,000件超[16]。トリガーアルゴリズムと目視検証で衝突1,549件、ニアミス2,705件を同定し、ケースコホート用のベースライン2万件を用意している[17]。
- 車両ネットワーク変数: アクセル、ブレーキペダル作動、ABS、ギア、操舵角、車速、ホーン、シートベルト、エアバッグ展開など。時系列は0.1秒刻み（10 Hz）[18]。
- アクセス: InSightは公開ポータルで、データ辞書とサンプルは閲覧できる。制限データにはIRB研修を受けた「qualified researcher」となる必要がある。個人を識別できるデータはデータ共有契約とIRB承認のうえ、セキュアエンクレーブ内でのみ閲覧できる[17]。
- 用途: 【推察】「CANで取れる種類の信号」と「事故・ニアミスラベル」を両方持つ、事実上唯一の大規模データ。事故予防モデルの教師あり学習と評価の中核候補だが、申請手続きと国外利用の可否を早めに確認する必要がある。

#### D17. 100-Car Naturalistic Driving Study [19]
- URL: https://www.vtti.vt.edu/PDFs/NDRS-abstracts/FINAL_Dozza_SAFER100Car.pdf （公開ポータル access.vtti.vt.edu）
- 公開分: ニアミス768件、衝突60件のイベント時系列（テキスト形式）。SAFER100Car GUIで時系列と視線を同期表示できる。
- 収録信号: 車速、車間距離、TTC、反応時間などが記録されている（NHTSA概要）。ブレーキ信号の有無はデータ辞書で確認が必要。

#### D18. UDRIVE [20b]
- URL: https://cordis.europa.eu/article/id/117051-firsthand-insight-into-drivers-natural-behaviour
- 収録: 欧州7か国の乗用車、トラック、二輪にCAN・運動学データと5〜8視点の映像を連続収集した。19機関のコンソーシアムで、2012〜2017年。集積は約87,871時間（DLRの報告）。
- アクセス: 「法的・倫理的制約の下で」外部研究者へ提供する方針とされるが、現行の手続きは確認できなかった。

#### D19. ヒヤリハットデータベース（東京農工大学）[36]
- URL: https://web.tuat.ac.jp/~nagaimu/kenkyu_smrc0.html
- 概要: 映像記録型ドライブレコーダーでヒヤリハットデータベースを構築・分析してきた拠点である。タクシー車両で急ブレーキや衝撃をトリガーに、前後の映像と速度パルス・ブレーキ操作信号などを記録する形式とされる。
- 公開条件: 確認できなかった。【推察】一般公開ではなく、共同研究や委託研究の枠組みでの提供と考えられる。

#### D20. JARI（日本自動車研究所）のドライブレコーダーデータ [36b]
- URL: https://jari.or.jp/en/research-content/safety
- 概要: 事故統計、事故現場データ、ニアミスのドライブレコーダーデータを使って事故発生メカニズムを分析している。過去の国交省事業ではタクシー200台から映像と車両データを集め、自動検出ソフトで事故・ニアミスを抽出していた（VTTI NDRSでの発表資料）。
- 公開条件: 一般研究者向けの公開は確認できなかった。

---

## 3. 信号定義・リバースエンジニアリング

### 3.1 公開DBC・信号定義

| 名称 | 内容 | ライセンス | 出典 |
|---|---|---|---|
| commaai/opendbc | `opendbc/dbc/` にDBC群。`opendbc/can/` はDBCからCANメッセージを解析・生成するライブラリ、`opendbc/car/<brand>/` は車種ごとのcarstate（受信解析）・carcontroller（送信生成）、`opendbc/safety/` は安全ファームウェア。対象車種は docs/CARS.md 参照。LKASとACCを持つ車両なら原理的に対応でき、対応の多くはコミュニティによる | MIT | [20] |
| OBD-II PID（SAE J1979） | Mode 01（現在値）に車速（PID 0x0D、0〜255 km/h）、エンジン回転数（0x0C、(256A+B)/4 rpm）、スロットル開度（0x11）など。最新規格ではサービスは10種 | 規格はSAE（有償）。PID一覧はWikipedia等で参照できる | [24][25] |
| SAE J1939（商用車） | 18ビットのPGNでメッセージを、SPNで信号を識別する。大半はブロードキャストで、一部はRequest（PGN 59904）で取得する。CSS ElectronicsがJ1939 Digital AnnexをDBC化（1,000超のPGN）したものを販売している | 規格はSAE（有償） | [26] |
| ROAD の信号時系列 | CAN-Dで抽出した信号CSV（実車の信号境界・エンディアンの推定例） | CC BY 4.0 | [7] |

【推察】乗用車の操舵角・ペダル・ブレーキ圧・ヨーレートなどはOBD-II PIDでは原則取れず、OEM独自のCAN IDを解読する必要がある。opendbcの対象車種と自社の対象車種が重なるかが、開発工数を大きく左右する。

### 3.2 CAN信号リバースエンジニアリング手法（論文）

| 手法 | 著者・掲載 | 概要 | 出典 |
|---|---|---|---|
| READ | Marchetti & Stabili, IEEE TIFS vol.14 no.4, 2019 | 未知のCANトレースからペイロード中の信号境界を自動で特定し、カウンタ・CRC・物理信号などに分類する。従来手法の2倍以上の信号を抽出し、処理時間を2桁短縮したと報告 | [21] |
| LibreCAN | Pesé ら（Univ. of Michigan）, ACM CCS 2019 | スマートフォンのセンサデータとOBD-IIを手がかりに、パワートレイン系に加えてボディ系信号も自動で翻訳する。ほぼ完全なCAN通信マトリクスを2分未満で生成するとされる。米国特許 12,225,044 | [22] |
| CAN-D | Verma ら（ORNL）, IEEE TVT vol.70 no.10, 2021 | 信号境界、エンディアン、符号有無を推定し、診断規格（OBD-II）との照合で物理的意味を与える4段パイプライン。10車両の評価で既存手法比ℓ1誤差が約5倍良いと報告。OBD-IIプラグインとして実装 | [23] |
| cabana＋can_print_changes / can_bit_transition | comma.ai | 多様なイベントを含む走行を記録し、cabanaで可視化してビット遷移を探す実務的な手法。2つの走行のCAN差分を取るスクリプトもある | [20][31] |

【推察】本プロジェクトの実務では、(1) opendbcに対象車がある場合はそれを使い、(2) ない場合はCAN-Dや READ で信号候補を自動抽出したうえで、OBD-II PID（車速・RPM）やスマホIMUとの相関で物理量を割り当てる（LibreCANの考え方）、という二段構えが妥当である。

### 3.3 CANで取れる信号と、事故予防に重要だがCANに流れにくい信号

以下は各データセットやDBCが実際に収録している信号[1][13][14][18][20]をもとに筆者が整理したもので、分類そのものは【推察】である。

| 区分 | 信号例 | 根拠・備考 |
|---|---|---|
| CANで比較的確実に取れる（運動・操作） | 車速、車輪速×4、操舵角・操舵角速度、ヨーレート、前後・横加速度、アクセル開度、ブレーキSW/マスタシリンダ圧、ギア、エンジン回転数 | comma2k19、nuScenes、A2D2、SHRP2の収録信号と共通する[1][13][14][18] |
| CANで取れることが多い（ボディ・状態） | ウインカー、ワイパー、ヘッドライト、シートベルト、ドア、ホーン、ABS/ESC作動 | SHRP2（ホーン・シートベルト・ABS）、nuScenes（ウインカー）[13][18] |
| 車種によって取れる（ADAS出力） | ACC/LKA/AEBの状態・警報、ACCレーダの先行車距離・相対速度、レーダトラック、車線認識結果 | comma2k19はレーダトラックを含む[1]。【推察】ADAS専用バスやゲートウェイの奥にあり、OBDポートからは見えない車種が多い |
| CANにほぼ流れない（本プロジェクトの盲点） | 運転者の視線・閉眼・姿勢（DMS）、周辺車両・歩行者の位置、路面摩擦・天候、道路形状・制限速度（地図）、精密GPS | 【推察】これらはカメラ・地図・外部センサ由来であり、CANのみの前提では代理指標（操舵の微修正パターンで眠気を推定する、など）で補う必要がある |

補足（事実）: 操舵角だけでも眠気分類ができ、居眠り起因の車線逸脱の少なくとも6秒前に分類できたとする研究がある[39]。操舵角・操舵角速度・ヨーレート・横加速度などの車両ベース指標を深層学習に入力する研究もある[39]。いずれも「CANのみ」で運転者状態に迫れる可能性を示している。一方で、操舵角は道路形状に依存するという限界も指摘されている[39]。

---

## 4. ツール一覧

| ツール | 種別 | 用途 | ライセンス | URL・出典 |
|---|---|---|---|---|
| python-can | Pythonライブラリ | 各種インタフェース（Kvaser、PCAN、IXXAT、SocketCAN等）の抽象化、送受信、ログI/O | LGPL-3.0（一部ファイル、例: blf.py はGPL-3） | https://github.com/hardbyte/python-can [27] |
| cantools | Pythonライブラリ | DBC/KCD/SYM/ARXML/CDDの解析、エンコード・デコード、candumpデコード、Cコード生成、プロット | MIT | https://github.com/cantools/cantools [28] |
| asammdf | Pythonライブラリ＋GUI | MDF v2/3/4の読み書き、DBC/ARXMLによるCANバスログの信号抽出、プロット | LGPLv3+ | https://github.com/danielhrisca/asammdf [29][29b] |
| SavvyCAN | GUI（Qt） | CANキャプチャ、可視化、リバースエンジニアリング、デバッグ | MIT | https://github.com/collin80/SavvyCAN [30] |
| cabana | GUI（openpilot） | 生CANの閲覧、DBCの作成・編集、opendbc連携、comma connectのルートやpandaからのライブ読み込み | openpilotに同梱（MIT）【推察】 | https://blog.comma.ai/open-sourcing-openpilot-development-tools/ [31] |
| panda | ハードウェア＋FW＋Python | CAN / CAN FD の取得・送信。opendbcの安全モデルをFWに組み込み | MIT | https://github.com/commaai/panda [32] |
| opendbc | Python＋DBC | DBCデータベースと車種インタフェース | MIT | https://github.com/commaai/opendbc [20] |
| can-utils（SocketCAN） | Linux CLI | candump（記録・フィルタ）、cansniffer（変化の検出）、canplayer（再生）、cansend、cangen | GPL/BSD（Linux SocketCAN系）【推察】 | https://github.com/linux-can/can-utils [33] |
| CSS Electronics CANedge | 市販ロガー | CAN/CAN FDをSDカードにMF4で記録（CANedge2はWiFiでS3へアップロード）。ソフト・APIは無償のオープンソース（asammdf、Python API、MF4変換） | ハードは有償、ソフトはオープンソース | https://www.csselectronics.com/products/can-logger-sd-canedge1 [34] |
| Kvaser CANlib SDK / pycanlib | SDK | Kvaserインタフェース用API（Windows/Linux）。`pip install canlib` | SDKは無償（登録不要） | https://kvaser.com/developer/canlib-sdk [35] |
| Vector CANalyzer / CANoe | 商用ツール | CANalyzerは解析（DBC/LDF/FIBEX/AUTOSAR対応）、CANoeは解析・シミュレーション・テスト・診断 | 商用 | https://en.wikipedia.org/wiki/CANalyzer [35b] |
| Vector CANdb++ Editor | DBCエディタ | DBCの閲覧・編集（フリーウェアとして提供） | フリーウェア | https://www.vector.com/en/business-unit/testing-validation-diagnostics/resources/database-tools-ldf-explorer-candb-editor-fibex-exporer-available-freeware/ [35c] |

【推察】推奨構成: 車両からの取得は panda（opendbc対応車）か CANedge（長期フリート記録）、前処理は cantools と asammdf（MF4→DBCデコード→Parquet）、信号探索は cabana と SavvyCAN、ラベル付けと可視化は自作のJupyter環境。すべてOSSで組めるため、PoCの初期費用を抑えられる。

---

## 5. 課題・ギャップ

1. 事故・ニアミスのラベル付き「生CAN」データは公開されていない（事実ベースの整理）。IDS系データのラベルはサイバー攻撃であり[3][5][7][8][9][10]、事故・ニアミスのラベルがあるSHRP2 / 100-Carは加工済みの車両変数で、アクセスも制限されている[16][17][19]。
2. 規模と多様性が足りない。生CANの実走行データで最大級の comma2k19 でも約33時間・2車種・ほぼ高速道路の単一ルートである[1]。【推察】一般道、夜間、雨天、高齢運転者などのリスク条件はほとんど含まれない。
3. IDSデータセットの品質に問題がある。HCRL Car-Hackingは攻撃時に車両が走行していなかった、Survival Analysisは正常データが短い、といった指摘がある[4]。【推察】正常走行データとして流用する場合も注意が必要である。
4. 信号定義は独自仕様である。乗用車のCAN信号エンコードはOEM固有で非公開であり[23]、opendbcの対象外の車種では解読コストがかかる。
5. 【推察】ゲートウェイとセキュリティの壁がある。近年の車両ではOBDポートとシャシー/ADASバスの間にゲートウェイがあり、OBDから見える信号が限られる。製品化では取り付け位置（ハーネス分岐など）とOEMの協力が必要になる。
6. 外部状況（先行車距離・車線位置）はCANに流れないことが多い。ACCレーダやレーンカメラの出力がCANに出る車種でなければ、TTCやTHWは計算できない。【推察】CANのみでの事故予兆検知は「自車の挙動異常」と「運転者操作の異常」の検知に重心を置かざるを得ない。
7. ライセンスの制約が強い。HDD（非商用・大学限定）[12]、SynCAN（非商用）[8]、TU/e（CC BY-NC）[10]など非商用条件が多い。商用に使えるのは comma2k19（MIT）[1]、ROAD（CC BY 4.0）[7]、VED（Apache-2.0）[15b]、A2D2（CC BY-ND 4.0）[14]に限られる。
8. 国内データがない。東京農工大やJARIのヒヤリハットDBは存在する[36][36b]が、一般公開は確認できなかった。

---

## 6. 次のアクション提案

1. comma2k19 と opendbc でベースラインのパイプラインを作る。Honda Civic / RAV4 のCANをopendbcのDBCでデコードし、車速・加速度・操舵・ブレーキなどの正常分布モデル（教師なし異常検知）と、急減速・急操舵イベントの自動抽出を試作する。根拠: [1][20][28]。
2. SHRP2 InSight のアクセスを申請する（可否確認を含む）。ゲスト閲覧で時系列データ辞書を確認し、衝突・ニアミスイベントの時系列（10 Hzの車両ネットワーク変数）の取得条件を調べる。Osman ら（約90%）[37]や Khattak ら（約95.6%）[38]のベースラインを再現できるか検討する。並行して100-Carの公開イベント（衝突60件・ニアミス768件）[19]で、すぐに試せる教師ありの小規模実験を行う。
3. Honda HDD の利用申請を検討する（大学との共同研究が前提）。CAN信号からの運転行動認識（車線変更・合流など）を前段タスクとして学習し、「行動と状況の不整合」を危険の予兆とする枠組みを検証する[12]。
4. 自社対象車種の信号カバレッジを調べる。panda または CANedge で実車のCANを記録し、opendbc対応の有無を確認する。非対応の場合は cabana / SavvyCAN と CAN-D・READ 型の自動抽出で、3.3節の「確実に取れる」区分の信号を揃える[21][23][30][31]。
5. 国内データの入手経路を確保する。東京農工大スマートモビリティ研究拠点とJARIに、ヒヤリハットDBのうち車両信号（車速・ブレーキ）部分の共同研究利用を打診する[36][36b]。

---

## 7. 参考文献リスト

データセット
- [1] commaai/comma2k19（GitHub）: https://github.com/commaai/comma2k19
- [2] comma2k19（Hugging Face データセットカード）: https://huggingface.co/datasets/commaai/comma2k19
- [2b] commaai/commaCarSegments（Hugging Face）: https://huggingface.co/datasets/commaai/commaCarSegments/commits/main/segments
- [3] HCRL Car-Hacking Dataset: https://sites.google.com/hksecurity.net/hcrl/Datasets/car-hacking-dataset
- [4] Verma ら「A Comprehensive Guide to CAN IDS Data & Introduction of the ROAD Dataset」arXiv:2012.14600（PLoS ONE 2024）: https://arxiv.org/abs/2012.14600
- [5] HCRL Survival Analysis Dataset for automobile IDS: https://sites.google.com/hksecurity.net/hcrl/Datasets/survival-ids
- [6b] HCRL Driving Dataset: https://sites.google.com/hksecurity.net/hcrl/Datasets/driving-dataset
- [6c] 「A Machine Learning Approach for Driver Identification Based on CAN-BUS Sensor Data」arXiv:2207.10807: https://arxiv.org/pdf/2207.10807
- [7] ROAD dataset（Zenodo）: https://zenodo.org/records/10462796
- [8] ETAS SynCAN（GitHub）: https://github.com/etas/SynCAN
- [9] Lampe & Meng「can-train-and-test: A Curated CAN Dataset for Automotive Intrusion Detection」arXiv:2308.04972: https://arxiv.org/abs/2308.04972 （データ: https://bitbucket.org/brooke-lampe/can-train-and-test/src/master/ ）
- [10] Dupont ら「Automotive Controller Area Network (CAN) Bus Intrusion Dataset v2」4TU.ResearchData: https://data.4tu.nl/datasets/efb320d8-c189-4e54-98af-3a79cc14f421
- [11] udacity/self-driving-car（GitHub、アーカイブ済み）: https://github.com/udacity/self-driving-car
- [11b] Udacity「Open Sourcing 223GB of Driving Data」: https://medium.com/udacity/open-sourcing-223gb-of-mountain-view-driving-data-f6b5593fbfa5
- [12] Honda Research Institute Driving Dataset（HDD）: https://usa.honda-ri.com/hdd ／ Ramanishka ら CVPR 2018 arXiv:1811.02307: https://arxiv.org/abs/1811.02307
- [13] nuScenes CAN bus expansion README: https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/can_bus/README.md
- [14] Geyer ら「A2D2: Audi Autonomous Driving Dataset」arXiv:2004.06320: https://arxiv.org/abs/2004.06320
- [15b] Oh, LeBlanc, Peng「Vehicle Energy Dataset (VED)」: https://github.com/gsoh/VED ／ arXiv:1905.02081: https://arxiv.org/abs/1905.02081
- [15c] Kidmose ら「A Critical Roadmap to Driver Authentication via CAN Bus ... KCID」arXiv:2510.25856: https://arxiv.org/abs/2510.25856
- [16] SHRP2 NDS InSight Data Access Website: https://insight.shrp2nds.us/
- [17] 「Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets」VTechWorks: https://vtechworks.lib.vt.edu/handle/10919/70850
- [18] National Academies Press（SHRP2 NDS 車両ネットワーク変数・Time Series Data Dictionary の記述）: https://nap.nationalacademies.org/read/22362/chapter/3
- [19] Dozza「SAFER100Car」VTTI NDRS abstract: https://www.vtti.vt.edu/PDFs/NDRS-abstracts/FINAL_Dozza_SAFER100Car.pdf
- [20b] CORDIS「Firsthand insight into drivers' natural behaviour」（UDRIVE）: https://cordis.europa.eu/article/id/117051-firsthand-insight-into-drivers-natural-behaviour
- [36] 東京農工大学 スマートモビリティ研究拠点: https://web.tuat.ac.jp/~nagaimu/kenkyu_smrc0.html
- [36b] JARI Safety research: https://jari.or.jp/en/research-content/safety ／ Uchida（VTTI NDRS発表資料）: https://vtti.whos.prod.es.cloud.vt.edu/PDFs/NDRS-presentations/Uchida.pdf

信号定義・リバースエンジニアリング
- [20] commaai/opendbc（GitHub）: https://github.com/commaai/opendbc
- [21] Marchetti & Stabili「READ: Reverse Engineering of Automotive Data Frames」IEEE TIFS 2019（著者版）: https://iris.unimore.it/handle/11380/1185929
- [22] Pesé ら「LibreCAN: Automated CAN Message Translator」ACM CCS 2019: https://par.nsf.gov/biblio/10200050-librecan-automated-can-message-translator
- [23] Verma ら「CAN-D: A Modular Four-Step Pipeline for Comprehensively Decoding Controller Area Network Data」arXiv:2006.05993: https://arxiv.org/abs/2006.05993v2
- [24] Wikipedia「OBD-II PIDs」: https://en.wikipedia.org/wiki/OBD-II_PIDs
- [25] CSS Electronics「OBD2 PID Overview」: https://www.csselectronics.com/pages/obd2-pid-table-on-board-diagnostics-j1979
- [26] CSS Electronics「J1939 Explained」: https://www.csselectronics.com/pages/j1939-explained-simple-intro-tutorial

ツール
- [27] python-can（Debian copyright、ライセンスのファイル別内訳）: https://sources.debian.org/src/python-can/4.6.1-4/debian/copyright ／ リポジトリ: https://github.com/hardbyte/python-can
- [28] cantools（GitHub）: https://github.com/cantools/cantools
- [29] asammdf（GitHub）: https://github.com/danielhrisca/asammdf
- [29b] asammdf（PyPI、LGPLv3+）: https://pypi.org/project/asammdf/
- [30] SavvyCAN（GitHub）: https://github.com/collin80/SavvyCAN
- [31] comma.ai blog「Open sourcing openpilot development tools」（cabana）: https://blog.comma.ai/open-sourcing-openpilot-development-tools/ ／ openpilot wiki cabana: https://github.com/commaai/openpilot/wiki/cabana/4db711b0f07db02cd0eea1debffa55577df43da5
- [32] commaai/panda（GitHub）: https://github.com/commaai/panda
- [33] linux-can/can-utils: https://github.com/linux-can/can-utils
- [34] CSS Electronics CANedge1: https://www.csselectronics.com/products/can-logger-sd-canedge1
- [35] Kvaser CANlib SDK: https://kvaser.com/developer/canlib-sdk ／ pycanlib: https://github.com/Kvaser/pycanlib
- [35b] Wikipedia「CANalyzer」: https://en.wikipedia.org/wiki/CANalyzer
- [35c] Vector「CANdb++ Editor ほかフリーウェア化」: https://www.vector.com/en/business-unit/testing-validation-diagnostics/resources/database-tools-ldf-explorer-candb-editor-fibex-exporer-available-freeware/

事故予防・運転者状態に関する研究（CAN相当信号の活用）
- [37] Osman ら「Crash and Near-Crash Prediction from Vehicle Kinematics Data: A SHRP2 Naturalistic Driving Study」TRB 2018: https://trid.trb.org/View/1496022
- [38] Khattak ら「Inferring safety critical events from vehicle kinematics in naturalistic driving environment」J. Intelligent Transportation Systems 2022: https://informahealthcare.com/doi/full/10.1080/15472450.2022.2048655
- [39] 操舵データによる眠気検知（Sensors 2019, PMC）: https://pmc.ncbi.nlm.nih.gov/articles/PMC6412352 ／ 操舵角のみで車線逸脱6秒前に分類（Traffic Injury Prevention）: https://informahealthcare.com/doi/full/10.1080/15389588.2019.1622005 ／ 車両ベース指標による多段階眠気分類（Expert Systems with Applications 2020）: https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_journals_2465481274

ソース件数: 参考文献リストの固有URLは計57件（文献番号は48項目）。うちデータセットは20種、論文は12本（READ、LibreCAN、CAN-D、ROAD、can-train-and-test、HDD、A2D2、VED、KCID、Osman、Khattak、眠気検知）。
