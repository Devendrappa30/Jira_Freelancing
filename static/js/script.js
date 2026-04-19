// ════════════════════════════════════════════════════════════════════════
// SCRIPT.JS — Interactive Features for Jira Freelancer Portfolio
// ════════════════════════════════════════════════════════════════════════

(function() {
  'use strict';

  // ──────────────────────────────────────────────────────────────────────
  // 1. NAVBAR TOGGLE (Mobile Menu)
  // ──────────────────────────────────────────────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navbar = document.getElementById('navbar');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      navToggle.classList.toggle('active');
    });

    // Close menu when clicking a nav item
    document.querySelectorAll('.nav-item, .nav-cta').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
      });
    });

    // Close menu on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-container')) {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
      }
    });
  }

  // ──────────────────────────────────────────────────────────────────────
  // 2. NAVBAR SCROLL EFFECT (Shadow on scroll)
  // ──────────────────────────────────────────────────────────────────────
  window.addEventListener('scroll', () => {
    if (navbar) {
      if (window.scrollY > 10) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }
  });

  // ──────────────────────────────────────────────────────────────────────
  // 3. SMOOTH SCROLL FOR ANCHOR LINKS
  // ──────────────────────────────────────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ──────────────────────────────────────────────────────────────────────
  // 4. SCROLL REVEAL ANIMATIONS (fade-in on scroll)
  // ──────────────────────────────────────────────────────────────────────
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all elements with data-reveal or data-reveal-delay
  document.querySelectorAll('[data-reveal], [data-reveal-delay]').forEach(el => {
    observer.observe(el);
  });

  // ──────────────────────────────────────────────────────────────────────
  // 5. BACK TO TOP BUTTON
  // ──────────────────────────────────────────────────────────────────────
  const bttButton = document.getElementById('btt');

  if (bttButton) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        bttButton.classList.add('visible');
      } else {
        bttButton.classList.remove('visible');
      }
    });

    bttButton.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ────────────��─────────────────────────────────────────────────────────
  // 6. FLASH MESSAGE AUTO-DISMISS
  // ──────────────────────────────────────────────────────────────────────
  const flashMessages = document.querySelectorAll('.flash');
  
  flashMessages.forEach(flash => {
    // Auto-dismiss after 6 seconds
    setTimeout(() => {
      flash.style.transition = 'opacity 0.3s ease-out';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 300);
    }, 6000);

    // Manual close button
    const closeBtn = flash.querySelector('button');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        flash.style.transition = 'opacity 0.3s ease-out';
        flash.style.opacity = '0';
        setTimeout(() => flash.remove(), 300);
      });
    }
  });

  // ──────────────────────────────────────────────────────────────────────
  // 7. FORM VALIDATION (Contact Form)
  // ──────────────────────────────────────────────────────────────────────
  const contactForm = document.querySelector('form[method="post"]');
  
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      const name = this.querySelector('input[name="name"]')?.value.trim();
      const email = this.querySelector('input[name="email"]')?.value.trim();
      const message = this.querySelector('textarea[name="message"]')?.value.trim();

      if (!name || !email || !message) {
        e.preventDefault();
        alert('Please fill in all required fields.');
      }

      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (email && !emailRegex.test(email)) {
        e.preventDefault();
        alert('Please enter a valid email address.');
      }
    });
  }

  // ──────────────────────────────────────────────────────────────────────
  // 8. ACTIVE NAV INDICATOR (highlight current page)
  // ──────────────────────────────────────────────────────────────────────
  const currentPage = window.location.pathname;
  document.querySelectorAll('.nav-item, .nav-cta').forEach(item => {
    const href = item.getAttribute('href');
    if (href === currentPage || (currentPage === '/' && href === '/')) {
      item.classList.add('active');
    }
  });

  // ──────────────────────────────────────────────────────────────────────
  // 9. LAZY LOAD IMAGES
  // ───────────────────────────────────────────────────��──────────────────
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src || img.src;
          img.classList.add('loaded');
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // ──────────────────────────────────────────────────────────────────────
  // 10. PREVENT MULTIPLE FORM SUBMISSIONS
  // ──────────────────────────────────────────────────────────────────────
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
      const buttons = this.querySelectorAll('button[type="submit"]');
      buttons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.6';
        btn.style.cursor = 'not-allowed';
      });
    });
  });

  // ──────────────────────────────────────────────────────────────────────
  // 11. SMOOTH PAGE TRANSITIONS
  // ───────────────────────────────────────────────────────────��──────────
  document.addEventListener('DOMContentLoaded', () => {
    document.body.style.opacity = '1';
  });

  // ──────────────────────────────────────────────────────────────────────
  // 12. KEYBOARD ACCESSIBILITY
  // ──────────────────────────────────────────────────────────────────────
  if (bttButton) {
    bttButton.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  // ──────────────────────────────────────────────────────────────────────
  // 13. PORTFOLIO CARD HOVER EFFECTS
  // ──────────────────────────────────────────────────────────────────────
  document.querySelectorAll('.pp-card, .svc-preview-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
    });
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // ──────────────────────────────────────────────────────────────────────
  // 14. COUNTER ANIMATION FOR STATS (numbers count up)
  // ──────────────────────────────────────────────────────────────────────
  const animateCounters = () => {
    document.querySelectorAll('.stat-num').forEach(stat => {
      const target = parseInt(stat.innerText.replace(/\D/g, ''));
      if (!isNaN(target) && !stat.dataset.animated) {
        stat.dataset.animated = 'true';
        let current = 0;
        const increment = target / 30;
        const timer = setInterval(() => {
          current += increment;
          if (current >= target) {
            stat.innerText = stat.innerText.replace(/\d+/, target);
            clearInterval(timer);
          } else {
            stat.innerText = stat.innerText.replace(/\d+/, Math.floor(current));
          }
        }, 30);
      }
    });
  };

  // Trigger counter animation when stats section comes into view
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters();
        statsObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  const statsSection = document.querySelector('.stats-strip');
  if (statsSection) statsObserver.observe(statsSection);

  // ──────────────────────────────────────────────────────────────────────
  // 15. HANDLE EXTERNAL LINKS (open in new tab)
  // ──────────────────────────────────────────────────────────────────────
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    if (!link.hostname || link.hostname !== window.location.hostname) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    }
  });

  console.log('✅ Jira Freelancer Portfolio — All scripts loaded!');
})();