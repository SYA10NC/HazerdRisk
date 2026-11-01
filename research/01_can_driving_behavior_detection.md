# テーマ1: CANデータを用いた運転行動分析・危険運転検知手法の調査

- 調査日: 2026-11-01
- テーマのゴール: 「CANデータを用いた運転行動分析・危険運転（急加速・急ブレーキ・急ハンドル・ふらつき・無合図車線変更・過速度等）の検知手法」に関する論文・記事・公式発表を収集し、どの信号でどの手法を使い、どの程度の性能が出ているかを整理する。
- 前提: カメラ・LiDAR・ドライバーモニタ映像は使わず、CAN由来の信号のみで危険の予兆を検知・警告する。
- 表記ルール: ソースに書かれている事実はそのまま要約し、筆者の推察には「【推察】」を付ける。性能値はソースの記載どおりで、条件（データ規模・評価方法）が揃っていないため、数値同士を直接比べることはできない。

---

## 2. エグゼクティブサマリー

1. 急ブレーキ・急発進・急旋回の検知は、前後/横加速度とヨーレートに閾値を当てる方式が基本である。自然運転研究（NDS）では、急ブレーキ ≤ −0.45 g、急発進 ≥ 0.35 g、横 ≥ 0.50 g が代表値として使われる（Simons-Morton ら）。日本のヒヤリハットDBでも前後0.45Gがトリガに使われている。
2. ただし、固定閾値だけで事故・ニアミスを拾うと、感度も適合率も低い（VTTI, Perez ら 2017）。速度に応じて変える閾値（Chalmers）や個人別閾値（Papazikou ら）が提案されている。
3. 機械学習・深層学習による「運転者識別・運転スタイル分類」は、OCSLab（HCRL）データセット（10名・51信号・1 Hz）で精度95〜99%台が報告され、ほぼ飽和している。一方、データセットが小さく固定ルートで走っているため、汎化性には疑問が残る（Kidmose ら 2025）。
4. 危険運転（攻撃的運転）の分類も CAN（OBD-II）信号で可能であり、CNN-LSTM 系・グラフ畳み込みLSTM で精度94〜98%台が報告されている。ただし、多くは少人数・独自ラベルで評価されている。
5. 眠気・ふらつきはステアリング角だけでも推定でき、Honda・Mercedes-Benz は操舵ベースの注意力低下警報を量産している。研究レベルでは実路で精度約78%、誤検知率15〜29%（Li ら 2017）であり、誤報が大きな課題である。
6. 正常運転だけを学習する異常検知（One-class SVM、LSTM自己符号化器、ドライバモデル予測誤差）は「危険ラベルが少ない」問題への現実的な解であり、国内にも研究の蓄積がある（自動車技術会論文集の田中・坂東 2013、名古屋大学 武田研究室）。
7. 無合図車線変更・追い越しは、ステアリング角・ヨーレート・ウインカーの組合せで検知できる。CANだけを使った研究はまだ少なく、トラックの追い越し検知では TPR 86.5%・TNR 93% である（Volvo データ）。
8. 【推察】本プロジェクトでは、(a) 物理閾値ルールによるベースライン、(b) 正常運転モデルからの逸脱度、(c) レーダ ECU 由来の TTC/THW と ADAS 警報フラグを組み合わせた複合リスクスコアにするのが、ラベル不足と誤報の両方への妥当な対応と考える。

---

## 3. 主要知見（ソースごと）

### 3.1 閾値ベース・自然運転研究（NDS）

#### [S1] Trajectories of Kinematic Risky Driving Among Novice Teenagers
- 著者/組織: B. G. Simons-Morton, K. Cheon, F. Guo, P. Albert（NIH/NICHD, VTTI）
- 年: 2012年オンライン公開（Accident Analysis & Prevention, Vol.51, 2013）
- 種別: 論文（査読）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3556237
- 要点: 新規免許取得の10代42名を18か月計測した自然運転研究。高Gイベントの発生率から、運転者は高リスク群と低リスク群に分かれ、その傾向は時間が経っても安定していた。先行研究（Simons-Morton ら 2012）では、前月の高Gイベント率が翌月の事故・ニアミス発生を予測したと引用されている。
- 使用信号: 前後加速度、横加速度、ヨーレート（計測は加速度計・GPS・カメラ）
- 手法: 固定閾値によるイベント計数。急ブレーキ ≥ 0.45 g の減速、急発進 ≥ 0.35 g、左右旋回 ≥ 0.50 g、ヨーレート > 6 deg/s
- 性能指標: 本論文では事故予測の性能を直接評価していない（群分けの安定性を示している）
- 本プロジェクトへの示唆: CAN の加速度・ヨーレート信号で同じ閾値イベントをそのまま計算できる。単発イベントで即時に警告するより、イベント頻度を「運転者リスク指標」として使うほうが根拠を示しやすい。

#### [S2] Performance of basic kinematic thresholds in the identification of crash and near-crash events within naturalistic driving data
- 著者/組織: M. A. Perez, J. D. Sudweeks, E. Sears ほか（Virginia Tech Transportation Institute）
- 年: 2017（Accident Analysis and Prevention, 103:10-19）
- 種別: 論文（査読）。確認できたのは要旨を紹介するニュース記事
- URL: https://insurancenewsnet.com/oarticle/findings-on-risk-management-reported-by-investigators-at-virginia-tech-performance-of-basic-kinematic-thresholds-in-the-identification-of-crash-and
- 要点: SHRP 2 NDS とカナダ NDS を使い、運動学的閾値で事故・ニアミスを検出する性能を検証した。多くの手法は感度が「かなり低い」場合があるが、閾値を選び直すことで改善できる。複数手法の組合せ、統計/AI手法、検証の自動化を今後の方向として挙げている。
- 使用信号: 前後/横加速度、ヨーレート等の運動学的信号
- 手法: 固定閾値トリガ
- 性能指標: 閾値ごとの具体値は記事中になし（感度が低いという定性的な結論のみ）
- 本プロジェクトへの示唆: 「急ブレーキ＝危険」という単純な閾値だけでは、事故の予兆検知として不十分であることを示す重要な根拠になる。

#### [S3] Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets（VTTI タスクレポート）
- 著者/組織: VTTI
- 年: 2016
- 種別: 公式報告書
- URL: https://vtechworks.lib.vt.edu/bitstream/handle/10919/70850/SHRP_2_CrashNearCrashBaselineReport_4-25-16.pdf?sequence=1
- 要点（検索結果の抜粋による）: 約12種類のトリガアルゴリズムを 5,512,900 トリップに適用し、手作業の検証で事故 1,549 件・ニアミス 2,705 件を特定した。トリガだけでは通常走行と安全上重要な事象を見分けられず、映像レビューが必要だった。
- 使用信号: 車両運動学信号（加速度・ヨーレート等）
- 手法: 運動学トリガ＋映像による人手検証
- 性能指標: 上記の件数（トリガ単体の適合率は抜粋では確認できず）
- 本プロジェクトへの示唆: 【推察】CANだけで運用すると映像による検証ができないため、誤報の扱い（警告をどう段階化するか）を最初から設計しておく必要がある。

#### [S4] A probabilistic framework for identifying safety critical events in naturalistic driving time series data
- 著者/組織: E. Stemmler, J. Kovaceva, M. Dotzauer（Chalmers University of Technology）
- 年: 2017（6th International Naturalistic Driving Research Symposium）
- 種別: 論文（会議）
- URL: https://research.chalmers.se/publication/254471
- 要点: UDRIVE NDS の前後加速度と速度の同時確率密度をカーネル密度推定で求め、そのパーセンタイル曲線を「速度依存のトリガ閾値」とする。高速道路では減速度の閾値を下げる、といった状況に応じた閾値になる。
- 使用信号: 前後加速度、車速
- 手法: 同時確率密度に基づく動的閾値（多項式で近似）
- 性能指標: 定量結果の記載なし（固定閾値より誤報を減らせると見込んでいる）
- 本プロジェクトへの示唆: 車速で条件付けした閾値表を自社データから作るだけで実装でき、CANのみの構成と相性が良い。

#### [S5] Developing personalised braking and steering thresholds for driver support systems from SHRP2 NDS data
- 著者/組織: E. Papazikou, P. Thomas, M. Quddus（Loughborough University ほか）
- 年: 2019前後（Elsevier 系誌。受理稿がリポジトリで公開）
- 種別: 論文（査読）
- URL: https://repository.lboro.ac.uk/articles/journal_contribution/Developing_personalised_braking_and_steering_thresholds_for_driver_support_systems_from_SHRP2_NDS_data/16744156
- 要点: 安全上重要な事象の直前30秒について、減速度とヨーレートから制動・操舵の反応を抽出し、その順序を判定するアルゴリズムを作った。運転者の20%は迫る事象に反応していなかった。個人に合わせた起動閾値を提言している。
- 使用信号: 前後減速度、ヨーレート
- 手法: ルールベースのイベント抽出と個人別の閾値設定
- 性能指標: 反応なし20%（検知性能値は要旨になし）
- 本プロジェクトへの示唆: 「反応がない」こと自体（減速もヨー変化もない）が危険の兆候になる。後述の TTC と組み合わせ、「接近しているのに操作がない」状態を検出する設計が考えられる【推察】。

#### [S6] 日本大学生産工学部 学術講演会資料（ヒヤリハットデータベースを用いた分析）
- 著者/組織: 日本大学生産工学部
- 年: 不明（講演会 No.56）
- 種別: 論文（国内学術講演会）
- URL: https://www.cit.nihon-u.ac.jp/laboratorydata/kenkyu/kouennkai/reference/No.56/pdf/2-20.pdf
- 要点（検索結果の抜粋による。PDF本文はテキスト抽出できず）: ドライブレコーダは前後加速度 0.45G のトリガ条件を満たすと、前10秒・後5秒の計15秒を自動記録する。ヒヤリハットは「事故・高・中・低」の4レベルに分類される。
- 使用信号: 前後加速度（＋映像）
- 手法: 加速度閾値トリガ＋レベル分類
- 性能指標: 抜粋では確認できず
- 本プロジェクトへの示唆: 国内のヒヤリハットDBも米国NDSとほぼ同じ0.45Gでトリガをかけている。CANの前後加速度で同じトリガを再現すれば、既存DBの知見と対応づけやすい【推察】。

### 3.2 機械学習・深層学習による運転者識別/運転スタイル分類

#### [S7] HCRL（旧 OCSLab）Driving Dataset
- 著者/組織: 高麗大学 Hacking and Countermeasure Research Lab（B. I. Kwak, H. K. Kim）
- 年: 2016公開
- 種別: データセット
- URL: https://sites.google.com/hksecurity.net/hcrl/Datasets/driving-dataset
- 要点: 10名（A〜J）が KIA Soul で高麗大学とソウル・ワールドカップ競技場の間を往復した。約23時間・1往復約46 km、1 Hz、OBD-II 経由の車載センサ値51項目。用途は運転者分類・個人化・盗難検知。
- 使用信号: エンジン回転数、車速、アクセル開度、各輪速、エンジントルク、燃料トリム、変速機油温など51項目
- 手法: なし（データセット）
- 性能指標: なし
- 本プロジェクトへの示唆: 公開ベンチマークとして手法の再現に使える。ただし危険ラベルがなく、サンプリングが1 Hz と粗いため、急操作の検知には不向きである【推察】。

#### [S8] Know Your Master: Driver Profiling-based Anti-theft Method
- 著者/組織: B. I. Kwak, J. Woo, H. K. Kim（高麗大学）
- 年: 2016（PST 2016）、arXiv 2017
- 種別: 論文（査読会議）/プレプリント
- URL: https://arxiv.org/abs/1704.05223 （本文: https://ar5iv.labs.arxiv.org/html/1704.05223 ）
- 要点: [S7] のデータで運転者を認証する。51特徴から15特徴を選択し、平均・中央値・標準偏差の統計特徴を追加した。60秒窓を速度と精度の妥協点として採用した（120秒窓のほうが高精度だが検知が遅れる）。
- 使用信号: 長期燃料トリム、変速機油温、摩擦トルク、吸気圧、エンジントルク、アクセルペダル値、各輪速など
- 手法: Decision Tree, Random Forest, KNN, MLP
- 性能指標: Random Forest で精度 約0.993〜0.998（道路種別ごと）。統計特徴を加えると 0.961 → 0.996
- 本プロジェクトへの示唆: 上位の特徴が燃料トリムや油温といった「車両状態」であり、運転者ではなく走行条件・車両を識別している可能性がある。危険運転検知に応用する際は特徴選択に注意が必要である【推察】。

#### [S9] A Deep Learning Framework for Driving Behavior Identification on In-Vehicle CAN-BUS Sensor Data
- 著者/組織: J. Zhang, Z. Wu, F. Li ほか（中国科学院、中国科学技術大学）
- 年: 2019（Sensors 19(6):1356）
- 種別: 論文（査読）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6471704/
- 要点: CNN＋GRU/LSTM＋Attention で、多チャネルCAN時系列から運転者（運転行動）を識別する。手作業の特徴選択をせず、51信号すべてを入力する。
- 使用信号: [S7] の51信号（ステアリング、車速、エンジン回転数、ブレーキ位置など）
- 手法: DeepConvGRU-Attention / DeepConvLSTM-Attention（窓長60）
- 性能指標: 精度 0.970〜0.984、F1 0.970〜0.984（GRU版）。15特徴の LSTM ベースラインも同程度（0.977〜0.993）
- 本プロジェクトへの示唆: 深層学習で特徴量設計を省けるが、手作業の特徴量でも同等の性能が出ている。小規模データでは解釈しやすい特徴量方式が有利である。

#### [S10] Lightweight Driver Behavior Identification Model with Sparse Learning on In-Vehicle CAN-BUS Sensor Data
- 著者/組織: S. Ullah, D.-H. Kim（仁荷大学）
- 年: 2020（Sensors 20(18):5030）
- 種別: 論文（査読）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7570946/
- 要点: Depthwise 畳み込み＋GRU/LSTM の軽量モデル。全結合層の強いノードを凍結して新クラスを追加学習する（スパース学習）。
- 使用信号: [S7] から選んだ15信号（輪速、エンジントルク、アクセル開度、冷却水温など）
- 手法: DepthConv-GRU / DepthConv-LSTM
- 性能指標: 10クラスで精度 98.72%（GRU）。モデルサイズ 1.69 MB（DeepConvGRU-Attention の 7.91 MB より約79%小さい）
- 本プロジェクトへの示唆: 車載ECUやエッジ機器に実装できるサイズでも高い精度が出る事例である。

#### [S11] Automatic Driver Identification from In-Vehicle Network Logs
- 著者/組織: M. Remeli, S. Lestyan, G. Acs, G. Biczok（ブダペスト工科経済大学）
- 年: 2019（arXiv）
- 種別: プレプリント
- URL: https://arxiv.org/abs/1911.09508
- 要点: DBC がなくても（CANプロトコルを解析しなくても）、生の CAN ログから運転者を再識別できる。
- 使用信号: 生CANログ（復号した車速・ブレーキ・操舵角には依存しない）
- 手法: 既製の機械学習手法
- 性能指標: 33名で精度 75〜85%
- 本プロジェクトへの示唆: DBC が手に入らない車種でも、生CANから信号を自動抽出して特徴を作れる可能性がある。

#### [S12] A Machine Learning Approach for Driver Identification Based on CAN-BUS Sensor Data
- 著者/組織: Md. A. A. Khan ほか
- 年: 2022（arXiv）
- 種別: プレプリント
- URL: https://arxiv.org/abs/2207.10807
- 要点: OBD-II（SAE J1979）経由の CAN データ（10名セットと2名セット）で、教師あり学習により運転者を検証する。人数が少ないほど精度が高い。
- 使用信号: OBD-II PID 群（要旨では具体名なし）
- 手法: 教師あり学習（検索結果の抜粋では、2値識別で Naive Bayes の精度 96.15% と記載）
- 性能指標: 上記
- 本プロジェクトへの示唆: OBD-II だけでも運転特性を捉えられるが、識別人数が増えると性能が落ちる。

#### [S13] Driving Behavior Analysis through CAN Bus Data in an Uncontrolled Environment
- 著者/組織: U. Fugiglando, E. Massaro, P. Santi ほか（MIT Senseable City Lab, Volkswagen）
- 年: 2017（arXiv。のち IEEE T-ITS 掲載）
- 種別: プレプリント
- URL: https://arxiv.org/abs/1710.04133
- 要点: 64名・10台・2,000トリップ以上を、運転指示なしの非統制環境で収集した。教師なしクラスタリングで運転者をグループ化し、頑健なクラスタリングに必要な最小データ量も求めた。
- 使用信号: アクセルペダル位置、ブレーキ圧、操舵角、操舵角速度（モーメンタム）、車速、エンジン回転数、前後/横加速度
- 手法: 教師なしクラスタリング＋頑健性検証
- 性能指標: 要旨に定量値なし
- 本プロジェクトへの示唆: 本プロジェクトの想定信号とほぼ一致する信号セットで、実環境の運転スタイル分類が成立している。

#### [S14] Scene-insensitive driving style recognition using CAN signals
- 著者/組織: Zhang ら（北京理工大学）
- 年: 2023（IEEE）
- 種別: 論文（査読）。確認できたのは書誌情報と検索結果の抜粋
- URL: https://pure.bit.edu.cn/zh/publications/scene-insensitive-driving-style-recognition-using-can-signals-bas/
- 要点（抜粋による）: 因子分析で走行シーンに依存しない共通特徴を抽出し、K-means で運転スタイルを分類した。100名のデータを運転スタイル質問紙と照合した。
- 使用信号: CAN 信号（詳細は未確認）
- 手法: 因子分析＋K-means
- 性能指標: 未確認
- 本プロジェクトへの示唆: 道路種別や交通状況の違いを特徴量の段階で吸収するという考え方は、地図・カメラを使えない本プロジェクトで重要である。

#### [S15] A Critical Roadmap to Driver Authentication via CAN Bus: Dataset Review, Introduction of the Kidmose CANid Dataset (KCID), and Proof of Concept
- 著者/組織: B. E. Kidmose, A. B. Kidmose, C. C. Zou（DTU, UCF）
- 年: 2025（arXiv）
- 種別: プレプリント/データセット
- URL: https://arxiv.org/abs/2510.25856
- 要点: 既存の公開データセットの限界として、(1) 生CANではなく復号済み診断データであること、(2) 人工的な固定ルート、(3) サンプリングレート不足、(4) 属性情報の欠如、を指摘した。生CANで16名・4車両の KCID（日常運転＋固定ルート）を公開し、単一ボードコンピュータで実車の路上試験を行った。
- 使用信号: 生CAN
- 手法: 運転者認証のプロトタイプ
- 性能指標: 要旨に定量値なし
- 本プロジェクトへの示唆: OCSLab の高精度は条件が整った実験での値であり、実運用での精度は割り引いて見る必要がある。生CAN・高サンプリングのデータを自社で取得する意義が大きい。

### 3.3 危険運転（攻撃的運転）の分類

#### [S16] Data Fusion for Driver Behaviour Analysis
- 著者/組織: J. Carmona, F. García, D. Martín, A. de la Escalera, J. M. Armingol（マドリード・カルロス3世大学）
- 年: 2015（Sensors 15(10):25968）
- 種別: 論文（査読）
- URL: https://www2.mdpi.com/1424-8220/15/10/25968
- 要点: IVVI 2.0 プラットフォームで CAN-BUS に GPS/IMU を融合し、攻撃的運転をリアルタイムで検出する。時間領域と周波数領域の両方の特徴を使い、市街地・郊外・高速道路で試験した。GPS からは制限速度などの文脈を得る。
- 使用信号: ブレーキ、スロットル、エンジン回転数、車速（CAN）＋GPS/IMU
- 手法: 時間・周波数特徴量によるルール/分類（後継論文はエキスパートシステム）
- 性能指標: 抜粋では確認できず
- 本プロジェクトへの示唆: 過速度判定には制限速度の情報が必要であり、CANのみでは原理的に難しい（地図・標識認識が必要）。ただし ADAS ECU が標識認識結果を CAN に流していれば代替できる【推察】。

#### [S17] Performance Evaluation of Major Classification Algorithms for Aggressive Driving Detection using CAN-bus Data
- 著者/組織: B. Karabuluter, Ö. Karaduman, M. Karabatak, H. Eren（イノニュ大学ほか）
- 年: 2020（European Journal of Science and Technology, No.20, pp.774-782）
- 種別: 論文（査読）
- URL: https://dergipark.org.tr/en/pub/ejosat/article/743076
- 要点: OBD-II から取得した CAN データに、統制走行で「攻撃的/穏やか」のラベルを付け、ANN・SVM・KNN・C4.5・Naive Bayes を比較した。Naive Bayes が最良だった。
- 使用信号: OBD-II 経由の CAN 信号
- 手法: 教師あり分類の比較
- 性能指標: 最良は Naive Bayes（精度の数値は抜粋では未確認）
- 本プロジェクトへの示唆: 少量データでは単純なモデルが勝つこともあり、ベースラインとして複数の古典手法を比べる価値がある。

#### [S18] An Efficient Deep Learning Model Based on Driver Behaviour Detection Within CAN-BUS Signals
- 著者/組織: H. M. Gheni, L. A. Abdul-Rahaim
- 年: 2024（Revue d'Intelligence Artificielle, 38(1):53-62, IIETA）
- 種別: 論文（査読）
- URL: https://iieta.org/node/16481
- 要点: 4名の男性ドライバーが固定の市街地ルートを走った独自データ（1 Hz）を使う。スライディング窓の FCN-LSTM で安全/危険運転を分類し、ANN・LSTM・1D-CNN と比べた。
- 使用信号: アクセル開度、スロットル位置、回転数、車速（OBD-II）。ほかに IMU のヨー角、GPS
- 手法: FCN-LSTM
- 性能指標: 窓設定により精度約94〜99%（最高 99.01%）
- 本プロジェクトへの示唆: 被験者4名・固定ルートなので、汎化性能の根拠としては弱い。

#### [S19] Enhancing Road Safety through Accurate Detection of Hazardous Driving Behaviors with Graph Convolutional Recurrent Networks
- 著者/組織: P. Khosravinia, T. Perumal, J. Zarrin
- 年: 2023（arXiv。IEEE Access 2023）
- 種別: 論文（査読）/プレプリント
- URL: https://arxiv.org/abs/2305.05670
- 要点: CAN の公開センサとベンダー固有の非公開センサを使い、グラフ畳み込み LSTM（GConvLSTM）で危険運転を検出する。Raspberry Pi 上のエッジ推論で動かした。
- 使用信号: CAN-bus センサ（公開/非公開）
- 手法: GConvLSTM（信号間の関係をグラフとして扱う）
- 性能指標: 精度 97.5%（公開センサ）、98.1%（非公開センサ平均）
- 本プロジェクトへの示唆: メーカー固有信号（DBC で復号したもの）を加えると精度が上がる。純正 CAN への深いアクセスが有利になる。

#### [S20] Overtake Detection in Trucks Using CAN Bus Signals: A Comparative Study of Machine Learning Methods
- 著者/組織: F. Alonso-Fernandez, T. H. Butt, P. Tiwari（ハルムスタッド大学, Volvo Group データ）
- 年: 2025（arXiv。ESWA 投稿中）
- 種別: プレプリント
- URL: https://arxiv.org/abs/2507.00593
- 要点: 実運用中のトラック5台の CAN ログで、追い越し（車線変更を含む操作）を検出する。ANN・RF・SVM を比べ、スコアレベル融合が最良だった。関連研究として、ステアリング信号のスペクトログラムで車線維持と車線変更を分離した研究を挙げ、CAN を使った深層学習の車線変更研究は少ないと指摘している。
- 使用信号: CAN 信号（要旨では具体名なし）
- 手法: ANN / Random Forest / SVM、スコア融合
- 性能指標: TPR 86.5%、TNR 93%（融合時）
- 本プロジェクトへの示唆: 「車線変更を検出し、ウインカーがOFFなら無合図車線変更」という2段構成が実現可能な範囲にある【推察】。

### 3.4 異常検知（正常運転モデルからの逸脱）

#### [S21] 車両挙動データを用いたドライバ異常状態検出（Anomaly Driver State Detection from Vehicle Behavior Data）
- 著者/組織: 田中 悠介, 坂東 誉司（所属は未確認）
- 年: 2013（自動車技術会論文集 Vol.44, No.2）
- 種別: 論文（査読）
- URL: https://www.jstage.jst.go.jp/article/jsaeronbun/44/2/44_20134240/_article/-char/en
- 要点: CAN から得た自車加速度と先行車との相対速度の関係を One-class SVM でモデル化する。正常運転だけで学習するため、異常運転データを集める必要がない。高速道路と一般道で評価し、推定した異常度は主観評価と相関した。
- 使用信号: 加速度、先行車相対速度（CAN）
- 手法: One-class SVM
- 性能指標: 主観評価との相関（要旨に数値なし）
- 本プロジェクトへの示唆: レーダ ECU の相対速度が CAN にあれば、そのまま適用できる日本の先行事例である。

#### [S22] Deep Multi-Task Learning for Anomalous Driving Detection Using CAN Bus Scalar Sensor Data
- 著者/組織: V. Sadhu, T. Misu, D. Pompili（ラトガース大学, Honda Research Institute USA）
- 年: 2019（IROS 2019, arXiv）
- 種別: 論文（査読会議）/プレプリント
- URL: https://arxiv.org/abs/1907.00749
- 要点: 150時間の実走 CAN データで、右左折・直進・Uターンなどの操作ラベルを補助タスクとするマルチタスク学習により、半教師ありで異常運転を検出する。操作の種類による正常データの偏りに対処し、異常スコアは上位0.01%などを順位づけて分析する。
- 使用信号: CAN スカラー信号（要旨では具体名なし）
- 手法: マルチタスク深層学習（LSTM 自己符号化器系）
- 性能指標: ベースラインより改善（要旨に数値なし）
- 本プロジェクトへの示唆: 異常度を「走行状況（操作の種類）で条件付け」すると誤報が減るという知見は、CANのみの異常検知設計で重要である。

#### [S23] 総務省 SCOPE 成果発表資料（名古屋大学 武田ら: ドライバモデルによる危険状況検出）
- 著者/組織: 名古屋大学（武田一哉 研究室）
- 年: 2011（平成23年度 SCOPE 成果発表会）
- 種別: 公式発表（研究成果資料）
- URL: https://www.soumu.go.jp/main_sosiki/joho_tsusin/scope/event/h23yokousyu/B1-2(pre).pdf
- 要点（検索結果の抜粋による。PDF本文はテキスト抽出できず）: 通常運転で学習した動的ドライバモデルの予測値と実測値の差から、通常からの逸脱を評価する。
- 使用信号: ペダル操作・車速等の運転行動信号（詳細は未確認）
- 手法: 動的ドライバモデルの予測誤差による異常検出
- 性能指標: 誤検出率約23%で潜在的な危険状況の約80%を検出
- 本プロジェクトへの示唆: CANのみの「予兆検知」に最も近い国内の先行例である。誤検出率23%は警告用途としては高く、段階的な警告や個人別の適応が必要になる【推察】。

#### [S24] 科研費 成果報告書 24500200（運転信号の記録と個人性の分析）
- 著者/組織: 名古屋大学（武田ら）
- 年: 2012〜2014年度頃
- 種別: 公式報告書（KAKEN）
- URL: https://kaken.nii.ac.jp/ja/file/KAKENHI-PROJECT-24500200/24500200seika.pdf
- 要点（検索結果の抜粋による）: HV・EV を含む7車種で15名の運転データ（ペダル操作量、車速、3軸加速度）を記録した。アクセル操作の時系列には、車種が変わってもドライバーごとに一貫した癖があった。
- 使用信号: アクセル/ブレーキペダル操作量、車速、加速度
- 手法: 時系列パターン分析
- 性能指標: 未確認
- 本プロジェクトへの示唆: ペダル操作の個人性が車種をまたいで保たれるなら、個人ベースラインからの逸脱で危険を検知する方式が成り立つ。

### 3.5 ステアリングのみによる眠気・ふらつき・車線逸脱推定

#### [S25] Online Detection of Driver Fatigue Using Steering Wheel Angles for Real Driving Conditions
- 著者/組織: Z. Li, S. E. Li, R. Li, B. Cheng, J. Shi（清華大学ほか）
- 年: 2017（Sensors 17(3):495）
- 種別: 論文（査読）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5375781/
- 要点: 6名・約14.68時間の実路データで、操舵角の近似エントロピー（ApEn）をスライディング窓で計算し、適応的な区分線形近似で特徴化した。オンラインで学習した「覚醒時参照系列」との DTW 距離を閾値0.31で判定する。ラベルは顔映像を使った専門家の評価（1分単位）。
- 使用信号: 操舵角のみ
- 手法: ApEn＋DTW 距離の閾値判定
- 性能指標: 精度 78.01%、覚醒状態の誤検出 29.35%、眠気状態の誤検出 15.15%
- 本プロジェクトへの示唆: 操舵角だけで実路の眠気検知が成立することを示す査読論文である。誤報率が実用上の壁になる。

#### [S26] Steering in a Random Forest: Ensemble Learning for Detecting Drowsiness-Related Lane Departures
- 著者/組織: A. D. McDonald, J. D. Lee, C. Schwarz, T. L. Brown（ウィスコンシン大学, アイオワ大学 NADS）
- 年: 2014（Human Factors 56(5):986-998）
- 種別: 論文（査読）
- URL: https://iro.uiowa.edu/esploro/outputs/journalArticle/Steering-in-a-Random-Forest-Ensemble/9984627327502771
- 要点: 72名のドライビングシミュレータ（NADS）データで、操舵角から眠気に関連する車線逸脱を Random Forest で検出した。カメラ指標の PERCLOS より精度・AUC が高く、陽性的中率は同程度だった。2012年の会議版では、眠気による車線逸脱を約6秒前に予測できると報告している（検索結果の抜粋による）。
- 使用信号: 操舵角のみ
- 手法: Random Forest
- 性能指標: PERCLOS より高い精度・AUC（要旨に数値なし）
- 本プロジェクトへの示唆: 車線を観測しなくても操舵だけで「逸脱の数秒前」を予測できる可能性を示しており、予兆検知に直結する。ただしシミュレータでの結果である。

#### [S27] Method and apparatus for determining workload of motor vehicle driver（ステアリングエントロピー特許）
- 著者/組織: US Patent 6,061,610（E. R. Boer ほか、Nissan 系）
- 年: 2000
- 種別: 公式文書（特許）
- URL: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6061610
- 要点（検索結果の抜粋による）: 操舵角の予測誤差の分布（ステアリングエントロピー）で運転負荷を推定する。眠気は長時間にわたる異常に低い予測誤差として現れる。必要なのは操舵角センサのみ。
- 使用信号: 操舵角
- 手法: 操舵角の予測誤差のエントロピー
- 性能指標: なし（特許）
- 本プロジェクトへの示唆: 計算が軽く、CAN の操舵角だけで実装できる古典的な特徴量である。

#### [S28] Honda ドライバー注意力モニター（公式技術解説）
- 著者/組織: 本田技研工業
- 年: 公開中（2026-11-01 確認）
- 種別: 公式発表
- URL: https://global.honda/jp/tech/Driver_Attention_Monitor/
- 要点: ステアリング操作のふらつきから、疲労・眠気による注意力レベルを間接的に推定し、4段階で表示する。レベル2・1で段階的に休憩を促す。実際の走行環境での誤検知低減を重視した。取扱説明書では、30分未満の運転では警告しないとしている（検索結果の抜粋による）。
- 使用信号: ステアリング操作（操舵角）
- 手法: 非公開
- 性能指標: 非公開
- 本プロジェクトへの示唆: 操舵のみによる注意力推定は量産車で実用化されている。「長時間かけて個人ベースラインを作る」「段階的に警告する」が実用化の型である。

#### [S29] Mercedes-Benz ATTENTION ASSIST（報道記事）
- 著者/組織: Mercedes-Benz（報道: Automotive Fleet ほか）
- 年: 2009前後
- 種別: 記事
- URL: https://www.automotive-fleet.com/65213/mercedes-benz-monitors-how-you-drive ／ https://www.auto123.com/en/news/mercedes-benzs-attention-assist-system/41639
- 要点: 高感度の操舵角センサで細かい修正操舵のパターンを監視し、約70（記事によっては72）のパラメータで、走り始めの約20分間に運転者プロファイルを作る。眠気パターンを検知するとコーヒーカップのアイコンと警告音を出す。80 km/h 以上でのみ作動するという記述もある。
- 使用信号: 操舵角・操舵速度、車速ほか
- 手法: 個人ベースライン＋逸脱検知（詳細は非公開）
- 性能指標: 非公開
- 本プロジェクトへの示唆: 「最初の一定時間で個人ベースラインを作り、そこからの逸脱を見る」「高速域に限定して誤報を減らす」という設計の参考になる。

---

## 4. CANのみで使える信号・特徴量の一覧

- 前後加速度（Gx）: 急ブレーキ（≤ −0.45 g）・急発進（≥ 0.35 g）のイベント数と頻度 [S1][S6]。速度で条件付けした動的閾値 [S4]。事象前の減速反応の有無 [S5]
- 横加速度（Gy）・ヨーレート: 急旋回（|Gy| ≥ 0.50 g）、ヨーレート > 6 deg/s の修正操舵 [S1]、事象前の操舵反応 [S5]
- 操舵角・操舵角速度:
  - 近似エントロピー（ApEn）[S25]、ステアリングエントロピー（予測誤差分布）[S27]
  - 修正操舵の頻度・パターン（量産システム）[S28][S29]
  - 統計・時系列特徴を Random Forest に入力し、車線逸脱を予測 [S26]
  - スペクトログラムで車線変更と車線維持を分離 [S20]
  - 操舵角・操舵モーメンタムによる運転スタイルのクラスタリング [S13]
- アクセル開度・スロットル位置: 運転者識別・攻撃的運転分類の主要入力 [S8][S10][S18]。ペダル操作の個人性 [S24]
- ブレーキ圧/ブレーキペダル位置: 運転スタイル分類 [S13]、攻撃的運転検出 [S16]
- 車速: 全手法の基本入力、動的閾値の条件変数 [S4]。過速度判定には制限速度情報が別途必要 [S16]
- エンジン回転数・エンジントルク: 運転スタイル・攻撃的運転分類 [S9][S16][S18]
- 先行車相対速度・車間距離（レーダ ECU）: One-class SVM による異常度 [S21]。TTC/THW はリスク指標として一般的（本調査では CAN 経由の具体例は [S21] のみ確認）
- ウインカー: 【推察】車線変更検知 [S20] と組み合わせて無合図車線変更を判定する（CAN のみで行った直接の研究は今回見つからず）
- 車両状態系（燃料トリム、油温、冷却水温など）: 運転者識別では上位特徴だが、危険運転とは因果関係が薄い [S8][S10]。【推察】危険検知では交絡要因として除外を検討する
- 生CANフレーム（DBC 未復号）: 運転者識別に使える（75〜85%）[S11]
- 派生特徴: 窓ごとの平均・中央値・標準偏差 [S8]、ジャーク・周波数特徴 [S16]、深層学習による自動抽出 [S9][S19]

---

## 5. 課題・ギャップ

1. 固定閾値は感度・適合率ともに低い: NDS でも運動学トリガだけでは事故・ニアミスを見分けられず、映像による人手検証に頼っている [S2][S3]。CANのみの構成では映像による確認ができないため、誤報の管理がより難しくなる。
2. 危険ラベルが少なく偏っている: 事故・ニアミスは稀な事象である。公開CANデータセット（OCSLab 等）には危険ラベルがない [S7][S15]。攻撃的運転の研究は統制走行の自己申告ラベルが多い [S17][S18]。
3. データセットの限界: 1 Hz・復号済み OBD-II・固定ルート・少人数（4〜10名）が主流である [S7][S15][S18]。急操作は1秒未満の現象なので、1 Hz では捉えきれない【推察】。
4. 誤報率の高さ: 操舵ベースの眠気検知は実路で誤検出15〜29% [S25]、ドライバモデル逸脱検知は誤検出約23% [S23]。量産車は30分以上の運転・80 km/h 以上などの条件を付けて誤報を抑えている [S28][S29]。
5. 文脈情報の欠落: 制限速度・道路形状・車線位置・周辺交通は CAN だけでは基本的に分からない。過速度判定 [S16] や「カーブでの正常な操舵」と「ふらつき」の区別が難しい。走行シーンへの依存を除く工夫が要る [S14][S22]。
6. 車種間の差: CAN ID・信号のスケールは車種ごとに異なり、DBC が必要である。生CANから直接扱う手法 [S11] はまだ識別タスクにとどまる。
7. 無合図車線変更: CAN だけで車線変更を検出した研究は少なく [S20]、乗用車での性能値はほとんど見つからなかった。緩いカーブと車線変更の見分けが難しい。
8. 報告精度の比較可能性: 95〜99%台の精度の多くは同一被験者・同一ルート内での評価であり、未知の運転者・未知の道路への汎化は検証が不十分である [S15]。【推察】論文の数値をそのまま目標値にしない方がよい。

---

## 6. 次のアクション提案

1. 閾値ルールのベースライン実装: [S1] の閾値（−0.45 g / 0.35 g / 0.50 g / 6 deg/s）と [S4] の速度依存閾値を自社 CAN データに当て、イベント発生率の分布を可視化する。まず「1,000 km あたりのイベント数」を運転者リスク指標として算出する。
2. 正常運転モデルによる異常検知のPoC: [S21] の One-class SVM（加速度×相対速度）と [S22] の考え方（操作種別で条件付けした自己符号化器）で、逸脱度スコアを作る。PCS/LDA 等の ADAS 警報フラグや急ブレーキイベントを「弱いラベル」として、予兆の先行時間（何秒前に上昇するか）を評価する。
3. 操舵ベースのふらつき指標: ApEn [S25] とステアリングエントロピー [S27] を、高速・直線区間（車速と |ヨーレート| が小さい区間）に限って計算する。LDA 警報フラグとの相関を検証する（LDA を擬似的な正解とする）【推察】。
4. 無合図車線変更検知: 操舵角とヨーレートから車線変更候補を抽出し（スペクトログラム/RF、[S20]）、ウインカーの状態と照合するルールを試作する。LDA ECU が CAN に車線情報を流していれば、正解データとして使う。
5. データ取得仕様の見直し: [S15] の指摘を踏まえ、生CANを 10〜100 Hz 程度で記録し、運転者ID・車種・日常運転を含めた記録を設計する。公開データ（HCRL [S7]、KCID [S15]）は手法の再現用ベンチマークとして併用する。

---

## 7. 参考文献リスト

| ID | 文献 | 種別 | URL |
|---|---|---|---|
| S1 | Simons-Morton B.G. et al., "Trajectories of Kinematic Risky Driving Among Novice Teenagers," Accid. Anal. Prev., 2012/2013 | 論文 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3556237 |
| S2 | Perez M.A. et al., "Performance of basic kinematic thresholds in the identification of crash and near-crash events within naturalistic driving data," Accid. Anal. Prev. 103, 2017（要旨紹介記事） | 論文 | https://insurancenewsnet.com/oarticle/findings-on-risk-management-reported-by-investigators-at-virginia-tech-performance-of-basic-kinematic-thresholds-in-the-identification-of-crash-and |
| S3 | VTTI, "Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets," 2016 | 公式報告書 | https://vtechworks.lib.vt.edu/bitstream/handle/10919/70850/SHRP_2_CrashNearCrashBaselineReport_4-25-16.pdf?sequence=1 |
| S4 | Stemmler E., Kovaceva J., Dotzauer M., "A probabilistic framework for identifying safety critical events in naturalistic driving time series data," NDRS 2017 | 論文（会議） | https://research.chalmers.se/publication/254471 |
| S5 | Papazikou E., Thomas P., Quddus M., "Developing personalised braking and steering thresholds for driver support systems from SHRP2 NDS data" | 論文 | https://repository.lboro.ac.uk/articles/journal_contribution/Developing_personalised_braking_and_steering_thresholds_for_driver_support_systems_from_SHRP2_NDS_data/16744156 |
| S6 | 日本大学生産工学部 学術講演会 No.56 資料 2-20（ヒヤリハットDB、0.45G トリガ） | 論文（国内講演） | https://www.cit.nihon-u.ac.jp/laboratorydata/kenkyu/kouennkai/reference/No.56/pdf/2-20.pdf |
| S7 | HCRL (Korea Univ.), Driving Dataset（旧 OCSLab） | データセット | https://sites.google.com/hksecurity.net/hcrl/Datasets/driving-dataset |
| S8 | Kwak B.I., Woo J., Kim H.K., "Know Your Master: Driver Profiling-based Anti-theft Method," PST 2016 / arXiv:1704.05223 | 論文/プレプリント | https://arxiv.org/abs/1704.05223 |
| S9 | Zhang J. et al., "A Deep Learning Framework for Driving Behavior Identification on In-Vehicle CAN-BUS Sensor Data," Sensors 19(6):1356, 2019 | 論文 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6471704/ |
| S10 | Ullah S., Kim D.-H., "Lightweight Driver Behavior Identification Model with Sparse Learning on In-Vehicle CAN-BUS Sensor Data," Sensors 20(18):5030, 2020 | 論文 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7570946/ |
| S11 | Remeli M. et al., "Automatic Driver Identification from In-Vehicle Network Logs," arXiv:1911.09508, 2019 | プレプリント | https://arxiv.org/abs/1911.09508 |
| S12 | Khan M.A.A. et al., "A Machine Learning Approach for Driver Identification Based on CAN-BUS Sensor Data," arXiv:2207.10807, 2022 | プレプリント | https://arxiv.org/abs/2207.10807 |
| S13 | Fugiglando U. et al., "Driving Behavior Analysis through CAN Bus Data in an Uncontrolled Environment," arXiv:1710.04133, 2017 | プレプリント | https://arxiv.org/abs/1710.04133 |
| S14 | Zhang et al., "Scene-insensitive driving style recognition using CAN signals ...," IEEE, 2023（北京理工大学 書誌） | 論文 | https://pure.bit.edu.cn/zh/publications/scene-insensitive-driving-style-recognition-using-can-signals-bas/ |
| S15 | Kidmose B.E., Kidmose A.B., Zou C.C., "A Critical Roadmap to Driver Authentication via CAN Bus ... (KCID) ...," arXiv:2510.25856, 2025 | プレプリント/データセット | https://arxiv.org/abs/2510.25856 |
| S16 | Carmona J. et al., "Data Fusion for Driver Behaviour Analysis," Sensors 15(10):25968, 2015 | 論文 | https://www2.mdpi.com/1424-8220/15/10/25968 |
| S17 | Karabuluter B. et al., "Performance Evaluation of Major Classification Algorithms for Aggressive Driving Detection using CAN-bus Data," EJOSAT No.20, 2020 | 論文 | https://dergipark.org.tr/en/pub/ejosat/article/743076 |
| S18 | Gheni H.M., Abdul-Rahaim L.A., "An Efficient Deep Learning Model Based on Driver Behaviour Detection Within CAN-BUS Signals," RIA 38(1), 2024 | 論文 | https://iieta.org/node/16481 |
| S19 | Khosravinia P., Perumal T., Zarrin J., "Enhancing Road Safety through Accurate Detection of Hazardous Driving Behaviors with Graph Convolutional Recurrent Networks," IEEE Access / arXiv:2305.05670, 2023 | 論文/プレプリント | https://arxiv.org/abs/2305.05670 |
| S20 | Alonso-Fernandez F., Butt T.H., Tiwari P., "Overtake Detection in Trucks Using CAN Bus Signals," arXiv:2507.00593, 2025 | プレプリント | https://arxiv.org/abs/2507.00593 |
| S21 | 田中悠介, 坂東誉司, 「車両挙動データを用いたドライバ異常状態検出」, 自動車技術会論文集 44(2), 2013 | 論文 | https://www.jstage.jst.go.jp/article/jsaeronbun/44/2/44_20134240/_article/-char/en |
| S22 | Sadhu V., Misu T., Pompili D., "Deep Multi-Task Learning for Anomalous Driving Detection Using CAN Bus Scalar Sensor Data," IROS 2019 / arXiv:1907.00749 | 論文/プレプリント | https://arxiv.org/abs/1907.00749 |
| S23 | 総務省 SCOPE 平成23年度 成果発表資料 B1-2（名古屋大学） | 公式発表 | https://www.soumu.go.jp/main_sosiki/joho_tsusin/scope/event/h23yokousyu/B1-2(pre).pdf |
| S24 | 科研費 24500200 研究成果報告書（名古屋大学） | 公式報告書 | https://kaken.nii.ac.jp/ja/file/KAKENHI-PROJECT-24500200/24500200seika.pdf |
| S25 | Li Z. et al., "Online Detection of Driver Fatigue Using Steering Wheel Angles for Real Driving Conditions," Sensors 17(3):495, 2017 | 論文 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5375781/ |
| S26 | McDonald A.D. et al., "Steering in a Random Forest: Ensemble Learning for Detecting Drowsiness-Related Lane Departures," Human Factors 56(5), 2014 | 論文 | https://iro.uiowa.edu/esploro/outputs/journalArticle/Steering-in-a-Random-Forest-Ensemble/9984627327502771 |
| S27 | US Patent 6,061,610, "Method and apparatus for determining workload of motor vehicle driver" | 特許 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6061610 |
| S28 | 本田技研工業, ドライバー注意力モニター（技術解説） | 公式発表 | https://global.honda/jp/tech/Driver_Attention_Monitor/ |
| S29 | Automotive Fleet, "Mercedes-Benz Monitors How You Drive" ／ auto123, "Mercedes-Benz's Attention Assist System" | 記事 | https://www.automotive-fleet.com/65213/mercedes-benz-monitors-how-you-drive ／ https://www.auto123.com/en/news/mercedes-benzs-attention-assist-system/41639 |

補足（参考・本文の主要知見には含めない）:
- Talebloo F., Mohammed E.A., Far B.H., "Dynamic and Systematic Survey of Deep Learning Approaches for Driving Behavior Analysis," arXiv:2109.08996, 2021（58本の論文をレビュー）: https://arxiv.org/abs/2109.08996

注記:
- S3・S6・S14・S23・S24・S27・S29 の一部の記述は、WebSearch の検索結果の抜粋に基づく（本文PDFの全文は未確認、または抽出不可）。それ以外は WebFetch で要旨・本文を確認した。
- 性能値はすべて各ソースの評価条件に依存し、相互に比較できない。
