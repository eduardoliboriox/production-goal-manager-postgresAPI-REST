/* Venttos SMT Service Worker (safe by default)
   - Cacheia somente assets estáticos
   - Não cacheia HTML
*/

const CACHE_VERSION = "venttos-smt-v1";
const STATIC_CACHE = `${CACHE_VERSION}-static`;

const STATIC_ASSETS = [
  "/offline",
  "/static/css/style.css",
  "/static/js/main.js",
  "/static/js/pcp.js",
  "/static/js/pwa.js",
  "/static/images/logos/icon-logo-mobile.png",
  "/static/images/logos/pwa-192.png",
  "/static/images/logos/pwa-512.png",
  "/static/images/logos/pwa-512-maskable.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((k) => k.startsWith("venttos-smt-") && k !== STATIC_CACHE)
          .map((k) => caches.delete(k))
      );
      await self.clients.claim();
    })()
  );
});

// Cache-first para assets estáticos
async function cacheFirst(req) {
  const cached = await caches.match(req);
  if (cached) return cached;

  const res = await fetch(req);
  const cache = await caches.open(STATIC_CACHE);
  cache.put(req, res.clone());
  return res;
}

// Network-first (com fallback offline) só para navegação
async function navigationNetworkFirst(req) {
  try {
    return await fetch(req);
  } catch (e) {
    const offline = await caches.match("/offline");
    return offline || new Response("Offline", { status: 503 });
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.method !== "GET") return;
  if (url.origin !== self.location.origin) return;

  // Navegação (HTML)
  if (req.mode === "navigate") {
    event.respondWith(navigationNetworkFirst(req));
    return;
  }

  // Assets estáticos
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(cacheFirst(req));
    return;
  }

  // SW e manifest: rede com fallback no cache
  if (url.pathname === "/sw.js" || url.pathname === "/manifest.webmanifest") {
    event.respondWith(
      (async () => {
        try {
          return await fetch(req);
        } catch (e) {
          const cached = await caches.match(req);
          return cached || new Response("", { status: 503 });
        }
      })()
    );
  }
});
