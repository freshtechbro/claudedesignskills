# Lightweight 3D Effects - Starter Template

Production-ready template combining **Vanta.js**, **Zdog**, and **Vanilla-Tilt** for stunning 3D effects with minimal overhead.

---

## Features

- 🌊 **Vanta.js Background** - Animated WebGL waves effect
- 🎨 **Zdog Illustrations** - Multiple pseudo-3D graphics
- 🎯 **Vanilla Tilt Cards** - Interactive 3D tilt effects with glare
- 📱 **Responsive Design** - Mobile-optimized with performance considerations
- ♿ **Accessible** - Semantic HTML and proper contrast
- 🚀 **Fast Loading** - CDN-based, optimized assets

---

## Quick Start

### 1. View Locally

Simply open `index.html` in a modern web browser. All dependencies are loaded via CDN.

```bash
# Option 1: Direct open
open index.html

# Option 2: Local server (recommended)
python -m http.server 8000
# Visit http://localhost:8000
```

### 2. Customize Colors

Edit `main.js` to change effect colors:

```javascript
// Vanta.js waves color
let vantaEffect = VANTA.WAVES({
  el: "#vanta-bg",
  color: 0x23153c,  // Change this hex number
  waveHeight: 15.00,
  waveSpeed: 0.75
});

// Zdog colors
const heroCube = new Zdog.Box({
  frontFace: '#667eea',  // Change face colors
  rearFace: '#764ba2'
});
```

### 3. Change Vanta Effect

Replace WAVES with any other Vanta effect:

```javascript
// Change from WAVES to BIRDS
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.birds.min.js"></script>

let vantaEffect = VANTA.BIRDS({
  el: "#vanta-bg",
  backgroundColor: 0x23153c,
  color1: 0xff0090,
  quantity: 5
});
```

Available effects: WAVES, CLOUDS, BIRDS, NET, CELLS, FOG, GLOBE, RINGS, DOTS, TOPOLOGY, TRUNK

---

## Project Structure

```
starter_lightweight/
├── index.html          # Main HTML structure
├── style.css           # Styling and responsive design
├── main.js             # All effects initialization
└── README.md           # This file
```

---

## What's Included

### Vanta.js Background

**Type**: WAVES effect
**Purpose**: Immersive animated background
**Performance**: ~15-20ms per frame on desktop

```javascript
// Located in main.js
let vantaEffect = VANTA.WAVES({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  color: 0x23153c,
  waveHeight: 15.00,
  zoom: 0.65
});
```

**Customization Options**:
- `color`: Wave color (hex number)
- `waveHeight`: Wave amplitude (0-30)
- `waveSpeed`: Animation speed (0-2)
- `shininess`: Surface reflectivity (0-100)

---

### Zdog Illustrations

**5 Different Illustrations**:

1. **Hero Cube** (`.hero-zdog`)
   - Rotating 3D cube with colored faces
   - Auto-animation on X and Y axes

2. **Card Icon 1 - Globe** (`.zdog-icon-1`)
   - Orbiting globe with particles
   - Represents Vanta.js

3. **Card Icon 2 - 3D Z** (`.zdog-icon-2`)
   - Layered "Z" letter with depth
   - Represents Zdog

4. **Card Icon 3 - Tilted Square** (`.zdog-icon-3`)
   - Stacked squares with parallax
   - Represents Vanilla-Tilt

5. **Demo Model** (`.demo-zdog`)
   - Interactive sphere with orbiting boxes
   - Drag to rotate
   - Control buttons for color/spin

**How to Add More**:

```javascript
const newIllo = new Zdog.Illustration({
  element: '.your-canvas-class',
  zoom: 2
});

new Zdog.Ellipse({
  addTo: newIllo,
  diameter: 40,
  stroke: 5,
  color: '#667eea'
});

function animate() {
  newIllo.rotate.y += 0.03;
  newIllo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();
```

---

### Vanilla Tilt Cards

**Applied to**: `.tilt-card` elements
**Features**:
- 15° max tilt
- Glare effect at 30% opacity
- 3% scale on hover
- 1000px perspective

**Configuration** (in `main.js`):

```javascript
VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
  max: 15,            // Max tilt angle
  speed: 400,         // Transition speed (ms)
  glare: true,        // Enable glare
  "max-glare": 0.3,   // Max glare opacity
  scale: 1.03,        // Scale multiplier
  perspective: 1000   // CSS perspective
});
```

**3D Transform Layers**:

```css
.card-icon {
  transform: translateZ(30px);
}
.card h2 {
  transform: translateZ(20px);
}
.card-btn {
  transform: translateZ(40px);
}
```

This creates depth when tilting.

---

## Customization Guide

### Change Hero Title

Edit `index.html`:

```html
<h1>Lightweight 3D Effects</h1>
<!-- Change to: -->
<h1>Your Custom Title</h1>
```

### Modify Card Content

Edit `index.html` card sections:

```html
<div class="card tilt-card" data-tilt>
  <canvas class="card-icon zdog-icon-1" width="120" height="120"></canvas>
  <h2>Your Title</h2>
  <p>Your description text here.</p>
  <button class="card-btn">Learn More</button>
</div>
```

### Add New Zdog Icon

1. Add canvas to HTML:
```html
<canvas class="zdog-icon-4" width="120" height="120"></canvas>
```

2. Create illustration in `main.js`:
```javascript
const icon4 = new Zdog.Illustration({
  element: '.zdog-icon-4',
  zoom: 2
});

new Zdog.Polygon({
  addTo: icon4,
  sides: 6,
  radius: 20,
  stroke: 3,
  color: '#667eea',
  fill: true
});

function animateIcon4() {
  icon4.rotate.z += 0.02;
  icon4.updateRenderGraph();
  requestAnimationFrame(animateIcon4);
}
animateIcon4();
```

### Change Tilt Settings per Card

Instead of global init, initialize individually:

```javascript
VanillaTilt.init(document.querySelector(".card-1"), {
  max: 25,
  glare: true
});

VanillaTilt.init(document.querySelector(".card-2"), {
  max: 10,
  glare: false
});
```

---

## Performance Optimization

### Mobile Optimization

**Automatic optimizations included**:

1. **Tilt disabled on mobile** (< 768px width)
```javascript
if (window.innerWidth < 768) {
  document.querySelectorAll('.tilt-card').forEach(card => {
    if (card.vanillaTilt) {
      card.vanillaTilt.destroy();
    }
  });
}
```

2. **Vanta mobile scale**
```javascript
scaleMobile: 1.00  // Adjust to 0.5 for better performance
```

3. **Responsive CSS**
```css
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }
}
```

### Further Optimizations

**1. Reduce Vanta complexity**

```javascript
VANTA.WAVES({
  el: "#vanta-bg",
  points: 5,           // Lower = faster (default: 10)
  maxDistance: 15,     // Lower = faster (default: 20)
  waveHeight: 10       // Lower = faster (default: 15)
});
```

**2. Limit Zdog animations**

```javascript
// Only animate when visible
let isVisible = true;

let observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    isVisible = entry.isIntersecting;
  });
});

observer.observe(document.querySelector('.hero-zdog'));

function animate() {
  if (isVisible) {
    heroCube.rotate.x += 0.01;
    heroIllo.updateRenderGraph();
  }
  requestAnimationFrame(animate);
}
```

**3. Pause Vanta when not visible**

```javascript
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    if (vantaEffect) vantaEffect.destroy();
  } else {
    vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });
  }
});
```

---

## Browser Support

| Browser | Vanta.js | Zdog | Vanilla-Tilt |
|---------|----------|------|--------------|
| Chrome  | ✅       | ✅   | ✅           |
| Firefox | ✅       | ✅   | ✅           |
| Safari  | ✅       | ✅   | ✅           |
| Edge    | ✅       | ✅   | ✅           |
| IE11    | ❌       | ✅   | ✅           |

**Notes**:
- Vanta.js requires WebGL support
- All effects gracefully degrade if unavailable
- Mobile gyroscope requires HTTPS

---

## Common Issues

### Vanta Not Loading

**Problem**: Background stays gradient, no animation

**Solutions**:
1. Check browser console for errors
2. Ensure Three.js loads before Vanta
3. Verify WebGL is enabled:
   ```javascript
   const canvas = document.createElement('canvas');
   const gl = canvas.getContext('webgl');
   console.log('WebGL:', gl ? 'Enabled' : 'Disabled');
   ```

### Tilt Not Working

**Problem**: Cards don't tilt on hover

**Solutions**:
1. Ensure `data-tilt` attribute exists
2. Check if Vanilla-Tilt script loaded
3. Verify card has dimensions:
   ```css
   .card {
     width: 300px;
     height: 400px;
   }
   ```

### Zdog Canvas Blank

**Problem**: Canvas shows nothing

**Solutions**:
1. Verify canvas dimensions are set
2. Check if illustration is updating:
   ```javascript
   console.log('Illustration:', illo);
   illo.updateRenderGraph();  // Force render
   ```
3. Ensure shapes have `stroke` or `fill`

---

## Deployment

### CDN Dependencies

All dependencies load from CDN (no build step required):

- Three.js: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js`
- Vanta.js: `https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js`
- Zdog: `https://unpkg.com/zdog@1/dist/zdog.dist.min.js`
- Vanilla-Tilt: `https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js`

### Hosting

**Static Hosting** (recommended):
- Netlify: Drag & drop folder
- Vercel: `vercel deploy`
- GitHub Pages: Push to `gh-pages` branch
- Cloudflare Pages: Connect repository

**Example Netlify Deploy**:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=.
```

### Build for Production (Optional)

For bundling with your app:

```bash
npm install three vanta zdog vanilla-tilt
```

```javascript
import * as THREE from 'three';
import WAVES from 'vanta/dist/vanta.waves.min.js';
import Zdog from 'zdog';
import VanillaTilt from 'vanilla-tilt';

// Use as before
```

---

## Advanced Examples

### Dynamic Effect Switching

```javascript
let effects = ['WAVES', 'BIRDS', 'NET'];
let currentEffect = 0;

document.getElementById('switchEffect').addEventListener('click', () => {
  vantaEffect.destroy();

  currentEffect = (currentEffect + 1) % effects.length;
  const effect = effects[currentEffect];

  if (effect === 'WAVES') {
    vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });
  } else if (effect === 'BIRDS') {
    vantaEffect = VANTA.BIRDS({ el: "#vanta-bg" });
  } else {
    vantaEffect = VANTA.NET({ el: "#vanta-bg" });
  }
});
```

### Synchronized Animations

```javascript
let masterTime = 0;

function animateAll() {
  masterTime += 0.02;

  // Sync hero cube
  heroCube.rotate.y = Math.sin(masterTime) * Math.PI;

  // Sync demo model
  demoModel.rotate.y = masterTime;

  // Update all
  heroIllo.updateRenderGraph();
  demoIllo.updateRenderGraph();

  requestAnimationFrame(animateAll);
}
animateAll();
```

### Scroll-Based Effects

```javascript
window.addEventListener('scroll', () => {
  const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);

  // Rotate demo model based on scroll
  demoModel.rotate.y = scrollPercent * Math.PI * 2;
  demoIllo.updateRenderGraph();

  // Change Vanta color
  const hue = Math.floor(scrollPercent * 360);
  const color = parseInt(`0x${hue.toString(16).padStart(6, '0')}`);
  vantaEffect.setOptions({ color });
});
```

---

## Resources

### Documentation
- **Vanta.js**: https://www.vantajs.com
- **Zdog**: https://zzz.dog
- **Vanilla-Tilt**: https://github.com/micku7zu/vanilla-tilt.js

### Inspiration
- **Vanta Gallery**: https://www.vantajs.com/?effect=waves
- **Zdog Examples**: https://codepen.io/desandro/
- **Tilt Patterns**: https://micku7zu.github.io/vanilla-tilt.js/

---

## License

This template is MIT licensed - free for personal and commercial use.

**Dependencies**:
- Three.js: MIT
- Vanta.js: MIT
- Zdog: MIT
- Vanilla-Tilt: MIT

---

## Support

For issues or questions:
1. Check browser console for errors
2. Review the [Common Issues](#common-issues) section
3. Consult official library documentation
4. Test in a different browser

---

**Built with ❤️ using lightweight 3D effects libraries**
