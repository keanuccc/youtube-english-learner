/* Content script: floating button on YouTube video pages */

(function () {
  "use strict";

  if (document.getElementById("yt-english-learner-btn")) return;

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
    btn.style.background = "";
    text.textContent = "Learn English";
  }

  // Send message to background script (avoids CORS issues)
  function sendMessage(msg) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(msg, resolve);
    });
  }

  btn.addEventListener("click", async () => {
    const url = window.location.href;

    btn.classList.add("loading");
    setProgress(5, "Connecting...");

    // Simulated progress stages
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
      const health = await sendMessage({ action: "health" });
      if (!health.ok) throw new Error("offline");

      // Generate PDF
      const result = await sendMessage({ action: "generate", url });

      timers.forEach(clearTimeout);

      if (!result.ok) {
        setProgress(100, result.data?.error || "Failed");
        btn.style.background = "#dc2626";
        doneTimer = setTimeout(resetBtn, 3000);
        return;
      }

      // Success — show count and trigger download
      const data = result.data;
      setProgress(100, `${data.pair_count} sentences`);
      btn.style.background = "#16a34a";

      sendMessage({ action: "download", filename: data.pdf });
      doneTimer = setTimeout(resetBtn, 3000);

    } catch (e) {
      timers.forEach(clearTimeout);
      setProgress(100, "Backend offline");
      btn.style.background = "#dc2626";
      doneTimer = setTimeout(resetBtn, 3000);
    }
  });
})();
