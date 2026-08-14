/**
 * main.js — Shared UI utilities: toasts, modals, sidebar,
 *           alert dismissal, AJAX helpers.
 */

"use strict";

// ── Toast notifications ────────────────────────────────────

function showToast(message, type = "info", duration = 4000) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }

  const icons = {
    success: "OK",
    danger:  "×",
    warning: "!",
    info:    "i",
  };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || "i"}</span>
    <span class="toast-message">${escapeHtml(message)}</span>
    <button class="btn btn-ghost btn-icon btn-sm toast-close" aria-label="Dismiss">×</button>
  `;

  toast.querySelector(".toast-close").addEventListener("click", () => dismissToast(toast));
  container.appendChild(toast);

  if (duration > 0) setTimeout(() => dismissToast(toast), duration);
}

function dismissToast(toast) {
  toast.style.opacity = "0";
  toast.style.transform = "translateX(20px)";
  toast.style.transition = "opacity .2s, transform .2s";
  setTimeout(() => toast.remove(), 220);
}

// ── Modals ─────────────────────────────────────────────────

function openModal(id) {
  const overlay = document.getElementById(id);
  if (!overlay) return;
  overlay.classList.add("open");
  overlay.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  overlay.querySelector("[autofocus]")?.focus();
}

function closeModal(id) {
  const overlay = document.getElementById(id);
  if (!overlay) return;
  overlay.classList.remove("open");
  overlay.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

// ── Confirm dialog ─────────────────────────────────────────

function confirmAction(message) {
  return window.confirm(message);
}

// ── HTML escaping ──────────────────────────────────────────

function escapeHtml(str) {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

// ── AJAX helpers ───────────────────────────────────────────

async function apiPost(url, data = {}) {
  const resp = await fetch(url, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(data),
  });
  return resp.json();
}

async function apiGet(url) {
  const resp = await fetch(url);
  return resp.json();
}

// ── DOM ready ──────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {

  // Alert dismiss
  document.querySelectorAll(".alert-close").forEach(btn => {
    btn.addEventListener("click", () => btn.closest(".alert")?.remove());
  });

  // Auto-dismiss flash alerts after 6s
  document.querySelectorAll(".alert[data-auto-dismiss]").forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity .4s";
      alert.style.opacity    = "0";
      setTimeout(() => alert.remove(), 420);
    }, 6000);
  });

  // Modal: close on overlay click
  document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", e => {
      if (e.target === overlay) closeModal(overlay.id);
    });
  });

  // Modal: close on Escape
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-overlay.open").forEach(o => closeModal(o.id));
    }
  });

  // Modal open triggers
  document.querySelectorAll("[data-modal-open]").forEach(btn => {
    btn.addEventListener("click", () => openModal(btn.dataset.modalOpen));
  });

  // Modal close triggers
  document.querySelectorAll("[data-modal-close]").forEach(btn => {
    btn.addEventListener("click", () => closeModal(btn.dataset.modalClose));
  });

  // Sidebar toggle (mobile)
  const sidebarToggle  = document.querySelector(".sidebar-toggle");
  const sidebar        = document.querySelector(".sidebar");
  const sidebarOverlay = document.querySelector(".sidebar-overlay");

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      sidebarOverlay?.classList.toggle("visible");
    });
    sidebarOverlay?.addEventListener("click", () => {
      sidebar.classList.remove("open");
      sidebarOverlay.classList.remove("visible");
    });
  }

  // File upload label updates
  document.querySelectorAll(".file-upload").forEach(zone => {
    const input   = zone.querySelector("input[type=file]");
    const nameEl  = zone.querySelector(".file-upload-name");
    if (!input) return;
    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", () => {
      if (nameEl && input.files[0]) {
        nameEl.textContent = input.files[0].name;
      }
    });
    // Drag-and-drop
    zone.addEventListener("dragover", e => { e.preventDefault(); zone.style.borderColor = "var(--color-primary)"; });
    zone.addEventListener("dragleave", () => { zone.style.borderColor = ""; });
    zone.addEventListener("drop", e => {
      e.preventDefault();
      zone.style.borderColor = "";
      if (e.dataTransfer.files[0]) {
        input.files = e.dataTransfer.files;
        if (nameEl) nameEl.textContent = e.dataTransfer.files[0].name;
      }
    });
  });

  // Toggle buttons that POST via fetch
  document.querySelectorAll("[data-toggle-url]").forEach(btn => {
    btn.addEventListener("click", async () => {
      if (!confirmAction(btn.dataset.confirm || "Are you sure?")) return;
      btn.disabled = true;
      try {
        const result = await apiPost(btn.dataset.toggleUrl);
        if (result.success) {
          showToast(result.message, "success");
          setTimeout(() => location.reload(), 800);
        } else {
          showToast(result.message || "An error occurred.", "danger");
          btn.disabled = false;
        }
      } catch {
        showToast("Network error. Please try again.", "danger");
        btn.disabled = false;
      }
    });
  });

});

// Expose for inline use
window.showToast  = showToast;
window.openModal  = openModal;
window.closeModal = closeModal;
