/*
  Affiliate link settings
  -----------------------
  Edit this file when affiliate accounts or custom domain details are ready.
  The product page reads this config and updates store buttons automatically.
*/
window.HONNE_AFFILIATE_CONFIG = {
  site: {
    canonicalDomain: "",
    disclosure:
      "当サイトはアフィリエイト広告を利用しています。掲載商品は編集方針に基づき選定し、購入リンクの一部から収益を得る場合があります。"
  },

  stores: {
    amazon: {
      enabled: true,
      associateTag: "", // Example: honnecatalog-22
      searchUrl: "https://www.amazon.co.jp/s",
      queryParam: "k",
      extraParams: {}
    },
    rakuten: {
      enabled: true,
      searchUrl: "https://search.rakuten.co.jp/search/mall/",
      /*
        Paste a Rakuten Affiliate URL template when available.
        Supported placeholders:
        - {url}: encoded destination URL
        - {query}: encoded product query
        Example:
        "https://hb.afl.rakuten.co.jp/hgc/YOUR_ID/?pc={url}&m={url}"
      */
      affiliateUrlTemplate: ""
    },
    yahoo: {
      enabled: true,
      searchUrl: "https://shopping.yahoo.co.jp/search",
      queryParam: "p",
      /*
        Use this for ValueCommerce / other ASP templates if needed.
        Supported placeholders:
        - {url}: encoded destination URL
        - {query}: encoded product query
      */
      affiliateUrlTemplate: ""
    }
  },

  /*
    Optional product-specific overrides.
    Key is data-affiliate-slot from products.html.

    Example:
    products: {
      "696": {
        amazon: "https://www.amazon.co.jp/dp/XXXXXXXX/?tag=honnecatalog-22",
        rakuten: "https://hb.afl.rakuten.co.jp/...",
        yahoo: "https://ck.jp.ap.valuecommerce.com/...",
        official: "https://example.com/product"
      }
    }
  */
  products: {}
};
