/*
 * Background service worker
 * Handles all API calls on behalf of popup and content scripts
 * (avoids CORS issues from content script running on youtube.com)
 */

const DEFAULT_API = "http://localhost:5000";

async function getApiUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["apiUrl"], (result) => {
      resolve(result.apiUrl || DEFAULT_API);
    });
  });
}

async function apiFetch(path, options = {}) {
  const base = await getApiUrl();
  const resp = await fetch(`${base}${path}`, options);
  return resp.json();
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "health") {
    getApiUrl().then((base) =>
      fetch(`${base}/api/health`)
        .then((r) => sendResponse({ ok: r.ok }))
        .catch(() => sendResponse({ ok: false }))
    );
    return true; // async
  }

  if (msg.action === "generate") {
    getApiUrl().then((base) =>
      fetch(`${base}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: msg.url }),
      })
        .then((r) => r.json().then((data) => sendResponse({ ok: r.ok, data })))
        .catch((e) => sendResponse({ ok: false, data: { error: e.message } }))
    );
    return true;
  }

  if (msg.action === "download") {
    getApiUrl().then((base) => {
      const downloadUrl = `${base}/api/download/${encodeURIComponent(msg.filename)}`;
      chrome.tabs.create({ url: downloadUrl });
      sendResponse({ ok: true });
    });
    return true;
  }
});
