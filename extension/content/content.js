/* Content script: floating button on YouTube video pages */

(function () {
  "use strict";

  if (document.getElementById("yt-english-learner-btn")) return;

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

  // Send message to background script via Promise
  function sendMessage(msg) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(msg, (response) => {
          if (chrome.runtime.lastError) {
            const err = chrome.runtime.lastError.message;
            if (err.includes("invalidated")) {
              setProgress(100, "Please refresh this page");
              btn.style.background = "#f59e0b";
              doneTimer = setTimeout(resetBtn, 3000);
            }
            reject(new Error(err));
          } else {
            resolve(response);
          }
        });
      } catch (e) {
        reject(e);
      }
    });
  }

  btn.addEventListener("click", async () => {
    const url = window.location.href;

    btn.classList.add("loading");
    setProgress(5, "Connecting...");

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
      if (!health || !health.ok) throw new Error("offline");

      // Generate PDF
      const result = await sendMessage({ action: "generate", url });

      timers.forEach(clearTimeout);

      if (!result || !result.ok) {
        const errMsg = result?.data?.error || "Generation failed";
        setProgress(100, errMsg);
        btn.style.background = "#dc2626";
        doneTimer = setTimeout(resetBtn, 4000);
        return;
      }

      // Success
      const data = result.data;
      setProgress(100, `${data.pair_count} sentences`);
      btn.style.background = "#16a34a";

      // Trigger download via background script
      sendMessage({ action: "download", filename: data.pdf }).catch(() => {});
      doneTimer = setTimeout(resetBtn, 3000);

    } catch (e) {
      timers.forEach(clearTimeout);
      console.error("YT English Learner error:", e);
      setProgress(100, "Backend offline");
      btn.style.background = "#dc2626";
      doneTimer = setTimeout(resetBtn, 4000);
    }
  });
})();
