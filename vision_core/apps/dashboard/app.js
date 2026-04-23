async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

const historyState = {
  page: 1,
  pageSize: 5,
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setPre(id, data) {
  document.getElementById(id).textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

function setSummary(data) {
  const target = document.getElementById("summaryOut");
  target.innerHTML = `
    <div class="pill">STATUS: ${escapeHtml(data.status)}</div>
    <div class="pill">MISSION_ID: ${escapeHtml(data.mission_id)}</div>
    <div class="pill">ROOT_CAUSE: ${escapeHtml(data.root_cause)}</div>
    <div class="pill">VALIDATION: ${escapeHtml(data.validation)}</div>
    <div class="pill">PASS_GOLD: ${escapeHtml(data.pass_gold)}</div>
    <div class="pill">PROMOTION_ALLOWED: ${escapeHtml(data.promotion_allowed)}</div>
    <div class="pill">APPLIED_FILES: ${escapeHtml(data.applied_files)}</div>
    <div class="pill">SNAPSHOT_ID: ${escapeHtml(data.snapshot_id)}</div>
  `;
}

function renderCheck(item) {
  const klass = item.passed ? "status-ok" : "status-bad";
  const badge = item.passed ? "PASS" : "BLOCK";
  return `
    <li class="${klass}">
      <strong>${escapeHtml(item.name)}</strong>
      <span class="pill ${klass}">${badge}</span>
      <div>${escapeHtml(item.detail)}</div>
    </li>
  `;
}

function setIntegrationPayload(payload) {
  const target = document.getElementById("integrationOut");
  const integration = payload?.integration || payload || {};
  const pr = integration.pr_validation || {};
  const gh = integration.github || {};
  const codex = integration.codex || {};
  const debug = payload?.github_debug || integration.metadata?.debug || gh.metadata?.debug || {};
  const checks = Array.isArray(pr.checks) ? pr.checks.map(renderCheck).join("") : "";

  target.innerHTML = `
    <div class="pill">INTEGRATION_STATUS: ${escapeHtml(integration.status ?? payload?.status ?? "-")}</div>
    <div class="pill">PR_VALIDATION: ${escapeHtml(pr.status ?? "-")}</div>
    <div class="pill">MERGE_ALLOWED: ${escapeHtml(pr.merge_allowed ?? "-")}</div>
    <div class="pill">GITHUB_STATUS: ${escapeHtml(gh.status ?? "-")}</div>
    <div class="pill">ERROR_CLASS: ${escapeHtml(gh.error_class ?? "-")}</div>
    <div class="pill">ATTEMPTS: ${escapeHtml(gh.attempts ?? "-")}</div>
    <div class="pill">PUSH_PERFORMED: ${escapeHtml(gh.push_performed ?? "-")}</div>
    <div class="pill">REUSED_PR: ${escapeHtml(gh.reused_pull_request ?? "-")}</div>
    <div class="pill">AUTO_MERGE_ATTEMPTED: ${escapeHtml(gh.auto_merge_attempted ?? "-")}</div>
    <div class="pill">AUTO_MERGE_COMPLETED: ${escapeHtml(gh.auto_merge_completed ?? "-")}</div>
    <div class="pill">CODEX_BUNDLE: ${escapeHtml(codex.bundle_path ?? "-")}</div>
    <div class="list-block">
      <div><strong>GitHub branch:</strong> ${escapeHtml(gh.branch ?? "-")}</div>
      <div><strong>Commit SHA:</strong> ${escapeHtml(gh.commit_sha ?? "-")}</div>
      <div><strong>PR URL:</strong> ${escapeHtml(gh.pr_url ?? "-")}</div>
      <div><strong>Reason:</strong> ${escapeHtml(gh.reason ?? codex.reason ?? "-")}</div>
      <div><strong>Repo root:</strong> ${escapeHtml(debug.repository_root ?? "-")}</div>
      <div><strong>Base branch:</strong> ${escapeHtml(debug.base_branch ?? "-")}</div>
      <div><strong>Max API attempts:</strong> ${escapeHtml(debug.max_api_attempts ?? "-")}</div>
    </div>
    <ul class="check-list">${checks || "<li>No checks</li>"}</ul>
  `;
}

function setDiffs(diffs) {
  const target = document.getElementById("diffsOut");
  if (!Array.isArray(diffs) || !diffs.length) {
    target.innerHTML = '<div class="empty">No diffs generated.</div>';
    return;
  }

  target.innerHTML = diffs.map((item) => `
    <article class="diff-card">
      <div class="diff-title">${escapeHtml(item.target_file)}</div>
      <pre>${escapeHtml(item.diff_text)}</pre>
    </article>
  `).join("");
}

function setHistory(payload) {
  const target = document.getElementById("historyOut");
  const meta = document.getElementById("historyMeta");
  const items = payload?.items || [];
  const pagination = payload?.pagination || {};

  if (!Array.isArray(items) || !items.length) {
    target.innerHTML = '<div class="empty">No integration history yet.</div>';
    meta.innerHTML = '<div class="empty">Page 1 of 1 · 0 items</div>';
    return;
  }

  meta.innerHTML = `
    <div class="pill">PAGE: ${escapeHtml(pagination.page)}</div>
    <div class="pill">PAGE_SIZE: ${escapeHtml(pagination.page_size)}</div>
    <div class="pill">TOTAL_ITEMS: ${escapeHtml(pagination.total_items)}</div>
    <div class="pill">TOTAL_PAGES: ${escapeHtml(pagination.total_pages)}</div>
  `;

  target.innerHTML = items.map((item) => {
    const gh = item?.integration?.github || {};
    const pr = item?.integration?.pr_validation || {};
    return `
      <article class="diff-card">
        <div class="diff-title">${escapeHtml(item.recorded_at)} — ${escapeHtml(item.mission_id)}</div>
        <div class="pill">STATUS: ${escapeHtml(item.status)}</div>
        <div class="pill">GITHUB: ${escapeHtml(gh.status ?? "-")}</div>
        <div class="pill">ERROR_CLASS: ${escapeHtml(gh.error_class ?? "-")}</div>
        <div class="pill">ATTEMPTS: ${escapeHtml(gh.attempts ?? "-")}</div>
        <div class="pill">MERGE_ALLOWED: ${escapeHtml(pr.merge_allowed ?? "-")}</div>
        <div class="list-block">
          <div><strong>Mission:</strong> ${escapeHtml(item?.summary?.mission ?? "-")}</div>
          <div><strong>Decision:</strong> ${escapeHtml(item?.summary?.decision ?? "-")}</div>
          <div><strong>PR:</strong> ${escapeHtml(gh.pr_url ?? "-")}</div>
          <div><strong>Reason:</strong> ${escapeHtml(gh.reason ?? "-")}</div>
        </div>
      </article>
    `;
  }).join("");
}

async function loadHealth() {
  try {
    const data = await api("/api/health");
    setPre("healthOut", data);
  } catch (err) {
    setPre("healthOut", String(err));
  }
}

async function loadLastIntegration() {
  try {
    const data = await api("/api/integration/last");
    setIntegrationPayload(data);
    setDiffs(data.diffs || []);
  } catch (err) {
    document.getElementById("integrationOut").innerHTML = `<div class="status-bad">${escapeHtml(String(err))}</div>`;
  }
}

async function loadIntegrationHistory(page = historyState.page) {
  try {
    const pageSizeInput = Number.parseInt(document.getElementById("historyPageSize").value, 10);
    if (Number.isFinite(pageSizeInput) && pageSizeInput > 0) {
      historyState.pageSize = pageSizeInput;
    }
    historyState.page = Math.max(1, page);
    const data = await api(`/api/integration/history?page=${encodeURIComponent(historyState.page)}&page_size=${encodeURIComponent(historyState.pageSize)}`);
    historyState.page = data?.pagination?.page || historyState.page;
    setHistory(data);
  } catch (err) {
    document.getElementById("historyOut").innerHTML = `<div class="status-bad">${escapeHtml(String(err))}</div>`;
  }
}

function nextHistoryPage() {
  loadIntegrationHistory(historyState.page + 1);
}

function prevHistoryPage() {
  loadIntegrationHistory(Math.max(1, historyState.page - 1));
}

async function runMission() {
  try {
    const mission = document.getElementById("missionText").value;
    const environment = document.getElementById("environment").value;
    const data = await api("/api/mission", {
      method: "POST",
      body: JSON.stringify({ mission, environment }),
    });
    setSummary(data);
    setIntegrationPayload(data.integration || {});
    setDiffs(data.diffs || []);
    setPre("stepsOut", data.steps);
    historyState.page = 1;
    await loadIntegrationHistory(1);
    if (data.snapshot_id) {
      document.getElementById("snapshotId").value = data.snapshot_id;
    }
    if (data.mission_id) {
      document.getElementById("memoryMissionId").value = data.mission_id;
    }
  } catch (err) {
    setSummary({ status: "FAIL", root_cause: "ui_request_failure" });
    document.getElementById("integrationOut").innerHTML = `<div class="status-bad">${escapeHtml(String(err))}</div>`;
    setDiffs([]);
    setPre("stepsOut", String(err));
  }
}

async function loadMemory() {
  try {
    const data = await api("/api/memory");
    setPre("memoryOut", data);
  } catch (err) {
    setPre("memoryOut", String(err));
  }
}

async function loadMemoryItem() {
  try {
    const missionId = document.getElementById("memoryMissionId").value;
    const data = await api(`/api/memory/${encodeURIComponent(missionId)}`);
    setPre("memoryOut", data);
  } catch (err) {
    setPre("memoryOut", String(err));
  }
}

async function rollbackSnapshot() {
  try {
    const snapshot_id = document.getElementById("snapshotId").value;
    const data = await api("/api/rollback", {
      method: "POST",
      body: JSON.stringify({ snapshot_id }),
    });
    setPre("rollbackOut", data);
  } catch (err) {
    setPre("rollbackOut", String(err));
  }
}

async function rollbackFile() {
  try {
    const snapshot_id = document.getElementById("snapshotId").value;
    const target_file = document.getElementById("targetFile").value;
    const data = await api("/api/rollback-file", {
      method: "POST",
      body: JSON.stringify({ snapshot_id, target_file }),
    });
    setPre("rollbackOut", data);
  } catch (err) {
    setPre("rollbackOut", String(err));
  }
}

loadHealth();
loadLastIntegration();
loadIntegrationHistory();
