// Lightweight 3D Effects - Starter Template
// Combining Vanta.js, Zdog, and Vanilla-Tilt

console.log('Lightweight 3D Effects initialized');

// ============================================================================
// VANTA.JS BACKGROUND
// ============================================================================

let vantaEffect = VANTA.WAVES({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0x23153c,
  shininess: 30.00,
  waveHeight: 15.00,
  waveSpeed: 0.75,
  zoom: 0.65
});

console.log('Vanta.js background initialized');

// ============================================================================
// ZDOG ILLUSTRATIONS
// ============================================================================

// Hero Zdog Icon (Rotating Cube)
const heroIllo = new Zdog.Illustration({
  element: '.hero-zdog',
  zoom: 2,
  dragRotate: false
});

const heroCube = new Zdog.Box({
  addTo: heroIllo,
  width: 40,
  height: 40,
  depth: 40,
  stroke: 2,
  color: '#fff',
  fill: true,
  frontFace: '#667eea',
  rearFace: '#764ba2',
  leftFace: '#5568d3',
  rightFace: '#8568df',
  topFace: '#98d5e8',
  bottomFace: '#f093fb'
});

// Animate hero cube
function animateHeroCube() {
  heroCube.rotate.x += 0.01;
  heroCube.rotate.y += 0.02;
  heroIllo.updateRenderGraph();
  requestAnimationFrame(animateHeroCube);
}
animateHeroCube();

// ============================================================================
// Card Icon 1 - Vanta (Globe)
const icon1 = new Zdog.Illustration({
  element: '.zdog-icon-1',
  zoom: 2,
  dragRotate: false
});

// Globe with particles
const globe1 = new Zdog.Anchor({
  addTo: icon1
});

new Zdog.Ellipse({
  addTo: globe1,
  diameter: 40,
  stroke: 2,
  color: '#667eea',
});

new Zdog.Ellipse({
  addTo: globe1,
  diameter: 40,
  rotate: { y: Math.PI/2 },
  stroke: 2,
  color: '#764ba2',
});

// Particles around globe
for (let i = 0; i < 8; i++) {
  const angle = (i / 8) * Math.PI * 2;
  new Zdog.Ellipse({
    addTo: globe1,
    diameter: 4,
    translate: {
      x: Math.cos(angle) * 30,
      y: Math.sin(angle) * 30
    },
    stroke: 2,
    color: '#fff',
    fill: true
  });
}

function animateIcon1() {
  globe1.rotate.y += 0.03;
  icon1.updateRenderGraph();
  requestAnimationFrame(animateIcon1);
}
animateIcon1();

// ============================================================================
// Card Icon 2 - Zdog (3D Z)
const icon2 = new Zdog.Illustration({
  element: '.zdog-icon-2',
  zoom: 3,
  dragRotate: false
});

const zShape = new Zdog.Anchor({
  addTo: icon2
});

// Draw "Z" with 3D depth
new Zdog.Shape({
  addTo: zShape,
  path: [
    { x: -15, y: -15 },
    { x: 15, y: -15 },
    { x: -15, y: 15 },
    { x: 15, y: 15 }
  ],
  stroke: 8,
  color: '#667eea'
});

// Add depth layers
for (let i = 0; i < 5; i++) {
  new Zdog.Shape({
    addTo: zShape,
    path: [
      { x: -15, y: -15, z: -i*2 },
      { x: 15, y: -15, z: -i*2 },
      { x: -15, y: 15, z: -i*2 },
      { x: 15, y: 15, z: -i*2 }
    ],
    stroke: 8,
    color: `hsl(${240 + i*10}, 70%, ${60 - i*5}%)`
  });
}

function animateIcon2() {
  zShape.rotate.y += 0.02;
  zShape.rotate.x += 0.01;
  icon2.updateRenderGraph();
  requestAnimationFrame(animateIcon2);
}
animateIcon2();

// ============================================================================
// Card Icon 3 - Vanilla Tilt (Tilted Square)
const icon3 = new Zdog.Illustration({
  element: '.zdog-icon-3',
  zoom: 2,
  dragRotate: false
});

const tiltSquare = new Zdog.Anchor({
  addTo: icon3,
  rotate: { x: Math.PI/6, y: Math.PI/6 }
});

// Layered squares
for (let i = 0; i < 3; i++) {
  new Zdog.Rect({
    addTo: tiltSquare,
    width: 35 - i*5,
    height: 35 - i*5,
    translate: { z: i*10 },
    stroke: 3,
    color: `hsl(${240 + i*30}, 70%, 60%)`,
    fill: true
  });
}

// Subtle rotation
function animateIcon3() {
  tiltSquare.rotate.y += 0.01;
  icon3.updateRenderGraph();
  requestAnimationFrame(animateIcon3);
}
animateIcon3();

// ============================================================================
// Demo Zdog (Interactive)
const demoIllo = new Zdog.Illustration({
  element: '.demo-zdog',
  zoom: 2,
  dragRotate: true,
  onDragStart: function() {
    isSpinning = false;
  }
});

let isSpinning = true;
let currentColor = '#667eea';

// Create complex 3D model
const demoModel = new Zdog.Anchor({
  addTo: demoIllo
});

// Center sphere
const centerSphere = new Zdog.Hemisphere({
  addTo: demoModel,
  diameter: 40,
  stroke: 5,
  color: currentColor,
  fill: true
});

// Orbiting elements
const orbitRadius = 60;
const orbitCount = 6;
const orbitingShapes = [];

for (let i = 0; i < orbitCount; i++) {
  const angle = (i / orbitCount) * Math.PI * 2;

  const orbitAnchor = new Zdog.Anchor({
    addTo: demoModel,
    rotate: { y: angle }
  });

  const shape = new Zdog.Box({
    addTo: orbitAnchor,
    width: 15,
    height: 15,
    depth: 15,
    translate: { z: orbitRadius },
    stroke: 2,
    color: `hsl(${(i / orbitCount) * 360}, 70%, 60%)`,
    fill: true
  });

  orbitingShapes.push({ anchor: orbitAnchor, shape: shape, angle: angle });
}

// Animation
let time = 0;
function animateDemo() {
  time += 0.02;

  if (isSpinning) {
    demoModel.rotate.y += 0.02;
  }

  // Animate orbiting shapes
  orbitingShapes.forEach((item, i) => {
    const wave = Math.sin(time + item.angle) * 10;
    item.shape.translate.z = orbitRadius + wave;
    item.shape.rotate.x += 0.03;
    item.shape.rotate.y += 0.02;
  });

  demoIllo.updateRenderGraph();
  requestAnimationFrame(animateDemo);
}
animateDemo();

// ============================================================================
// VANILLA TILT
// ============================================================================

VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
  max: 15,
  speed: 400,
  glare: true,
  "max-glare": 0.3,
  scale: 1.03,
  perspective: 1000
});

console.log('Vanilla Tilt initialized');

// ============================================================================
// DEMO CONTROLS
// ============================================================================

document.getElementById('toggleSpin').addEventListener('click', function() {
  isSpinning = !isSpinning;
  this.textContent = isSpinning ? 'Pause' : 'Play';
});

document.getElementById('changeColor').addEventListener('click', function() {
  // Generate random color
  const hue = Math.floor(Math.random() * 360);
  currentColor = `hsl(${hue}, 70%, 60%)`;
  centerSphere.color = currentColor;

  // Randomize orbiting shapes
  orbitingShapes.forEach(item => {
    const randomHue = Math.floor(Math.random() * 360);
    item.shape.color = `hsl(${randomHue}, 70%, 60%)`;
  });
});

document.getElementById('resetView').addEventListener('click', function() {
  demoModel.rotate.x = 0;
  demoModel.rotate.y = 0;
  demoModel.rotate.z = 0;
  isSpinning = true;
  document.getElementById('toggleSpin').textContent = 'Pause';
});

// ============================================================================
// CARD BUTTON INTERACTIONS
// ============================================================================

document.querySelectorAll('.card-btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.stopPropagation(); // Prevent tilt effect from interfering

    const card = this.closest('.card');
    const cardTitle = card.querySelector('h2').textContent;

    console.log(`Button clicked: ${cardTitle}`);

    // Add visual feedback
    this.style.transform = 'translateZ(40px) scale(0.95)';
    setTimeout(() => {
      this.style.transform = 'translateZ(40px) scale(1)';
    }, 100);

    // You can add navigation or modal logic here
    alert(`Learn more about ${cardTitle}!`);
  });
});

// ============================================================================
// RESPONSIVE HANDLING
// ============================================================================

// Disable tilt on mobile for better performance
if (window.innerWidth < 768) {
  document.querySelectorAll('.tilt-card').forEach(card => {
    if (card.vanillaTilt) {
      card.vanillaTilt.destroy();
    }
  });
  console.log('Tilt disabled on mobile');
}

// Resize handler for Vanta
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (vantaEffect && vantaEffect.resize) {
      vantaEffect.resize();
    }
  }, 250);
});

// ============================================================================
// CLEANUP ON PAGE UNLOAD
// ============================================================================

window.addEventListener('beforeunload', () => {
  if (vantaEffect && vantaEffect.destroy) {
    vantaEffect.destroy();
  }

  document.querySelectorAll('.tilt-card').forEach(card => {
    if (card.vanillaTilt) {
      card.vanillaTilt.destroy();
    }
  });

  console.log('Effects cleaned up');
});

// ============================================================================
// PERFORMANCE MONITORING
// ============================================================================

if (typeof performance !== 'undefined' && performance.now) {
  const startTime = performance.now();

  window.addEventListener('load', () => {
    const loadTime = performance.now() - startTime;
    console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
  });
}

console.log('All effects initialized successfully');
