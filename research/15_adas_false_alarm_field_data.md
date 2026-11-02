# 15. 量産ADASの誤警報・不要作動の実測データと偽警報率の定義比較（B-02）

- 調査日: 2026-11-02
- 論点: 量産 FCW・LDW・DDAW・AEB の誤警報・不要作動を実測した公的データ・研究を集め、偽警報率の定義（/100km、/h、PPV など）の違いを比較する
- 既存調査との関係: 10 §2.4（警報疲れ）・§3.1〜3.3（警報分類・KPI・ROC 運用点）、10 の Seaman ら、IVBSS、Euro NCAP 2026 の誤警報の扱い（04・10）は扱い済みとして除外した。14 に載っている URL（tongji 論文、arXiv 2510.22260）と 02 の Euro NCAP Driver Engagement は既出として再掲にとどめた
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）31件／既出の再掲 3件
- 確認状況: WebFetch は arxiv.org、govinfo.gov、iihs.org、ncbi.nlm.nih.gov など調べた全ホストで名前解決に失敗した（ISSUES I-01）。以下の数値はすべて WebSearch の検索結果の抜粋に基づき、一次資料との照合はしていない。ソース間で数値が食い違う箇所は併記する

## エグゼクティブサマリー

- 「率」として分母つきで誤警報を報告した量産 ADAS の公的フィールドデータは、今回の探索では見つからなかった。得られたのは、苦情件数、無効化率（オフにされた割合）、満足度（PP100）、アンケートの自己申告であり、いずれも誤警報の発生率ではない。
- 不要作動は規制側でも問題視されている。NHTSA は FMVSS 127 に false activation 試験を入れた（数値は未取得）。Honda の AEB 調査は PE22-003 から EA24002 に格上げされた。
- 単位は研究ごとにばらばらである（/1,000マイル、/回避イベント、/警告、/分、/サンプル）。/100km や /h に直接換算できる数値は 0 件であった。換算できるのは全警報頻度の 1 件のみ（筆者計算）。
- 利用者の離脱は LDW が最も大きく、FCW/AEB は小さい傾向が複数の調査で一致する。
- 【推察】CAN のみ方式の KPI は、/h（利用者が体感する頻度）と PPV（警報の当たり率）の両方を、分母を明記して報告する必要がある。

## 主要知見

### 3.1 NHTSA の不要作動（phantom braking）調査・規則（サブ論点1）

| # | タイトル / 組織 / 年 / 種別 | URL | 要点（事実） | 示唆 |
|---|---|---|---|---|
| N1 | FMVSS 127 最終規則（89 FR 39686）/ NHTSA / 2024-05-09 / 連邦官報 | https://www.govinfo.gov/content/pkg/FR-2024-05-09/html/2024-09054.htm | 目次に False Activation Requirement 節がある。AEB は 2 つの false activation 試験に合格する必要があり、全車の適合期限は 2029-09-01（抜粋） | 【推察】減速度閾値は未取得。本文確認後に 10 §3 へ反映 |
| N2 | 同規則の再検討決定（89 FR 93199）/ NHTSA / 2024-11-26 | https://www.federalregister.gov/documents/2024/11/26/2024-27349/federal-motor-vehicle-safety-standards-automatic-emergency-braking-systems-for-light-vehicles | 一部の petition を認め、試験シナリオを修正（抜粋）。false activation 試験への影響は不明 | N1 の数値はこの改正後か要確認 |
| N3 | Tesla PE22002 終了報道 / Drive Tesla Canada / 2026 / 報道 | https://driveteslacanada.ca/news/tesla-phantom-braking-investigation-closed-nhtsa/（news 2026-11 に既出） | 2022-02 開始、約 70 万台。苦情は 2024 年 45 件、2025 年 19 件、2026 年上期 3 件との報道。ACC/TACC 系で、NHTSA は AEB と別事象とした。台数・件数は報道間で食い違う | 苦情件数は分母（走行距離・作動回数）がなく発生率にならない |
| N4 | Honda CR-V/Accord の AEB 不要作動（PE22-003→EA24002）/ AP / 2024-04-17 | https://qz.com/us-probe-of-hondas-that-can-activate-emergency-braking-1851417464 | 2022-02 開始時は約 170 万台、苦情 278 件。EA 格上げ時は約 300 万台。47 件の衝突、負傷は 93 件または 112 件と要約により異なる。ディーラーで再現しない例がある | 【推察】再現しない作動は、CAN ログ（車速・距離・ブレーキ要求）で後追い検証できる |
| N5 | Nissan Rogue AEB 調査 / Transport Topics / 2019 | https://www.ttnews.com/articles/nhtsa-opens-probe-nissan-rogue-automatic-emergency-braking | 対象約 55.3 万台。カナダのリコール報道では金属構造物（踏切、頭上標識）が誘因とされる。件数は報道で 14 件、約 750 件、840 件超とばらつく | 【推察】静止物に対する距離・相対速度の急変を検知する特徴量の根拠になる |
| N6 | Honda リコール 3566 / 本田技研工業 / 2015-05 | https://www.honda.co.jp/recall/auto/info/150514_3566.html | ミリ波レーダのプログラム不適切で防護柵を障害物と誤認し急制動のおそれ。対象台数の表記は 9,966 台ほか | 原因分類（レーダ誤認識）の例。届出台数であり発生件数ではない |
| N7 | AEB「過信」事故の注意喚起 / 乗りものニュース（国交省発表の報道）/ 2019 | https://trafficnews.jp/post/92240 | 過信とみられる事故が 2017 年 72 件、2018 年 101 件、2019 年 1〜9 月 80 件 | 不作動・過信の件数であり、誤警報ではない。取り違え注意 |
| N8 | Freightliner AEB 調査 / Land Line / 2024 | https://landline.media/?p=81566 | 2023-05 の調査で、障害物がないのに作動したとの苦情が 18 件との記述 | 二次報道。一次資料の確認が必要 |

探したが見つからなかったもの: Ford の AEB 不要作動を扱った NHTSA 調査・リコール（Mach-E の別件のみ）、Honda EA24002 の最終結果、FMVSS 127 の false activation 試験の数値。

### 3.2 IIHS・FOT・消費者調査（サブ論点2）

| # | タイトル / 組織 / 年 / 種別 | URL | 要点（事実） | 示唆 |
|---|---|---|---|---|
| F1 | 11 car technology features drivers disable most / Erie Insurance / 2020 / 保険会社調査 | https://www.erieinsurance.com/newsroom/press-releases/2020/car-safety-survey | 2016〜2020 年式の車を持つ米国ドライバー 500 人。LDW をオフにする人 21%（理由の一つが誤警報の多さ）、FCW は搭載車の 11%、DMS は 22% がオフ。別抜粋に AEB 17% の記載もあるが出所の違いは未確認 | 自己申告の無効化率であり誤警報率ではない |
| F2 | Fewer drivers are opting out of lane departure prevention / IIHS / 2025 / 観察研究 | https://www.iihs.org/news/detail/fewer-drivers-are-opting-out-of-lane-departure-prevention | ワシントン D.C. 地域で整備入庫した約 2,400 台。LDW/LDP の有効率 87%、前方衝突防止 96%（別抜粋は 94%）。2016 年調査の LDW は 51%（報道）。音の警報が切られやすい | 【推察】無効化率は HMI 設計で大きく変わり、閾値だけでは説明できない |
| F3 | Subaru DriverFocus オーナー調査 / IIHS / 2025-08 | https://www.iihs.org/research-areas/bibliography/ref/2344 | オーナー 3,475 人。一部の警報を誤検知と認識。切った人は 4% で、主因は警報過多と不快感 | 映像 DMS は対象外。ただし「誤警報と感じること」と実際の誤検知は一致しない点は L6 の評価設計に使える【推察】 |
| F4 | LDW のオーナー調査 / IIHS を報じた Globe and Mail / 2012 年頃（推定）/ 二次報道 | https://www.theglobeandmail.com/globe-drive/news/two-car-safety-technologies-you-definitely-need/article4403996 | 誤警報または不要な警報の経験が Volvo 43%、Infiniti 46%。「うっとうしい」は Volvo 25%、Infiniti 41% | 主観申告。原典未特定 |
| F5 | NHTSA 連邦官報公示 / NHTSA / 2025 | https://public-inspection.federalregister.gov/2025-06077.pdf | ドライバーは LDW を「最大 50% の頻度で」オフにするとの趣旨（二次引用、根拠調査は不明） | 単独で数値として使わない |
| F6 | U.S. ADAS study / J.D. Power / 2022〜2024 | https://www.jdpower.com/sites/default/files/file/2022-11/2022138%20U.S.%20ADAS.pdf | 2022 年は ADAS が 23.1 PP100、うち LDW/LKA 6.3、FCW/AEB 4.6。2024 年は 24.9 PP100 で警報が苦情の最多（報道） | PP100 は満足度指標で誤警報率ではない。LDW 系 > FCW 系の順は一貫 |
| F7 | Road Departure Crash Warning FOT / UMTRI・NHTSA / 2006 | https://rosap.ntl.bts.gov/view/dot/9533/dot_9533_DS1.pdf | 11 台・78 人、約 13 万 km（独立評価）。レーダ入力で警報閾値を調整し nuisance 警報を削減 | 時間・距離あたりの率は抜粋にない。試験システムで量産品ではない |
| F8 | ACAS FOT 記録 / USDOT ITS KRS / 2007 | https://www.itskrs.its.dot.gov/2007-l00328 | FCW の最低作動速度を 25 mph より上げても、誤警報・nuisance 警報は 50% 超は減らない | 【推察】速度閾値だけでなく、先行車との関係で判定する必要がある（ACAS の別 URL は 10 に既出） |
| F9 | 自然運転での FCW 2,000 件超のレビュー / Chalmers と推定 / 年不明 | https://odr.chalmers.se/handle/20.500.12380/118609?locale=en | 敏感な FCW は衝突確率が低い状況で多数の警報を出し、切迫と判断されたのは 9 件のみ（抜粋）。抜粋との対応は未確認 | 【推察】警報フラグそのものを教師ラベルにすると PPV が極めて低い可能性 |
| F10 | トラック FCW の誤警報評価 / 同済大学 / 2024 | https://tjsafety.tongji.edu.cn/65/d0/c36037a353744/page.htm（14 に既出） | 回避イベント 450 件中、誤警報 47 件（11.19%）。車間が近いと 30% 超 | 分母が「回避イベント」。走行距離あたりではない |
| F11 | 先進安全自動車に関する調査 / 国民生活センター / 2018-01-18 | https://www.kokusen.go.jp/news/data/n-20180118_1.html | ハイテクカー所有者 2,000 人のうち、想定外の出来事の経験者は 25%（J-CAST 経由）。相談 142 件中 119 件が衝突被害軽減ブレーキ（ベストカー経由） | 想定外の作動であり警報の誤警報率ではない。逆算した母数が合わない旨の指摘あり |
| F12 | JAF ASV 認知度アンケート / JAF / 2016 | https://trafficnews.jp/post/52660/ | 名称の認知 97.3%、作動しない条件まで知る人 24.8% | 期待と実挙動のずれが nuisance 認識の背景【推察】 |

探したが見つからなかったもの: euroFOT・UDRIVE・SeMiFOT・日本 FOT での誤警報率（/100km、/h）、HLDI のステータスレポート本体、車種別のオフ率表。

### 3.3 偽警報率の定義と換算（サブ論点3）

| # | 分野 | 報告単位 | 分母 | 数値（抜粋内） | 出典 URL |
|---|---|---|---|---|---|
| D1 | FCW 実走行（Volpe/NHTSA） | 警報回数/1,000 マイル | 走行距離（全警報） | 平均約 21、個人差 0.7〜101 | https://nhtsa.gov/node/10346（数値との対応は未確認） |
| D2 | 事故予測 | FAR（偽陽性率）を λ で制約 | 非事故側の判定【推察】 | λ=0.1（既定） | https://arxiv.org/pdf/2510.22260（14 に既出） |
| D3 | 事故予測 | FAR の実用例 | 時間（分） | 「1 回/分超は許容不可」 | 同上 |
| D4 | LDW | 偽警告の割合 | 警告数または試験時間（不明） | 1.18%（47/4000）、0.32% | https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/barickman_lanedepartuerwarning_final.pdf（対応未確認） |
| D5 | LDW（西オーストラリア） | 警告イベントに占める失敗 | 警告イベント | 19%（35/189）、路肩では正解 39% | https://www.wa.gov.au/system/files/2021-08/Automated-Driving-Lane-departure-Warning-LDW-project-report_1.pdf |
| D6 | LDW（機械学習） | 偽警報率（%） | 不明 | TLC 比で 12.9% 減（相対値） | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7038345/ |
| D7 | 眠気（行動検知） | 偽警報率 | 非対象サンプル | 3.06% 以下 | https://arxiv.org/pdf/2503.23393 |
| D8 | 眠気（呼吸信号） | 偽陽性/時間（先行研究の引用） | 時間 | 約 1.7/h | https://www.scribd.com/document/584522946/10-1109-ACCESS-2019-2924481（孫引き） |
| D9 | 規格 | False alarm test（ISO 17361:2017 の目次 5.6.3） | 有償本文で未確認 | - | https://genorma.com/en/standards/iso-17361-2017 |

換算の例（筆者計算）: 約 21 警報/1,000 マイル ÷ 1.609 ≒ 約 1.3 警報/100 km。これは全警報の頻度であり、偽警報の比率は別途必要である。分母が「サンプル」「イベント」「警告」のものは、走行距離・時間の情報がないと /100km や /h に換算できない。

## 統合アーキテクチャ（12）への反映点

- L6（検証）: 誤警報 KPI を 3 通りで併記する。(a) /h（体感頻度）、(b) PPV（警報のうち真の危険だった割合）、(c) /100km（比較用）。いずれも分母と、警報の定義（フラグ立上り回数かイベント数か）を明記する【推察】。
- L5（警告）: 無効化率は HMI 設計（音かハプティクか、解除の手間）で変わるという F2 の知見から、警報モダリティ設計を L5 の評価項目に入れる。
- L4: ACAS の知見（F8）から、速度閾値だけでなく相対状態で判定する。
- L3 の教師ラベル: 量産 FCW の警報フラグをそのままラベルにすると PPV が低い可能性がある（F9）【推察】。
- L2/L1: 不要作動の誘因（静止物、防護柵）に対し、距離・相対速度の信号が急に有効値になる不整合を検知する特徴量が候補（N5、N6）【推察】。

## 課題・ギャップ

- 本文確認が 0 件である。FMVSS 127 の false activation 試験の数値、ODI resume の件数、IIHS の有効率の食い違い（LDW 32%/51%、前方衝突防止 94%/96%）は未解消。
- 率を分母つきで出した量産 ADAS のフィールドデータは未発見。euroFOT・UDRIVE の一次報告の本文が必要。
- 日本の FOT・JNCAP の誤警報データは見つからなかった。

## 次のアクション提案

1. ISSUES I-01 の解消後、govinfo.gov・nhtsa.gov・iihs.org を許可し、N1・N3・N4・F2 を本文確認する。
2. UMTRI-2006-9-1（F7）と ACAS 報告書の nuisance 警報の表を読み、/h 換算を試みる。
3. 誤警報 KPI の定義書（分母・単位・換算）を 12 の L6 向けに起こす（設計タスク）。
4. J-STAGE で国内 FOT・自動車技術会の誤警報報告を検索する。
5. Euro NCAP の誤警報の合否基準の一次資料を確認する。

## 参考文献リスト

3.1〜3.3 の各表の URL を参照。補助 URL: https://www.nhtsa.gov/node/10191（RDCW 報告 Vol.1）、https://arxiv.org/abs/2603.14841（運転安全スコア、確認のみ）。
