# 出産祝いの本音カタログ — 運用ルール

このリポジトリは GitHub Pages で https://honne-catalog.com/ として公開されている静的サイト。
mainにpushすると数分で本番に反映される。

## 必読ドキュメント

記事の作成・リライト・商品選定・SNS素材の作成を行う前に、必ず `AI_OPERATION_PROMPT.md` を読むこと。
編集方針(禁止表現・断定回避・固有フリマサービス名の禁止)、記事テンプレート(§6)、商品採点基準(§7)、
記事クラスタ(§9)はすべてそこに定義されている。このルールに反する記事は公開しない。

## サイト構成

- `index.html` / `products.html` / `onegai-list.html` / `about.html` / `privacy.html` — ルートページ
- `articles/*.html` — 記事(全ページ共通のヘッダー・フッター構造。新記事は既存記事をテンプレートにする)
- `js/affiliate-config.js` — アフィリエイトID・リンクテンプレートの一元管理(`AFFILIATE_MANAGEMENT.md` 参照)
- `js/analytics.js` — GA4ローダー(測定IDはこのファイルの `MEASUREMENT_ID` のみ)
- `scripts/` — 運用スクリプト(下記)

## 運用スクリプト

- `python3 scripts/update_sitemap.py` — articles/ とルートのHTMLを走査して sitemap.xml を再生成。記事を追加・削除したら必ず実行する
- `python3 scripts/check_links.py` — 全HTMLのリンク検査(内部リンク切れ、アフィリエイトリンクのHTTP到達性、`rel="sponsored"` 漏れ、広告表記漏れ)。レポートを標準出力に出す

## 記事を追加するときの手順

1. `AI_OPERATION_PROMPT.md` §9 のクラスタから未執筆テーマを選ぶ(優先順: 2人目 → 困ったもの → 嬉しかったもの → 内祝い)
2. 既存記事(例: `articles/second-child-gifts.html`)の構造をテンプレートに記事HTMLを作成
   - 広告表記、`rel="sponsored"`、著者・調査方法・更新日、目次、FAQ、内部リンクを必ず入れる
   - 禁止表現(顔文字・「いかがでしたか」・断定NG表現)に注意
3. 関連する既存記事から新記事への内部リンクを2〜3本追加
4. `python3 scripts/update_sitemap.py` を実行
5. `python3 scripts/check_links.py` でエラーがないことを確認
6. **draftブランチ(`draft/記事スラッグ`)にコミットしてpush**し、ユーザーの確認を待つ。mainへの直接公開はユーザーが明示的に許可した場合のみ
7. SNS素材(X投稿文・Pinterest画像案)を `docs/sns/記事スラッグ.md` に保存

## 禁止事項

- `js/affiliate-config.js` のID・テンプレートを推測で書き換えない(実IDはユーザーから受け取る)
- 広告表記・PR表記・`rel="sponsored"` を削除しない(ステマ規制対応)
- 公開記事に特定のフリマサービス名を書かない(「フリマサイト」と一般化する)
