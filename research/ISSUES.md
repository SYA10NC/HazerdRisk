# 調査の問題点とタスク

調査の進め方や既存レポートの問題点をタスクとして管理する。自動調査ループは毎回このファイルを読み、手順 3 で状態を更新する（docs/LOOP.md）。

- 状態: `未対応` / `対応中` / `完了 YYYY-MM-DD` / `要オーナー対応`（環境設定など、ループでは直せないもの）
- 種別: `環境` / `プロセス` / `品質` / `重複` / `設計`（調査ではなく設計・実装の作業）
- 調査で解く必要がある問題は BACKLOG.md のテーマ（B-xx）に紐づけ、ここでは追跡だけを行う

棚卸し日: 2026-11-01（01〜13、news、ルーチン設定を確認。`python3 scripts/sources_index.py --dups` の結果を含む）

## 未対応・対応中

### I-01 [環境] WebFetch が多くのホストで名前解決に失敗する — 要オーナー対応
- 事実: 2026-11-01 の実行で、arxiv.org、waymo.com、mobileye.com、tesla.com、global.toyota、pressroom.toyota.com、woven.toyota、docs.autoware.org、autowarefoundation.github.io、blog.comma.ai、techcrunch.com、bloomberg.com、automotiveworld.com などで `getaddrinfo ENOTFOUND` になった。github.com は読めた
- 影響: 13 のソース28件のうち、本文を読めたのは GitHub の README 等の一部だけで、残りは検索結果の抜粋のみ。news の arXiv 新着も取れていない
- 対処: クラウド環境の Network access で、上記ホストを Allowed domains に追加するか、より広いアクセスレベルにする（https://code.claude.com/docs/en/cloud-environments#network-access）
- 完了条件: 上記ホストで WebFetch が成功する。その後 B-15 で 13 の本文再確認を行う

### I-03 [環境] ルーチンの実行時刻が名前・設定書と食い違う — 要オーナー対応
- 事実: ルーチン名と docs/ROUTINE_PROMPT.md は「毎日 06:00 JST（cron `0 21 * * *` UTC）」だが、実際のスケジュールは `CRON_TZ=Asia/Tokyo 0 4 * * *`（毎日 04:00 JST）である
- 対処: どちらに合わせるかをオーナーが決める。決まったらルーチンか ROUTINE_PROMPT.md を直す

### I-04 [重複] 13 が既存レポートと同じ論点・ソースを再調査した — 対策実施、効果確認中
- 事実:
  - 13 は 07 の Toyota Guardian [1]・RSS [9]・openpilot 安全モデル [19]、11 の openpilot（§6.1）・Autoware（§6.2）と論点が重なる
  - 13 が新規ソースとして載せた URL のうち 6 件は既出だった（waymo.com/safety/impact=04、tesla safety-score=06、comma ブログ=07、SAE 2026-01-0520=08、opendbc=03/11、openpilot SAFETY.md=11）
  - 原因: サブエージェントへのゴールプロンプトに「既存調査で扱い済みの論点」を渡しておらず、既出URLの照合もしていなかった
- 対策（2026-11-01 実施）:
  - 論点の網羅表 research/COVERAGE.md を作成
  - BACKLOG の各テーマにゴールプロンプトと「扱い済み（調べない）」欄を付けた
  - 既出URL索引 research/SOURCES.md と照合スクリプト scripts/sources_index.py を追加
  - docs/LOOP.md に重複チェック手順を追加
- 完了条件: 次回以降の 2 回の実行で、新規ファイルの「新規ソース」に既出URLが混ざらないこと

### I-05 [品質] 13 の次のアクション「RSS 式を arXiv 1708.06374 で照合」は 07 で既出 — 完了 2026-11-01
- 07 の [9] がすでに arXiv:1708.06374 を扱っている。13 に【訂正】を追記した。式そのものの照合（d_min の各項）は B-15 で 07 [9] を起点に行う

### I-06 [プロセス] 日付の不整合 — 完了 2026-11-01（訂正追記）
- README・BACKLOG・LOG は第2弾（07〜12）を 2026-11-02 としているが、各ファイルの調査日は 2026-11-01 であり、2026-11-01 時点で未来の日付になっている。README と LOG に【訂正】を追記した
- 再発防止: LOOP.md 手順 0 で `date -u +%Y-%m-%d` を取り、その値だけを使う（既存の手順どおり）

### I-07 [プロセス] BACKLOG の番号に欠番・空行があり、テーマにゴールが書かれていない — 完了 2026-11-01
- 15 番が欠け、16・17 の前に空行があった。各テーマは1行の題名だけで、サブエージェントに渡すゴール・範囲・除外が毎回その場の作文になっていた
- BACKLOG.md を B-xx 形式に作り直し、テーマごとにゴールプロンプトを置いた（題名の文言はすべて残した）

### I-08 [品質] news の最新動向ウォッチがほぼ機能していない — 未対応

- 2026-11-01 の news は 4 件で、すべて検索抜粋ベースの報道。arXiv 新着・NHTSA・UNECE・Euro NCAP・国交省の一次発表は取れていない
- 原因: I-01（arXiv・公式サイトの WebFetch 不可）と、検索クエリが毎回その場の作文であること
- 対処: docs/LOOP.md 手順 2 に固定の検索クエリ表を追加した（2026-11-01）。I-01 解消後に効果を確認する

### I-09 [品質] 13 のソースに二次報道・ベンダー宣伝・個人ブログが多い — 未対応
- 例: CSDN 個人ブログ（S3）、Apex.AI のベンダー紹介（S26）、Drive Tesla Canada・The Autopian の二次報道（S22・S23）。Wayve の安全アーキテクチャは一次資料が見つかっていない
- 対処: B-15 で一次資料に置き換えるか、一次資料が無い旨を明記する

### I-10 [品質] ソース件数の数え方がファイルごとに違う — 未対応
- README の件数表記は「29件、うち論文21件」「参考文献48項目、うちデータセット20種」など基準がまちまち。13 は補足URL（S11・S16・S19）も1件に数えている
- 対処: 今後は「本文確認済み／抜粋のみ／既出の再掲」の3区分で件数を書く（LOOP.md 手順 1 に追記した）。既存ファイルは触らず、README に注記する

### I-11 [設計] 統合アーキテクチャ（12）への具体設計の反映が溜まっている — 未対応（調査ループの対象外）
- 13 の「入力健全性 DAG・可用性ベクトル・警告の単調エスカレート／ラッチ」（旧 BACKLOG 17）
- 07〜11 の次のアクションにある試作・ベンチマーク（縦RSS のオフライン検証、comma2k19 での同一条件ベンチマーク、KPI 定義書、シャドーモードの偽警報ベンチマーク、openpilot 縮小構成での試作）
- これらは調査ではなく設計・実装の作業なので、自動調査ループでは扱わない。人が着手するときにこの項目を分割する

### I-12 [品質] B-01（14）は全ソースが検索抜粋のみで、数値が未検証 — 未対応（I-01 依存）
- 事実: 2026-11-01 の実行でも arxiv.org への WebFetch が名前解決に失敗した（I-01 継続）。14 の38件はすべて抜粋のみ
- 対処: I-01 解消後に B-16 で主要6件の本文確認を行う

### I-25 [環境] I-01 継続: unece.org・eur-lex.europa.eu・www.mlit.go.jp・nhtsa.gov も WebFetch 不可 — 要オーナー対応
- 事実: 2026-11-12 の実行で arxiv.org・unece.org・eur-lex.europa.eu・www.mlit.go.jp が ENOTFOUND。25 は全て抜粋のみ
- 対処: 上記ホストを許可ドメインに追加（I-01 に統合してよい）

## 完了

- I-02 [環境] main への push が 403（Claude GitHub App の権限なし）— 完了 2026-11-01。オーナーが権限を直し、同日の再 push が成功した（commit d256ae2）

## 追記 2026-11-02
- I-01 継続: 2026-11-02 も arxiv.org に加え govinfo.gov・iihs.org・ncbi.nlm.nih.gov・erieinsurance.com 等が WebFetch 不可。15 の本文確認は 0 件。要オーナー対応
- I-03 継続: 今回の起動は 2026-11-02 19:15 UTC（04:15 JST ではなく 04:15 相当の食い違い未解消。ルーチン名は毎日6時JST）

### I-12 [環境] 2026-11-03 の実行でも arxiv.org・csselectronics.com・blog.comma.ai・wikipedia・isobus.net・youcanic.com が WebFetch 不可
- 事実: 名前解決に失敗。github.com と raw.githubusercontent.com は取得できた。I-01 の対処（Allowed domains 追加）が未実施
- 影響: 16 の抜粋のみ 6 件、AEBS の PGN/SPN 未確認（B-17）。状態: 要オーナー対応

### I-13 [プロセス] 15 までの「ファイルを書くとき BACKLOG の旧テーマ定義を消さない」運用
- 事実: B-03 を完了に移す際、定義を要約して「完了」欄に残した（CLAUDE.md の削除禁止に配慮）。LOOP.md に「完了へ移すときは元定義を要約して残す」と明記するとよい。状態: 未対応

### I-14 [環境] 2026-11-04 も vtechworks・mlit.go.jp・saemobilus・cir.nii.ac.jp・onlinepubs.trb.org・arxiv.org が WebFetch 不可
- 事実: 名前解決に失敗。17 の全ソース24件が検索抜粋のみ。SHRP2 トリガ表は確定できず（B-19）。状態: 要オーナー対応（I-01 と同根）

### I-15 [プロセス] サブエージェント間で同一文献を別 URL で返す重複
- 事実: 17 の調査で、Sudweeks・Perez 2017・SWOV 書誌ページ・Chalmers が複数エージェントから返り、さらに Sudweeks・Perez は 05 の既出文献だった（URL が異なるため sources_index.py は NEW と判定）。対策案: URL だけでなく著者・題名でも照合する。状態: 未対応

### I-16 [環境] 2026-11-05 実行でも WebFetch 不可（I-01 継続）
- 事実: arxiv.org に加え、mlit.go.jp、saemobilus.sae.org、patents.google.com、unece.org、toyota.jp、cdn.euroncap.com、nhtsa.gov、jstage.jst.go.jp 等で名前解決に失敗。18 の全ソースが抜粋のみ。B-15・B-16・B-19・B-20 は前提未達で着手不可。状態: 要オーナー対応（I-01 と同じ）

### I-17 [環境] 2026-11-06 実行でも WebFetch 不可（I-01 継続）
- 事実: arxiv.org に加え vtechworks・ugpti.org・pref.aichi.jp・jama.or.jp・scilit.net・sciencegate.app で名前解決に失敗。19 の全18件が抜粋のみ。状態: 要オーナー対応（I-01 と同じ）

### I-18 [品質] 19 の一部ソースは著者・年・正規URLが未特定
- 事実: S2（図書館カタログ）、SAE 論文2件（test ホストURL）、愛知県PDF（対象特定未了）。次回、原典特定が要る。状態: 未対応

### I-19 [環境] 2026-11-07 実行でも WebFetch 不可（I-01 継続）
- arxiv.org・blog.comma.ai・monoist.itmedia.co.jp が名前解決に失敗。20 は全34件が抜粋のみ。B-20（I-01 解消後）は前提未達のため見送り。

### I-20 [環境] 2026-11-08 実行でも WebFetch 不可（I-01 継続）
- arxiv.org・docs.comma.ai・preprints.org・jstage.jst.go.jp が名前解決に失敗。21 は全31件が抜粋のみ。B-20（I-01 前提）は見送り。状態: 要オーナー対応

### I-21 [品質] 21 の一部ソースは題名・著者・URL対応が未確定
- 事実: 21 の [29]（tjsai）・[30]（jsceiii）は検索要約依存で、論文との対応が未確定。次回、本文または書誌で特定が要る

### I-22 [環境] 2026-11-09 実行でも WebFetch 不可（I-01 継続）
- arxiv.org・pmc/ncbi・cir.nii.ac.jp・jstage.jst.go.jp・c2smarter 等が名前解決に失敗。22 は全27件が抜粋のみ。B-20 は前提未達で見送り。状態: 要オーナー対応

### I-23 [品質] 22 の一部ソースは題名・著者・年が未特定
- [S4][S5][S6][S9][S14] と [S8] の図書館カタログURL。次回、書誌の特定が要る。状態: 未対応

### I-24 [環境] 2026-11-10 実行でも WebFetch 不可（I-01 継続）
- arxiv.org・iihs.org・pmc/ncbi・jstage・www8.cao.go.jp・rosap.ntl.bts.gov・medinform.jmir.org が名前解決に失敗（セッションの許可ドメイン外）。23 は全34件が抜粋のみ。B-20 は前提未達で見送り。状態: 要オーナー対応（上記ホストの許可）

### I-25 [品質] 23 の一部ソースは書誌・対応URLが未確定
- [S25]（高齢者RF判別0.859）、[S19] の原論文、[S21] の論文対応、[S30]、[S34] 等。数値は暫定。次回、書誌の特定が要る。状態: 未対応

### I-26 [環境] 2026-11-11 実行でも WebFetch 不可（I-01 継続）
- arxiv.org・www.mlit.go.jp・www.mhlw.go.jp・www.fmcsa.dot.gov・isobus.net・csselectronics.com 等が名前解決に失敗。24 は全29件が抜粋のみ。また GitHub MCP は本リポジトリ以外を読めず、公開 j1939 DBC を直接確認できなかった。状態: 要オーナー対応（I-01 と同じ）

### I-27 [品質] 24 の一部ソースは版・年が未特定
- 保安基準告示 S151.pdf の版、厚労省 0912-2d の題名・年、事故調査委員会 001326946 が個別報告か、FMCSA の数値の出典表。数値は暫定。状態: 未対応

