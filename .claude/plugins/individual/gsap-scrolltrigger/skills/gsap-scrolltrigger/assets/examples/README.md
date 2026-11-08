# GSAP ScrollTrigger Examples

Real-world patterns and implementations for common ScrollTrigger use cases.

## 📚 Available Examples

### Core Patterns

All examples are self-contained HTML files demonstrating specific ScrollTrigger patterns. Open any file directly in your browser to see the demo.

---

## 🎯 Pattern Categories

### 1. Fade & Entrance Animations

**Use Cases**: Content reveals, card grids, feature sections

```javascript
// Basic fade in
gsap.from(".element", {
  opacity: 0,
  y: 50,
  scrollTrigger: {
    trigger: ".element",
    start: "top 80%"
  }
});
```

**Variations**:
- Batch animations for multiple elements
- Stagger from different directions (center, edges, random)
- Grid-based stagger patterns

---

### 2. Pinning Animations

**Use Cases**: Storytelling, feature highlights, step-by-step guides

```javascript
ScrollTrigger.create({
  trigger: ".section",
  start: "top top",
  end: "+=1000",
  pin: true,
  scrub: 1
});
```

**Variations**:
- Pin with timeline animations
- Multiple pinned sections (stacked cards)
- Pin with snap points

---

### 3. Horizontal Scrolling

**Use Cases**: Portfolios, product showcases, timelines

```javascript
gsap.to(".panels", {
  xPercent: -100 * (panels.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    end: () => "+=" + container.offsetWidth
  }
});
```

**Variations**:
- With snap points between panels
- Nested animations within panels
- Progress indicators

---

### 4. Parallax Effects

**Use Cases**: Hero sections, immersive storytelling, depth perception

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

**Variations**:
- Multi-layer parallax (2-5 layers)
- Parallax with zoom
- Directional parallax (horizontal/vertical)

---

### 5. Text Animations

**Use Cases**: Headlines, storytelling, attention-grabbing reveals

```javascript
// Requires SplitText plugin (Club GreenSock)
const split = new SplitText(".text", { type: "lines" });

gsap.from(split.lines, {
  opacity: 0,
  y: 20,
  stagger: 0.1,
  scrollTrigger: {
    trigger: ".text",
    start: "top 80%"
  }
});
```

**Variations**:
- Line-by-line reveals
- Character animations
- Typewriter effects
- Text masking

---

### 6. Image Reveals

**Use Cases**: Galleries, case studies, portfolio pieces

```javascript
// Curtain reveal
gsap.to(".curtain", {
  xPercent: 100,
  duration: 1,
  scrollTrigger: {
    trigger: ".image",
    start: "top 80%"
  }
});
```

**Variations**:
- Clip-path reveals
- Scale reveals
- Directional wipes
- Parallax zoom

---

## 🚀 Quick Start

### Run Any Example

1. Open any `.html` file in your browser
2. Or serve with a local server:

```bash
python -m http.server 8000
# Navigate to http://localhost:8000/pin_animation.html
```

### Integrate into Your Project

Each example is self-contained. Copy the relevant code sections:

1. **HTML Structure** - Copy the markup
2. **CSS Styles** - Copy relevant styles
3. **JavaScript** - Copy animation code, adjust selectors

---

## 📖 Learning Path

### Beginner

1. Study basic fade-in patterns
2. Experiment with stagger animations
3. Try different easing functions
4. Enable debug markers to visualize triggers

### Intermediate

1. Build pinned sections with timelines
2. Create parallax effects
3. Implement horizontal scrolling
4. Add scroll progress indicators

### Advanced

1. Create image sequence animations
2. Build complex multi-section experiences
3. Integrate with Three.js or Canvas
4. Implement custom ScrollTrigger behaviors

---

## 💡 Best Practices

### Performance

1. Use `transform` and `opacity` (GPU-accelerated)
2. Apply `will-change` to animated elements
3. Use `scrub` for smooth scroll-driven animations
4. Limit number of active ScrollTriggers

### UX

1. Keep animations subtle and purposeful
2. Test on multiple devices and screen sizes
3. Provide fallbacks for users with motion sensitivity
4. Ensure content is accessible without animations

### Development

1. Enable debug markers during development
2. Use meaningful trigger/element names
3. Comment complex animation sequences
4. Test scroll performance with DevTools

---

## 🔗 Additional Resources

### Official GSAP Resources

- [ScrollTrigger Docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger)
- [GSAP Showcase](https://gsap.com/showcase/)
- [CodePen Examples](https://codepen.io/GreenSock/pens/popular)
- [GSAP Forums](https://gsap.com/community/)

### Included in This Package

- `../references/api_reference.md` - Complete GSAP & ScrollTrigger API
- `../references/easing_guide.md` - Visual easing reference
- `../references/common_patterns.md` - Copy-paste pattern library
- `../easings/easing_visualizer.html` - Interactive easing tool
- `../starter_scroll/` - Complete website template

---

## 🎨 Customization Tips

### Adjust Timing

```javascript
// Slower animation
duration: 2  // instead of 1

// More gradual scroll response
scrub: 2  // instead of true or 1
```

### Change Trigger Points

```javascript
// Trigger earlier
start: "top 90%"  // instead of "top 80%"

// Trigger later
start: "top 50%"
```

### Modify Easing

```javascript
// More dramatic
ease: "power3.out"  // instead of "power2.out"

// Playful
ease: "back.out(1.7)"
```

---

## 🐛 Common Issues

### Animation Not Triggering

- Check element selectors
- Enable debug markers: `markers: true`
- Verify trigger element exists in DOM
- Check browser console for errors

### Jumpy Animations

- Use `scrub` for smooth scroll-tied animations
- Add `anticipatePin: 1` for pinned sections
- Check for layout shifts (images without dimensions)

### Poor Performance

- Reduce number of animated elements
- Use `ScrollTrigger.batch()` for many elements
- Avoid animating expensive properties (width, height)
- Test on target devices

---

## 📱 Mobile Considerations

```javascript
// Disable complex animations on mobile
if (window.innerWidth < 768) {
  // Use simpler animations or CSS-only
}

// Or use ScrollTrigger.matchMedia()
ScrollTrigger.matchMedia({
  "(min-width: 800px)": function() {
    // Desktop animations
  },
  "(max-width: 799px)": function() {
    // Mobile animations
  }
});
```

---

## 🎯 Example Use Cases

### E-commerce

- Product reveals on scroll
- Feature highlights with pinning
- Parallax hero sections
- Image galleries with stagger

### Portfolios

- Horizontal project showcases
- Case study storytelling with pins
- Image sequence animations
- Smooth page transitions

### Marketing Sites

- Feature sections with animations
- Testimonial sliders
- Pricing table reveals
- CTA animations

### Storytelling

- Chapter-based pinned sections
- Text reveals for narrative
- Image sequences for progression
- Parallax depth for immersion

---

## 📝 Code Snippets

### Quick Copy-Paste Examples

#### Fade In on Scroll

```html
<div class="fade-in">Content here</div>

<script>
gsap.from(".fade-in", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: ".fade-in",
    start: "top 80%"
  }
});
</script>
```

#### Progress Bar

```html
<div class="progress" style="position: fixed; top: 0; left: 0; height: 4px; background: blue; transform-origin: left;"></div>

<script>
gsap.to(".progress", {
  scaleX: 1,
  ease: "none",
  scrollTrigger: {
    start: "top top",
    end: "bottom bottom",
    scrub: 0.3
  }
});
</script>
```

#### Smooth Scroll Navigation

```html
<a href="#section2">Go to Section 2</a>

<script>
gsap.registerPlugin(ScrollToPlugin);

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    gsap.to(window, {
      duration: 1,
      scrollTo: this.getAttribute("href"),
      ease: "power2.inOut"
    });
  });
});
</script>
```

---

## 🎓 Next Steps

1. **Explore** - Open examples and study the code
2. **Modify** - Change values and see what happens
3. **Combine** - Mix patterns to create unique effects
4. **Build** - Create your own scroll-driven experience

---

**Need Help?**

- Check the [API Reference](../references/api_reference.md)
- Try the [Easing Visualizer](../easings/easing_visualizer.html)
- Browse [Common Patterns](../references/common_patterns.md)
- Visit [GSAP Forums](https://gsap.com/community/)

---

**Happy Scrolling!** 🎉
