# PixiJS API Reference

Complete API reference for PixiJS v8+ core classes and methods.

---

## Table of Contents

1. [Application](#application)
2. [Sprite](#sprite)
3. [Texture](#texture)
4. [Graphics](#graphics)
5. [Container](#container)
6. [ParticleContainer](#particlecontainer)
7. [Filters](#filters)
8. [Text](#text)
9. [Assets](#assets)
10. [Renderer](#renderer)
11. [DisplayObject](#displayobject)
12. [Events](#events)

---

## Application

Core application class that manages the renderer, stage, and update loop.

### Constructor

```typescript
new Application()
```

### Methods

#### `init(options)`

Initialize the application with configuration options.

```typescript
await app.init({
  width: 800,
  height: 600,
  backgroundColor: 0x1099bb,
  backgroundAlpha: 1,
  antialias: true,
  resolution: window.devicePixelRatio || 1,
  autoDensity: true,
  powerPreference: 'high-performance',
  hello: true  // Show PixiJS banner in console
});
```

**Options**:
- `width: number` - Canvas width (default: 800)
- `height: number` - Canvas height (default: 600)
- `backgroundColor: number` - Background color (default: 0x000000)
- `backgroundAlpha: number` - Background alpha 0-1 (default: 1)
- `antialias: boolean` - Enable antialiasing (default: false)
- `resolution: number` - Device pixel ratio (default: 1)
- `autoDensity: boolean` - Adjust CSS pixel size automatically
- `powerPreference: string` - 'high-performance' | 'low-power' | 'default'
- `hello: boolean` - Show PixiJS banner (default: false)

#### `destroy(removeView, stageOptions)`

Destroy the application and release resources.

```typescript
app.destroy(true, { children: true, texture: true });
```

**Parameters**:
- `removeView: boolean` - Remove canvas from DOM (default: false)
- `stageOptions: object` - Options for stage destruction
  - `children: boolean` - Destroy all children
  - `texture: boolean` - Destroy textures
  - `baseTexture: boolean` - Destroy base textures

#### `resizeCanvas()`

Resize canvas to fill window.

```typescript
window.addEventListener('resize', () => {
  app.resizeCanvas();
});
```

### Properties

```typescript
app.stage: Container          // Root display object container
app.renderer: Renderer        // WebGL/WebGPU renderer instance
app.ticker: Ticker            // Update loop manager
app.canvas: HTMLCanvasElement // Canvas element
app.screen: Rectangle         // Screen dimensions
app.view: HTMLCanvasElement   // Alias for canvas (deprecated)
```

### Plugins

```typescript
// Ticker Plugin - manages update loop
app.ticker.add((ticker) => {
  // Update logic
  sprite.rotation += 0.01 * ticker.deltaTime;
});

app.ticker.stop();
app.ticker.start();
app.ticker.speed = 0.5;  // Half speed

// Resize Plugin
app.resizeTo = window;  // Auto-resize to window

// Culler Plugin - automatic viewport culling
app.cullable = true;
```

**API References**:
- TickerPlugin: https://pixijs.download/release/docs/app.TickerPlugin.html
- ResizePlugin: https://pixijs.download/release/docs/app.ResizePlugin.html
- CullerPlugin: https://pixijs.download/release/docs/app.CullerPlugin.html

---

## Sprite

Visual element that displays a texture.

### Constructor

```typescript
new Sprite(texture: Texture)
Sprite.from(source: string | Texture)  // Convenience method
```

### Properties

```typescript
sprite.texture: Texture       // The texture to display
sprite.anchor: ObservablePoint // Pivot point (0-1, default: 0,0)
sprite.tint: number           // Color tint (0xRRGGBB)
sprite.blendMode: BLEND_MODES // How sprite blends with background

// Transform properties (inherited from DisplayObject)
sprite.position: ObservablePoint  // x, y position
sprite.scale: ObservablePoint     // x, y scale
sprite.rotation: number           // Rotation in radians
sprite.pivot: ObservablePoint     // Rotation pivot point
sprite.skew: ObservablePoint      // x, y skew

// Visibility
sprite.alpha: number              // Opacity (0-1)
sprite.visible: boolean           // Show/hide
sprite.renderable: boolean        // Should render

// Interaction
sprite.eventMode: string          // 'none' | 'passive' | 'static' | 'dynamic'
sprite.cursor: string             // CSS cursor
sprite.hitArea: Rectangle | Circle | Polygon  // Custom hit area

// Performance
sprite.cullable: boolean          // Enable viewport culling
sprite.cacheAsBitmap: boolean     // Convert to texture for performance
```

### Methods

```typescript
// Anchor
sprite.anchor.set(x, y)
sprite.anchor.set(0.5)  // Center (shorthand)

// Position
sprite.position.set(x, y)
sprite.setTransform(x, y, scaleX, scaleY, rotation, skewX, skewY, pivotX, pivotY)

// Bounds
sprite.getBounds()
sprite.getLocalBounds()

// Destroy
sprite.destroy({ children: true, texture: false, baseTexture: false })
```

### Example

```typescript
import { Sprite, Texture } from 'pixi.js';

const texture = Texture.from('bunny.png');
const sprite = new Sprite(texture);

sprite.anchor.set(0.5);
sprite.position.set(400, 300);
sprite.scale.set(2);
sprite.rotation = Math.PI / 4;
sprite.tint = 0xff0000;
sprite.alpha = 0.8;

app.stage.addChild(sprite);
```

---

## Texture

Image data that can be rendered by Sprites and Graphics.

### Static Methods

```typescript
Texture.from(source: string | HTMLImageElement | HTMLCanvasElement)
Texture.fromURL(url: string, options?: object)
Texture.fromBuffer(buffer: Uint8Array, width: number, height: number)
```

### Properties

```typescript
texture.width: number           // Texture width
texture.height: number          // Texture height
texture.baseTexture: BaseTexture  // Underlying GPU texture
texture.frame: Rectangle        // Region of baseTexture to use
texture.source: TextureSource   // Source data
```

### Methods

```typescript
texture.destroy(destroyBase?: boolean)
texture.update()                // Update from source
texture.clone()                 // Create copy
```

### Example

```typescript
import { Texture, Assets } from 'pixi.js';

// Load texture
const texture = await Assets.load('image.png');

// From URL
const tex = Texture.from('https://example.com/image.png');

// From canvas
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
// ... draw on canvas
const canvasTex = Texture.from(canvas);

// Destroy
texture.destroy(true);  // Also destroy baseTexture
```

**API Reference**: https://pixijs.download/release/docs/rendering.Texture.html

---

## Graphics

API for drawing vector shapes programmatically.

### Constructor

```typescript
new Graphics()
new Graphics(context: GraphicsContext)  // Share geometry
```

### Shape Methods

All shape methods return `this` for chaining.

```typescript
graphics.rect(x, y, width, height)
graphics.circle(x, y, radius)
graphics.ellipse(x, y, radiusX, radiusY)
graphics.roundRect(x, y, width, height, radius)
graphics.poly(points: number[] | Point[])
graphics.star(x, y, points, radius, innerRadius?, rotation?)
```

### Path Methods

```typescript
graphics.moveTo(x, y)
graphics.lineTo(x, y)
graphics.bezierCurveTo(cpX, cpY, cpX2, cpY2, toX, toY)
graphics.quadraticCurveTo(cpX, cpY, toX, toY)
graphics.arcTo(x1, y1, x2, y2, radius)
graphics.arc(x, y, radius, startAngle, endAngle, anticlockwise?)
graphics.closePath()
```

### Fill & Stroke

```typescript
// Fill
graphics.fill(color: number | string)
graphics.fill({ color, alpha })
graphics.fill(texture: Texture)

// Stroke
graphics.stroke({ width, color, alpha, alignment, cap, join })

// Options
{
  width: number,          // Line width
  color: number | string, // Line color
  alpha: number,          // Line opacity (0-1)
  alignment: number,      // 0=inner, 0.5=middle, 1=outer
  cap: string,            // 'butt' | 'round' | 'square'
  join: string            // 'miter' | 'round' | 'bevel'
}
```

### Holes

```typescript
graphics.rect(0, 0, 100, 100).fill('red')
  .beginHole()
  .circle(50, 50, 20)
  .endHole();
```

### SVG Support

```typescript
graphics.svg('<svg><path d="M 100 350 q 150 -300 300 0" /></svg>');
```

### Other Methods

```typescript
graphics.clear()                    // Remove all shapes
graphics.clone()                    // Create copy
graphics.destroy(options)           // Destroy and release memory

// Context sharing
const context = new GraphicsContext().circle(50, 50, 30).fill('red');
const g1 = new Graphics(context);
const g2 = new Graphics(context);  // Shares same geometry
```

### Properties

```typescript
graphics.context: GraphicsContext   // Drawing instructions
graphics.pixelLine: boolean         // Force 1px line width regardless of scale
graphics.fillStyle: FillStyle       // Current fill style
graphics.lineStyle: StrokeStyle     // Current line style
```

### Example

```typescript
import { Graphics } from 'pixi.js';

const graphics = new Graphics();

// Rectangle with gradient
graphics.rect(50, 50, 200, 100).fill({ color: 0x3399ff, alpha: 0.8 });

// Circle with stroke
graphics.circle(400, 300, 80)
  .fill('yellow')
  .stroke({ width: 4, color: 'orange' });

// Star
graphics.star(600, 300, 5, 50).fill(0xffdf00);

// Custom path
graphics
  .moveTo(100, 400)
  .bezierCurveTo(150, 300, 250, 300, 300, 400)
  .stroke({ width: 3, color: 'white' });

// Hole
graphics.rect(450, 400, 150, 100).fill('red')
  .beginHole()
  .circle(525, 450, 30)
  .endHole();

app.stage.addChild(graphics);
```

**API References**:
- Graphics: https://pixijs.download/release/docs/scene.Graphics.html
- GraphicsContext: https://pixijs.download/release/docs/scene.GraphicsContext.html
- FillStyle: https://pixijs.download/release/docs/scene.FillStyle.html
- StrokeStyle: https://pixijs.download/release/docs/scene.StrokeStyle.html

---

## Container

Display object that can contain children (like a group).

### Constructor

```typescript
new Container()
```

### Children Management

```typescript
container.addChild(child: DisplayObject)
container.addChildAt(child: DisplayObject, index: number)
container.removeChild(child: DisplayObject)
container.removeChildAt(index: number)
container.removeChildren(beginIndex?, endIndex?)
container.getChildAt(index: number)
container.getChildIndex(child: DisplayObject)
container.setChildIndex(child: DisplayObject, index: number)
container.swapChildren(child1: DisplayObject, child2: DisplayObject)
```

### Properties

```typescript
container.children: DisplayObject[]  // Array of children
container.width: number               // Combined width of children
container.height: number              // Combined height of children
container.sortableChildren: boolean   // Enable z-index sorting
container.interactiveChildren: boolean // Enable child interaction
```

### Filters

```typescript
container.filters: Filter[]          // Array of filters
container.filterArea: Rectangle      // Filter bounding box
```

### Iteration

```typescript
for (const child of container.children) {
  // Process child
}

container.children.forEach(child => {
  // Process child
});
```

### Example

```typescript
import { Container, Sprite } from 'pixi.js';

const container = new Container();
container.position.set(100, 100);

// Add children
const sprite1 = Sprite.from('image1.png');
const sprite2 = Sprite.from('image2.png');
sprite2.x = 50;

container.addChild(sprite1, sprite2);

// Z-index sorting
container.sortableChildren = true;
sprite1.zIndex = 2;
sprite2.zIndex = 1;  // Renders behind sprite1

app.stage.addChild(container);
```

---

## ParticleContainer

Optimized container for rendering thousands of sprites with limited transform capabilities.

### Constructor

```typescript
new ParticleContainer(options?: ParticleContainerOptions)
```

**Options**:
```typescript
{
  maxSize: number,          // Max particles (default: 1500)
  dynamicProperties: {
    position: boolean,      // Allow position updates (default: true)
    scale: boolean,         // Allow scale updates (default: false)
    rotation: boolean,      // Allow rotation updates (default: false)
    color: boolean          // Allow tint/alpha updates (default: false)
  }
}
```

### Methods

```typescript
container.addParticle(particle: Particle)
container.removeParticle(particle: Particle)
container.update()  // Call if changing static properties
container.destroy()
```

### Properties

```typescript
container.maxSize: number                // Maximum particle count
container.dynamicProperties: object      // Which properties can change
container.particleChildren: Particle[]   // Array of particles
```

### Particle Interface

```typescript
interface IParticle {
  x: number;
  y: number;
  scaleX: number;
  scaleY: number;
  anchorX: number;
  anchorY: number;
  rotation: number;
  color: number;    // Tint
  texture: Texture;
}

// Create particle
const particle = new Particle({
  texture: Texture.from('spark.png'),
  x: 100,
  y: 200,
  scaleX: 0.5,
  scaleY: 0.5,
  rotation: 0,
  tint: 0xffffff,
  alpha: 1.0
});
```

### Example

```typescript
import { ParticleContainer, Particle, Texture } from 'pixi.js';

const texture = Texture.from('particle.png');

const particles = new ParticleContainer({
  maxSize: 10000,
  dynamicProperties: {
    position: true,   // Update positions
    scale: true,      // Update scale
    rotation: false,  // Static rotation
    color: false      // Static color
  }
});

for (let i = 0; i < 10000; i++) {
  const particle = new Particle({
    texture,
    x: Math.random() * 800,
    y: Math.random() * 600
  });

  particles.addParticle(particle);
}

app.stage.addChild(particles);

// Update loop
app.ticker.add(() => {
  particles.particleChildren.forEach(p => {
    p.y += 1;  // Move down
    if (p.y > 600) p.y = 0;
  });
});
```

---

## Filters

WebGL shader-based effects applied to display objects.

### Built-in Filters

#### BlurFilter

```typescript
import { BlurFilter } from 'pixi.js';

const blur = new BlurFilter({
  strength: 8,      // Blur amount (default: 8)
  quality: 4,       // Iterations (default: 4)
  kernelSize: 5     // Sample size: 5, 7, 9, 11, 13, 15
});

sprite.filters = [blur];
```

#### ColorMatrixFilter

```typescript
import { ColorMatrixFilter } from 'pixi.js';

const colorMatrix = new ColorMatrixFilter();

// Presets
colorMatrix.greyscale(0.5);     // 0-1
colorMatrix.sepia();
colorMatrix.blackAndWhite();
colorMatrix.contrast(1.5);      // >1 increases
colorMatrix.saturate(2);        // -1 to 1
colorMatrix.brightness(1.2);    // >1 brightens
colorMatrix.hue(45);            // Rotate hue (degrees)
colorMatrix.negative();
colorMatrix.kodachrome();
colorMatrix.technicolor();
colorMatrix.polaroid();
colorMatrix.vintage();

sprite.filters = [colorMatrix];
```

#### DisplacementFilter

```typescript
import { DisplacementFilter, Sprite } from 'pixi.js';

const displacementSprite = Sprite.from('displacement.jpg');
const displacementFilter = new DisplacementFilter({
  sprite: displacementSprite,
  scale: 50  // Displacement amount
});

sprite.filters = [displacementFilter];

// Animate displacement
app.ticker.add(() => {
  displacementSprite.x += 1;
});
```

#### AlphaFilter

```typescript
import { AlphaFilter } from 'pixi.js';

const alphaFilter = new AlphaFilter(0.5);  // 0-1
container.filters = [alphaFilter];  // Flattens alpha across children
```

#### NoiseFilter

```typescript
import { NoiseFilter } from 'pixi.js';

const noise = new NoiseFilter({
  noise: 0.5,  // Amount (0-1)
  seed: Math.random()
});

sprite.filters = [noise];
```

#### FXAAFilter

```typescript
import { FXAAFilter } from 'pixi.js';

const fxaa = new FXAAFilter();
sprite.filters = [fxaa];  // Anti-aliasing
```

### Custom Filters

```typescript
import { Filter, GlProgram } from 'pixi.js';

const vertex = `...`;  // Vertex shader
const fragment = `...`;  // Fragment shader

const customFilter = new Filter({
  glProgram: new GlProgram({ vertex, fragment }),
  resources: {
    customUniforms: {
      uTime: { value: 0.0, type: 'f32' },
      uColor: { value: [1.0, 0.0, 0.0], type: 'vec3<f32>' }
    }
  }
});

sprite.filters = [customFilter];

// Update uniforms
app.ticker.add((ticker) => {
  customFilter.resources.customUniforms.uniforms.uTime += 0.01 * ticker.deltaTime;
});
```

### Filter Optimization

```typescript
// Specify filterArea to avoid runtime measurement
sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);

// Release filters
sprite.filters = null;

// Generate filtered texture (apply once)
const filteredTexture = renderer.filters.generateFilteredTexture({
  texture: originalTexture,
  filters: [blurFilter]
});
```

**API References**:
- BlurFilter: @pixi/filter-blur
- ColorMatrixFilter: @pixi/filter-color-matrix
- DisplacementFilter: @pixi/filter-displacement
- AlphaFilter: @pixi/filter-alpha
- NoiseFilter: @pixi/filter-noise
- FXAAFilter: @pixi/filter-fxaa

---

## Text

Render styled text as a texture.

### Text

Standard text rendering:

```typescript
import { Text, TextStyle } from 'pixi.js';

const style = new TextStyle({
  fontFamily: 'Arial',
  fontSize: 36,
  fontStyle: 'italic',
  fontWeight: 'bold',
  fill: '#ffffff',
  stroke: { color: '#000000', width: 4 },
  dropShadow: {
    alpha: 0.5,
    angle: Math.PI / 6,
    blur: 4,
    color: '#000000',
    distance: 6
  },
  wordWrap: true,
  wordWrapWidth: 400,
  align: 'center',
  filters: [new BlurFilter()]  // Bake filter into texture
});

const text = new Text({
  text: 'Hello PixiJS!',
  style
});

text.position.set(100, 100);
app.stage.addChild(text);

// Update text
text.text = 'New text';

// Adjust resolution
text.resolution = 2;  // Higher = sharper but more memory
```

### BitmapText

High-performance text for dynamic content:

```typescript
import { BitmapText } from 'pixi.js';

// Requires bitmap font asset
const bitmapText = new BitmapText({
  text: 'Score: 0',
  style: {
    fontFamily: 'MyBitmapFont',
    fontSize: 24,
    tint: 0xff0000
  }
});

app.stage.addChild(bitmapText);

// Update frequently (very fast)
app.ticker.add(() => {
  bitmapText.text = `Score: ${++score}`;
});
```

### TextStyle Options

```typescript
interface TextStyleOptions {
  // Font
  fontFamily: string | string[];
  fontSize: number | string;
  fontStyle: 'normal' | 'italic' | 'oblique';
  fontWeight: 'normal' | 'bold' | '100-900';

  // Fill
  fill: number | string | string[] | number[];  // Gradient support
  fillGradientStops: number[];

  // Stroke
  stroke: { color: number | string, width: number, alpha?: number };

  // Shadow
  dropShadow: {
    alpha: number,
    angle: number,
    blur: number,
    color: number | string,
    distance: number
  };

  // Layout
  align: 'left' | 'center' | 'right' | 'justify';
  wordWrap: boolean;
  wordWrapWidth: number;
  breakWords: boolean;
  lineHeight: number;
  letterSpacing: number;
  leading: number;

  // Other
  padding: number;
  trim: boolean;
  whiteSpace: 'normal' | 'pre' | 'pre-line';
}
```

---

## Assets

Asset loading and management system.

### Loading Assets

```typescript
import { Assets } from 'pixi.js';

// Load single asset
const texture = await Assets.load('image.png');
const spritesheet = await Assets.load('spritesheet.json');

// Load multiple assets
const assets = await Assets.load([
  'image1.png',
  'image2.png',
  'sound.mp3'
]);

// Load with aliases
await Assets.add({ alias: 'hero', src: 'hero.png' });
const heroTexture = await Assets.load('hero');

// Load bundle
Assets.addBundle('game', {
  player: 'player.png',
  enemy: 'enemy.png',
  background: 'bg.jpg'
});
const bundle = await Assets.loadBundle('game');

// Access loaded assets
const playerTexture = Assets.get('player');
```

### Progress Tracking

```typescript
Assets.load('large-file.png', (progress) => {
  console.log(`Loading: ${Math.round(progress * 100)}%`);
});

// Or with promises
const promise = Assets.load(['file1.png', 'file2.png']);
promise.progress = (progress) => {
  console.log(`Progress: ${progress * 100}%`);
};
await promise;
```

### Background Loading

```typescript
// Load in background (non-blocking)
Assets.backgroundLoad(['asset1.png', 'asset2.png']);

// Check if loaded
if (Assets.cache.has('asset1.png')) {
  const texture = Assets.get('asset1.png');
}
```

### Unloading Assets

```typescript
// Unload single asset
await Assets.unload('image.png');

// Unload bundle
await Assets.unloadBundle('game');

// Clear cache
Assets.reset();
```

---

## Renderer

Low-level rendering system (WebGL/WebGPU).

### Properties

```typescript
renderer.type: string              // 'webgl' | 'webgpu'
renderer.width: number
renderer.height: number
renderer.resolution: number
renderer.backgroundColor: number
renderer.backgroundAlpha: number
```

### Methods

```typescript
// Manual rendering
renderer.render(container);

// Resize
renderer.resize(width, height);

// Clear
renderer.clear();

// Generate texture from display object
const texture = renderer.generateTexture(displayObject, {
  resolution: 1,
  frame: new Rectangle(0, 0, 100, 100)
});

// Destroy
renderer.destroy();
```

---

## DisplayObject

Base class for all renderable objects (Sprite, Graphics, Container, etc.).

### Transform Properties

```typescript
displayObject.position: ObservablePoint     // x, y
displayObject.scale: ObservablePoint        // x, y scale
displayObject.rotation: number              // Radians
displayObject.pivot: ObservablePoint        // Rotation pivot
displayObject.skew: ObservablePoint         // x, y skew
displayObject.angle: number                 // Degrees (converts to rotation)
```

### Visibility

```typescript
displayObject.alpha: number                 // 0-1 opacity
displayObject.visible: boolean              // Show/hide
displayObject.renderable: boolean           // Render flag
displayObject.cullable: boolean             // Viewport culling
displayObject.mask: Graphics | Sprite       // Masking
```

### Hierarchy

```typescript
displayObject.parent: Container
displayObject.children: DisplayObject[]  // If Container
displayObject.zIndex: number             // Render order (if sortableChildren enabled)
displayObject.removeFromParent()
displayObject.destroy(options)
```

### Bounds

```typescript
displayObject.getBounds()           // Global bounds
displayObject.getLocalBounds()      // Local bounds
displayObject.width: number         // Bounding width
displayObject.height: number        // Bounding height
```

### Interaction

```typescript
displayObject.eventMode: string     // 'none' | 'passive' | 'static' | 'dynamic'
displayObject.cursor: string        // CSS cursor
displayObject.hitArea: Shape        // Custom hit detection area
displayObject.interactive: boolean  // Enable events (deprecated, use eventMode)
```

---

## Events

Interactive event system.

### Event Modes

```typescript
sprite.eventMode = 'static';   // Enable interaction
sprite.eventMode = 'dynamic';  // Enable + propagate to children
sprite.eventMode = 'passive';  // Receive events but don't block
sprite.eventMode = 'none';     // No interaction (default)
```

### Mouse Events

```typescript
sprite.on('pointerdown', (event) => {
  console.log('Clicked at:', event.global.x, event.global.y);
});

sprite.on('pointerup', handler);
sprite.on('pointermove', handler);
sprite.on('pointerover', handler);   // Mouse enter
sprite.on('pointerout', handler);    // Mouse leave
sprite.on('pointerupoutside', handler);  // Released outside

// Once
sprite.once('pointerdown', handler);

// Remove
sprite.off('pointerdown', handler);
sprite.removeAllListeners();
```

### Touch Events

```typescript
sprite.on('touchstart', handler);
sprite.on('touchend', handler);
sprite.on('touchmove', handler);
sprite.on('tap', handler);
```

### Event Object

```typescript
interface FederatedPointerEvent {
  global: Point;         // Global coordinates
  client: Point;         // Client coordinates
  screen: Point;         // Screen coordinates
  movement: Point;       // Delta movement
  page: Point;           // Page coordinates
  button: number;        // Mouse button (0=left, 1=middle, 2=right)
  buttons: number;       // Bitmask of pressed buttons
  target: DisplayObject; // Event target
  currentTarget: DisplayObject;
  type: string;          // Event type
  preventDefault(): void;
  stopPropagation(): void;
}
```

### Custom Cursor

```typescript
sprite.cursor = 'pointer';
sprite.cursor = 'grab';
sprite.cursor = 'help';
```

### Hit Area

```typescript
import { Rectangle, Circle, Polygon } from 'pixi.js';

// Rectangle hit area
sprite.hitArea = new Rectangle(0, 0, 100, 100);

// Circle hit area
sprite.hitArea = new Circle(50, 50, 30);

// Polygon hit area
sprite.hitArea = new Polygon([0,0, 100,0, 100,100, 0,100]);
```

---

## Utility Classes

### Rectangle

```typescript
const rect = new Rectangle(x, y, width, height);
rect.contains(x, y);
rect.intersects(otherRect);
```

### Circle

```typescript
const circle = new Circle(x, y, radius);
circle.contains(x, y);
```

### Point

```typescript
const point = new Point(x, y);
point.set(x, y);
point.clone();
point.equals(otherPoint);
```

### ObservablePoint

```typescript
const observable = new ObservablePoint(callback, scope);
observable.set(x, y);
observable.x = 100;  // Triggers callback
```

---

## Performance APIs

### CacheAsBitmap

```typescript
// Convert to texture for faster rendering
displayObject.cacheAsBitmap = true;

// Disable when updating frequently
displayObject.cacheAsBitmap = false;
```

### Ticker

```typescript
import { Ticker } from 'pixi.js';

const ticker = Ticker.shared;

ticker.add((delta) => {
  // Update logic
  // delta = time since last frame
});

ticker.speed = 0.5;  // Half speed
ticker.maxFPS = 30;  // Cap at 30 FPS
ticker.minFPS = 10;  // Min for deltaTime calculation

ticker.stop();
ticker.start();
```

---

## Constants

### Blend Modes

```typescript
import { BLEND_MODES } from 'pixi.js';

sprite.blendMode = BLEND_MODES.NORMAL;
sprite.blendMode = BLEND_MODES.ADD;
sprite.blendMode = BLEND_MODES.MULTIPLY;
sprite.blendMode = BLEND_MODES.SCREEN;
sprite.blendMode = BLEND_MODES.OVERLAY;
sprite.blendMode = BLEND_MODES.DARKEN;
sprite.blendMode = BLEND_MODES.LIGHTEN;
sprite.blendMode = BLEND_MODES.COLOR_DODGE;
sprite.blendMode = BLEND_MODES.COLOR_BURN;
sprite.blendMode = BLEND_MODES.HARD_LIGHT;
sprite.blendMode = BLEND_MODES.SOFT_LIGHT;
sprite.blendMode = BLEND_MODES.DIFFERENCE;
sprite.blendMode = BLEND_MODES.EXCLUSION;
sprite.blendMode = BLEND_MODES.HUE;
sprite.blendMode = BLEND_MODES.SATURATION;
sprite.blendMode = BLEND_MODES.COLOR;
sprite.blendMode = BLEND_MODES.LUMINOSITY;
```

### Scale Modes

```typescript
import { SCALE_MODES } from 'pixi.js';

texture.baseTexture.scaleMode = SCALE_MODES.LINEAR;   // Smooth (default)
texture.baseTexture.scaleMode = SCALE_MODES.NEAREST;  // Pixelated
```

---

## TypeScript Support

PixiJS is written in TypeScript and provides full type definitions.

```typescript
import { Application, Sprite, Texture, Container } from 'pixi.js';

const app: Application = new Application();
const sprite: Sprite = new Sprite(Texture.WHITE);
const container: Container = new Container();
```

---

## Official API Documentation

- **Main Docs**: https://pixijs.download/release/docs/
- **Examples**: https://pixijs.io/examples/
- **GitHub**: https://github.com/pixijs/pixijs

---

This API reference covers PixiJS v8+ core functionality. For advanced features, plugins, and detailed shader programming, consult the official documentation.
