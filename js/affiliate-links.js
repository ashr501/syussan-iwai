(function () {
  const config = window.HONNE_AFFILIATE_CONFIG;
  if (!config) return;

  const hasValue = (value) => typeof value === "string" && value.trim() !== "";

  const encode = (value) => encodeURIComponent(value || "");

  const applyTemplate = (template, destinationUrl, query) => {
    if (!hasValue(template)) return destinationUrl;
    return template
      .replaceAll("{url}", encode(destinationUrl))
      .replaceAll("{query}", encode(query));
  };

  const addParams = (url, params) => {
    const nextUrl = new URL(url);
    Object.entries(params || {}).forEach(([key, value]) => {
      if (hasValue(value)) nextUrl.searchParams.set(key, value);
    });
    return nextUrl.toString();
  };

  const makeSearchUrl = (storeKey, query) => {
    const store = config.stores && config.stores[storeKey];
    if (!store || store.enabled === false) return "";

    if (storeKey === "rakuten") {
      const base = store.searchUrl.endsWith("/") ? store.searchUrl : `${store.searchUrl}/`;
      const destination = `${base}${encode(query)}`;
      return applyTemplate(store.affiliateUrlTemplate, destination, query);
    }

    const destination = new URL(store.searchUrl);
    destination.searchParams.set(store.queryParam || "q", query);

    if (storeKey === "amazon" && hasValue(store.associateTag)) {
      destination.searchParams.set("tag", store.associateTag.trim());
    }

    const withParams = addParams(destination.toString(), store.extraParams);
    return applyTemplate(store.affiliateUrlTemplate, withParams, query);
  };

  const normalizeLink = (link) => {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "sponsored noopener");
    link.setAttribute("data-affiliate-managed", "true");
  };

  const replaceOfficialPlaceholder = (container, url) => {
    const current = container.querySelector(".store-button.muted");
    if (!current || !hasValue(url)) return;

    const link = document.createElement("a");
    link.className = current.className;
    link.href = url;
    link.textContent = current.textContent || "公式確認";
    normalizeLink(link);
    current.replaceWith(link);
  };

  document.querySelectorAll(".store-buttons[data-query]").forEach((container) => {
    const slot = container.dataset.affiliateSlot || "";
    const query = container.dataset.query || "";
    const overrides = (config.products && config.products[slot]) || {};

    ["amazon", "rakuten", "yahoo"].forEach((storeKey) => {
      const link = container.querySelector(`.store-button.${storeKey}`);
      if (!link) return;

      const url = overrides[storeKey] || makeSearchUrl(storeKey, query);
      if (!hasValue(url)) {
        link.hidden = true;
        return;
      }

      link.href = url;
      normalizeLink(link);
    });

    replaceOfficialPlaceholder(container, overrides.official);
  });

  document.querySelectorAll("[data-affiliate-disclosure]").forEach((node) => {
    node.textContent = config.site && config.site.disclosure ? config.site.disclosure : node.textContent;
  });
})();
