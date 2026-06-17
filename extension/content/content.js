/* Content script: floating button on YouTube video pages */

(function () {
  "use strict";

  const DEFAULT_API = "http://localhost:5000";
  let API = DEFAULT_API;

  if (document.getElementById("yt-english-learner-btn")) return;

  function loadApiUrl() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(["apiUrl"], (result) => {
        if (result.apiUrl) API = result.apiUrl;
        resolve();
      });
    });
  }

  // Create button with progress bar
  const btn = document.createElement("button");
  btn.id = "yt-english-learner-btn";
  btn.innerHTML = `
    <div class="progress-bar"></div>
    <span class="btn-text">Learn English</span>
  `;
  btn.title = "Generate bilingual PDF from this video";
  document.body.appendChild(btn);

  const bar = btn.querySelector(".progress-bar");
  const text = btn.querySelector(".btn-text");

  let doneTimer = null;

  function setProgress(pct, label) {
    bar.style.width = pct + "%";
    if (label) text.textContent = label;
  }

  function resetBtn() {
    clearTimeout(doneTimer);
    btn.classList.remove("loading");
    bar.style.width = "0%";
    text.textContent = "Learn English";
  }

  btn.addEventListener("click", async () => {
    const url = window.location.href;

    btn.classList.add("loading");
    setProgress(5, "Connecting...");

    await loadApiUrl();

    // Simulated progress stages (advance while waiting for response)
    const stages = [
      [15,  "Extracting subtitles...", 4000],
      [40,  "Translating...",          8000],
      [70,  "Still translating...",    16000],
      [85,  "Generating PDF...",       24000],
    ];
    const timers = stages.map(([pct, label, delay]) =>
      setTimeout(() => setProgress(pct, label), delay)
    );

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

      // Clear simulated stages
      timers.forEach(clearTimeout);

      const data = await resp.json();

      if (!resp.ok) {
        setProgress(100, data.error || "Failed");
        btn.style.background = "#dc2626";
        doneTimer = setTimeout(() => {
          btn.style.background = "";
          resetBtn();
        }, 3000);
        return;
      }

      // Success
      setProgress(100, `${data.pair_count} sentences`);
      btn.style.background = "#16a34a";
      window.open(`${API}/api/download/${data.pdf}`, "_blank");
      doneTimer = setTimeout(() => {
        btn.style.background = "";
        resetBtn();
      }, 3000);

    } catch (e) {
      timers.forEach(clearTimeout);
      setProgress(100, "Backend offline");
      btn.style.background = "#dc2626";
      doneTimer = setTimeout(() => {
        btn.style.background = "";
        resetBtn();
      }, 3000);
    }
  });
})();
