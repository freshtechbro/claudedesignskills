/**
 * Locomotive Scroll Starter - Main JavaScript
 *
 * This file initializes Locomotive Scroll and demonstrates:
 * - Basic smooth scrolling
 * - Scroll event handling
 * - Call events
 * - Progress tracking
 * - Programmatic scrolling
 */

import LocomotiveScroll from 'https://cdn.skypack.dev/locomotive-scroll@4';

// Initialize Locomotive Scroll
const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  lerp: 0.1,          // Smoothness (0-1, lower = smoother)
  multiplier: 1,      // Speed multiplier
  class: 'is-inview', // Class added to visible elements
  repeat: true,       // Repeat in-view detection
  offset: ['10%', 0], // Global offset [bottom, top]
  getSpeed: true,     // Track scroll speed
  getDirection: true, // Track scroll direction

  // Tablet settings
  tablet: {
    smooth: true,
    breakpoint: 1024
  },

  // Smartphone settings
  smartphone: {
    smooth: true,
    breakpoint: 768
  }
});

// Update on window resize
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    scroll.update();
  }, 250);
});

// Scroll event - Fires on every scroll update
scroll.on('scroll', (args) => {
  // Current scroll position
  const scrollY = args.scroll.y;

  // Scroll speed and direction
  const speed = args.speed;
  const direction = args.direction; // 'up', 'down', 'left', 'right'

  // Log scroll info (remove in production)
  // console.log('Scroll Y:', scrollY, 'Speed:', speed, 'Direction:', direction);

  // Track specific element progress
  if (args.currentElements['hero-title']) {
    const progress = args.currentElements['hero-title'].progress;
    // Use progress (0 to 1) for custom animations
    // console.log('Hero title progress:', progress);
  }

  // Track special card
  if (args.currentElements['special-card']) {
    const el = args.currentElements['special-card'];
    // console.log('Special card in view:', el.inView);
  }
});

// Call event - Fires when elements with data-scroll-call enter/exit viewport
scroll.on('call', (func, way, obj) => {
  console.log(`Call event: ${func} - ${way}`);

  // Handle specific callbacks
  if (func === 'fadeIn') {
    if (way === 'enter') {
      console.log('Element entered viewport:', obj.el);
      obj.el.style.opacity = '1';
    } else if (way === 'exit') {
      console.log('Element exited viewport:', obj.el);
    }
  }
});

// Smooth scroll to section on nav click
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = link.getAttribute('href');

    if (target === '#hero') {
      scroll.scrollTo('top');
    } else {
      scroll.scrollTo(target, {
        offset: -80,      // Offset for fixed nav
        duration: 1000,   // Duration in ms
        easing: [0.25, 0.0, 0.35, 1.0] // Cubic bezier
      });
    }
  });
});

// Example: Programmatic scrolling
// Uncomment to test scrolling to specific elements
/*
setTimeout(() => {
  // Scroll to parallax section after 3 seconds
  scroll.scrollTo('#parallax', {
    offset: -100,
    duration: 2000,
    callback: () => console.log('Scrolled to parallax section!')
  });
}, 3000);
*/

// Example: Stop/Start scrolling
/*
// Stop scrolling
scroll.stop();

// Resume scrolling
setTimeout(() => {
  scroll.start();
}, 2000);
*/

// Example: Set scroll position directly (no animation)
/*
scroll.setScroll(0, 500); // x, y
*/

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  scroll.destroy();
});

// Log initialization
console.log('Locomotive Scroll initialized');
console.log('Scroll instance:', scroll);

// Export for debugging
window.locomotiveScroll = scroll;
