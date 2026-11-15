# 28. 運転・CAN時系列のドメイン汎化・少数ショット適応・軌跡予測のドメインシフト（B-23）

- 調査日: 2026-11-15
- 論点: B-23。ドメイン汎化（DG。目標ドメインのデータ無し）、少数ショット／テスト時適応、軌跡予測・運転行動予測のドメインシフト対策を集め、各研究で leave-one-domain-out（LODO。車種・ドライバー・データセットまたぎ）評価の有無を明記する。
- 既存調査との関係: 21（IDS 中心の車種間転移、AdaTime・RAINCOAT・POND、DriveDNA、信号同定、openpilot paramsd）と 09 §4.7 は扱い済みとして除外した。21 の次の一歩（DG・少数ショット・日本語）に当たる。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）29件／既出の再掲 0件。`scripts/sources_index.py --check` で全URLが NEW であることを確認した。サブエージェント間の重複（MetaFollower、車線変更の2集団論文）は1件に統合した。
- 確認方法の注記: この実行でも arxiv.org・jstage 等で WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の抜粋のみで確認しており、本文は未読である。数値・LODO の有無は抜粋由来で、原文照合が必要。著者名が抜粋で取れなかったものは「不明」とした。

## 1. エグゼクティブサマリー

- CAN のみを入力に、未見の車種・ドライバーへのDG／LODO評価を行った事故予兆・運転リスク研究は、英語・日本語の検索で見つからなかった。21 の結論（事故予兆のCAN車種間転移は未発見）を維持する。
- 評価プロトコルの先行例は他分野に豊富である。HAROOD（2025）は人・位置・データセット・時間の4種のシフトを LODO で評価し、DG 手法が単純な ERM を安定して上回らないと報告する（抜粋）。DOMINO は k-fold より LODO の精度が大きく下がることを述べる（抜粋）。
- 運転分野では、車線変更意図の2集団またぎで精度が大きく落ちる例がある（クロスデータセットで約72%対約85%、または約41%対約85%と抜粋間で数値が食い違い、原文照合が必要）。混合学習が最低限の対策になる。
- 少数ショット適応では、MAML でドライバー1人=1タスクとする MetaFollower（42〜44ドライバー規模）、新ドライバーを既存クラスタに割り当てる方式（追従10回未満で85.7%）、テスト時更新（T4P、MetaDAT）がある。入力は車間・相対速度・速度で、CAN 由来の変数に近いものがある。
- 車両またぎの大規模例として、EV フリート1.1M走行のベンチマーク（ICLR 2026）が未見の車両アーキテクチャで誤差増加8.1%と述べる（抜粋）。ただし事故予兆ではなくEVエネルギーのタスクである。
- 日本語資料は個人別モデルや個人差分析が中心で、少数ショット適応の定量評価や LODO は確認できなかった。
- 【推察】現実的な方針は、(a) 評価を leave-one-vehicle/driver-out に固定し、(b) ERM＋混合学習を基準線とし、(c) 共通成分＋車種・ドライバー固有の小さな適応部（低ランク残差・ベイズヘッド・クラスタ割当）を持たせ、(d) OOD 検知で保守的な閾値へ退避する構成である。

## 2. 主要知見

凡例: 各ソースに【LODO】の有無を明記する。確認方法はすべて「抜粋のみ」。

### 2.1 時系列ドメイン汎化（DG）とベンチマーク

**[1] HAROOD: A Benchmark for Out-of-distribution Generalization in Sensor-based HAR** — Wang Lu, Yao Zhu, Jindong Wang、2025（KDD 2026 採択と記載）、ベンチマーク。https://arxiv.org/abs/2512.10807
- 事実: cross-person・cross-position・cross-dataset（または cross-device）・cross-time の4シフトを評価。16手法・2種のモデル選択プロトコル。MLDG・DANN・CORAL 等が ERM を常に上回るとは限らず、勝つ手法が一定しないと報告。
- 【LODO】あり（3回反復）。
- 【推察】車種・ドライバー・ECU をドメインとして再利用できる。DG 手法より ERM＋モデル選択設計のほうが効く可能性がある。L0〜L1 と L6 の評価設計に効く。

**[2] Diversify: Out-of-Distribution Representation Learning for Time Series Classification** — Wang Lu, Jindong Wang ら（Microsoft Research）、2023（ICLR 2023）、手法。https://arxiv.org/abs/2209.07027
- 事実: 時系列内の潜在分布を敵対的に求め、サブドメイン間を整合させる。EMG・音声・HAR で最大4.3%の精度向上（二次要約）。
- 【LODO】抜粋では未確認。
- 【推察】車種ID が不確かな・混在するときに、ドメインラベル不要の点が利く。

**[3] Diversify の拡張（OOD 検出と汎化）** — Wang Lu, Jindong Wang ら、2023、プレプリント。https://arxiv.org/pdf/2308.02282
- 事実: ICLR 版を時系列 OOD 検出へ拡張。【LODO】未確認。
- 【推察】「この車両は分布外」の検知が L5/L6 の保守的閾値への退避判断に使える。

**[4] DOMINO: Domain-Invariant Hyperdimensional Classification for Multi-Sensor Time Series** — UC Irvine（Junyao Wang ら）、2023（ICCAD 2023）、手法。https://arxiv.org/pdf/2308.03295
- 事実: 低消費電力向けの多センサ時系列分類。既存の HDC 手法は k-fold より LODO で精度が明確に低いとの検索要約。
- 【LODO】あり。
- 【推察】ランダム k-fold は未見ドメイン性能を過大評価する。CAN 評価は車種・ドライバー単位で分割すべき。

**[5] 産業時系列のDG研究（J. Sens. Sens. Syst. 14, 119）** — 著者・題名未確認、2025、論文。https://jsss.copernicus.org/articles/14/119/2025/jsss-14-119-2025.pdf
- 事実: 7つの公開データセットで leave-one-group-out によりシフトを模擬。別の機械への移行などで性能が有意に低下。
- 【LODO】あり（leave-one-group-out）。

**[6] Investigating Domain-agnostic Performance in Activity Recognition** — Univ. of Cambridge、2022（HASCA）、ワークショップ論文。https://mobile-systems.cl.cam.ac.uk/papers/hasca22.pdf
- 事実: leave-one-subject-out を拡張した leave-datasets-out を提案。最新の深層モデルが未見ドメインで大きく劣化。【LODO】あり。

**[7] Causal-based Time Series Domain Generalization for Vehicle Intention Prediction（CTSDG）** — Yeping Hu, Xiaogang Jia, Masayoshi Tomizuka, Wei Zhan（UC Berkeley）、2021（ICRA 2022）、手法。https://arxiv.org/abs/2112.02093
- 事実: 構造因果モデルでドメイン不変な表現を得て、リカレント潜在変数モデルで時間依存を扱う。実走行データの未見シナリオで DG・行動予測のベースラインを上回ると報告。
- 【LODO】抜粋では分割が未確認（未見シナリオで評価）。
- 【推察】運転時系列DGの直接の先行例。車種固有のゲイン・オフセットを非因果成分として分離する発想を L1〜L2 に持ち込める。

**[8] Improving the Generalizability of Trajectory Prediction Models with Frenet-Based Domain Normalization** — 著者不明、2023、手法＋ベンチマーク（argoverse-shift）。https://arxiv.org/pdf/2305.17965
- 事実: 1つのデータセットをドメインに分け、未見ドメインで評価。Frenet 座標への正規化が未見ドメインでの予測を改善。【LODO】ドメイン分割の保留評価（詳細未確認）。
- 【推察】CAN での類推は、車両固有スケールによる速度・加速度の正規化（L1）。

**[9] Recurrent Aligned Network for Generalized Pedestrian Trajectory Prediction** — 著者不明、2024、手法。https://arxiv.org/abs/2403.05810
- 事実: 複数ソースデータで学習し、保留した対象データセットで評価（ETH-UCY・SDD・NBA）。【LODO】あり（多ソース→未見対象）。歩行者データのため手法参照のみ。

**[10] MetaTra: Meta-Learning for Generalized Trajectory Prediction in Unseen Domain** — 著者不明、2024、手法。https://arxiv.org/abs/2402.08221
- 事実: meta-train/meta-test 分割でドメインシフトを模擬し、更新なしで未見ドメインに対応。【LODO】模擬分割（厳密な LODO かは未確認）。
- 【推察】車種単位のエピソード分割は CAN に適用可能だが、HAROOD の知見ではメタ学習の利得は未証明。

**[11] Do Foundation Models Generalize to Real-World EV Fleets? A 1.1M-Drive Benchmark** — 著者不明、2026（ICLR 2026）、ベンチマーク。https://iclr.cc/virtual/2026/10013860
- 事実: ゼロショットの時系列基盤モデル3種と、クラスタ対応の混合エキスパート付き教師ありモデル2種を、EV 走行110万系列で比較。未見の車両アーキテクチャで誤差増加は8.1%（アブストラクト抜粋）。
- 【LODO】あり（車両アーキテクチャ単位。詳細未確認）。
- 【推察】基盤モデルのゼロショット＋クラスタ別エキスパートという構成は L2 の候補になる。タスクは EV エネルギーで、事故予兆ではない。

**[12] Causality-Inspired Latent Feature（CILF）による車両軌跡予測の OOD 汎化** — Li ら、2023、手法。https://arxiv.org/pdf/2307.05624v1.pdf
- 事実: K 個のソースドメイン・M 個のターゲットドメインの設定で、目標ドメインのラベル無しサンプルすら得にくいため DA は困難と著者が述べる。【LODO】K源→M目標（DG 設定）。
- 【推察】「目標ドメインのデータ無し」前提は本プロジェクトの車種またぎ DG の定義に合う。題名は抜粋では未確認（略称で記載）。

**[13] Exploring rounD Dataset for Domain Generalization in Autonomous Vehicle Trajectory Prediction** — Zhang ら、2024、Sensors 24(23) 7538。https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11644556/
- 事実: DG を転移学習・DA と区別し（新規シナリオのデータを使わない）、道路構成・録画時期の違いで訓練/テストをまたいで評価。【LODO】データセット内の条件またぎ（LODO 明記かは未確認）。道路・地図情報前提で CAN のみには直接適用できない。

**[14] Adaptive Prediction Ensemble（補助）** — Li ら、2024、手法。https://arxiv.org/pdf/2407.09475v2
- 事実: ルーティング関数付きアンサンブルで Waymo/Argoverse のゼロショット性能を改善と報告（数値未確認）。【LODO】未確認。

### 2.2 運転行動・軌跡予測のドメインシフトと少数ショット／テスト時適応

**[15] T4P: Test-Time Training of Trajectory Prediction via Masked Autoencoder and Actor-specific Token Memory** — Park ら、2024（CVPR 2024）。https://arxiv.org/pdf/2403.10052
- 事実: 従来のオンライン手法はラベル遅延と少サンプルのため最終層しか更新しなかったと指摘。MAE の自己教師あり損失とアクタ別トークンメモリで深い層も更新。【LODO】不明。
- 【推察】CAN でも実際のブレーキ等のラベルは後から得られる遅延ラベル構造は同じで、自己教師あり再構成損失による車両・ドライバー別の推論時更新を L4 付近の候補にできる。

**[16] MetaDAT: Generalizable Trajectory Prediction via Meta Pre-training and Data-Adaptive Test-Time Updating** — 著者不明、2026（CVPR 2026）。https://www.alphaxiv.org/abs/2603.09419
- 事実: メタ事前学習とデータ適応的な学習率のテスト時更新。二次要約では2,000サンプルで T4P（10,000サンプル）と同等以上（mADE6 0.327対0.343）。二次要約のため未検証。【LODO】不明。
- 【推察】適応に要するデータ量の見積り軸（Nイベントで適応）を CAN 版の評価に設けられる。

**[17] Trends in Motion Prediction Toward Deployable and Generalizable Autonomy: A Revisit and Perspectives** — 著者不明、2025、サーベイ。https://arxiv.org/pdf/2505.09074
- 事実: ドメイン汎化・適応手法を4分類し、一つを少数ショット/テスト時適応とする。【LODO】サーベイのため該当せず。分類枠（DG／UDA／少数ショット／TTA）の流用元。

**[18] Expanding the Deployment Envelope of Behavior Prediction via Adaptive Meta-Learning** — 著者不明、2022、プレプリント。https://arxiv.org/pdf/2209.11820
- 事実: 既存モデルに適応的ベイズ回帰層を足し、オフライン微調整またはオンライン適応でドメイン転移。【LODO】不明。
- 【推察】凍結した特徴抽出器＋軽量ベイズヘッドは車載の計算制約下での個人適応に向く。

**[19] MetaFollower: Adaptable Personalized Autonomous Car Following** — Xianda Chen ら、2024、プレプリント。https://arxiv.org/pdf/2406.16978
- 事実: IDM と LSTM のハイブリッドを MAML で学習し、ドライバー1人=1タスクとして共有事前分布を獲得。新ドライバーの少量データで微調整。Shanghai Naturalistic Driving Study の44ドライバー・3,050追従イベントで評価（サブエージェント間で3,050件・44人の記述は一致）。ベースライン超えと報告（数値未確認）。
- 【LODO】ドライバーまたぎの少数ショット形式だが leave-one-driver-out かは未確認。
- 【推察】自車速・相対速度・車間距離という CAN 由来の変数で成立する。ドライバー単位タスクの MAML は車種単位タスクへも拡張できる。

**[20] Lane Change Intention Prediction of two distinct Populations using a Transformer** — De Cristofaro ら、2025、プレプリント。https://arxiv.org/pdf/2509.06529（別の抜粋では https://arxiv.org/abs/2507.08365 とされ、どちらが正しいかは未確認）
- 事実: 他方のデータセットで学習して適用すると精度が低下。抜粋Aではクロスデータセット71.94%・別学習85.44%・混合学習最大86.84%。抜粋Bでは同一データで 85.35%（exiD）・77.64%（香港）、exiD→香港で41.30%。2つの抜粋で数値・ID が食い違うため、どちらも原文照合が必要。
- 【LODO】2集団間の片方向転移（LODO ではない）。
- 【推察】地域またぎで大きく落ちるため、ドメイン混合学習が最低限の対策になる。

**[21] An Intention-driven Lane Change Framework Considering Heterogeneous Dynamic Cooperation in Mixed-traffic Environment** — 著者不明、2025。https://arxiv.org/pdf/2509.22550
- 事実: NGSIM で学習し再学習なしで highD に適用するゼロショット転移。全手法が劣化し、原因は交通密度・道路形状・撮影視点の差とされる。最強ベースラインの精度は0.8290。【LODO】なし（一方向ゼロショット）。

**[22] Multi-scenario highway lane change intention prediction: a physics-informed AI framework** — Shi ら、2025、プレプリント。https://arxiv.org/pdf/2509.17354v1（後版 https://arxiv.org/pdf/2512.24075v2）
- 事実: highD（直線高速）と exiD（ランプ）でシナリオまたぎ汎化を評価。LightGBM が LSTM より汎化したと報告。後版は物理由来特徴の Bi-LSTM。【LODO】LODO 形式かは未確認。
- 【推察】TTC・THW 等の物理量特徴はシナリオ依存を減らす可能性があり、L1 の特徴設計と整合する。表形式の木モデルが深層モデルより頑健な場合がある点は要検証。

**[23] LoRD: Adapting Differentiable Driving Policies to Distribution Shifts** — Diehl, Karkus, Veer, Pavone, Bertram、2025（ICRA 2025）。https://arxiv.org/pdf/2410.09681
- 事実: 低ランク残差デコーダを付けて微調整（例: 別の国の交通規範）。標準の微調整比で忘却を最大23.33%軽減、閉ループ OOD 運転スコアが向上（版により8.83%または9.93%）。【LODO】なし（特定の地域・シナリオシフトへの微調整）。
- 【推察】低ランク残差など小さな追加パラメータは、車種別・地域別アダプタに向く。

**[24] Cross-cultural Deployment of Autonomous Vehicles Using Data-light Inverse Reinforcement Learning（DLIRL）** — Hongliang Lu ら、2025。https://arxiv.org/pdf/2504.11506
- 事実: 運転行動を転移可能な「運転アーキタイプ」と文化固有成分に分解し、後者を少量の現地データで推定。独・中・米の高速道路データで評価。最良ケースで必要データ量が98.67%減（最良値で平均ではない）。【LODO】3か国間の転移評価があるが LODO かは未確認。
- 【推察】「共通成分＋車種・地域固有の小さな成分」の分解を CAN の車種またぎ適応に使える。

### 2.3 日本語資料・ドライバー個人適応

**[25] A Study on Learning and Simulating Personalized Car-Following Driving Style** — Sheng, Pakdamanian, Han, Wang, Feng、2022（ITSC）。https://arxiv.org/pdf/2208.08002
- 事実: 42ドライバーの追従イベントから IRL で個人の報酬関数を学習。データが少ない新規ドライバーは GMM でクラスタとの類似度から運転スタイルを予測し、追従10回未満で85.7%の精度。【LODO】leave-one-driver-out の明示は未確認。
- 【推察】微調整不要のクラスタ割当は L1〜L2 のドライバー条件付けに使える。

**[26] PDB: Not All Drivers Are the Same – A Personalized Dataset for Understanding Driving Behavior** — Chuheng Wei ら、2025、データセット。https://arxiv.org/abs/2503.06477v1
- 事実: 同一車両・同一ルートで複数ドライバーを収録。CAN 信号（スロットル・ブレーキ・舵角）、LiDAR、カメラ、GNSS、IMU、顔動画、心拍を含む。ドライバー数12は二次要約のみで未検証。【LODO】データセット論文で評価プロトコル未確認。
- 【推察】車両を固定してドライバー差のみを分離でき、leave-one-driver-out の検証基盤になりうる。

**[27] 車速追従制御のための強化学習における転移可能な方策の学習手法** 【日本語】 — 夏有輝也ら、2021、電気学会論文誌C 141(12)。https://www.jstage.jst.go.jp/article/ieejeiss/141/12/141_1492/_article/-char/ja
- 事実: 階層型強化学習で走行ロボットの車速追従制御の転移可能な方策を学習。サンプル効率の悪さを課題とする。【LODO】確認不可。危険予測ではなく関連度は低〜中。

**[28] LSTMを用いた個人適合型ドライバモデルに関する研究** 【日本語】 — 芝浦工業大学（ADAM関連資料）、2021〜2024（年は抜粋から未確定）。https://www.shibaura-it.ac.jp/assets/11_ADAM_LSTM_2024_1.pdf
- 事実: ドライビングシミュレータの個人データから LSTM で個人別モデルを作成。追い越しで車両進行方向距離の誤差平均が0.09m以下と報告。【LODO】個人別モデルでドライバーまたぎ評価は未確認。
- 【推察】「個人別モデル」対「共通＋適応」の比較対象になる。

**[29] 車両挙動の個人差に着目した特徴抽出** 【日本語】 — 横山達也ら（三菱電機）、2018〜2020年頃（抜粋から未確認）、情報処理学会発表。https://ipsj.ixsq.nii.ac.jp/record/205423/files/IPSJ-Z82-5E-02.pdf
- 事実: 車載センサデータから個人差のある車両挙動を抽出。操舵の左右挙動を対象に、先行車との相対速度で個人差が現れる条件を検討。【LODO】なし（分析研究）。
- 【推察】個人差が出る条件（近接時・相対速度）は、TTC/THW 系閾値をドライバー別に較正する根拠になる。

## 3. 統合アーキテクチャ（12）への反映点

- L0〜L1: 車種またぎでスケール差が出る信号は、車両固有スケールで正規化する（[8]、21 の物理量化と整合）【推察】。
- L2: ドライバー・車種ごとの小さな適応部（クラスタ割当 [25]、ベイズヘッド [18]、低ランク残差 [23]）と、共通成分の分離（[7]、[24]）を候補とする【推察】。基盤モデルのゼロショット＋クラスタ別エキスパート [11] も候補。
- L3（R4）: 少数ショット適応のデータ量を「Nイベント」で評価軸にする（[16]、[19]）。ラベル遅延を使った推論時更新は [15] が参考【推察】。
- L5/L6: OOD 検知（[3]）で保守的な閾値へ退避する設計を検討する【推察】。評価は leave-one-vehicle/driver-out、ERM と混合学習を基準線に置く（[1]、[4]、[20]）。

## 4. 課題・ギャップ

- CAN のみ・事故予兆・未見車種またぎの DG／LODO 評価は未発見（英語・日本語とも）。
- 全29件が抜粋のみで、LODO の有無の多くが「未確認」のまま。原文確認は I-01 解消後。
- 車線変更2集団論文（[20]）の ID と数値が抜粋間で食い違う。
- 軌跡予測系は地図・位置入力で、CAN のみに直接は移せない。

## 5. 次のアクション提案

1. arxiv.org を許可して [1]・[7]・[11]・[20] を本文で確認し、LODO の分割と数値を確定する。
2. comma2k19 等の公開データで、HAROOD 型の leave-one-vehicle-out による ERM 基準線を設計する（設計作業、ISSUES I-11 側）。
3. ドライバー別少数ショット適応（クラスタ割当 vs MAML）の評価軸「Nイベントでの適応」を 14 のホライズン評価と組み合わせる。
4. PDB [26] の CAN 信号を確認し、同一車両でのドライバーまたぎ評価に使えるか調べる。
5. 日本語の予稿（JSAE・IEICE）で車種間・ドライバー間評価を個別検索する（B-27 と連携）。

## 6. 参考文献リスト（URL付き）

[1] https://arxiv.org/abs/2512.10807 / [2] https://arxiv.org/abs/2209.07027 / [3] https://arxiv.org/pdf/2308.02282 / [4] https://arxiv.org/pdf/2308.03295 / [5] https://jsss.copernicus.org/articles/14/119/2025/jsss-14-119-2025.pdf / [6] https://mobile-systems.cl.cam.ac.uk/papers/hasca22.pdf / [7] https://arxiv.org/abs/2112.02093 / [8] https://arxiv.org/pdf/2305.17965 / [9] https://arxiv.org/abs/2403.05810 / [10] https://arxiv.org/abs/2402.08221 / [11] https://iclr.cc/virtual/2026/10013860 / [12] https://arxiv.org/pdf/2307.05624v1.pdf / [13] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11644556/ / [14] https://arxiv.org/pdf/2407.09475v2 / [15] https://arxiv.org/pdf/2403.10052 / [16] https://www.alphaxiv.org/abs/2603.09419 / [17] https://arxiv.org/pdf/2505.09074 / [18] https://arxiv.org/pdf/2209.11820 / [19] https://arxiv.org/pdf/2406.16978 / [20] https://arxiv.org/pdf/2509.06529 / [21] https://arxiv.org/pdf/2509.22550 / [22] https://arxiv.org/pdf/2509.17354v1 / [23] https://arxiv.org/pdf/2410.09681 / [24] https://arxiv.org/pdf/2504.11506 / [25] https://arxiv.org/pdf/2208.08002 / [26] https://arxiv.org/abs/2503.06477v1 / [27] https://www.jstage.jst.go.jp/article/ieejeiss/141/12/141_1492/_article/-char/ja / [28] https://www.shibaura-it.ac.jp/assets/11_ADAM_LSTM_2024_1.pdf / [29] https://ipsj.ixsq.nii.ac.jp/record/205423/files/IPSJ-Z82-5E-02.pdf
