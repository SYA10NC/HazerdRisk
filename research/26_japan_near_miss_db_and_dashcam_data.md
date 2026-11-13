# 26 日本のヒヤリハットDB・ドラレコ事故データの入手条件と研究利用事例

- 調査日: 2026-11-13
- 論点: B-13。国内のヒヤリハットDB・ドラレコ・事故データについて、入手条件、ライセンス、収録信号（CAN相当があるか）、研究利用事例を整理する。
- 既存調査との関係: 03 §5-8（DBの存在のみ確認、公開は未確認）を前提とし、その先（入手条件・信号・利用事例）だけを扱う。17 に載る国交省 dora-houkoku2.pdf は既出（1件、再掲）。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）35件／既出の再掲 1件（S25）。WebFetch が使えず（ISSUES I-01。今回は web.tuat.ac.jp、itarda.or.jp、npa.go.jp、jstage 等も名前解決不可）、全ソースが WebSearch の抜粋のみで、本文は未読である。

## 1. エグゼクティブサマリー

1. 公開ダウンロードできる日本のヒヤリハット／ドラレコDBは、抜粋の範囲では確認できなかった。入手は共同研究・会員制研究会・審査付き提供のいずれかに見える。
2. 東京農工大SMRCのDBは、22万件超（現行About）の規模で、会員制の研究会が運営を支える。申請様式・ライセンス・料金は見つからなかった。
3. 収録信号は車速（パルス由来で低分解能）・ブレーキ・加速度・ウインカー・GPSが中心である。アクセル開度・操舵角は、確認した抜粋に出てこなかった。ADAS状態フラグやレーダ距離も未確認。
4. 1件はトリガ前10秒・後5秒の短い区間で、連続走行ログではない。検出は加速度トリガ式であり、約70%が段差等による誤検出との記述がある（抜粋）。再ラベリングが前提になる。
5. ITARDAのミクロデータは内部分析用が原則で、外部提供は審査会と警察庁承認を経る仕組みである。EDR由来の車速・ヨーレートを含むが低レートである。
6. 保険会社は自社データを自社サービスやメーカー共創に使う（東京海上日動×マツダ 2026年3月）。外部研究者に開かれた経路は見つからなかった。
7. 【推察】CANのみ推論モデルの学習データとしては、信号の粗さと誤検出率から「ラベル生成・評価用の補助」にとどまる。本線は共同研究での入手交渉になる。

## 2. 主要知見

### 2.1 東京農工大 スマートモビリティ研究拠点（SMRC）
全て抜粋のみ。

- [S1] SMRC "What is the Near-Miss Database?"（東京農工大SMRC、現行ページ、公式）https://web.tuat.ac.jp/~smrc/en/about.html — 事実: 220,000件超のヒヤリハットデータと165,000件超の2カメラデータ、タクシー200台超、収集拠点8か所。2010年にJSAEから東京農工大へ管理が移管。自動車会社等の会員制研究会が運営を支え、利用・共同研究の問い合わせを受け付ける。示唆: 【推察】入手は問い合わせ・共同研究・会員参加で、有償や守秘契約の可能性がある。
- [S2] SMRCトップ（英） https://web.tuat.ac.jp/~smrc/en/index.html — 入口ページ。要点は得られず。
- [S3] SMRC Drive Recorder Data Center（旧サイト） https://web.tuat.ac.jp/~smrc/oldSMRC/drcenter_eng.html — 2005年から取得、評価タグ付きで約15万件（旧記載）。用途は能動安全・自動運転の設計評価など。件数は資料の年で異なる（約8.9万→15万→22万）。
- [S4] FOT-NET Tokyo Workshop 2013 発表（Raksincharoensak ら、東京農工大）https://fot-net.eu/download/international_workshops/tokyo/rt3_20131014_fotnet_pr_tuat_raksincharoensak.pdf ／ https://web.tuat.ac.jp/~smrc/oldSMRC/pdf/Driverecorder.pdf — 2カメラ研究会は2012年7月発足、大学2校＋企業7社。会員がデータ維持費・更新費を負担する方式。抜粋では記録信号は車速・ブレーキ信号・前後左右加速度・映像・GPS。
- [S5] 長井研「ヒヤリハット収録型ドライブレコーダ」 https://web.tuat.ac.jp/~nagaimu/kenkyu_its1.html（既出の関連ページあり）— ASV評価等への活用を述べる。
- [S6] 赤松ら「ドライブレコーダ加速度を用いた高分解能車速推定」（2011、交通・物流部門大会）https://www.jstage.jst.go.jp/article/jsmetld/2011.20/0/2011.20_19/_article/-char/ja — DBの速度は分解能が低く、加速度から最小二乗法とカルマンフィルタで推定する、と抜粋にある。示唆: CAN由来の速度とは同等に扱えない。
- [S7] 交通・物流部門大会 2022 TL4-2 https://www.jstage.jst.go.jp/article/jsmetld/2022.31/0/2022.31_TL4-2/_article/-char/en — 抜粋に「約70%が段差等による減速の誤検出」とあるが、この論文の記述か未確認。
- [S8] Akikawa ら PerCom Workshops 2020 https://staff.itee.uq.edu.au/jaga/proceedings/percomworkshops2020/papers/p518-akikawa.pdf — 同様に約70%が誤検出との抜粋。
- [S9] JTEKT Engineering Journal（2010前後）https://www.jtekt.co.jp/engineering-journal/assets/1001/1001_08.pdf ／ 英 https://www.jtekt.co.jp/e/engineering-journal/assets/1001/1001e_08.pdf — 合成加速度が閾値を超えた時点で15秒（前10秒・後5秒）の映像と車両データを記録。
- [S10] Car Watch「ヒヤリハットデータベース活用委員会」https://car.watch.impress.co.jp/docs/news/080336.html — 2006年活動開始、2008年度末で約3.3万件。
- [S11] SIP-adus 市民ダイアログ2018資料 https://www.sip-adus.go.jp/file/citizens2018/citizens2018_05.pdf — DBの高・中・低リスクシーンでリスク予測の知識モデルを紹介（研究利用例）。
- [S12] 科研費 26350455 成果報告書 https://kaken.nii.ac.jp/file/KAKENHI-PROJECT-26350455/26350455seika.pdf — 東京・静岡・福岡・札幌のデータを登録との記載（抜粋）。
- [S13] Yamamoto ら（NTT）"Identifying Near-Miss Traffic Incidents in Event Recorder Data"（2020）https://link.springer.com/chapter/10.1007/978-3-030-47436-2_54 — 車両状態時系列＋YOLO特徴。TUATのDBかは未確認。
- [S14] J. Applied Statistics 2021 無信号交差点のヒヤリハット統計モデル https://www.tandfonline.com/doi/abs/10.1080/02664763.2021.1962263 — 32,354件中1,090件の車対車（抜粋）。DB名は未確認。

### 2.2 公的機関（ITARDA・国交省・NILIM・警察庁・産総研）
全て抜粋のみ。

- [S15] ITARDA 交通事故集計ツール https://www.itarda.or.jp/tool — 事故ごとに60〜80項目のコード化データ。登録会員が集計ツールを使える（会員区分で範囲が異なる）。CAN相当信号なし。
- [S16] ITARDA 会員規約（2018年付と記載）https://www.itarda.or.jp/members/agree — 論文利用は出典明示が条件、営利の資料集化・受託業務・第三者利用は禁止。
- [S17] ITARDA FAQ https://www.itarda.or.jp/outline/faq — 受託集計は有償。第三者・他者委託への利用は原則断る。
- [S18] ITARDA 事業計画・報告（令和2・3・6年度）https://www.itarda.or.jp/assets/outline/disclosure/2020keikaku-4a007a6e2a769e315b67b707431badd9d86a5c2fb3e19d7d7a8a02d19bb4eb64.pdf ほか — ミクロデータは内部分析目的。外部提供は保全措置が適正な場合に限り、警察庁承認と審査会の仕組み。客員研究員制度の記載あり。
- [S19] ITARDA Pre-Crash-Matrix（JSAE 2021）https://tech.jsae.or.jp/paperinfo/ja/content/conf2021-02.14/ — 衝突前5秒の車両挙動を再構成し SAKURA のシナリオ検証に使用。
- [S20] ITARDA EDR軌跡推定（SAE 2022-01-0837）https://tech.jsae.or.jp/paperinfo/ja/content/sae2022-01.720/ — EDRの車速とヨーレートを積分。急変時はサンプリング周波数が低く再現できない。
- [S21] EDR特性・J-NCAP（SAE 2011-01-0810）https://saemobilus.sae.org/content/2011-01-0810 — 衝突前速度の誤差は4%未満、制動中は精度低下（抜粋）。
- [S22] 警察庁 交通事故統計ページ https://www.npa.go.jp/publications/statistics/index.html — オープンデータ（CSV）の掲載あり。項目一覧・規約は未確認。車両時系列信号は含まないと【推察】。
- [S23] 国交省 ドラレコ調査 平成17年度 https://www.mlit.go.jp/jidosha/anzen/03driverec/resourse/data/dora-houkoku17.pdf — 試作機200台、市販機1,620台。報告書は公開、生データ公開は未確認。
- [S24] 国交省 収集項目・DB化検討 https://www.mlit.go.jp/common/000140127.pdf — 標準的な収集項目は映像、3軸加速度、速度、ブレーキ、方向指示、時刻、緯度経度（抜粋）。
- [S25] 国交省 dora-houkoku2.pdf（既出: 17）https://www.mlit.go.jp/jidosha/anzen/03driverec/resourse/data/dora-houkoku2.pdf — タクシー仕様でブレーキ・ウインカー・車速パルスを受けて記録、データ判別ソフトを公開（抜粋）。再掲。
- [S26] ESV資料 Accidents and Near-Misses Analysis by Using VD-Rs in a Fleet Test https://www.nhtsa.gov/sites/nhtsa.gov/files/accidents_and_near-misses_analysis_by_using_vd-rs_in_fleet_test.pdf — ニアミスのトリガは前後加速度±8 m/s² またはヨーレート±35 deg/s（抜粋）。日本の試験かは未確認。
- [S27] NILIM 年報2010 https://www.nilim.go.jp/english/annual/annual2010/27.pdf — 簡易抽出アルゴリズムの抽出率80%超（抜粋）。事業者協力が必要。
- [S28] 産総研 Kataoka ら（ICRA 2018）https://arxiv.org/pdf/1804.02555 — タクシー100台超・約10年のDBは著作権上、非公開と抜粋にある。
- [S29] 名古屋大／愛知県資料（タクシー会社提供データ）https://www.pref.aichi.jp/uploaded/attachment/483546.pdf — 事業者提供の共同研究型。

### 2.3 保険会社・事業者
全て抜粋のみ。

- [S30] 損保ジャパン・第一交通産業・アクセンチュア共同研究（2017）https://it.impress.co.jp/articles/-/22525 — ドラレコ画像・運転挙動・生体情報・車両情報。第一弾は100台分。生体情報の比重が大きい。
- [S31] 損保ジャパン×理研AIP（2019）https://eetimes.itmedia.co.jp/ee/articles/1911/18/news036.html — 走行データの機械学習解析。信号種別は不明。
- [S32] 損保ジャパン 事故リスク予測AI（2021）https://www.watch.impress.co.jp/docs/news/1285743.html — ドラレコの位置・速度・加速度から事故リスクを予測し、運転診断として提供。【推察】CANなしの低次元信号の比較ベースライン。
- [S33] 東京海上日動×マツダ（2026年3月）https://newsroom.mazda.com/ja/publicity/release/2026/202603/260323a.pdf — 事故前の車両挙動・ドライバー操作・視線・周辺情報をマツダのADAS研究開発に提供。同意取得と匿名化が条件で、提供先は共創関係のメーカー。
- [S34] あいおいニッセイ同和損保×東京農工大 包括連携（2023）https://www.aioinissaydowa.co.jp/corporate/about/news/pdf/2023/news_2023032301136.pdf — ヒヤリハットデータ分析を含む共同研究。
- [S35] あいおいニッセイ同和損保×群馬大（2026年3月）https://hospital.med.gunma-u.ac.jp/1_web/wp-content/uploads/2026/03/press_R080326.pdf — 運転挙動と健康の実証。事故予兆とは遠い。
- [S36] Nauto 日本展開 https://nauto.com/blog/improving-commercial-fleet-safety-in-japan — 2018年に日本の商用フリートへ展開（抜粋）。公開研究データは見つからず。

## 3. 統合アーキテクチャ（12）への反映点

- L6（記録・検証・更新）: 国内データの入手は「共同研究・会員参加・審査」型である。12 の L6 に「国内データ入手経路」として SMRC研究会、ITARDA客員研究員、保険会社共創の3経路を追記する案。
- 学習データの扱い: 【推察】SMRC系の信号は粗く（車速パルス由来、アクセル・操舵なし）、誤検出が多い。CAN信号の学習データには使わず、(a) 事象ラベル・リスクレベルの供給、(b) 評価用シナリオ、(c) 学習時のみ映像を使う蒸留（20）の教師、の用途に限る。
- L0〜L2: 日本のタクシー用ドラレコは、CANではなく個別信号（ブレーキ、ウインカー、車速パルス）の取り込みである。CAN相当と呼ぶ際は粗さを注記する。
- L3（R1）: ニアミス定義の閾値（±8 m/s²、±35 deg/s）は S26 の抜粋由来で、17 の SHRP2 トリガと並べて比較する材料になる。

## 4. 課題・ギャップ

- 申請様式・ライセンス・料金は、どの機関でも見つからなかった。
- SMRCの収録信号にアクセル開度・操舵角が含まれるかは未確認。
- ADAS状態フラグ・レーダ距離を含む日本の公開データは見つからなかった。
- 全ソースが抜粋のみ（I-01）。件数・誤検出率70%の帰属は未確認。
- 件数が資料ごとに食い違う（3.3万／8.9万／15万／20.5万／22万）。

## 5. 次のアクション提案

1. SMRCとITARDAへ、データ提供条件（費用、守秘、倫理審査）と収録信号一覧を問い合わせる文案を作る。
2. I-01 解消後、S1・S15〜S18・S22 の本文を確認する。
3. 誤検出率約70%の出典（S7、S8）を本文で特定する。
4. 17 のSHRP2トリガと S26 の閾値を同一表で比較する。
5. 12 の L6 に国内データ入手経路を追記する（設計作業）。

## 6. 参考文献リスト

本文 §2 の S1〜S36 の URL を参照。いずれも WebSearch の結果に現れたもので、本文は未読。
