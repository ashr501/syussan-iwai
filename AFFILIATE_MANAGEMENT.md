# アフィリエイトリンク一括管理メモ

商品リンクは `js/affiliate-config.js` で管理します。

## まず編集する場所

```js
window.HONNE_AFFILIATE_CONFIG = {
  site: {
    canonicalDomain: "https://example.com",
  },
  stores: {
    amazon: {
      associateTag: "YOUR_TAG"
    }
  }
}
```

## Amazon

AmazonアソシエイトのトラッキングIDが発行されたら、ここに入れます。

```js
amazon: {
  associateTag: "honnecatalog-22"
}
```

`products.html` のAmazonボタンは、各商品の検索URLに `tag=` を自動付与します。

## 楽天

楽天の公式リンク作成画面で商品ごとに発行したURLを、下記の `products` に登録します。未発行のURLを推測して作らないでください。検索リンクは収益化されません。

## Yahoo / ValueCommerceなど

ASPで提携承認後、そのプログラムのリンク作成画面から発行したURLを商品別に登録します。契約前にURLラップ形式を自作しないでください。

## 商品ごとに個別URLを指定したい場合

`products` に `data-affiliate-slot` の番号で指定します。

```js
products: {
  "696": {
    amazon: "https://www.amazon.co.jp/dp/XXXXXXXX/?tag=honnecatalog-22",
    rakuten: "https://hb.afl.rakuten.co.jp/...",
    yahoo: "https://ck.jp.ap.valuecommerce.com/...",
    official: "https://example.com/product"
  }
}
```

個別URLがある商品は検索URLより優先されます。

## 運用ルール

- 設定済みの広告リンクには `rel="sponsored noopener"`、通常のショップ検索リンクには `rel="noopener"` が入ります。
- 商品価格・在庫は遷移先で確認してもらう前提です。
- 広告リンクが1件でも有効になったら、サイト冒頭と対象のSNS投稿に明瞭な「広告・PR」表記を入れます。
- `canonicalDomain` は現在 `https://honne-catalog.com` です。

## 申請順序

1. サイトURLとSNSの公開プロフィールを確定し、プライバシーポリシー・連絡先・広告表示を整える。
2. 楽天アフィリエイトでサイト情報を登録し、公式のリンク作成画面から商品ごとのURLを発行する。
3. Amazonアソシエイトを申請する。申請後180日以内に3件以上の適格販売が必要で、Amazonがサイトを審査する。
4. Yahoo等はASPで該当プログラムへ提携申請し、承認後に発行リンクを設定する。
5. `products` にURLを登録し、実際に遷移と計測を確認してから広告表示を公開する。

申請時の氏名、住所、振込先、税務情報、規約同意はサイト所有者が確認して入力してください。IDや決済情報はリポジトリに保存しません。
