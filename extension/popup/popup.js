// Default API - Railway production
const DEFAULT_API = "https://web-production-e7326.up.railway.app";

let API = DEFAULT_API;

const $ = (sel) => document.querySelector(sel);

// ========== Load API URL from storage ==========
async function loadApiUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["apiUrl"], (result) => {
      if (result.apiUrl) {
        API = result.apiUrl;
        $("#api-url-input").value = result.apiUrl;
      }
      resolve();
    });
  });
}

// ========== Save API URL ==========
async function saveApiUrl() {
  const url = $("#api-url-input").value.trim().replace(/\/+$/, ""); // strip trailing slash
  if (!url) return;

  API = url || DEFAULT_API;
  chrome.storage.sync.set({ apiUrl: API });

  const statusEl = $("#api-status");
  try {
    const resp = await fetch(`${API}/api/health`);
    if (resp.ok) {
      statusEl.className = "api-status ok";
      statusEl.textContent = "✓ Connected";
    } else throw new Error();
  } catch {
    statusEl.className = "api-status err";
    statusEl.textContent = "✗ Cannot reach server";
  }
}

// ========== Detect current tab URL ==========
async function detectCurrentVideo() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.url && tab.url.includes("youtube.com/watch")) {
      $("#url-input").value = tab.url;
    }
  } catch (e) {
    // Not in extension context
  }
}

// ========== API health check ==========
async function checkHealth() {
  try {
    const resp = await fetch(`${API}/api/health`);
    if (!resp.ok) throw new Error();
    return true;
  } catch {
    showStatus("error", "❌",
      API.includes("localhost")
        ? "Backend not running. Start with: <b>python server.py</b>"
        : "Cannot reach backend. Check Settings ⚙️"
    );
    return false;
  }
}

// ========== Generate PDF ==========
async function generate() {
  const url = $("#url-input").value.trim();
  if (!url) {
    showStatus("error", "⚠️", "Please paste a YouTube URL");
    return;
  }

  if (!(await checkHealth())) return;

  $("#result").classList.add("hidden");
  $("#generate-btn").disabled = true;
  showStatus("loading", "", '<span class="spinner"></span> Extracting subtitles...');

  try {
    const resp = await fetch(`${API}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await resp.json();

    if (!resp.ok) {
      showStatus("error", "❌", data.error || "Generation failed");
      return;
    }

    showStatus("success", "✅", "PDF generated successfully!");
    $("#result").classList.remove("hidden");
    $("#result-title").textContent = data.title;
    $("#result-meta").textContent = `${data.channel}  ·  ${data.pair_count} sentences  ·  ${data.word_count} words`;
    $("#download-btn").dataset.filename = data.pdf;

    loadHistory();

  } catch (e) {
    showStatus("error", "❌", "Connection failed. Check Settings ⚙️");
  } finally {
    $("#generate-btn").disabled = false;
  }
}

// ========== Download PDF ==========
function download() {
  const filename = $("#download-btn").dataset.filename;
  if (filename) {
    chrome.tabs.create({ url: `${API}/api/download/${filename}` });
  }
}

// ========== Show status ==========
function showStatus(type, icon, text) {
  const el = $("#status");
  el.className = `status ${type === "loading" ? "" : type}`;
  $("#status-icon").innerHTML = icon;
  $("#status-text").innerHTML = text;
  el.classList.remove("hidden");
}

// ========== Load history ==========
async function loadHistory() {
  const container = $("#history");
  try {
    const resp = await fetch(`${API}/api/history`);
    const items = await resp.json();

    if (!items.length) {
      container.innerHTML = '<div class="history-empty">No PDFs yet</div>';
      return;
    }

    container.innerHTML = items.map(item => `
      <div class="history-item">
        <span class="history-icon">📄</span>
        <div class="history-info">
          <div class="history-name" title="${item.name}">${item.name}</div>
          <div class="history-meta">${item.time}  ·  ${item.size} KB</div>
        </div>
      </div>
    `).join("");
  } catch {
    container.innerHTML = '<div class="history-empty">Backend offline</div>';
  }
}

// ========== Init ==========
document.addEventListener("DOMContentLoaded", async () => {
  await loadApiUrl();

  detectCurrentVideo();
  loadHistory();

  $("#generate-btn").addEventListener("click", generate);
  $("#download-btn").addEventListener("click", download);
  $("#detect-btn").addEventListener("click", detectCurrentVideo);
  $("#save-api-btn").addEventListener("click", saveApiUrl);

  // Toggle settings
  $("#settings-toggle").addEventListener("click", () => {
    $("#settings").classList.toggle("hidden");
  });

  // Enter key triggers
  $("#url-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") generate();
  });
  $("#api-url-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") saveApiUrl();
  });
});
