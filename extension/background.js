/*
 * Background service worker
 * All API calls go through here to avoid CORS issues from content scripts
 */

const DEFAULT_API = "http://localhost:5000";

function getApiUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["apiUrl"], (result) => {
      resolve(result.apiUrl || DEFAULT_API);
    });
  });
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
    getApiUrl().then((base) => {
      fetch(`${base}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: msg.url }),
        signal: AbortSignal.timeout(120000),
      })
        .then((r) => r.json().then((data) => sendResponse({ ok: r.ok, data })))
        .catch((e) => sendResponse({ ok: false, data: { error: e.message } }));
    }).catch((e) => sendResponse({ ok: false, data: { error: e.message } }));
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
