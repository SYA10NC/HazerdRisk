# 29. 離散時間ハザードの校正と警告閾値の運用設計（B-24）

- 調査日: 2026-11-16
- 論点: B-24。稀少事象の生存モデルの校正評価（IPCW Brier、D-calibration 等）と、確率出力を警告閾値へ変換して偽警報負担を制御する既存知見を集める。
- 既存調査との関係: 22（生存・ハザードモデルの運転への適用。既出URLを除外）、09 §4.1（ラベル不足・不均衡）、10 §3（偽警報KPI・ROC運用点）は扱い済みとして除外した。22 の次の一歩（校正と閾値）に当たる。
- ソース件数: 新規（本文確認）0件／新規（抜粋のみ）24件／既出の再掲 0件。`scripts/sources_index.py --check` で全URLが NEW であることを確認した。サブエージェントが「題名・URLのみ」とした項目（PMC11785332、2507.02807 等）は件数に含めず、末尾に注記した。
- 確認方法の注記: arxiv.org・eur-lex 等で WebFetch が名前解決に失敗した（ISSUES I-01 継続）。全ソースは WebSearch の抜粋のみで確認し、本文は未読である。数値・書誌は抜粋由来で、原文照合が必要。著者・年が取れなかったものは「不明」とした。

## 1. エグゼクティブサマリー

- 校正評価の基本は、(a) IPCW 型 Brier/IBS、(b) D-calibration、(c) 固定時刻の校正曲線と ICI の3系統である。いずれも抜粋ベースで、高打ち切り下の IPCW が不安定になる旨の記述が複数ある。
- IBS と右打ち切り対数尤度は理論上 improper とされるが、シミュレーションでは proper に近く振る舞うとの報告がある（Sonabend ら）。proper な代替（Cen-log、Cen-Brier）も提案されている。
- 順位性能が良くても確率が合わないことがある。TCGA 系の校正監査では、時刻別 1-calibration 検定の多くが棄却され、Platt 補正で改善するとの抜粋がある。
- 校正を学習時に組み込む手法（X-CAL、DCS）と、事後補正（Conformalized Survival Distributions）が存在する。
- 閾値運用では、医療の早期警戒で「警報件数の上限（約10件/日）から閾値を逆算する」実例（Penn EWS）と、PPV の逆数 NNE・100入院あたりの警報率を報告する提案がある。
- 理論面では、コスト比から校正済み確率の閾値を直接決める式（Elkan）、net benefit による閾値帯評価（DCA）、有限標本で偽警報率を保証する Learn then Test、時系列向けの重み付き共形リスク制御がある。
- 車載 FCW では、早い警報ほど nuisance が増え、受容が下がる。大型トラックの RSS ベース評価で偽警報率 11.19%（近接で30%超）との抜粋がある。
- 見つからなかったもの: 離散時間ハザードの連続確率から「走行時間あたりの警報率上限」を保証して閾値を選ぶ直接研究（車載・医療とも）。CAN のみの事故予兆でハザード校正を扱った研究も未発見である。
- 効く層: L3（R4）、L4、L6。

## 2. 主要知見

### 2.1 稀少事象・高打ち切り下の校正評価（サブ論点1）

各項目は検索抜粋のみ。事象率・打ち切り率は抜粋に記載がないものが大半で、記載がある場合のみ書く。

1. **An Effective Meaningful Way to Evaluate Survival Models**（著者不明、2023、arXiv）https://arxiv.org/pdf/2306.01196
   - 事実: 高打ち切りでは IPCW 統合 Brier が、遅い時点の少数の非打ち切り例に支配され分散が増えるとの要約。
   - 示唆: 【推察】稀少事象では IBS 単独は不安定で、重み分布の報告と bootstrap 区間が要る。
2. **Good Rankings, Wrong Probabilities: A Calibration Audit of Multimodal Cancer Survival Models**（Ghawami、2026、arXiv）https://arxiv.org/pdf/2604.04239
   - 事実: 時刻別 1-calibration 検定 290 件中 166 件が BH 補正後も棄却。離散時間出力の実験 A は 15 件中 12 件棄却。Platt 補正で順位を損なわず改善。BRCA で打ち切り 85%、IPCW が有効標本を 52〜68% に減らすとの記述は要約間で揺れがあり未検証。
   - 示唆: 【推察】C-index が良い離散時間ハザードでも、閾値設定の前に事後校正（Platt・isotonic）が要る。対象は医療で、運転データは未検証。
3. **When Are Scoring Rules Proper? / Examining marginal properness…**（Sonabend ら、2022〜、arXiv）https://arxiv.org/pdf/2212.05260
   - 事実: IBS と RCLL は理論上 improper だが、著者のシミュレーションでは proper として振る舞った。
   - 示唆: 【推察】相対比較には使えるが、閾値判断には校正曲線を併用する。
4. **Proper Scoring Rules for Survival Analysis**（Yanagisawa、ICML 2023）https://proceedings.mlr.press/v202/yanagisawa23a.html
   - 事実: 対数スコアの拡張が strictly proper と証明され、Brier・RPS の拡張（Cen-log、Cen-Brier）を与える。IBS・C-index 系の不適切性を指摘。
   - 示唆: 【推察】打ち切り分布の推定を要さない評価・損失の候補。
5. **Effective Ways to Build and Evaluate Individual Survival Distributions**（Haider ら、JMLR 2020、D-calibration）https://ar5iv.labs.arxiv.org/html/1811.11347
   - 事実: 予測確率の一様性を χ² 検定し、打ち切り例は予測生存後の確率区間に「ぼかして」配分する。
   - 示唆: 【推察】事象が極少だと打ち切り分が支配的になり検出力が落ちうる。
6. **X-CAL: Explicit Calibration for Survival Analysis**（Goldstein ら、NeurIPS 2020）https://www.arxiv.org/pdf/2101.05346
   - 事実: D-calibration を微分可能にし正則化項として使う。識別性能・尤度を大きく落とさず D-calibration が改善。
   - 示唆: 【推察】離散時間ハザードの損失への追加候補。
7. **Conformalized Survival Distributions（CSD）**（ICML 2024）https://arxiv.org/pdf/2405.07374
   - 事実: 事後処理で校正を改善し識別性能を保つ。打ち切りの条件付き独立を仮定し、4種の打ち切り処理を持つ。
   - 示唆: 【推察】CAN の観測窓が打ち切りと共変量に依存する場合、仮定の検証が要る。
8. **Toward Conditional Distribution Calibration in Survival Prediction**（2024、arXiv）https://arxiv.org/abs/2410.20579v3
   - 事実: D-calibration のぼかしを基にした条件付き校正指標を提案し、15データセットで実験。
   - 示唆: 【推察】道路種別・速度帯などの部分集団ごとの校正確認に向く。
9. **Deep Learning-Based Discrete Calibrated Survival Prediction（DCS）**（Fuhlert ら、2022）https://arxiv.org/pdf/2208.08182
   - 事実: 3つの医療データで離散時間モデルのうち最良の校正。出力ノード間隔を可変にし、打ち切り・非打ち切り双方を使う損失項を加える。
   - 示唆: 【推察】稀少事象では時間ビン幅の不均一化が有効な可能性がある。
10. **Graphical calibration curves and the integrated calibration index（ICI）for survival models**（Austin, Harrell, van Klaveren、2020、Stat Med）https://repub.eur.nl/pub/129441/Repub_129441_O-A.pdf
    - 事実: 適応型ハザード回帰や制限3次スプラインで校正曲線を作り、ICI・E50・E90 を定義。
    - 示唆: 【推察】固定ホライズンの校正プロットの標準手順になる。
11. **Administrative Brier score（pycox ノートブック）** https://nbviewer.jupyter.org/github/havakv/pycox/blob/master/examples/administrative_brier_score.ipynb
    - 事実: 打ち切り分布の推定を要さない。pycox のシミュレーションで IPCW が手法を誤って順位づけた例を示す。打ち切り時刻が共変量から識別できる場合は IPCW が無効。
    - 示唆: 【推察】走行単位の固定観測窓（管理的打ち切り）なら有力。

### 2.2 確率出力から警告閾値への変換（サブ論点2）

12. **Penn EWS（ML敗血症アラート）**（Critical Care Medicine、2019頃）https://pmc.ncbi.nlm.nih.gov/articles/PMC6791738
    - 事実: 感度閾値を病院全体で約10件/日になるよう事前設定（前版は約6件/日）。362件のアンケートで新しい臨床所見を得たとした割合は看護師24%・医師13%。PMC番号と論文の対応は文脈からの推定。
    - 示唆: 【推察】ワークロード上限から閾値を逆算する固定警報率運用の実例。走行時間あたりの警報許容回数から閾値を決める設計が成立しうる。
13. **Early Warning Systems: The Neglected Importance of Timing**（J Hosp Med 論説、年不明）https://www.mdedge.com/jhospmed/article/202628/hospital-medicine/early-warning-systems-neglected-importance-timing/page/0/1
    - 事実: PPV が低いと alert fatigue が増える。早期検知とリードタイムはトレードオフ。評価単位を入院でなく patient-hour／15分エポックにすべきと提案。
    - 示唆: 【推察】秒・フレーム単位の離散時間ハザードの警報率・PPV 評価の根拠。
14. **Epic Sepsis Model の外部検証**（Wong ら、JAMA Intern Med 2021。二次報道経由）https://www.healthcareitnews.com/news/research-suggests-epic-sepsis-model-lacking-predictive-power
    - 事実: 入院単位 AUC 0.63（社内資料 0.76〜0.83）。閾値6以上の警報が入院の約18%に発報されたが、敗血症の67%を見逃した。論文本文は未確認。
    - 示唆: 【推察】ベンダー既定閾値のままでは警報率が想定を外れる。導入先データで再校正し、警報率・NNE で検証する。
15. **臨床悪化予測アルゴリズムのスコーピングレビュー**（Peelen ら、年不明）https://pmc.ncbi.nlm.nih.gov/articles/PMC10167173
    - 事実: NNE は PPV の逆数（PPV 20% = NNE 5）。警報率は100入院・日あたりで表し閾値で調整できる。導入前評価では AUROC より PPV・NNE・警報率を報告すべきと主張。重み付き平均有病率 3.0%。PMC番号がレビュー本体かは断定できない。
    - 示唆: 【推察】警報KPIを「感度＋走行時間あたり警報率＋NNE」で一組にする根拠。有病率依存のため走行環境別の層別が要る。
16. **Decision Curve Analysis**（Vickers & Elkin 2006）https://pmc.ncbi.nlm.nih.gov/articles/PMC2577036
    - 事実: net benefit = TP/n − FP/n × pt/(1−pt)。単一閾値でなく妥当な閾値範囲で評価する。
    - 示唆: 【推察】pt を「偽警報コスト:見逃しコスト」比として明示でき、全警報／無警報との比較ができる。ハザードの校正が前提。
17. **The Foundations of Cost-Sensitive Learning**（Elkan、IJCAI 2001）https://mlanthology.org/ijcai/2001/elkan2001ijcai-foundations
    - 事実: 最適閾値はコスト比で決まり0.5とは限らない。確率が校正済みであることに依存する。式本体は未取得。
    - 示唆: 【推察】校正が崩れるとコスト比由来の閾値も崩れる。B-24 の接点。
18. **Learn then Test**（Angelopoulos ら、arXiv 2110.01052）https://arxiv.org/pdf/2110.01052
    - 事実: リスク制御を多重仮説検定として扱い、FWER 制御で有限標本のリスク保証を持つ閾値集合を出力。単調性を仮定しない。
    - 示唆: 【推察】警報率・偽警報割合の上限を保証して閾値を選ぶ標準枠組み。保守的になりうる。
19. **Adaptive Learn-then-Test**（Zecchin ら、ICML 2025）https://arxiv.org/abs/2409.15844v2
    - 事実: e-process による逐次・適応検定で LTT 並みの性能を検定ラウンドの一部で得る。評価対象は RL・プロンプト選択。
    - 示唆: 【推察】候補閾値が多い場合の効率化。時系列警報には未検証。
20. **Conformal early warning systems**（arXiv 2109.14082）https://arxiv.org/pdf/2109.14082v5
    - 事実: 目標の偽陰性率 ε を約 1/ε 件のデータで保証する形で警報を調整。逐次時系列設定ではないとの注記。
21. **Non-Exchangeable Conformal Risk Control**（arXiv 2310.01262）https://arxiv.org/pdf/2310.01262
    - 事実: 校正点を新しいほど重く重み付けして時系列へ拡張。標準法は目標リスクを超えうるが、重み付き版は平均的に満たす。
    - 示唆（20・21）: 【推察】走行データは非交換可能で、走行単位のブロック化や重み付けが要る。
22. **On Continuous Monitoring of Risk Violations under Unknown Shift**（UAI 2025）https://arxiv.org/pdf/2506.16416
    - 事実: 候補閾値ごとの逐次検定で、偽警報保証は「各閾値について時間方向」に成立し、全閾値同時ではない。
    - 示唆: 【推察】運用中のシフト監視と閾値再選択では、保証の範囲の違いに注意する。
23. **生存モデルでの閾値校正**（arXiv 2512.18118、著者・年不明）https://arxiv.org/pdf/2512.18118v2
    - 事実: 高確率リスク制御と FDR 制御を比較し、校正データで事象率推定と閾値選択を兼ねる「二重使用」を警告、データ分割を推奨。
    - 示唆: 【推察】本テーマに直結する可能性が高いが本文未確認。I-01 解消後に精読する。

### 2.3 車載 FCW の警報閾値

24. **FCW 警報タイミングと nuisance alarm（複数文献）** https://informahealthcare.com/doi/abs/10.1080/15389588.2014.928703 ほか（同ドメイン10.1080/15389588.2019.1623397、https://doaj.org/article/75d0af3188d848728de804f89b29972b。書誌は未確定）
    - 事実: 早く保守的な警報ほど不要警報が増え、不信・OFF 化につながる。テストトラックでは早い警報は受容が低く、遅い警報は反応が速かった。2024年の大型トラック研究（RSS 使用）で偽警報率 11.19%、近接車間で30%超。多段階警報で受容・信頼が高い研究もある。
    - 示唆: 【推察】単一閾値でなく注意／警告の二段階と、ドライバー別・状況別の適応が選択肢。CAN のみでは適応に使える特徴が限られる。
- 補足（件数外）: A-TTC（2026、個別化トラック FCW、後ろ向きで nuisance 警報割合 13.74%・脅威 recall 89.25%、マルチモーダル入力）は抜粋で確認したが、URL が大学ページ経由のため載せない。PHM Society の予知保全の閾値コスト最適化論文群も、個別の書誌が確定できなかったため載せない。

## 3. 統合アーキテクチャ（12）への反映点

- L3（R4 リスク推定）: 離散時間ハザード出力に、事後校正（Platt・isotonic、CSD）と校正曲線／ICI の評価を必須にする。
- L4（警告判断）: 閾値は、走行時間あたりの警報許容回数（Penn 型の固定警報率）またはコスト比（Elkan・DCA）から逆算する。校正が前提。
- L6（検証）: KPI を「感度＋走行100時間あたり警報率＋NNE」で報告する。評価単位は走行時間窓にする。閾値選択は Learn then Test や重み付き共形で、走行単位ブロックのデータ分割を使う。
- 運用: シフト下の閾値再選択は、時間方向と閾値方向の保証の違いを設計書に明記する。

## 4. 課題・ギャップ

- 離散時間ハザードの連続確率から、走行時間あたり警報率の上限を保証して閾値を選ぶ直接研究は見つからなかった。
- 全て抜粋のみで、事象率・打ち切り率の記載がほとんど取れていない。完了条件（各研究の事象率明記）は未達である。
- 日本語資料は今回調べていない（「警報閾値 誤報率」「早期警戒スコア アラート疲労」等が候補）。
- 警報の再発報抑制（refractory period）と警報率の関係は未調査である。

## 5. 次のアクション提案

1. I-01 解消後に 2512.18118、2604.04239、2306.01196 を本文で確認し、事象率・打ち切り率を表にする。
2. 合成データまたは公開データ（comma2k19 系など）で、離散時間ハザード＋Platt／CSD＋Learn then Test の閾値選択を試す設計書を作る（設計タスク I-11 に紐づけ）。
3. 日本語の警報疲労・予知保全閾値の文献を調べる（新規バックログ化）。
4. 再発報抑制と警報率の関係を調べる（新規バックログ化）。

## 6. 参考文献リスト

2.1〜2.3 の各項目に記載した URL（24件）が参考文献である。いずれも WebSearch の結果に URL が現れたもので、本文は未読。
題名・URLのみで内容を確認できず件数外としたもの: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11785332/ 、https://arxiv.org/pdf/2507.02807
