# 27. 日本語文献・国内各社資料による、運転操作列の基盤モデル・蒸留・世界モデルの確認（B-22）

- 調査日: 2026-11-14
- 論点: B-22。20 で日本語ソースが乏しかった点を、J-STAGE・IPSJ・JSAE・CiNii・国内各社の公開資料で補う。各資料の推論時入力を明記する。
- 既存調査との関係: 20 の全ソース（E2E・世界モデル・蒸留の海外文献中心）は扱い済みとして除外した。本稿は国内資料の有無と推論時入力の確認に限る。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）16件／既出の再掲 0件。`scripts/sources_index.py --check` で全URLが NEW であることを確認した。
- 確認方法の注記: arxiv.org、global.honda、www.woven.toyota、global.nissannews.com、jstage、ipsj.ixsq.nii.ac.jp、kaken、aisin 等で WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の検索結果抜粋のみで確認しており、本文は未読である。

## 1. エグゼクティブサマリー

- 運転操作列の事前学習・自己教師あり、特権情報蒸留、世界モデルを「CANのみ」で推論する日本語の学会論文・国内各社資料は、検索範囲では見つからなかった（クエリは §5 に記載）。20 の「日本語ソースが乏しい」という結論を補強する。
- 国内の運転基盤モデルの公開資料は映像中心である（Turing の ACT-Bench/CoVLA、Toyota/Woven の AI Vision Engine、日産の次世代 ProPILOT＋Wayve、TIER IV の E2E）。推論時入力はカメラ・LiDAR 等で、本プロジェクトの制約に合わない。
- 日本語の学会文献は、(a) シミュレータ上の LSTM ドライバモデル（芝浦工大、JSAE）、(b) ドラレコ映像による急ブレーキ分析、(c) 視線＋車両情報による運転行動予測（名古屋大）が中心である。いずれも推論時に CAN のみではない。
- 「操作の前に現れる信号を識別器に入れる」構成（名古屋大）と、天候など外的文脈を学習時に使う構成（九州大）は、学習時のみ他センサを使う蒸留・特権情報の国内での素材になりうる【推察】。
- Honda の Driver Coaching は車両通信データとドライバモデルで診断する国内OEM事例だが、入力信号が CAN かは未確認である。
- 国内データとして CoVLA（車両信号を含む、非商用）と NEDO 報告の STRIDE-QA が確認できたが、CAN のみ学習用としては映像が前提で、ライセンス制約もある。

## 2. 主要知見

### 2.1 国内各社・研究機関（サブ論点2）

**S1. ACT-Bench（Terra を含む）** — Turing、2024、arXiv。https://arxiv.org/abs/2412.05337 （抜粋のみ）
- 要点: 行動指示への追従度を測る世界モデルのベンチマーク。Terra は GAIA-1 の構成に従い、短い動画と目標軌道から動画を生成する。学習データは OpenDV-YouTube、nuScenes、CoVLA。報告値の行動追従 Accuracy は Vista 0.307、Terra v1 0.441、Terra v2 0.632（公式ページ記載）。
- 推論時入力: 映像と目標軌道。CAN のみではない。
- 示唆: 【推察】「操作を条件に未来を生成する」枠組みは CAN の操作列条件付けと対応するが、出力は映像である。CAN のみ系に要るのは未来の CAN 状態予測である。追従度を測る考え方は、予測した操作列と実挙動の整合性検証に流用できる可能性がある。

**S2. CoVLA Dataset** — Turing、WACV 2025（検索結果の記載）、データセット。https://huggingface.co/datasets/turing-motors/CoVLA-Dataset （抜粋のみ）
- 要点: 東京で収集した 30 秒クリップ 1 万本（約 80 時間超。ある要約は 83.3 時間）。前方カメラ、車両信号、GNSS、IMU を同期。ステアリング角・加速度・ウインカー等の同時分布に逆比例する重みで稀な操作を優遇してサンプリングする。ライセンスは学術・非商用。
- 推論時入力: データ単体では規定されない。
- 示唆: 【推察】稀な操作の逆頻度サンプリングは、CAN のみの学習データ設計（稀事象の重み付け）の参考になる。非商用のため産業利用には直接使えない。

**S3. Toyota/Woven by Toyota の AI Vision Engine・Integrated ANZEN System** — 2026-04-22、プレスリリース。https://www.woven.toyota/en/news/20260422 （抜粋のみ）
- 要点: カメラ映像等を使う視覚言語基盤モデル。Woven City Behavior AI（人の動きの解釈・予測）等と組み合わせる。世界モデル・蒸留の言及は検索結果に無かった。
- 推論時入力: カメラ映像中心。
- 示唆: 【推察】映像基盤モデルを前提とし、CAN のみ系とは別系統である。

**S4. 日産・次世代 ProPILOT** — 2025-09-22、プレスリリース。https://global.nissannews.com/ja-JP/releases/next-gen-propilot-technology （抜粋のみ）
- 要点: Wayve AI Driver と次世代 LiDAR を組み合わせる。試作車は 11 カメラ・5 レーダー・1 LiDAR、2027 年度に国内市販車へ搭載予定。「世界モデル」の語は見つからず、説明は「エンボディド AI」「基盤モデル」。
- 推論時入力: カメラ・レーダー・LiDAR。
- 示唆: 【推察】国内OEMは映像系 E2E を外部導入する形で、CAN のみの予兆検知とは別系統である。

**S5. TIER IV の E2E アーキテクチャ** — 2025-07、プレスリリース（転載記事）。https://www.automotiveworld.com/news/tier-iv-unveils-end-to-end-architecture-for-level-4-autonomy-to-be-demonstrated-across-50-locations-nationwide/ （抜粋のみ）
- 要点: Autoware 基盤に拡散モデル系 ML とルールベース部品を併用。2026 年初頭から国内 50 か所で段階導入の計画。蒸留・世界モデルの言及は見つからなかった。
- 推論時入力: 自動運転向けセンサ認識を含むと読める（詳細未確認）。
- 示唆: 【推察】学習系の出力をルール層で監督する構成の例で、12 の L5 付近の考え方と対応する可能性がある。

**S6. Honda Driver Coaching Service** — Honda、2025-08（ITS世界会議 展示資料）。https://global.honda/jp/safety/ITS/2025/pdf/04_Honda-Driver-Coaching-Service_1.pdf （抜粋のみ）
- 要点: 車両の通信データと運転行動モデルでリアルタイムに運転を診断し、熟練運転者モデルと比較する。
- 推論時入力: 車両通信データ（CAN 由来かは明記なし）。
- 示唆: 【推察】国内OEMによる CAN 系データ＋ドライバモデルの事例になりうるが、本文未確認で信号・手法は不明。

**S7. Honda State Estimation Technology** — Honda、2025（ITS世界会議 展示資料）。https://global.honda/jp/safety/ITS/2025/pdf/05_State-Estimation-Technology_1.pdf （抜粋のみ）
- 要点: 飲酒・感情状態の推定。SHRP2 を独自解析し、ドライバモニタカメラで表情・動きを検知する。
- 推論時入力: ドライバモニタカメラ。
- 示唆: 【推察】学習時のみ映像を使い推論時は CAN のみにする蒸留の候補テーマになりうるが、この展示自体は映像依存である。

**S8. Dream2Assist** — CoRL 2024、論文（所属は掲載ページで未確認）。https://dream2assist.github.io （抜粋のみ）
- 要点: 人間の目的を推定する世界モデル（RSSM）と支援エージェントの組み合わせ。評価は高速レーシング環境の合成ドライバで、実車ログではない。
- 推論時入力: シミュレーション状態。
- 示唆: 【推察】意図を潜在状態として推定する構成は、CAN 操作列からの意図・危険状態推定に転用しうる。実車検証は未確認。

**S9. NEDO 事業報告（身体性マルチモーダル基盤モデル、Turing 関連）** — NEDO。https://www.nedo.go.jp/content/800036443.pdf （抜粋のみ。年・正式題名は未確認）
- 要点: 東京都内で 3,500 時間以上の走行データを取得し、100 時間超の視覚・言語・行動データセット「STRIDE-QA」を整備したとされる。
- 推論時入力: 映像（VLA）。
- 示唆: 【推察】国内の運転基盤モデル化は映像中心で、CAN のみの操作列基盤モデルは国内文献上空白の可能性がある。

### 2.2 日本語の学会文献（サブ論点1）

**S10. ドライブレコーダーデータから深層学習により推定した天候情報を用いた急ブレーキ推定** — 九州大・東京大生産技術研究所、2021、『生産研究』73巻2号。https://cir.nii.ac.jp/crid/1390006050801747200 （抜粋のみ）
- 要点: ドラレコ映像から天候を推定し、プローブデータと合わせて急ブレーキを識別する。研究室ページによると 3 クラス天候では天候なしより精度が向上し、6 クラスでは全体として悪化した。
- 推論時入力: 映像（天候推定）。
- 示唆: 【推察】天候・路面など外的文脈を学習時のみ映像から得て推論時は CAN 由来信号で代替する特権情報の候補。6 クラスで悪化した点はラベル品質への注意を示す。

**S11. MDL原理を用いた車両挙動データからの特徴抽出手法の提案** — 横山・白石、2018、情報処理学会 DPSWS。https://ipsj.ixsq.nii.ac.jp/record/191923/files/IPSJ-DPSWS2018014.pdf （抜粋のみ）
- 要点: 車載スマートフォンのセンサ時系列を SAX で文字列化し、N-gram＋MDL で運転行動の部分文字列を抽出する。数値結果は抜粋に無かった。
- 推論時入力: スマートフォンのセンサ（CAN ではない）。
- 示唆: 【推察】操作列の離散トークン化の古典的前身で、20 のトークン化基盤モデルとの比較対象になる。

**S12. LSTMを用いた個人適応型ドライバモデルに関する研究** — 芝浦工大、2021、自動車技術会秋季大会予稿集 No.92-21。https://tech.jsae.or.jp/paperinfo/ja/content/p202102.053/ （抜粋のみ）
- 要点: LSTM で個人の運転特性を再現する。関連資料ではドライビングシミュレータのデータを使い、追従シーンで Jerk の累積分布の類似性を評価する。
- 推論時入力: シミュレータの車両状態・操作量。
- 示唆: 【推察】個人別操作列生成の国内先行例で、ドライバ個人化の根拠になる。目的は再現であり予測・警告ではない。

**S13. LSTMドライバモデル（追い越し挙動）** — 芝浦工大、2022、自動車技術会秋季大会予稿集 No.136-22。https://tech.jsae.or.jp/paperinfo/en/content/p202202.247/ （抜粋のみ。和文題名は未確認）
- 要点: 追い越し挙動を LSTM でモデル化し、位置と車線変更タイミングで評価。ADAS 適用は今後の課題とされる。
- 推論時入力: シミュレータデータ。
- 示唆: 【推察】操作列生成モデルの出力を規則と照合する使い方は、L6 側の検証の参考になる。

**S14. ドライバの視線情報と車両情報を組み合わせた運転行動予測** — 名古屋大ほか、年・掲載誌は抜粋で未確認。https://pubdb.vislab.is.i.nagoya-u.ac.jp/~murase/pdf/952-pdf.pdf （抜粋のみ）
- 要点: 視線と車両情報から識別器を構築し、一般道実験で 6 種類（左折・右折・左右車線変更・信号直進・信号停止）の予測の有効性を確認した。数値は抜粋に無かった。
- 推論時入力: 視線（ドライバ映像由来）＋車両情報。本プロジェクトの制約に不適合。
- 示唆: 【推察】視線は推論時に使えないため、学習時のみの特権情報として蒸留する設計の根拠になりうる。

**S15. 予防安全効果評価シミュレータ（ASSESS）におけるドライバのブレーキ操作タイミングの決定方法** — 森田ら、2013、日本機械学会論文集C編 79巻800号。https://www.jstage.jst.go.jp/article/kikaic/79/800/79_1003/_article/-char/ja （抜粋のみ）
- 要点: 模擬ドライバのブレーキ操作を「タイミング」と「踏力」で決め、本論文はタイミングを扱う。続報では自車速度を算定に含めると実データとの一致度が上がったとされる。
- 推論時入力: シミュレータ上の模擬ドライバ。
- 示唆: 【推察】ブレーキ開始タイミングの物理・ルール系ベースラインとして、学習系予測の比較やラベル定義（意図の開始点）の整理に使える。

**S16. 潜在リスク予測ドライバモデルに基づくブレーキ制御支援システムの設計と有効性評価** — 東京農工大、2016、自動車技術会論文集 47巻6号。https://cir.nii.ac.jp/crid/1390282679589564160?lang=en （抜粋のみ）
- 要点: 死角からの歩行者飛び出しなどの潜在リスクに対し、AEB より早期に介入する減速の共有制御を提案。ドライビングシミュレータで評価。
- 推論時入力: 周辺環境（歩行者・死角）の認識情報。
- 示唆: 【推察】熟練ドライバの潜在リスク予測を内部モデルとして持つ国内先行例。周辺認識が前提で CAN のみでは入力が不足する。

## 3. 統合アーキテクチャ（12）への反映点【推察】

- L0〜L1: CoVLA の逆頻度サンプリング（S2）とトークン化の前身（S11）を、CAN 操作列の学習データ設計・記号化の参考として 20 に紐づける。
- L2〜L3（R4）: ブレーキ開始タイミングのルール系ベースライン（S15）を、学習系予測の比較対象として加える。
- L5 付近: 学習系をルールで監督する構成（S5）、ドライバ個人化（S12）。
- 学習時のみ使う特権情報の候補: 視線（S14）、天候（S10）、ドライバモニタ映像（S7）。いずれも蒸留の実証は未発見で、12 の構成変更は不要である。

## 4. 課題・ギャップ

- CAN のみで、ブレーキ意図予測・操作列の事前学習・特権情報蒸留・世界モデルを行う日本語の査読論文・国内各社資料は未発見。
- 全ソースが抜粋のみ。Honda の入力信号、S14 の年・掲載誌、S9 の年・題名など未確認が残る。
- 日本語学会予稿（JSAE 春秋季大会、IEICE ITS 研究会）の直接検索は未実施。

## 5. 次のアクション提案

1. jstage・ipsj・kaken・global.honda を WebFetch で取得できるようにし（I-01）、S6・S14 の本文で入力信号・年を確定する。
2. JSAE 予稿集（tech.jsae.or.jp）と IEICE ITS 研究会の直接検索で、CAN 系ブレーキ意図予測を探す。
3. S15 のブレーキ開始タイミングモデルを、14 の予測ホライズン設計のベースラインとして比較する。
4. CoVLA の車両信号仕様（論文本文）を確認し、20 の学習データ設計に反映する。

検索クエリ: 「ブレーキ意図 予測 運転行動 CAN データ 深層学習 J-STAGE」「運転行動 自己教師あり学習 事前学習 車両信号」「運転行動 世界モデル 潜在状態」「知識蒸留 運転行動 特権情報」「Turing 完全自動運転 世界モデル Terra」「Preferred Networks 自動運転 基盤モデル 蒸留」「Honda Research Institute Japan 運転行動 予測 世界モデル」「Woven by Toyota 世界モデル 蒸留」「Tier IV End-to-End 知識蒸留」「日産 ProPILOT 次世代 AI 世界モデル」「デンソー アイシン 運転行動 予測 基盤モデル」ほか。Preferred Networks・Honda Research Institute Japan・デンソー・アイシンの該当資料は未発見。

## 6. 参考文献リスト

S1 https://arxiv.org/abs/2412.05337
S2 https://huggingface.co/datasets/turing-motors/CoVLA-Dataset
S3 https://www.woven.toyota/en/news/20260422
S4 https://global.nissannews.com/ja-JP/releases/next-gen-propilot-technology
S5 https://www.automotiveworld.com/news/tier-iv-unveils-end-to-end-architecture-for-level-4-autonomy-to-be-demonstrated-across-50-locations-nationwide/
S6 https://global.honda/jp/safety/ITS/2025/pdf/04_Honda-Driver-Coaching-Service_1.pdf
S7 https://global.honda/jp/safety/ITS/2025/pdf/05_State-Estimation-Technology_1.pdf
S8 https://dream2assist.github.io
S9 https://www.nedo.go.jp/content/800036443.pdf
S10 https://cir.nii.ac.jp/crid/1390006050801747200
S11 https://ipsj.ixsq.nii.ac.jp/record/191923/files/IPSJ-DPSWS2018014.pdf
S12 https://tech.jsae.or.jp/paperinfo/ja/content/p202102.053/
S13 https://tech.jsae.or.jp/paperinfo/en/content/p202202.247/
S14 https://pubdb.vislab.is.i.nagoya-u.ac.jp/~murase/pdf/952-pdf.pdf
S15 https://www.jstage.jst.go.jp/article/kikaic/79/800/79_1003/_article/-char/ja
S16 https://cir.nii.ac.jp/crid/1390282679589564160?lang=en
