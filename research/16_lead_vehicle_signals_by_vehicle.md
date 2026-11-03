# 16. 先行車情報（レーダ/ACC ターゲット）が CAN に出る車種の調査

- 調査日: 2026-11-03
- 論点: B-03。opendbc 等の公開 DBC から、先行車の距離・相対速度・PCS/AEB 段階・ACC 状態の信号が定義されている車種を整理し、OBD ポートから見えるか（ゲートウェイ）、J1939・CAN-FD の扱いも確認する
- 既存調査との関係: 03 §3.1（opendbc の概要）・§3.3（CAN に流れにくい信号の一般論）、11 §6.1（openpilot の構成）は扱い済みとして除外。本書は車種×信号の表と、OBD 可視性の公開情報に絞る
- ソース件数: 新規（本文確認）24件（[1]〜[23]・[30]）／新規（抜粋のみ）6件（[24]〜[29]）／既出の再掲 0件（`scripts/sources_index.py --check` で全件 NEW を確認）
- 確認方法の注記: 本文確認とは WebFetch で GitHub 上のファイルを取得して信号名を抽出したことを指す。WebFetch は内部で要約するため原文そのものではない。巨大ファイルは先頭約10万文字のみ（[5][8]）。単位・ビット位置・スケールは多くを未確認

## 1. エグゼクティブサマリー
- 先行車の距離・相対速度を物理量で持つ公開 DBC は、Toyota（TRACK_A）、GM（LRRObject）、Mazda（RADAR_TRACK）、Ford（Object_xx、MRR）、Hyundai/Kia CAN（SCC11・FCA11）、Honda Nidec（RADAR_HUD）にある（[1]〜[4][6]〜[9][11]）
- PCS/AEB 段階の信号は、VW MQB（ACC_10・ACC_15）、Hyundai（SCC12・FCA11）、Honda（AEB_STATUS 4段階）、GM（FrntVsn*）、Tesla（DI_aebState）にある（[4][5][9][11][12][13]）
- ECU が算出した TTC を持つ信号は、Hyundai FCA11 の FCA_TimetoCollision と VW ACC_10 の PCF_Time_to_collision（0〜2.5 s）の2つが確認できた（[5][9]）
- Tesla Model 3 の DBC には先行車の距離・相対速度の信号は見つからず、代わりに FCW・AEB・衝突警報の種別（CIPV・割込みなど）の段階フラグがある（[13]）
- OBD ポートで先行車情報が「見える／見えない」と車種別に明記した公開資料は見つからなかった。レーダ点列は多くの車種で専用バス（panda の bus1 など）に載る実装であり、OBD 直結で取れる保証はない（[14][15][18]）
- 商用車 J1939 では ACC1（PGN 65135）に前方車両距離（SPN 1587）・速度（SPN 1586）・前方衝突警報（SPN 5022）が定義されている（[21][25]）。AEBS の PGN/SPN は確認できなかった

## 2. 主要知見

### 2.1 車種×信号の表（事実）
凡例: 「—」は読めた範囲に無し。URL は §7 の番号に対応

| メーカー | DBC | 距離・相対速度 | PCS/AEB/FCW 段階 | ACC 状態 | 出典 |
|---|---|---|---|---|---|
| Toyota（DSU 系） | toyota_adas.dbc | TRACK_A_0〜15: LONG_DIST, LAT_DIST, REL_SPEED | — | STATUS_MSG の RADAR_STATUS のみ | [2] |
| Toyota（TSS2） | toyota_tss2_adas.dbc | TRACK_A_0〜15（BO_384〜399）: LONG_DIST, LAT_DIST, REL_SPEED | — | RADAR_STATUS | [1] |
| Toyota（TSS-P） | toyota_radar_dsu_tssp.dbc | OBJECT_0〜11、CLUSTER_*: LONG_DIST, LAT_DIST, SPEED（相対かは dbc に明記なし） | — | — | [3] |
| GM | gm_global_a_object.dbc | LRRObject01〜20: TrkRange, TrkRangeRate | F_Vision_Obj_Header_2: FrntVsnInPthVehBrkNwSt, FrntVsnInPthVehAlrtNwFlg ほか | ASCMAccSpeedStatus（ACC 状態そのものではない） | [4] |
| VW MQB | vw_mqb.dbc | 物理量なし（ACC_Abstandsindex は距離指数） | ACC_10: ANB_Zielbremsung_Freigabe, PCF_Time_to_collision。ACC_15: AWV_Warnlevel | ACC_06: ACC_Status_ACC | [5] |
| Mazda | mazda_radar.dbc | RADAR_TRACK_361〜366: DIST_OBJ, RELV_OBJ | — | — | [6] |
| Ford | ford_fusion_2018_adas.dbc / FORD_CADS.dbc | Object_00〜63: X_Rel, V_Rel（レーダ物体リストという解釈は【推察】）。MRR_Detection_xxx: RANGE, RANGE_RATE | 読めた範囲に無し | — | [7][8] |
| Hyundai/Kia（CAN） | hyundai_can.dbc | SCC11: ACC_ObjDist, ACC_ObjRelSpd | SCC12: AEB_Status, AEB_CmdAct。FCA11: FCA_Status, FCA_TimetoCollision | SCC11: MainMode_ACC ほか | [9] |
| Hyundai/Kia（CAN FD） | hyundai_canfd.dbc | CCNC_0x162: LEAD_DISTANCE（0.1 m）、LEAD_LATERAL。相対速度は見つからず。RADAR_0x251 は CHECKSUM/COUNTER のみ | FCA_*WrnSta, AEB_SETTING | SCC_CONTROL: ACCMode | [10] |
| Honda（Nidec） | _nidec_common.dbc | RADAR_HUD: LEAD_DISTANCE, LEAD_SPEED（先行車速度とみられる【推察】） | BRAKE_COMMAND: AEB_STATUS（4段階）, FCW | CRUISE_STATES ほか | [11] |
| Honda（Bosch） | _bosch_radar_acc.dbc | — | ACC_CONTROL: AEB_STATUS, AEB_BRAKING | ACC_ENABLED, ACC_FAULTED | [12] |
| Tesla Model 3 | tesla_model3_party.dbc | なし。レーダ生トラックは別定義（LongDist 0.0625 m、LongSpeed 0.0625 m/s）| DI_aebState, DAS_aebEvent, DAS_forwardCollisionWarning, DAS_longCollisionWarning（CIPV・割込み等の区別） | DAS_accState, DI_cruiseState | [13][22] |

### 2.2 OBD から見えるか（事実と【推察】を分ける）
- 事実: Toyota のレーダ点列は panda の bus1（TSS2 は 0x180〜0x19F）で解析される実装である［14］。Hyundai の Mando レーダは 0x500〜0x51F を bus1［15］、Chrysler は別 DBC のレーダバス［16］、Honda Nidec は別 radar バス、Bosch は CAN にレーダ点列を出さない扱い［17］
- 事実: Ford は GWM が CAN 間中継と OBD-II 診断バスを担い、レーダは IPMA との専用 CAN にある［18］。VW は多くの車でカメラではなくゲートウェイ（J533）の extended CAN に接続する［19］［20］
- 事実（抜粋のみ）: FCA の SGW は OBD-II と車内 CAN の間のファイアウォールで、2018年以降の車に搭載とされる（ベンダー情報）［24］。メーカーが OBD をゲートウェイで保護し、整備工場の登録が必要との説明がある［26］
- 事実（抜粋のみ）: sunnypilot の投稿では、レーダを無効化すると FCW/AEB も止まり、CAN FD 車は ADAS モジュールにデータが集まる［27］。Kia Carnival 2026 では ADAS ECU（0x730）が SCC_CONTROL（0x1A0）を ECAN に 50 Hz で出すとの記載がある［28］
- 【推察】先行車の距離・相対速度は ADAS 専用バスにあることが多く、OBD ポート直結での取得は車種ごとに実車確認が要る。Hyundai/Kia の CAN 車は SCC が bus0 にあるが、OBD の背後にゲートウェイがあるかは未検証である
- 【推察】車載機を組み込み型（ECU 内蔵・TCU）にするか、ADAS バスへ割り込むハーネス型にするかを、車種ごとに選ぶ必要がある（11 §3 の配置と対応）

### 2.3 J1939 と CAN-FD
- J1939 ACC1: PGN 65135（0xFE6F）、周期 100 ms。SpeedOfForwardVehicle（SPN 1586、1 km/h、0〜250）、DistanceToForwardVehicle（SPN 1587、1 m、0〜250）、ForwardCollisionWarning（SPN 5022）などがある［21］。PGN 65135 の名称と SPN 1586/1587 の紐づけは別の DB の抜粋でも一致した［25］
- 同 DBC に AEBS という名のメッセージはなかった［21］。AEBS1/AEBS2 の PGN・SPN は確認できなかった
- 事実: opendbc 内に J1939 の ACC1 定義は見つからなかった（サブエージェントの grep による）
- FMS 標準は J1939 ベースの車隊管理向け PGN 表だが、ACC1 を含むかは未確認［29］
- CAN FD: Hyundai/Kia は CCNC_0x161/0x162 に先行車距離・横位置・左右隣接車線の車両がある［10］。メッセージ名はコミュニティによる推定名で公式仕様ではない
- 【推察】J1939 の距離・速度は各 8 bit（分解能 1 m/1 km/h、250 上限）で、乗用車のレーダ信号より粗い

### 2.4 その他
- Toyota TSS-P では DSU が縦、カメラが横を担当し、配線上の経路が複数ある［30］。【推察】OBD で全信号が見える保証はない
- openpilot の対応表では、車種ごとに harness box とコネクタが並び、OBD-C ケーブルは電源・panda 接続用とみられる【推察】［23］

## 3. 統合アーキテクチャ（12）への反映点
- L0（取得・正規化）: 先行車信号の有無を「車種×信号」の能力表（本書 §2.1）として持ち、信号が無い車種（VW の距離、Tesla の距離・速度）は ECU の TTC や段階フラグで代替する経路を設ける【推察】
- L2（LEAD・ADS）: LEAD 入力を3種に分ける提案【推察】: (a) 物理量あり（Toyota・GM・Mazda・Ford・Hyundai・Honda Nidec）、(b) ECU 算出 TTC のみ（VW・Hyundai FCA11）、(c) 段階フラグのみ（Tesla・Honda Bosch）
- L3（R1）: TTC/THW を自前計算できるのは (a) のみ。(b)(c) では ECU の警報段階を R1 の入力にする
- 取得経路: OBD 非可視の車種が多い可能性があるため、12 の「後付け」構成では ADAS バスへの割り込み（ハーネス）か OEM 連携を前提とする必要がある【推察】

## 4. 課題・ギャップ
1. OBD ポートでの可視性を車種別に明記した一次資料は見つからなかった。実機ログでの検証が必要
2. Honda・Hyundai の車種別完成版 DBC、mazda_2017/mazda_3_2019、vw_mqbevo/mlb/pq、ford_lincoln_base_pt（BO_/SG_）は未読
3. 単位・スケール・ビット位置を確認していない。Toyota の LONG_DIST 無効値などは radar_interface.py の記述のみ
4. J1939 の AEBS1/AEBS2 の番号は未確認（J1939-71／J1939DA は有償）
5. 日本語の一次資料は 0 件（国内メーカーの OBD 開放方針、国交省の関連文書は未調査）
6. WebFetch 不可ホスト（csselectronics.com、blog.comma.ai、wikipedia、isobus.net、youcanic など）は抜粋のみ（ISSUES I-01）

## 5. 次のアクション提案
1. ネットワーク許可後に J1939DA 派生の公開 DB で AEBS1/AEBS2 の PGN・SPN を確認する
2. 実車（Hyundai/Kia・Toyota）で OBD ポートと ADAS バスの両方を記録し、先行車信号の可視性を確認する
3. 日本語資料（日野・いすゞ・三菱ふそう・UD の予防安全、国交省の AEBS 基準）を調べる（B-05 と併せる）
4. 未読の DBC（Honda 車種別、hyundai_canfd 完成版、VW MQB 後半）を読み、表を完成させる
5. 12 の L2 に LEAD 入力の3区分を反映するか判断する

## 6. 事実と推察の区別
本書の「示唆」「提案」は【推察】を付けた箇所を除き、ソースの記載である。

## 7. 参考文献（URL付き）
本文確認（opendbc 基点は上記 URL に含まれる。[30] も本文確認）
1. toyota_tss2_adas.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/toyota_tss2_adas.dbc
2. toyota_adas.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/toyota_adas.dbc
3. toyota_radar_dsu_tssp.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/toyota_radar_dsu_tssp.dbc
4. gm_global_a_object.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/gm_global_a_object.dbc
5. vw_mqb.dbc（先頭約10万/12.7万文字） — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/vw_mqb.dbc
6. mazda_radar.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/mazda_radar.dbc
7. ford_fusion_2018_adas.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/ford_fusion_2018_adas.dbc
8. FORD_CADS.dbc（先頭約10万/21.6万文字） — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/FORD_CADS.dbc
9. hyundai_can.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/generator/hyundai/hyundai_can.dbc
10. hyundai_canfd.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/generator/hyundai/hyundai_canfd.dbc
11. honda _nidec_common.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/generator/honda/_nidec_common.dbc
12. honda _bosch_radar_acc.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/generator/honda/_bosch_radar_acc.dbc
13. tesla_model3_party.dbc — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/tesla_model3_party.dbc
14. toyota radar_interface.py — https://github.com/commaai/opendbc/blob/master/opendbc/car/toyota/radar_interface.py
15. hyundai radar_interface.py — https://github.com/commaai/opendbc/blob/master/opendbc/car/hyundai/radar_interface.py
16. chrysler radar_interface.py — https://github.com/commaai/opendbc/blob/master/opendbc/car/chrysler/radar_interface.py
17. honda radar_interface.py — https://github.com/commaai/opendbc/blob/master/opendbc/car/honda/radar_interface.py
18. openpilot wiki: Ford — https://github.com/commaai/openpilot/wiki/Ford
19. openpilot wiki: Volkswagen — https://github.com/commaai/openpilot/wiki/Volkswagen
20. openpilot wiki: VW J533 (Gateway) Cable — https://github.com/commaai/openpilot/wiki/VW-J533-%28Gateway%29-Cable
21. j1939.dbc（Konik-ai、出自・J1939DA 版は不明） — https://github.com/Konik-ai/j1939_dbc/blob/main/dbc/j1939.dbc
22. tesla _radar_common.py — https://github.com/commaai/opendbc/blob/master/opendbc/dbc/generator/tesla/_radar_common.py
23. openpilot docs/CARS.md（先頭約10万/16.6万文字） — https://raw.githubusercontent.com/commaai/openpilot/master/docs/CARS.md

抜粋のみ
24. YouCanIC「FCA Secure (Firewall) Gateway Module Explained」 — https://www.youcanic.com/fca-sgm/
25. isobus.net PGN 65135 / SPN — https://www.isobus.net/isobus/pGNAndSPN/14677?type=PGN
26. MAHLE Workshop Heroes「cyber security pass」 — https://workshop-heroes.mahle.com/en/article/cyber-security-pass
27. sunnypilot ESCC — https://community.sunnypilot.ai/t/3743
28. sunnypilot Kia Carnival 2026 — https://community.sunnypilot.ai/t/-/4831/1
29. FMS-Standard 仕様書 v02.00（2010） — https://www.thierry-lequeu.fr/data/fms_document_ver02.00vers_11_11_2010.pdf
30. toyota-dsu-reroute-harness（本文確認） — https://github.com/cydia2020/toyota-dsu-reroute-harness
