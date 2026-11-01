# テーマ5: ヒヤリハット（ニアミス）検知・代理安全指標・事故リスク予測モデル

- 調査日: 2026-11-01
- テーマのゴール: 有人運転車両において、CANバス由来の信号（車速、ステアリング角、アクセル開度、ブレーキ圧、ヨーレート、前後/横加速度、ウインカー、ADAS警報フラグ、レーダ前方車両距離/相対速度）"のみ"で、ニアミスを定義・検出し、事故の予兆を予測する方法を文献に基づいて整理する。
- 表記ルール: 出典に基づく事実には出典番号 [n] を付す。筆者の推論・設計提案には「【推察】」を付す。数値は一次資料（本文PDF）で確認できたものと、抄録・二次資料でのみ確認できたものを区別して記載する。

---

## 1. エグゼクティブサマリー

1. 自然運転研究（100-Car, SHRP2, UDRIVE, 東京農工大ヒヤリハットDB）では、ニアミスは「衝突回避のために急速な回避操作（制動・操舵・加速）を要した事象」と定義され、候補抽出は前後加速度・横加速度・ヨーレート・ジャーク・ABS/ESC作動などの運動学的トリガで行われている [1][2][5]。トリガ信号の大半はCANで取得可能である。
2. ただしトリガ単独の適合率は低い。SHRP2では最も成績の良い前後減速度トリガ（≤-0.65G）でも、候補のうち有効事象は22%にとどまった [1]。100-Carでは無効:有効の比が前後加速度で約2:1、前方TTCで約5:1、ヨーレートで約51:1であった [2]。そのためCANだけで運用する場合は、トリガの組合せ、信号の機能的分類、学習モデルによる二次判定が欠かせない。
3. 減速度閾値は研究により-0.3Gから-0.75Gまで幅がある（-0.45Gが若年ドライバ研究や農工大DBのトリガ値、-0.65GがSHRP2初期スクリーニング値など）[3][5][13][21]。閾値を一律に決めず、目的（網羅的な抽出か高適合率か）と道路種別に応じて設定すべきである。
4. 代理安全指標（TTC/THW/DRAC/MTTC）は前方レーダの距離・相対速度がCANに流れていれば計算できる。一方、PETは交差する相手の軌跡が必要なので、CANだけでは計算できない。Luら（2021）は6指標を比較し、精度・即時性・頑健性・効率のすべてで優れる単一指標はないと結論している [4]。
5. 機械学習による予測では、運動学データのみで約1秒先のニアミスを高精度に予測した報告がある（AdaBoost、予測ホライズン1 s・観測窓3〜4 s）[6][7]。ラベルなしで学習する一般化代理安全指標（GSSM）は、PR-AUC 約0.9、中央値2.6 sの先行時間を報告している [8]。ただし、どの報告も偽警報率（単位時間・距離あたり）をほとんど示していない。
6. EDRの事故前5秒データ解析では、追突側の約20%が無制動であり、制動開始時のTTCは平均1.1〜1.4 sであった [16]。NHTSAは5秒では回避操作の開始を捉えきれないとして、事故前記録を20秒・10 Hzへ延長する規則を2024年に最終化した（2027年9月から適用）[17]。【推察】事故の予兆検知には少なくとも10〜20秒の事前窓を使うべきである。
7. ドライバ単位では、クリティカルインシデント率や高G事象率が将来の事故・ニアミスリスクの有力な予測因子である（高リスクドライバ判別でAUC 0.938 [12]、前月の高G事象率が翌月の事故リスクを上げ、OR=1.07 [14]）。【推察】リアルタイム警報と、ドライバ単位のリスクスコアリングとの二層構成が現実的である。

---

## 2. 代理安全指標（Surrogate Safety Measures）・運動学的トリガ一覧

記号: D=車間距離 [m]、v_f=自車速度、v_l=先行車速度、a_f / a_l=自車 / 先行車の加速度、Δv=v_f−v_l、Δa=a_f−a_l。
CAN可否: ◎=自車センサのみで可能、○=レーダ情報がCANに流れていれば可能、△=推定を伴えば部分的に可能、×=CANのみでは不可。

| 指標 | 定義式・概要 | 典型閾値（出典） | CAN可否 | 出典 |
|---|---|---|---|---|
| TTC（Time To Collision） | TTC = D / Δv（Δv>0のとき）。現在の速度と進路を保った場合に衝突するまでの時間 | 1.5 s（FHWAのSSAMが提案した値として引用 [23]）。臨界値は文献により1.5〜4 sと幅がある [23]。4 sを安全と不快の境界、1.5 s以下を重度コンフリクトとする整理もある（Kongらのレビュー [3]） | ○（レーダの距離・相対速度） | [3][22][23] |
| MTTC（Modified TTC） | 相対加速度を考慮し、D = Δv·t + ½Δa·t² を満たす最小の正のtとする | 本調査では一次資料の閾値を確認できなかった。TTCが閾値を下回った際の補助指標として使われる [3] | ○（先行車加速度は相対速度の微分で推定） | [3] |
| THW（Time Headway） | THW = D / v_f | 0.4 s未満をtailgating（煽り）とする例がある（Kongらのレビュー [3]）。追従時のTHWを「急ぎ運転」検出の特徴量に用いた研究もある [25] | ○ | [3][25] |
| DRAC（Deceleration Rate to Avoid Crash） | DRAC = Δv² / (2D)。衝突を避けるために必要な最小減速度 | 3.35 m/s²（Archer 2005 を引用 [23]） | ○ | [23] |
| CPI（Crash Potential Index） | DRACが車両の最大減速能力を超える時間の割合 | — | △（路面μが不明なので最大減速度を仮定する） | [22]（DRACの拡張として言及） |
| PET（Post-Encroachment Time） | 先行者が交錯点を離れてから後続者が到達するまでの時間 | — | ×（相手の軌跡と交錯点が必要） | [22] |
| 前後減速度 | 前後加速度 a_x ≤ 閾値 | -0.3G（SHRP2の高速道路限定トリガ [1]、国交省中部の相関分析 [21]）／-0.45G（若年ドライバ研究 [13]、農工大DBのトリガ0.45G [19]）／-0.5G（国交省中部のヒヤリハット定義 [21]）／-0.6G（100-Carの候補事故基準、Kongらによる引用 [3]）／-0.65G（SHRP2 [1]）／-0.75G（Perezら2017の推奨、Kongらによる引用 [3]） | ◎ | [1][3][13][19][21] |
| 前後加速度（急発進） | a_x ≥ 閾値 | 0.35G [13]、0.50G [1] | ◎ | [1][13] |
| 横加速度 | \|a_y\| ≥ 閾値 | 0.50G [13]、0.75Gを0.2 s以上継続 [1] | ◎ | [1][13] |
| ヨーレート | 正負反転・振幅 | ±6 deg/s [13]。±8 deg/sから逆向き±8 deg/sへ0.75 s以内に反転、13.4 m/s以上（SHRP2。自己相関による雑音除去を併用）[1] | ◎ | [1][13] |
| スワーブ | ヨー角加速度が1周期の正弦波形で±15 deg/s²を2 s以内に超える、5 m/s以上 | 同左 [1] | ◎ | [1] |
| 前後ジャーク | da_x/dt | -1.0 g/s未満が1 s継続、5 m/s以上（SHRP2）[1]。Bagdadiらはpeak-to-peakジャークを提案した [10] | ◎（微分による雑音増幅に注意） | [1][10] |
| 横ジャーク（操舵回避） | \|da_y/dt\| | 1.0 g/sを0.8 s継続、5 m/s以上（SHRP2）[1] | ◎ | [1] |
| 安全装置作動 | ABS、ESC、TCS、エアバッグ作動フラグ | 作動の有無（SHRP2）[1] | ◎（車種依存） | [1] |
| 高G事象率 | 走行距離あたりの急制動・急発進・急旋回の回数 | 上記閾値を用いた月次の発生率 [13][14] | ◎ | [13][14] |
| クリティカルインシデント率 | 距離あたりのクリティカルインシデント件数 | ドライバのリスク層別に使用 [12] | △（インシデントの判定が必要） | [12] |

補足:
- 1D（直線追従）を前提とするSSMは、TTCが非臨界域では約300%、臨界域（1.5 s未満）でも約20%ずれうる。3D化した一般化枠組みが提案されている [22]。【推察】CANだけの環境では横方向の相対位置が得られないため、カーブや車線変更の場面ではTTC/DRACが過大または過小になりうる。
- 100-Carの「制動0.5G超、または横加速度0.4G超を急速な回避操作の目安とする」という基準は二次資料でしか確認できなかったため、表には入れていない。

---

## 3. 主要知見（ソースごと）

### 3.1 自然運転研究におけるcrash / near-crashの定義とトリガ

#### [1] Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets
- 著者/組織: J.M. Hankey, M.A. Perez, J.A. McClafferty（VTTI）
- 年 / 種別: 2016 / 技術報告書
- URL: https://vtechworks.lib.vt.edu/handle/10919/70850 （PDF: https://vtechworks.lib.vt.edu/bitstream/handle/10919/70850/SHRP_2_CrashNearCrashBaselineReport_4-25-16.pdf?sequence=1 ）
- データ: SHRP2 NDS。約3,400人、5,512,900トリップファイル。DASが車両ネットワーク（速度、ブレーキ、アクセル）、前方レーダ、加速度計を記録。
- 手法: 12種のトリガを実行し、全候補を映像で人手検証した。重大な運動学的特徴を持つ候補から順に検証した。
- 定義:
  - Crash: 運動エネルギーの授受を伴う接触。意図しない路外逸脱を含む。Level 1（エアバッグ展開、負傷、横転、高Delta-V（20 mph超、または±2 G超）、レッカー移動）からLevel 4（低リスクのタイヤ接触）まで4段階。
  - Near-crash: 回避のために急速な回避操作を要した事象。非接触・非計画的・回避が必要・急速性の4要件を満たす。
  - Crash-Relevant Conflict（CRC）: near-crashより緊急度が低い回避を要した事象。
- 結果: 有効事象はcrash 1,549件、near-crash 2,705件。ベースラインは32,586件。主なトリガの有効率（crash/NC/CRCを含む）は、前後減速度（≤-0.65G）22%、高速道路減速度（≤-0.3G）8%、ABS 4%、ヨーレート3%、横加速度2%、前後加速度2%、ESC・TCS・操舵回避 各1%。乗員が押すCIボタンは15%。
- 示唆: SHRP2のトリガ定義（表2.1）は、CAN信号だけで再現できる具体的な仕様として最も参考になる。複数トリガを2 s窓で統合する、ヨーレートの雑音を自己相関で除去する、最低車速条件を付ける、といった工夫はそのまま流用できる。【推察】有効率22%は、CAN単独で警報を出すと約8割が誤報になる水準を意味する。

#### [2] Using Functional Classification to Enhance Naturalistic Driving Data Crash/Near Crash Algorithms（100-Carトリガ性能）
- 著者/組織: J. Sudweeks（VTTI / NSTSCE）
- 年 / 種別: 2015 / 技術報告書（Report 15-UT-030）
- URL: https://vtechworks.lib.vt.edu/bitstreams/5ac3b5e4-7c35-4dd8-9d40-c3534bc4ad40/download
- データ: 100-Car NDS。約20種の運動学的閾値で12万件超のトリガが発生し、有効は約11,500件。事象はcrash 68件、near-crash 760件、critical incident 8,295件。
- 結果: 無効:有効の比は、前後加速度約2:1、前方TTC約5:1、ヨーレート約51:1。前後加速度トリガは有効トリガの約32%を占めた一方、無効トリガに占める割合は約6%にとどまった。前方TTCは有効の約47%を占めたが、無効の19%も占めた。ヨーレート波形を関数データとして分類する手法では、crashの92%とNCの81%を保持したまま、無効トリガを42%削減した。
- 示唆: 閾値超過の有無だけで判定せず、波形の形状を分類すれば誤検出を大きく減らせる。CAN時系列への適用は容易である。

#### [3] Patterns of near-crash events in a naturalistic driving dataset: Applying rules mining
- 著者: X. Kong, S. Das, H. Zhou, Y. Zhang
- 年 / 種別: 2021 / 査読論文（Accident Analysis & Prevention 161, 106346）
- URL: https://subasish.github.io/ait_lab/pdfs/2021%20(A)%20Kong%20AAAP%20Near-crash%20using%20Rules%20Mining.pdf
- データ: Safety Pilot Model Deployment（SPMD、ミシガン州、92台・約35,000マイル）のDAS前後加速度と道路台帳（HPMS）。
- 手法: 前後減速度が-0.45G以下の事象をnear-crashとし、-0.75G以下をnon-trivialに区分した。先行車がいない場合は除外し、3分以上離れた制動を別事象として扱った。957事象にAprioriアソシエーションルールを適用した。
- 文献整理（二次情報として有用）: 近接事象の識別に使われた減速度閾値として、-0.45G（Simons-Mortonら、AASHTOグリーンブック）、-0.6G（100-Car候補事故、Dingusら2006）、-0.65G（SHRP2初期スクリーニング）、-0.75G（Perezら2017がSHRP2/CNDSで推奨）を挙げている。SHRP2ではnear-crashの方がcrashより平均0.018G強く減速していた（Wood & Zhang 2021）という知見も紹介している。TTC 4 s／1.5 s、tailgating THW 0.4 sも挙げている。
- 結果: 2時間を超えるトリップではnon-trivial near-crashが起きやすかった。中央分離帯や路肩のない低規格道路ではtrivial near-crashが多かった。
- 示唆: 減速度閾値の比較表を作る際の起点になる。【推察】トリップ継続時間（疲労の代理変数）はCANから得られるリスク特徴量になる。

#### [5] UDRIVE: Evaluation of safety critical event triggers in the UDRIVE data
- 組織: UDRIVE（EU FP7）コンソーシアム
- 年 / 種別: 2017頃 / 査読論文・プロジェクト報告（検索結果で存在を確認。本文は未取得）
- URL: https://swov.nl/en/publicatie/evaluation-safety-critical-event-triggers-udrive-data
- 要点（抄録レベル）: 欧州5か国・約200万kmの自然運転データについて、安全上重要な事象（SCE）を検出する運動学的トリガを記述している。生データが膨大なので、誤検出の手作業確認コストを抑えるためにトリガ性能の評価が重要だと論じている。
- 示唆: 欧州でも閾値トリガと映像による確認という構成は共通している。

#### [19] 出会い頭ニアミスにおける非優先道路側の対象車の状態による影響（東京農工大ヒヤリハットDBの利用例）
- 著者/組織: 鈴木大雅、丸茂喜高、風間恵介（日本大学）、毛利宏（東京農工大学）
- 年 / 種別: 2024 / 学術講演会概要（日本大学生産工学部 第57回）
- URL: https://www.cit.nihon-u.ac.jp/laboratorydata/kenkyu/kouennkai/reference/No.57/pdf/2-34.pdf
- データ: 東京農工大学スマートモビリティ研究拠点ドライブレコーダデータセンターのヒヤリハットDB。タクシーに搭載したドライブレコーダで、札幌・秋田・東京・静岡・福岡の5都市から2005〜2023年に21.5万件を収録。記録項目は前方・車内映像、加速度、速度、ブレーキ、ウインカ、GPS、音声。
- トリガとレベル: 前後・左右加速度が0.45Gに達すると、トリガ前10 s・後5 sの計15 sを自動記録する。ヒヤリハットのレベルは、回避操作が1.0 s未満遅れただけで事故になったと思われるものを「高」、1.0〜2.0 sを「中」、2.0 s以上を「低」としている。出会い頭・対乗用車の条件で、高897件、中8,727件が抽出された。
- 示唆: 日本の代表的なヒヤリハットDBは、トリガ値（0.45G）、記録窓（-10 s〜+5 s）、重大度の定義（想定される遅れ時間）が明確である。【推察】CANログでも同じトリガと窓長を採用すれば、このDBの知見と比べやすくなる。

#### [20] 統計的機械学習を用いたプローブカーデータからのヒヤリハット発生形態の推定
- 著者/組織: 森村哲郎、井手剛（IBM東京基礎研究所）、谷澤祐介、山崎慎也（マツダ）
- 年 / 種別: 2011 / 自動車技術会 秋季学術講演会
- URL: https://ide-research.net/papers/2011_JSAE_Morimura.pdf
- データ: ヒヤリハット発生の10 s前から5 s後までを30 Hzで記録したプローブカーデータ。速度、前後・横加速度、ブレーキ、ウインカ、GPS。右折時の高・中レベル事例160件（右直80件、右折先の歩行者・自転車80件）。
- 手法: 統計的機械学習で有効な特徴量を選び、発生形態を分類した。
- 結果: 有効な特徴量を同定でき、形態分類に有望な結果を得たと報告している（抄録レベル）。
- 示唆: 映像を使わず、車両挙動とドライバ操作の時系列からニアミスの「型」を分類できる可能性を示している。CAN信号と近い構成である。

#### [24] Estimation of Dangerous Routes using the Near-miss Incident Data of Probe-car
- 著者: 山崎慎也、船久保明、谷澤祐介
- 年 / 種別: 2011 / 査読論文（自動車技術会論文集 42(2), 639-644）
- URL: https://www.jstage.jst.go.jp/article/jsaeronbun/42/2/42_2_639/_article/-char/en
- 手法: ヒヤリハットと通常の減速を、ジャークと最大減速度で判別する手法を提案した。JSAEヒヤリハットDBと意図的な減速データで検討した。
- 結果: 広島市の事故多発交差点3か所で、経路別ヒヤリハット頻度の傾向が死亡事故頻度と類似した。
- 示唆: 減速度だけでなくジャークを組み合わせると、通常の制動と区別しやすくなる。この結論はBagdadiら [10] と一致する。

#### [21] プローブデータの交通安全対策への活用について
- 著者/組織: 山田浩、市川英敏、片野裕介（国土交通省 中部地方整備局）
- 年 / 種別: 平成22年度（2010）国交省 技術研究発表会 / 行政報告
- URL: https://www.mlit.go.jp/chosahokoku/h22giken/program/kadai/pdf/ippan/ippan1-06.pdf
- 定義: 40 km/hから約2 sで急停止する程度の減速を基準に、「0.5G以上の負の前後加速度を伴う減速」をヒヤリハットと定義した。国道23号の相関分析では、データ量を増やすため0.3Gに下げた。
- 結果: 県全域ではヒヤリハット地点と事故の相関は低かった。データが豊富な特定路線（100 m区間単位）に限ると概ね相関が見られた。一律0.5Gの定義が実際の危険回避行動を表しているかは検討の余地がある、と著者自身が述べている。
- 示唆: 閾値の選び方とデータ量によって、事故との対応関係が変わる。

#### [26] 東京農工大学 学長記者会見資料「個別適合型の先急ぎ運転警報つきドライブレコーダの開発」
- 組織: 東京農工大学（永井正夫、道辻洋平）
- 年 / 種別: 2008 / 大学発表資料
- URL: https://www.tuat.ac.jp/documents/tuat/outline/disclosure/pressrelease/2008/20090223162216812265831.pdf
- 要点: ドライブレコーダの世代を、事故映像の記録、ヒヤリハット映像の記録（JSAEのDB約3万件）、不安全行動の常時記録の順に整理している。加減速が0.3Gを超えたときに警報する方式に加え、過去のトリップから作ったドライバ個人の加減速の度数分布に基づいて閾値を変える「個別適合型」警報を提案している。
- 示唆: 閾値をドライバごとに適応させる発想は、後年の個人化閾値研究 [15][9] につながる。

### 3.2 ニアミスと事故の関係・ドライバリスク

#### [11] Near Crashes as Crash Surrogate for Naturalistic Driving Studies
- 著者: F. Guo, S. Klauer, J. Hankey, T. Dingus
- 年 / 種別: 2010 / 査読論文（Transportation Research Record 2147, 66-74）
- URL: https://trid.trb.org/view/1353218
- 要点: 100-Carデータで、crashとnear-crashの寄与要因の頻度には正の関係があった。両者をまとめて解析すると、寄与要因のリスクを一貫して過小評価する一方、推定の精度は上がる。
- 示唆: 事故が少ない小規模データでは、ニアミスを代理指標として使うことに妥当性がある。ただしリスク推定値は保守的（過小）になる。

#### [27] What is the relation between crashes from crash databases and near crashes from naturalistic data?
- 著者: M. Dozza（Chalmers）
- 年 / 種別: 2020 / 査読論文（Journal of Transportation Safety & Security 12(1)）
- URL: https://research.chalmers.se/publication/511868
- 要点: 自転車の自然走行データを対象に、ニアミスと事故の関係は未解明であり、ニアミスを代理指標とすることの是非は議論が続いていると述べ、曝露データでリスク水準を付与する手法を提案している。

#### [12] Individual driver risk assessment using naturalistic driving data
- 著者: F. Guo, Y. Fang（VTTI）
- 年 / 種別: 2013 / 査読論文（Accident Analysis & Prevention 61, 3-9）
- URL: https://pubmed.ncbi.nlm.nih.gov/22785091/
- データ / 手法: 100-Car。負の二項回帰、k-meansによる3層化、ロジスティック回帰。
- 結果: 高リスク層（約6%、1,000マイルあたりcrash/NC 3.95件）、中リスク層（約12%、1.75件）、低リスク層（約84%、0.39件）に分かれた。予測AUCは高リスク判別0.938、中リスク判別0.930。クリティカルインシデント率が高リスクドライバの有効な予測因子だった。
- 示唆: 【推察】CANで検出した軽微なインシデント（急制動など）の頻度を、ドライバ単位のリスク指標として使える。

#### [13] Trajectories of Kinematic Risky Driving Among Novice Teenagers
- 著者: B.G. Simons-Morton, K. Cheon, F. Guo, P. Albert
- 年 / 種別: 2013 / 査読論文（Accident Analysis & Prevention 51, 27-32）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3556237
- 閾値: 急制動≤-0.45G、急発進≥0.35G、左右旋回|a_y|≥0.50G、ヨーレート±6 deg/s。
- 結果: 新規免許取得者42人を18か月追跡した。高リスク層と低リスク層の2クラスに分かれ、高リスク層の約9割が各6か月期間で中央値を上回り続けた（個人の傾向は持続する）。

#### [14] Do elevated gravitational-force events while driving predict crashes and near crashes?
- 著者: B.G. Simons-Morton, Z. Zhang, J.C. Jackson, P.S. Albert
- 年 / 種別: 2012 / 査読論文（American Journal of Epidemiology 175(10), 1075-1079）
- URL: https://experts.llu.edu/en/publications/do-elevated-gravitational-force-events-while-driving-predict-cras/
- 結果（抄録の検索結果で確認）: 前月の高G事象率が高いと、翌月の事故リスクが上がった（OR=1.07、95%CI 1.02-1.12）。事故・ニアミスと高G事象率の相関は0.60。GEEロジスティック回帰を用いた。AUCは一次資料で確認できなかった（同著者の発表スライドでは0.7367）。
- 示唆: 高G事象の「率」は将来リスクのマーカーになる。ただし著者は、高G事象が事故の原因だと主張しているわけではない。

### 3.3 キネマティックトリガの性能・改良

#### [9] Performance of basic kinematic thresholds in the identification of crash and near-crash events within naturalistic driving data
- 著者: M.A. Perez, J.D. Sudweeks, E. Sears, J. Antin, S. Lee, J.M. Hankey, T.A. Dingus
- 年 / 種別: 2017 / 査読論文（Accident Analysis & Prevention 103, 10-19）
- URL: https://insurancenewsnet.com/oarticle/findings-on-risk-management-reported-by-investigators-at-virginia-tech-performance-of-basic-kinematic-thresholds-in-the-identification-of-crash-and （抄録紹介記事。書誌はKongら [3] の参考文献でも確認）
- 要点: SHRP2とカナダNDS（CNDS）で基本的な運動学閾値を開発・検証した。多くの手法の感度はかなり低いが、検出性能に基づいて閾値水準を選べば改善できる。Kongら [3] によれば、-0.75Gへの引き上げでスクリーニング性能が向上すると示唆している。
- 示唆: 閾値はデータに基づいて最適化すべきである。

#### [10] Development of a method for detecting jerks in safety critical events
- 著者: O. Bagdadi, A. Várhelyi（Lund大学）
- 年 / 種別: 2013 / 査読論文（Accident Analysis & Prevention 50, 83-91）
- URL: https://lup.lub.lu.se/record/3347798
- 要点: 時間的余裕のない場面でドライバが行う制動の特徴に基づき、負のジャークとpeak-to-peakジャークを比較した。提案法は「危険」と「潜在的危険」の事象をより明確に分けた。検索結果によれば、後続研究で100-Carの637件のnear-crashに適用したところ、加速度法の約1.6倍の成功率だった（二次情報）。
- 示唆: CANの前後加速度（またはブレーキ圧）の微分から得るジャークは、ニアミス判定の有力な特徴量である。

#### [28] Recognizing safety-critical events from naturalistic driving data（Dozza & Pañeda González）
- 著者: M. Dozza, N. Pañeda González（Chalmers）
- 年 / 種別: 2013 / 査読論文（Accident Analysis & Prevention 60, 298-304）。元は2011年修士論文と2012年Procedia論文
- URL: https://research.chalmers.se/en/publication/173520
- 要点: 運動学的トリガによる絞り込みは感度・特異度が低く、映像の人手確認が必要になっている。euroFOT（Volvo車100台）の約400件のトリガ映像を確認し、ドライバの反応がSCE判別の鍵になりうると結論した。ドライバ映像の自動処理を加えるとnear-crash認識の感度が上がった。
- 示唆: 【推察】本プロジェクトは映像を使わないので、「ドライバの反応」を、CANから得られるペダル踏み替え時間、ブレーキ圧の立ち上がり、操舵速度などで代替する設計が鍵になる。

### 3.4 事故・ニアミス予測モデル

#### [6] Crash and Near-Crash Prediction from Vehicle Kinematics Data: A SHRP2 Naturalistic Driving Study
- 著者: O.A. Osman, M. Hajij, S. Karbalaieali, S. Ishak
- 年 / 種別: 2018 / 学会発表（TRB 97th Annual Meeting, 18-03927）
- URL: https://trid.trb.org/View/1496022
- データ: SHRP2の速度、前後・横加速度、ヨーレート、ペダル位置。いずれもCANで取得可能な信号である。
- 手法: KNN、RF、SVM、DT、AdaBoost、MLP、QDA、カーネルSVM。
- 性能: AdaBoostとカーネルSVMが、予測ホライズン約1 s、変動ホライズン（観測窓）約4 sで約90%の精度だった。適合率・再現率の記載はない（抄録レベル）。

#### [7] Prediction of Near-Crashes from Observed Vehicle Kinematics using Machine Learning
- 著者: O.A. Osman, M. Hajij, P.R. Bakhit, S. Ishak
- 年 / 種別: 2019 / 査読論文（Transportation Research Record, DOI 10.1177/0361198119862629）
- URL: https://www.bohrium.com/paper-details/prediction-of-near-crashes-from-observed-vehicle-kinematics-using-machine-learning/812751158522150912-4628
- 性能: 予測ホライズン1 s・観測窓3 sで最適だった。AdaBoostが再現率100%、適合率98%、F1 99%（抄録）。
- 示唆: 【推察】この精度は、事象とベースラインを均衡サンプリングした評価だと考えられる。実走行でのベース率（ニアミスは極めて稀）では適合率が大きく下がるおそれがある。予測ホライズン1 sは、人の反応時間を考えると警報としては短い。

#### [29] Risk Levels Classification of Near-Crashes in Naturalistic Driving Data
- 著者: H.A.H. Naji, Q. Xue, N. Lyu, X. Duan, T. Li
- 年 / 種別: 2022 / 査読論文（Sustainability 14(10), 6032）
- URL: https://ideas.repec.org/a/gam/jsusta/v14y2022i10p6032-d816665.html
- 手法: 階層クラスタリングでnear-crashのリスク水準を定義し、adaptive lassoで要因を選択した。ML、DL、統計モデルを比較した。
- 性能: LSTMが最良で、精度96%、再現率0.93、適合率0.88、F1 0.91。
- 示唆: ニアミスの「重大度」を多段階で予測する場面でも、時系列DLが有利だった。

#### [30] A CNN-LSTM-Attention Model for Near-Crash Event Identification on Mountainous Roads
- 著者: Zhaoら
- 年 / 種別: 2024 / 査読論文（Applied Sciences 14(11), 4934）（検索結果で確認。本文は未取得）
- URL: https://doaj.org/article/8a0de17d5f6c4982863efadd908e15de
- データ: 中国雲南省山岳路の自然運転データ（速度、前後・横加速度など）。
- 性能: 全体精度98.8%、near-crash適合率90.1%（検索結果の抄録要約による）。
- 示唆: 「識別」タスク（事後検出）では、CANと同種の信号で高い性能が得られている。

#### [8] Learning collision risk proactively from naturalistic driving data at scale（GSSM）
- 著者: Y. Jiao, S.C. Calvert, S. van Cranenburgh, H. van Lint（TU Delft）
- 年 / 種別: 2025（v5は2026年3月）/ プレプリント（arXiv 2505.13556。Nature Machine Intelligence 掲載とされる）
- URL: https://arxiv.org/abs/2505.13556
- 手法: 一般化代理安全指標（GSSM）。事故やリスクのラベルを使わず、自然運転データから衝突リスクを学習する。
- 性能: 瞬時の運動学だけを使う基本版でも、実世界のcrash/near-crash 2,591件でPR-AUC 約0.9、衝突までの先行時間の中央値2.6 s。追突・合流・右左折のいずれでも既存ベースラインを上回り、相互作用や文脈の特徴を加えるとさらに向上した。
- 示唆: ラベル不足という最大の問題に対する有力な方向性である。【推察】入力に周辺車両の相対状態を必要とするので、CANだけの場合は前方レーダの1対象に限った縮退版になる。

#### [31] Comparison-Based Ordinal Learning for Proactive Driving Risk Assessment
- 著者: Zhuoren Liら
- 年 / 種別: 2026 / プレプリント（arXiv 2607.11128）
- URL: https://arxiv.org/abs/2607.11128
- 手法: フレーム単位のリスクラベルを使わず、ペア比較から相対的なリスク順序を学習する。ペアは、危険シーケンス内の時間進行、危険と通常の対比、物理的な反実仮想摂動から作る。100-Carの5分割交差検証で学習し、SHRP2 crashで分布外評価した。
- 性能: 抄録によれば、代理指標ベースのベースラインに対して、高再現率域での判別、警報の適合率、警報リードタイムがいずれも改善した（具体的な数値は未確認）。
- 示唆: 希少事象の問題を、ラベル設計（順序学習）の側から回避するアプローチである。

#### [15] How Much Is Too Much? Adaptive, Context-Aware Risk Detection in Naturalistic Driving
- 著者: A.H. Kalantari, E. Papadimitriou, A. Zgonnikov, A.P. Afghari（TU Delft）
- 年 / 種別: 2025 / プレプリント（arXiv 2508.00888）
- URL: https://arxiv.org/abs/2508.00888
- 手法: ローリング窓でラベルとモデルを時間・ドライバに応じて適応させる。安全指標には速度加重ヘッドウェイと急挙動イベントを用い、RF、XGBoost、DNNとそのアンサンブルを比較した。
- 結果（定性）: 速度加重ヘッドウェイの方が、急挙動イベント数より安定して文脈に即した分類を与えた。XGBoostは閾値変更に頑健で、DNNは低閾値で再現率が高い代わりにばらつきが大きかった。アンサンブルは反応性と誤警報抑制のバランスを取った。
- 示唆: 固定閾値ではなく、文脈とドライバに適応する閾値が誤警報の抑制に有効である。

#### [32] Unsupervised Learning for Detection of Rare Driving Scenarios
- 著者: D. Le, T. Manhardt, M. Venator, J. Betz
- 年 / 種別: 2025 / プレプリント（arXiv 2512.23585）
- URL: https://arxiv.org/abs/2512.23585
- 手法: 車両ダイナミクスと環境条件のスライディング窓統計特徴にDeep Isolation Forestを適用し、t-SNEで可視化した。定量指標と映像フレームの定性確認を組み合わせた代理正解で評価した。
- 示唆: ラベルなしで稀で危険なシナリオを抽出する。【推察】CAN特徴量だけでも、異常度スコアをニアミス候補の一次スクリーニングに使える。

#### [33] Driving Behavior Analysis through CAN Bus Data in an Uncontrolled Environment
- 著者: U. Fugiglando ほか（MIT Senseable City Lab / Audi）
- 年 / 種別: 2017 / プレプリント（arXiv 1710.04133）
- URL: https://arxiv.org/abs/1710.04133
- データ: 64人・10台・2,000トリップ超のCAN（アクセル、ブレーキ圧、操舵角、操舵モーメント、速度、RPM、前後・横加速度）。
- 手法: 教師なしクラスタリングでドライバを分類し、頑健なクラスタリングに必要な最小データ量を算出した。
- 示唆: CANのみによるドライバ行動の層別は実データで実証されている。

### 3.5 事故前挙動・EDR

#### [16] Method for Estimating Time to Collision at Braking in Real-World, Lead Vehicle Stopped Rear-End Crashes for Use in Pre-Crash System Design
- 著者: K.D. Kusano, H.C. Gabler（Virginia Tech）
- 年 / 種別: 2011 / 査読論文（SAE Int. J. Passeng. Cars - Mech. Syst. 4(1)）
- URL: https://saemobilus.sae.org/articles/method-estimating-time-collision-braking-real-world-lead-vehicle-stopped-rear-end-crashes-use-pre-crash-system-design-2011-01-0576
- データ: NASS/CDS 2000-2009の先行車停止型追突で、EDRの事故前速度とブレーキ記録が揃った59件。
- 結果: 12件（約20%）は衝突前に制動していなかった。平均制動減速度は0.52G、制動開始時のTTCの平均は1.1〜1.4 s。
- 示唆: 実事故の追突では制動開始が遅く（TTC 1.1〜1.4 s）、無制動も多い。【推察】警報はTTCが概ね2〜3 sより長い段階で出す必要があり、予測ホライズン1 s程度のモデルでは足りない。

#### [17] Federal Motor Vehicle Safety Standards; Event Data Recorders（49 CFR Part 563 最終規則）
- 組織: NHTSA（米国運輸省）
- 年 / 種別: 2024年12月18日 / 連邦規則（Federal Register 89(243)）
- URL: https://www.govinfo.gov/content/pkg/FR-2024-12-18/html/2024-29862.htm
- 要点: 事故前の時系列データの記録を、5 s・2 Hzから20 s・10 Hzに延長する。対象は車速、アクセル開度、ブレーキON/OFF（必須）と、エンジン回転数、ABS、横滑り防止、操舵入力（記録する場合）。適用は2027年9月1日から。根拠となった2018年のEDR Duration Studyでは、5 sでは回避操作（特に操舵）の開始を多く取り逃がしており、20 sで分析対象の事故前操作の90パーセンタイルをカバーできた。
- 示唆: 事故前の挙動変化を捉えるには、少なくとも20 s程度の窓と10 Hz程度の分解能が要る、という規制当局の判断である。これはCANログの設計（リングバッファ長とサンプリング周波数）の根拠になる。

### 3.6 代理安全指標の評価・レビュー

#### [4] Performance evaluation of surrogate measures of safety with naturalistic driving data
- 著者: J. Lu, X. He, H. van Lint, H. Tu, R. Happee, M. Wang
- 年 / 種別: 2021 / 査読論文（Accident Analysis & Prevention 162, 106403）
- URL: https://research.tudelft.nl/en/publications/performance-evaluation-of-surrogate-measures-of-safety-with-natur
- 手法: 縦方向の6指標（TTC、S-PDRF、DRAC、PICUD、PFS、CFS）を同一のリスク検出基準で較正し、精度・即時性・頑健性・効率の4軸で評価した。
- 結果: すべての軸で優れる単一指標はなかった。
- 示唆: 【推察】単一のSSM閾値で警報するより、複数指標を特徴量として学習モデルに入力する方が合理的である。

#### [18] A systematic review of traffic conflict-based safety measures with a focus on application context
- 著者: A. Arun, M.M. Haque, S. Washington, T. Sayed, F. Mannering
- 年 / 種別: 2021 / 査読論文（Analytic Methods in Accident Research 32, 100185）
- URL: https://eprints.qut.edu.au/212594
- 要点: 交差点コンフリクト指標に関する386研究をレビューした。TTCとPETが最も多く使われていた。閾値は交通環境の種類、データ源、適用目的によって異なり、回帰モデルで整理している。
- 示唆: 閾値は文脈に依存するので、文献値をそのまま流用せず、自車データで較正する必要がある。

#### [22] Beyond 1D and oversimplified kinematics: A generic analytical framework for surrogate safety measures
- 著者: S. Li, M. Anis, D. Lord, H. Zhang, Y. Zhou, X. Ye
- 年 / 種別: 2023 / プレプリント（arXiv 2312.07019）
- URL: https://arxiv.org/abs/2312.07019
- 要点: 任意の車両運動モデルと空間的な重なりに基づく衝突判定で、SSMを一般化した。1D SSMは3D SSMに比べ、非臨界TTCで約300%、臨界TTC（1.5 s未満）で約20%ずれうる。

#### [23] A microsimulation approach for the impact assessment of a V2I based Road Hazard Warning system
- 著者: K.N. Porfyri, A. Kotsi, E. Mitsakis（CERTH）
- 年 / 種別: 2020 / プレプリント（arXiv 2010.10262）
- URL: https://arxiv.org/abs/2010.10262
- 要点（SSM閾値の出典として利用）: 臨界TTCは文献で1.5〜4 s。FHWAのSSAMが提案した1.5 sを採用し、DRACはArcher（2005）の3.35 m/s²を潜在的コンフリクトの閾値として用いた。

#### [25] Hurry Driving State Detection Algorithm Based on Urban Driving Database
- 著者: P. Raksincharoensak, T. Iijima, Y. Michitsuji, K. Maeda, M. Nagai
- 年 / 種別: 2010 / 査読論文（自動車技術会論文集 41(3), 751-758）
- URL: https://www.jstage.jst.go.jp/article/jsaeronbun/41/3/41_3_751/_article/-char/en
- 要点: 常時記録型ドライブレコーダの都市部自然運転データを用い、ペダル操作時の加速度と追従時のTHWを速度域・道路環境・ドライバ別に比較して、「急ぎ運転」状態の検出を検討した。
- 示唆: ヒヤリハットが起きる前段階の「先急ぎ」状態を、CAN相当の信号（ペダル、加速度、車間）で捉える試みである。

#### [34] Surrogate Safety Measures from Traffic Simulation Models（FHWA-RD-03-050）
- 組織: FHWA
- 年 / 種別: 2003 / 政府報告書
- URL: https://www.fhwa.dot.gov/publications/research/safety/03050/02.cfm
- 要点: TTC、PET、減速度（DR）、ギャップ時間、侵入時間、PSD、TET/TITを定義している。TTCを主要な重大度指標とする立場がある一方、速度を含まないので衝突の激しさは示せないという指摘も併記している。

### 3.7 ラベル不足・クラス不均衡

#### [35] SynSHRP2: A Synthetic Multimodal Benchmark for Driving Safety-critical Events Derived from Real-world Driving Data
- 著者: L. Shi, B. Jiang, Z. Yuan, M.A. Perez, F. Guo（VTTI）
- 年 / 種別: 2025 / プレプリント（arXiv 2505.06276。CVPR 2025ポスター）
- URL: https://arxiv.org/abs/2505.06276
- データ: SHRP2由来のcrash 1,874件超、near-crash 6,924件。事象前5 sから事象中までの運動学時系列、注釈、合成キーフレーム（Stable Diffusion + ControlNet）。
- 示唆: SHRP2の運動学時系列にアクセスしやすくする試みである。事象前5 sの運動学データは、CANのみのモデルの事前学習や評価に転用できる可能性がある【推察】。

（補足）SMOTEやGANによるオーバーサンプリングを、事故・ニアミス予測に使った研究は多数ある。ただし本調査では、自然運転ニアミスの運動学時系列で偽警報率まで報告した一次資料を確認できなかった。これはギャップとして第5章に記す。

---

## 4. ニアミス検出・事故予測のパイプライン案（文献に基づく）

ここでは文献の知見と【推察】を分けて示す。

### 4.1 全体構成

```
[CAN取得 10Hz以上] → [前処理・派生信号] → [L1: ルールトリガ] → [L2: 事象判定(学習)] → [L3: 予兆予測(リアルタイム)] → [警報ポリシ]
                                                     ↓                                                 ↑
                                               [事象DB/ラベル] ———→ [L4: ドライバ単位リスク評価] ——————┘
```

### 4.2 各層の設計

| 層 | 内容 | 文献の根拠 | 【推察】設計上の注意 |
|---|---|---|---|
| 取得 | 10 Hz以上で記録し、リングバッファに事象前20 s・後5〜10 sを保持する | SHRP2トリガは10 Hz前提 [1]。NHTSAは20 s・10 Hzへ延長 [17]。農工大DBは-10 s〜+5 s [19] | 車種ごとにCAN IDとスケールの対応表を作る。ブレーキ圧・操舵速度は可能な限り20 Hz以上で取る |
| 前処理・派生信号 | ジャーク（前後・横）、ヨー角加速度、ペダル踏み替え時間、TTC・THW・DRAC・MTTC（レーダ値がある場合）、トリップ経過時間 | ジャーク [1][10][24]、SSM [4][23]、トリップ長 [3] | 微分前にローパスフィルタをかける。レーダの対象ロスト（距離の急変）を除去する |
| L1 ルールトリガ（高感度スクリーニング） | 前後減速度（≤-0.45G、高速道路では≤-0.3G）、|a_y|≥0.5〜0.75G、ヨーレート反転、ジャーク≤-1.0 g/s、ABS/ESC/TCS作動、ADAS警報（FCW/PCS）、TTC<1.5 s、DRAC>3.35 m/s² | [1][3][13][23] | トリガ同士は2 s窓で統合する [1]。最低車速条件（5 m/sなど）を付ける [1]。網羅性を優先するので誤検出は多い（有効率は2〜22%程度 [1][2]） |
| L2 事象判定（ニアミスか否か、重大度） | 事象前後15〜25 sの多変量時系列を分類する。波形の機能的分類 [2]、ジャークとピーク減速度による判別 [10][24]、LSTM/CNN-LSTM [29][30] | 機能的分類で無効トリガを42%削減 [2]。LSTMで精度96% [29] | 正解ラベルは開発フェーズに限り、映像付きの少数車両で作るのが現実的。運用時はCANのみで推論する。「ドライバの反応」[28] を、ペダル遷移時間や操舵速度で代替する |
| L3 予兆予測（リアルタイム） | 直近3〜10 sの窓から、Δt秒後のニアミス確率を出す。予測ホライズンを1〜5 sで掃引して評価する | 観測窓3〜4 s・予測1 sで精度約90%以上 [6][7]。GSSMは先行時間の中央値2.6 s [8] | 実事故の制動開始はTTC 1.1〜1.4 s [16] なので、有用な警報には2 s以上のリードタイムが必要である。ラベルなしの手法（GSSM [8]、順序学習 [31]、DIF [32]）を併用する |
| 警報ポリシ | 確率の閾値を、偽警報の予算（例: 1時間あたりの許容回数）で決める。ドライバ個人に適応させた閾値 | 個別適合型閾値 [26]、適応的・文脈依存の閾値 [15] | 評価指標はPR-AUC、警報適合率、走行距離・時間あたりの偽警報数、リードタイム分布とし、Accuracyは使わない |
| L4 ドライバ単位リスク | 走行距離あたりのインシデント率・高G事象率から、高リスクドライバを判別しコーチングする | AUC 0.938 [12]、OR 1.07/月 [14]、個人傾向の持続 [13] | リアルタイム警報の誤報を許容しにくい場合は、L4を先に実用化する方が費用対効果が高い |

### 4.3 CANのみで成立する範囲 【推察】

- 成立しやすい: 追突型（前方レーダあり）のニアミス。単独の挙動異常（急操舵、スリップ、ESC介入）。ドライバ単位のリスク傾向。
- 成立しにくい: 出会い頭、右左折時の歩行者・自転車とのニアミス（PETは計算不可）。農工大DBでは出会い頭が主要な類型であり [19]、CANだけでは事後検出（急制動）はできても、事前の予兆予測は難しい。
- 補完策: ウインカー、操舵角、車速から右左折・交差点進入の局面を推定し、局面別のモデルや閾値を使う（Morimuraらは右折局面のニアミス形態を運動学だけで分類している [20]）。

---

## 5. 課題・ギャップ

1. トリガの低適合率: CANで取れる運動学トリガは、最良でも有効率が約22%（SHRP2）[1]。100-Carでは無効:有効が2:1〜51:1 [2]。映像による確認なしで運用すると誤警報が多い。
2. ラベル不足と評価の偏り: 高精度の報告 [6][7][29][30] の多くは事象とベースラインを均衡させた評価で、実際のベース率での適合率や偽警報率がほぼ報告されていない。【推察】実運用の性能は過大評価されている可能性が高い。
3. 予測ホライズンの短さ: 運動学だけの予測は約1 s先が中心である [6][7]。ラベルなしのGSSMでも中央値2.6 s [8]。人の反応と制動に要する時間を考えると、警報の有効性はまだ限られる。
4. 閾値の非標準化: 減速度閾値は-0.3〜-0.75Gまで散らばり [1][3][21]、TTCの臨界値も1.5〜4 s [23]。日本の公開DBで閾値別の感度・適合率を評価した一次資料は、本調査では見つからなかった。
5. 文脈情報の欠如: CANだけでは道路形状、交差点、交通弱者の存在が分からない。ニアミスと事故の関係そのものにも議論がある [11][27]。
6. 車種間の移植性: CAN信号の定義・分解能・周期は車種ごとに異なる。【推察】モデルの汎化には、信号の正規化とドメイン適応が必要になる。

---

## 6. 次のアクション提案

1. SHRP2型の多重トリガのベースラインを実装する: 自社CANログにSHRP2の表2.1相当のトリガ [1] と農工大型の0.45Gトリガ [19] を実装し、1時間・100 kmあたりのトリガ件数を、閾値別（-0.3/-0.45/-0.65/-0.75G）、道路種別、車速域別に集計する。目的は誤検出負荷の見積もりである。
2. 弱ラベルと少量の正解ラベルによるデータセットを構築する: ADAS警報フラグ（FCW/PCS作動）、ABS/ESC介入、TTC<1.5 sを弱ラベルとする。開発フェーズに限り、映像付きの少数車両で数百件の正解ラベル（crash/near-crash/CRC/非事象、SHRP2定義 [1] 準拠）を付けて較正に使う。運用時の入力はCANのみとする。
3. 予測ホライズンを掃引する評価プロトコルを定める: 観測窓3/5/10 s、予測ホライズン1/2/3/5 sのグリッドで、PR-AUC、警報適合率、偽警報数（/時間）、リードタイム分布を報告する。ベースラインには単純閾値（TTC、DRAC、減速度）を置き、AdaBoost [6][7]、LSTM [29]、異常検知（DIF/Autoencoder）[32] を比較する。
4. ラベルなし・順序学習の手法を検証する: GSSM [8] と比較ベース順序学習 [31] を、前方レーダ1対象・CAN信号のみの縮退入力で再現し、教師ありモデルとリードタイムを比べる。
5. ドライバ単位のリスクスコアを先行して実用化する: インシデント率・高G事象率からドライバリスクを層別し [12][14]、追跡データで将来のインシデント増加との関係を検証する。リアルタイム警報より誤報コストが低く、早期に価値を出しやすい【推察】。

---

## 7. 参考文献

査読論文・プレプリントは★、その他（報告書・規則・講演・資料）は☆。

1. ☆ Hankey, J.M., Perez, M.A., McClafferty, J.A. (2016). Description of the SHRP 2 Naturalistic Database and the Crash, Near-Crash, and Baseline Data Sets. VTTI. https://vtechworks.lib.vt.edu/handle/10919/70850
2. ☆ Sudweeks, J. (2015). Using Functional Classification to Enhance Naturalistic Driving Data Crash/Near Crash Algorithms. NSTSCE Report 15-UT-030. https://vtechworks.lib.vt.edu/bitstreams/5ac3b5e4-7c35-4dd8-9d40-c3534bc4ad40/download
3. ★ Kong, X., Das, S., Zhou, H., Zhang, Y. (2021). Patterns of near-crash events in a naturalistic driving dataset: Applying rules mining. Accident Analysis & Prevention 161, 106346. https://subasish.github.io/ait_lab/pdfs/2021%20(A)%20Kong%20AAAP%20Near-crash%20using%20Rules%20Mining.pdf
4. ★ Lu, J., He, X., van Lint, H., Tu, H., Happee, R., Wang, M. (2021). Performance evaluation of surrogate measures of safety with naturalistic driving data. Accident Analysis & Prevention 162, 106403. https://research.tudelft.nl/en/publications/performance-evaluation-of-surrogate-measures-of-safety-with-natur
5. ★ UDRIVE consortium. Evaluation of safety critical event triggers in the UDRIVE data. https://swov.nl/en/publicatie/evaluation-safety-critical-event-triggers-udrive-data
6. ☆ Osman, O.A., Hajij, M., Karbalaieali, S., Ishak, S. (2018). Crash and Near-Crash Prediction from Vehicle Kinematics Data: A SHRP2 Naturalistic Driving Study. TRB 97th Annual Meeting. https://trid.trb.org/View/1496022
7. ★ Osman, O.A., Hajij, M., Bakhit, P.R., Ishak, S. (2019). Prediction of Near-Crashes from Observed Vehicle Kinematics using Machine Learning. Transportation Research Record. https://www.bohrium.com/paper-details/prediction-of-near-crashes-from-observed-vehicle-kinematics-using-machine-learning/812751158522150912-4628
8. ★ Jiao, Y., Calvert, S.C., van Cranenburgh, S., van Lint, H. (2025). Learning collision risk proactively from naturalistic driving data at scale. arXiv:2505.13556. https://arxiv.org/abs/2505.13556
9. ★ Perez, M.A., Sudweeks, J.D., Sears, E., Antin, J., Lee, S., Hankey, J.M., Dingus, T.A. (2017). Performance of basic kinematic thresholds in the identification of crash and near-crash events within naturalistic driving data. Accident Analysis & Prevention 103, 10-19.（抄録紹介）https://insurancenewsnet.com/oarticle/findings-on-risk-management-reported-by-investigators-at-virginia-tech-performance-of-basic-kinematic-thresholds-in-the-identification-of-crash-and
10. ★ Bagdadi, O., Várhelyi, A. (2013). Development of a method for detecting jerks in safety critical events. Accident Analysis & Prevention 50, 83-91. https://lup.lub.lu.se/record/3347798
11. ★ Guo, F., Klauer, S., Hankey, J., Dingus, T. (2010). Near Crashes as Crash Surrogate for Naturalistic Driving Studies. Transportation Research Record 2147, 66-74. https://trid.trb.org/view/1353218
12. ★ Guo, F., Fang, Y. (2013). Individual driver risk assessment using naturalistic driving data. Accident Analysis & Prevention 61, 3-9. https://pubmed.ncbi.nlm.nih.gov/22785091/
13. ★ Simons-Morton, B.G., Cheon, K., Guo, F., Albert, P. (2013). Trajectories of Kinematic Risky Driving Among Novice Teenagers. Accident Analysis & Prevention 51, 27-32. https://pmc.ncbi.nlm.nih.gov/articles/PMC3556237
14. ★ Simons-Morton, B.G., Zhang, Z., Jackson, J.C., Albert, P.S. (2012). Do elevated gravitational-force events while driving predict crashes and near crashes? American Journal of Epidemiology 175(10), 1075-1079. https://experts.llu.edu/en/publications/do-elevated-gravitational-force-events-while-driving-predict-cras/
15. ★ Kalantari, A.H., Papadimitriou, E., Zgonnikov, A., Afghari, A.P. (2025). How Much Is Too Much? Adaptive, Context-Aware Risk Detection in Naturalistic Driving. arXiv:2508.00888. https://arxiv.org/abs/2508.00888
16. ★ Kusano, K.D., Gabler, H.C. (2011). Method for Estimating Time to Collision at Braking in Real-World, Lead Vehicle Stopped Rear-End Crashes for Use in Pre-Crash System Design. SAE Int. J. Passeng. Cars - Mech. Syst. 4(1). https://saemobilus.sae.org/articles/method-estimating-time-collision-braking-real-world-lead-vehicle-stopped-rear-end-crashes-use-pre-crash-system-design-2011-01-0576
17. ☆ NHTSA (2024). Event Data Recorders, Final Rule (49 CFR Part 563). Federal Register 89(243), 2024-12-18. https://www.govinfo.gov/content/pkg/FR-2024-12-18/html/2024-29862.htm
18. ★ Arun, A., Haque, M.M., Washington, S., Sayed, T., Mannering, F. (2021). A systematic review of traffic conflict-based safety measures with a focus on application context. Analytic Methods in Accident Research 32, 100185. https://eprints.qut.edu.au/212594
19. ☆ 鈴木大雅、丸茂喜高、風間恵介、毛利宏 (2024). 出会い頭ニアミスにおける非優先道路側の対象車の状態による影響. 日本大学生産工学部 第57回学術講演会. https://www.cit.nihon-u.ac.jp/laboratorydata/kenkyu/kouennkai/reference/No.57/pdf/2-34.pdf
20. ☆ 森村哲郎、谷澤祐介、山崎慎也、井手剛 (2011). 統計的機械学習を用いたプローブカーデータからのヒヤリハット発生形態の推定. 自動車技術会 秋季学術講演会. https://ide-research.net/papers/2011_JSAE_Morimura.pdf
21. ☆ 山田浩、市川英敏、片野裕介 (2010). プローブデータの交通安全対策への活用について. 国土交通省 技術研究発表会. https://www.mlit.go.jp/chosahokoku/h22giken/program/kadai/pdf/ippan/ippan1-06.pdf
22. ★ Li, S., Anis, M., Lord, D., Zhang, H., Zhou, Y., Ye, X. (2023). Beyond 1D and oversimplified kinematics: A generic analytical framework for surrogate safety measures. arXiv:2312.07019. https://arxiv.org/abs/2312.07019
23. ★ Porfyri, K.N., Kotsi, A., Mitsakis, E. (2020). A microsimulation approach for the impact assessment of a Vehicle-to-Infrastructure based Road Hazard Warning system. arXiv:2010.10262. https://arxiv.org/abs/2010.10262
24. ★ 山崎慎也、船久保明、谷澤祐介 (2011). Estimation of Dangerous Routes using the Near-miss Incident Data of Probe-car. 自動車技術会論文集 42(2), 639-644. https://www.jstage.jst.go.jp/article/jsaeronbun/42/2/42_2_639/_article/-char/en
25. ★ Raksincharoensak, P., Iijima, T., Michitsuji, Y., Maeda, K., Nagai, M. (2010). Hurry Driving State Detection Algorithm Based on Urban Driving Database. 自動車技術会論文集 41(3), 751-758. https://www.jstage.jst.go.jp/article/jsaeronbun/41/3/41_3_751/_article/-char/en
26. ☆ 東京農工大学 (2008). 学長記者会見資料「運転教習ドライブレコーダを活用した教習所運転教育に向けた取り組み」「個別適合型の先急ぎ運転警報つきドライブレコーダの開発」. https://www.tuat.ac.jp/documents/tuat/outline/disclosure/pressrelease/2008/20090223162216812265831.pdf
27. ★ Dozza, M. (2020). What is the relation between crashes from crash databases and near crashes from naturalistic data? Journal of Transportation Safety & Security 12(1), 37-51. https://research.chalmers.se/publication/511868
28. ★ Dozza, M., Pañeda González, N. (2013). Recognizing safety-critical events from naturalistic driving data. Accident Analysis & Prevention 60, 298-304. https://research.chalmers.se/en/publication/173520
29. ★ Naji, H.A.H., Xue, Q., Lyu, N., Duan, X., Li, T. (2022). Risk Levels Classification of Near-Crashes in Naturalistic Driving Data. Sustainability 14(10), 6032. https://ideas.repec.org/a/gam/jsusta/v14y2022i10p6032-d816665.html
30. ★ Zhao et al. (2024). A CNN-LSTM-Attention Model for Near-Crash Event Identification on Mountainous Roads. Applied Sciences 14(11), 4934. https://doaj.org/article/8a0de17d5f6c4982863efadd908e15de
31. ★ Li, Z. et al. (2026). Comparison-Based Ordinal Learning for Proactive Driving Risk Assessment. arXiv:2607.11128. https://arxiv.org/abs/2607.11128
32. ★ Le, D., Manhardt, T., Venator, M., Betz, J. (2025). Unsupervised Learning for Detection of Rare Driving Scenarios. arXiv:2512.23585. https://arxiv.org/abs/2512.23585
33. ★ Fugiglando, U. et al. (2017). Driving Behavior Analysis through CAN Bus Data in an Uncontrolled Environment. arXiv:1710.04133. https://arxiv.org/abs/1710.04133
34. ☆ FHWA (2003). Surrogate Safety Measures from Traffic Simulation Models (FHWA-RD-03-050). https://www.fhwa.dot.gov/publications/research/safety/03050/02.cfm
35. ★ Shi, L., Jiang, B., Yuan, Z., Perez, M.A., Guo, F. (2025). SynSHRP2: A Synthetic Multimodal Benchmark for Driving Safety-critical Events Derived from Real-world Driving Data. arXiv:2505.06276. https://arxiv.org/abs/2505.06276

ソース件数: 35件（★査読論文・プレプリント 26件、☆報告書・規則・講演・資料 9件）。

確認レベルの注記:
- 本文PDFで数値を確認したもの: [1][2][3][19][20]（書誌と抄録）、[21][23][26]
- 抄録・書誌ページで確認したもの: [4][6][8][10][11][12][13][15][16][17][22][24][25][27][28][29][31][32][33][34][35]
- 検索結果（抄録要約・紹介記事）でのみ確認したもの: [5][7][9][14][18][30]。数値の利用前に原典を確認することを推奨する。
