# 17. SHRP2 運動学トリガの仕様と、CAN のみでの再現（B-04）

- 調査日: 2026-11-04
- 論点: B-04。SHRP2 の crash/near-crash 抽出に使われた運動学トリガ12種の「信号・閾値・継続時間・最低車速・出典ページ」を確定し、CAN 信号での再現可否と精度上の注意を整理する
- 既存調査との関係: 05 §2（トリガ一覧表）・§3.1（Baseline Report の定義と有効率22%）・§3.3（トリガ性能。Sudweeks の92%/81%/42%、Perez ら2017 の -0.75G 推奨、euroFOT）、01 §3.1（閾値の一般値）、16（先行車信号の車種別表）は扱い済みとして除外した。本書はその先（12種の行ごとの値、トリガ別性能、CAN 再現の精度上の注意）だけを探した
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）21件／既出の再掲 3件（URL は新規だが内容は05と同一の文献。[R1]〜[R3]）。`scripts/sources_index.py --check` で全 URL が NEW であることを確認した
- 確認方法の注記: この実行では arxiv.org、vtechworks.lib.vt.edu、mlit.go.jp、saemobilus.sae.org、cir.nii.ac.jp、onlinepubs.trb.org などで WebFetch が名前解決に失敗した（ISSUES I-01 の継続）。全ソースが WebSearch の抜粋のみで、本文は1件も読めていない。検索ツールの要約は、数値が原文か要約者の補足かを判別できない。数値は「抜粋記載」として扱い、引用前に一次確認が要る

## 1. エグゼクティブサマリー
- 主目的であった「SHRP2 トリガ12種の行ごとの表」は確定できなかった。Baseline Report 本文（05 [1]）を読めないためである。表番号・ページ番号は1つも確認できていない。05 §2 の表が現時点で最良の二次整理であり、一次確認は I-01 解消後（新設 B-19）に回す
- 抜粋から言える事実は、(a) 12種のうち前後方向減速度ベースのアルゴリズムが有効な crash/near-crash の割合が最も高かったこと（[R3]）、(b) 運動学トリガは感度・特異度が低く映像の人手確認が前提であること（[R2][14]）、(c) 前後加速度が通常運転からの逸脱の最良の指標で、前方 TTC は誤報率が高いとする報告があること（[16]）の3点である
- トリガ別の感度・適合率・再現率を数値で報告した新規文献は見つからなかった。数値が得られたのは、既出の Sudweeks（ヨーレート）と、深層学習の精度（[15]、精度のみ）だけである
- CAN での再現に関する抜粋ベースの注意点は、(1) 微分を重ねるほどノイズが増える（ジャークは2階微分）、(2) 制動中は車輪スリップで車輪速由来の加速度が実際の車体運動とずれる、(3) 加速度センサの取付軸ずれ・較正で精度が変わる、(4) 国内ドラレコは車速パルス2Hz・加速度30Hzなど記録周期が低い、(5) 路面の段差による誤検知が多い、の5点である
- 【推察】CAN のみで SHRP2 型トリガを再現するときは、縦加速度は ESC の縦G信号を第一候補とし、無ければ車輪速の1階微分、ジャークは平滑化した縦Gを1回だけ微分する。ABS/ESC 作動中は車輪速微分の信頼度を下げる

## 2. 主要知見

### 2.1 トリガ仕様（サブ論点1）

**[R3] Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets（書誌ページ）**
- 組織・年・種別: SWOV（VTTI 報告書 Hankey ら 2016 の書誌）、報告書
- URL: https://swov.nl/en/publicatie/description-shrp2-naturalistic-database-and-crash-near-crash-and-baseline-data-sets
- 確認方法: 抜粋のみ。内容は05 [1] と同一（再掲）
- 要点（事実）: 約12種のトリガアルゴリズムを 5,512,900 トリップファイルに適用し、人手検証で crash 1,549件・near-crash 2,705件を確認した。前後方向減速度ベースのアルゴリズムが有効事象の割合が最も高かった
- 示唆: 【推察】CAN のみのベースラインは、まず前後減速度トリガから始めるのが妥当である

**[23] SHRP2 Project Brief（S08）**
- 組織・年・種別: TRB / SHRP2、2013、プロジェクト概要
- URL: https://onlinepubs.trb.org/onlinepubs/shrp2/SHRP2_PB_S08_2013-05.pdf
- 確認方法: 抜粋のみ
- 要点（事実）: 抜粋によれば、イベントファイルはイベント前約20秒、後約10秒を含む
- 示唆: 【推察】農工大 DB（前10 s・後5 s）より窓が長い。CAN ログの切り出し窓を決める際の参照になる

**[22] FHWA-HRT-24-070**
- 組織・年・種別: FHWA、2024頃、報告書
- URL: https://highways.dot.gov/sites/fhwa.dot.gov/files/FHWA-HRT-24-070.pdf
- 確認方法: 抜粋のみ
- 要点（事実）: 前後加速度は過去の SHRP2 研究でも crash/near-crash の主要指標として使われている。横加速度は右向きを正とする。Muttart のスワーブ解析では、初回の車線端での平均横加速度が約 0.27 g だった（抜粋記載）
- 示唆: 符号規約は CAN 側と SHRP2 側で揃える必要がある【推察】

### 2.2 トリガ別の有効率・性能（サブ論点2）

**[14] Recognizing Safety-critical Events from Naturalistic Driving Data**
- 著者・組織・年・種別: Dozza, Pañeda González（Chalmers）、2012、会議論文（Procedia – Social and Behavioral Sciences 48）
- URL: https://research.chalmers.se/publication/162698
- 確認方法: 抜粋のみ
- 要点（事実）: 運動学トリガ（例: 減速度が閾値を下回る急ブレーキ）は感度・特異度が低く、人手の映像確認が必要と述べる。運転者の個別反応の映像分析を加えると分類が改善しうる
- 示唆: 【推察】CAN のみでは映像併用の改善分が使えず、誤検出は「運動学のみ」の水準になる。05 の euroFOT 約400件の整理と同じ方向の結論である

**[16] Detecting Deviation from Normal Driving Using SHRP2 NDS Data（プレプリント）**
- 著者・組織・年・種別: Papazikou ら（UWE リポジトリ掲載）、年は未確認、プレプリント
- URL: https://uwe-repository.worktribe.com/index.php/OutputFile/12111851
- 確認方法: 抜粋のみ
- 要点（事実）: 前後加速度が通常運転からの逸脱の最良の指標。前方 TTC は誤報率が高い。受領した SHRP2 データには TTC が変数として含まれていなかった。前後加速度・横加速度・ヨーレートが信頼できる指標とされ、例示された閾値は横加速度 約 ±0.65 g、前後加速度 約 ±0.5 g（抜粋記載。原典との照合は未完）
- 示唆: 【推察】CAN のみ運用では TTC を距離・相対速度から自前で導出する必要があり、TTC 単独トリガは誤報が多いので減速度との併用が前提になる

**[20] What came before the crash? An investigation through SHRP2 NDS data**
- 著者・組織・年・種別: Papazikou, Quddus, Thomas, Kidd、2019（Safety Science）、論文
- URL: https://www.sciencedirect.com/science/article/abs/pii/S0925753518300092
- 確認方法: 抜粋のみ
- 要点（事実）: SHRP2 の crash/near-crash について、TTC が車種・自車速度・前後加速度・イベント内の時間でどう変わるかを調べた
- 示唆: 周辺文献。TTC 系リスク指標の事象内推移の参考【推察】

**[15] Inferring safety critical events from vehicle kinematics in naturalistic driving environment: Application of deep learning algorithms**
- 著者・組織・年・種別: ORNL / テネシー大の研究者ら、年・掲載誌は未確認、論文
- URL: https://www.ornl.gov/publication/inferring-safety-critical-events-vehicle-kinematics-naturalistic-driving-environment
- 確認方法: 抜粋のみ（著者・掲載誌の一致は未確認）
- 要点（事実）: 変動性ベースの運動学閾値で抽出した9,553事象を用い、アンサンブル CNN が 20% ホールドアウトで crash/near-crash 検出の精度95.6%（最良の単一 CNN より2.5ポイント高い）。精度のみで適合率・再現率・クラス比は不明
- 示唆: 【推察】クラス比が不明なため閾値方式との公平な比較には使えない。運動学時系列のみから判定できるという存在証明にとどまる

**[9] A probabilistic framework for identifying safety critical events in naturalistic driving time series data**
- 組織・年・種別: Chalmers、2017（検索要約による）、論文
- URL: https://research.chalmers.se/en/publication/254471
- 確認方法: 抜粋のみ
- 要点（事実）: 固定閾値の代わりに、トリガ変数の同時確率分布から速度依存の閾値を作る。固定閾値は従来広く使われてきたと述べる
- 示唆: 【推察】CAN 信号は車種ごとに分布が違うため、SHRP2 の固定閾値を直接使わず、車種別・速度別の分布で較正する根拠になる

**[19] ヒヤリハット検出精度の検証結果（2024年報告）**
- 組織・年・種別: 国土交通省 国土技術政策総合研究所（NILIM）、2024、研究報告
- URL: https://www.nilim.go.jp/lab/bcg/siryou/2024report/ar2024hp043.pdf
- 確認方法: 抜粋のみ
- 要点（事実）: 交差点で検出指標と閾値を検証し、正解率・適合率・再現率・F値を交差点ごとに示している。歩行者・自転車対自動車では当事者間距離 6 m 以下を基準とする例がある。画像ベースの検出で加速度センサではない。具体的な数値は未取得
- 示唆: 日本でヒヤリハット検出を適合率・再現率で評価した事例。CAN のみ運用とは距離があるが、閾値の置き方の比較枠組みの参考になる【推察】。B-06（交差点）にも関連

**[R1][R2] 既出文献の再掲（内容は05と同一）**
- [R1] Perez ら 2017, Performance of basic kinematic thresholds ...（Accident Analysis & Prevention 103, 10–19）: https://www.sciencedirect.com/science/article/abs/pii/S0001457517301033 — 抜粋のみ。SHRP2 と CNDS で運動学閾値を検証、一部の閾値は事象を高率で検出できずサブセットを推奨。感度の具体値は未取得
- [R2] Sudweeks 2015, Using Functional Classification ...（VTTI/NSTSCE 15-UT-030）: https://vtechworks.lib.vt.edu/items/65032784-5c46-48e6-8d2e-12eb1964d3e9/full（同内容の別ページ: https://vtechworks.lib.vt.edu/items/version/16）— 抜粋のみ。ヨーレート機能分類器で crash 92%・near-crash 81% を保持し無効トリガを42%削減（05 [2] と同じ数値）。100-Car で約20個の運動学閾値が定義されたとの記載がある
- 件数上は「既出の再掲」に含め、新規ソースには数えない（[R3] を含め3件）

### 2.3 CAN 信号との対応・再現上の注意（サブ論点3）

**[1] ドライブレコーダ活用の報告書（dora-houkoku2）**
- 組織・年・種別: 国土交通省 自動車局、年は未確認（2009年前後の可能性）、官公庁報告書
- URL: https://www.mlit.go.jp/jidosha/anzen/03driverec/resourse/data/dora-houkoku2.pdf
- 確認方法: 抜粋のみ
- 要点（事実）: 急ブレーキ・急ハンドル・急アクセルの判定は加速度センサが担う。タクシー用構成例では車両側からブレーキ信号・ウインカー信号・車速パルス信号・電源が供給される。記録周期は項目ごとに異なり、加速度30 Hz、車速パルス2 Hz と記載されている（抜粋）
- 示唆: 【推察】車速パルス由来の減速度は 2 Hz 級では時間分解能が足りない。CAN の車輪速は通常これより高周期だが、周期は車種依存で未確認

**[2] 国交省 2009-06-30 報道発表資料（ドラレコ関連）**
- URL: https://www.mlit.go.jp/kisha/kisha06/09/090630_4/02.pdf
- 確認方法: 抜粋のみ（題名と URL のみで、要点は未確認）
- 示唆: ドラレコ急ブレーキ判定の国内資料候補。本文確認が必要

**[18] ドライブレコーダ関連資料（タクシー用機器の仕様）**
- 組織・年・種別: 国土交通省、年不明、行政資料
- URL: https://www.mlit.go.jp/common/000051538.pdf
- 確認方法: 抜粋のみ
- 要点（事実）: 加速度は前後・左右・上下の3方向を 100 Hz で記録する仕様が示されている。閾値の設定根拠の記述は無い
- 示唆: 閾値の根拠にはならず、サンプリング条件の参照のみ

**[17] 東京都 報告書（ドライブレコーダ関連）**
- 組織・年・種別: 東京都生活文化局、年不明、報告書
- URL: https://www.seikatubunka.metro.tokyo.lg.jp/documents/d/seikatubunka/houkokusyo
- 確認方法: 抜粋のみ
- 要点（事実）: 市販ドラレコは急減速・急ハンドルを加速度センサで検出する。段差の衝撃による誤検知が多いとされ、誤検知を減らす設計事例が挙げられている。数値は未取得
- 示唆: 【推察】CAN のみでは車体上下加速度が無いことが多く、路面起因の誤検出を抑える手段が限られる。上下加速度の有無は CAN 仕様次第で要確認

**[3] Analysis of the Conditions for the Occurrence of Sudden Braking using Drive Recorder Videos**
- 組織・年・種別: 東京農工大学の研究とされる（著者・年は未確認）、学術論文（CiNii）
- URL: https://cir.nii.ac.jp/crid/1390009714522138496
- 確認方法: 抜粋のみ（題名と URL の対応は未確認）
- 要点（事実）: ドラレコ DB の車速データは分解能が低いことが課題とされ、加速度から車速を高分解能・高サンプリングで推定する手法が検討されている（抜粋）
- 示唆: 【推察】国内ドラレコの車速由来減速度は量子化が粗い。CAN の車輪速との分解能差を整理する根拠になる

**[4] JP6213359B2 ドライブレコーダ及びドライブレコーダにおける加速度補正プログラム**
- 種別: 特許（出願人・年は未確認）
- URL: https://patents.google.com/patent/JP6213359B2/ja
- 確認方法: 抜粋のみ
- 要点（事実）: 加速度センサの設置角度がずれると正確な加速度が検出できず、補正が必要になる
- 示唆: 専用加速度計（SHRP2 DAS）と ECU 内蔵センサの差として取付軸ずれが効く。ECU 内蔵センサは車体固定のため補正の要否は車種依存【推察】

**[5] Speed and Acceleration Filters/Estimators for Powertrain and Vehicle Controls（SAE 2007-01-1599）**
- 組織・年・種別: SAE、2007、学会論文
- URL: https://saemobilus.sae.org/papers/speed-acceleration-filters-estimators-powertrain-vehicle-controls-2007-01-1599
- 確認方法: 抜粋のみ
- 要点（事実）: 速度・加速度・ジャークを離散状態方程式でモデル化しカルマンフィルタを適用。車両試験データで、顕著な遅れなしにノイズが低減したとされる
- 示唆: 【推察】車輪速→加速度→ジャークの微分ノイズ対策の候補。遅れが小さいことはトリガの時間窓判定との整合に重要

**[6] Second-order models and traffic data from mobile sensors**
- 組織・年・種別: arXiv:1211.0319、2012（番号から推定）、プレプリント
- URL: https://arxiv.org/pdf/1211.0319
- 確認方法: 抜粋のみ（arXiv は取得不可）
- 要点（事実）: 正則化微分とロバスト局所回帰を比較し、微分の階数が上がるほど2手法の推定が乖離する、つまり微分がノイズを増幅する
- 示唆: 【推察】ジャーク系トリガを CAN で再現するなら、加速度を直接出力する信号（ESC の縦Gなど）を優先する

**[7] Vehicle Speed Estimation Using Accelerometer and Wheel Speed Measurements（SAE 2002-01-2229 と思われる）**
- 組織・年・種別: SAE、2002、学会論文
- URL: https://saemobilus.sae.org/content/2002-01-2229
- 確認方法: 抜粋のみ（題名と番号の対応は未確認）
- 要点（事実）: ABS の車輪速センサと加速度計を組み合わせ、制動中の縦方向速度を推定する
- 示唆: 【推察】制動中は車輪スリップで車輪速由来の速度・加速度が車体運動と乖離しうる。ABS 作動時は車輪速微分の信頼度を落とすべき

**[8] Calibration of an Inertial Measurement Unit and Its Impact on Antilock Braking System Performance（SAE 2024-26-0014）**
- 組織・年・種別: SAE、2024、学会論文
- URL: https://saemobilus.sae.org/papers/calibration-inertial-measurement-unit-impact-antilock-braking-system-performance-2024-26-0014
- 確認方法: 抜粋のみ
- 要点（事実）: IMU 出力は車内の取付位置・姿勢の影響を受ける。較正により、生の IMU データに対して縦加速度の推定が94〜98%改善したとされる（抜粋記載）
- 示唆: 【推察】CAN 上の ECU 較正済み加速度は、較正前の生値より信頼できる可能性がある

**[10] Smartphone-based Hard Braking Events Detection at Scale for Road Safety Services**
- 組織・年・種別: Google Research、年は不明、論文
- URL: https://research.google/pubs/smartphone-based-hard-braking-events-detection-at-scale-for-road-safety-services/
- 確認方法: 抜粋のみ
- 要点（事実）: スマートフォンの運動データで学習したモデルを使い、学習には車両側センサとスマートフォンの同時計測データを用いる
- 示唆: 【推察】車両側信号を教師にする方式は「学習時のみ他センサ可」の方針と相性がよい

**[11] Method and device for detecting a panic braking operation（US 6623090）**
- 種別: 特許
- URL: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6623090
- 確認方法: 抜粋のみ
- 要点（事実）: 車輪速の変化量を閾値と比較して急制動を検出する。路面の凹凸がある場合は検出を止める仕組みを含む（抜粋）
- 示唆: 【推察】路面凹凸による車輪速変動が誤検出の原因になる

**[24] Smartphones vs. in-vehicle data acquisition systems as tools for naturalistic driving studies: A comparative review**
- 著者・組織: Grimberg ら（検索抜粋記載）、レビュー論文
- URL: https://cris.iucc.ac.il/en/publications/smartphones-vs-in-vehicle-data-acquisition-systems-as-tools-for-n-2/
- 確認方法: 抜粋のみ
- 要点（事実）: スマートフォンは運転スタイル研究には向くが、事故再構成や短期の事象間関係には弱い、という結論（抜粋）
- 示唆: 【推察】車載データはイベントのタイミング精度で有利

## 3. SHRP2 トリガ表の確認状況（12種）
| トリガ | 確認できた内容 | 状態 |
|---|---|---|
| 前後減速度 | 有効事象の割合が最も高い（[R3]）。閾値・継続は05 §2・§3.1 の二次整理を参照 | 一次未確認 |
| 高速道路減速度、ジャーク、横加速度、ヨーレート（反転）、ABS/ESC/TCS、操舵回避、CI ボタン、前方 TTC など | 本書では新たな数値を確認できず | 一次未確認 |
| 後処理（自己相関によるノイズ除去、2 s 窓での統合） | 05 [1] の記載のみ。他ソースでの確認なし | 一次未確認 |

表番号・ページ番号は取得できていない。商用車プロジェクト（VTTI）のトリガ表を引く検索要約（前後加速度 15 mph 以上で 0.35 g、以下で 0.5 g など）が出たが、URL を個別に確認できず SHRP2 の表でもないため載せない。

## 4. 統合アーキテクチャ（12）への反映点
- L3（R1・R2）: 縦加速度の入力は ESC 縦G > 車輪速1階微分の優先順で定義し、ジャークは平滑化後に1階だけ微分する【推察】。ABS/ESC 作動フラグで車輪速微分のゲートをかける【推察】
- L1: 加速度信号の取付軸ずれ・符号規約・サンプリング周期・分解能を車種プロファイルとして持つ。SHRP2 の固定閾値は車種別・速度別の分布で較正する（[9]）【推察】
- L6: ラベル定義に SHRP2 トリガを使う場合、閾値の一次確認が済むまで 05 §2 の値を「暫定」と明記する。TTC 系は誤報が多い報告があるため、単独トリガにせず減速度と併用する（[16]）

## 5. 課題・ギャップ
- SHRP2 Baseline Report のトリガ表の行ごとの値（信号・閾値・継続・最低車速・ページ）は未確認
- トリガ別の感度・適合率・再現率の数値は未発見。Perez ら2017（[R1]）の本文に載っている可能性がある
- ESC/ABS 加速度信号の CAN 上の分解能・周期・量子化の公開資料、CAN 縦加速度と専用加速度計の一致度を検証した論文、SHRP2 DAS の加速度計・ジャイロの仕様は見つからなかった
- 全ソースが抜粋のみ。取得不可のホストが解消するまで数値は暫定

## 6. 次のアクション提案
1. ネットワーク許可（vtechworks.lib.vt.edu、onlinepubs.trb.org、www.mlit.go.jp、saemobilus.sae.org、sciencedirect.com、research.chalmers.se）後に、Baseline Report の PDF から12行の表を取得する（B-19）
2. Perez ら2017（[R1]）の本文から閾値別の感度表を取る
3. 手元の CAN ログ（comma2k19 など公開データ）で、ESC 縦G と車輪速微分の一致度を測り、ABS 作動時の乖離を定量化する【推察】
4. SHRP2 DAS の加速度計・サンプリング仕様を Baseline Report 本文で確認する

## 7. 参考文献リスト
本文中の URL を参照（[1]〜[24]、[R1]〜[R3]）。補助として [22] FHWA-HRT-24-070、[23] SHRP2 Project Brief を含む。
