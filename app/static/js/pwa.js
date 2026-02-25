// Registro do Service Worker (PWA)
(function () {
  if (!("serviceWorker" in navigator)) return;

  window.addEventListener("load", async () => {
    try {
      // Importante: /service-worker.js (raiz) para controlar todo o site
      await navigator.serviceWorker.register("/service-worker.js");
    } catch (err) {
      // Sem logs verbosos em produção
      // console.warn("SW registration failed", err);
    }
  });
})();
