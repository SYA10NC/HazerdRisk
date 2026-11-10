# 23. 高齢ドライバー・初心者の運転特性とCANでの検出

- 調査日: 2026-11-10
- 論点: B-10。高齢・初心者ドライバーの操作特性・事故類型と、車両信号から年齢層・経験を推定、またはリスクを検出した研究
- 既存調査との関係: 01 §3.2（運転者識別の一般手法）、02（ドライバー状態）、18（踏み間違い）を前提とし、再調査していない。重なる踏み間違いは 18 を参照のこと
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）34件／既出の再掲 2件（[S35][S36]）。WebFetch は全対象ホストで名前解決に失敗（ISSUES I-01）。全件が WebSearch の抜粋のみで、本文は未読である
- 効く層: L1・L2（DRV＝運転者プロファイル）、L3（R3・R5）、L5（警告閾値の個人適応）

## 2. エグゼクティブサマリー

- CANの瞬時信号（操舵・アクセル・ブレーキ・車速）だけで年齢層を推定した、または年齢層別に事故予兆を検出した査読研究は、日英の複数クエリで見つからなかった（探した範囲は §5）。
- 近い例は次の4系統である。(a) 運転警報システムのデータで高齢者を判別（正答率0.859、書誌未特定）[S25]、(b) 高齢コホートの車載記録装置データでMCIを判別 [S26][S27][S28]、(c) 操作量による熟練度分類（主にシミュレータ）[S29][S30][S31]、(d) 初心者の加減速イベント率と事故リスク [S17][S21][S35]。
- 高齢者の事故類型は、警察庁・内閣府資料の抜粋では「操作不適」「車両単独」「工作物衝突・路外逸脱」が目立つ [S1][S2][S3]。ただし全国値と県値が混在し、数値の突合は本文確認後に行う必要がある。
- 初心者は免許取得後の初期（約6か月）にリスクが急速に変わるとされる（二次引用）[S19]。加減速イベント率は早期から持続するとの記述があり [S21]、少ない走行でのプロファイル化の根拠になりうる。【推察】
- 年齢・免許年数は CAN に流れない。【推察】運転者プロファイルは走行ログからの推定と、車両ID＋イグニッション履歴の管理が必要である。年齢で閾値を変えるより、個人内変化の追跡のほうが妥当と考える。

## 3. 主要知見

### 3.1 高齢ドライバー（年齢の定義）
- 警察統計は「高齢運転者」を65歳以上とし、死亡事故分析では75歳以上と75歳未満を比較する（宮城県警資料の見出しなどの抜粋による）。免許制度では、70歳以上で高齢者講習、75歳以上で認知機能検査、75歳以上かつ一定の違反歴で運転技能検査（令和4年5月13日施行）とされる（対応URLは未特定のため [S9] 参照）。内閣府の整理も65歳以上・75歳以上の2区分である [S3]。

### 3.2 高齢者の事故類型・操作特性（すべて抜粋のみ）
- [S1] 警察庁交通局「令和6年における交通事故の発生状況」。65歳以上の死者1,513人（前年比+47人）。75歳以上の高齢運転者による死亡事故は、免許保有者10万人当たりで75歳未満の約2.0倍。「車両単独」の構成率が約2.5倍との記述は千葉県警資料の記載で、全国値との関係は未確認。URL: https://www.npa.go.jp/publications/statistics/koutsuu/jiko/R06bunseki.pdf
- [S2] 警察庁「令和6年上半期における交通死亡事故の発生状況」。75歳以上は「操作不適」が多く、ブレーキとアクセルの踏み違いが前年同期比で約2.9倍とされる。URL: https://www.npa.go.jp/bureau/traffic/bunseki/kamihanki/060725R06kamihanki.pdf
- [S3] 内閣府 交通安全白書（令和7年版概要／令和8年版 topic_2）。65歳以上の運転者は交通死亡事故件数の約3割、操作不適の割合が高いとされる。URL: https://www8.cao.go.jp/koutu/taisaku/r07kou_haku/pdf/gaiyo.pdf ／ https://www8.cao.go.jp/koutu/taisaku/r08kou_haku/zenbun/genkyo/topics/topic_2.html（令和7年版は題名のみの抜粋）
- [S5] 愛知県警資料。運転操作の誤りが主因と思われる死亡事故の構成率は、75歳未満19.6%に対し75歳以上35.6%（平成28〜令和2年、原付以上）。1県の値。URL: https://www.pref.aichi.jp/police/koutsu/topics/images/koureiunten.pdf
- [S6] ホンダ「安全運転のススメ」（ITARDA データの二次引用）。ITARDA が2018年から認知機能検査データを受け取り不安全行動を分析しているとの言及。ITARDA 原典は未確認。URL: https://global.honda/jp/safetyinfo/senior/senior03.html
- [S7] ベストカーWeb（二次情報）。踏み間違い死亡事故は75歳以上が最多、車両単独事故は75歳以上が65〜74歳の倍近い。URL: https://bestcarweb.jp/feature/column/422080?prd=2
- [S10] Joshi ら, "Driver Age and Its Effect on Key Driving Metrics: Insights from Dynamic Vehicle Data", arXiv プレプリント（2025年1月）。自然走行で、有意な年齢差は主に75mph制限での速度遵守に見られ、ADAS を年齢別に調整する基準に使えると提案（アブストラクト断片のみ）。URL: https://arxiv.org/abs/2501.06918v1
- [S11] Merickel ら, "Real-Time Effects of Age-Related Cognitive Dysfunction on Driver Vehicle Control", Driving Assessment 2019。65〜90歳77名。認知機能低下は制動・加速に影響し、操舵には影響しないと報告（抜粋）。URL: https://pubs.lib.uiowa.edu/driving/article/id/28342/
- [S12] 高齢運転者の信号・無信号交差点での運転行動（2025年、シミュレータ39名）。無信号交差点で速度と操舵の変動が頻繁。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC12192173
- [S13] Staplin ら, "Older Driver Performance across Six Naturalistic Studies"（NHTSA DOT HS 813 181, 2021年）。232名を集約、SHRP2 も使用。クラッシュ・ニアクラッシュ時の反応に認知・身体機能指標と関連する差があると示唆。URL: https://rosap.ntl.bts.gov/view/dot/58549
- [S14] NHTSA 関連のシミュレータ報告「Comparison of Older and Younger Driver Responses to Emergency Driving Events」。緊急回避の反応時間とブレーキ踏力に年齢差はなく、交差点での横位置に差があった（年は未確認）。URL: https://rosap.ntl.bts.gov/view/dot/68204/dot_68204_DS1.pdf
- [S15] 高齢者のペダル操作・左折自然走行・SHRP2 の知見（抜粋）。アクセルからブレーキへの移行にためらい、左折は低速で長い間隙を待つ、高齢者のニアクラッシュは交差点が最多。個別URLは対応未特定のため、参照先として https://www.fhwa.dot.gov/publications/research/safety/17016/005.cfm を挙げるにとどめる（FHWA ページの内容は未確認）。
- [S17] Carleton 大学リポジトリ。健康状態が安定した高齢運転者は月ごとの加速パターンが安定していた（抜粋）。URL: https://curve.carleton.ca/c9191d8e-0ea2-4cf0-92c3-fb8d191afae5

### 3.3 初心者（定義と特性）
- 定義: 日本（茨城県警 交通白書）は「当該車両の免許取得後1年以内、国際免許・仮免許を除く」[S20]。米国 IIHS は年齢（16〜19歳）で区切る [S16][S17b]。
- [S16] IIHS "Fatality Facts: Teenagers"。16〜19歳の走行距離あたり死亡事故率は20歳以上の約3倍強、夜間は昼間の約4倍、速度超過が約3分の1に関与（抜粋）。URL: https://www.iihs.org/topics/fatality-statistics/detail/teenagers
- [S17b] IIHS Teenagers トピック。警察報告事故率は20歳以上の約4倍（3倍と4倍は指標の違い。【推察】）。URL: https://www.iihs.org/topics/teenagers
- [S18] CDC "Risk Factors for Teen Drivers"。危険の過小評価・認識不足（抜粋）。URL: https://www.cdc.gov/teen-drivers/risk-factors/
- [S19] Mayhew らの初期事故率低下（二次引用）。免許取得1か月目の約120件/1万人から6か月後に70件/1万人未満へ低下、最初の約6か月（約1000マイル）で急激。原論文は未確認。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC1942043（孫引き元。Mayhew 本人の論文かは未確認）
- [S20] 茨城県警 交通白書。定義の出典として使う（件数のみで率は無い）。URL: https://www.pref.ibaraki.jp/kenkei/a02_traffic/archives/white_paper/documents/29.pdf
- [S21] Simons-Morton らの Naturalistic Teen Driving 関連資料（VTTI の2資料を含む）。加速度計・GPS由来のイベント閾値は急ブレーキ ≤ -0.45 g、急発進 ≥ 0.35 g、急旋回 ≥ 0.50 g。新人ティーンのイベント率は親の約5倍、最初の6か月の率は18か月まで概ね維持（どの論文の記述かの対応は未確認）。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3556237（既出、[S35]）、https://www.vtti.vt.edu/PDFs/NDRS-2012-presentations/Simons-Morton%20G-Force%20Analyses%208-22-12.pdf
- [S22] Pradhan, Fisher ら RAPT 研究。新人の高リスクは先読み（リスク予測）不足が大きい。URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2563434（他に PMC2707454・PMC4180240・trid.trb.org/View/763123 が候補だが、個別内容は未確認）
- [S23] 岐阜県 初心運転者の事故資料。過去5年平均で、初心運転者は免許保有者の約1.5%に対し運転者事故の約4.0%、1万人あたり54.0件（全体20.3件）。1県の値。URL: https://www.pref.gifu.lg.jp/uploaded/attachment/435945.pdf
- [S24] 内閣府 専門委員会資料（ITARDA 統計引用）。免許人口あたりでは16〜19歳の事故件数が最多（抜粋）。URL: https://www8.cao.go.jp/koutu/kihon/keikaku10/senmon/k_2/pdf/s3_6.pdf
- [S29] 自動車技術会 論文集, "Effect of Different Driving Experiences on Following Vehicle Distance When Perceiving Road Rage"。シミュレータで、非熟練者はあおり知覚時の車間距離変化が大きい（抜粋）。URL: https://tech.jsae.or.jp/paperinfo/ja/content/jt202203.15/
- [S30] J-STAGE 運転技能の熟練差研究（バス運転士の訓練ログ等）。URL: https://www.jstage.jst.go.jp/article/jsmetld/2024.33/0/2024.33_PS2-4/_article/-char/ja（他の候補URLとの対応は未確認）
- [S31] FISITA 2010 F2010E015。操舵角と周波数係数で初心者/熟練者を SVM・PNN で識別（数値は抜粋になし）。URL: https://go.fisita.com/store/papers/FISITA2010/F2010E015
- [S32] テレマティクス保険（UBI）。City University of London の論文は加速・ブレーキ・旋回イベント頻度を使う。事業者の事故削減率は自己報告で因果不明のため引用しない。URL: https://openaccess.city.ac.uk/id/eprint/22515/1/acceptedNAAJ-1648.R1-withnames30_5_2019.pdf
- [S33] 英国 DfT・TRL の若年・新人運転者テレマティクス調査。リスクは経験不足とリスクテイクの両方に由来し、事故低減の証拠は決定的でない。URL: https://www.gov.uk/government/publications/telematics-research-impact-on-young-and-novice-driver-behaviour
- [S34] 若年ドライバーの kinematic 事象（PMC11581603）。免許1年以内のティーンで走行の10.9%に事象、100マイルあたり2.65件、閾値に標準が無い（抜粋）。URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11581603/
- [S34b] Teen driving レビュー（MDPI）。URL: https://mdpi.com/2313-576X/3/4/29

### 3.4 車両信号からの年齢・経験・認知機能の推定
- [S25] 運転警報システムの大規模データで高齢者/非高齢者をランダムフォレストで判別、正答率0.859、重要特徴量は車間距離警報の回数と発生時車速（抜粋。書誌は未特定で、候補URLは https://www.chugaiigaku.jp/upfile/browse/browse2691.pdf ほか2件のどれかは未確定。数値は書誌確認後に引用すること）。
- [S26] Columbia Engineering（Di ら, Geriatrics 2021）。LongROAD の65〜79歳2,977人、車載記録装置から29変数、MCI判別88%。上位は年齢・自宅近傍走行割合・トリップ時間・急ブレーキ回数。URL: https://www.engineering.columbia.edu/news/driving-behaviors-harbor-early-signals-of-dementia
- [S27] Nebraska の目的地モデルによる MCI 予測（再現率中央値0.68、GPS依存）。URL: https://trid.trb.org/View/2714573
- [S28] JMIR Medical Informatics 2026 の MCI 検出（全トリップ深層学習。題名・使用信号は未確認）。URL: https://medinform.jmir.org/2026/1/e83622
- [S37] Frontiers in Aging Neuroscience 2025（Putra ら）。脳MRIで運転性能低下高齢者を判別、実用には不十分と著者が記載。推論時に使えず、学習時の補助ラベル候補。URL: https://www.frontiersin.org/articles/10.3389/fnagi.2025.1462951/full
- [S38] Drexel 学位論文（2017年）。シミュレータ16件のみの初心者/熟練者識別。URL: https://researchdiscovery.drexel.edu/esploro/outputs/graduate/Classifying-human-driving-behavior-via-deep/991014632393404721
- [S39] SWOV 登録「Learning characteristic driving operations in curve sections that reflect drivers' skill levels」（シミュレータ、AdaBoost）。URL: https://swov.nl/nl/publicatie/learning-characteristic-driving-operations-curve-sections-reflect-drivers-skill-levels
- [S40] JSAE Review 30(4) の高齢運転者の分類（シミュレータ・質問紙のクラスタ分析と検索側が説明）。URL: https://www.jstage.jst.go.jp/article/jsaereview/30/4/30_4_461/_article/-char/en
- [S9] 免許制度の年齢区分は、神奈川県・内閣府・大阪府警の資料の抜粋による（対応未特定）。URL: https://www.pref.kanagawa.jp/documents/75843/r6-1-4.pdf
- 既出の再掲: [S35] PMC3556237（01・05 に既出）、[S36] arXiv 1710.04133（01・05 に既出。CAN からの運転者識別）。

## 4. 統合アーキテクチャ（12）への反映点（すべて【推察】）
- L1（特徴量）: アクセルオフ〜ブレーキオンの遅れ、制動開始時の距離・TTC（レーダ値がある場合）、車速維持の変動、左折・無信号交差点の低速、操舵と車速の変動、車間警報フラグ回数 [S25]。
- L2（DRV）: 年齢・免許年数は取れないため、急ブレーキ（-0.45 g 等の文献値を初期値）・急発進・急旋回のイベント率を運転者単位に集約し、数か月単位で更新する [S19][S21]。閾値は車種別に再校正する。
- L3（R3・R5）: 技能不足とリスク選好の2系統を分けて扱う [S33]。高齢者は操作不適・単独事故・交差点を優先リスクとする。
- L5（警告）: 年齢別の固定閾値より、個人内変化の追跡（月ごとの加速パターンの安定性 [S17]）を基本にする。年齢差を示す [S10] は ADAS の個人適応の根拠候補。
- L6（学習）: MRI など推論時に使えない情報は、学習時のラベルとしてのみ使う [S37]。

## 5. 課題・ギャップ
- CAN の瞬時信号だけで年齢層・熟練度を実路データで推定した研究は未発見。探したクエリ: driver age group classification from CAN bus; novice driver telematics crash risk; 運転者属性 推定 高齢運転者 車両挙動 CAN; older driver detect cognitive decline naturalistic; older drivers CAN braking steering age classification。DB は WebSearch のみ。
- ITARDA 原典（免許後経過年数別、高齢者の人的要因）、警察庁の令和6年通年の75歳以上「操作不適」割合、交差点での発見遅れの国内集計は取得できなかった。
- [S25] の0.859、[S34] の10.9%・2.65件、[S19] の事故率は書誌未確定または二次引用のため、数値は暫定である。
- 年齢の定義は制度により異なり（65・70・75歳）、研究間の比較には注意が必要である。
- 全件が抜粋のみ（I-01）。iihs.org、pmc.ncbi.nlm.nih.gov、jstage.jst.go.jp、npa.go.jp、www8.cao.go.jp、rosap.ntl.bts.gov の許可が要る。

## 6. 次のアクション提案
1. I-01 解消後に [S1][S3][S13][S25][S21] の本文を確認し、書誌と数値を確定する。
2. ITARDA の「イタルダ・インフォメーション」「交通事故分析レポート」から高齢者・若者の人的要因別データを特定する。
3. 運転者単位のイベント率プロファイル（L2）の設計メモを 12 に反映する（B-23 のドメイン適応と合わせる）。
4. 手持ちの CAN ログがあれば、急ブレーキ・急発進イベント率の運転者間分散を計測する。
5. 高齢者の個人内変化（縦断）を CAN で追う研究を追加検索する。

## 7. 参考文献リスト
上記 §3 の各 [S] 項目の URL を参照（すべて WebSearch 抜粋で実在を確認。本文未読）。
