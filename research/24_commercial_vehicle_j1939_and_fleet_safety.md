# 24 商用車（J1939）・バス・トラックでの事故予防とCAN活用

- 調査日: 2026-11-11
- 論点: B-11。J1939 で取れる安全関連 PGN/SPN、国内デジタコの危険運転判定、国内外の事業用（大型）車の事故統計
- 既存調査との関係: 03 §3.1（J1939 概要）、06 §2.4・§6.1-5（フリート事例・デジタコ閾値は非公開）、16 §2.3（ACC1 = PGN 65135、SPN 1586/1587/5022）、04 §4（事故統計概要）は扱い済みとして除外した。本稿はその先（AEBS・EBC 系 PGN、デジタコの法定要件、事業用事故の目標・類型）だけを扱う
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）29件／既出の再掲 0件。WebFetch が全ホストで名前解決に失敗（ISSUES I-01）し、GitHub MCP は本リポジトリ以外を許可しないため、全ソースが検索結果の抜粋のみである

## 2. エグゼクティブサマリー

- J1939 の安全関連信号のうち、本調査で出典付きで挙げられたのは EBC1（PGN 61441）、CCVS1（PGN 65265）、EBC5（PGN 64964）と AEBS2 の SPN 3件にとどまる。AEBS1/AEBS2 の PGN 番号と AEBS1 の SPN 番号は確定できなかった（J1939DA は有償で、公開 DBC は ADAS 系を含まない例が多いとの記述がある）。
- 緊急制動作動フラグ（SPN 5847、EBC5）という AEBS1 以外の経路が見つかった。ただし抜粋のみである。
- 国内デジタコの法定要件は速度・距離・時間の3要素の記録と精度（告示）であり、急加減速・急ハンドルの判定閾値は公開資料で確認できなかった。06 §6.1-5 の結論は覆らない。
- 国内ではメーカーが FMS 以外の CAN 接続を認めていないとの国交省系資料の記述があり、外付け機器は車速パルスか FMS 経由に制約される可能性がある。
- 事業用自動車の令和6年実績は 24時間死者286人で、令和7年目標225人を大きく超過している（S1）。追突・健康起因が主要な対象である。
- 米国 LTCCS（2006）では非遂行（居眠り・発作等）が critical reason の12%、同一車線の前車追突が critical event の22% とされる（抜粋）。2000年代のデータで、AEB 普及後の構成は異なる可能性がある。
- 総じて「CAN のみで商用車の予兆を検知する」ことの一次資料は不足しており、信号の可用性確認が先決である。

## 3. 主要知見

### 3.1 J1939 の安全関連 PGN/SPN（全て抜粋のみ）

| PGN | 名称 | SPN | 内容 | 出典 |
|---|---|---|---|---|
| 61441 | EBC1 | 561/563/1243/521 | ASR 作動／ABS 作動／ABS 完全動作／ブレーキペダル位置 | [1] |
| 65265 | CCVS1 | 84/596/597/599/600 | 車速（1/256 km/h、100 ms、Hatz 資料）／クルーズ有効／ブレーキSW／セット／コースト | [3][4] |
| 64964 | EBC5 | 5847 | Emergency Braking Active | [2] |
| 未確認 | AEBS2 | 5681/5682/5683 | AEBS 作動の運転者要求／カウンタ／チェックサム | [5] |
| 未確認 | AEBS1、VDC2 | 未確認 | PGN 一覧に名称のみ | [6] |

- 【推察】AEBS1/2 と VDC2 は標準 DBC に収録されていると思われるが、番号は一覧本文で確認する必要がある。検索 AI が示した AEBS1 の SPN（2888/2889）は出典がなく採用しない。
- LDW の J1939 PGN は見つからなかった（検索で出た SPN は ISOBUS 側の定義）。【推察】独自 PGN の可能性。
- 同一 SPN でも送信元アドレスが車種・版で変わる（Prevost 資料）[4a]。ログ解析で SA を固定しない設計が要る【推察】。
- J1939 DBC は J1939DA の電子表現で、SAE は知的財産とみなす（Kvaser）[8]。公開 DBC の網羅性に限界がある。

### 3.2 国内デジタコ・運行管理（全て抜粋のみ）

- 保安基準の細目告示（運行記録計）は、24時間以上の瞬間速度と走行距離の自動記録を求め、許容誤差を瞬間速度は最高目盛の3％以内、距離は100kmにつき1km以内、時間は24時間につき3分以内とする（抜粋）[9]。急加減速の判定は法定要件の外【推察】。
- 厚労省資料の抜粋に、運行管理情報の例として急加速・急減速警報があるが、発生条件の数値は抜粋に無い [10]。
- 国交省系資料の抜粋は、FMS では車両メーカーが FMS インターフェース以外の CAN 接続を禁じていると記す [11]。【推察】国内の後付け機器は CAN 直読みに制約がある。
- 矢崎 YDX-8（ドラレコ一体型、クラウド連携）[12]、デンソーのドライビングパートナー（危険運転時の前後20秒の記録、判定G値は記載なし）[13]、LEVO の運行管理連携型デジタコ選定リスト（109型式、令和8年7月1日付）[14] を確認したが、いずれも閾値・信号方式の記載は抜粋に無い。
- Teltonika（海外）の資料は、J1939・FMS ともに全パラメータを網羅せず OEM 独自解釈が要ると述べる [15]。

### 3.3 事業用自動車の統計・規制（全て抜粋のみ。数値は原典再確認が必要）

- 事業用自動車総合安全プラン2025: 令和7年目標は24時間死者225人以下、トラック追突件数3,350件以下など。令和6年実績は24時間死者286人、人身事故22,623件、22目標のうち6指標達成（抜粋の要約）[16]。
- 事業用自動車の傾向分析・事故統計年報は令和5年版が掲載（令和6年版は未確認）[17]。
- 健康起因: 令和4年は報告のうち3割が交通事故に至った（抜粋）。北陸信越の令和6年の重大事故は健康状態が20件・25.3%（地域限定）[18]。事故調査委員会の追突事例に体調不良下の運転がある [19]。
- 大型車 AEBS: 3.5t 超が対象、歩行者対応は新型車2025年9月・継続生産車2028年9月 [20][21]。UN-R131 の改定は2023年1月とする解説もある [22]。
- 米国: NHTSA/FMCSA の大型車 AEB 提案規則（2023年）は 10,000 lb 超が対象で、追突する側の事故を年約6万件と推計。最終規則は未確認 [23]。
- LTCCS: 非遂行12%、同一車線の前車追突22%（critical event）。確率標本に基づく推定で過失認定が目的ではない [24]。FMCSA 概要資料の2022年の死亡事故関与は5,252件、ただし他の集計と食い違う [25]。

## 4. 統合アーキテクチャ（12）への反映点

- L0（入力・可用性）: 商用車では J1939 の AEBS・EBC5 の有無を車両ごとに確認し、可用性ベクトルに「PGN 受信有無・送信元」を加える。ACC1 の距離・速度は 8bit で粗い（16 §2.3）。
- L2/L3: 追突（R1 系）と健康起因（操作の途絶）を商用車の優先対象にできる【推察】。健康起因は CAN 上の無入力・無操舵の持続として現れるか要検証。
- L6: 事業用の目標・実績（令和6年）を効果指標の分母候補とする（原典確認後）。
- 12 の本文は変更しない。

## 5. 課題・ギャップ

1. AEBS1/AEBS2/VDC2 の PGN・SPN の一次確認（J1939DA または公開 DBC）。
2. 国内デジタコの判定閾値・取得信号は未確認。
3. 令和6年版の追突割合・ヒューマンエラー比率・予防安全の普及率は未取得。
4. 全件が抜粋のみ。I-01 の解消が前提。

## 6. 次のアクション提案

1. ネットワーク許可後、isobus.net・CSS Electronics の PGN 一覧で AEBS1/AEBS2/VDC2 を確定する（B-17）。
2. 厚労省0912-2d と国交省 001173873 を本文確認し、デジタコのイベント条件と CAN 接続方針を確定する。
3. 国交省の令和6年版傾向分析で追突・健康起因の割合を取得する。
4. 商用車の健康起因事故を CAN のみで検知できるかの文献調査を別テーマ化する。

## 7. 参考文献リスト（全て検索結果の抜粋のみ・本文未読）

1. isobus.net PGN 61441（EBC1）: https://www.isobus.net/isobus/pGNAndSPN/1966?type=PGN
2. isobus.net PGN 64964 / GM Upfitter UVM J1939 一覧（2024）: https://www.isobus.net/isobus/pGNAndSPN/14346?type=PGN 、 https://www.gmupfitter.com/wp-content/uploads/2024/05/UVM-J1939-Information-List.pdf
3. isobus.net PGN 65265（CCVS1）: https://www.isobus.net/isobus/pGNAndSPN/17157?type=PGN
4. Hatz H50 CAN Protokoll: https://dsp.hatz.com/images/docu-files/SPNFMI-CAN/H50_CAN-Protokoll.pdf ／ 4a. Prevost 技術文書: https://techpub.prevostcar.com/content/media/18722/view
5. SAE J1939DA 抜粋（Scribd 2015-08）／ SAE Mobilus: https://www.scribd.com/document/803127533/j1939da-Digital-Annex-of-Serial-Control-and-Communication-2015-08 、 https://saemobilus.sae.org/content/J1939DA_201510
6. CSS Electronics J1939 PGN List／DBC: https://csselectronics.com/pages/j1939-pgn-list 、 https://www.csselectronics.com/products/j1939-dbc-file
7. NMFTA Heavy Vehicle Networking Using SAE J1939（2026年掲載、内容未確認）: https://nmfta.org/wp-content/uploads/2026/04/Heavy-Vehicle-Networking-Using-SAE-J1939.pdf
8. Kvaser J1939 と DBC: https://kvaser.com/developer-blog/an-introduction-j1939-and-dbc-files/
9. 国交省 保安基準の細目告示 運行記録計（版は未特定）: https://www.mlit.go.jp/jidosha/content/S151.pdf
10. 厚労省 安全衛生資料（年不明）: https://www.mhlw.go.jp/new-info/kobetu/roudou/gyousei/anzen/dl/0912-2d.pdf
11. 国交省 FMS 検討資料: https://www.mlit.go.jp/common/001173873.pdf
12. 矢崎 YDX 報道（LOGISTICS TODAY）: https://www.logi-today.com/984747
13. デンソー報道（LOGISTICS TODAY）: https://www.logi-today.com/420/amp
14. LEVO 運行管理連携型デジタコ選定（令和8年7月1日）: https://www.levo.or.jp/wp-content/uploads/unkou20260701.pdf
15. Teltonika（FMS/ECU）: https://www.teltonika-gps.com/ja/blog/webinar-takeaways-truck-and-trailer-insights-directly-from-the-ecu
16. 国交省 事業用自動車総合安全プラン2025 目標・実績: https://www.mlit.go.jp/jidosha/content/001990603.pdf
17. 国交省 事業用自動車の事故統計（令和5年版）: https://www.mlit.go.jp/jidosha/jidosha_tk2_000059.html
18. 国交省 健康起因事故セミナー資料（2024）: https://www.mlit.go.jp/jidosha/anzen/03safety/resourse/data/seminar2024_2-2.pdf
19. 事業用自動車事故調査委員会 報告（個別報告かは未確認）: https://www.mlit.go.jp/report/press/content/001326946.pdf
20. 国交省 大型車 AEBS 強化（2023-01）: https://www.mlit.go.jp/report/press/content/001579807.pdf
21. 同 関連資料: https://www.mlit.go.jp/report/press/content/001579809.pdf
22. ベストカーWeb（R131-02 解説）: https://bestcarweb.jp/fullload/1628465/2
23. NHTSA 大型車 AEB 提案規則（2023）: https://www.nhtsa.gov/press-releases/heavy-vehicles-automatic-emergency-braking-proposed-rule
24. FMCSA LTCCS 分析ブリーフ: https://www.fmcsa.dot.gov/safety/research-and-analysis/large-truck-crash-causation-study-analysis-brief
25. FMCSA CMV Crash Data Overview（2024-12）: https://www.fmcsa.dot.gov/sites/fmcsa.dot.gov/files/2024-12/Commercial%20Motor%20Vehicle%20Crash%20Data%20Overview%20508.pdf
