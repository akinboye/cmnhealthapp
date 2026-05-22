/**
 * CMN Health App — shared JS utility namespace
 * Loaded via base.html on every page.
 */
const App = (() => {
  // ─── Auth helpers ──────────────────────────────────────────────────────────

  function getToken() {
    return localStorage.getItem('cmn_token');
  }

  function getUser() {
    try { return JSON.parse(localStorage.getItem('cmn_user')) || {}; }
    catch { return {}; }
  }

  /**
   * Redirect to /login if no token.
   * Pass `adminOnly = true` to also redirect non-admins to /dashboard.
   */
  function requireAuth(adminOnly = false) {
    if (!getToken()) {
      window.location.href = (window.APP_BASE || '') + '/login';
      return;
    }
    if (adminOnly) {
      const user = getUser();
      if (!user.isAdmin) {
        window.location.href = (window.APP_BASE || '') + '/dashboard';
      }
    }
  }

  function logout() {
    localStorage.removeItem('cmn_token');
    localStorage.removeItem('cmn_user');
    window.location.href = (window.APP_BASE || '') + '/login';
  }

  // ─── API fetch wrapper ────────────────────────────────────────────────────

  /**
   * Fetch wrapper that injects Authorization header and
   * sets Content-Type to application/json for requests with a body.
   */
  function api(url, options = {}) {
    const token = getToken();
    const headers = { ...(options.headers || {}) };
    // Prepend the server subdirectory prefix (e.g. /healthapp) when present
    const base = window.APP_BASE || '';
    const fullUrl = url.startsWith('/') ? base + url : url;

    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (options.body && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    return fetch(fullUrl, { ...options, headers });
  }

  // ─── Sidebar ───────────────────────────────────────────────────────────────

  /**
   * Populate sidebar user info and mark the active nav link.
   * `activePage` should match the data-page attribute on <a> tags in sidebar.html
   */
  function initSidebar(activePage) {
    const user = getUser();

    // Fill user info
    const name  = `${user.firstName || ''} ${user.lastName || ''}`.trim() || 'User';
    const email = user.email || '';
    const initials = `${user.firstName?.charAt(0) || ''}${user.lastName?.charAt(0) || ''}`.toUpperCase() || '?';

    const avatarEl = document.getElementById('sidebar-avatar');
    const nameEl   = document.getElementById('sidebar-name');
    const emailEl  = document.getElementById('sidebar-email');
    if (avatarEl) avatarEl.textContent = initials;
    if (nameEl)   nameEl.textContent   = name;
    if (emailEl)  emailEl.textContent  = email;

    // Show admin nav section
    if (user.isAdmin) {
      const adminNav = document.getElementById('admin-nav');
      if (adminNav) adminNav.classList.remove('hidden');
    }

    // Mark active page
    if (activePage) {
      document.querySelectorAll('[data-page]').forEach(el => {
        if (el.getAttribute('data-page') === activePage) {
          el.classList.add('active');
        }
      });
    }
  }

  // ─── Toast notifications ───────────────────────────────────────────────────

  function toast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const colorMap = {
      success: 'bg-green-600',
      error:   'bg-red-600',
      info:    'bg-[#1E3A8A]',
      warning: 'bg-yellow-500',
    };
    const bg = colorMap[type] || colorMap.info;

    const el = document.createElement('div');
    el.className = `${bg} text-white text-sm font-medium px-4 py-3 rounded-xl shadow-lg flex items-center gap-2 transform transition-all duration-300 translate-y-2 opacity-0`;
    el.innerHTML = `<span>${esc(message)}</span>`;

    container.appendChild(el);

    // Animate in
    requestAnimationFrame(() => {
      el.classList.remove('translate-y-2', 'opacity-0');
    });

    // Remove after 3.5s
    setTimeout(() => {
      el.classList.add('opacity-0', 'translate-y-2');
      el.addEventListener('transitionend', () => el.remove());
    }, 3500);
  }

  // ─── String / display helpers ──────────────────────────────────────────────

  /** HTML-escape a string to prevent XSS */
  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g,  '&amp;')
      .replace(/</g,  '&lt;')
      .replace(/>/g,  '&gt;')
      .replace(/"/g,  '&quot;')
      .replace(/'/g,  '&#039;');
  }

  /** Capitalise first letter */
  function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  /** Human-readable status labels */
  function statusLabel(status) {
    const map = {
      reported:   'Reported',
      inProgress: 'In Progress',
      resolved:   'Resolved',
      onhold:     'On Hold',
    };
    return map[status] || capitalize(status);
  }

  /** Format ISO date string to "Jan 5, 2025" */
  function formatDate(isoString) {
    if (!isoString) return '—';
    try {
      return new Date(isoString).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
      });
    } catch { return isoString; }
  }

  // ─── Public API ───────────────────────────────────────────────────────────
  return { getToken, getUser, requireAuth, logout, api, initSidebar, toast, esc, capitalize, statusLabel, formatDate };
})();

// ─── Global sidebar toggle (used by hamburger buttons) ────────────────────────
function toggleSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebar-overlay');
  if (!sidebar) return;
  const isOpen = !sidebar.classList.contains('-translate-x-full');
  if (isOpen) {
    sidebar.classList.add('-translate-x-full');
    if (overlay) overlay.classList.add('hidden');
  } else {
    sidebar.classList.remove('-translate-x-full');
    if (overlay) overlay.classList.remove('hidden');
  }
}

// Close sidebar when overlay is clicked
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('sidebar-overlay');
  if (overlay) overlay.addEventListener('click', toggleSidebar);

  // Wire logout buttons
  document.querySelectorAll('[data-logout]').forEach(btn => {
    btn.addEventListener('click', (e) => { e.preventDefault(); App.logout(); });
  });
});
