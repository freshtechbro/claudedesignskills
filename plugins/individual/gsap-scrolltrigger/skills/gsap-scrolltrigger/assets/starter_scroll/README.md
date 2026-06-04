# GSAP ScrollTrigger Starter Template

A production-ready, scroll-driven website template featuring modern GSAP & ScrollTrigger animations.

## ✨ Features

### Animations Included

- ✅ **Hero Section** - Parallax background with fade-out content
- ✅ **Fade-in Cards** - Staggered entrance animations
- ✅ **Parallax Section** - Multi-layer depth effect
- ✅ **Pin Section** - Content pinned while animations play
- ✅ **Stagger Gallery** - Grid animation from center
- ✅ **Horizontal Scroll** - Vertical scroll triggering horizontal movement
- ✅ **Text Reveal** - Line-by-line text animations
- ✅ **Progress Bar** - Scroll progress indicator
- ✅ **Smart Navigation** - Hide on scroll down, show on scroll up
- ✅ **Active Nav Tracking** - Highlights current section
- ✅ **Smooth Scroll** - Click anchors for smooth navigation
- ✅ **Responsive** - Mobile-optimized animations
- ✅ **Loading Screen** - Smooth intro animation

### Technical Features

- 🚀 **Performance Optimized** - GPU-accelerated animations, will-change optimization
- 📱 **Mobile Responsive** - Adapts animations for smaller screens
- 🎨 **Modern Design** - Clean, gradient-based aesthetic
- ⚡ **Zero Dependencies** - Only GSAP required (via CDN)
- 🛠 **Easy Customization** - Well-organized, commented code
- 📦 **Production Ready** - Tested and optimized for real-world use

---

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Serve with any static server
python -m http.server 8000
# Or
npx serve
# Or
php -S localhost:8000
```

Open `http://localhost:8000` in your browser.

### Option 2: Direct Open

Simply open `index.html` in your browser (some animations may require a server for full functionality).

---

## 📁 Project Structure

```
starter_scroll/
├── index.html    # Main HTML structure
├── style.css     # Complete styles (~580 lines)
├── main.js       # GSAP animations (~420 lines)
└── README.md     # This file
```

---

## 🎨 Customization Guide

### 1. Change Colors

Edit CSS variables in `style.css`:

```css
:root {
  --primary: #667eea;      /* Primary gradient color */
  --secondary: #764ba2;    /* Secondary gradient color */
  --text-dark: #333;       /* Main text color */
  --text-light: #666;      /* Secondary text color */
  --bg-light: #f9f9f9;     /* Light background */
}
```

### 2. Adjust Animation Timing

In `main.js`, modify animation durations and easing:

```javascript
// Example: Hero animation
tl.from(".hero-title", {
  opacity: 0,
  y: 100,
  duration: 1,        // Change duration
  ease: "power3.out"  // Change easing
});
```

**Common Easing Options**:
- `power2.out` - Standard (most common)
- `power3.out` - Dramatic
- `back.out(1.7)` - Playful overshoot
- `elastic.out` - Bouncy
- `none` - Linear (for scrubbed animations)

### 3. Modify Scroll Trigger Points

Adjust `start` and `end` positions:

```javascript
scrollTrigger: {
  trigger: ".section",
  start: "top 80%",      // When top of section hits 80% of viewport
  end: "bottom 20%",     // When bottom hits 20% of viewport
  scrub: true            // Tie animation to scroll
}
```

**Position Format**: `"[trigger position] [viewport position]"`
- Examples: `"top top"`, `"center center"`, `"bottom 80%"`

### 4. Enable Debug Markers

In `main.js`, set `DEBUG = true`:

```javascript
const DEBUG = true;  // Shows visual scroll trigger markers
```

This displays colored markers showing trigger start/end points.

### 5. Add Your Own Sections

**HTML**:
```html
<section class="section my-section">
  <div class="container">
    <h2 class="section-title">My Section</h2>
    <p class="fade-in">Content here...</p>
  </div>
</section>
```

**JavaScript**:
```javascript
gsap.from(".my-section .fade-in", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: ".my-section",
    start: "top 80%"
  }
});
```

---

## 🎯 Animation Patterns Reference

### Fade In on Scroll

```javascript
gsap.from(".element", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: ".element",
    start: "top 80%"
  }
});
```

### Scroll-Driven Animation (Scrubbed)

```javascript
gsap.to(".element", {
  x: 500,
  scrollTrigger: {
    trigger: ".container",
    start: "top top",
    end: "bottom top",
    scrub: true  // Animation tied to scroll position
  }
});
```

### Pin Section

```javascript
ScrollTrigger.create({
  trigger: ".section",
  start: "top top",
  end: "+=1000",  // Pin for 1000px of scrolling
  pin: true,
  pinSpacing: true
});
```

### Stagger Animation

```javascript
gsap.from(".item", {
  opacity: 0,
  y: 50,
  stagger: 0.15,  // 0.15s delay between each
  scrollTrigger: {
    trigger: ".container",
    start: "top 80%"
  }
});
```

### Parallax Effect

```javascript
gsap.to(".bg", {
  y: 200,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

---

## 📱 Responsive Behavior

Animations automatically adapt for mobile devices:

- Reduced animation complexity on `< 768px` screens
- `limitCallbacks` enabled for better mobile performance
- Navigation adapts to touch interactions
- Horizontal scroll becomes vertical scroll on mobile

**Manual Responsive Control**:

```javascript
ScrollTrigger.matchMedia({
  // Desktop
  "(min-width: 800px)": function() {
    // Desktop-only animations
  },

  // Mobile
  "(max-width: 799px)": function() {
    // Mobile-only animations
  }
});
```

---

## ⚡ Performance Tips

### Already Implemented

1. **GPU Acceleration** - Using `transform` and `opacity` (GPU-friendly properties)
2. **Will-change** - Applied to animated elements
3. **Efficient Selectors** - Cached element queries
4. **Debounced Resize** - Prevents excessive refresh calls
5. **Mobile Optimization** - Simplified animations on small screens

### Additional Optimizations

1. **Reduce Animation Count**

```javascript
// Instead of animating many elements
gsap.from(".item", { ... });

// Use batch for better performance
ScrollTrigger.batch(".item", {
  onEnter: batch => gsap.from(batch, { ... })
});
```

2. **Lower Scrub Precision**

```javascript
scrollTrigger: {
  scrub: 1  // Instead of true (smoother but less precise)
}
```

3. **Disable Markers in Production**

```javascript
const DEBUG = false;  // Removes visual markers
```

---

## 🐛 Troubleshooting

### Animations Not Triggering

1. Check console for errors
2. Enable debug markers: `DEBUG = true`
3. Verify element selectors match HTML
4. Ensure content is loaded: animations run after `window.load`

### Jumpy Scroll on Mobile

```javascript
// Add to ScrollTrigger config
ScrollTrigger.config({
  ignoreMobileResize: true
});
```

### Layout Shifts After Pin

```javascript
ScrollTrigger.create({
  pin: true,
  pinSpacing: true  // or false, depending on desired behavior
});
```

### Horizontal Scroll Issues

1. Check container width calculation
2. Verify number of panels
3. Test on different screen sizes

---

## 🔧 Advanced Customization

### Add Timeline Sequences

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".section",
    start: "top 80%"
  }
});

tl.from(".title", { opacity: 0, y: -50 })
  .from(".subtitle", { opacity: 0, y: -30 }, "-=0.3")
  .from(".button", { scale: 0 }, "-=0.2");
```

### Callback Functions

```javascript
scrollTrigger: {
  trigger: ".section",
  start: "top 80%",
  onEnter: () => console.log("Entered"),
  onLeave: () => console.log("Left"),
  onEnterBack: () => console.log("Scrolled back"),
  onLeaveBack: () => console.log("Left backwards")
}
```

### Toggle Actions

```javascript
scrollTrigger: {
  toggleActions: "play pause resume reset"
  // Format: onEnter onLeave onEnterBack onLeaveBack
  // Options: play, pause, resume, reset, restart, complete, reverse, none
}
```

---

## 📚 Resources

- [GSAP Documentation](https://gsap.com/docs/)
- [ScrollTrigger Docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger)
- [Easing Visualizer](../easings/easing_visualizer.html) - Included in this package
- [GSAP Forums](https://gsap.com/community/)
- [CodePen GSAP Examples](https://codepen.io/GreenSock/pens/popular)

---

## 🎓 Learning Path

### Beginner

1. Study `main.js` - Understand each animation function
2. Enable debug markers to visualize trigger points
3. Modify existing animations (timing, easing, distances)
4. Add simple fade-in animations to new elements

### Intermediate

1. Create custom timeline sequences
2. Build your own pinned sections
3. Implement custom scroll progress indicators
4. Add toggle actions and callbacks

### Advanced

1. Create image sequence animations
2. Build complex horizontal scroll experiences
3. Integrate with Three.js or Canvas
4. Implement custom easing functions

---

## 📄 Browser Compatibility

- ✅ Chrome/Edge 90+ (Excellent)
- ✅ Firefox 88+ (Excellent)
- ✅ Safari 14+ (Good)
- ⚠️ IE11 (Not supported - requires polyfills)

---

## 🚢 Deployment

### Production Checklist

1. ✅ Set `DEBUG = false` in `main.js`
2. ✅ Remove console logs (or keep welcome message)
3. ✅ Test on multiple devices and browsers
4. ✅ Optimize images and assets
5. ✅ Consider self-hosting GSAP (instead of CDN)
6. ✅ Minify CSS and JS for production
7. ✅ Test scroll performance with DevTools

### Hosting

Works with any static hosting:
- **Netlify** - Drop folder, auto-deploy
- **Vercel** - Git integration, instant deploys
- **GitHub Pages** - Free hosting from repo
- **Cloudflare Pages** - Fast global CDN

---

## 📝 License

This template is provided as-is for use in any project (personal or commercial).

GSAP and all official plugins (ScrollTrigger, SplitText, CustomEase, and others) are free for all uses, including commercial. See [GSAP licensing](https://gsap.com/licensing/) and the [Webflow + GreenSock announcement](https://gsap.com/blog/webflow-greensock/).

---

## 🙏 Credits

Built with:
- [GSAP](https://gsap.com) - Animation library
- [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger) - Scroll-driven animations
- [ScrollToPlugin](https://gsap.com/docs/v3/Plugins/ScrollToPlugin) - Smooth scroll navigation

---

## 💡 Tips for Success

1. **Start Simple** - Add animations incrementally, test frequently
2. **Use Debug Markers** - Visual feedback makes learning easier
3. **Study Examples** - Check GSAP CodePens for inspiration
4. **Test on Mobile** - Performance can vary significantly
5. **Read the Docs** - ScrollTrigger has many powerful options
6. **Join Community** - GSAP forums are helpful and active

---

## 🎉 What's Next?

- Add your own content and branding
- Customize colors and typography
- Experiment with different easing functions
- Try the [Easing Visualizer](../easings/easing_visualizer.html)
- Explore advanced patterns in `common_patterns.md`
- Build something amazing! 🚀

---

**Happy Animating!** ⚡
