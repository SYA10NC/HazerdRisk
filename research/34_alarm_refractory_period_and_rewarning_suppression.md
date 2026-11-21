# 34. 警報の再発報抑制（不応期・遅延・ラッチ）と警報率の関係

- 調査日: 2026-11-21
- 論点: B-30。連続する高リスク窓での警報の重複抑制・不応期・ラッチ・持続条件が、警報件数・見逃し・検出遅延に与える影響を扱う既存研究の整理
- 既存調査との関係: 29（校正・閾値変換の全ソース）、10 §2、33 §2.1・§2.2（医療アラーム疲労の内訳比率、EEMUA 191 系の概要）は扱い済みとして除外した。Rolnick & Weissman 2019（mdedge）と早稲田・島田資料は既出（29・33）のため再掲扱い
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）29件／既出の再掲 2件。WebFetch は pmc.ncbi.nlm.nih.gov・bmjopenquality.bmj.com・controlglobal.com・hexagon.com・automation.com 等で名前解決に失敗した（ISSUES I-01 継続）ため、全件が検索結果の抜粋のみである。数値は検索要約に現れたものだけで、原文との照合はしていない

## 1. エグゼクティブサマリー

- 再発報の抑制は「遅延（持続条件）」「デッドバンド」「不応期（同一患者・同一事象への再発報禁止時間）」「ラッチ」「階層ルール」に分けられ、医療・プラント分野に資料が多い。ADAS（FCW/LDW）の再警報間隔・ヒステリシスを秒数で示した公開文献は見つからなかった。
- 遅延は件数を大きく減らすと報告されている。ICU の SpO2 で 14秒遅延により無効・無視アラームが51%減、19秒で67%減（孫引き・遡及試算）。NICU の RCT では90秒遅延＋広い限界値で警報の中央値が5.2→1.6件/時、低酸素時間（0.1%未満）に差はなかった（抜粋）。
- ただし見逃しを実測した例はほとんどない。削減率は遡及計算が多く、真のイベントの欠落は測られていない。
- 不応期を一律にせず、重症度が上がった時だけ再発報を許す階層ルールの先例がある（Christiana Care の CEWS アラート。critical では抑制しない）。
- プラントでは chattering を「1分に3回以上」などの頻度で定義し、デッドバンド→遅延の順で適用する実務指針がある。遅延・限界値の最適設計は未解決との記述もある（Tulsyan 系）。
- FCW の反復曝露では2回目以降の効果が初回と異なる（持ち越し効果）。再警報は無効とは限らない。
- 直接の数値（運転の時間尺度での不応期長と警報率の関係）は未発見。【推察】自前データで不応期長ごとに件数・見逃し・遅延の曲線を出す設計が必要。

## 2. 主要知見

凡例: 確認方法は全件「抜粋のみ」。【推察】は事実と区別した推論。

### 2.1 医療（早期警告スコア・患者モニタ）

1. Data-driven approach to Early Warning Score-based alert management — Capan ら（Christiana Care）、2018、査読論文（BMJ Open Quality 7(3):e000088）。URL: https://bmjopenquality.bmj.com/content/7/3/e000088.abstract（補助 https://pmc.ncbi.nlm.nih.gov/articles/PMC6109824）。
   - 事実: conservative / intermediate / liberal の3種のアラートアルゴリズムを比較。各々が発報規則と抑制（muting）規則の集合。liberal は低リスク域に留まる間は最初の1回以降は発報しない。3種とも critical では抑制しない。件数・頻度はユニットの重症度に依存し、ユニット別調整が必要と結論。件数の具体値・抑制時間・見逃し数は抜粋から取れなかった。
   - 示唆: 【推察】高リスク閾値を超えている間は再発報を抑え、段階が上がる時だけ再発報を許す設計が対応する。L4〜L6。
2. 敗血症アラートの抑制期間 — 3件、抜粋のみ。
   - Northern Light Health の Cerner SIRS/Sepsis ナース向けガイド（院内運用資料、年不明）: 新しい Sepsis アラートは同一患者に48時間は再発報しない。URL: https://hi.northernlighthealth.org/Flyers/Non-Providers/Hospital-Nurse/IC/Cerner-IP-RN-SIRS_-Sepsis.aspx
   - 敗血症の臨床意思決定支援のレビュー（抜粋の出典記事は未特定）: 各陽性アラートの後に所定時間だけ抑制する病院がある。引用研究では全患者の17%がアラートを受け、うち40%が複数回受けた。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7684552
   - Epic Sepsis Model の24病院記述研究（出典未確定）: 閾値6、患者あたり最大1アラートで集計。ミシガン大は看護師の過剰警報の訴えを受け2020年4月に ESM アラートを停止。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8605481
   - 示唆: 【推察】「患者あたり1回」「48時間」は事実上のラッチ。見逃しへの影響は未評価。
3. Improving Alarm Performance in the Medical ICU Using Delays and Clinical Context — Görges, Markewitz, Westenskow、2009、査読論文（Anesth Analg 108(5)）。URL: https://psnet.ahrq.gov/issue/improving-alarm-performance-medical-intensive-care-unit-using-delays-and-clinical-context
   - 事実: 臨床家はアラームの41%を無視（抜粋）。遅延と文脈検出が提案された。孫引き（Philips 資料 https://www.philips.com/c-dam/b2bhc/onesite-master/articles/hpm-clinical-series-alarm-fatigue-and-ways-to-address-it.pdf の抜粋経由、一次未確認）: 14秒遅延で無効・無視アラーム51%減、19秒で67%減、19秒遅延＋日常ケースの自動検出で934件→274件と試算。遡及計算で、見逃しは測られていない。
   - 示唆: 【推察】短時間で消える警報（chatter）を落とす効果が大きい。窓単位の高リスク判定の持続条件（何窓連続で超えたら発報）に相当。
4. Retrospective analysis of pulse oximeter alarm settings in an ICU patient population — MIMIC-II、査読論文（著者・年は抜粋から不明）。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4891882
   - 事実: SpO2 閾値84/86/88/90%と遅延10〜60秒の組合せで警報率をシミュレート。低い閾値と長い遅延が警報率を下げ、少数の患者が大半の警報を出した。孫引き: 閾値90→88%で総アラーム45%減、15秒遅延を足すと70%減（術後患者）。遅延による真のイベント見逃し数は抜粋から確認できず。
   - 示唆: 【推察】警報が少数のドライバー（走行）に集中する偏りはドライバー単位で別途見る必要がある。
5. Evaluation of two SpO2 alarm strategies during automated FiO2 control in the NICU（ランダム化クロスオーバー試験、著者・年は抜粋から不明）。URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6501373/
   - 事実: 90秒遅延＋広い限界値の戦略で警報の中央値が5.2→1.6件/時。低酸素時間（0.1%未満）に差なし。
   - 示唆: 件数を約70%減らしてもアウトカム代理指標が悪化しなかった数少ない無作為化の例。新生児 SpO2 で時間尺度は運転と異なる。【推察】
6. Reducing Alarm Burden in a Level IV NICU（Fang ら、2021頃、QI 報告。論説経由の抜粋）。URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10990340/ ／補助: https://www.childrenshospitals.org/news/childrens-hospitals-today/2019/04/patient-safety-project-aims-to-reduce-alarm-fatigue-in-the-nicu
   - 事実: 目標は黄色の自己解消型 SpO2 アラームを14→7件/患者時に半減。論説では64%減らしても10分に1回は発生。別抜粋に、30秒遅延を二次通知に入れると非実行可能アラームが82%減る見込みとの試算（観察からの予測）。
   - 示唆: 【推察】一次（モニタ）と二次（ページング）で遅延を分ける二段構成は、車内警告と車外記録・通知の層分けに近い。
7. Testing physiologic monitor alarm customization software — Yale 他、2018、PLoS ONE（ベンダー資金あり、単一施設前後比較）。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6193710
   - 事実: 56床の内科 ICU で、中優先度の心拍・呼吸・動脈圧アラームが 9.3%・11.8%・15.9%減。SpO2 は減らず。「緊急アラームを見逃した」と答えた看護師は43.9%→25.0%。
   - 示唆: 閾値カスタマイズだけでは1〜2割。【推察】時間構造の操作との併用で大きく効く。
8. Computational approaches to alleviate alarm fatigue in intensive care medicine: A systematic literature review — Chromik ら、2022、Frontiers in Digital Health。URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9424650/
   - 事実: 69編採択。アラームの72〜99%は技術的に偽または臨床的に無関係。件数削減だけでは疲労は解決しない可能性。抑制・遅延の削減率の統合値は抜粋になし。
9. Classification of Methods to Reduce Clinical Alarm Signals for Remote Patient Monitoring: A Critical Review（arXiv 2302.03885、著者・年は抜粋から不明）。URL: https://arxiv.org/pdf/2302.03885
   - 事実: 15秒遅延で偽陽性アラームが約60%減るとの記述（元の引用先は未確認）。
10. 日本語: 大阪大学病院 医療安全セミナー資料（新井、2022）。URL: https://www.hosp.med.osaka-u.ac.jp/home/hp-cqm/ingai/seminar/pdf/2022/005_arai.pdf
   - 事実: 検索要約では、過去2時間の不要アラーム数がアラーム反応時間の延長と比例するとの整理が国内病院の資料として紹介されていた（どの資料に載るかは未確認）。循環器病棟で22秒に1回発動し57%がテクニカルアラームとの事例。具体的な設定値・削減率は抜粋になし。
   - 示唆: 【推察】直近の警報数が多いほど応答が遅れるなら、不応期は見逃しと応答遅れの両方に作用する。
- 既出の再掲: Rolnick & Weissman 2019（29 に既出。PPV 低下と疲労・リード時間のトレードオフ）、早稲田・島田（33 に既出）。

### 2.2 産業プラント（ISA-18.2・EEMUA 191 系の chattering 対策）

11. How to reduce alarm chatter — Control Global 誌、2016、業界誌。URL: https://www.controlglobal.com/articles/2016/how-to-reduce-alarm-chatter
   - 事実: 振動するプロセスが11件のアラームを出すところ on-delay で1件になるデモ。off-delay も件数は減るが偽条件で standing alarm になりうる。on-delay はノイズ状態で限界値付近の本物の警報をマスクしうる。割合指定のデッドバンドは大きすぎると張り付く恐れ。
   - 示唆: 【推察】不応期を長くするほど重複は減るが、窓内の本物の再悪化を隠す見逃しリスクがある。
12. Shut up! Fixing chattering and fleeting alarms — Hexagon（ALI 資料、年不明、ベンダー）。URL: https://aliresources.hexagon.com/mining/shut-up-fixing-chattering-and-fleeting-alarms
   - 事実: chattering の目安は「1分間に3回以上」。アナログ信号はまずデッドバンド、その後に遅延タイマー。ON-delay が30秒〜1分を超える場合は慎重に扱うべき。
   - 示唆: 【推察】「N回/分」の頻度定義は CAN 警報の再発報判定（窓内 N 回以上）に移植できる。
13. Solve common problems in industrial automation alarm systems — automation.com（年不明）。URL: https://www.automation.com/article/solve-common-problems-industrial-automation-alarm-systems
   - 事実: デッドバンド1%または off-delay 5秒で chattering が大幅に減る（経験則、実測ではない）。off-delay 60秒で chattering の塊が1件になるとも。
14. Taming the wild alarm system — part three — Octave（ベンダーブログ、年不明）。URL: https://www.octave.com/learn/resources/blogs/taming-wild-alarm-system-part-three
   - 事実: 遅延時間は再発報アラームの通常の間隔より長く選ぶのが鍵。
   - 示唆: 【推察】不応期は再発報間隔の分布（CAN の連続窓長）から決めるのが妥当。
15. Online reduction of chattering alarms due to random noise and oscillation — Wang, Chen、2014、IFAC World Congress。URL: https://skoge.folk.ntnu.no/prost/proceedings/ifac2014/media/files/0114.pdf
   - 事実: 遅延タイマーで chattering 件数を減らすオンライン手法。振動由来の検出に振動指標 η ≥ 0.005。m サンプル窓の2規則でノイズ由来と振動由来を分けて除去。削減率の数値は抜粋になし。
16. Analysis and design of time-deadbands for univariate alarm systems（Bohrium 掲載ページ、著者・年は抜粋から不明）。URL: https://www.bohrium.com/paper-details/analysis-and-design-of-time-deadbands-for-univariate-alarm-systems/813084497376444418-2564
   - 事実: time-deadband について、誤警報率（FAR）・見逃し率（MAR）・期待検出遅延（EDD）の解析式と設計手順を導出。
   - 示唆: 【推察】不応期は FAR 低下と MAR・遅延増加のトレードオフとして定式化できる。
17. Afzal & Chen の学位論文（generalized delay timers、Univ. of Alberta）。URL: https://era.library.ualberta.ca/items/cf7ce9ee-6e2b-404d-892c-0ae2b31ca361/download/08f7b9bc-7fb6-43a1-8370-d6f761d0cce2
   - 事実: generalized delay timer についてマルコフ過程で FAR・MAR・EDD を計算し従来型と比較（この URL が当該論文である確証は取れていない）。
18. Tulsyan ら（UBC）の delay-timer / deadband 設計論文プレプリント、2017〜2019頃。URL: https://dais.chbe.ubc.ca/assets/preprints/2019J7_Tulsyan_IECR.pdf
   - 事実: 非ガウス・非線形プロセスで FAR と MAR を最小化するデッドバンド警報の設計アルゴリズムを提案。delay-timer 構成では限界値と遅延時間が2大パラメータで、最適調整は未解決問題と記述。
19. アラーム合理化 — ABB System 800xA（日本語、ベンダー記事、年不明）。URL: https://new.abb.com/control-systems/ja/system-800xa/800xa-dcs/operator-interfaces/alarm-management/articles/alarm-rationalization
   - 事実: 経験則として運転員1人あたり1時間6件、フラッド時は通常の5〜10倍（検索要約、原文未照合）。
20. Siemens 白書（2021）と ISA 記事（2021-08）。URL: https://assets.new.siemens.com/siemens/assets/api/uuid:234f1026-298f-49dc-8961-0c5223c38588/white-paper-alarm-management-2021-final.pdf ／ https://www.isa.org/intech-home/2021/august-2021/features/from-alarm-floods-to-highly-protected-status
   - 事実: ISA-18.2 は chattering を短時間にアラーム状態と正常状態を往復するものと定義し、fleeting 型と repeating 型に分類。「chattering が件数の約10〜60%」という数値は特許文献由来の引用として検索要約が述べたもので、出典特定不能のため根拠にしない。

### 2.3 ADAS・運転支援

21. Repeated Measures Testing of Driver Collision Warning — SAE 2015-01-1413、2015。URL: https://saemobilus.sae.org/papers/repeated-measures-testing-driver-collision-warning-2015-01-1413
   - 事実: FCW の連続する脅威イベント間で持ち越し効果。反復曝露を避けるか持ち越しを明示的に扱うよう推奨。
22. Effects of forward collision warning and repeated event exposure on emergency braking（著者・年は抜粋から不明、図書館カタログ経由）。URL: https://opact.sdu.edu.tr/vufind/SummonRecord/FETCH-LOGICAL-c467t-c5fce0163a09fd5f5e606fed2cae1f54ffc76d6b820dd5d39adea1e60d3d7fd33
   - 事実: FCW の効果は初回曝露では見られず、繰返しで強く現れた。反復曝露と初期の車間時間に強く依存。
   - 示唆: 【推察】再警報は無効どころか反復で効く面がある。不応期は一律でなく車間状況で変える余地。
23. SAVE-IT Adaptive Safety Warning Countermeasures — Volpe/USDOT（年不明）。URL: https://www.volpe.dot.gov/sites/volpe.dot.gov/files/docs/SAVE-IT%20-%20Adaptive%20Safety%20Warning%20Countermeasures.doc
   - 事実: 「Alert Suppression」はドライバーが注意を向けている時に警報を出さない適応。タイミングの数値は抜粋になし。
   - 示唆: 【推察】ドライバーモニタ映像が前提で、CAN のみの推論には直接使えない。概念のみ参考。
24. NHTSA 接続車両の複数衝突リスク時の警報提示（URL の node が該当文書かは未特定）。URL: https://nhtsa.gov/node/10181
   - 事実: 個別に出すか、最初だけ出して後続を抑制するかを検討したと記述。結論・数値は抜粋になし。
   - 示唆: 【推察】「最初だけ出して後続を抑制」は不応期・ラッチの先行例候補。本文確認が必要。
25. ISO 17361:2017（LDWS 性能要求・試験法、Amd 1:2023）。URL: https://www.iso.org/standard/72349.html
   - 事実: 再警報間隔・抑制規則・ヒステリシス値は検索から得られなかった（規格は有償）。

## 3. 統合アーキテクチャ（12）への反映点

- L4（警報ポリシー）: 不応期を一律にせず、(a) 持続条件（何窓連続で閾値超過なら発報。医療の14〜19秒、15〜90秒遅延が桁の参考）、(b) 段階上昇時のみ再発報を許す階層ルール（Capan 型）、(c) 窓内 N 回/分の頻度による chattering 判定、の3要素を設計パラメータとして持つ。【推察】
- L5〜L6: 一次（車内警告）と二次（車外記録・通知）で遅延・抑制を分ける二段構成。【推察】
- L6: 評価は不応期長ごとに「警報件数（件/走行時間）・見逃し・検出遅延」の3軸の曲線で出す（Tulsyan 系・time-deadband 系の FAR/MAR/EDD の定式化に倣う）。医療文献は件数削減率しか出していないものが多い。【推察】
- 変えるべき前提: 再警報は一律に有害ではない（FCW の反復曝露で効果が出る報告）。抑制は車間・段階に依存させる余地がある。【推察】

## 4. 課題・ギャップ

- 運転の時間尺度（0.1〜数秒窓）での不応期長と警報率・見逃しの関係を測った公開研究は未発見。
- 医療の削減率は遡及計算が中心で、見逃しの定量が欠ける。孫引き数値（Philips 資料経由、Welch 経由）は一次未確認。
- FCW/LDW の再警報間隔・ヒステリシスの秒数は公開文献で未発見（ISO 17361 等は有償で未確認）。
- 全ソースが抜粋のみ（I-01）。NHTSA node の該当文書、Afzal & Chen 学位論文の URL 対応は未確認。

## 5. 次のアクション提案

1. comma2k19 等の公開走行データまたはシミュレータで、不応期0〜10秒・持続条件1〜5窓の掃引を行い、警報件数・見逃し・遅延の曲線を出す（設計タスク、I-11 に統合）。
2. 階層ルール（段階上昇時のみ再発報）と一律不応期を、同じ警報率で見逃し・遅延を比較する。
3. I-01 解消後、Capan 2018・Görges 2009・Wang & Chen 2014・NHTSA node 10181 の本文で数値を確定する。
4. UN R130（LDWS）・FMVSS 127・Euro NCAP の警報仕様で再警報間隔の規定の有無を確認する。
5. FCW 反復曝露（持ち越し効果）の一次を本文で確認し、再警報の効果を設計に反映する。

## 6. 参考文献リスト

2 章に記載の URL（25 項目、一部は補助 URL 付き）。確認方法は全件「抜粋のみ」。
