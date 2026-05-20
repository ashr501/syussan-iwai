# 独自ドメイン運用メモ

このサイトは GitHub Pages のまま、通常の独自ドメインで公開できます。

## 結論

このサイトは `honne-catalog.com` で公開します。GitHub Pages の Custom domain とDNSを設定すれば、`ashr501.github.io/syussan-iwai/` ではなく `https://honne-catalog.com/` で表示できます。

## やること

1. GitHub のリポジトリ設定で Pages の Custom domain に `honne-catalog.com` を入れる
2. リポジトリ直下に `CNAME` ファイルを置き、`honne-catalog.com` を1行だけ書く
3. お名前.comでDNSを設定する
4. GitHub Pages 側で HTTPS を有効にする
5. Search Console、Analytics、ASPのサイトURLを独自ドメインに変更する

## DNSの考え方

### ルートドメインで運用する場合

対象：`honne-catalog.com`

お名前.comのDNSレコードに次のAレコードを設定します。

```txt
TYPE: A
HOST: @ または空欄
VALUE:
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

IPv6も使う場合は、AAAAレコードも設定します。

```txt
TYPE: AAAA
HOST: @ または空欄
VALUE:
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

### wwwも使う場合

`www.honne-catalog.com` も使う場合は、追加でCNAMEを設定します。

```txt
TYPE: CNAME
HOST: www
VALUE: ashr501.github.io
```

GitHub Pages側の Custom domain は `honne-catalog.com` にして、GitHubの自動リダイレクトに任せます。

## このサイトでの設定

- `CNAME`: `honne-catalog.com`
- `sitemap.xml`: `https://honne-catalog.com/` に更新済み
- `js/affiliate-config.js`: `canonicalDomain` を `https://honne-catalog.com` に更新済み

## 注意

- DNS反映には最大24時間程度かかることがあります
- GitHub側にドメインを登録する前にDNSだけ向けると、サブドメイン乗っ取りリスクがあります
- GitHub公式ドキュメントでは、事前にカスタムドメインを検証することが推奨されています
- ワイルドカードDNS（`*.example.com`）は避けます
- GitHub Pages は静的サイト向きです。商品カード、記事、アフィリエイトリンクの運用には向いています。一方で、会員機能、購入カート、在庫同期、フォーム送信などを本格的にやる場合は、ShopifyやWordPress、または外部サービスとの連携が必要です
