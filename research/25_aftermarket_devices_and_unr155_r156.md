# 25 後付け機器（受信専用CAN機器）と UN R155/R156・ISO/SAE 21434・OBDアクセス規制

- 調査日: 2026-11-12
- 論点: B-12。受信専用の後付けCAN機器が UN R155/R156・ISO/SAE 21434・各国の型式認証／保安基準・OBDポートアクセス規制でどう扱われるか
- 既存調査との関係: 11 §5.2・§5.3（R155=CSMS、R156=SUMS/RXSWIN の概要、EU 2025/5）は扱い済みとして除外した。本稿は「後付け機器の扱い」「OBDアクセス規制（SERMI・SGW・UDS・DoIP）」「日本の保安基準・OBD検査」だけを扱う
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）26項目／既出の再掲 2件（EU 2025/5 と repairerdrivennews 2020、いずれも11に既出）。項目は複数URLを含むものがある。unece.org・eur-lex.europa.eu・www.mlit.go.jp 等が WebFetch で名前解決に失敗した（ISSUES I-01 継続）ため、本文は1件も読めていない。条項番号は検索抜粋に現れたものだけを記す

## 2. エグゼクティブサマリー

- R155 の適用範囲（para.1）は「ECU を1つ以上搭載した L・M・N・O 類車両」とされる（EU 2025/5 の抜粋）。規制の単位は車両型式であり、受信専用の後付けCAN機器を名指しで扱う条項・公式解釈は今回見つからなかった。
- 後付け機器を R155 で「部品／分離技術単位として承認する」構想は UNECE の概念文書にあるが、確定規則ではなく初期構想と明記されている（globalautoregs 抜粋）。現行の義務とは言えない。
- 日本の保安基準も車両単位のサイバーセキュリティ要件（別添120）で、後付け装置の扱いを述べた通達は見つからなかった。OBD検査（2024年10月開始）は車検時の故障コード照会であり、後付け機器の規制ではない。
- OBDアクセス規制（EU 2018/858 Chapter XIV、SERMI、FCA SGW）は、整備事業者の診断ツール認可が主眼である。受信専用ドングルがこの枠でどう扱われるかを述べた資料は未発見である。
- 【推察】受信専用機器の実務上の論点は、型式認証より「車両側の防御（SGW 等）に遮断される可能性」「機器自体が攻撃経路になる脆弱性」「送信できない設計の担保」にある。

## 3. 主要知見

### 3.1 R155/R156・ISO/SAE 21434 の適用範囲と後付け機器（全て抜粋のみ）

1. Regulation (EU) 2025/5（UN R155 の EU 版）— EU、2025、法令。URL: https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng（既出）。事実: para.1 は「ECU を1つ以上搭載した L・M・N・O 類車両」を対象とする（検索要約による。逐語は未確認）。示唆: 【推察】後付け機器を載せた車両は R155 の対象車両のままである。機器単体の扱いは別問題。
2. UK VCA「Cyber Security and Software Updating」— 英国型式承認機関、年不明、ガイダンス。URL: https://www.vehicle-certification-agency.gov.uk/connected-and-automated-vehicles/cyber-security-and-software-updating/。事実: メーカーにサプライチェーンのリスク特定とサプライヤーへの要求展開が求められる。条項番号は抜粋になし。示唆: 【推察】OEM に納入する形の後付け・組込み機器は、OEM のサプライチェーン管理経由で要求が下りてくる可能性がある。
3. GlobalAutoRegs 「R155 Interpretation Document 改正」議題ページ — UNECE 文書の第三者索引、二次情報。URL: https://globalautoregs.com/agendas/11471。事実: 2020年に日本が提出した aftermarket 関連コメント（TFCS-17-29）に言及がある。R155 para.7.3 のリスクアセスメントが aftermarket を扱うとされるが、要約は途中で切れている。示唆: 【推察】aftermarket は議論されたが、受信専用機器の適用除外が明文化されたかは不明。
4. GlobalAutoRegs 概念文書（devices as components / separate technical units）— UNECE 関連、年不明。URL: https://globalautoregs.com/documents/42898、https://globalautoregs.com/documents/42949。事実: 機器を R155 に沿って部品または分離技術単位として承認し、R155 承認済み車両へ装着する構想が「初期コンセプト」として記載されている。示唆: 【推察】後付け機器が任意で認証を受ける道筋になり得るが、現行の義務ではない。
5. SIP-adus ワークショップ資料（川名氏、2020・2021）— 内閣府 SIP、資料。URL: https://www.sip-adus.go.jp/evt/workshop2020/file/cs/10CS_04J_Kawana.pdf。事実: 検索要約によれば、R155 の 7.3.5（アフターマーケットのソフトウェア・サービス・アプリ・データの実行）を引用している。年次版のどちらかは未確認。示唆: 【推察】R155 は後付け「ソフトウェア・サービス」への対処を OEM 側に求める構造で、機器の規制ではなく OEM 側の脅威評価の問題として現れる。
6. SAE Mobilus「ISO/SAE 21434」— SAE/ISO、2021、標準カタログ。URL: https://saemobilus.sae.org/standards/isosae21434-road-vehicles-cybersecurity-engineering。事実: 道路車両の E/E システムのサイバーセキュリティ工程要求を定める。特定技術は規定しない。aftermarket への言及は抜粋になし。示唆: 【推察】21434 は R155 の法定要件ではなく、CSMS を実装する工程標準の位置づけ。R155 との関係を述べた公式文書は今回未確認。
7. Automotive IQ「Annex 5 was written for a car, your fleet isn't one」— 業界記事、年不明。URL: https://www.automotive-iq.com/cybersecurity/articles/annex-5-was-written-for-a-car-your-fleet-isnt-one。事実: フリートが第三者ドングルを診断ポートに挿す点を指摘し、附属書5 の緩和策として M9（特権アクセスの防止・検知）、M18（最小権限）が診断アクセスに関連づけられている（二次情報）。示唆: 脅威番号（OBD 経由）は原文未確認。【推察】車両側は OBD 接続機器を脅威として評価している。

### 3.2 OBDポート・診断IFのアクセス規制（全て抜粋のみ）

8. Regulation (EU) 2018/858 Chapter XIV（legislation.gov.uk の再掲）— EU、2018。URL: https://www.legislation.gov.uk/eur/2018/858/article/65?view=plain。事実: Art.65 は独立事業者がメーカーの違反を申し立てた際の承認機関による監査、Art.66 は車両情報アクセスフォーラム、Annex X は標準化アクセスを規定する。示唆: 【推察】独立整備事業者への情報提供義務であり、受信専用の後付けテレマティクス機器を直接対象とする条項は確認できない。
9. Delegated Regulation (EU) 2021/1244 — 欧州委員会、2021-05-20。URL: https://eur-lex.europa.eu/eli/reg_del/2021/1244/oj。事実: セキュリティ機能にアクセスする独立事業者の承認手続を Annex X Appendix 3 に追加し、信頼センター経由で電子証明書の有効性を確認する（要約）。示唆: 【推察】SERMI は整備ツールの認可スキームで、読み取り専用の常時接続ドングルは対象外と考えられる（条文未確認）。
10. Delegated Regulation (EU) 2026/699 — 欧州委員会、2026-03-23。URL: https://eur-lex.europa.eu/eli/reg_del/2026/699/oj/eng。事実: Annex X を再改正し、セキュアアクセスの要件・手続を定める。前文の抜粋のみ。示唆: 最新規定のため本文確認が必須。
11. IGARR「EU updates on access to vehicle OBD requirements」— 法律事務所系解説、2025-11-07。URL: https://igarr.com/2025/11/07/eu-updates-on-access-to-vehicle-on-board-diagnostics-obd-requirements/。事実: 委任規則 2022/1398 が UN R155 を参照し、一般安全規則 2019/2144 がサイバー脅威からの保護を求める（要約）。示唆: 二次情報。条項番号は未確認。
12. Hella Gutmann「What is SERMI?」— ベンダー解説、年不明。URL: https://www.hella-gutmann.com/en/sermi。事実: SERMI は盗難・セキュリティ関連情報へのアクセスを認証するスキームで、証明書の有効性はメーカーと SERMI 信頼センター間で確認する。示唆: 一次情報（SERMI 公式）は未発見。
13. FCA Secure Gateway 解説 — Repairer Driven News 2023、FenderBender、YouCanIC。URL: https://www.repairerdrivennews.com/2023/10/09/fca-gateway-unlock-now-available-on-7111-tablet/、https://www.fenderbender.com/running-a-shop/operations/article/33029713/making-sense-of-chryslers-secure-gateway-module、https://www.youcanic.com/fca-security-gateway/（2020年記事は11に既出）。事実: 2018年以降の Chrysler/Dodge/Jeep/RAM に搭載され、OEM または登録済み機器以外の診断要求を暗号で遮断する。示唆: 【推察】パッシブ受信のみのドングルが SGW 搭載車で動くかは資料に記載がなく未確認。
14. ISO 14229-1（UDS）二次解説 — 年不明。URL: https://en.wikipedia.org/wiki/Unified_Diagnostic_Services、https://pyudskit.readthedocs.io/en/latest/concepts/security-access/。事実: 0x27 はシード・キー認証、0x29 は証明書ベース認証（2020年版で追加とされる）。示唆: 【推察】受信専用機器が診断要求を一切送らない設計なら UDS 認証の対象外にできるが、送信しないことの担保は規格に書かれていない。
15. ISO 13400（DoIP）— ISO、規格。URL: https://www.iso.org/standard/57317.html、https://docs.autopi.io/developer_guides/setting-up-doip/。事実: 13400-4 は ISO 15031-3 準拠のコネクタ仕様で、イーサネット有効化はピン8のアクティベーション線が一般的（ベンダー資料）。示唆: 【推察】CAN のみ受信する機器が DoIP 線を使わなければ DoIP 経路には関与しない。
16. NHTSA「Cybersecurity Best Practices for the Safety of Modern Vehicles」— NHTSA、2016（DOT HS 812 333）、2022 pre-final。URL: https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/documents/812333_cybersecurityformodernvehicles.pdf、https://www.hunton.com/privacy-and-cybersecurity-law-blog/nhtsa-releases-new-automobile-cybersecurity-best-practices。事実: 2016版にアフターマーケット機器の節があり、メーカーは機器が安全に影響しうることを考慮すべきとする。2022版に「Aftermarket/User Owned Devices」「Diagnostic Tools」の節がある（抜粋）。示唆: 非拘束ガイダンス。節番号は未確認。
17. ScanNetSecurity（JVN 関連報道）2015・2016。URL: https://scan.netsecurity.ne.jp/article/2015/08/14/37098.html、https://scan.netsecurity.ne.jp/article/2016/04/11/38352.html。事実: 保険用 OBD2 ドングルや別の OBD2 デバイスに、Bluetooth 認証不備や CAN へのコマンド送信可能な脆弱性が報告された。示唆: 【推察】後付け機器自体が攻撃経路になり得る。CAN TX の物理的遮断が「受信専用」の担保として有効と考えられる。
18. Bundestag ロビー登録簿の意見書（メーカー側の立場表明）— 2026年頃。URL: https://www.lobbyregister.bundestag.de/media/af/3b/691967/Stellungnahme-Gutachten-SG2602090015.pdf。事実: OBD ポート経由の権限のない者による悪用を防ぐため、規則 2018/858 に基づく委任法で OBD ポート要件を定めるよう求めている。示唆: 意見書の主張で規制の現状ではない。【推察】OBD 経由の入力が将来制限される可能性はリスクとして残る。
19. Auto Rental News「Will cybersecurity concerns limit OBDII access」— 業界記事、年不明。URL: https://www.autorentalnews.com/157211/will-cybersecurity-concerns-limit-obdii-access。事実: OBDII は当初セキュリティを念頭に設計されておらず、ポートアクセスが制限される可能性があるとの記載。示唆: 12 のデプロイ前提に対するリスク。

### 3.3 日本（保安基準・OBD検査）（全て抜粋のみ）

20. 国交省 サイバーセキュリティ関連資料（別添120）— 2020年11月、PDF。URL: https://www.mlit.go.jp/jidosha/content/001844079.pdf。事実: 適用範囲は二輪・三輪・特殊自動車等を除く自動車。技術基準は細目告示の別添120。後付け装置への言及は抜粋になし。示唆: 【推察】日本の基準も車両単位。
21. 国交省 報道発表（サイバーセキュリティ・SU の取込み、2020年12月）。URL: https://www.mlit.go.jp/report/press/jidosha10_hh_000242.html。事実: 自動運行装置・サイバーセキュリティ・ソフトウェア更新の基準を保安基準に取り込む。無線更新対応車は新型車2022年7月、継続生産車2024年7月から適用（要約。どの記載がこのページ由来かは未特定）。
22. 国交省 二輪・三輪への R155 適用拡大 — 第17条の2関係。URL: https://www.mlit.go.jp/jidosha/content/001867805.pdf。事実: 新型車は2029年7月1日、継続生産車は2031年7月1日から適用（要約。該当 PDF は未確定）。示唆: 条が保安基準か細目告示かは未確認。
23. 国交省 別添124「継続検査等に用いる車載式故障診断装置の技術基準」。URL: https://www.mlit.go.jp/jidosha/content/B124.pdf。事実: 故障コード規格・接続端子・通信プロトコルを規定（要約）。示唆: 検査用スキャンツールの規定で、後付け機器の安全性は扱わない。
24. 国交省 OBD検査 審査事務規程 S04 ほか。URL: https://www.mlit.go.jp/jidosha/content/OBDkensa-regulations_S04.pdf、https://www.mlit.go.jp/jidosha/OBD_Inspection_System.html（存在のみ確認）。事実: 令和8年9月1日以降に指定を受けた型式指定車に、車線逸脱警報装置・側方衝突警報装置などの故障情報が順次追加されるとの記載（要約。該当 PDF は未確定）。示唆: 【推察】ADAS 系の DTC が OBD 検査の対象に拡大する流れ。本プロジェクトの入力側（L0）とは接点があるが、受信専用機器の規制ではない。
25. くるまのニュース「OBD検査」— 2024、解説記事。URL: https://kuruma-news.jp/post/825582。事実: 国産車は2024年10月1日に正式運用、輸入車は2025年10月から（要約。一次資料ではない）。
26. BSR「JOURNAL」— 業界ニュース。URL: https://bsrweb.jp/article/792297。事実: 道路運送車両法第94条の5が適合証への虚偽記載を禁じるとの説明。示唆: 後付け機器とは別の論点。
27. SIP-adus「rd06/224.pdf」— 資料。URL: https://www.sip-adus.go.jp/rd/rddata/rd06/224.pdf。事実: UN-R155/R156 の合意に伴いサイバー攻撃対策が必要とされる（要約）。

## 4. 統合アーキテクチャ（12）への反映点

- L0（入力）・デプロイ: 受信専用の担保を設計要件に加える。CAN TX のハードウェア遮断（トランシーバの送信無効化、診断要求を出さない）と、その旨の脅威分析書を後付け形態（11 方式 D〜F）の標準成果物とする【推察】。
- L0: OBD 経由の入力が SGW・将来規制で遮断される可能性を、入力健全性（L1）の「入力喪失」ケースに明記する【推察】。
- デプロイ（11 §5.3 への追記候補）: OEM 組込み形態は OEM の CSMS・サプライチェーン管理経由、後付けは R155 の対象外だが車両側の脅威評価の対象、と整理する【推察】。

## 5. 課題・ギャップ

- 受信専用の後付け機器を直接扱う条項・公式解釈は見つからなかった。R155 para.7.3・7.3.5、TFCS-17-29、GRVA-25-32 は原文未確認。
- R156 の適用範囲、21434 と R155 の関係、附属書5 の OBD 経由脅威の項番は未確認。
- 日本の細目告示・通達番号、後付け装置の保安基準上の扱い（改造・構造変更）は未確認。
- 全ソースが抜粋のみ（I-01）。unece.org・eur-lex.europa.eu・www.mlit.go.jp 等の許可が前提。

## 6. 次のアクション提案

1. I-01 解消後、R155 本文（para.1・2・7.3・7.3.5）、Interpretation Document、TFCS-17-29 を原文で確認する。
2. 別添120・別添124・OBD検査審査事務規程の PDF を本文で確認し、後付け機器の記載の有無を確定する。
3. SGW 搭載車でのパッシブ受信ドングルの動作を、メーカー技術文書または実測で確認する（B-18 と連携）。
4. 規則 2018/858 Art.61・Annex X、2026/699 の最終条文を確認する。

## 7. 参考文献リスト

3.1〜3.3 の各項に記載した URL（EU 2025/5 と repairerdrivennews 2020 は11に既出。他は検索結果で実在を確認、本文は未読）。
