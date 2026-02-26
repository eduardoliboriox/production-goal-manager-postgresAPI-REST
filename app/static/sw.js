/* Venttos SMT Service Worker (safe by default)
   - Cacheia somente assets estáticos essenciais
   - Não cacheia HTML
   - Instala mesmo se 1 asset falhar (evita quebrar o PWA por 404)
*/

const CACHE_VERSION = "venttos-smt-v2";
const STATIC_CACHE = `${CACHE_VERSION}-static`;

// Mantenha essa lista MINIMAL e com arquivos 100% existentes
const STATIC_ASSETS = [
  "/offline",
  "/static/css/style.css",
  "/static/js/pwa.js",

  // ícones do PWA
  "/static/images/logos/pwa-192.png",
  "/static/images/logos/pwa-512.png",
  "/static/images/logos/pwa-512-maskable.png",
  "/static/images/logos/icon-logo-mobile.png"
];

// Faz cache “best-effort”: não falha a instalação se algum asset der erro
async function addAllBestEffort(cache, urls) {
  const results = await Promise.allSettled(
    urls.map(async (url) => {
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error(`${url} -> ${res.status}`);
      await cache.put(url, res);
    })
  );

  // Opcional: log (útil em devtools do SW)
  // results.forEach((r, i) => {
  //   if (r.status === "rejected") console.warn("SW cache fail:", urls[i], r.reason);
  // });

  return results;
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(STATIC_CACHE);
      await addAllBestEffort(cache, STATIC_ASSETS);
      await self.skipWaiting();
    })()
  );
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

// Network-first com fallback no offline para navegação
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

  // Manifest e SW: sempre rede (com fallback no cache)
  if (url.pathname === "/sw.js" || url.pathname === "/manifest.webmanifest") {
    event.respondWith(
      (async () => {
        try {
          return await fetch(req, { cache: "no-store" });
        } catch (e) {
          const cached = await caches.match(req);
          return cached || new Response("", { status: 503 });
        }
      })()
    );
  }
});
