/*
 * Background service worker
 * All API calls go through here to avoid CORS issues from content scripts
 */

const DEFAULT_API = "https://web-production-e7326.up.railway.app";

function getApiUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["apiUrl"], (result) => {
      resolve(result.apiUrl || DEFAULT_API);
    });
  });
}

// Keep-alive mechanism for long-running requests
let keepAliveInterval = null;

function startKeepAlive() {
  if (keepAliveInterval) return;
  keepAliveInterval = setInterval(() => {
    // Send a message to keep the service worker alive
    chrome.runtime.getPlatformInfo(() => {});
  }, 20000); // Every 20 seconds
}

function stopKeepAlive() {
  if (keepAliveInterval) {
    clearInterval(keepAliveInterval);
    keepAliveInterval = null;
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  // Health check
  if (msg.action === "health") {
    getApiUrl().then((base) => {
      fetch(`${base}/api/health`, { signal: AbortSignal.timeout(5000) })
        .then((r) => sendResponse({ ok: r.ok }))
        .catch(() => sendResponse({ ok: false }));
    }).catch(() => sendResponse({ ok: false }));
    return true;
  }

  // Generate PDF
  if (msg.action === "generate") {
    startKeepAlive(); // Keep service worker alive during long request
    getApiUrl().then((base) => {
      fetch(`${base}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: msg.url }),
        signal: AbortSignal.timeout(180000), // Extended to 3 minutes
      })
        .then((r) => {
          stopKeepAlive();
          return r.json().then((data) => sendResponse({ ok: r.ok, data }));
        })
        .catch((e) => {
          stopKeepAlive();
          sendResponse({ ok: false, data: { error: e.message } });
        });
    }).catch((e) => {
      stopKeepAlive();
      sendResponse({ ok: false, data: { error: e.message } });
    });
    return true;
  }

  // Download PDF (opens new tab)
  if (msg.action === "download") {
    getApiUrl().then((base) => {
      const url = `${base}/api/download/${encodeURIComponent(msg.filename)}`;
      chrome.tabs.create({ url });
      sendResponse({ ok: true });
    }).catch(() => sendResponse({ ok: false }));
    return true;
  }
});
