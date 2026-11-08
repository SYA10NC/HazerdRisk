# 21. CAN信号の車種間ドメイン適応・転移学習（B-08）

- 調査日: 2026-11-08
- 論点: B-08。車種・ECU が異なる CAN 信号間でモデルを移植する手法（信号の正規化・物理量化、ドメイン適応、少数ショット適応）を、運転データ・侵入検知（IDS）・他分野の多変量時系列から集める。各研究で「車種をまたいだ評価をしたか」を明記する。
- 既存調査との関係: 09 §4.7（「明示的な研究は見つからなかった」）、09 [5]（Foundation CAN LM）、06 §2.4（Geotab 車格別閾値）、03（DBC 概要）、09 の既出 arXiv（1911.09508、2412.10780、2409.07505、2507.00593、2602.00866、2207.10807、2106.06947、2007.08795、2106.08692）は扱い済みとして除外した。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）31件／既出の再掲 0件。`scripts/sources_index.py --check` で全URLが NEW であることを確認した（サブエージェント間の重複 2207.10814・1902.08956 は1件に統合）。
- 確認方法の注記: この実行でも arxiv.org・docs.comma.ai・preprints.org・jstage.jst.go.jp で WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の検索結果の抜粋のみで確認しており、本文は未読である。「車種またぎ評価」の記載も抜粋ベースで、本文での再確認が要る。

## 1. エグゼクティブサマリー

- CAN の車種間転移を扱う研究は IDS（侵入検知）に集中している。運転行動・事故予兆を CAN のみで車種間転移した研究は、探した範囲では見つからなかった（09 §4.7 の結論を維持する）。
- 最新の否定的知見として、preprints.org の 2026 年プレプリントは「識別子・周期・ペイロード符号化が車種固有のため、ゼロショットの車種間転移は難しい」とし、対象車の正常データだけで適応する方式を提案している（抜粋のみ・査読なし）。
- 車種またぎ評価が確認できる例は少なく小規模である。DriveDNA（2026）は 115 車種の運転データで車種またぎ分割を設けているが、CAN 単独の数値は抜粋では確認できない。
- 前処理の面では、(a) 信号セマンティクスの自動同定（Lestyán 2019、OSTI の LSTM 復号）、(b) ステアリング比・タイヤ剛性・質量のオンライン推定（openpilot paramsd、MERL）が、DBC の無い・ばらつく車種を物理量化する実用手段になりうる。
- 汎用の時系列 UDA（AdaTime、RAINCOAT、POND）は被験者・機器またぎが標準の評価だが、車両・CAN での検証例は見つからなかった。評価設計としては「ターゲットラベルを使わないモデル選択」（AdaTime）が、事故ラベルのほぼ無い新車種に直結する。
- 【推察】現実的な運用は「物理量化（L0）＋車種ごとの正常走行データによるキャリブレーション＋車種非依存の信号サブセット」であり、ゼロショット移植を前提にしない設計である。
- 日本語では CAN の車種間転移を直接扱う論文を確認できなかった（周辺の2〜3件も本文未読）。

## 2. 主要知見

凡例: 各ソースに【車種またぎ評価】を明記する。すべて確認方法は「抜粋のみ」。

### 2.1 CAN を対象とした転移・ドメイン適応（IDS 中心）

**[1] Supervised Contrastive ResNet and Transfer Learning for the In-vehicle Intrusion Detection System** — Hoang, Kim（検索抜粋の記載。所属不明）、2022（arXiv ID から推定）、arXiv プレプリント。https://arxiv.org/pdf/2207.10814
- 事実: 教師付きコントラスト学習 ResNet と転移学習で、ソース車種の知識を別の車種へ移す。あるデータセットで F1=0.9994 と報告（抜粋）。先行の LSTM 車種間転移は良好でなかったとの記述も抜粋に出る。
- 【車種またぎ評価】抜粋上は「異なる車種の CAN データ間」を謳う。別車種で train/test したかは本文で要確認。
- 【推察】IDS の転移であり、予兆特徴量に直結しない。「車種ごとの微調整が要るか」の参照点になる。

**[2] Target-adaptive CAN intrusion detection（正式題名未確認）** — 著者不明、2026（URL から推定）、preprints.org プレプリント（査読なし）。https://www.preprints.org/manuscript/202609.1557
- 事実: 識別子・タイミング・ペイロード符号化が車種固有のため、ゼロショットの車種間転移は難しいとする。正常データのみによる対象車での適応（Isolation Forest）を提案。capture 分離の評価で AUPRC 約 0.55（抜粋）。多くの評価が単一車両・単一データセットに留まると指摘。
- 【車種またぎ評価】あり（抜粋より）。
- 【推察】対象車の正常走行でキャリブレーションする運用が現実的。09 §4.7 を補強する最新の否定的知見。

**[3] Transfer learning for LSTM-based CAN intrusion detection（正式題名未確認）** — Cal Poly 学位論文、年不明。https://digitalcommons.calpoly.edu/theses/3272
- 事実: 基準車で学習した LSTM を拡張データセット・別構成へ転移。検索の説明では学習データ 75% 削減でも同等以上の F1（条件未確認）。
- 【車種またぎ評価】部分的。完全に別車種かは不明。
- 【推察】新車種立ち上げ時のデータ量削減の根拠候補。

**[4] A Transfer Learning Based Intrusion Detection System for Internet of Vehicles** — 著者・年不明、HAL 登録。https://hal-iogs.archives-ouvertes.fr/ERA-UTT/hal-04439575v1
- 事実: 題名と検索ヒットのみ。【車種またぎ評価】不明。周辺文献として挙げるに留める。

**[5] Image-based CAN IDS with CNN transfer learning** — Yang, Shami（抜粋）、2022（ID から推定）、arXiv。https://arxiv.org/pdf/2201.11812
- 事実: CAN トラフィックを画像化し CNN＋転移学習で検出。Car-Hacking データセットと CICIDS2017 で評価。
- 【車種またぎ評価】なし（単一車両データと一般ネットワークデータ）。

**[7] DAdAE（domain-adversarial autoencoder による車載 CAN 異常検知）** — Mavikumbure ら（dblp キーより）、2023、IECON 2023。https://dblp.uni-trier.de/rec/conf/iecon/MavikumbureCWVPM23.html
- 事実: ドメイン敵対学習型 AE を CAN 異常検知に適用（書誌ページのみ）。【車種またぎ評価】評価プロトコル不明。
- 【推察】正常データのみで学習する点が本プロジェクトの用途と相性がよい可能性がある。要本文確認。

**[9] Vehicles driving behavior recognition based on transfer learning** — 著者不明、2023、Expert Systems with Applications（抜粋の記載）。https://www.bohrium.com/paper-details/vehicles-driving-behavior-recognition-based-on-transfer-learning/864976224756170760-2452
- 事実: 事前学習した CNN を新しい車種へ転移（同質転移）。より多くの車種での検証は今後の課題とされる。
- 【車種またぎ評価】あり（新車種へ転移とされる）。入力が CAN かは未確認。運転行動の車種間転移の数少ない例だが、採否は本文次第。

**[10] An innovative generalization method for data-driven models of steering feedback torque** — 著者不明、2023、Proc. IMechE Part D（抜粋の記載）。https://www.aminer.org/pub/65cf7f37939a5f4082c709b6/an-innovative-generalization-method-for-data-driven-models-of-steering-feedback-torque
- 事実: 複数ソース車両で学習したモデルを少量データの対象車両へ転移。対象ドメインで精度が 58%〜74.7% 向上と記載（抜粋）。
- 【車種またぎ評価】あり（ソース車両→対象車両）。
- 【推察】操舵トルクは CAN 信号の一つで、車種間回帰の例になる。用途は事故予兆ではない。

**[11] CANデータによる危険予測（東京大学 酒井・入江研）【日本語】** — 研究室紹介ページ、年不明。https://www.mtl.t.u-tokyo.ac.jp/site_archives/sakai_irie/archives/researches/882/
- 事実: トヨタ自動車との共同研究で、CAN データや車載カメラ情報から操作ミス・異常を検知。公開データにない異常時・事故時の実データで実験。
- 【車種またぎ評価】なし（記載なし）。国内の関連研究の所在を示すもの。

### 2.2 信号の同定・正規化・物理量化

**[6] Extracting vehicle sensor signals from CAN logs for driver re-identification** — Lestyán, Acs, Biczók, Szalay、2019、ICISSP 2019（arXiv cs.CR）。https://arxiv.org/abs/1902.08956 （PDF: https://arxiv.org/pdf/1902.08956）
- 事実: 同じ物理量の信号は車種が違っても統計的特徴が似る、という前提で、ある車の既知信号で学習した分類器により、位置未知の別車両の信号を同定する。抽出信号で 33 名のドライバー再識別が可能。「信号位置を伏せても個人データでなくなるわけではない」と結論。
- 【車種またぎ評価】あり（信号マッチング部分）。ドライバー識別自体の車種間転移ではない。
- 【推察】DBC 未公開車種の L0 自動マッピングに使える可能性。個人データ性への配慮が要る。

**[8] Lightweight LSTM for CAN Signal Decoding** — 著者・年不明、OSTI 登録。https://www.osti.gov/biblio/1783432
- 事実: 未復号の CAN データを、別車両の復号済みデータとの類似性で識別する。メーカーごとに符号化が異なることを課題とする。
- 【車種またぎ評価】あり（復号済み車両→未復号車両）。
- 【推察】DBC が無い車種への移植で信号同定の自動化に使える可能性。

**[13] DriveDNA: A Large-Scale Multimodal Naturalistic Driving Dataset and Benchmark for Driving Style Identification** — HenryYHW 名義で Hugging Face 公開（著者未確認）、2026、arXiv＋データセット（同意制）。https://arxiv.org/pdf/2607.23822 （補助: https://huggingface.co/papers/2607.23822）
- 事実: 465 名・115 車種・4,121 ドライブ・975 時間。10 Hz の前方映像と同期した制御信号を含む。論文は 20 名が 2 車種以上に跨るとし、Hugging Face カードは 16 名と記載しており、出典間で人数が食い違う。車種固定タスク（24 車種、各 4 名以上）を設ける。映像のみモデルの再識別精度は .937 で、条件を揃えると .675 に低下し、ショートカットの存在を示す。
- 【車種またぎ評価】あり（同一ドライバーの複数車種間。副次的ケーススタディ）。CAN 単独の数値は抜粋で確認できない。
- 【推察】車種またぎ分割の設計と、車種・経路ショートカット排除の手本になる（L6）。

**[14] openpilot selfdrive.locationd.paramsd** — comma.ai、年・版不明、公式ソースコード文書。https://docs.comma.ai/_modules/selfdrive/locationd/paramsd.html （補助: https://docs.comma.ai/_modules/selfdrive/controls/lib/vehicle_model.html）
- 事実: カルマンフィルタの状態に steer ratio と stiffness を持ち liveParameters に出力。不確かさも出力。車両モデルは学習した係数を公称コーナリング剛性に乗じる。
- 【車種またぎ評価】なし（実装資料）。
- 【推察】ギア比・剛性を「車種ごとの定数」でなくオンライン推定量として扱う実例。L1 の物理量化（操舵角→前輪角→曲率）に使える。収束条件と上下限は本文要確認。

**[15] opendbc 車種ページ（Rivian R1S 2025、Honda CR-V 2015-16 など）** — opendbc コミュニティ由来の第三者ホスト、年不明。https://opendbc-site.pages.dev/cars/rivian-r1s-2025 （補助: https://opendbc-site.pages.dev/cars/honda-cr-v-2015-16）
- 事実: 車種ごとに stiffness factor、前後タイヤ剛性、steer ratio の初期値を持つ。R1S 2025 は stiffness factor 約 1.00、前後剛性約 366,031 / 578,621。CR-V 2015-16 は stiffness factor 約 0.44。Acura MDX 2025 の steer ratio は 16.20（いずれも検索抜粋）。
- 【車種またぎ評価】なし（カタログ）。公式サイトではなく値は抜粋のもの。
- 【推察】車種間でギア比・剛性が数倍異なりうる根拠。車種メタデータ表（L0）の設計例。

**[16] 大型車両の操舵制御のための運動力学モデルの構築とパラメータ同定手法【日本語】** — 金子哲也ほか（日本大学ほか、組織は抜粋から推定）、2010、自動車技術会論文集 41巻6号。https://www.jstage.jst.go.jp/article/jsaeronbun/41/6/41_6_1231/_article/-char/ja
- 事実: 隊列走行の大型トラックの操舵制御向けに、最小次元の物理モデルとパラメータ同定を提案。関連講演資料は等価コーナリングパワーとして同定。
- 【車種またぎ評価】なし。【推察】等価コーナリングパワー同定は車種差を吸収するパラメータ化の候補。乗用車↔トラックの適用可否は別途検証が要る。

**[17] MERL TR2021-060（粒子フィルタによるタイヤ剛性・質量・慣性のオンライン推定）** — MERL、2021（ID から推定）。https://shadow.merl.com/publications/docs/TR2021-060.pdf
- 事実: 粒子フィルタによるタイヤ剛性推定を質量・慣性のオンライン適応へ拡張。量産車で利用できる CAN 信号を使うとされる（関連レコードの記載）。
- 【車種またぎ評価】確認できず。【推察】積載量・車重の変動を CAN のみで補正できる可能性（L1 個別化）。

**[18] A Prototypical Network with an Attention-based Encoder for Drivers Identification Application（P-AttEnc）** — 著者不明、2025（arXiv 2510.17250 から推定）。https://fugumt.com/fugumt/paper_check/2510.17250v1_enmode （補助: https://www.themoonlight.io/review/a-prototypical-network-with-an-attention-based-encoder-for-drivers-identification-application）
- 事実: CAN の少数ショットドライバー識別。精度は OcsLab で 5-way 10-shot が 93.4%、hciLab で 10-way 10-shot が 98.7%。未知ドライバーへの汎化を評価。二次サイト経由で arXiv 本体は未確認。
- 【車種またぎ評価】抜粋の範囲ではなし。
- 【推察】「車種」を新クラスとする少数ショット適応へ読み替えられる可能性。

### 2.3 多変量時系列の UDA／TTA（他分野から転用）

**[19] AdaTime: A Benchmarking Suite for Domain Adaptation on Time Series Data** — Ragab, Eldele ら（NTU / A*STAR）、2021 プレプリント・TKDD 2023、ベンチマーク。https://arxiv.org/abs/2203.08321
- 事実: 評価方式・データ・バックボーンの不統一を指摘し標準化。ターゲットのラベル付きデータをモデル選択に使うのは UDA の前提に反すると指摘。プレプリントでは 10 手法・3 データセット・15 のクロスドメイン設定（TKDD 版は 11 手法）。適切にハイパラを選べば視覚用 DA も時系列専用手法と同等。モデル選択方式が性能を大きく左右する。
- 【ドメインまたぎ評価】あり（被験者・機器単位）。ラベル無しターゲット対応。
- 【推察】車種A→Bの評価も「ターゲットラベル不使用のモデル選択」を前提にすべき（新車種の事故ラベルはほぼ無い）。

**[20] Domain Adaptation for Time Series Under Feature and Label Shifts（RAINCOAT）** — He, Queen, Koker, Cuevas, Tsiligkaridis, Zitnik、2023、ICML 2023。https://arxiv.org/abs/2302.03133
- 事実: ラベルシフトとターゲット固有ラベルの検出を扱う。時間・周波数特徴を併用。5 データセット・13 の UDA 手法との比較で最大 16.33% 向上（著者自己報告）。
- 【ドメインまたぎ評価】あり。データセット名は抜粋に無い。
- 【推察】車種ごとのイベント発生率差はラベルシフトに近い。周波数特徴はサンプリング周期差に頑健な可能性があるが、CAN の非周期・離散信号では要検証。

**[21] POND: Multi-Source Time Series Domain Adaptation with Information-Aware Prompt Tuning** — Wang, Bai, Cheng, Chen, Zhao, Chen、2023-12（初版）・KDD 2024。https://arxiv.org/abs/2312.12276
- 事実: 複数ソースの時系列 DA にプロンプトを使う。適応時に学習済みプロンプトでターゲットに最も近いソースを選ぶ。5 データセット・50 シナリオで F1 が最大 66% 向上（自己報告。SOTAVerified では Unverified）。
- 【ドメインまたぎ評価】あり（マルチソース→ターゲット）。
- 【推察】複数車種のデータがある場合、「新車種に最も近い既存車種を選ぶ」設計に対応する。

**[22] Continuous Test-Time Domain Adaptation for Efficient Fault Detection under Evolving Operating Conditions** — Sun, Fink（抜粋）、2025（ID から推定）。https://arxiv.org/pdf/2507.16354v1
- 事実: 産業センサで運転条件が変化する状況の連続テスト時 DA。制御変数とセンサ計測値に別々の適応モジュール。
- 【ドメインまたぎ評価】運転条件の変化。機種間かは抜粋に無い。
- 【推察】CAN の入力（ペダル・操舵）と応答（速度・加速度）を分けて適応する発想（L0・L1）。

**[23] When Model Meets New Normals: Test-Time Adaptation for Unsupervised Time-Series Anomaly Detection（M2N2）** — Kim, Park, Choo、2024（抜粋の記載、arXiv 2312.11976）。https://arxiv.org/html/2312.11976v2
- 事実: 「新しい正常」へのシフトを前提に、教師なし時系列異常検知へ TTA を適用。別論文 CANDI がベースラインとして使用（抜粋）。
- 【ドメインまたぎ評価】時間経過の分布シフト。機種間かは不明。
- 【推察】事故ラベルの無い新車種で「正常運転分布」だけを適応する異常検知型予兆検知と整合。

**[24] PI-TTA（物理制約付き source-free TTA、ウェアラブル HAR）** — 著者不明、2026（ID から推定）。https://arxiv.org/pdf/2604.25435
- 事実: 確信度駆動のベースラインは継続ストリーミングで大きく劣化すると報告。物理ベースの制約を足して適応を安定化。
- 【ドメインまたぎ評価】詳細不明。【推察】速度と加速度・ヨーレートの整合など車両物理を TTA の安定化制約に使える。source-free は車種提供元がデータを共有できない場合に有利。

**[25] SMORE（超次元計算によるマルチセンサ時系列 DA）** — 著者不明、2024（ID から推定）。https://arxiv.org/pdf/2402.13233v2.pdf
- 事実: HDC による DA。DNN ベース DA より約 2% 高精度で学習・推論が大幅に高速と報告。【ドメインまたぎ評価】抜粋では不明。【推察】車載 ECU 上のオンデバイス適応の候補だが根拠は弱い。

**[26] MVAdapt（マルチ車両ゼロショット適応、E2E 自動運転）** — 著者不明、2026（ID から推定）。https://arxiv.org/pdf/2604.11854
- 事実: 学習済み以外の車両へゼロショットで適応する E2E 自動運転（WebSearch の要約のみ）。
- 【車種またぎ評価】あり（未学習車両へのゼロショット）。入力は CAN のみとは限らず適用可否は要精査。車両諸元を条件入力にする発想は参考になる。

**[27] Enhancing Lithium-Ion Battery SOC Estimation Across Battery Types via Unsupervised Domain Adaptation** — 著者不明、2024、PHME 2024。https://www.papers.phmsociety.org/index.php/phme/article/view/4012
- 事実: 回帰ベースの教師なし DA で電池種別間・温度間の SOC 推定を評価。
- 【ドメインまたぎ評価】あり（電池種別間）。【推察】TTC・THW のような連続量予測を車種間で移す際の回帰 UDA の参照。

### 2.4 日本語（運転・車両データ）

**[28] ドライブレコーダ映像のヒヤリハット分類における教師なしドメイン適応（CiNii 登録）** — 著者・年不明。https://cir.nii.ac.jp/crid/1050285299827575040
- 事実: 車種・カメラ種別など収集条件が違うと分布が変わり精度が制限される、という問題意識。既存 CNN-RNN 分類器に「収集環境を推定する層」を足し環境非依存特徴を抽出（敵対的学習）。教師なし環境のデータにも高い精度と報告。数値・車種の組は未確認。概要のみ。
- 【ドメインまたぎ評価】あり（車種・カメラ等の収集条件）。ただし映像データ。
- 【推察】DANN 型「収集環境識別器＋勾配反転」を CAN 時系列エンコーダに載せる設計の先行例。車種ごとの CAN 配信仕様差を「環境」として扱える。

**[29] 人工知能学会論文誌（J-STAGE）: 他車種から新車種へ知識を移す車載ネットワーク攻撃検知（要再確認）** — 題名・著者・年は未確認。https://www.jstage.jst.go.jp/article/tjsai/37/5/37_37-5_C-M42/_article/-char/en
- 事実（検索要約による。再検索では再現せず、同一論文か未確認）: データが豊富な別車種から新車種の攻撃検知へ知識を移す。教師あり学習モデルと、対象車両の正常データのみで学習する教師なし検知器を組み合わせる。引用前に本文確認が必要。
- 【推察】内容が正しければ日本語の CAN 車種間転移の先行例だが、用途は攻撃検知。

**[30] 余寿命予測における運転条件を考慮した時系列 UDA（J-STAGE）【日本語】** — 題名・著者・年は検索要約依存。https://www.jstage.jst.go.jp/article/jsceiii/6/3/6_1038/_article/-char/en
- 事実（検索要約による。URL と論文の対応付けは未確定）: DANN の領域識別器を複数識別器に置き換える。対象は航空機エンジンで車両ではない。
- 【推察】運転条件（速度域・負荷）ごとにドメインを分ける設計の転用候補。

**[31] プラントデータにおける転移学習の可能性（横河技報 Vol.63 No.1）【日本語】** — 横河電機、2020。https://web-material3.yokogawa.com/19/29622/files/rd-tr-r06301-004.pdf
- 事実: ある設備の学習データを似た別設備の異常検知へ適用する方法を紹介。車載ではない。【車種またぎ評価】なし。【推察】「同種設備間転移」の考え方を車種間に当てはめる際の参考。

（注: サブエージェントが候補に挙げた jsaisigtwo/2024/SMSHM-001 は内容未確認のため載せていない。）

## 3. 統合アーキテクチャ（12）への反映点

- L0（入力・正規化）: DBC 公開有無にかかわらず、物理量（速度 m/s、操舵角→前輪角、加速度 g）に正規化する。信号セマンティクスの自動同定（[6][8]）は DBC の無い車種への補助手段として検討する【推察】。車種メタデータ表（ギア比・剛性・車重）を持つ（[15]）。
- L1: ステアリング比・タイヤ剛性・質量のオンライン推定（[14][17]）で車種差・積載差を吸収する候補。推定の不確かさを可用性・信頼度に載せる【推察】。
- L2（DRV・個別化）: 対象車の正常走行データによるキャリブレーション（[2]）と少数ショット適応（[18]）。車種非依存の信号サブセット（09 §4.7 の推察）を維持する。
- L3（R4）: ゼロショット移植を前提にしない。DANN 型の収集環境識別器（[28]）、RAINCOAT 型の時間・周波数併用（[20]）、物理制約付き TTA（[24]）は検証候補【推察】。
- L6（評価）: 車種またぎ分割（leave-one-vehicle-out）とターゲットラベル不使用のモデル選択（[19]）を標準にする。ショートカット（車種・経路）の排除（[13]）。

## 4. 課題・ギャップ

- 事故予兆を CAN のみで車種間転移した研究は未発見。IDS の転移結果は予兆タスクに直接は使えない【推察】。
- 全31件が抜粋のみで、車種またぎ評価の有無・数値は本文で未確認（ISSUES I-01）。
- 日本語文献は周辺のみ。J-STAGE・CiNii の直接検索（WebSearch は US 限定のため網羅性が低い可能性）が要る。
- 未検索: ドメイン汎化（DG）、少数ショット適応の運転データ版、軌跡予測のドメインシフト。
- [29][30] は題名・対応付けが未確定で、引用不可に近い。

## 5. 次のアクション提案

1. I-01 解消後、[1][2][6][9][20][28] の本文で車種またぎ評価の有無・数値を確定する。
2. 公開データ（comma2k19、DriveDNA 等）で leave-one-vehicle-out と、AdaTime 流のラベル不使用モデル選択の評価手順を設計に落とす（設計タスク、I-11 系）。
3. 車種メタデータ表（ギア比・剛性・車重）と paramsd 型オンライン推定の L0/L1 仕様案を作る。
4. ドメイン汎化・少数ショット適応・軌跡予測のドメインシフトを次回以降の追加論点とする（BACKLOG 追加済み）。

## 6. 参考文献リスト

本文中の URL を参照（[1]〜[31]）。すべて検索結果で実在を確認したが、本文は未読である。
