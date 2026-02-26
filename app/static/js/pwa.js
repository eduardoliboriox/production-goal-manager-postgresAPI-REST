(function () {
  if (!("serviceWorker" in navigator)) return;

  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js", { scope: "/" })
      .then(function () {
        // Opcional: log útil no começo (pode remover depois)
        // console.log("Service Worker registered");
      })
      .catch(function () {
        // Opcional: log útil no começo (pode remover depois)
        // console.warn("Service Worker registration failed", err);
      });
  });
})();
