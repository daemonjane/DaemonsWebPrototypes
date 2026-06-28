// Main JavaScript for the website.
(function () {
  const scrollBtn = document.getElementById('scroll-to-top');
  if (scrollBtn) {
    document.addEventListener('scroll', function () {
      scrollBtn.style.display = window.scrollY > 300 ? 'flex' : 'none';
    }, { passive: true });
    scrollBtn.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', function () {
      mobileMenu.classList.toggle('hidden');
    });
  }

  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    });
  }

  if (localStorage.getItem('theme') === 'light') {
    document.documentElement.classList.remove('dark');
  }

  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 300);
    }, 5000);
  });

  document.querySelectorAll('.alert-close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var alert = this.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 300);
      }
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
      }
    }
  });
  document.addEventListener('click', function (e) {
    if (mobileMenu && !mobileMenu.classList.contains('hidden') && !e.target.closest('#mobile-menu') && !e.target.closest('#mobile-menu-toggle')) {
      mobileMenu.classList.add('hidden');
    }
  });
})();
