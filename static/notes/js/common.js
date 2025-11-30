// Global loader management
(function() {
  function showLoader(message) {
    const overlay = document.getElementById('loader-overlay');
    if (!overlay) return;
    if (message) {
      const textEl = overlay.querySelector('.loader-text');
      if (textEl) textEl.textContent = message;
    }
    overlay.classList.remove('hidden');
  }

  function hideLoader() {
    const overlay = document.getElementById('loader-overlay');
    if (!overlay) return;
    overlay.classList.add('hidden');
  }

  window.showLoader = showLoader;
  window.hideLoader = hideLoader;

  document.addEventListener('DOMContentLoaded', function() {
    // Hide overlay at start in case it's visible
    hideLoader();

    // Show loader on link navigation (internal links) to give impression of navigation
    document.querySelectorAll('a[href]').forEach(a => {
      const href = a.getAttribute('href');
      // Skip anchors and external links and JS triggers
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) return;
      a.addEventListener('click', function(e) {
        // Only for same-origin navigations
        try {
          const url = new URL(href, window.location.href);
          if (url.origin === window.location.origin) {
            // Allow ctrl/meta clicks (open in new tab)
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
            showLoader();
          }
        } catch (e) {
          // ignore invalid URLs
        }
      });
    });

    // Show loader on all form submits by default
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', function(e) {
        // Do not show for AJAX forms if they handle their own loading
        if (form.dataset.skipLoader === 'true') return;
        showLoader();
      });
    });

    // Intercept fetch and show loader
    if (window.fetch) {
      const originalFetch = window.fetch;
      window.fetch = async function() {
        showLoader();
        try {
          const res = await originalFetch.apply(this, arguments);
          hideLoader();
          return res;
        } catch (err) {
          hideLoader();
          throw err;
        }
      }
    }

    // Intercept XMLHttpRequest
    (function() {
      const XHRProto = XMLHttpRequest.prototype;
      const originalOpen = XHRProto.open;
      XHRProto.open = function(method, url) {
        this.addEventListener('loadstart', function() { showLoader(); });
        this.addEventListener('loadend', function() { hideLoader(); });
        originalOpen.apply(this, arguments);
      }
    })();

    // Hide loader after page fully loads
    window.addEventListener('load', function() {
      hideLoader();
    });

  });
})();
