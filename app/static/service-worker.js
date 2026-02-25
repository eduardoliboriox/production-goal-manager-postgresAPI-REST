/* Venttos SMT - Service Worker (simple + safe)
   - Cache básico de "app shell"
   - Fallback offline para uma página simples
   - Estratégias:
     * Navegação (HTML): network-first com fallback
     * Assets estáticos (css/js/img/font): cache-first
*/

const CACHE_VERSION = "v1";
const CACHE_NAME = `venttos-smt-${CACHE_VERSION}`;

const APP_SHELL = [
  "/",
  "/dashboard",
  "/static/css/style.css",
  "/static/js/pwa.js",
  "/static/images/logos/icon-logo-mobile.png",
  "/static/images/logos/pwa-192.png",
  "/static/images/logos/pwa-512.png",
  "/static/images/logos/pwa-512-maskable.png",
  "/offline"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k.startsWith("venttos-smt-") && k !== CACHE_NAME)
          .map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

function isNavigationRequest(request) {
  return request.mode === "navigate" || (request.headers.get("accept") || "").includes("text/html");
}

function isStaticAsset(url) {
  return (
    url.pathname.startsWith("/static/") &&
    (url.pathname.endsWith(".css") ||
      url.pathname.endsWith(".js") ||
      url.pathname.endsWith(".png") ||
      url.pathname.endsWith(".jpg") ||
      url.pathname.endsWith(".jpeg") ||
      url.pathname.endsWith(".svg") ||
      url.pathname.endsWith(".webp") ||
      url.pathname.endsWith(".woff2"))
  );
}

self.addEventListener("fetch", (event) => {
  const request = event.request;

  // Só GET
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Apenas mesmo domínio
  if (url.origin !== self.location.origin) return;

  // HTML: network-first
  if (isNavigationRequest(request)) {
    event.respondWith(
      fetch(request)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return resp;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          return cached || caches.match("/offline");
        })
    );
    return;
  }

  // Assets estáticos: cache-first
  if (isStaticAsset(url)) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;

        return fetch(request).then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return resp;
        });
      })
    );
  }
});
