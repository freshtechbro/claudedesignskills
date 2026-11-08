// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

// ============================
// Loading Screen
// ============================

window.addEventListener("load", () => {
  const loading = document.getElementById("loading");

  gsap.to(loading, {
    opacity: 0,
    duration: 0.5,
    delay: 0.5,
    onComplete: () => {
      loading.classList.add("hidden");
      initAnimations();
    }
  });
});

// ============================
// Initialize All Animations
// ============================

function initAnimations() {
  // Refresh ScrollTrigger after initialization
  ScrollTrigger.refresh();

  // Progress Bar
  setupProgressBar();

  // Navigation
  setupNavigation();

  // Hero Section
  animateHero();

  // Features Section (Fade In Cards)
  animateFeatures();

  // Parallax Section
  setupParallax();

  // Pin Section
  setupPinSection();

  // Gallery Section (Stagger)
  animateGallery();

  // Horizontal Scroll Section
  setupHorizontalScroll();

  // Text Reveal Section
  animateTextReveal();

  // Contact Form
  animateContactForm();

  // Smooth Scroll Links
  setupSmoothScroll();

  // Active Nav Tracking
  trackActiveSection();
}

// ============================
// Progress Bar
// ============================

function setupProgressBar() {
  gsap.to(".progress-bar", {
    scaleX: 1,
    ease: "none",
    scrollTrigger: {
      start: "top top",
      end: "bottom bottom",
      scrub: 0.3
    }
  });
}

// ============================
// Navigation Hide/Show
// ============================

function setupNavigation() {
  let lastScroll = 0;
  const nav = document.querySelector(".nav");

  ScrollTrigger.create({
    start: 100,
    end: 99999,
    onUpdate: (self) => {
      const currentScroll = self.scroll();

      if (currentScroll > lastScroll && currentScroll > 100) {
        // Scrolling down - hide nav
        gsap.to(nav, { y: -100, duration: 0.3, ease: "power2.out" });
      } else {
        // Scrolling up - show nav
        gsap.to(nav, { y: 0, duration: 0.3, ease: "power2.out" });
      }

      lastScroll = currentScroll;
    }
  });
}

// ============================
// Hero Section
// ============================

function animateHero() {
  const tl = gsap.timeline();

  tl.from(".hero-title", {
    opacity: 0,
    y: 100,
    duration: 1,
    ease: "power3.out"
  })
  .from(".hero-subtitle", {
    opacity: 0,
    y: 50,
    duration: 0.8,
    ease: "power2.out"
  }, "-=0.5")
  .from(".cta-btn", {
    scale: 0,
    duration: 0.5,
    ease: "back.out(1.7)"
  }, "-=0.3")
  .from(".scroll-indicator", {
    opacity: 0,
    y: 30,
    duration: 0.8,
    ease: "power2.out"
  }, "-=0.3");

  // Parallax effect on hero background
  gsap.to(".hero-bg", {
    yPercent: 50,
    ease: "none",
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "bottom top",
      scrub: true
    }
  });

  // Fade out hero content on scroll
  gsap.to(".hero-content", {
    opacity: 0,
    y: 100,
    ease: "none",
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "bottom top",
      scrub: true
    }
  });
}

// ============================
// Features Section (Cards)
// ============================

function animateFeatures() {
  gsap.from(".card", {
    opacity: 0,
    y: 80,
    duration: 0.8,
    ease: "power2.out",
    stagger: {
      each: 0.15,
      from: "start"
    },
    scrollTrigger: {
      trigger: ".features-section",
      start: "top 80%"
    }
  });
}

// ============================
// Parallax Section
// ============================

function setupParallax() {
  gsap.to(".parallax-bg", {
    y: 200,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-section",
      start: "top bottom",
      end: "bottom top",
      scrub: true
    }
  });

  gsap.from(".parallax-content", {
    opacity: 0,
    scale: 0.8,
    scrollTrigger: {
      trigger: ".parallax-section",
      start: "top 80%",
      end: "top 50%",
      scrub: true
    }
  });
}

// ============================
// Pin Section with Animation
// ============================

function setupPinSection() {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".pin-section",
      start: "top top",
      end: "+=1000",
      pin: true,
      scrub: 1,
      anticipatePin: 1
    }
  });

  tl.from(".pin-title", { opacity: 0, y: -50 })
    .from(".pin-text", { opacity: 0, y: -30 }, "-=0.5")
    .from(".pin-box", {
      scale: 0,
      rotation: 180,
      stagger: 0.2,
      ease: "back.out(1.7)"
    })
    .to(".pin-box", {
      y: -50,
      stagger: {
        each: 0.1,
        yoyo: true,
        repeat: 1
      }
    });
}

// ============================
// Gallery Section (Stagger)
// ============================

function animateGallery() {
  gsap.from(".gallery-item", {
    opacity: 0,
    scale: 0.5,
    duration: 0.8,
    ease: "back.out(1.7)",
    stagger: {
      each: 0.15,
      from: "center",
      grid: "auto"
    },
    scrollTrigger: {
      trigger: ".gallery-section",
      start: "top 70%"
    }
  });
}

// ============================
// Horizontal Scroll Section
// ============================

function setupHorizontalScroll() {
  const panels = gsap.utils.toArray(".horizontal-panel");

  const scrollTween = gsap.to(panels, {
    xPercent: -100 * (panels.length - 1),
    ease: "none",
    scrollTrigger: {
      trigger: ".horizontal-wrapper",
      pin: true,
      scrub: 1,
      snap: {
        snapTo: 1 / (panels.length - 1),
        duration: { min: 0.2, max: 0.5 },
        ease: "power1.inOut"
      },
      end: () => "+=" + (document.querySelector(".horizontal-wrapper").offsetWidth * panels.length)
    }
  });

  // Animate content within each panel
  panels.forEach((panel, i) => {
    gsap.from(panel.children, {
      opacity: 0,
      y: 50,
      scrollTrigger: {
        trigger: panel,
        containerAnimation: scrollTween,
        start: "left center",
        end: "center center",
        scrub: true
      }
    });
  });
}

// ============================
// Text Reveal Section
// ============================

function animateTextReveal() {
  gsap.from(".reveal-line", {
    opacity: 0,
    y: 100,
    duration: 1,
    ease: "power3.out",
    stagger: 0.2,
    scrollTrigger: {
      trigger: ".text-section",
      start: "top 70%"
    }
  });
}

// ============================
// Contact Form
// ============================

function animateContactForm() {
  gsap.from(".contact-form .fade-in", {
    opacity: 0,
    y: 50,
    duration: 0.8,
    ease: "power2.out",
    stagger: 0.15,
    scrollTrigger: {
      trigger: ".contact-form",
      start: "top 80%"
    }
  });

  // Form submission animation (demo)
  const form = document.querySelector(".contact-form");
  const submitBtn = document.querySelector(".submit-btn");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    gsap.to(submitBtn, {
      scale: 0.9,
      duration: 0.1,
      yoyo: true,
      repeat: 1,
      onComplete: () => {
        submitBtn.textContent = "✓ Message Sent!";
        submitBtn.style.background = "#4caf50";

        setTimeout(() => {
          submitBtn.textContent = "Send Message";
          submitBtn.style.background = "";
          form.reset();
        }, 3000);
      }
    });
  });
}

// ============================
// Smooth Scroll to Sections
// ============================

function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));

      if (target) {
        gsap.to(window, {
          duration: 1,
          scrollTo: {
            y: target,
            offsetY: 80 // Account for fixed header
          },
          ease: "power2.inOut"
        });
      }
    });
  });
}

// ============================
// Active Navigation Tracking
// ============================

function trackActiveSection() {
  const sections = gsap.utils.toArray("section[id]");
  const navItems = gsap.utils.toArray(".nav-item");

  sections.forEach((section, i) => {
    ScrollTrigger.create({
      trigger: section,
      start: "top center",
      end: "bottom center",
      onEnter: () => setActiveNav(section.id),
      onEnterBack: () => setActiveNav(section.id)
    });
  });

  function setActiveNav(id) {
    navItems.forEach(item => {
      if (item.getAttribute("href") === `#${id}`) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });
  }
}

// ============================
// Responsive Handling
// ============================

// Disable complex animations on mobile for performance
if (window.innerWidth < 768) {
  ScrollTrigger.config({
    limitCallbacks: true,
    ignoreMobileResize: true
  });
}

// ============================
// Refresh on Resize
// ============================

let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    ScrollTrigger.refresh();
  }, 250);
});

// ============================
// Performance Optimizations
// ============================

// Add will-change to animated elements
gsap.set(".fade-in, .card, .gallery-item, .pin-box", {
  willChange: "transform, opacity"
});

// Debug mode (set to false in production)
const DEBUG = false;

if (DEBUG) {
  ScrollTrigger.defaults({
    markers: true
  });
}

// ============================
// Console Welcome Message
// ============================

console.log(
  "%c🚀 GSAP ScrollTrigger Starter",
  "font-size: 20px; font-weight: bold; color: #667eea;"
);
console.log(
  "%cBuilt with GSAP 3 & ScrollTrigger",
  "font-size: 14px; color: #764ba2;"
);
