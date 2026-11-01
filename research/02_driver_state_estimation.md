# テーマ2: CAN信号のみによるドライバー状態推定（眠気・疲労・注意散漫・飲酒・体調急変）

- 調査日: 2026-11-01
- テーマのゴール: ステアリング・ペダル操作・車両挙動など、CANバスから取得できる信号だけを使ってドライバー状態（眠気・疲労・注意散漫・脇見・飲酒・体調急変）を推定する手法について、論文・記事・公式発表を集め、実用化事例と研究水準を整理する。カメラ・LiDAR・ドライバーモニタ映像は使わない前提とする。
- 表記ルール: 「【推察】」を付けた記述は調査者の推察であり、ソースに書かれた事実ではない。それ以外はソース記載の事実を要約したものである。

---

## 1. エグゼクティブサマリー

1. ステアリング主体の眠気検知は2009〜2010年に量産化されている（Mercedes ATTENTION ASSIST、Bosch/VW）。現在もマツダDAA、日産インテリジェントDA、ホンダ ドライバー注意力モニターが「運転開始直後の操作を学習し、その後の逸脱を見る」方式で実装している。
2. EUのDDAW（委任規則2021/1341）は、車線位置やステアリング入力による車両ベースの解析を推奨手法として明記している。性能要件はKSS 8以上で警告し、平均感度40%超（またはその90%信頼区間の下限が20%超）であり、ハードルは高くない。CANのみの方式で法規要件を満たせる余地がある。
3. 一方、ADDW（2023/2590）は視線の監視を前提としており、Euro NCAP 2026のDriver Engagementプロトコルも脇見・マイクロスリープ・睡眠を視線や閉眼時間で定義している。脇見（視覚的注意散漫）をCANのみで規制・評価基準に適合させるのは難しい。
4. 研究水準を見ると、シミュレータでは車両信号のCNN-LSTMで3クラス精度96.0%（Arefnezhad 2020）という報告がある。実路では、Mercedesの大規模データ（54名・204走行）を使っても3クラス誤り率16.6%（ANN）にとどまり、「眠気クラス」の正答は54.6%であった（Friedrichs & Yang 2010）。シミュレータと実路の差は大きい。
5. 飲酒は車線位置の変動と平均車速から精度73〜86%（NHTSA, シミュレータ）、低血糖はCANのみでAUROC 0.73（NEJM AI, テストコース）で検出できたとの報告がある。「眠気以外の体調変化」もCAN挙動に表れるという根拠はあるが、いずれも小規模である。
6. 体調急変（EDSS）について、国交省ガイドラインはハンドル無操作継続時間を検知項目の一つとして挙げている（閾値は規定なし、応答確認は必須）。トヨタはカメラを使わず、アクセル・ブレーキ・ステアリングの一定時間無操作で異常と判断する方式を量産化した。
7. 主な課題は次の3点である。(a) 意図的な「ゆるい運転」と眠気の区別ができない。(b) 個人差が大きく、ベースライン学習が必須である。(c) 正解ラベル（KSS）の時間分解能が5〜15分と粗い。

---

## 2. 主要知見（ソースごと）

### 2.1 規格・法規・公的ガイドライン

#### [R1] Commission Delegated Regulation (EU) 2021/1341（DDAW: Driver Drowsiness and Attention Warning）
- 組織/年/種別: 欧州委員会 / 2021年4月23日 / 規格・法規
- URL: https://eur-lex.europa.eu/eli/reg_del/2021/1341/oj （本文の確認には https://lawplayer.com/eu/act/32021R1341 を併用）
- 要点:
  - 作動: 70 km/h超で自動的に起動し、65〜130 km/h（または車両の最高速度の低い方）で作動する。
  - 警告閾値: KSS 8以上相当で警告する。KSS 7での警告は任意である。
  - 検証: 被験者10名以上、真陽性と偽陰性を合わせて10件以上。平均感度40%超、または90%信頼区間の下限20%超。公道試験では緩和される。KSSの自己評価は約5分間隔で行い、昼夜の両条件で試験する。
  - 手法: 車線位置とステアリング入力（steering reversal rate, SDLPなど）を使う車両ベースの解析を推奨している。生理指標などの代替指標も、精度と頑健性があれば認める。
  - データ: 通常運用での顔認識などの生体データ処理は禁止。データは機能に必要なものに限り、クローズドループで保持する。
- 使用CAN信号: 規定なし（ステアリング入力・車線位置が例示）
- 性能指標: 感度（KSS≥8イベントの検出率）
- 本プロジェクトへの示唆: CANのみ方式のベンチマークとして、DDAW附属書の検証手順（5分ごとのKSS、感度40%）をそのまま評価プロトコルに使える。【推察】偽警報の数値上限がないため、製品ではEU基準より厳しいFP管理が必要になる。
- 補足: DDAWの適用時期は新型車2022年7月・全新車2024年7月と理解しているが、今回は原文で確認していない（要確認）。

#### [R2] Commission Delegated Regulation (EU) 2023/2590（ADDW: Advanced Driver Distraction Warning）
- 組織/年/種別: 欧州委員会 / 2023年7月13日 / 規格・法規
- URL: https://eur-lex.europa.eu/eli/reg_del/2023/2590/oj/eng
- 要点: 長時間の視覚的脇見の警告に焦点を当てている。業界解説では、作動中は運転者の視線方向を監視することが求められるとされる。昼夜の両方で有効に作動する必要がある。前文にはADDW要件を2024年7月7日から適用する旨の記載がある。全新規登録車への適用は2026年7月と解説する業界記事もある（要原文確認）。
- 使用CAN信号: 対象外（視線ベース）
- 本プロジェクトへの示唆: 【推察】脇見（視覚的注意散漫）の法規適合をCANのみで行うことは事実上できない。本プロジェクトではADDW適合を目的とせず、注意散漫の「影響として現れる操作劣化」を補助的に検知する位置づけにするのが妥当である。

#### [R3] Euro NCAP "Safe Driving – Driver Engagement Protocol" Version 1.2（2026年7月、2026年1月実施）
- 組織/年/種別: Euro NCAP / 2026 / 評価基準（公式）
- URL: https://cdn.euroncap.com/cars/assets/Euro_NCAP_Protocol_Safe_Driving_Driver_Engagement_v1_2_ebce03a443.pdf
- 要点:
  - Driver Monitoringは25点で、内訳はTransient 15点、Non-transient 10点。
  - 眠気（2点）は「KSS>7に達するまでに検知、または同等の指標」で、50 km/h以上で機能すること。
  - 非疲労性の障害（アルコール・薬物、2点）も得点対象である。
  - 障害状態の検知には、50 km/h以上で最大10分の学習期間が認められる。
  - マイクロスリープは1〜2秒の閉眼、睡眠は3秒以上の閉眼で定義される。無反応ドライバーは、脇見警告後3秒以内に視線が戻らない、または6秒以上の閉眼で定義される（より早い別手段も可）。
- 本プロジェクトへの示唆: 【推察】眠気と非疲労性障害の項目は「同等の指標」を認める書き方なので、CANベースでも理論上は得点の余地がある。ただし、脇見・マイクロスリープ・睡眠・無反応は視線や閉眼で定義されるため、CANのみではほぼ得点できない。CANのみの方式は「カメラ非搭載車・後付け用途の補完」と位置づけるべきである。

#### [R4] 国土交通省 報道発表「世界初！『ドライバー異常時対応システム』のガイドラインを策定しました」
- 組織/年/種別: 国土交通省 自動車局 / 2016年3月29日 / 公式発表
- URL: https://www.mlit.go.jp/report/press/jidosha07_hh_000202.html
- 要点: 急病などで運転継続が困難になった場合に車両を自動停止させるシステムのガイドラインである。対象は二輪車を除く全自動車。検知方式は自動検知・ドライバー押しボタン・同乗者押しボタンの3種。誤作動を考慮し、減速開始前に一定時間の警報を出す。

#### [R5] 国土交通省「ドライバー異常時対応システムについて」（路肩退避型・異常自動検知システム ガイドライン概要）
- 組織/年/種別: 国土交通省 / 2018年3月策定分の概要資料 / 公的ガイドライン
- URL: https://www.mlit.go.jp/common/001228684.pdf
- 要点:
  - ドライバーの異常に起因する事故は年間200〜300件発生している。
  - 異常自動検知の検知項目は、①姿勢崩れ（7パターン）、②閉眼（2秒以上）、③ハンドル無操作（指標はハンドル無操作継続時間、閾値は具体値を規定せず、応答確認アクチュエーションは必須）である。
  - 路肩退避型では50 km/h上限で同一車線を走行し、作動開始から180秒を超えた場合は減速停止する。
- 使用CAN信号: ハンドル無操作（操舵角・操舵トルク）
- 本プロジェクトへの示唆: CANのみで扱える公的な検知項目は「ハンドル無操作」である。誤検知が避けられないため、応答確認（警報に対する操作応答）の設計が前提になる。【推察】ペダル無操作や車線逸脱傾向を組み合わせると、無操作時間の閾値を短くできる可能性がある。

### 2.2 メーカー・サプライヤーの公式情報と量産事例

#### [M1] Mercedes-Benz ATTENTION ASSIST（10周年記念プレスリリース）
- 組織/年/種別: Mercedes-Benz Italia（メディアサイト）/ 2019年頃（2009年導入から10周年）/ 公式発表
- URL: https://media.mercedes-benz.it/international-coffee-day---prenditi-una-pausa-lattention-assist-celebra-il-suo-decimo-anniversario/
- 要点:
  - 2009年に世界初として導入され、現在は全乗用車で標準装備。
  - 70以上のパラメータを監視し、ステアリング操作が眠気の特に強い指標であるとしている。
  - 走行開始後の数分で個人プロファイルを作り、その後のセンサ値と比較する。
  - 作動域は60〜200 km/h。開発ではほぼ700名のドライバーで試験した。
- 使用CAN信号: ステアリング操作、ウインカー・ペダル操作、車速、前後・横加速度、外乱（横風・路面のうねり）
- 本プロジェクトへの示唆: 外乱（横風・路面）の推定と抑制を量産品が明示的に実装している点が重要である。

#### [M2] Bosch Driver Drowsiness Detection（Electronic Specifier記事）
- 組織/年/種別: Bosch（Electronic Specifier掲載）/ 2012年4月13日 / 記事（メーカー情報ベース）
- URL: https://www.electronicspecifier.com/products/sensors/bosch-driver-drowsiness-detection
- 要点:
  - 入力は電動パワステ、またはESPの舵角センサである。
  - 「ほとんど操舵しない期間」の後に「小さく速く急な修正操舵」が来るパターンを検出する。
  - 走行時間、ウインカー使用、時刻、修正頻度を加味して疲労度を算出し、閾値を超えるとコーヒーカップ表示で休憩を促す。
  - 2010年のVW Passatで初めて標準装備された。
- 使用CAN信号: 操舵角、ウインカー、車速、時刻、走行時間
- 本プロジェクトへの示唆: 「デッドバンド＋急修正」イベント（後述のSTWEVNT）が量産ロジックの中核である。既存の舵角センサだけで実装でき、追加コストがほぼない。

#### [M3] マツダ技報 No.32「マツダの先進安全技術『i-ACTIVSENSE』の進化」（4章 ドライバー・アテンション・アラート）
- 著者/組織/年/種別: 中村正・内海将司・朝日雅博・古山貫一・三戸手亮太（マツダ）/ 2015 / メーカー技報
- URL: https://www.mazda.com/contentassets/ca8528da3716443289911272a04795d1/files/2015_no038.pdf
- 要点:
  - ハンドル操作・アクセル操作・前方カメラ（FSC）の情報などの多要素を、マハラノビス距離の単位空間（改良MTシステム）で扱う。
  - 運転開始から約20分は覚醒状態とみなして運転特性を学習し、その後は学習結果との距離値がしきい値以上なら休憩を促す。
  - 統計量（平均・中央値・最小・最大など）を算出して判定する。
  - 検証では複数ドライバーが5分ごとに疲労や注意力の低下を自己申告し、それとの対応を示した（定量指標の記載はない）。
- 使用CAN信号: 操舵角、ヨーレート、ヨー角、アクセル操作（＋カメラの車線情報）
- 手法: 改良MTシステム（マハラノビス・タグチ法）による個人ベースラインからの異常度
- 本プロジェクトへの示唆: 「個人ベースライン＋多変量異常度」は、ラベルが少なくても実装でき、本プロジェクトの初期アルゴリズムとして最も現実的である。

#### [M4] Mazda USA Owner's Manual "How to Use the Driver Attention Alert (DAA)"（2025 MX-5）
- 組織/年/種別: Mazda North American Operations / 2025年モデル / 公式取扱説明書
- URL: https://www.mazdausa.com/static/manuals/2025/mx-5/contents/65420300.html
- 要点:
  - 作動条件: 白線または黄線を検知していること、運転開始から60分以上経過していること、約65〜140 km/hが20分以上続いていること、そのドライブでの初期学習が完了していること。
  - 急カーブ中や車線変更中は作動しない。
  - 15分以上の停車、約65 km/h未満での約30分走行、電源OFFで学習がリセットされる。
- 本プロジェクトへの示唆: 量産品は作動条件（ゲーティング）を厳しく絞っている。誤報を避けるための判定区間選別が重要である。

#### [M5] 日産 FAQ「インテリジェント DA（ふらつき警報）」（ルークス 2025年10月〜）
- 組織/年/種別: 日産自動車 / 2025 / 公式FAQ
- URL: https://faq2.nissan.co.jp/faq/show/77812
- 要点: ドライバーの普段のステアリング操作を学習し、直近の操作パターンと比べて注意力の低下を判断すると、表示と警報音で休憩を促す。約60 km/h以上で作動し、プロパイロットのハンドル支援中はOFFになる。
- 使用CAN信号: 操舵角（ステアリング操作パターン）
- 本プロジェクトへの示唆: 【推察】軽自動車の全車に標準装備していることから、舵角のみの低コストなロジックで量産できることがわかる。LKA作動中は操舵がドライバー由来でなくなるため、ADAS状態フラグで判定を止める必要がある。

#### [M6] Honda ACCORD 2025 取扱説明書「ドライバー注意力モニター」
- 組織/年/種別: 本田技研工業 / 2025 / 公式取扱説明書
- URL: https://www.honda.co.jp/ownersmanual/webom/jpn/accord/2025/details/136256090-344480.html
- 要点:
  - ハンドル操作から眠気や注意力が低下した運転を検知し、注意力レベルを段階表示する。
  - レベル1ではメッセージ・警報音・ステアリング振動で休憩を促し、休憩しなければ15分後に再警告する。30分未満の運転では表示しない。
  - 40 km/h超かつEPS警告灯消灯時に作動する。LKAS/渋滞運転支援の作動中、悪路、強風、頻繁な車線変更・加減速時は作動しない。
- 使用CAN信号: 操舵（EPS由来）、車速、ADAS作動状態
- 本プロジェクトへの示唆: 警告を段階化し、再警告間隔を設けるHMI設計の参考になる。

#### [M7] MONOist「レクサスの安全システムをトヨタ車で民主化、ハード変更せずにコストを抑制」
- 組織/年/種別: MONOist（ITmedia）/ 2020年2月 / 記事（トヨタ説明会の報道）
- URL: https://monoist.itmedia.co.jp/mn/spv/2002/04/news042_2.html
- 要点: トヨタのドライバー異常時停車支援システムは、一定時間アクセル・ブレーキ・ステアリングが操作されない場合にドライバーの異常と判断する。コスト抑制のため、ドライバーモニタ用カメラは使わない。警告に反応がなければホーンとハザードで周囲に知らせながら減速し、車線内で停車する。
- 使用CAN信号: アクセル開度、ブレーキSW/圧、操舵（角/トルク）、LTA状態
- 本プロジェクトへの示唆: CANのみで体調急変（無反応状態）を検知する量産例である。ただし「無操作が続いた後」の検知なので、予兆検知ではなく事後対応である。

### 2.3 査読論文・プレプリント・技術報告

#### [P1] Steering Entropy（Nakayama et al. 1999 / Boer et al. 2005）
- 著者/年/種別: O. Nakayama, T. Futami, T. Nakamura, E. R. Boer / 1999 / 論文（SAE Technical Paper 1999-01-0892、原典は有料のため二次文献で書誌を確認）。再検討論文はBoer, Rakauskas, Ward, Goodrich (2005) "Steering Entropy Revisited"（Driving Assessment 2005）。
- URL: https://swov.nl/en/publicatie/steering-entropy-revisited （Boer 2005）、実装ドキュメント https://pythonhosted.org/undaqTools/steeringentropy.html
- 要点: 操舵角の予測誤差の分布からエントロピーを求め、操舵の「滑らかさ／予測しにくさ」を定量化する。非運転タスク（NDRT）中の負荷評価のために導入された。undaqToolsの実装では、5次Butterworthで低域通過した後に4 Hzへリサンプルし、前半データでARモデルを、後半データで予測誤差のベースライン分布を作る。αでビン幅を決め、2M+2ビンでエントロピーを計算する。ベースラインには最低2分のデータが必要である。
- 使用CAN信号: 操舵角
- 性能指標: 負荷条件間の感度（Markkula 2006でSRRと並び最も感度が高いと報告）
- 本プロジェクトへの示唆: ベースライン区間が必要な相対指標であり、トリップ冒頭の学習と相性が良い。

#### [P2] Markkula & Engström (2006) "A Steering Wheel Reversal Rate Metric for Assessing Effects of Visual and Cognitive Secondary Task Load"
- 著者/年/種別: G. Markkula, J. Engström（Volvo）/ 2006 / 論文（ITS World Congress）
- URL: https://eprints.whiterose.ac.uk/131534/ （実装: https://github.com/gmarkkula/SteeringWheelReversalRate ）
- 要点: 操舵角の反転回数率（SRR）を提案した。比較した操舵指標の中で、SRRとSteering Entropyが実験条件間で最も感度が高かった。認知負荷では操舵活動が増えて車線位置の分散が減り、視覚負荷では操舵活動も車線位置の変動も増える。
- 使用CAN信号: 操舵角
- 本プロジェクトへの示唆: 操舵活動の大きさだけでは脇見と認知的注意散漫を区別できないが、車線位置（またはヨー/横変位の代替量）と組み合わせれば区別できる可能性がある。

#### [P3] Kountouriotis et al. (2016) 「Reversal rates identify the type of driver distraction」（リポジトリ版）
- 著者/年/種別: G. Kountouriotis ほか（Leeds）/ 2016 / 論文（査読付き受理稿）
- URL: https://eprints.whiterose.ac.uk/id/eprint/102869/1/Reversal%20rates%20identify%20the%20type%20of%20driver%20distraction%20Resubmission_final.pdf
- 要点: 反転率で認知的注意散漫を識別できることを示した。視覚タスクを中央に提示すると車線偏差が減り（非視覚的な注意散漫と似る）、操舵活動は増える。
- 使用CAN信号: 操舵角（＋シミュレータの車線位置）
- 本プロジェクトへの示唆: 注意散漫の種類によって操舵指標の変化方向が異なるため、単純な閾値ではなく多変量で判定すべきである。

#### [P4] Friedrichs & Yang (2010) "Drowsiness Monitoring by Steering and Lane Data based Features under Real Driving Conditions"
- 著者/年/種別: F. Friedrichs, B. Yang（Univ. Stuttgart、データはMercedes-Benz提供）/ 2010 / 論文（EUSIPCO 2010, pp.209-213）
- URL: https://www.iss.uni-stuttgart.de/forschung/publikationen/friedrichs-eusipco2010.pdf
- 要点:
  - データ: Mercedesの眠気データベース（約10,300走行・123万km）を絞り込み、204走行・54名・10台（52,768 km）を使用。ラベルは15分間隔のKSSで、覚醒（KSS<6）、中間（6≤KSS<8）、眠気（KSS≥8）の3クラス。
  - 特徴量: 48特徴をLANE/STW/CANに分類。主なものは以下。
    - 操舵速度の四分位（STV25/50/75。眠いほど操舵速度は低下し、ρp≈-0.3）
    - NMRHOLD（0.5°未満の保持）、NMWRONG（急修正回数、ρs=0.25）、STWEVNT（無操舵デッドバンド＋急修正）
    - ELLIPSE、VHAL、MICROSTEERINGS、STWZCR
    - DEGOINT（舵角から単一軌跡モデルで計算した横加速度と実測横加速度の差。操舵トルク不要）
    - CROSSWIND、ROADBUMP（車輪速から路面を推定）
    - CIRCADIAN（ρp=0.49）、TOT、MONOTONY、TRFCDENS
  - 作動条件: 80〜180 km/hで作動。車線変更・カーブ・スポーティ運転・加減速・スイッチ操作時は抑制する。各特徴を最初の数分間の最大値で正規化（ベースライン化）し、窓は最大40分。
  - 結果: SFFSで選んだ11特徴で、3クラスのテスト誤りはANN 16.6%、LDA 32.4%。ANNの眠気クラス正答率は54.6%（45.4%は中間クラスと誤判定）。
- 使用CAN信号: 操舵角・操舵速度、横加速度、前後加速度、車輪速、車速、ウインカー、各種スイッチ操作、時刻（＋車線カメラ）
- 性能指標: 3クラス誤り率、Pearson/Spearman相関
- 本プロジェクトへの示唆: CAN特徴量カタログとして最も直接使える。著者は、覚醒していても空いた高速道路や会話中には眠気と同じ「ゆるい運転」になり区別できないと述べている。この点は本プロジェクトの根本的な限界として認識すべきである。

#### [P5] Forsman, Vila, Short, Mott, Van Dongen (2013) "Efficient driver drowsiness detection at moderate levels of drowsiness"
- 著者/年/種別: P. M. Forsman ほか（Washington State Univ.）/ 2013 / 査読論文（Accident Analysis & Prevention 50:341-350）
- URL: https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Efficient-driver-drowsiness-detection-at-moderate/99900546990301842
- 要点: 2つの模擬シフト勤務研究（高忠実度シミュレータ）で、文献にある87の眠気指標を評価した。PCAで主要な2次元（操舵変動と車線変動）が得られた。操舵入力から車線位置変化への伝達関数を導き、操舵変動から車線変動を推定できることを示した。中程度の眠気の段階で検知できるとしている。
- 使用CAN信号: 操舵角
- 本プロジェクトへの示唆: 車線カメラがなくても、操舵から「SDLP相当」を推定できる根拠になる。ただしシミュレータ限定の結果である。

#### [P6] McDonald, Lee, Schwarz, Brown (2014) "Steering in a Random Forest: Ensemble Learning for Detecting Drowsiness-Related Lane Departures"
- 著者/年/種別: A. D. McDonald ほか（Univ. of Iowa / NADS）/ 2014 / 査読論文（Human Factors 56(5):986-998）
- URL: https://iro.uiowa.edu/esploro/outputs/journalArticle/Steering-in-a-Random-Forest-Ensemble/9984627327502771
- 要点: NADSシミュレータの72名分のデータで、操舵角のみからランダムフォレストで眠気関連の車線逸脱を検知した。PERCLOS（閉眼率）より分類精度とAUCが高く、PPVは同程度であった。2012年の会議版では、眠気関連の車線逸脱を6秒前に予測できると報告している（検索結果記載）。
- 使用CAN信号: 操舵角
- 手法: ランダムフォレスト
- 本プロジェクトへの示唆: 「眠気の度合い」ではなく「眠気による車線逸脱イベント」を予測対象にすると、カメラ指標を上回り得る。事故予防という最終目的に近い定式化である。

#### [P7] Li, Li, Li, Cheng, Shi (2017) "Online Detection of Driver Fatigue Using Steering Wheel Angles for Real Driving Conditions"
- 著者/年/種別: Z. Li ほか（清華大学）/ 2017 / 査読論文（Sensors 17(3):495）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5375781/
- 要点: 北京〜秦皇島の実路を100 km/h一定で走行し、有効ドライバー6名・約14.68時間のデータを得た（4名は眠くならず除外）。ラベルは3名の専門家による1分単位の顔映像判定（覚醒/眠気）。操舵角（100 Hz）の近似エントロピー（ApEn, m=2, r=0.2SD）を時系列化して適応的な区分線形近似を行い、覚醒参照系列とのDTW距離を閾値で判定する。191サンプルで精度78.01%、誤警報29.35%、見逃し15.15%。
- 使用CAN信号: 操舵角
- 本プロジェクトへの示唆: 実路・舵角のみの性能は8割弱、誤警報は3割程度という目安になる。

#### [P8] Arefnezhad, Samiee, Eichberger, Frühwirth, Kaufmann, Klotz (2020) "Applying deep neural networks for multi-level classification of driver drowsiness using Vehicle-based measures"
- 著者/年/種別: S. Arefnezhad ほか（TU Graz）/ 2020 / 査読論文（Expert Systems with Applications 162:113778）
- URL: https://tugraz.elsevierpure.com/en/publications/applying-deep-neural-networks-for-multi-level-classification-of-d/
- 要点: 固定式シミュレータで単調な夜間高速道路を走行した44セッションを使用。入力は横偏差、横加速度、ヨーレート、操舵角、操舵角速度の5信号。CNN＋RNN（LSTM/GRU）で3クラスに分類し、CNN-LSTMで最高精度96.0%。SVMやk-NNを上回った。
- 使用CAN信号: 横加速度、ヨーレート、操舵角、操舵角速度（横偏差はシミュレータ由来）
- 手法: CNN-LSTM / CNN-GRU
- 本プロジェクトへの示唆: 深層学習の上限的な性能を示している。ただしシミュレータであり、実路のP4・P7との差（約96% 対 約78〜83%）がドメインギャップの大きさを示す。

#### [P9] Sahayadhas, Sundaraj, Murugappan (2012) "Detecting Driver Drowsiness Based on Sensors: A Review"
- 著者/年/種別: A. Sahayadhas ほか / 2012 / 査読論文（レビュー、Sensors 12(12):16937-16953）
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3571819
- 要点:
  - SWM（0.5〜5°の微小修正）は、眠気で減少する。
  - SDLPはKSS 1/5/8/9でそれぞれ0.19/0.26/0.36/0.47 mと上昇する。ただしKSS 9でも0.25 m未満の個人がいる。
  - 車両ベース指標の限界として、道路形状と車両ダイナミクスへの依存、個人差、眠り始めてから現れるため遅いこと、飲酒や薬物でも同様に変化することを挙げている。
  - 結論として、生理・行動指標とのハイブリッドを推奨している。
- 本プロジェクトへの示唆: CANのみの限界を整理する際の基本文献である。

#### [P10] Lee et al. (2010) "Assessing the Feasibility of Vehicle-Based Sensors to Detect Alcohol Impairment"（DOT HS 811 358）
- 著者/年/種別: J. D. Lee ほか（NHTSA / NADS）/ 2010 / 公的技術報告
- URL: https://www.nhtsa.gov/sites/nhtsa.gov/files/811358_0.pdf
- 要点: NADSシミュレータのデータで飲酒検知アルゴリズムを構築した。ロジスティック回帰（標準的な速度・車線維持指標）と決定木（広範な運転指標）を使い、車線位置の標準偏差と平均車速がBAC水準を最もよく分けた。精度は約73〜86%で、車両ベースの飲酒検知は実現可能と結論している。
- 使用CAN信号: 車速、操舵（＋車線位置）
- 本プロジェクトへの示唆: 飲酒は「トリップ開始時点から存在する障害」であり、トリップ内ベースライン方式（M1/M3）では検出できない。【推察】ドライバー単位で複数トリップにまたがるベースラインが必要になる。

#### [P11] Lehmann et al. (2023) "Machine learning for non-invasive sensing of hypoglycaemia while driving in people with diabetes"
- 著者/年/種別: V. Lehmann ほか（ETH Zurich / Bern / LMU ほか）/ 2023 / 査読論文（Diabetes, Obesity and Metabolism）
- URL: https://boris.unibe.ch/178864/
- 要点: 1型糖尿病患者がシミュレータで運転した。研究1（n=18）は正常血糖と顕著な低血糖、研究2（n=9）は正常血糖と軽度の低血糖を比較した。CANと視線計測データのみのMLで低血糖を検知できることを示した。
- 使用CAN信号: シミュレータのCAN相当信号（詳細は原文参照）

#### [P12] Lehmann et al. (2024, NEJM AI) 実車での低血糖検知
- 著者/年/種別: Lehmann ほか / 2024 / 査読論文（NEJM AI）。2 Minute Medicineの解説記事（2024-09-13）とLMUリポジトリのアップロード版で確認した。
- URL: https://2minutemedicine.com/machine-learning-model-non-invasively-detects-suspected-cases-of-hypoglycemia-during-real-world-driving ／ https://epub.ub.uni-muenchen.de/123399/1/NEJM_AI_Upload.pdf
- 要点: 1型糖尿病の成人30名が、絶食で低血糖を誘発した状態で教官同乗のもとテストコースを走行した。AUROCはCANのみで0.73±0.07、ドライバーモニタカメラ（頭部運動）のみで0.70±0.16、併用で0.80±0.11。
- 使用CAN信号: 運転特性（具体的な変数は記事に記載なし）
- 本プロジェクトへの示唆: 「体調急変の予兆」をCANのみで捉えられる可能性を示す、数少ない実車の根拠である。カメラ単独と同程度の性能であった点は、CANのみ方式にとって追い風である。

#### [P13] Izmir Bakircay University ＋ Tofas: "Enhancing Driver Safety: Integrating ECG and CAN-Bus Data for Accurate Drowsiness Detection"
- 組織/年/種別: Izmir Bakircay Univ.・Tofas（トルコ）/ 2025 / 査読論文（Traitement du Signal, IIETA）。紹介記事はCiA CAN Newsletter 2025年12月号。
- URL: https://www.iieta.org/journals/ts/paper/10.18280/ts.420238 ／ https://can-cia.org/fileadmin/cia/documents/publications/cnlm/december_2025/cnlm_25-4_p12_can-based_ivn_data_used_for_drowsiness_detection_holger_zeltwanger_cia.pdf
- 要点: 実ドライバーの実路走行で約10時間のデータを集めた。ECG由来のHRVと、CAN由来の車速・ステアリング・ブレーキ圧を統合し、3クラスで精度85%（ECGのみの従来研究は多クラスで70%未満が一般的）。ECGを使わないCANのみの分類も検討した。ランダムフォレストでCANパラメータの重要度を分析した。組込み向けの最適化を今後の課題としている。
- 使用CAN信号: 車速、ステアリング、ブレーキ圧
- 本プロジェクトへの示唆: 量産CANフレームを直接使った最近の実路研究である。データ量は小さい。

#### [P14] 近森・大谷・清水 (2001)「ドライバの覚醒度低下による操舵特性の変化」
- 著者/年/種別: 近森順・大谷崇・清水裕 / 2001 / 査読論文（自動車技術会論文集 32巻1号 pp.107-112）
- URL: https://cir.nii.ac.jp/crid/1520290883580145536
- 要点: 覚醒度の低下と操舵特性の関係を扱った国内論文である（書誌のみ確認、本文は未取得）。
- 本プロジェクトへの示唆: 国内でも2000年前後から操舵ベースの研究がある。本文の入手は次のアクションとする。

---

## 3. ドライバー状態推定に使えるCAN指標の一覧

| # | 指標 | 定義・計算方法 | 主な対象状態 | 必要CAN信号 | 根拠ソース |
|---|---|---|---|---|---|
| 1 | Steering Entropy (SE) | 操舵角を低域通過して約4 Hzへリサンプルし、ベースライン区間でARなどの予測モデルを作る。予測誤差をαで決めたビンに分け、エントロピーを計算する（ベースライン比で評価）。 | 負荷・注意散漫・眠気 | 操舵角 | P1, P2 |
| 2 | Steering Reversal Rate (SRR) | 低域通過した操舵角で、ギャップ角（例: 数度）以上の向きの反転が起きた回数を毎分で数える | 視覚的/認知的注意散漫 | 操舵角 | P2, P3, R1 |
| 3 | 微小修正率（SWM / MICROSTEERINGS） | 0.5〜5°程度の小さな修正操舵の頻度。眠いと減少する | 眠気 | 操舵角 | P9, P4 |
| 4 | NMRHOLD（保持率） | 操舵角の変化が0.5°未満の状態が一定時間以上続く割合 | 眠気 | 操舵角 | P4 |
| 5 | NMWRONG / STWEVNT（デッドバンド＋急修正） | 無操舵区間の後に来る急な修正操舵の回数・強度。車速・単調さ・横風・悪路・車線変更で閾値を調整し、抑制する | 眠気（量産ロジックの中核） | 操舵角、車速、ウインカー | M2, P4 |
| 6 | 操舵速度の四分位（STV25/50/75） | 操舵角速度（多項式平滑化微分）のEWMA窓での第1四分位・中央値・第3四分位。眠いと低下する（ρp≈-0.3） | 眠気 | 操舵角（速度） | P4 |
| 7 | 操舵角のSD・ゼロ交差率（STWZCR） | 窓内の標準偏差、毎秒の操舵方向の反転数。ZCRは個人差が大きい | 眠気・運転スタイル | 操舵角 | P4, P9 |
| 8 | ELLIPSE（位相面） | 操舵角と操舵角速度の平均からの距離の大きさ | 眠気 | 操舵角 | P4 |
| 9 | 近似エントロピー（ApEn） | 操舵角の短窓ApEn（m=2, r=0.2SD）の時系列を、覚醒参照とDTWで比較する | 疲労 | 操舵角 | P7 |
| 10 | DEGOINT（ドライバー・車両相互作用） | 舵角から単一軌跡モデルで計算した横加速度ă_y = l·v²·δ/(1+SG·v²)と、実測a_yの差のEWMA | 眠気（反応低下） | 操舵角、車速、横加速度 | P4 |
| 11 | SDLP代替量 | ①操舵→車線位置の伝達関数で推定（Forsman）、②ADAS（LDA/LKA）ECUがCANに出す車線内オフセットを直接使う【推察】 | 眠気・飲酒 | 操舵角／ADAS車線情報 | P5, P9, P10, R1 |
| 12 | 外乱推定（CROSSWIND / ROADBUMP） | 計算横加速度と実測横加速度の差から横風・路面の傾きを、車輪速から路面の凹凸を推定し、判定を抑制する | （抑制用） | 横加速度、車輪速、操舵角 | P4, M1, M6 |
| 13 | 事前要因（TOT・CIRCADIAN・MONOTONY・TRFCDENS） | 連続運転時間、時刻（概日リズムで重み付け）、単調走行時間、車線変更率と加減速イベントから推定した交通密度 | 眠気の事前確率 | 時刻、車速、前後加速度、ウインカー | P4（CIRCADIAN ρp=0.49）, M2 |
| 14 | 平均車速・車速変動 | 窓内の平均と標準偏差 | 飲酒・低血糖 | 車速 | P10, P13 |
| 15 | 多変量異常度（マハラノビス距離） | トリップ冒頭の約20分で単位空間（平均・共分散）を学習し、以後の統計量ベクトルの距離を閾値で判定する | 疲労・注意力低下 | 操舵角、ヨーレート、アクセル開度など | M3 |
| 16 | 無操作継続時間 | 操舵（角/トルク）、アクセル、ブレーキがいずれも無操作の連続時間。応答確認アクチュエーション（警報への操作応答）と組み合わせる | 体調急変・無反応 | 操舵角/トルク、アクセル、ブレーキSW | R5, M7 |
| 17 | ウインカー関連（TURNINDADVANCE・使用率） | 車線変更に対するウインカーの先行時間、ウインカー使用の有無 | 注意力低下（個人差大） | ウインカー、（車線変更検出用のヨー/車線情報） | P4, M2 |

共通の前処理（ソース記載）:
- 作動条件によるゲーティング: 65〜130/140 km/h、またはそれ以上の車速。急カーブ・車線変更・加減速・LKA作動中・悪路・強風時は除外する（R1, M4, M6, P4）。
- 個人ベースライン化: トリップ冒頭の数分〜約20分を覚醒状態とみなして正規化する（M1, M3, P4）。
- EWMA/EWVARによる逐次統計量（P4）。

---

## 4. 課題・ギャップ

### 4.1 CANのみ方式の本質的な限界
- **眠気と「意図的にゆるい運転」の区別ができない**: 覚醒していても、空いた高速道路や会話中には眠気と同じ操舵パターンになる（P4の結論）。【推察】誤警報率を下げるには、事前要因（時刻・連続運転時間）や交通密度との組み合わせが必須である。
- **検知が遅い**: 車両ベースの指標は眠り始めてから変化することが多く、事故予防には遅い場合がある（P9）。DDAWの閾値もKSS 8で、すでに「眠気と闘っている」段階である（R1）。
- **注意散漫の種類で変化の方向が逆になる**: 視覚負荷では車線変動が増え、認知負荷では車線変動が減って操舵活動が増える（P2, P3）。一つの指標の閾値だけでは判定できない。
- **規制・評価のトレンドはカメラ方向**: ADDWは視線前提（R2）であり、Euro NCAP 2026は脇見・マイクロスリープ・睡眠・無反応を視線や閉眼で定義している（R3）。CANのみで制度上カバーしやすいのは、DDAW（眠気）と、Euro NCAPの眠気・非疲労性障害の「同等指標」枠に限られる。
- **体調急変は事後検知になりがち**: 量産の無操作検知（M7）は、意識喪失の後に一定時間が経ってから作動する。予兆検知の根拠は低血糖研究（P11, P12）などに限られ、まだ小規模である。
- **外乱の影響**: 横風、路面の傾き、轍、悪路で操舵指標が汚れる（M1, M6, P4, P9）。【推察】日本の一般道（カーブが多い、低速、信号停止）では作動条件を満たす区間が少なく、高速道路以外での有効性は未検証である。

### 4.2 個人差
- SDLPと眠気の相関は個人ごとに大きく異なり、KSS 9でもSDLPが0.25 m未満のドライバーがいる（P9）。
- 車線を細かく修正し続けるタイプと、ゆるく保持するタイプがいる（P4）。STWZCRなどはドライバー固有性が高い（P4）。
- 量産品はいずれも走行ごとの初期学習（数分〜20分、M1/M3/M4/M5）で対処している。ただし、トリップ開始時点で既に眠い、あるいは飲酒している場合はベースラインが汚れる。【推察】ドライバーIDを紐づけた長期プロファイル（複数トリップ）と、トリップ内ベースラインの併用が必要である。

### 4.3 正解ラベルの取得
- **KSS**: 5分間隔（R1, M3）〜15分間隔（P4）の自己申告である。時間分解能が粗く、急な変動を捉えられない（P4）。申告そのものが覚醒刺激になるという問題もある（P4はこれを考慮して15分間隔とした）。
- **観察者評価・顔映像評定**: P7は専門家3名による1分単位の評定を使い、不一致サンプルは除外した。
- **生理指標**: EEG/EOG/PERCLOSは高分解能だが、全被験者で安定して取れるとは限らない（P4）。
- **イベントラベル**: 眠気関連の車線逸脱（P6）は、事故予防の目的に直結するラベルである。【推察】本プロジェクトでは、PCS・LDA警報フラグ、急ブレーキ、車線逸脱フラグなどのCAN上のイベントを「危険の代理ラベル」として使い、その数十秒〜数分前の操舵特徴から予測する設計にすれば、KSSなしで大量データを使える。
- **シミュレータと実路の差**: シミュレータでは96%（P8）、実路では約78%（P7）、3クラスの眠気クラスでは54.6%（P4）である。実路では安全上、強い眠気になる前に走行を中止する必要があり、眠気サンプルが少なくなる（P4）。

---

## 5. 次のアクション提案

1. **ベースライン特徴量の実装（短期）**: 既存のCANログに対し、第3節の#1〜#10、#12、#13を実装する。作動条件ゲーティング（車速65〜130 km/h、ウインカーOFF、|ヨーレート|小、LKA/ACC操舵介入OFF）と、EWMAによる逐次計算を行う。CAN信号はP4の特徴リストに合わせる。
2. **個人ベースライン＋多変量異常度モデル（短期〜中期）**: マツダ方式（M3）を参考に、トリップ冒頭の学習によるマハラノビス距離と、ドライバー単位の長期プロファイルを併用する異常度スコアを作る。教師なしで先行評価する。
3. **代理ラベルによる教師あり評価（中期）**: PCS・LDA警報、急ブレーキ、車線逸脱フラグをイベントラベルとし、直前N分の操舵特徴から発生を予測するモデル（ランダムフォレスト→LSTM）を作る（P6の定式化を参照）。AUC・PPV・リードタイムで評価する。
4. **小規模なKSSラベル付き実験（中期）**: DDAW附属書に準拠した5分間隔のKSS、昼夜両条件、10名以上の実験を行い、「KSS≥8の感度40%超」を最低ライン、誤警報率を独自KPIとして性能を測る（R1）。
5. **無反応・体調急変ロジックの試作（中期）**: 国交省ガイドライン（R5）とトヨタ方式（M7）に倣い、操舵・アクセル・ブレーキの無操作継続時間に、車線内のふらつき（ヨーレート/横加速度の低周波ドリフト）と応答確認警報を組み合わせて検知する。閾値短縮の余地をログで検証する。

---

## 6. 参考文献リスト

### 規格・法規・公的資料
- [R1] Commission Delegated Regulation (EU) 2021/1341 (DDAW). https://eur-lex.europa.eu/eli/reg_del/2021/1341/oj ／ 本文参照: https://lawplayer.com/eu/act/32021R1341
- [R2] Commission Delegated Regulation (EU) 2023/2590 (ADDW). https://eur-lex.europa.eu/eli/reg_del/2023/2590/oj/eng
- [R3] Euro NCAP, Safe Driving – Driver Engagement Protocol v1.2 (July 2026). https://cdn.euroncap.com/cars/assets/Euro_NCAP_Protocol_Safe_Driving_Driver_Engagement_v1_2_ebce03a443.pdf
- [R4] 国土交通省 報道発表（2016-03-29）「ドライバー異常時対応システム」ガイドライン策定. https://www.mlit.go.jp/report/press/jidosha07_hh_000202.html
- [R5] 国土交通省「ドライバー異常時対応システムについて」（路肩退避型・異常自動検知ガイドライン概要）. https://www.mlit.go.jp/common/001228684.pdf

### メーカー・サプライヤー・報道
- [M1] Mercedes-Benz Italia, ATTENTION ASSIST 10周年. https://media.mercedes-benz.it/international-coffee-day---prenditi-una-pausa-lattention-assist-celebra-il-suo-decimo-anniversario/
- [M2] Electronic Specifier (2012), Bosch Driver Drowsiness Detection. https://www.electronicspecifier.com/products/sensors/bosch-driver-drowsiness-detection
- [M3] 中村ほか (2015) マツダ技報 No.32「マツダの先進安全技術『i-ACTIVSENSE』の進化」. https://www.mazda.com/contentassets/ca8528da3716443289911272a04795d1/files/2015_no038.pdf
- [M4] Mazda USA, 2025 MX-5 Owner's Manual, How to Use the Driver Attention Alert (DAA). https://www.mazdausa.com/static/manuals/2025/mx-5/contents/65420300.html
- [M5] 日産 FAQ, インテリジェント DA（ルークス 2025年10月〜）. https://faq2.nissan.co.jp/faq/show/77812
- [M6] Honda ACCORD 2025 取扱説明書, ドライバー注意力モニター. https://www.honda.co.jp/ownersmanual/webom/jpn/accord/2025/details/136256090-344480.html
- [M7] MONOist (2020-02)「レクサスの安全システムをトヨタ車で民主化、ハード変更せずにコストを抑制」. https://monoist.itmedia.co.jp/mn/spv/2002/04/news042_2.html

### 論文・技術報告
- [P1] Nakayama, Futami, Nakamura, Boer (1999) Development of a steering entropy method for evaluating driver workload, SAE 1999-01-0892（書誌は二次文献で確認）／ Boer et al. (2005) Steering Entropy Revisited. https://swov.nl/en/publicatie/steering-entropy-revisited ／ 実装: https://pythonhosted.org/undaqTools/steeringentropy.html
- [P2] Markkula & Engström (2006) A Steering Wheel Reversal Rate Metric for Assessing Effects of Visual and Cognitive Secondary Task Load. https://eprints.whiterose.ac.uk/131534/ ／ https://github.com/gmarkkula/SteeringWheelReversalRate
- [P3] Kountouriotis et al. (2016) Reversal rates identify the type of driver distraction（受理稿）. https://eprints.whiterose.ac.uk/id/eprint/102869/1/Reversal%20rates%20identify%20the%20type%20of%20driver%20distraction%20Resubmission_final.pdf
- [P4] Friedrichs & Yang (2010) Drowsiness Monitoring by Steering and Lane Data based Features under Real Driving Conditions, EUSIPCO 2010. https://www.iss.uni-stuttgart.de/forschung/publikationen/friedrichs-eusipco2010.pdf
- [P5] Forsman et al. (2013) Efficient driver drowsiness detection at moderate levels of drowsiness, Accid. Anal. Prev. 50:341-350. https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Efficient-driver-drowsiness-detection-at-moderate/99900546990301842
- [P6] McDonald et al. (2014) Steering in a Random Forest, Human Factors 56(5):986-998. https://iro.uiowa.edu/esploro/outputs/journalArticle/Steering-in-a-Random-Forest-Ensemble/9984627327502771
- [P7] Li et al. (2017) Online Detection of Driver Fatigue Using Steering Wheel Angles for Real Driving Conditions, Sensors 17(3):495. https://pmc.ncbi.nlm.nih.gov/articles/PMC5375781/
- [P8] Arefnezhad et al. (2020) Applying deep neural networks for multi-level classification of driver drowsiness using Vehicle-based measures, Expert Syst. Appl. 162:113778. https://tugraz.elsevierpure.com/en/publications/applying-deep-neural-networks-for-multi-level-classification-of-d/
- [P9] Sahayadhas, Sundaraj, Murugappan (2012) Detecting Driver Drowsiness Based on Sensors: A Review, Sensors 12(12):16937-16953. https://pmc.ncbi.nlm.nih.gov/articles/PMC3571819
- [P10] Lee et al. (2010) Assessing the Feasibility of Vehicle-Based Sensors to Detect Alcohol Impairment, NHTSA DOT HS 811 358. https://www.nhtsa.gov/sites/nhtsa.gov/files/811358_0.pdf
- [P11] Lehmann et al. (2023) Machine learning for non-invasive sensing of hypoglycaemia while driving in people with diabetes, Diabetes Obes. Metab. https://boris.unibe.ch/178864/
- [P12] Lehmann et al. (2024) NEJM AI（実車での低血糖検知）. 解説: https://2minutemedicine.com/machine-learning-model-non-invasively-detects-suspected-cases-of-hypoglycemia-during-real-world-driving ／ 原稿: https://epub.ub.uni-muenchen.de/123399/1/NEJM_AI_Upload.pdf
- [P13] Izmir Bakircay Univ. / Tofas (2025) Enhancing Driver Safety: Integrating ECG and CAN-Bus Data for Accurate Drowsiness Detection, Traitement du Signal. https://www.iieta.org/journals/ts/paper/10.18280/ts.420238 ／ 紹介記事: CiA CAN Newsletter 4/2025 https://can-cia.org/fileadmin/cia/documents/publications/cnlm/december_2025/cnlm_25-4_p12_can-based_ivn_data_used_for_drowsiness_detection_holger_zeltwanger_cia.pdf
- [P14] 近森・大谷・清水 (2001)「ドライバの覚醒度低下による操舵特性の変化」自動車技術会論文集 32(1):107-112. https://cir.nii.ac.jp/crid/1520290883580145536

（計26件: 規格・法規・公的資料5件、メーカー・サプライヤー・報道7件、論文・技術報告14件。うち査読論文・プレプリント・会議論文12件、公的技術報告1件、技報1件。いずれも検索結果またはfetchで実在を確認した。P1の原典SAE論文とP14は書誌情報のみ確認。）
