/*
  Google Analytics 4 loader
  -------------------------
  GA4の測定IDが発行されたら MEASUREMENT_ID に入れるだけで全ページ有効になります。
  例: var MEASUREMENT_ID = "G-XXXXXXXXXX";
*/
(function () {
  var MEASUREMENT_ID = "";
  if (!MEASUREMENT_ID) return;

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", MEASUREMENT_ID);
})();
