# Zdog API Reference

Complete API documentation for Zdog - a pseudo-3D engine for canvas and SVG.

**Version**: 1.1.3
**License**: MIT
**CDN**: `https://unpkg.com/zdog@1/dist/zdog.dist.min.js`

---

## Table of Contents

1. [Core Classes](#core-classes)
2. [Shape Types](#shape-types)
3. [Properties](#properties)
4. [Methods](#methods)
5. [Animation](#animation)
6. [Advanced Techniques](#advanced-techniques)

---

## Core Classes

### Zdog.Illustration

The root display object that manages the scene and rendering.

```javascript
let illo = new Zdog.Illustration({
  element: '.zdog-canvas',  // CSS selector or DOM element
  zoom: 4,                  // Scale multiplier
  dragRotate: false,        // Enable drag-to-rotate
  resize: false,            // Auto-resize to element
  centered: true,           // Center origin
  onDragStart: function() {},
  onDragMove: function() {},
  onDragEnd: function() {},
  onResize: function(width, height) {}
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `element` | String\|Element | Required | Canvas or SVG element |
| `zoom` | Number | 1 | Scale multiplier |
| `dragRotate` | Boolean\|Zdog.Anchor | false | Enable drag rotation |
| `resize` | Boolean | false | Auto-resize to fit element |
| `centered` | Boolean | true | Center scene at origin |
| `rotate` | Zdog.Vector | {x:0,y:0,z:0} | Rotation in radians |
| `translate` | Zdog.Vector | {x:0,y:0,z:0} | Position offset |

#### Methods

```javascript
// Render scene
illo.updateRenderGraph();

// Update size
illo.setSize(width, height);
```

---

### Zdog.Anchor

Group container for organizing and transforming child shapes.

```javascript
let group = new Zdog.Anchor({
  addTo: illo,
  translate: { x: 0, y: 0, z: 0 },
  rotate: { x: 0, y: 0, z: 0 },
  scale: 1
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `addTo` | Zdog.Anchor | null | Parent object |
| `translate` | Object | {x:0,y:0,z:0} | Position |
| `rotate` | Object | {x:0,y:0,z:0} | Rotation (radians) |
| `scale` | Number\|Object | 1 | Uniform or {x,y,z} scale |

#### Methods

```javascript
// Add child
group.addChild(shape);

// Remove child
group.removeChild(shape);

// Remove from parent
group.remove();

// Copy all properties
let copy = group.copy();

// Copy with options
let copy = group.copyGraph({
  translate: { x: 10 }
});
```

---

### Zdog.Shape

Base class for all rendered shapes (usually not used directly).

```javascript
let shape = new Zdog.Shape({
  addTo: group,
  stroke: 1,
  fill: false,
  color: '#333',
  visible: true,
  backface: true
});
```

#### Common Shape Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `stroke` | Number | 1 | Line thickness |
| `fill` | Boolean | false | Fill shape interior |
| `color` | String | '#333' | CSS color value |
| `visible` | Boolean | true | Render visibility |
| `backface` | Boolean\|String | true | Show back face / color |
| `front` | Object | {z:0} | Front face offset |
| `closed` | Boolean | true | Close path |

---

## Shape Types

### Ellipse

Circle or ellipse shape.

```javascript
new Zdog.Ellipse({
  addTo: illo,
  diameter: 80,        // Circle
  // OR
  width: 80,           // Ellipse width
  height: 40,          // Ellipse height
  quarters: 4,         // Number of curve segments
  stroke: 20,
  color: '#636',
  fill: true
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `diameter` | Number | 1 | Circle diameter |
| `width` | Number | diameter | Ellipse width |
| `height` | Number | diameter | Ellipse height |
| `quarters` | Number | 4 | Bezier curve segments (4 = smooth) |

---

### Rect

Rectangle shape.

```javascript
new Zdog.Rect({
  addTo: illo,
  width: 80,
  height: 60,
  stroke: 2,
  color: '#E62',
  fill: true
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `width` | Number | 1 | Rectangle width |
| `height` | Number | 1 | Rectangle height |

---

### RoundedRect

Rectangle with rounded corners.

```javascript
new Zdog.RoundedRect({
  addTo: illo,
  width: 80,
  height: 60,
  cornerRadius: 10,
  stroke: 2,
  color: '#E62',
  fill: true
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `width` | Number | 1 | Rectangle width |
| `height` | Number | 1 | Rectangle height |
| `cornerRadius` | Number | 0 | Corner curve radius |

---

### Polygon

Multi-sided polygon shape.

```javascript
// Triangle
new Zdog.Polygon({
  addTo: illo,
  sides: 3,
  radius: 40,
  stroke: 2,
  color: '#EA0',
  fill: true
});

// Pentagon
new Zdog.Polygon({
  sides: 5,
  radius: 40
});

// Star (using path hack)
new Zdog.Polygon({
  sides: 5,
  radius: 40,
  rotate: { z: -Math.PI/2 }
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `sides` | Number | 3 | Number of sides |
| `radius` | Number | 1 | Distance from center |

---

### Line

Straight line segment.

```javascript
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -40, y: 0, z: 0 },  // Start point
    { x: 40, y: 0, z: 0 }    // End point
  ],
  stroke: 4,
  color: '#636'
});
```

---

### Bezier

Bezier curve path.

```javascript
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -40, y: 0 },           // Start
    {
      bezier: [
        { x: -20, y: -40 },     // Control point 1
        { x: 20, y: -40 },      // Control point 2
        { x: 40, y: 0 }         // End point
      ]
    }
  ],
  stroke: 4,
  color: '#E62'
});
```

---

### Hemisphere

Half-sphere shape.

```javascript
new Zdog.Hemisphere({
  addTo: illo,
  diameter: 80,
  stroke: 5,
  color: '#EA0',
  fill: true,
  // Render semi-circles
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `diameter` | Number | 1 | Sphere diameter |

---

### Cylinder

Cylindrical shape.

```javascript
new Zdog.Cylinder({
  addTo: illo,
  diameter: 80,
  length: 120,
  stroke: 5,
  color: '#636',
  fill: true,
  frontFace: '#EA0',   // Front cap color
  backface: '#E62'     // Back cap color
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `diameter` | Number | 1 | Cylinder diameter |
| `length` | Number | 1 | Cylinder length (depth) |
| `frontFace` | String\|Boolean | true | Front cap color |

---

### Cone

Conical shape.

```javascript
new Zdog.Cone({
  addTo: illo,
  diameter: 80,
  length: 120,
  stroke: 5,
  color: '#636',
  fill: true,
  backface: '#E62'
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `diameter` | Number | 1 | Base diameter |
| `length` | Number | 1 | Cone height |

---

### Box

3D box shape (composed of rectangles).

```javascript
new Zdog.Box({
  addTo: illo,
  width: 80,
  height: 100,
  depth: 60,
  stroke: 2,
  color: '#C25',
  fill: true,
  frontFace: '#EA0',
  rearFace: '#E62',
  leftFace: '#636',
  rightFace: '#C25',
  topFace: '#EA0',
  bottomFace: '#E62'
});
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `width` | Number | 1 | Box width (x-axis) |
| `height` | Number | 1 | Box height (y-axis) |
| `depth` | Number | 1 | Box depth (z-axis) |
| `frontFace` | String\|Boolean | true | Front face color |
| `rearFace` | String\|Boolean | true | Rear face color |
| `leftFace` | String\|Boolean | true | Left face color |
| `rightFace` | String\|Boolean | true | Right face color |
| `topFace` | String\|Boolean | true | Top face color |
| `bottomFace` | String\|Boolean | true | Bottom face color |

---

## Properties

### Transform Properties

Available on all Zdog.Anchor and Zdog.Shape objects.

#### translate

Position in 3D space.

```javascript
shape.translate = { x: 0, y: 0, z: 0 };
shape.translate.x = 10;
shape.translate.y += 5;
```

#### rotate

Rotation in radians around each axis.

```javascript
shape.rotate = { x: 0, y: 0, z: 0 };
shape.rotate.y = Math.PI / 4;  // 45 degrees
shape.rotate.z += 0.03;        // Incremental
```

**Helper**: Convert degrees to radians
```javascript
const TAU = Math.PI * 2;
let degrees = 90;
let radians = degrees / 360 * TAU;
```

#### scale

Uniform or per-axis scaling.

```javascript
// Uniform scale
shape.scale = 2;

// Per-axis scale
shape.scale = { x: 1, y: 2, z: 1 };
```

---

### Appearance Properties

#### color

CSS color string.

```javascript
shape.color = '#E62';
shape.color = 'rgb(255, 100, 50)';
shape.color = 'hsl(200, 100%, 50%)';
```

#### stroke

Line thickness.

```javascript
shape.stroke = 10;
```

#### fill

Fill interior of closed shapes.

```javascript
shape.fill = true;
```

#### visible

Control rendering visibility.

```javascript
shape.visible = false;  // Hidden but still in scene
```

#### backface

Control back face rendering.

```javascript
// Show back face with same color
shape.backface = true;

// Hide back face
shape.backface = false;

// Different back face color
shape.backface = '#EA0';
```

---

## Methods

### Rendering

#### updateRenderGraph()

Update and render the entire scene graph.

```javascript
function animate() {
  illo.rotate.y += 0.03;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

**Important**: Must call on root Illustration, not individual shapes.

---

### Hierarchy

#### addChild(shape)

Add a child shape to an anchor.

```javascript
let group = new Zdog.Anchor({ addTo: illo });
let shape = new Zdog.Ellipse({ diameter: 40 });
group.addChild(shape);
```

#### removeChild(shape)

Remove a child from an anchor.

```javascript
group.removeChild(shape);
```

#### remove()

Remove shape from its parent.

```javascript
shape.remove();
```

---

### Copying

#### copy(options)

Create a duplicate of a shape.

```javascript
let original = new Zdog.Ellipse({
  addTo: illo,
  diameter: 40,
  color: '#636'
});

let duplicate = original.copy({
  translate: { x: 50 },
  color: '#E62'
});
```

#### copyGraph(options)

Copy shape including all children.

```javascript
let group = new Zdog.Anchor({ addTo: illo });
// ... add children ...

let groupCopy = group.copyGraph({
  translate: { x: 100 }
});
```

---

## Animation

### Basic Animation Loop

```javascript
let illo = new Zdog.Illustration({
  element: '.zdog-canvas'
});

let shape = new Zdog.Ellipse({
  addTo: illo,
  diameter: 80,
  stroke: 20,
  color: '#636'
});

function animate() {
  // Update properties
  shape.rotate.y += 0.03;

  // Render
  illo.updateRenderGraph();

  // Loop
  requestAnimationFrame(animate);
}

animate();
```

---

### Rotation Animation

```javascript
// Continuous rotation
function animate() {
  illo.rotate.y += 0.03;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}

// Rotate specific shape
function animate() {
  shape.rotate.z += 0.05;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}

// Multi-axis rotation
function animate() {
  shape.rotate.x += 0.02;
  shape.rotate.y += 0.03;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Position Animation

```javascript
let time = 0;

function animate() {
  time += 0.05;

  // Sine wave motion
  shape.translate.y = Math.sin(time) * 40;

  // Circular motion
  shape.translate.x = Math.cos(time) * 50;
  shape.translate.y = Math.sin(time) * 50;

  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Scale Animation

```javascript
let time = 0;

function animate() {
  time += 0.05;

  // Pulsing scale
  let scale = 1 + Math.sin(time) * 0.3;
  shape.scale = scale;

  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Color Animation

Zdog doesn't support direct color interpolation. Use external libraries or manual RGB interpolation.

```javascript
// Manual RGB interpolation
function lerpColor(color1, color2, t) {
  let r1 = parseInt(color1.substr(1,2), 16);
  let g1 = parseInt(color1.substr(3,2), 16);
  let b1 = parseInt(color1.substr(5,2), 16);

  let r2 = parseInt(color2.substr(1,2), 16);
  let g2 = parseInt(color2.substr(3,2), 16);
  let b2 = parseInt(color2.substr(5,2), 16);

  let r = Math.round(r1 + (r2 - r1) * t);
  let g = Math.round(g1 + (g2 - g1) * t);
  let b = Math.round(b1 + (b2 - b1) * t);

  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

let time = 0;
function animate() {
  time += 0.05;
  let t = (Math.sin(time) + 1) / 2;  // 0 to 1
  shape.color = lerpColor('#636', '#E62', t);

  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Easing

Use easing functions for smooth animations.

```javascript
// Easing functions
const easing = {
  linear: t => t,
  easeInOut: t => t < 0.5
    ? 2 * t * t
    : -1 + (4 - 2 * t) * t,
  easeOut: t => t * (2 - t),
  easeIn: t => t * t
};

// Animate with easing
let progress = 0;
function animate() {
  progress += 0.01;
  if (progress > 1) progress = 0;

  let eased = easing.easeInOut(progress);
  shape.translate.x = eased * 100 - 50;

  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Interactive Animation

```javascript
let isDragging = false;

let illo = new Zdog.Illustration({
  element: '.zdog-canvas',
  dragRotate: true,
  onDragStart: function() {
    isDragging = true;
  },
  onDragEnd: function() {
    isDragging = false;
  }
});

// Auto-rotate when not dragging
function animate() {
  if (!isDragging) {
    illo.rotate.y += 0.01;
  }
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

## Advanced Techniques

### Custom Paths

Create complex shapes using path arrays.

```javascript
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: 0, y: -40 },           // Start point
    { x: 40, y: 0 },            // Line to
    { x: 0, y: 40 },            // Line to
    { x: -40, y: 0 },           // Line to
  ],
  closed: true,
  stroke: 4,
  color: '#636',
  fill: true
});
```

---

### Bezier Curves

```javascript
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -60, y: 0 },
    {
      bezier: [
        { x: -30, y: -60 },    // Control 1
        { x: 30, y: -60 },     // Control 2
        { x: 60, y: 0 }        // End point
      ]
    },
    {
      bezier: [
        { x: 30, y: 60 },
        { x: -30, y: 60 },
        { x: -60, y: 0 }
      ]
    }
  ],
  closed: true,
  stroke: 4,
  color: '#E62',
  fill: true
});
```

---

### Arc Curves

```javascript
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -40, y: 0 },
    {
      arc: [
        { x: 0, y: -40 },      // Corner
        { x: 40, y: 0 }        // End
      ]
    }
  ],
  stroke: 4,
  color: '#636'
});
```

---

### Complex Models

Build complex 3D objects using groups.

```javascript
// Robot example
let robot = new Zdog.Anchor({
  addTo: illo,
  translate: { y: -40 }
});

// Head
new Zdog.Box({
  addTo: robot,
  width: 40,
  height: 40,
  depth: 40,
  stroke: 2,
  color: '#636',
  topFace: '#EA0',
  bottomFace: '#E62'
});

// Body
new Zdog.Box({
  addTo: robot,
  translate: { y: 50 },
  width: 50,
  height: 60,
  depth: 40,
  stroke: 2,
  color: '#636'
});

// Arms (group for symmetry)
[-1, 1].forEach(xSide => {
  new Zdog.Box({
    addTo: robot,
    translate: { x: xSide * 40, y: 50 },
    width: 20,
    height: 60,
    depth: 20,
    stroke: 2,
    color: '#C25'
  });
});

// Legs
[-1, 1].forEach(xSide => {
  new Zdog.Box({
    addTo: robot,
    translate: { x: xSide * 15, y: 100 },
    width: 20,
    height: 60,
    depth: 20,
    stroke: 2,
    color: '#C25'
  });
});

// Animate
function animate() {
  robot.rotate.y += 0.03;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();
```

---

### Instancing

Efficiently create multiple copies.

```javascript
// Create template
let sphere = new Zdog.Hemisphere({
  diameter: 20,
  stroke: 2,
  color: '#636',
  fill: true
});

// Instance grid
for (let x = -100; x <= 100; x += 40) {
  for (let y = -100; y <= 100; y += 40) {
    sphere.copy({
      addTo: illo,
      translate: { x, y },
      color: `hsl(${(x+100)/2}, 70%, 50%)`
    });
  }
}
```

---

### Responsive Sizing

Make Zdog canvas responsive to container.

```javascript
let illo = new Zdog.Illustration({
  element: '.zdog-canvas',
  resize: true,
  onResize: function(width, height) {
    // Adjust zoom based on size
    this.zoom = Math.min(width, height) / 200;
  }
});

// Manual resize handling
function handleResize() {
  let container = document.querySelector('.zdog-container');
  illo.setSize(container.offsetWidth, container.offsetHeight);
}

window.addEventListener('resize', handleResize);
handleResize();
```

---

### Performance Optimization

**1. Limit Update Frequency**

```javascript
let needsUpdate = false;

element.addEventListener('mousemove', () => {
  needsUpdate = true;
});

function animate() {
  if (needsUpdate) {
    illo.updateRenderGraph();
    needsUpdate = false;
  }
  requestAnimationFrame(animate);
}
```

**2. Use Visibility**

```javascript
// Hide off-screen objects
shapes.forEach(shape => {
  shape.visible = isInView(shape);
});
```

**3. Throttle Drag Rotation**

```javascript
let lastUpdate = 0;

let illo = new Zdog.Illustration({
  element: '.zdog-canvas',
  dragRotate: true,
  onDragMove: function() {
    const now = Date.now();
    if (now - lastUpdate > 16) {  // ~60fps
      this.updateRenderGraph();
      lastUpdate = now;
    }
  }
});
```

---

### SVG vs Canvas

**Canvas** (default):
- Better performance
- Smaller file size
- Rasterized output

```javascript
let illo = new Zdog.Illustration({
  element: 'canvas'  // Canvas element
});
```

**SVG**:
- Vector output (scalable)
- Accessible/indexable
- Slower performance

```javascript
let illo = new Zdog.Illustration({
  element: 'svg'  // SVG element
});
```

---

### Coordinate System

Zdog uses a right-handed coordinate system:

- **X-axis**: Right (+) / Left (-)
- **Y-axis**: Down (+) / Up (-)
- **Z-axis**: Forward (+) / Back (-)

```javascript
// Move right
shape.translate.x = 50;

// Move up
shape.translate.y = -50;

// Move forward
shape.translate.z = 50;
```

---

### Rotation Order

Rotations apply in ZYX order (z-axis first, then y, then x).

```javascript
shape.rotate = {
  x: Math.PI / 4,   // Pitch (applied last)
  y: Math.PI / 6,   // Yaw (applied second)
  z: Math.PI / 8    // Roll (applied first)
};
```

---

## Common Patterns

### Clickable Shapes

Zdog doesn't have built-in click detection. Use canvas coordinates.

```javascript
let canvas = document.querySelector('canvas');

canvas.addEventListener('click', (event) => {
  let rect = canvas.getBoundingClientRect();
  let x = event.clientX - rect.left;
  let y = event.clientY - rect.top;

  // Check if click is near shape (approximate)
  let shapeX = shape.translate.x * illo.zoom + canvas.width / 2;
  let shapeY = shape.translate.y * illo.zoom + canvas.height / 2;

  let distance = Math.sqrt(
    Math.pow(x - shapeX, 2) +
    Math.pow(y - shapeY, 2)
  );

  if (distance < 50) {
    console.log('Shape clicked!');
  }
});
```

---

### Sprite Sheets

Animate through multiple Zdog illustrations.

```javascript
let frames = [];

// Create frames
for (let i = 0; i < 10; i++) {
  let illo = new Zdog.Illustration({
    element: '.canvas',
    zoom: 4
  });

  let shape = new Zdog.Ellipse({
    addTo: illo,
    diameter: 20,
    rotate: { y: i * Math.PI / 10 }
  });

  illo.updateRenderGraph();
  frames.push(illo);
}

// Play frames
let currentFrame = 0;
function animate() {
  currentFrame = (currentFrame + 1) % frames.length;
  frames[currentFrame].updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

### Particle Systems

Create simple particle effects.

```javascript
let particles = [];

for (let i = 0; i < 50; i++) {
  particles.push({
    shape: new Zdog.Ellipse({
      addTo: illo,
      diameter: 4,
      stroke: 2,
      color: '#636'
    }),
    velocity: {
      x: (Math.random() - 0.5) * 4,
      y: (Math.random() - 0.5) * 4
    }
  });
}

function animate() {
  particles.forEach(p => {
    p.shape.translate.x += p.velocity.x;
    p.shape.translate.y += p.velocity.y;

    // Bounce off edges
    if (Math.abs(p.shape.translate.x) > 100) {
      p.velocity.x *= -1;
    }
    if (Math.abs(p.shape.translate.y) > 100) {
      p.velocity.y *= -1;
    }
  });

  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
```

---

## TypeScript Support

Zdog includes TypeScript definitions.

```typescript
import Zdog from 'zdog';

const illo: Zdog.Illustration = new Zdog.Illustration({
  element: '.zdog-canvas',
  zoom: 4
});

const shape: Zdog.Ellipse = new Zdog.Ellipse({
  addTo: illo,
  diameter: 80,
  stroke: 20,
  color: '#636'
});
```

---

## Browser Support

- Chrome: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Edge: ✅ Full support
- IE11: ⚠️ Requires polyfills

---

## Resources

- **Official Site**: https://zzz.dog
- **GitHub**: https://github.com/metafizzy/zdog
- **CodePen Examples**: https://codepen.io/desandro/
- **NPM**: `npm install zdog`

---

## License

MIT License - Free for commercial and personal use.
