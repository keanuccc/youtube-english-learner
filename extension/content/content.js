/* Content script: floating button on YouTube video pages */

(function () {
  "use strict";

  const DEFAULT_API = "http://localhost:5000";
  let API = DEFAULT_API;

  // Don't inject twice
  if (document.getElementById("yt-english-learner-btn")) return;

  // Load API URL from storage
  function loadApiUrl() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(["apiUrl"], (result) => {
        if (result.apiUrl) API = result.apiUrl;
        resolve();
      });
    });
  }

  // Create floating button
  const btn = document.createElement("button");
  btn.id = "yt-english-learner-btn";
  btn.innerHTML = '<span class="icon">📚</span> Learn English';
  btn.title = "Generate bilingual PDF from this video";
  document.body.appendChild(btn);

  btn.addEventListener("click", async () => {
    const url = window.location.href;

    btn.innerHTML = '<span class="icon">⏳</span> Processing...';
    btn.classList.add("loading");

    await loadApiUrl();

    try {
      // Health check
      const health = await fetch(`${API}/api/health`);
      if (!health.ok) throw new Error("offline");

      // Generate
      const resp = await fetch(`${API}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await resp.json();

      if (!resp.ok) {
        btn.innerHTML = `<span class="icon">❌</span> ${data.error || "Failed"}`;
        setTimeout(() => resetBtn(), 3000);
        return;
      }

      // Download
      btn.innerHTML = `<span class="icon">✅</span> ${data.pair_count} sentences`;
      window.open(`${API}/api/download/${data.pdf}`, "_blank");
      setTimeout(() => resetBtn(), 3000);

    } catch (e) {
      btn.innerHTML = '<span class="icon">⚠️</span> Backend offline';
      setTimeout(() => resetBtn(), 3000);
    }
  });

  function resetBtn() {
    btn.innerHTML = '<span class="icon">📚</span> Learn English';
    btn.classList.remove("loading");
  }
})();
