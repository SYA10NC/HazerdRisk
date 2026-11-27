# 39. J1939 の AEBS 信号と、国内大型車・FMS における予防安全信号の外部公開状況

- 調査日: 2026-11-27
- 論点: B-17。J1939 の AEBS1/AEBS2 の PGN・SPN の確定、国内大型車（日野・いすゞ・三菱ふそう・UD）の予防安全装置と CAN 公開状況、FMS-Standard の公開 PGN 範囲
- 既存調査との関係: 24 §3.1（EBC1=61441、CCVS1=65265、EBC5=64964、AEBS2 の SPN 5681〜5683）、16 §2.3（ACC1=65135）、24 §3.3（国交省 大型車 AEBS 強化 2023-01）、06 §2.4 は除外した。24 に載っている CSS Electronics PGN 一覧と 16 の FMS 2.0 文書（thierry-lequeu.fr）は既出として再掲のみ
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）30件／既出の再掲 2件。補助（件数外）1件（mlit.go.jp 別版 001085173）
- 確認方法: WebFetch は arxiv.org に加え、isobus.net・csselectronics.com・docs.rs・static.nhtsa.gov・mlit.go.jp・bodybuilder.scania.com・govinfo.gov・eur-lex.europa.eu・wikipedia・omniplus.com などで名前解決に失敗した（I-01 継続）。全件 WebSearch の検索結果抜粋のみ。本文は 1 件も読んでいない
- 効く層: L0（入力・可用性）、L2

## 2. エグゼクティブサマリー

- AEBS1/AEBS2 の PGN 番号は、今回も確定できなかった。J1939DA は有償で、公開 DB（isobus.net・CSS Electronics）の本文が取得できなかったためである。
- SPN は 24 の 5681〜5683 に加え、5676〜5680 が AEBS 関連として検索抜粋に現れた（名称は英語要約）。PGN との対応、ビット幅、分解能は未確認である。
- FMS-Standard の公開項目は燃料・速度・回転数・ドライバーID など運行管理向けで、ADAS 状態（AEBS 作動・LDW・前方距離）が含まれるとする資料は見つからなかった（本文未読で、無いと断定はしない）。
- 日野・いすゞ・三菱ふそう・UD の 4 社とも、予防安全の警報フラグや前方車両距離を外部機器へ公開しているという一次資料は見つからなかった。国内はメーカークラウド経由の連携が見える範囲では主流である。
- 装備面は事実として整理できた（PCS・ドライバーモニタ・EDSS・60 秒無操作検知など）。ただし年式・地域差が大きい。
- 結論: 商用車の CAN のみ方式は、L0 の可用性ベクトルで「AEBS 系 PGN 受信なし」を既定とし、ADAS 警報なしでも動く縮退構成を前提にすべきである【推察】。

## 3. 主要知見

全て検索抜粋のみ。本文は未確認である。

### 3.1 J1939 の AEBS 関連 SPN・PGN

| SPN | 名称（検索要約の英語表現） | PGN | 出典 |
|---|---|---|---|
| 5676 | forward collision AEBS state | 未確認 | [1][2] |
| 5677 | collision warning level | 未確認 | [1][2] |
| 5678 | relevant object detection flag | 未確認 | [1][2] |
| 5679 | bend-off probability | 未確認 | [2] |
| 5680 | time to collision | 未確認 | [1] |
| 5681 | driver activation demand（24 の AEBS2 と一致） | 未確認 | [1] |
| 5682/5683 | AEBS2 の counter / checksum | 未確認 | [1] |

- 名称は検索要約の表現で、J1939DA の正式名称とは限らない。ビット幅・分解能・値の意味は未確認。
- 【推察】5680（time to collision）が実車で送信されるなら、L2 で TTC を計算せず直接使える可能性がある。ただし送信の有無は車両依存である。
- VDC2 の SPN、LDW の PGN/SPN は見つからなかった。検索に出た「PGN 41984 = 0xA400」などの番号は検索要約側の記述または探索語の仮説であり、出典として採用しない。

| # | ソース | 要点 |
|---|---|---|
| [1] | ISOBUS Data Dictionary SPN 一覧 39 頁（公開 DB）https://www.isobus.net/isobus/pGNAndSPN/index?type=SPN&PGNAndSPN_page=39 | SPN 5676〜5683 の名称を列挙（抜粋） |
| [2] | NHTSA ODI TSB「J-1939 Fault Code SA, SPN/FMI」2018 https://static.nhtsa.gov/odi/tsbs/2018/MC-10141869-9999.pdf | SPN 5676〜5683 を挙げる。PGN 対応なし（抜粋） |
| [3] | SAE「J1939 Enhanced DBC（202603）」https://saemobilus.sae.org/media/j1939-enhanced-dbc-j1939dbc_202603 | 2,400 超の PGN・16,000 超の SPN を含む有償 DBC。per user/PC ライセンス |
| [4] | SAE J1939DA_202606 Digital Annex https://saemobilus.sae.org/standards/j1939da_202606-j1939-digital-annex | 一次情報だが有償 |
| [5] | docs.rs j1939 crate spn.rs https://docs.rs/crate/j1939/latest/source/src/spn.rs | 検索ヒットのみ。AEBS の有無は不明 |
| [6] | docs.rs dbcc 例 j1939.dbc https://docs.rs/crate/dbcc/latest/source/examples/j1939.dbc | 同上 |
| 既出 | CSS Electronics J1939 PGN List（24 [6]）https://www.csselectronics.com/pages/j1939-pgn-list | 検索要約では AEBS1/AEBS2 が一覧にあるとされるが PGN 番号は出ず、本文は取得失敗 |

### 3.2 FMS-Standard と商用車 AEBS 規制

| # | ソース | 要点 |
|---|---|---|
| [7] | FMS-Standard interface description v01.00（Scribd 写し）https://www.scribd.com/document/415007879/Fms-Standard | 作業グループは Daimler・Scania・MAN・Volvo・DAF・Iveco・Renault（抜粋） |
| 既出 | FMS 2.0 文書 2010-11-11（16 で既出）https://www.thierry-lequeu.fr/data/fms_document_ver02.00vers_11_11_2010.pdf | CCVS（65265）、EEC2（61443）などの例示（抜粋） |
| [8] | Scania「CAN Communication Specification for FMS」https://bodybuilder.scania.com/content/dam/bodybuilder/local-page/thailand/CAN_Communication_Specification_for_FMS.PDF | FMS-Standard 03 版対応と記載。詳細は fms-standard.com 参照とある |
| [9] | Scania「CAN interface for FMS」https://bodybuilder.scania.com/content/dam/bodybuilder/local-page/thailand/CAN_interface_for_FMS.PDF | 同上 |
| [10] | AU Electronics simfms マニュアル https://www.auelectronics.com/downloads/usermanual_simfms.pdf | 「FMS-Standard Version 04」（2017-10-13 とする要約）に言及。安全内容は不明 |
| [11] | EU 2025/1329（UN R131 改訂）https://eur-lex.europa.eu/eli/reg/2025/1329/oj | 大型車 AEBS の改訂。新型式 2025-09、全新車 2028-09 とする要約。要確認 |
| [12] | CLEPA 解説 https://clepa.eu/?p=20952 | R131 改訂の業界解説（抜粋） |
| [13] | NHTSA/FMCSA NPRM「Heavy Vehicle AEB」2023-07-06 https://www.govinfo.gov/content/pkg/FR-2023-07-06/html/2023-13622.htm | 10,000 lb 超が対象。FCW を AEB の一部とする。最終規則の有無は未確認 |
| [14] | NHTSA NPRM 文書ページ https://www.nhtsa.gov/document/nprm-heavy-vehicles-automatic-emergency-braking-systems | 同上 |

- 【推察】R131 は警報・故障表示・無効化表示の存在を定めるが、CAN/J1939 上の符号化は定めていないとみられる（抜粋ベース）。FMS の版別（03〜05）の安全信号の有無は、検索では確認できなかった。

| FMS 版 | 基本信号 | AEBS 状態 | ACC 距離 | LDW | ドライバー状態 |
|---|---|---|---|---|---|
| 01〜02（2009〜2010） | あり（CCVS・EEC2 等、抜粋） | 抜粋に無し | 抜粋に無し | 抜粋に無し | 抜粋に無し |
| 03・04・05 | 未取得 | 未確認 | 未確認 | 未確認 | 未確認 |

「抜粋に無し」は不在の証明ではない。

### 3.3 国内（日本語）・FMS の公開範囲と第三者接続

| # | ソース | 要点（事実） |
|---|---|---|
| [15] | 国交省「FMSスタンダードについて」https://www.mlit.go.jp/jidosha/content/001994650.pdf | FMS は 2001 年に欧州 4 社が合意。外部機器は FMS ユニット経由で CAN に接続し、メーカーは FMS 以外の CAN 接続を禁じる。取得項目例は燃料消費・残量・エンジン出力率・回転数（抜粋）。補助: https://www.mlit.go.jp/common/001085173.pdf |
| [16] | iWave Global FMS 解説 https://iwave-global.com/ja/articles/fms-standard-for-commercial-vehicles-enabling-smarter-unified-fleet-management/ | FMS 2.0（2010）で PTO・ドライバーID・詳細燃費、3.0（2012）でトラック/バス統一（抜粋、ベンダー記事） |
| [17] | Teltonika FM5500 マニュアル https://manualshive.com/en/manual/teltonika/fm5500/1084754?page=111 | FMS は OEM のオプションで、取得項目は装備依存 |
| [18] | Teltonika ブログ https://www.teltonika-gps.com/blog/what-is-can-bus-a-fleet-management-guide | J1939/FMS は全パラメータを網羅しない |
| [19] | Navixy ブログ https://navixy.com/blog/telematics-commissioning-gate/ | FMS ゲートウェイは第三者に事前記述の範囲のみ許す、との主張（ベンダー） |
| [20] | ドコマップジャパン https://www.docomap.jp/en/notice/64 | 日野・三菱ふそうのテレマ経由で位置と車速を連携。年式限定 |
| [21] | Response 日野レンジャー改良 2026-08-28 https://response.jp/article/2026/08/28/415833.html | 標識認識とデジタコが全車標準 |
| [22] | LNEWS いすゞ ギガ 2019-12 https://www.lnews.jp/2019/12/l122721.html | 脇見・開眼監視、PCS の検知拡大 |
| [23] | TRAFFIC NEWS いすゞ EDSS https://trafficnews.jp/post/107128 | 急病時の自動停止（EDSS）を国内トラックで初採用（2021-05 とする要約） |
| [24] | TRAFFIC NEWS ふそう ADA3 https://trafficnews.jp/post/107734 | 2025-03 から順次。約 60 秒ハンドル無操作で警告・減速停止 |
| [25] | Car Watch ふそう https://car.watch.impress.co.jp/docs/news/1671697.html | 車線変更時の衝突回避支援（要約） |
| [26] | UD Trucks クオン安全装備（豪州サイト）https://www.udtrucks.com/australia/trucks/quon/safety | ドライバーモニタは 2022 モデルで追加など。地域差あり |
| [27] | Logi-Today UD クオン https://www.logi-today.com/535686 | LKA・車輪脱落予兆の改良報道 |
| [28] | 日刊工業新聞 コネクテッド拡大 https://www.nikkan.co.jp/articles/view/00509979 | 約 7 年前の報道。技術仕様なし |
| [29] | Daimler Truck Australia Connected Vehicle Data Policy https://daimlertruck.com.au/contentassets/11160e6d522e4b81a705fa8b158dfb33/connected-vehicle-data-policy_04062024-1.pdf | FUSO 車両のテレマ送信。豪州向けで日本とは限らない |
| [30] | Volvo Buses Active Safety Fact Sheet 2023 https://www.volvobuses.com/content/dam/volvo-buses/markets/master/why-volvo/safety-first/Fact-sheet-Active-Safety-Systems-EN-Volvo-Buses-2023.pdf | 機能説明のみ。CAN 内容なし |

国内 4 社の信号公開状況（探した範囲）:

| 社 | 予防安全装備（報道ベース） | 外部への CAN/FMS 公開 | ADAS 警報・前方距離の公開 |
|---|---|---|---|
| 日野 | PCS・ドライバーモニタ（古い報道） | 不明 | 不明 |
| いすゞ | PCS、ドライバーモニタ、EDSS | 不明（北米向け Isuzu は FMS ポートの報告あり、抜粋） | 不明 |
| 三菱ふそう | ADA3、無操作検知 | 不明（クラウド経由で車速・位置） | 不明 |
| UD | ドライバーモニタ、LDP/LKA、BSIS | 不明 | 不明 |

「不明」は一次資料が見つからなかったという意味で、非公開の証明ではない。

## 4. 統合アーキテクチャ（12）への反映点

- L0: 商用車では AEBS 系 SPN（5676〜5683 など）の有無を車両ごとに実測する前提とし、可用性ベクトルに「PGN 送信元・受信周期・SPN の有効値」を持たせる。国内大型は既定で「ADAS 系なし」とする【推察】。
- L2: ADAS 信号が無い車両向けに、EBC1/CCVS1・車速・ステアリング由来の縮退特徴で動く構成を併設する。ハンドル無操作検知（ふそう ADA3 の約 60 秒）は、ステアリング角 CAN から再現を試せる【推察】。
- L6: 国内大型の評価は、OEM クラウド経由の車速・位置のみが取れる場合の粒度（秒単位か分単位か）を別途確認する。

## 5. 課題・ギャップ

- AEBS1/AEBS2/VDC2/LDW の PGN と SPN の対応・ビット幅は未確認（isobus.net・J1939DA 本文が必要）。
- FMS 03〜05 の版別 PGN 一覧は未取得（fms-standard.com に到達できない）。
- 国内 4 社の外部機器接続仕様書（架装要領書・デジタコ接続）は未探索。
- 各社クラウド API（HINO CONNECT など）が ADAS イベントを返すかは未調査。
- 検索の英語要約に含まれる PGN 番号は検証できず、採用していない。

## 6. 次のアクション提案

1. isobus.net・csselectronics.com・fms-standard.com・mlit.go.jp・github.com を許可後、AEBS1/AEBS2 の PGN を本文で確定し 24 に【訂正】追記する。
2. GitHub の J1939DA 由来 JSON（pretty_j1939 など）と SPN 5676〜5683 を突合する。
3. 国内デジタコ各社（矢崎・デンソー等）の車両信号接続仕様を調べる（新テーマ B-35）。
4. HINO CONNECT 等の OEM クラウドが返す安全イベントの種類を調べる（B-36）。

## 7. 参考文献リスト

3.1〜3.3 の表の URL を参照。既出: https://www.csselectronics.com/pages/j1939-pgn-list 、https://www.thierry-lequeu.fr/data/fms_document_ver02.00vers_11_11_2010.pdf
