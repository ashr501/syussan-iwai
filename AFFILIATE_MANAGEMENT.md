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

楽天アフィリエイトでリンクテンプレートを使う場合は、`affiliateUrlTemplate` に入れます。

```js
rakuten: {
  affiliateUrlTemplate: "https://hb.afl.rakuten.co.jp/hgc/YOUR_ID/?pc={url}&m={url}"
}
```

`{url}` は商品検索URL、`{query}` は商品名に自動置換されます。

## Yahoo / ValueCommerceなど

ASP側でURLラップ形式のテンプレートがある場合は、Yahoo側に入れます。

```js
yahoo: {
  affiliateUrlTemplate: "https://ck.jp.ap.valuecommerce.com/servlet/referral?sid=YOUR_SID&pid=YOUR_PID&vc_url={url}"
}
```

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

- 広告リンクには自動で `rel="sponsored noopener"` が入ります。
- 商品価格・在庫は遷移先で確認してもらう前提です。
- ステマ規制対応のため、広告表記は削除しないでください。
- 独自ドメインが決まったら `canonicalDomain` と `sitemap.xml` を更新します。
