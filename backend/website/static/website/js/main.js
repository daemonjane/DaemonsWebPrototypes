(function () {
  const scrollBtn = document.getElementById('scroll-to-top');
  if (scrollBtn) {
    document.addEventListener('scroll', function () {
      scrollBtn.style.display = window.scrollY > 300 ? 'flex' : 'none';
    }, { passive: true });
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
})();
