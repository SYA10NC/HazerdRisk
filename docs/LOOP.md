# 自動調査ループ手順書

クラウドルーチンが毎回この手順に従って実行する。人が手動で回す場合も同じ手順でよい。

## 0. 準備
1. `CLAUDE.md`、`research/README.md`、`research/BACKLOG.md`、`research/LOG.md` の末尾10件を読む
2. `research/12_integrated_architecture.md` の「4. 統合参照アーキテクチャ」と「7. 未解決の論点」を読む
3. 今日の日付を `date -u +%Y-%m-%d` で取得する

## 1. 深掘り調査（1テーマ）
1. `research/BACKLOG.md` の「未着手」の先頭テーマを選ぶ
   - 未着手が空なら、既存レポートの「課題・ギャップ」「次のアクション提案」と `12` の「未解決の論点」から、まだ扱っていない論点を3件以上バックログに補充してから先頭を選ぶ
2. テーマをさらに2〜4個のサブ論点に分解する
3. サブ論点ごとにサブエージェント（Agent tool, general-purpose）を並列で立て、ゴールプロンプトで調査させる。ゴールプロンプトには必ず次を入れる
   - プロジェクト背景（CLAUDE.md の目的をそのまま渡す）
   - ゴール（何を明らかにするか）と調査範囲の例
   - 成果物の形（サブ論点ごとの知見リストを返答で返す。ファイルは書かせない）
   - 完了条件（ソース件数、URL 実在確認、【推察】の区別、日本語・英語両方の情報源）
4. サブエージェントの結果を統合し、`CLAUDE.md` の書式で `research/NN_<slug>.md` を1本書く
   - Agent tool が使えない場合は、自分で WebSearch / WebFetch を使って同じ内容を調査する

## 2. 最新動向ウォッチ
1. 直近7日程度の新着情報を WebSearch で探す。対象は次のとおり
   - arXiv などの新着論文（CAN、driver monitoring without camera、near-miss prediction、crash risk、ADAS safety、end-to-end autonomous driving safety など）
   - 公式発表（NHTSA、UNECE WP.29/GRVA、Euro NCAP、国交省、警察庁、自動車メーカー、Waymo・Tesla・Mobileye・Wayve・Woven by Toyota 等の自動運転企業）
2. 本プロジェクトに関係する3〜8件を `news/YYYY-MM.md`（当月のファイル。なければ作る）に追記する
   - 書式: `- YYYY-MM-DD [種別] タイトル — 要点1行 — 示唆1行 — URL`
   - 既に載っているURLは重複させない

## 3. 索引・状態の更新
1. `research/README.md` のファイル一覧に新ファイルを追記する。テーマ横断の要点を更新すべき知見があれば追記する
2. `research/BACKLOG.md`
   - 処理したテーマを「完了」に移し、日付とファイル名を付ける
   - 調査中に見つけた新しい論点を「未着手」の末尾に追加する（1回あたり最大3件）
3. 統合アーキテクチャ（12）を変えるべき重要な知見があれば、`12` の末尾に「## 更新履歴」節を作り（既にあればそこに）、日付と変更点を追記する
4. `research/LOG.md` に1行追記する
   - 書式: `- YYYY-MM-DD | NN_<slug>.md | ソースN件 | news M件 | 一言メモ`

## 4. コミット・push
1. `git add -A`
2. `git commit -m "docs(research): add NN_<slug> and news YYYY-MM-DD"`
3. `git pull --rebase origin main` の後、`git push origin main`
4. push に失敗した場合は、原因（権限・競合など）を `research/LOG.md` に書けないため、最終返答に明記して終了する

## 5. 最終返答
- 追加したファイル、ソース件数、主要知見（300字以内）、確認しきれなかった点、push の成否を返す
