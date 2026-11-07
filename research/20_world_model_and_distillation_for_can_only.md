# 20. E2E自動運転・ワールドモデル技術の、CANのみ予兆検知への転用（B-07）

- 調査日: 2026-11-07
- 論点: B-07。E2E運転モデル・ワールドモデルの表現学習・未来予測を、推論時はCANのみの予兆検知へ転用する手法（クロスモーダル蒸留、特権情報、行動ワールドモデル）を整理し、各手法で「推論時に必要な入力」を明記してCANのみで成立するかを判定する
- 既存調査との関係: 09 §4.3（LUPI、Chen ら 2025・SVM+）、09 [27]（Quantized Distillation）、09 [5]（Foundation CAN LM）、13 S20（GAIA-1 概要）は扱い済みとして除外した
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）34件／既出の再掲 0件。`scripts/sources_index.py --check` で全URLが NEW であることを確認した（abs 形式で照合。pdf/html 形式での既出は未確認）
- 確認方法の注記: この実行でも arxiv.org・blog.comma.ai・monoist.itmedia.co.jp などで WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の検索結果抜粋のみで確認した。数値・入力定義は抜粋に出たものだけを書き、抜粋に無い点は【推察】または「未確認」とした

## 1. エグゼクティブサマリー

- 「学習時のみ映像/LiDAR、推論時は CAN/車両信号のみ」で運転リスク・事故予測・軌道予測を行った研究は、検索範囲では見つからなかった（サブ論点1・3の探索クエリは §6 に記載）。
- 主要なワールドモデル（GAIA-2、Vista、Drive-OccWorld、Cosmos、comma.ai のモデル）は推論時に映像を要する。そのままでは CAN のみ制約を満たさない。
- 転用できるのは構造である。【推察】(a) 自車操作を条件にした次状態予測、(b) 予測誤差を異常度・危険度として使うこと、(c) 映像・LiDAR・VLM を学習時の教師だけに使うこと。
- 「映像で事前学習し、推論はセンサ時系列のみ」を満たす枠組みとして最も近いのは COMODO（映像→IMU 蒸留、人間活動認識）である。運転・CAN での検証は見つかっていない。
- CAN のみで成立する要素は、ego 動力学の予測（VDD、DyTR）と、予測誤差による異常検知の仕組み（CAN IDS 系）である。ただし目的は運転リスクではない。
- 否定的な知見がある。nuScenes/nuPlan では ego 状態だけの単純モデルが強く（抜粋）、自車履歴だけの学習は慣性外挿のショートカットに陥り得る。【推察】CAN のみの予兆モデルでも、物理・ルール系ベースラインを先に置き、ADAS フラグ・前方車距離を併用すべきである。
- 日本語ソースは3件のみで、いずれも周辺的（トレード誌、利用報告、情報処理学会の映像ベース研究）。日本語の一次研究は見つからなかった。

## 2. 主要知見

凡例: 推論時入力 / CANのみ判定（成立・条件付き・不成立）。確認方法はすべて「抜粋のみ」。

### 2.1 クロスモーダル蒸留・特権情報（サブ論点1）

**S1. COMODO: Cross-Modal Video-to-IMU Distillation for Efficient Egocentric Human Activity Recognition**
- Baiyu Chen, Wilson Wongso, Zechen Li, Yonchanok Khaokaew, Hao Xue, Flora Salim、2025、arXiv。https://arxiv.org/abs/2503.07259
- 事実: 凍結した映像エンコーダで IMU エンコーダを誘導する自己教師あり蒸留。ラベル不要。映像は学習時のみで、推論は IMU のみ。対象は一人称視点の人間活動認識で運転ではない。
- 推論時入力: IMU 時系列のみ / 方式としては成立（運転・CAN での実証なし）。
- 【推察】CAN 時系列エンコーダに置き換え、前方映像で意味的に事前学習する案が考えられる。

**S2. Enhancing Multimodal Large Language Models for Safety-Critical Driving Video Analysis**
- 著者未確認、2026年5月、arXiv。https://arxiv.org/abs/2605.22185
- 事実: ダッシュカム映像と同期した IMU（100Hz）・GPS 速度（1Hz）を使う。加速度ヒューリスティクスで候補イベントを抽出し、汎用 MLLM の疑似ラベルで小型 student を学習する。IMU ドロップアウト（確率50%）で映像のみ推論に対応。報告値は private データの3クラス分類 87.7%、2値判定 private 90.0%、Nexar 76.1%（映像のみ）。主タスクは事故予測ではなくイベント分類。
- 推論時入力: 映像のみ / 不成立（方向が本プロジェクトと逆）。
- 【推察】疑似ラベル生成とモダリティ・ドロップアウトの発想は CAN 側に転用できる可能性がある。

**S3. Learning by Cheating**（Dian Chen ら、2019、CoRL）https://arxiv.org/abs/1912.12294
- 事実: 地図・交通参加者位置を見る特権エージェントが、視覚のみの student を教える。最終エージェントは特権情報を使わない。
- 推論時入力: 前方カメラ映像 / 不成立（student が映像入力）。
- 【推察】特権教師と非特権 student の2段階構成の原型。特権情報を CAN の前方距離などで揃える構成の参考になる。

**S4. Learning from All Vehicles (LAV)**（Dian Chen, Philipp Krähenbühl、2022、CVPR）https://arxiv.org/abs/2203.11934
- 事実: 他車両軌道も含めて学習し、特権モーションプランナからオンポリシー蒸留で生センサ入力の方策にまとめる。アブレーションで他車両からの学習と特権蒸留がともに重要と報告。
- 推論時入力: カメラ映像 / 不成立。

**S5. Rakd: Risk-Aware Knowledge Distillation for Autonomous Driving in Adversarial Scenarios**（Yuenan Zhao、2025、IEEE、TRID 記録）https://trid.trb.org/View/2731608
- 事実: 特権情報を持つ RL 教師が、方策蒸留・特徴蒸留で視覚ベースの student を学習させる。敵対的道路利用者がいる場面が対象。
- 推論時入力: 視覚入力 / 不成立。

**S6. Enhancing End-to-End Autonomous Driving with Risk Semantic Distillation from VLM (RSD)**（著者未確認、2025年11月、arXiv）https://arxiv.org/abs/2511.14499
- 事実: 大規模 VLM のリスク認識知識をコンパクトな E2E 運転モデルに蒸留する。Bench2Drive で評価。
- 推論時入力: 運転モデルのセンサ入力（映像系）。VLM は学習時のみ / 不成立（元論文では）。
- 【推察】CAN student に VLM の疑似ラベルでリスク意味情報を蒸留する枠組みは転用候補。

**S7. Lightweight Spatio-Temporal Modeling via Temporally Shifted Distillation for Real-Time Accident Anticipation**（Patera, Chen, Fang、国立台湾科技大、ICLR 2026）https://proceedings.iclr.cc/paper_files/paper/2026/hash/cd6bca5b49813ec04556cd37eecb87dd-Abstract-Conference.html
- 事実: 凍結した画像ベース MobileCLIP を教師、軽量 student（RepMixer、RWKV 風再帰）に蒸留。蒸留は学習時のみ。arXiv 2508.15216 が同内容かは未確認。
- 推論時入力: 未確認（【推察】ダッシュカム映像）/ 不成立の可能性が高い。

**S8. ドライブレコーダ映像からの交通事故発生予測**（瀧本ら、情報処理学会、年未確認）https://ipsj.ixsq.nii.ac.jp/records/209071/export/bibtex
- 事実: 前方映像と自車位置情報から事故までの猶予時間を予測する。知識蒸留は扱っていない。
- 推論時入力: 前方映像＋位置情報 / 不成立。CAN のみ手法の比較ベースラインに使える【推察】。

**周辺（CAN 入力で蒸留が成立する例。映像教師ではなく、目的は侵入検知）**
- KD-GAT: https://arxiv.org/abs/2507.19686（student が教師の約6%）
- Multi-Stage Knowledge-Distilled VGAE and GAT: https://arxiv.org/abs/2508.04845（student が約1.5%）
- 【推察】CAN 入力の教師-student 蒸留自体は成立している。
- 西オンタリオ大学の学位論文（教師-student 蒸留による ADAS 操作予測。視線データも入力に使うため CAN のみではない）: https://ir.lib.uwo.ca/etd/6844

### 2.2 ワールドモデルの未来予測・予測誤差の転用（サブ論点2）

**S9. Trajectory-level unsupervised anomaly detection（multi-agent Transformer、予測残差）**
- Lyu & Fu（所属は検索要約によるが未確認）、2026、arXiv。https://arxiv.org/abs/2601.20367
- 事実: 正常運転を多エージェント Transformer で学習し、予測残差で逸脱を測る教師なし枠組み。検出した異常が物理的危険と一致するかを解釈可能なリスク指標で確認する。
- 推論時入力: ego と周辺エージェントの過去軌跡（【推察】地図の要否は未確認）/ 条件付き（周辺車の相対距離・相対速度がレーダ由来で CAN に載る場合のみ）。
- 【推察】「予測誤差＝リスク」を TTC/THW 系指標で検証する設計は、L3〜L5 にそのまま当てはまる最も近い雛形。

**S10. Exploring the Potential of World Models for Anomaly Detection in Autonomous Driving**（Bogdoll ら、2023、arXiv）https://arxiv.org/abs/2308.05701
- 事実: 世界モデルによる異常検知の概観。予測と実観測の乖離が大きいときに異常とする。
- 推論時入力: 調査対象手法では主に camera 等の知覚入力【推察】 / 不成立（原理は CAN 状態予測器で再利用可能）。

**S11. Camera-based anomaly detection on generative world models**（Noël Ollick、KIT 学士論文、年未確認）https://publikationen.bibliothek.kit.edu/1000170314/152752678
- 事実: 予測フレームと実フレームを絶対誤差・二乗誤差・SSIM・知覚差で比較する。教師なしで、学習データに異常を要しない。
- 推論時入力: カメラ映像 / 不成立。【推察】CAN では信号ごとの正規化誤差で代替できる。

**S12. Learning to Drive from a World Model**（comma.ai、2025、CVPR 2025 ワークショップ）https://arxiv.org/abs/2504.19077 ／ https://blog.comma.ai/mlsim/ ／ https://blog.comma.ai/011release/
- 事実: reprojective シミュレータと学習済み世界モデルで運転方策をオンポリシー学習する。世界モデルは過去の状態・行動から次状態を予測し、将来フレームも条件にできるため逆動力学モデルとしても働く。openpilot 0.11 は世界モデル由来の計画で訓練したモデルを出荷（公式ブログは URL とタイトルのみ抜粋で確認、本文未取得。「Diffusion Transformer」「3月17日」は第三者情報）。
- 推論時入力: 映像特徴と過去の行動 / 不成立。学習時のみ世界モデルを使う点は「学習時のみ他センサ」方針に合う。
- 【推察】逆動力学（状態遷移から操作を推定）は、CAN 上の異常操作検知に使える仮説。

**S13. GAIA-2**（Russell, Hu ら、Wayve、2025年3月、arXiv）https://arxiv.org/abs/2503.20523 ／ https://wayve.ai/wp-content/uploads/2025/03/GAIA_2_Technical_Report.pdf
- 事実: 動画トークナイザと潜在世界モデルからなる潜在拡散モデル。過去の潜在状態・行動・制御信号から将来の潜在状態を予測（latent flow matching）。最大5カメラ448×960の整合した映像を生成。制御は ego 動力学、他エージェント、道路配置、天候。
- 推論時入力: 過去の映像潜在＋行動 / 不成立。【推察】ego 行動を条件にした将来予測部分だけを CAN 潜在で再構成する案は研究仮説。

**S14. Drive-OccWorld**（Yang ら、浙江大、AAAI 2025）https://arxiv.org/abs/2408.14197 ／ https://ojs.aaai.org/index.php/AAAI/article/view/33010
- 事実: 多視点画像を BEV 履歴エンコーダに通し、将来の占有・フローを予測。速度・ステアリング角・軌道・コマンドを行動条件に受け、安全性・道路遵守コストで候補軌道を評価。nuScenes で dilated occupancy・flow の mIoU_f が +2.0%（抜粋）。
- 推論時入力: 多視点映像＋ ego 行動 / 不成立。

**S15. Vista**（OpenDriveLab、NeurIPS 2024）https://arxiv.org/abs/2405.17398 ／ https://github.com/OpenDriveLab/Vista
- 事実: 高レベルコマンドから軌道・操舵角・速度まで多様な行動条件を受け、長期予測が可能。真値の行動なしで候補行動を評価する報酬関数としても使える。
- 推論時入力: 過去フレーム＋行動 / 不成立。

**S16. Cosmos World Foundation Model Platform for Physical AI**（NVIDIA、2025、arXiv）https://arxiv.org/abs/2501.03575
- 事実: 拡散・自己回帰 Transformer とトークナイザを含み、カメラ姿勢条件・行動条件・自動運転向けのポストトレーニングを備える。運転モデルの行動条件の詳細は抜粋で確認できず。
- 推論時入力: 映像＋テキスト/行動 / 不成立。【推察】学習時のデータ拡張・合成危険シーン生成には使える。

**S17. A Survey of World Models for Autonomous Driving**（2025、arXiv）https://arxiv.org/abs/2501.11260
- 事実: 世界モデルを知覚・予測・計画の統合として整理し、4D 占有予測、生成によるデータ合成、ロングテール異常対応を課題に挙げる。
- 【推察】非カメラ系の世界モデルを探す索引に使える。

**S18. Towards a CAN IDS based on a neural-network data field predictor**（2018、arXiv）https://arxiv.org/abs/1812.11596
- 事実: 検索要約では、正常な CAN データで次メッセージ予測器を学習し、予測誤差を異常度とする。どの引用論文の記述かは抜粋から不明確で要確認。
- 推論時入力: CAN メッセージのみ / 仕組みとしては成立（目的は侵入検知で運転リスクではない）。

**S19. Turing「Terra」（MONOist）**（Turing、2024年9月記事）https://monoist.itmedia.co.jp/mn/spv/2409/05/news089.html
- 事実（抜粋）: 約1,500時間の走行映像で学習。自社データはアクセル・ブレーキ等の操作情報を含む。将来予測を運転判断に使え、障害物や車線逸脱などの稀な状況をシミュレートできる。精度数値は未確認。
- 推論時入力: 走行映像【推察】 / 不明（おそらく不成立）。

**S20. 松尾研究所 ABCI 利用報告 FY24-42**（2024年度、PDF）https://abci.ai/ja/acceleration_program/fy24/FY24-42.pdf
- 事実（抜粋）: 行動・カメラ画像・テキストを使い、自己教師あり将来予測で世界モデルを構築。データは CARLA で、GAIA-1 を模した Transformer。
- 推論時入力: 映像＋行動＋テキスト / 不成立。シミュレータ上の実証のみ。

### 2.3 自車操作列・状態列のみを入力とするモデル（サブ論点3）

**S21. DriveGPT: Scaling Autoregressive Behavior Models for Driving**（Cruise、2024、arXiv）https://arxiv.org/abs/2412.14415
- 事実: エージェントの将来状態をトークン化して自己回帰予測。1億件超の人間運転例、1B パラメータ超。公開データの約50倍と記載。事前学習が別の予測タスクを改善すると報告。
- 推論時入力: 全エージェントの軌跡（地図の要否は未確認）/ そのままでは不成立。【推察】前方車1台に縮約すれば近似できる可能性。

**S22. GPD-1: Generative Pre-training for Driving**（2024、arXiv）https://arxiv.org/abs/2412.08643
- 事実: ego・周辺・地図を統一トークンで自己回帰 Transformer に入力。ego 軌跡だけに限定したモデルではない。
- 推論時入力: ego・agent・map トークン / 不成立。

**S23. Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?**（2023、arXiv）https://arxiv.org/abs/2312.03031
- 事実: nuScenes では E2E モデルが将来経路計画で主に ego 状態に依存する。二次情報では、nuScenes が単純なため知覚情報が十分使われていない。
- 推論時入力: ego 状態 / ego-only 部分は成立。ただしリスク検知としての有効性は未検証。
- 【推察】オープンループ評価の限界を示すもので、「ego-only で十分」の根拠にはならない。

**S24. Rethinking Imitation-based Planner for Autonomous Driving（PlanTF）**（2023、arXiv）https://arxiv.org/abs/2309.10443
- 事実: 自車の過去の動きがクローズドループ性能を大きく劣化させると主張。過去の動きを外しても kinematic state からショートカットを学習し得る。
- 推論時入力: 自車履歴・周辺車・地図 / 不成立。【推察】自車履歴だけの予測は「慣性外挿」に頼る危険がある。

**S25. Parting with Misconceptions about Learning-based Vehicle Motion Planning**（2023、arXiv）https://arxiv.org/abs/2306.07962
- 事実: 現在の動的状態と中心線だけを条件とする単純なオープンループ・プランナーが、複雑なモデルを上回ると報告。ルールベースと組み合わせて nuPlan challenge 2023 で優勝。
- 推論時入力: ego 動的状態＋中心線（地図由来）/ 部分的（中心線は CAN で得られない）。

**S26. Vehicle Dynamics Embedded World Models for Autonomous Driving**（2025、arXiv）https://arxiv.org/abs/2512.02417
- 事実: Dreamer 型 VDD で ego 動力学と環境遷移を分離。入力は位置・向き・速度・加速度などの状態変数。階層的な再帰状態空間で Transformer ではない。シミュレーション評価。車両パラメータの異なる車両への汎化を狙う（日本語検索抜粋）。
- 推論時入力: ego 状態変数＋環境観測（詳細未確認）/ ego 動力学部分は成立。実車 CAN での検証なし。

**S27. Residual Learning towards High-fidelity Vehicle Dynamics Modeling with Transformer（DyTR）**（2025、arXiv）https://arxiv.org/abs/2502.11800
- 事実: 3自由度の物理モデルの残差を Transformer で補正する。履歴状態と制御入力から車両動力学を符号化。CAN 固有ではない。
- 推論時入力: 履歴の車両状態と制御入力 / 成立。
- 【推察】物理モデル＋残差の残差を異常度（摩擦低下・荷重・故障兆候）として使う転用は本ソースの主張ではない。

**S28. Level 2 Autonomous Driving on a Single Device: Diving into the Devils of Openpilot**（2022、arXiv）https://arxiv.org/abs/2206.08176
- 事実: 単眼入力から ego 将来軌跡を予測する supercombo モデルの分析。
- 推論時入力: 単眼映像＋車両状態（詳細未確認）/ 不成立。

**S29. Learning a Driving Simulator**（Santana & Hotz、comma.ai、2016、arXiv）https://arxiv.org/abs/1608.01230
- 事実: 運転者の挙動を模倣し、将来の道路上の出来事をシミュレートして計画する。
- 推論時入力: 映像 / 不成立。

**S30. commaVQ**（comma.ai、2023、GitHub）https://github.com/commaai/commavq
- 事実: 運転映像を VQ-VAE で10ビットのトークンに圧縮し、GPT 型世界モデルを学習。300万分の映像で学習したモデルと10万分の圧縮データセットを含む。
- 推論時入力: 映像トークン / 不成立。【推察】CAN 信号用のトークン化は別設計が要る（09 [5] が扱い済み）。

（S1〜S30 の他、周辺として KD-GAT・VGAE/GAT・UWO 学位論文の計3件を上に挙げ、合計34件。）

## 3. 手法ごとの判定表（推論時入力と CAN のみでの成立）

| 手法の型 | 代表 | 推論時入力 | CANのみ |
|---|---|---|---|
| 映像→センサ時系列の蒸留 | S1 COMODO | センサ時系列 | 方式は成立（運転で未検証） |
| センサ→映像の逆向き蒸留 | S2 | 映像 | 不成立 |
| 特権教師→視覚 student | S3〜S5 | 映像 | 不成立 |
| VLM リスク疑似ラベル蒸留 | S6 | 映像系 | 疑似ラベル枠組みのみ転用可 |
| 映像世界モデル | S12〜S16, S19, S20 | 映像＋行動 | 不成立（学習時の教師・合成には可） |
| 予測残差による異常検知 | S9, S18 | 軌跡/CAN | 条件付き〜成立（目的は別） |
| 自己回帰の行動モデル | S21, S22 | 全エージェント軌跡＋地図 | 不成立（縮約すれば条件付き） |
| ego 動力学モデル | S26, S27 | ego 状態・制御入力 | 成立 |

## 4. 統合アーキテクチャ（12）への反映点

- 【推察】L3 R4（ML 予兆）: 映像世界モデルは推論に使えないが、学習パイプラインで「映像→CAN エンコーダの蒸留（S1型）」「VLM 疑似ラベルによるリスク意味の付与（S2・S6型）」を試す価値がある。推論は CAN のみのまま。
- 【推察】L3 R4 / L4: 予測誤差を危険度とする設計（S9）。ego 動力学の物理＋残差モデル（S27）の残差を、R2（自車安定性）の異常度に使える。TTC/THW 系指標との整合検証を L6 に入れる。
- 【推察】L2・L6: 自車履歴だけの学習は慣性外挿に陥る（S24）。ADAS フラグと前方車距離を併用し、物理・ルールのベースラインを必ず比較対象に置く。オープンループの ego-only 好成績（S23）を有効性の根拠にしない。

## 5. 課題・ギャップ

- 「映像教師→CAN student」で運転リスクを扱った直接の研究は未発見。空白である可能性があるが、検索のみの結論であり、本文確認が必要である。
- 全34件が抜粋のみ。特に S9・S12・S21・S22 の入力定義は本文で確認していない。
- 日本語ソースが乏しい。J-STAGE・情報処理学会・自動車技術会の予稿の直接検索が未実施。
- 「CAN のみの操作 Transformer を自己教師あり事前学習して maneuver anticipation に使う」研究は未確認【推察】空白の可能性。
- 調査中に見つかった未確認の手がかり: LAW（ICLR 2025）、Toyota/Woven の世界モデル（求人情報のみで公開論文は確認できず）。

## 6. 次のアクション提案

1. I-01 解消後、S1・S9・S12・S21・S22 を本文確認し、入力定義と ego-only アブレーションを確かめる。
2. 映像付き公開データ（03 既出）で、映像→CAN エンコーダの COMODO 型蒸留と、CAN のみ学習を比較する PoC を設計する（09 の PoC 案と統合）。
3. ego 動力学の物理＋残差モデルの残差と、TTC/THW 等の指標との関係を検証する計画を 12 の L6 に追記する。
4. 日本語文献（J-STAGE、JSAE、情報処理学会）を直接検索する（B-22 として追加）。

探したが見つからなかったクエリ（サブ論点1・3）: privileged information distillation driver behavior crash risk prediction vehicle signals; cross-modal distillation LiDAR camera to CAN bus driving behavior; learning using privileged information trajectory prediction ego state only; video-to-IMU cross-modal pretraining vehicle telemetry accident risk; 特権情報 蒸留 運転 リスク予測 車両信号 映像 学習時のみ; driving behavior foundation model ego trajectory only autoregressive; human driver behavior prediction from CAN transformer pretraining; latent world model vehicle state CAN bus data only future prediction。

## 7. 参考文献リスト

本文 §2 の各ソースの URL を参照（S1〜S30 と周辺3件、すべて URL 付き）。
