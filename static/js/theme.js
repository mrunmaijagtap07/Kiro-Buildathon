/**
 * theme.js — Light/dark mode management.
 *
 * Inline script in <head> prevents flash of incorrect theme.
 * This module handles toggle interaction and persistence.
 */

const THEME_KEY = "ca-theme";

function getStoredTheme() {
  try { return localStorage.getItem(THEME_KEY); } catch { return null; }
}

function setStoredTheme(theme) {
  try { localStorage.setItem(THEME_KEY, theme); } catch {}
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  // Update all toggle button icons
  document.querySelectorAll(".theme-toggle").forEach(btn => {
    btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    btn.querySelector(".theme-icon-sun")?.classList.toggle("hidden", theme !== "dark");
    btn.querySelector(".theme-icon-moon")?.classList.toggle("hidden", theme === "dark");
  });
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next    = current === "dark" ? "light" : "dark";
  applyTheme(next);
  setStoredTheme(next);
}

// Initialize on DOMContentLoaded (theme was already applied inline in <head>)
document.addEventListener("DOMContentLoaded", () => {
  const stored = getStoredTheme();
  const theme  = stored || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  applyTheme(theme);

  document.querySelectorAll(".theme-toggle").forEach(btn => {
    btn.addEventListener("click", toggleTheme);
  });
});

// Export for inline <head> use
window.CA_initTheme = function() {
  const stored = getStoredTheme();
  const theme  = stored || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
};
