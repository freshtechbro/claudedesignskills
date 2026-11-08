# PixiJS Examples and Patterns

Comprehensive real-world examples and patterns for building production-ready PixiJS applications.

## Table of Contents

1. [Basic Applications](#basic-applications)
2. [Interactive Elements](#interactive-elements)
3. [Particle Systems](#particle-systems)
4. [Filters and Effects](#filters-and-effects)
5. [Custom Shaders](#custom-shaders)
6. [Animation Patterns](#animation-patterns)
7. [Performance Optimization](#performance-optimization)
8. [Game Development](#game-development)
9. [UI Components](#ui-components)
10. [Framework Integration](#framework-integration)
11. [Mobile Optimization](#mobile-optimization)
12. [Advanced Techniques](#advanced-techniques)

---

## Basic Applications

### 1. Minimal PixiJS Application

The absolute minimum code to get started with PixiJS v8+:

```javascript
(async () => {
    const app = new PIXI.Application();

    await app.init({
        width: 800,
        height: 600,
        backgroundColor: 0x1099bb
    });

    document.body.appendChild(app.canvas);

    // Create a sprite
    const texture = await PIXI.Assets.load('bunny.png');
    const bunny = new PIXI.Sprite(texture);

    bunny.anchor.set(0.5);
    bunny.position.set(400, 300);

    app.stage.addChild(bunny);

    // Animation loop
    app.ticker.add((ticker) => {
        bunny.rotation += 0.05 * ticker.deltaTime;
    });
})();
```

### 2. Responsive Canvas Application

Canvas that automatically resizes to fill the window:

```javascript
(async () => {
    const app = new PIXI.Application();

    await app.init({
        width: window.innerWidth,
        height: window.innerHeight,
        backgroundColor: 0x1a1a2e,
        antialias: true,
        resolution: window.devicePixelRatio || 1,
        autoDensity: true
    });

    document.body.appendChild(app.canvas);

    // Handle window resize
    window.addEventListener('resize', () => {
        app.renderer.resize(window.innerWidth, window.innerHeight);

        // Reposition elements if needed
        updateLayout();
    });

    function updateLayout() {
        // Center content or adjust layout based on new dimensions
        const centerX = app.screen.width / 2;
        const centerY = app.screen.height / 2;

        // Update element positions...
    }
})();
```

### 3. Asset Loading with Progress

Load multiple assets with loading screen:

```javascript
(async () => {
    const app = new PIXI.Application();
    await app.init({ width: 800, height: 600 });
    document.body.appendChild(app.canvas);

    // Create loading text
    const loadingText = new PIXI.Text({
        text: 'Loading: 0%',
        style: { fontSize: 32, fill: 0xffffff }
    });
    loadingText.anchor.set(0.5);
    loadingText.position.set(400, 300);
    app.stage.addChild(loadingText);

    // Assets to load
    const assets = [
        { alias: 'bunny', src: 'bunny.png' },
        { alias: 'spritesheet', src: 'spritesheet.json' },
        { alias: 'background', src: 'background.jpg' }
    ];

    // Load assets with progress
    PIXI.Assets.load(assets, (progress) => {
        loadingText.text = `Loading: ${Math.round(progress * 100)}%`;
    }).then((textures) => {
        // Remove loading screen
        app.stage.removeChild(loadingText);

        // Start application with loaded assets
        startApp(textures);
    });

    function startApp(textures) {
        const bunny = new PIXI.Sprite(textures.bunny);
        bunny.position.set(400, 300);
        app.stage.addChild(bunny);
    }
})();
```

### 4. Multi-Scene Application

Manage multiple scenes/screens:

```javascript
class SceneManager {
    constructor(app) {
        this.app = app;
        this.scenes = new Map();
        this.currentScene = null;
    }

    addScene(name, scene) {
        this.scenes.set(name, scene);
        scene.visible = false;
        this.app.stage.addChild(scene);
    }

    switchTo(name) {
        if (this.currentScene) {
            this.currentScene.visible = false;
            this.currentScene.onExit?.();
        }

        const scene = this.scenes.get(name);
        if (scene) {
            scene.visible = true;
            scene.onEnter?.();
            this.currentScene = scene;
        }
    }
}

// Usage
(async () => {
    const app = new PIXI.Application();
    await app.init({ width: 800, height: 600 });
    document.body.appendChild(app.canvas);

    const sceneManager = new SceneManager(app);

    // Create scenes
    const menuScene = new PIXI.Container();
    menuScene.onEnter = () => console.log('Entered menu');
    menuScene.onExit = () => console.log('Exited menu');

    const gameScene = new PIXI.Container();
    gameScene.onEnter = () => console.log('Game started');
    gameScene.onExit = () => console.log('Game paused');

    // Add menu content
    const menuText = new PIXI.Text({
        text: 'Main Menu',
        style: { fontSize: 48, fill: 0xffffff }
    });
    menuText.position.set(300, 250);
    menuScene.addChild(menuText);

    const startButton = new PIXI.Text({
        text: 'Start Game',
        style: { fontSize: 32, fill: 0x00ff00 }
    });
    startButton.position.set(320, 350);
    startButton.eventMode = 'static';
    startButton.cursor = 'pointer';
    startButton.on('pointerdown', () => sceneManager.switchTo('game'));
    menuScene.addChild(startButton);

    // Add game content
    const gameText = new PIXI.Text({
        text: 'Game Scene',
        style: { fontSize: 48, fill: 0xffffff }
    });
    gameText.position.set(300, 300);
    gameScene.addChild(gameText);

    // Register scenes
    sceneManager.addScene('menu', menuScene);
    sceneManager.addScene('game', gameScene);

    // Start with menu
    sceneManager.switchTo('menu');
})();
```

---

## Interactive Elements

### 1. Draggable Sprites

Implement drag-and-drop functionality:

```javascript
function makeDraggable(sprite) {
    sprite.eventMode = 'static';
    sprite.cursor = 'pointer';

    let dragData = null;

    sprite.on('pointerdown', (event) => {
        dragData = event.global.clone();
        sprite.alpha = 0.5;
        app.stage.on('pointermove', onDragMove);
    });

    sprite.on('pointerup', onDragEnd);
    sprite.on('pointerupoutside', onDragEnd);

    function onDragMove(event) {
        if (dragData) {
            const newPosition = event.global;
            sprite.x += newPosition.x - dragData.x;
            sprite.y += newPosition.y - dragData.y;
            dragData = newPosition.clone();
        }
    }

    function onDragEnd() {
        if (dragData) {
            sprite.alpha = 1;
            dragData = null;
            app.stage.off('pointermove', onDragMove);
        }
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.position.set(100, 100);
app.stage.addChild(sprite);
makeDraggable(sprite);
```

### 2. Hover Effects

Add visual feedback on mouse hover:

```javascript
function addHoverEffect(sprite, options = {}) {
    const {
        hoverScale = 1.2,
        hoverTint = 0xffff00,
        animationSpeed = 0.1
    } = options;

    sprite.eventMode = 'static';
    sprite.cursor = 'pointer';

    const originalScale = sprite.scale.x;
    const originalTint = sprite.tint;

    sprite.on('pointerover', () => {
        animateScale(sprite, hoverScale, animationSpeed);
        sprite.tint = hoverTint;
    });

    sprite.on('pointerout', () => {
        animateScale(sprite, originalScale, animationSpeed);
        sprite.tint = originalTint;
    });
}

function animateScale(sprite, targetScale, speed) {
    const ticker = (delta) => {
        const currentScale = sprite.scale.x;
        const diff = targetScale - currentScale;

        if (Math.abs(diff) < 0.01) {
            sprite.scale.set(targetScale);
            app.ticker.remove(ticker);
        } else {
            const newScale = currentScale + diff * speed * delta.deltaTime;
            sprite.scale.set(newScale);
        }
    };

    app.ticker.add(ticker);
}

// Usage
const sprite = new PIXI.Sprite(texture);
addHoverEffect(sprite, { hoverScale: 1.3, hoverTint: 0x00ff00 });
```

### 3. Button Component

Reusable button with states:

```javascript
class Button extends PIXI.Container {
    constructor(text, options = {}) {
        super();

        const {
            width = 200,
            height = 60,
            backgroundColor = 0x4CAF50,
            hoverColor = 0x45a049,
            textColor = 0xffffff,
            fontSize = 24,
            borderRadius = 10
        } = options;

        // Background
        this.background = new PIXI.Graphics();
        this.drawBackground(backgroundColor, width, height, borderRadius);
        this.addChild(this.background);

        // Text
        this.label = new PIXI.Text({
            text,
            style: {
                fontSize,
                fill: textColor,
                fontWeight: 'bold'
            }
        });
        this.label.anchor.set(0.5);
        this.label.position.set(width / 2, height / 2);
        this.addChild(this.label);

        // Interactive
        this.eventMode = 'static';
        this.cursor = 'pointer';

        // Store colors
        this.normalColor = backgroundColor;
        this.hoverColor = hoverColor;
        this.width = width;
        this.height = height;
        this.borderRadius = borderRadius;

        // Events
        this.on('pointerover', () => {
            this.drawBackground(this.hoverColor, this.width, this.height, this.borderRadius);
        });

        this.on('pointerout', () => {
            this.drawBackground(this.normalColor, this.width, this.height, this.borderRadius);
        });

        this.on('pointerdown', () => {
            this.scale.set(0.95);
        });

        this.on('pointerup', () => {
            this.scale.set(1);
        });
    }

    drawBackground(color, width, height, borderRadius) {
        this.background.clear();
        this.background.roundRect(0, 0, width, height, borderRadius).fill(color);
    }

    setText(text) {
        this.label.text = text;
    }

    onClick(callback) {
        this.on('pointerdown', callback);
        return this;
    }
}

// Usage
const playButton = new Button('Play Game', {
    width: 250,
    height: 70,
    backgroundColor: 0x3498db,
    hoverColor: 0x2980b9
});

playButton.position.set(275, 400);
playButton.onClick(() => {
    console.log('Play button clicked!');
    startGame();
});

app.stage.addChild(playButton);
```

### 4. Click Detection with Shapes

Detect clicks on custom shapes (not just sprites):

```javascript
const graphics = new PIXI.Graphics();
graphics.circle(400, 300, 100).fill(0xff0000);

graphics.eventMode = 'static';
graphics.cursor = 'pointer';
graphics.hitArea = new PIXI.Circle(400, 300, 100);

graphics.on('pointerdown', (event) => {
    console.log('Circle clicked!');
    graphics.tint = Math.random() * 0xffffff;
});

app.stage.addChild(graphics);

// Custom polygon hit area
const star = new PIXI.Graphics();
star.star(400, 300, 5, 50, 25).fill(0xffff00);

star.eventMode = 'static';
star.cursor = 'pointer';

// Define hit area as polygon
const starPoints = [
    400, 250,  // Top
    420, 290,
    460, 300,
    430, 330,
    440, 370,
    400, 350,
    360, 370,
    370, 330,
    340, 300,
    380, 290
];
star.hitArea = new PIXI.Polygon(starPoints);

star.on('pointerdown', () => {
    console.log('Star clicked!');
});

app.stage.addChild(star);
```

---

## Particle Systems

### 1. Basic Particle Emitter

Simple particle emitter with gravity:

```javascript
class ParticleEmitter {
    constructor(app, texture) {
        this.app = app;
        this.texture = texture;
        this.particles = [];
        this.maxParticles = 1000;

        this.container = new PIXI.ParticleContainer(this.maxParticles, {
            position: true,
            rotation: true,
            scale: true,
            tint: true,
            alpha: true
        });

        app.stage.addChild(this.container);

        app.ticker.add((ticker) => this.update(ticker));
    }

    emit(x, y, count = 10) {
        for (let i = 0; i < count; i++) {
            if (this.particles.length >= this.maxParticles) break;

            const particle = new PIXI.Sprite(this.texture);
            particle.anchor.set(0.5);
            particle.position.set(x, y);

            // Random velocity
            particle.vx = (Math.random() - 0.5) * 10;
            particle.vy = -Math.random() * 10;

            // Lifetime
            particle.life = 1.0;
            particle.maxLife = 1.0;

            this.container.addChild(particle);
            this.particles.push(particle);
        }
    }

    update(ticker) {
        const gravity = 0.5;
        const delta = ticker.deltaTime;

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];

            // Apply physics
            p.vy += gravity * delta;
            p.x += p.vx * delta;
            p.y += p.vy * delta;

            // Update life
            p.life -= 0.02 * delta;
            p.alpha = p.life / p.maxLife;
            p.scale.set(p.alpha);

            // Remove dead particles
            if (p.life <= 0) {
                this.container.removeChild(p);
                p.destroy();
                this.particles.splice(i, 1);
            }
        }
    }
}

// Usage
const particleTexture = createCircleTexture(10, 0xffffff);
const emitter = new ParticleEmitter(app, particleTexture);

// Emit on click
app.stage.eventMode = 'static';
app.stage.on('pointerdown', (event) => {
    emitter.emit(event.global.x, event.global.y, 50);
});

function createCircleTexture(radius, color) {
    const graphics = new PIXI.Graphics();
    graphics.circle(radius, radius, radius).fill(color);
    return app.renderer.generateTexture(graphics);
}
```

### 2. Fire Effect

Realistic fire particle effect:

```javascript
class FireEmitter {
    constructor(app, x, y) {
        this.app = app;
        this.x = x;
        this.y = y;
        this.particles = [];

        this.container = new PIXI.ParticleContainer(2000, {
            position: true,
            scale: true,
            tint: true,
            alpha: true
        });

        app.stage.addChild(this.container);

        // Create particle texture
        const graphics = new PIXI.Graphics();
        graphics.circle(8, 8, 8).fill(0xffffff);
        this.texture = app.renderer.generateTexture(graphics);

        // Emit continuously
        app.ticker.add((ticker) => this.update(ticker));
    }

    update(ticker) {
        const delta = ticker.deltaTime;

        // Emit new particles
        for (let i = 0; i < 5; i++) {
            this.emitParticle();
        }

        // Update existing particles
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];

            // Rise upward with slight horizontal drift
            p.y += p.vy * delta;
            p.x += p.vx * delta;

            // Update life
            p.life -= 0.02 * delta;

            // Color transition: yellow -> orange -> red -> transparent
            const t = 1 - p.life;
            if (t < 0.33) {
                // Yellow to orange
                const localT = t / 0.33;
                p.tint = this.colorLerp(0xffff00, 0xff8800, localT);
            } else if (t < 0.66) {
                // Orange to red
                const localT = (t - 0.33) / 0.33;
                p.tint = this.colorLerp(0xff8800, 0xff0000, localT);
            } else {
                // Red to dark red
                const localT = (t - 0.66) / 0.34;
                p.tint = this.colorLerp(0xff0000, 0x880000, localT);
            }

            p.alpha = p.life;
            p.scale.set(p.life * 1.5);

            // Remove dead particles
            if (p.life <= 0) {
                this.container.removeChild(p);
                p.destroy();
                this.particles.splice(i, 1);
            }
        }
    }

    emitParticle() {
        const particle = new PIXI.Sprite(this.texture);
        particle.anchor.set(0.5);
        particle.position.set(
            this.x + (Math.random() - 0.5) * 20,
            this.y
        );

        particle.vx = (Math.random() - 0.5) * 2;
        particle.vy = -2 - Math.random() * 3;
        particle.life = 1.0;

        this.container.addChild(particle);
        this.particles.push(particle);
    }

    colorLerp(color1, color2, t) {
        const r1 = (color1 >> 16) & 0xff;
        const g1 = (color1 >> 8) & 0xff;
        const b1 = color1 & 0xff;

        const r2 = (color2 >> 16) & 0xff;
        const g2 = (color2 >> 8) & 0xff;
        const b2 = color2 & 0xff;

        const r = Math.floor(r1 + (r2 - r1) * t);
        const g = Math.floor(g1 + (g2 - g1) * t);
        const b = Math.floor(b1 + (b2 - b1) * t);

        return (r << 16) | (g << 8) | b;
    }
}

// Usage
const fireEmitter = new FireEmitter(app, 400, 500);
```

### 3. Trail Effect

Create motion trails behind moving objects:

```javascript
class TrailEffect {
    constructor(app, target, options = {}) {
        this.app = app;
        this.target = target;
        this.trailSegments = [];
        this.maxSegments = options.maxSegments || 20;
        this.segmentLife = options.segmentLife || 0.5;

        this.container = new PIXI.Container();
        app.stage.addChildAt(this.container, 0);  // Behind target

        app.ticker.add((ticker) => this.update(ticker));
    }

    update(ticker) {
        const delta = ticker.deltaTime;

        // Create new segment at target position
        const segment = new PIXI.Graphics();
        segment.circle(0, 0, this.target.width / 2).fill(this.target.tint);
        segment.position.set(this.target.x, this.target.y);
        segment.life = this.segmentLife;
        segment.maxLife = this.segmentLife;

        this.container.addChild(segment);
        this.trailSegments.push(segment);

        // Remove old segments
        if (this.trailSegments.length > this.maxSegments) {
            const old = this.trailSegments.shift();
            this.container.removeChild(old);
            old.destroy();
        }

        // Update existing segments
        for (const seg of this.trailSegments) {
            seg.life -= 0.016 * delta;
            seg.alpha = seg.life / seg.maxLife;
        }
    }

    destroy() {
        for (const seg of this.trailSegments) {
            seg.destroy();
        }
        this.container.destroy();
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.anchor.set(0.5);
sprite.position.set(400, 300);
app.stage.addChild(sprite);

const trail = new TrailEffect(app, sprite, {
    maxSegments: 30,
    segmentLife: 0.8
});

// Move sprite with mouse
app.stage.eventMode = 'static';
app.stage.on('pointermove', (event) => {
    sprite.position.set(event.global.x, event.global.y);
});
```

### 4. Explosion Effect

One-shot explosion particle effect:

```javascript
class Explosion {
    constructor(app, x, y, particleCount = 50) {
        this.app = app;
        this.particles = [];

        const graphics = new PIXI.Graphics();
        graphics.circle(5, 5, 5).fill(0xffffff);
        const texture = app.renderer.generateTexture(graphics);

        const container = new PIXI.ParticleContainer(particleCount, {
            position: true,
            rotation: true,
            scale: true,
            tint: true,
            alpha: true
        });

        app.stage.addChild(container);

        // Create particles
        for (let i = 0; i < particleCount; i++) {
            const angle = (Math.PI * 2 * i) / particleCount;
            const speed = 5 + Math.random() * 5;

            const particle = new PIXI.Sprite(texture);
            particle.anchor.set(0.5);
            particle.position.set(x, y);
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;
            particle.life = 1.0;
            particle.tint = Math.random() > 0.5 ? 0xff8800 : 0xffff00;

            container.addChild(particle);
            this.particles.push(particle);
        }

        // Update and cleanup
        const ticker = (delta) => {
            let allDead = true;

            for (const p of this.particles) {
                p.x += p.vx * delta.deltaTime;
                p.y += p.vy * delta.deltaTime;
                p.vy += 0.3 * delta.deltaTime;  // Gravity

                p.life -= 0.02 * delta.deltaTime;
                p.alpha = p.life;
                p.scale.set(p.life);

                if (p.life > 0) allDead = false;
            }

            if (allDead) {
                app.ticker.remove(ticker);
                container.destroy({ children: true });
            }
        };

        app.ticker.add(ticker);
    }
}

// Usage - trigger on click
app.stage.eventMode = 'static';
app.stage.on('pointerdown', (event) => {
    new Explosion(app, event.global.x, event.global.y, 100);
});
```

---

## Filters and Effects

### 1. Glow Effect

Add glowing outline to sprites:

```javascript
import { BlurFilter, ColorMatrixFilter } from 'pixi.js';

function addGlowEffect(sprite, options = {}) {
    const {
        glowColor = [1, 1, 0],  // Yellow
        glowStrength = 2,
        blurStrength = 10
    } = options;

    // Create blur filter
    const blurFilter = new BlurFilter();
    blurFilter.strength = blurStrength;

    // Create color filter for glow
    const colorFilter = new ColorMatrixFilter();
    colorFilter.brightness(glowStrength, false);

    // Apply filters
    sprite.filters = [blurFilter, colorFilter];

    return { blurFilter, colorFilter };
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
app.stage.addChild(sprite);

const glow = addGlowEffect(sprite, {
    glowColor: [0, 1, 1],  // Cyan
    glowStrength: 3,
    blurStrength: 15
});

// Animate glow intensity
let time = 0;
app.ticker.add((ticker) => {
    time += 0.05 * ticker.deltaTime;
    const intensity = Math.sin(time) * 0.5 + 1.5;
    glow.blurFilter.strength = 10 + intensity * 5;
});
```

### 2. Chromatic Aberration

RGB color separation effect:

```javascript
import { Filter, GlProgram } from 'pixi.js';

class ChromaticAberrationFilter extends Filter {
    constructor(offset = 5) {
        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform vec2 uOffset;

            out vec4 finalColor;

            void main() {
                vec2 coord = vTextureCoord;
                float r = texture(uTexture, coord + uOffset).r;
                float g = texture(uTexture, coord).g;
                float b = texture(uTexture, coord - uOffset).b;
                float a = texture(uTexture, coord).a;

                finalColor = vec4(r, g, b, a);
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                chromaUniforms: {
                    uOffset: {
                        value: new Float32Array([offset / 800, 0]),
                        type: 'vec2<f32>'
                    }
                }
            }
        });
    }

    set offset(value) {
        this.resources.chromaUniforms.uniforms.uOffset[0] = value / 800;
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
app.stage.addChild(sprite);

const chromaFilter = new ChromaticAberrationFilter(10);
sprite.filters = [chromaFilter];

// Animate offset
let time = 0;
app.ticker.add((ticker) => {
    time += 0.1 * ticker.deltaTime;
    chromaFilter.offset = Math.sin(time) * 20;
});
```

### 3. CRT Monitor Effect

Old-school CRT screen effect with scanlines and curvature:

```javascript
class CRTFilter extends Filter {
    constructor() {
        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform float uTime;

            out vec4 finalColor;

            void main() {
                vec2 uv = vTextureCoord;

                // Screen curvature
                vec2 dc = uv - 0.5;
                float dist = dot(dc, dc);
                uv = uv + dc * dist * 0.1;

                // Scanlines
                float scanline = sin(uv.y * 800.0) * 0.04;

                // Vignette
                float vignette = 1.0 - dist * 1.5;

                // Color aberration on edges
                float r = texture(uTexture, uv + vec2(0.001, 0.0)).r;
                float g = texture(uTexture, uv).g;
                float b = texture(uTexture, uv - vec2(0.001, 0.0)).b;

                vec3 color = vec3(r, g, b);
                color -= scanline;
                color *= vignette;

                // Flicker
                color *= 0.95 + 0.05 * sin(uTime * 100.0);

                finalColor = vec4(color, 1.0);
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                crtUniforms: {
                    uTime: { value: 0, type: 'f32' }
                }
            }
        });

        this.time = 0;
    }

    update(deltaTime) {
        this.time += deltaTime * 0.016;
        this.resources.crtUniforms.uniforms.uTime = this.time;
    }
}

// Usage
const crtFilter = new CRTFilter();
app.stage.filters = [crtFilter];

app.ticker.add((ticker) => {
    crtFilter.update(ticker.deltaTime);
});
```

### 4. Displacement Map Effect

Create water ripple or distortion effects:

```javascript
import { DisplacementFilter } from 'pixi.js';

(async () => {
    // Create displacement sprite
    const displacementSprite = PIXI.Sprite.from('displacement_map.png');
    displacementSprite.texture.baseTexture.wrapMode = PIXI.WRAP_MODES.REPEAT;

    // Create displacement filter
    const displacementFilter = new DisplacementFilter({
        sprite: displacementSprite,
        scale: 50
    });

    // Apply to stage or specific sprite
    app.stage.filters = [displacementFilter];

    // Animate displacement
    app.ticker.add((ticker) => {
        displacementSprite.x += 1 * ticker.deltaTime;
        displacementSprite.y += 0.5 * ticker.deltaTime;
    });
})();

// Generate displacement map programmatically
function createDisplacementMap(size = 512) {
    const graphics = new PIXI.Graphics();

    for (let i = 0; i < 50; i++) {
        const x = Math.random() * size;
        const y = Math.random() * size;
        const radius = Math.random() * 50 + 20;

        graphics.circle(x, y, radius)
            .fill({ color: 0xffffff, alpha: Math.random() * 0.5 });
    }

    const texture = app.renderer.generateTexture(graphics, {
        resolution: 1,
        multisample: PIXI.MSAA_QUALITY.NONE
    });

    return PIXI.Sprite.from(texture);
}
```

---

## Custom Shaders

### 1. Wave Distortion Shader

Create animated wave distortion:

```javascript
import { Filter, GlProgram } from 'pixi.js';

class WaveFilter extends Filter {
    constructor() {
        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform float uTime;
            uniform float uAmplitude;
            uniform float uFrequency;

            out vec4 finalColor;

            void main() {
                vec2 coord = vTextureCoord;

                // Apply wave distortion
                coord.x += sin(coord.y * uFrequency + uTime) * uAmplitude;
                coord.y += cos(coord.x * uFrequency + uTime) * uAmplitude;

                finalColor = texture(uTexture, coord);
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                waveUniforms: {
                    uTime: { value: 0, type: 'f32' },
                    uAmplitude: { value: 0.01, type: 'f32' },
                    uFrequency: { value: 10.0, type: 'f32' }
                }
            }
        });
    }

    set time(value) {
        this.resources.waveUniforms.uniforms.uTime = value;
    }

    set amplitude(value) {
        this.resources.waveUniforms.uniforms.uAmplitude = value;
    }

    set frequency(value) {
        this.resources.waveUniforms.uniforms.uFrequency = value;
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
app.stage.addChild(sprite);

const waveFilter = new WaveFilter();
sprite.filters = [waveFilter];

let time = 0;
app.ticker.add((ticker) => {
    time += 0.05 * ticker.deltaTime;
    waveFilter.time = time;
});
```

### 2. Pixelate Shader

Dynamic pixelation effect:

```javascript
class PixelateFilter extends Filter {
    constructor(pixelSize = 10) {
        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform vec2 uSize;
            uniform float uPixelSize;

            out vec4 finalColor;

            void main() {
                vec2 coord = vTextureCoord * uSize;
                vec2 pixelCoord = floor(coord / uPixelSize) * uPixelSize;
                vec2 pixelUV = pixelCoord / uSize;

                finalColor = texture(uTexture, pixelUV);
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                pixelateUniforms: {
                    uSize: {
                        value: new Float32Array([800, 600]),
                        type: 'vec2<f32>'
                    },
                    uPixelSize: { value: pixelSize, type: 'f32' }
                }
            }
        });
    }

    set pixelSize(value) {
        this.resources.pixelateUniforms.uniforms.uPixelSize = value;
    }

    setSize(width, height) {
        this.resources.pixelateUniforms.uniforms.uSize[0] = width;
        this.resources.pixelateUniforms.uniforms.uSize[1] = height;
    }
}

// Usage with animated pixelation
const pixelateFilter = new PixelateFilter(1);
app.stage.filters = [pixelateFilter];

let pixelSize = 1;
let direction = 1;

app.ticker.add(() => {
    pixelSize += direction * 0.5;

    if (pixelSize >= 20) direction = -1;
    if (pixelSize <= 1) direction = 1;

    pixelateFilter.pixelSize = pixelSize;
});
```

### 3. Color Grading Shader

Professional color grading with adjustable parameters:

```javascript
class ColorGradingFilter extends Filter {
    constructor(options = {}) {
        const {
            brightness = 0,
            contrast = 0,
            saturation = 0,
            temperature = 0
        } = options;

        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform float uBrightness;
            uniform float uContrast;
            uniform float uSaturation;
            uniform float uTemperature;

            out vec4 finalColor;

            void main() {
                vec4 color = texture(uTexture, vTextureCoord);

                // Brightness
                color.rgb += uBrightness;

                // Contrast
                color.rgb = (color.rgb - 0.5) * (1.0 + uContrast) + 0.5;

                // Saturation
                float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
                color.rgb = mix(vec3(gray), color.rgb, 1.0 + uSaturation);

                // Temperature (blue/orange tint)
                color.r += uTemperature * 0.1;
                color.b -= uTemperature * 0.1;

                finalColor = color;
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                colorGradingUniforms: {
                    uBrightness: { value: brightness, type: 'f32' },
                    uContrast: { value: contrast, type: 'f32' },
                    uSaturation: { value: saturation, type: 'f32' },
                    uTemperature: { value: temperature, type: 'f32' }
                }
            }
        });
    }

    set brightness(value) {
        this.resources.colorGradingUniforms.uniforms.uBrightness = value;
    }

    set contrast(value) {
        this.resources.colorGradingUniforms.uniforms.uContrast = value;
    }

    set saturation(value) {
        this.resources.colorGradingUniforms.uniforms.uSaturation = value;
    }

    set temperature(value) {
        this.resources.colorGradingUniforms.uniforms.uTemperature = value;
    }
}

// Usage with UI controls
const colorFilter = new ColorGradingFilter({
    brightness: 0.1,
    contrast: 0.2,
    saturation: 0.3,
    temperature: 0.5
});

app.stage.filters = [colorFilter];

// Interactive controls
document.getElementById('brightness').addEventListener('input', (e) => {
    colorFilter.brightness = parseFloat(e.target.value);
});

document.getElementById('contrast').addEventListener('input', (e) => {
    colorFilter.contrast = parseFloat(e.target.value);
});
```

### 4. Outline Shader

Add colored outline to sprites:

```javascript
class OutlineFilter extends Filter {
    constructor(thickness = 2, color = 0xffffff) {
        const fragment = `
            in vec2 vTextureCoord;
            uniform sampler2D uTexture;
            uniform vec2 uTextureSize;
            uniform float uThickness;
            uniform vec3 uOutlineColor;

            out vec4 finalColor;

            void main() {
                vec2 pixelSize = 1.0 / uTextureSize;

                // Sample surrounding pixels
                float alpha = 0.0;
                for (float x = -uThickness; x <= uThickness; x++) {
                    for (float y = -uThickness; y <= uThickness; y++) {
                        vec2 offset = vec2(x, y) * pixelSize;
                        alpha = max(alpha, texture(uTexture, vTextureCoord + offset).a);
                    }
                }

                vec4 original = texture(uTexture, vTextureCoord);

                // If pixel is transparent but surrounded by opaque, it's an outline
                if (original.a < 0.5 && alpha > 0.5) {
                    finalColor = vec4(uOutlineColor, 1.0);
                } else {
                    finalColor = original;
                }
            }
        `;

        super({
            glProgram: new GlProgram({
                fragment,
                vertex: GlProgram.defaultVertexSrc
            }),
            resources: {
                outlineUniforms: {
                    uTextureSize: {
                        value: new Float32Array([256, 256]),
                        type: 'vec2<f32>'
                    },
                    uThickness: { value: thickness, type: 'f32' },
                    uOutlineColor: {
                        value: new Float32Array([
                            ((color >> 16) & 0xff) / 255,
                            ((color >> 8) & 0xff) / 255,
                            (color & 0xff) / 255
                        ]),
                        type: 'vec3<f32>'
                    }
                }
            }
        });
    }

    set thickness(value) {
        this.resources.outlineUniforms.uniforms.uThickness = value;
    }

    set color(value) {
        this.resources.outlineUniforms.uniforms.uOutlineColor[0] = ((value >> 16) & 0xff) / 255;
        this.resources.outlineUniforms.uniforms.uOutlineColor[1] = ((value >> 8) & 0xff) / 255;
        this.resources.outlineUniforms.uniforms.uOutlineColor[2] = (value & 0xff) / 255;
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
app.stage.addChild(sprite);

const outlineFilter = new OutlineFilter(3, 0xffff00);
sprite.filters = [outlineFilter];

// Animate outline color
let hue = 0;
app.ticker.add(() => {
    hue = (hue + 1) % 360;
    outlineFilter.color = hslToHex(hue, 100, 50);
});

function hslToHex(h, s, l) {
    l /= 100;
    const a = s * Math.min(l, 1 - l) / 100;
    const f = n => {
        const k = (n + h / 30) % 12;
        const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
        return Math.round(255 * color);
    };
    return (f(0) << 16) | (f(8) << 8) | f(4);
}
```

---

## Animation Patterns

### 1. Sprite Sheet Animation

Load and play sprite sheet animations:

```javascript
(async () => {
    // Load sprite sheet
    await PIXI.Assets.load('spritesheet.json');

    // Get animation frames
    const frames = [];
    for (let i = 0; i < 30; i++) {
        frames.push(PIXI.Texture.from(`run_${i}.png`));
    }

    // Create animated sprite
    const animatedSprite = new PIXI.AnimatedSprite(frames);
    animatedSprite.anchor.set(0.5);
    animatedSprite.position.set(400, 300);
    animatedSprite.animationSpeed = 0.5;
    animatedSprite.play();

    app.stage.addChild(animatedSprite);

    // Control playback
    document.getElementById('play').addEventListener('click', () => {
        animatedSprite.play();
    });

    document.getElementById('pause').addEventListener('click', () => {
        animatedSprite.stop();
    });

    document.getElementById('speed').addEventListener('input', (e) => {
        animatedSprite.animationSpeed = parseFloat(e.target.value);
    });
})();
```

### 2. Tweening Library Integration (GSAP)

Smooth animations with GSAP:

```javascript
import gsap from 'gsap';
import { PixiPlugin } from 'gsap/PixiPlugin';

// Register PIXI plugin
gsap.registerPlugin(PixiPlugin);
PixiPlugin.registerPIXI(PIXI);

// Create sprite
const sprite = new PIXI.Sprite(texture);
sprite.anchor.set(0.5);
sprite.position.set(100, 300);
app.stage.addChild(sprite);

// Animate with GSAP
gsap.to(sprite, {
    pixi: {
        x: 700,
        rotation: 360,
        scale: 1.5,
        tint: 0xff0000
    },
    duration: 2,
    ease: 'elastic.out(1, 0.5)',
    onComplete: () => {
        console.log('Animation complete!');
    }
});

// Complex timeline
const timeline = gsap.timeline({ repeat: -1, yoyo: true });

timeline
    .to(sprite, { pixi: { y: 100 }, duration: 1, ease: 'power2.out' })
    .to(sprite, { pixi: { x: 700 }, duration: 1, ease: 'power2.inOut' })
    .to(sprite, { pixi: { y: 500 }, duration: 1, ease: 'power2.in' })
    .to(sprite, { pixi: { x: 100 }, duration: 1, ease: 'power2.inOut' });
```

### 3. Custom Easing Functions

Implement custom easing without external libraries:

```javascript
class Tween {
    constructor(target, to, duration, easing = 'linear') {
        this.target = target;
        this.from = {};
        this.to = to;
        this.duration = duration;
        this.elapsed = 0;
        this.easing = this.easingFunctions[easing] || this.easingFunctions.linear;
        this.complete = false;
        this.onCompleteCallback = null;

        // Store starting values
        for (const key in to) {
            this.from[key] = target[key];
        }
    }

    easingFunctions = {
        linear: t => t,
        easeInQuad: t => t * t,
        easeOutQuad: t => t * (2 - t),
        easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
        easeInCubic: t => t * t * t,
        easeOutCubic: t => (--t) * t * t + 1,
        easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
        elastic: t => {
            if (t === 0 || t === 1) return t;
            const p = 0.3;
            return -Math.pow(2, 10 * (t - 1)) * Math.sin(((t - 1 - p / 4) * (2 * Math.PI)) / p);
        },
        bounce: t => {
            if (t < 1 / 2.75) {
                return 7.5625 * t * t;
            } else if (t < 2 / 2.75) {
                return 7.5625 * (t -= 1.5 / 2.75) * t + 0.75;
            } else if (t < 2.5 / 2.75) {
                return 7.5625 * (t -= 2.25 / 2.75) * t + 0.9375;
            } else {
                return 7.5625 * (t -= 2.625 / 2.75) * t + 0.984375;
            }
        }
    };

    update(deltaTime) {
        if (this.complete) return;

        this.elapsed += deltaTime;
        const progress = Math.min(this.elapsed / this.duration, 1);
        const easedProgress = this.easing(progress);

        // Update target properties
        for (const key in this.to) {
            const from = this.from[key];
            const to = this.to[key];
            this.target[key] = from + (to - from) * easedProgress;
        }

        // Check completion
        if (progress >= 1) {
            this.complete = true;
            if (this.onCompleteCallback) {
                this.onCompleteCallback();
            }
        }
    }

    onComplete(callback) {
        this.onCompleteCallback = callback;
        return this;
    }
}

// Tween manager
class TweenManager {
    constructor(app) {
        this.app = app;
        this.tweens = [];

        app.ticker.add((ticker) => this.update(ticker.deltaTime));
    }

    to(target, to, duration, easing) {
        const tween = new Tween(target, to, duration, easing);
        this.tweens.push(tween);
        return tween;
    }

    update(deltaTime) {
        for (let i = this.tweens.length - 1; i >= 0; i--) {
            const tween = this.tweens[i];
            tween.update(deltaTime * 0.016);  // Convert to seconds

            if (tween.complete) {
                this.tweens.splice(i, 1);
            }
        }
    }
}

// Usage
const tweenManager = new TweenManager(app);

const sprite = new PIXI.Sprite(texture);
sprite.position.set(100, 300);
app.stage.addChild(sprite);

tweenManager
    .to(sprite.position, { x: 700 }, 2, 'elastic')
    .onComplete(() => {
        console.log('Move complete!');

        tweenManager
            .to(sprite, { rotation: Math.PI * 2 }, 1, 'easeOutCubic')
            .onComplete(() => {
                console.log('Rotation complete!');
            });
    });
```

### 4. Path Following Animation

Make sprites follow curved paths:

```javascript
class PathFollower {
    constructor(sprite, path, duration) {
        this.sprite = sprite;
        this.path = path;  // Array of {x, y} points
        this.duration = duration;
        this.elapsed = 0;
    }

    update(deltaTime) {
        this.elapsed += deltaTime;
        const progress = Math.min(this.elapsed / this.duration, 1);

        // Get position along path
        const position = this.getPositionAtProgress(progress);
        this.sprite.position.set(position.x, position.y);

        // Get rotation based on direction
        if (progress < 1) {
            const futureProgress = Math.min(progress + 0.01, 1);
            const futurePosition = this.getPositionAtProgress(futureProgress);
            const angle = Math.atan2(
                futurePosition.y - position.y,
                futurePosition.x - position.x
            );
            this.sprite.rotation = angle;
        }

        return progress >= 1;
    }

    getPositionAtProgress(t) {
        // Catmull-Rom spline interpolation
        const points = this.path;
        const segmentCount = points.length - 1;
        const segment = Math.floor(t * segmentCount);
        const localT = (t * segmentCount) - segment;

        const p0 = points[Math.max(0, segment - 1)];
        const p1 = points[segment];
        const p2 = points[Math.min(points.length - 1, segment + 1)];
        const p3 = points[Math.min(points.length - 1, segment + 2)];

        const t2 = localT * localT;
        const t3 = t2 * localT;

        const x = 0.5 * (
            (2 * p1.x) +
            (-p0.x + p2.x) * localT +
            (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 +
            (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3
        );

        const y = 0.5 * (
            (2 * p1.y) +
            (-p0.y + p2.y) * localT +
            (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 +
            (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3
        );

        return { x, y };
    }
}

// Usage
const sprite = new PIXI.Sprite(texture);
sprite.anchor.set(0.5);
app.stage.addChild(sprite);

const path = [
    { x: 100, y: 300 },
    { x: 300, y: 100 },
    { x: 500, y: 300 },
    { x: 700, y: 500 },
    { x: 400, y: 550 }
];

const pathFollower = new PathFollower(sprite, path, 5000);

app.ticker.add((ticker) => {
    const complete = pathFollower.update(ticker.deltaTime * 16);
    if (complete) {
        console.log('Path complete!');
    }
});

// Visualize path
const graphics = new PIXI.Graphics();
graphics.moveTo(path[0].x, path[0].y);
for (let i = 1; i < path.length; i++) {
    graphics.lineTo(path[i].x, path[i].y);
}
graphics.stroke({ width: 2, color: 0xffffff, alpha: 0.3 });
app.stage.addChild(graphics);
```

---

## Performance Optimization

### 1. Object Pooling System

Reuse objects to avoid garbage collection:

```javascript
class ObjectPool {
    constructor(createFunc, resetFunc, initialSize = 100) {
        this.createFunc = createFunc;
        this.resetFunc = resetFunc;
        this.available = [];
        this.active = new Set();

        // Pre-create objects
        for (let i = 0; i < initialSize; i++) {
            this.available.push(this.createFunc());
        }
    }

    acquire() {
        let obj;

        if (this.available.length > 0) {
            obj = this.available.pop();
        } else {
            obj = this.createFunc();
            console.warn('Pool exhausted, creating new object');
        }

        this.active.add(obj);
        return obj;
    }

    release(obj) {
        if (this.active.has(obj)) {
            this.active.delete(obj);
            this.resetFunc(obj);
            this.available.push(obj);
        }
    }

    releaseAll() {
        for (const obj of this.active) {
            this.resetFunc(obj);
            this.available.push(obj);
        }
        this.active.clear();
    }

    getStats() {
        return {
            available: this.available.length,
            active: this.active.size,
            total: this.available.length + this.active.size
        };
    }
}

// Usage
const texture = await PIXI.Assets.load('bullet.png');

const bulletPool = new ObjectPool(
    // Create function
    () => {
        const bullet = new PIXI.Sprite(texture);
        bullet.anchor.set(0.5);
        return bullet;
    },
    // Reset function
    (bullet) => {
        bullet.visible = false;
        bullet.position.set(0, 0);
        bullet.rotation = 0;
    },
    50  // Initial size
);

// Shoot bullet
function shootBullet(x, y, angle) {
    const bullet = bulletPool.acquire();
    bullet.position.set(x, y);
    bullet.rotation = angle;
    bullet.visible = true;
    bullet.vx = Math.cos(angle) * 5;
    bullet.vy = Math.sin(angle) * 5;
    app.stage.addChild(bullet);
}

// Update bullets
app.ticker.add((ticker) => {
    for (const bullet of bulletPool.active) {
        bullet.x += bullet.vx * ticker.deltaTime;
        bullet.y += bullet.vy * ticker.deltaTime;

        // Release off-screen bullets
        if (bullet.x < 0 || bullet.x > 800 || bullet.y < 0 || bullet.y > 600) {
            app.stage.removeChild(bullet);
            bulletPool.release(bullet);
        }
    }
});

// Monitor pool
setInterval(() => {
    console.log('Bullet pool:', bulletPool.getStats());
}, 1000);
```

### 2. Viewport Culling

Only render visible sprites:

```javascript
class ViewportCuller {
    constructor(app, margin = 100) {
        this.app = app;
        this.margin = margin;
        this.trackedSprites = new Set();
    }

    track(sprite) {
        this.trackedSprites.add(sprite);
    }

    untrack(sprite) {
        this.trackedSprites.delete(sprite);
    }

    update() {
        const bounds = {
            left: -this.margin,
            right: this.app.screen.width + this.margin,
            top: -this.margin,
            bottom: this.app.screen.height + this.margin
        };

        for (const sprite of this.trackedSprites) {
            const spriteBounds = sprite.getBounds();

            const visible = (
                spriteBounds.x + spriteBounds.width >= bounds.left &&
                spriteBounds.x <= bounds.right &&
                spriteBounds.y + spriteBounds.height >= bounds.top &&
                spriteBounds.y <= bounds.bottom
            );

            sprite.renderable = visible;
        }
    }
}

// Usage
const culler = new ViewportCuller(app, 50);

// Create many sprites
for (let i = 0; i < 1000; i++) {
    const sprite = new PIXI.Sprite(texture);
    sprite.x = Math.random() * 2000 - 500;
    sprite.y = Math.random() * 2000 - 500;
    app.stage.addChild(sprite);
    culler.track(sprite);
}

app.ticker.add(() => {
    culler.update();
});

// Camera/viewport movement
let cameraX = 0;
let cameraY = 0;

window.addEventListener('keydown', (e) => {
    const speed = 10;
    switch (e.key) {
        case 'ArrowLeft': cameraX += speed; break;
        case 'ArrowRight': cameraX -= speed; break;
        case 'ArrowUp': cameraY += speed; break;
        case 'ArrowDown': cameraY -= speed; break;
    }

    app.stage.position.set(cameraX, cameraY);
});
```

### 3. Texture Atlases

Combine multiple textures into one for reduced draw calls:

```javascript
// Generate texture atlas programmatically
class TextureAtlas {
    constructor(app, textures, padding = 2) {
        this.app = app;
        this.textures = textures;
        this.padding = padding;
        this.atlas = null;
        this.frames = {};

        this.generate();
    }

    generate() {
        // Calculate atlas size using bin packing
        const rects = Object.entries(this.textures).map(([name, texture]) => ({
            name,
            width: texture.width + this.padding * 2,
            height: texture.height + this.padding * 2,
            texture
        }));

        // Sort by height (descending) for better packing
        rects.sort((a, b) => b.height - a.height);

        // Simple shelf packing algorithm
        let atlasWidth = 0;
        let atlasHeight = 0;
        let shelfY = 0;
        let shelfX = 0;
        let shelfHeight = 0;

        const packed = [];

        for (const rect of rects) {
            // Check if we need a new shelf
            if (shelfX + rect.width > 2048) {  // Max texture size
                shelfY += shelfHeight;
                shelfX = 0;
                shelfHeight = 0;
            }

            rect.x = shelfX + this.padding;
            rect.y = shelfY + this.padding;

            shelfX += rect.width;
            shelfHeight = Math.max(shelfHeight, rect.height);

            atlasWidth = Math.max(atlasWidth, shelfX);
            atlasHeight = Math.max(atlasHeight, shelfY + shelfHeight);

            packed.push(rect);
        }

        // Round up to power of 2
        atlasWidth = Math.pow(2, Math.ceil(Math.log2(atlasWidth)));
        atlasHeight = Math.pow(2, Math.ceil(Math.log2(atlasHeight)));

        // Create canvas for atlas
        const canvas = document.createElement('canvas');
        canvas.width = atlasWidth;
        canvas.height = atlasHeight;
        const ctx = canvas.getContext('2d');

        // Draw all textures to canvas
        for (const rect of packed) {
            const source = rect.texture.source;
            ctx.drawImage(
                source.resource,
                rect.x,
                rect.y,
                rect.texture.width,
                rect.texture.height
            );

            // Store frame data
            this.frames[rect.name] = {
                x: rect.x,
                y: rect.y,
                width: rect.texture.width,
                height: rect.texture.height
            };
        }

        // Create PixiJS texture from canvas
        this.atlas = PIXI.Texture.from(canvas);
    }

    getFrame(name) {
        const frame = this.frames[name];
        if (!frame) return null;

        return new PIXI.Texture({
            source: this.atlas.source,
            frame: new PIXI.Rectangle(frame.x, frame.y, frame.width, frame.height)
        });
    }
}

// Usage
const textures = {
    'player': await PIXI.Assets.load('player.png'),
    'enemy': await PIXI.Assets.load('enemy.png'),
    'bullet': await PIXI.Assets.load('bullet.png'),
    'powerup': await PIXI.Assets.load('powerup.png')
};

const atlas = new TextureAtlas(app, textures);

// Use frames from atlas
const player = new PIXI.Sprite(atlas.getFrame('player'));
const enemy = new PIXI.Sprite(atlas.getFrame('enemy'));

// All sprites now share one texture = one draw call!
```

### 4. Spatial Hashing for Collisions

Optimize collision detection from O(n²) to O(n):

```javascript
class SpatialHash {
    constructor(cellSize = 100) {
        this.cellSize = cellSize;
        this.cells = new Map();
    }

    clear() {
        this.cells.clear();
    }

    insert(obj) {
        const bounds = obj.getBounds();
        const cells = this.getCellsForBounds(bounds);

        for (const cellKey of cells) {
            if (!this.cells.has(cellKey)) {
                this.cells.set(cellKey, new Set());
            }
            this.cells.get(cellKey).add(obj);
        }
    }

    getCellsForBounds(bounds) {
        const cells = [];

        const minX = Math.floor(bounds.x / this.cellSize);
        const maxX = Math.floor((bounds.x + bounds.width) / this.cellSize);
        const minY = Math.floor(bounds.y / this.cellSize);
        const maxY = Math.floor((bounds.y + bounds.height) / this.cellSize);

        for (let x = minX; x <= maxX; x++) {
            for (let y = minY; y <= maxY; y++) {
                cells.push(`${x},${y}`);
            }
        }

        return cells;
    }

    getNearby(obj) {
        const bounds = obj.getBounds();
        const cells = this.getCellsForBounds(bounds);
        const nearby = new Set();

        for (const cellKey of cells) {
            const cell = this.cells.get(cellKey);
            if (cell) {
                for (const other of cell) {
                    if (other !== obj) {
                        nearby.add(other);
                    }
                }
            }
        }

        return nearby;
    }
}

// Usage
const spatialHash = new SpatialHash(100);
const sprites = [];

// Create many sprites
for (let i = 0; i < 500; i++) {
    const sprite = new PIXI.Sprite(texture);
    sprite.position.set(
        Math.random() * 800,
        Math.random() * 600
    );
    sprite.vx = (Math.random() - 0.5) * 3;
    sprite.vy = (Math.random() - 0.5) * 3;
    app.stage.addChild(sprite);
    sprites.push(sprite);
}

app.ticker.add((ticker) => {
    // Update positions
    for (const sprite of sprites) {
        sprite.x += sprite.vx * ticker.deltaTime;
        sprite.y += sprite.vy * ticker.deltaTime;

        // Bounce off edges
        if (sprite.x < 0 || sprite.x > 800) sprite.vx *= -1;
        if (sprite.y < 0 || sprite.y > 600) sprite.vy *= -1;
    }

    // Rebuild spatial hash
    spatialHash.clear();
    for (const sprite of sprites) {
        spatialHash.insert(sprite);
    }

    // Check collisions (only nearby sprites)
    for (const sprite of sprites) {
        const nearby = spatialHash.getNearby(sprite);

        for (const other of nearby) {
            if (checkCollision(sprite, other)) {
                // Handle collision
                sprite.tint = 0xff0000;
                other.tint = 0xff0000;
            } else {
                sprite.tint = 0xffffff;
            }
        }
    }
});

function checkCollision(a, b) {
    const ab = a.getBounds();
    const bb = b.getBounds();

    return ab.x < bb.x + bb.width &&
           ab.x + ab.width > bb.x &&
           ab.y < bb.y + bb.height &&
           ab.y + ab.height > bb.y;
}
```

---

## Game Development

### 1. Simple Platformer Physics

Basic 2D platformer with jumping and gravity:

```javascript
class Player {
    constructor(app, x, y) {
        this.app = app;

        // Create sprite
        const graphics = new PIXI.Graphics();
        graphics.rect(0, 0, 32, 48).fill(0x3498db);
        const texture = app.renderer.generateTexture(graphics);
        this.sprite = new PIXI.Sprite(texture);
        this.sprite.position.set(x, y);
        app.stage.addChild(this.sprite);

        // Physics
        this.vx = 0;
        this.vy = 0;
        this.isGrounded = false;
        this.gravity = 0.5;
        this.jumpPower = -12;
        this.moveSpeed = 5;

        // Input
        this.keys = {};
        this.setupInput();
    }

    setupInput() {
        window.addEventListener('keydown', (e) => {
            this.keys[e.key] = true;

            if (e.key === ' ' && this.isGrounded) {
                this.vy = this.jumpPower;
                this.isGrounded = false;
            }
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.key] = false;
        });
    }

    update(platforms) {
        // Horizontal movement
        this.vx = 0;
        if (this.keys['ArrowLeft']) this.vx = -this.moveSpeed;
        if (this.keys['ArrowRight']) this.vx = this.moveSpeed;

        // Apply gravity
        if (!this.isGrounded) {
            this.vy += this.gravity;
        }

        // Update position
        this.sprite.x += this.vx;
        this.sprite.y += this.vy;

        // Check platform collisions
        this.isGrounded = false;

        for (const platform of platforms) {
            if (this.checkCollision(platform)) {
                // Resolve collision
                const playerBottom = this.sprite.y + this.sprite.height;
                const platformTop = platform.y;

                if (this.vy > 0 && playerBottom <= platformTop + this.vy) {
                    // Landing on platform
                    this.sprite.y = platformTop - this.sprite.height;
                    this.vy = 0;
                    this.isGrounded = true;
                }
            }
        }

        // Keep in bounds
        if (this.sprite.x < 0) this.sprite.x = 0;
        if (this.sprite.x > 800 - this.sprite.width) {
            this.sprite.x = 800 - this.sprite.width;
        }
    }

    checkCollision(platform) {
        return this.sprite.x < platform.x + platform.width &&
               this.sprite.x + this.sprite.width > platform.x &&
               this.sprite.y < platform.y + platform.height &&
               this.sprite.y + this.sprite.height > platform.y;
    }
}

// Usage
const player = new Player(app, 100, 100);

// Create platforms
const platforms = [
    { x: 0, y: 550, width: 800, height: 50 },    // Ground
    { x: 200, y: 450, width: 150, height: 20 },
    { x: 450, y: 350, width: 150, height: 20 },
    { x: 100, y: 250, width: 150, height: 20 }
];

// Draw platforms
for (const platform of platforms) {
    const graphics = new PIXI.Graphics();
    graphics.rect(platform.x, platform.y, platform.width, platform.height)
        .fill(0x2ecc71);
    app.stage.addChild(graphics);
}

// Game loop
app.ticker.add(() => {
    player.update(platforms);
});
```

### 2. Top-Down Movement

8-direction movement with collision:

```javascript
class TopDownCharacter {
    constructor(app, x, y) {
        this.app = app;

        const graphics = new PIXI.Graphics();
        graphics.circle(16, 16, 16).fill(0xe74c3c);
        const texture = app.renderer.generateTexture(graphics);
        this.sprite = new PIXI.Sprite(texture);
        this.sprite.anchor.set(0.5);
        this.sprite.position.set(x, y);
        app.stage.addChild(this.sprite);

        this.speed = 3;
        this.keys = {};

        window.addEventListener('keydown', (e) => this.keys[e.key] = true);
        window.addEventListener('keyup', (e) => this.keys[e.key] = false);
    }

    update(obstacles = []) {
        let dx = 0;
        let dy = 0;

        if (this.keys['w'] || this.keys['ArrowUp']) dy -= this.speed;
        if (this.keys['s'] || this.keys['ArrowDown']) dy += this.speed;
        if (this.keys['a'] || this.keys['ArrowLeft']) dx -= this.speed;
        if (this.keys['d'] || this.keys['ArrowRight']) dx += this.speed;

        // Normalize diagonal movement
        if (dx !== 0 && dy !== 0) {
            dx *= 0.707;  // 1/√2
            dy *= 0.707;
        }

        // Try horizontal movement
        this.sprite.x += dx;
        if (this.checkCollisions(obstacles)) {
            this.sprite.x -= dx;
        }

        // Try vertical movement
        this.sprite.y += dy;
        if (this.checkCollisions(obstacles)) {
            this.sprite.y -= dy;
        }

        // Face movement direction
        if (dx !== 0 || dy !== 0) {
            this.sprite.rotation = Math.atan2(dy, dx);
        }
    }

    checkCollisions(obstacles) {
        for (const obstacle of obstacles) {
            const bounds = this.sprite.getBounds();

            if (bounds.x < obstacle.x + obstacle.width &&
                bounds.x + bounds.width > obstacle.x &&
                bounds.y < obstacle.y + obstacle.height &&
                bounds.y + bounds.height > obstacle.y) {
                return true;
            }
        }
        return false;
    }
}

// Usage
const character = new TopDownCharacter(app, 400, 300);

const obstacles = [
    { x: 200, y: 200, width: 100, height: 100 },
    { x: 500, y: 300, width: 80, height: 120 }
];

// Draw obstacles
for (const obstacle of obstacles) {
    const graphics = new PIXI.Graphics();
    graphics.rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        .fill(0x95a5a6);
    app.stage.addChild(graphics);
}

app.ticker.add(() => {
    character.update(obstacles);
});
```

### 3. Health Bar Component

Reusable health bar UI:

```javascript
class HealthBar extends PIXI.Container {
    constructor(maxHealth = 100, width = 100, height = 10) {
        super();

        this.maxHealth = maxHealth;
        this.currentHealth = maxHealth;
        this.barWidth = width;
        this.barHeight = height;

        // Background (red)
        this.background = new PIXI.Graphics();
        this.background.rect(0, 0, width, height).fill(0xff0000);
        this.addChild(this.background);

        // Foreground (green)
        this.foreground = new PIXI.Graphics();
        this.foreground.rect(0, 0, width, height).fill(0x00ff00);
        this.addChild(this.foreground);

        // Border
        this.border = new PIXI.Graphics();
        this.border.rect(0, 0, width, height)
            .stroke({ width: 2, color: 0x000000 });
        this.addChild(this.border);
    }

    setHealth(value) {
        this.currentHealth = Math.max(0, Math.min(value, this.maxHealth));
        this.updateBar();
    }

    damage(amount) {
        this.setHealth(this.currentHealth - amount);
    }

    heal(amount) {
        this.setHealth(this.currentHealth + amount);
    }

    updateBar() {
        const percentage = this.currentHealth / this.maxHealth;
        const newWidth = this.barWidth * percentage;

        // Animate width
        this.foreground.clear();
        this.foreground.rect(0, 0, newWidth, this.barHeight).fill(this.getHealthColor());
    }

    getHealthColor() {
        const percentage = this.currentHealth / this.maxHealth;

        if (percentage > 0.5) return 0x00ff00;  // Green
        if (percentage > 0.25) return 0xffff00; // Yellow
        return 0xff0000;  // Red
    }
}

// Usage
const enemy = new PIXI.Sprite(texture);
enemy.position.set(400, 300);
app.stage.addChild(enemy);

const healthBar = new HealthBar(100, 80, 8);
healthBar.position.set(enemy.x - 40, enemy.y - 50);
app.stage.addChild(healthBar);

// Damage over time
setInterval(() => {
    healthBar.damage(10);

    if (healthBar.currentHealth === 0) {
        console.log('Enemy defeated!');
    }
}, 1000);
```

### 4. State Machine for Game Logic

Manage game states (menu, playing, paused, game over):

```javascript
class StateMachine {
    constructor() {
        this.states = new Map();
        this.currentState = null;
    }

    addState(name, state) {
        this.states.set(name, state);
    }

    setState(name) {
        if (this.currentState) {
            this.currentState.exit?.();
        }

        const newState = this.states.get(name);
        if (newState) {
            this.currentState = newState;
            newState.enter?.();
        }
    }

    update(deltaTime) {
        this.currentState?.update?.(deltaTime);
    }

    render() {
        this.currentState?.render?.();
    }
}

// Game states
class MenuState {
    constructor(app, stateMachine) {
        this.app = app;
        this.stateMachine = stateMachine;
        this.container = new PIXI.Container();

        const title = new PIXI.Text({
            text: 'Main Menu',
            style: { fontSize: 64, fill: 0xffffff }
        });
        title.anchor.set(0.5);
        title.position.set(400, 200);
        this.container.addChild(title);

        const startButton = new PIXI.Text({
            text: 'Start Game',
            style: { fontSize: 32, fill: 0x00ff00 }
        });
        startButton.anchor.set(0.5);
        startButton.position.set(400, 350);
        startButton.eventMode = 'static';
        startButton.cursor = 'pointer';
        startButton.on('pointerdown', () => {
            stateMachine.setState('playing');
        });
        this.container.addChild(startButton);
    }

    enter() {
        this.app.stage.addChild(this.container);
    }

    exit() {
        this.app.stage.removeChild(this.container);
    }
}

class PlayingState {
    constructor(app, stateMachine) {
        this.app = app;
        this.stateMachine = stateMachine;
        this.container = new PIXI.Container();
        this.score = 0;

        this.scoreText = new PIXI.Text({
            text: 'Score: 0',
            style: { fontSize: 24, fill: 0xffffff }
        });
        this.scoreText.position.set(10, 10);
        this.container.addChild(this.scoreText);

        // Setup pause key
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.stateMachine.currentState === this) {
                this.stateMachine.setState('paused');
            }
        });
    }

    enter() {
        this.app.stage.addChild(this.container);
        this.score = 0;
    }

    exit() {
        // Keep container for paused state
    }

    update(deltaTime) {
        // Game logic here
        this.score++;
        this.scoreText.text = `Score: ${Math.floor(this.score / 60)}`;
    }
}

class PausedState {
    constructor(app, stateMachine) {
        this.app = app;
        this.stateMachine = stateMachine;
        this.container = new PIXI.Container();

        const overlay = new PIXI.Graphics();
        overlay.rect(0, 0, 800, 600).fill({ color: 0x000000, alpha: 0.7 });
        this.container.addChild(overlay);

        const pausedText = new PIXI.Text({
            text: 'PAUSED',
            style: { fontSize: 64, fill: 0xffffff }
        });
        pausedText.anchor.set(0.5);
        pausedText.position.set(400, 250);
        this.container.addChild(pausedText);

        const resumeButton = new PIXI.Text({
            text: 'Resume',
            style: { fontSize: 32, fill: 0x00ff00 }
        });
        resumeButton.anchor.set(0.5);
        resumeButton.position.set(400, 350);
        resumeButton.eventMode = 'static';
        resumeButton.cursor = 'pointer';
        resumeButton.on('pointerdown', () => {
            stateMachine.setState('playing');
        });
        this.container.addChild(resumeButton);
    }

    enter() {
        this.app.stage.addChild(this.container);
    }

    exit() {
        this.app.stage.removeChild(this.container);
    }
}

// Usage
const stateMachine = new StateMachine();

stateMachine.addState('menu', new MenuState(app, stateMachine));
stateMachine.addState('playing', new PlayingState(app, stateMachine));
stateMachine.addState('paused', new PausedState(app, stateMachine));

stateMachine.setState('menu');

app.ticker.add((ticker) => {
    stateMachine.update(ticker.deltaTime);
});
```

---

## UI Components

### 1. Progress Bar

Animated progress bar with percentage:

```javascript
class ProgressBar extends PIXI.Container {
    constructor(width = 200, height = 30, options = {}) {
        super();

        const {
            backgroundColor = 0x333333,
            fillColor = 0x3498db,
            borderColor = 0xffffff,
            borderWidth = 2,
            showPercentage = true
        } = options;

        this.barWidth = width;
        this.barHeight = height;
        this.progress = 0;
        this.targetProgress = 0;
        this.animationSpeed = 0.05;

        // Background
        this.background = new PIXI.Graphics();
        this.background.roundRect(0, 0, width, height, 5).fill(backgroundColor);
        this.addChild(this.background);

        // Fill
        this.fill = new PIXI.Graphics();
        this.addChild(this.fill);

        // Border
        this.border = new PIXI.Graphics();
        this.border.roundRect(0, 0, width, height, 5)
            .stroke({ width: borderWidth, color: borderColor });
        this.addChild(this.border);

        // Percentage text
        if (showPercentage) {
            this.percentageText = new PIXI.Text({
                text: '0%',
                style: {
                    fontSize: height * 0.6,
                    fill: 0xffffff,
                    fontWeight: 'bold'
                }
            });
            this.percentageText.anchor.set(0.5);
            this.percentageText.position.set(width / 2, height / 2);
            this.addChild(this.percentageText);
        }

        this.fillColor = fillColor;
        this.updateBar();
    }

    setProgress(value, animate = true) {
        this.targetProgress = Math.max(0, Math.min(1, value));
        if (!animate) {
            this.progress = this.targetProgress;
            this.updateBar();
        }
    }

    update() {
        if (Math.abs(this.targetProgress - this.progress) > 0.001) {
            this.progress += (this.targetProgress - this.progress) * this.animationSpeed;
            this.updateBar();
        }
    }

    updateBar() {
        const fillWidth = this.barWidth * this.progress;

        this.fill.clear();
        if (fillWidth > 0) {
            this.fill.roundRect(0, 0, fillWidth, this.barHeight, 5).fill(this.fillColor);
        }

        if (this.percentageText) {
            this.percentageText.text = `${Math.round(this.progress * 100)}%`;
        }
    }
}

// Usage
const loadingBar = new ProgressBar(400, 40, {
    backgroundColor: 0x2c3e50,
    fillColor: 0x27ae60,
    showPercentage: true
});

loadingBar.position.set(200, 280);
app.stage.addChild(loadingBar);

// Simulate loading
let loaded = 0;
const interval = setInterval(() => {
    loaded += 0.1;
    loadingBar.setProgress(loaded);

    if (loaded >= 1) {
        clearInterval(interval);
        console.log('Loading complete!');
    }
}, 100);

app.ticker.add(() => {
    loadingBar.update();
});
```

### 2. Modal Dialog

Reusable modal dialog component:

```javascript
class Modal extends PIXI.Container {
    constructor(title, message, buttons = ['OK']) {
        super();

        // Dark overlay
        this.overlay = new PIXI.Graphics();
        this.overlay.rect(0, 0, 800, 600).fill({ color: 0x000000, alpha: 0.7 });
        this.overlay.eventMode = 'static';  // Block clicks
        this.addChild(this.overlay);

        // Modal background
        this.modal = new PIXI.Graphics();
        this.modal.roundRect(200, 150, 400, 300, 10).fill(0xffffff);
        this.modal.roundRect(200, 150, 400, 300, 10)
            .stroke({ width: 3, color: 0x3498db });
        this.addChild(this.modal);

        // Title
        const titleText = new PIXI.Text({
            text: title,
            style: {
                fontSize: 32,
                fill: 0x2c3e50,
                fontWeight: 'bold'
            }
        });
        titleText.anchor.set(0.5, 0);
        titleText.position.set(400, 170);
        this.addChild(titleText);

        // Message
        const messageText = new PIXI.Text({
            text: message,
            style: {
                fontSize: 20,
                fill: 0x34495e,
                align: 'center',
                wordWrap: true,
                wordWrapWidth: 350
            }
        });
        messageText.anchor.set(0.5);
        messageText.position.set(400, 280);
        this.addChild(messageText);

        // Buttons
        const buttonContainer = new PIXI.Container();
        const buttonWidth = 120;
        const buttonSpacing = 20;
        const totalWidth = buttons.length * buttonWidth + (buttons.length - 1) * buttonSpacing;

        buttons.forEach((label, index) => {
            const button = this.createButton(label, buttonWidth, 40);
            button.position.set(
                index * (buttonWidth + buttonSpacing),
                0
            );
            buttonContainer.addChild(button);
        });

        buttonContainer.position.set(400 - totalWidth / 2, 380);
        this.addChild(buttonContainer);

        this.visible = false;
    }

    createButton(label, width, height) {
        const button = new PIXI.Container();

        const bg = new PIXI.Graphics();
        bg.roundRect(0, 0, width, height, 5).fill(0x3498db);
        button.addChild(bg);

        const text = new PIXI.Text({
            text: label,
            style: {
                fontSize: 18,
                fill: 0xffffff,
                fontWeight: 'bold'
            }
        });
        text.anchor.set(0.5);
        text.position.set(width / 2, height / 2);
        button.addChild(text);

        button.eventMode = 'static';
        button.cursor = 'pointer';

        button.on('pointerover', () => {
            bg.clear();
            bg.roundRect(0, 0, width, height, 5).fill(0x2980b9);
        });

        button.on('pointerout', () => {
            bg.clear();
            bg.roundRect(0, 0, width, height, 5).fill(0x3498db);
        });

        button.on('pointerdown', () => {
            this.visible = false;
            this.emit('buttonClick', label);
        });

        return button;
    }

    show() {
        this.visible = true;
    }

    hide() {
        this.visible = false;
    }
}

// Usage
const modal = new Modal(
    'Game Over',
    'You scored 1,234 points!\nWould you like to play again?',
    ['Play Again', 'Main Menu', 'Quit']
);

app.stage.addChild(modal);

modal.on('buttonClick', (button) => {
    console.log(`Clicked: ${button}`);

    if (button === 'Play Again') {
        startGame();
    } else if (button === 'Main Menu') {
        showMenu();
    } else if (button === 'Quit') {
        quitGame();
    }
});

// Show modal after 3 seconds
setTimeout(() => {
    modal.show();
}, 3000);
```

### 3. Slider Component

Interactive slider for settings:

```javascript
class Slider extends PIXI.Container {
    constructor(min = 0, max = 100, value = 50, width = 200) {
        super();

        this.min = min;
        this.max = max;
        this.value = value;
        this.width = width;
        this.isDragging = false;

        // Track
        this.track = new PIXI.Graphics();
        this.track.roundRect(0, -2, width, 4, 2).fill(0x7f8c8d);
        this.addChild(this.track);

        // Fill
        this.fill = new PIXI.Graphics();
        this.addChild(this.fill);

        // Handle
        this.handle = new PIXI.Graphics();
        this.handle.circle(0, 0, 10).fill(0x3498db);
        this.handle.circle(0, 0, 10).stroke({ width: 2, color: 0xffffff });
        this.handle.eventMode = 'static';
        this.handle.cursor = 'pointer';
        this.addChild(this.handle);

        // Events
        this.handle.on('pointerdown', this.onDragStart.bind(this));
        this.handle.on('pointerup', this.onDragEnd.bind(this));
        this.handle.on('pointerupoutside', this.onDragEnd.bind(this));

        this.updateVisuals();
    }

    onDragStart(event) {
        this.isDragging = true;
        this.handle.on('globalpointermove', this.onDragMove.bind(this));
    }

    onDragMove(event) {
        if (!this.isDragging) return;

        const localX = event.global.x - this.getGlobalPosition().x;
        const percentage = Math.max(0, Math.min(1, localX / this.width));
        this.setValue(this.min + (this.max - this.min) * percentage);
    }

    onDragEnd() {
        this.isDragging = false;
        this.handle.off('globalpointermove');
    }

    setValue(value) {
        this.value = Math.max(this.min, Math.min(this.max, value));
        this.updateVisuals();
        this.emit('change', this.value);
    }

    updateVisuals() {
        const percentage = (this.value - this.min) / (this.max - this.min);
        const handleX = this.width * percentage;

        // Update fill
        this.fill.clear();
        this.fill.roundRect(0, -2, handleX, 4, 2).fill(0x3498db);

        // Update handle position
        this.handle.position.set(handleX, 0);
    }
}

// Usage
const volumeSlider = new Slider(0, 100, 75, 250);
volumeSlider.position.set(275, 300);
app.stage.addChild(volumeSlider);

const label = new PIXI.Text({
    text: 'Volume: 75',
    style: { fontSize: 20, fill: 0xffffff }
});
label.position.set(275, 270);
app.stage.addChild(label);

volumeSlider.on('change', (value) => {
    label.text = `Volume: ${Math.round(value)}`;
    console.log('Volume changed to:', value);
});
```

---

(Continuing with Framework Integration, Mobile Optimization, and Advanced Techniques in next message due to length constraints...)

## Framework Integration

### 1. React Integration with @pixi/react

Use PixiJS components in React:

```javascript
// Install: npm install @pixi/react pixi.js

import { Stage, Container, Sprite, useApp, useTick } from '@pixi/react';
import { useState, useCallback } from 'react';
import * as PIXI from 'pixi.js';

// Animated sprite component
function RotatingSprite({ x, y, texture }) {
    const [rotation, setRotation] = useState(0);

    useTick((delta) => {
        setRotation((prev) => prev + 0.05 * delta);
    });

    return (
        <Sprite
            texture={texture}
            x={x}
            y={y}
            anchor={0.5}
            rotation={rotation}
        />
    );
}

// Interactive sprite
function DraggableSprite({ initialX, initialY, texture }) {
    const [position, setPosition] = useState({ x: initialX, y: initialY });
    const [isDragging, setIsDragging] = useState(false);

    const handlePointerDown = useCallback(() => {
        setIsDragging(true);
    }, []);

    const handlePointerUp = useCallback(() => {
        setIsDragging(false);
    }, []);

    const handlePointerMove = useCallback((event) => {
        if (isDragging) {
            setPosition({
                x: event.global.x,
                y: event.global.y
            });
        }
    }, [isDragging]);

    return (
        <Sprite
            texture={texture}
            x={position.x}
            y={position.y}
            anchor={0.5}
            interactive
            pointerdown={handlePointerDown}
            pointerup={handlePointerUp}
            pointerupoutside={handlePointerUp}
            pointermove={handlePointerMove}
            cursor="pointer"
        />
    );
}

// Main app component
function PixiApp() {
    const [bunnyTexture] = useState(() => PIXI.Texture.from('bunny.png'));
    const [spriteCount, setSpriteCount] = useState(5);

    return (
        <div>
            <button onClick={() => setSpriteCount(prev => prev + 5)}>
                Add Sprites
            </button>
            <Stage width={800} height={600} options={{ backgroundColor: 0x1099bb }}>
                <Container>
                    {Array.from({ length: spriteCount }, (_, i) => (
                        <RotatingSprite
                            key={i}
                            x={Math.random() * 800}
                            y={Math.random() * 600}
                            texture={bunnyTexture}
                        />
                    ))}
                    <DraggableSprite
                        initialX={400}
                        initialY={300}
                        texture={bunnyTexture}
                    />
                </Container>
            </Stage>
        </div>
    );
}

export default PixiApp;
```

### 2. Vue Integration

```javascript
// Install: npm install vue pixi.js

<template>
  <div>
    <div ref="pixiContainer"></div>
    <div class="controls">
      <button @click="addSprite">Add Sprite</button>
      <button @click="clearSprites">Clear</button>
      <p>Sprites: {{ sprites.length }}</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import * as PIXI from 'pixi.js';

export default {
    setup() {
        const pixiContainer = ref(null);
        let app = null;
        const sprites = ref([]);

        onMounted(async () => {
            app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x1099bb
            });

            pixiContainer.value.appendChild(app.canvas);

            // Start ticker
            app.ticker.add((ticker) => {
                sprites.value.forEach(sprite => {
                    sprite.rotation += 0.05 * ticker.deltaTime;
                });
            });
        });

        onUnmounted(() => {
            app?.destroy(true, { children: true });
        });

        const addSprite = async () => {
            if (!app) return;

            const texture = await PIXI.Assets.load('bunny.png');
            const sprite = new PIXI.Sprite(texture);

            sprite.anchor.set(0.5);
            sprite.position.set(
                Math.random() * 800,
                Math.random() * 600
            );

            app.stage.addChild(sprite);
            sprites.value.push(sprite);
        };

        const clearSprites = () => {
            sprites.value.forEach(sprite => {
                app.stage.removeChild(sprite);
                sprite.destroy();
            });
            sprites.value = [];
        };

        return {
            pixiContainer,
            sprites,
            addSprite,
            clearSprites
        };
    }
};
</script>

<style scoped>
.controls {
    margin-top: 20px;
}

button {
    margin-right: 10px;
    padding: 10px 20px;
}
</style>
```

---

## Mobile Optimization

### 1. Touch Controls

Implement mobile-friendly touch controls:

```javascript
class TouchJoystick {
    constructor(app, options = {}) {
        this.app = app;
        this.container = new PIXI.Container();
        this.isActive = false;
        this.centerX = 0;
        this.centerY = 0;
        this.touchId = null;

        const { radius = 60, color = 0x3498db } = options;

        // Outer circle (base)
        this.base = new PIXI.Graphics();
        this.base.circle(0, 0, radius).fill({ color: 0x000000, alpha: 0.3 });
        this.base.circle(0, 0, radius).stroke({ width: 3, color, alpha: 0.5 });
        this.container.addChild(this.base);

        // Inner circle (stick)
        this.stick = new PIXI.Graphics();
        this.stick.circle(0, 0, radius / 2).fill({ color, alpha: 0.7 });
        this.container.addChild(this.stick);

        this.radius = radius;
        this.container.position.set(100, app.screen.height - 100);
        this.container.alpha = 0.5;

        app.stage.addChild(this.container);

        // Touch events
        app.stage.eventMode = 'static';
        app.stage.on('pointerdown', this.onTouchStart.bind(this));
        app.stage.on('pointermove', this.onTouchMove.bind(this));
        app.stage.on('pointerup', this.onTouchEnd.bind(this));
        app.stage.on('pointerupoutside', this.onTouchEnd.bind(this));

        this.direction = { x: 0, y: 0 };
        this.magnitude = 0;
    }

    onTouchStart(event) {
        const pos = event.global;
        const dist = this.distance(
            pos.x,
            pos.y,
            this.container.x,
            this.container.y
        );

        if (dist < this.radius * 1.5) {
            this.isActive = true;
            this.touchId = event.pointerId;
            this.container.alpha = 1;
        }
    }

    onTouchMove(event) {
        if (!this.isActive || event.pointerId !== this.touchId) return;

        const pos = event.global;
        const dx = pos.x - this.container.x;
        const dy = pos.y - this.container.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > this.radius) {
            // Clamp to radius
            this.stick.position.set(
                (dx / dist) * this.radius,
                (dy / dist) * this.radius
            );
            this.magnitude = 1;
        } else {
            this.stick.position.set(dx, dy);
            this.magnitude = dist / this.radius;
        }

        // Normalized direction
        if (dist > 0) {
            this.direction.x = dx / dist;
            this.direction.y = dy / dist;
        }
    }

    onTouchEnd(event) {
        if (event.pointerId === this.touchId) {
            this.isActive = false;
            this.touchId = null;
            this.stick.position.set(0, 0);
            this.container.alpha = 0.5;
            this.direction = { x: 0, y: 0 };
            this.magnitude = 0;
        }
    }

    distance(x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        return Math.sqrt(dx * dx + dy * dy);
    }

    getDirection() {
        return {
            x: this.direction.x * this.magnitude,
            y: this.direction.y * this.magnitude
        };
    }
}

// Usage
const joystick = new TouchJoystick(app, { radius: 70, color: 0xe74c3c });

const player = new PIXI.Sprite(texture);
player.anchor.set(0.5);
player.position.set(400, 300);
app.stage.addChild(player);

app.ticker.add((ticker) => {
    const dir = joystick.getDirection();
    const speed = 5;

    player.x += dir.x * speed * ticker.deltaTime;
    player.y += dir.y * speed * ticker.deltaTime;

    // Keep in bounds
    player.x = Math.max(0, Math.min(app.screen.width, player.x));
    player.y = Math.max(0, Math.min(app.screen.height, player.y));
});
```

### 2. Device Detection and Adaptive Settings

```javascript
class DeviceOptimizer {
    constructor(app) {
        this.app = app;
        this.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        this.isLowEnd = this.detectLowEndDevice();

        this.applyOptimizations();
    }

    detectLowEndDevice() {
        // Check hardware concurrency (CPU cores)
        const cores = navigator.hardwareConcurrency || 2;

        // Check device memory (if available)
        const memory = navigator.deviceMemory || 4;

        // Low-end: < 4 cores or < 4GB RAM
        return cores < 4 || memory < 4 || this.isMobile;
    }

    applyOptimizations() {
        if (this.isLowEnd) {
            console.log('Applying low-end device optimizations');

            // Reduce resolution
            this.app.renderer.resolution = 1;

            // Disable antialiasing
            this.app.renderer.antialias = false;

            // Reduce max FPS
            this.app.ticker.maxFPS = 30;

            return {
                maxSprites: 50,
                particleLimit: 100,
                enableFilters: false,
                textureQuality: 'low'
            };
        } else {
            console.log('Using high-quality settings');

            return {
                maxSprites: 500,
                particleLimit: 5000,
                enableFilters: true,
                textureQuality: 'high'
            };
        }
    }

    getOptimalSettings() {
        return this.applyOptimizations();
    }
}

// Usage
(async () => {
    const app = new PIXI.Application();
    await app.init({
        width: window.innerWidth,
        height: window.innerHeight,
        backgroundColor: 0x1a1a2e
    });

    const optimizer = new DeviceOptimizer(app);
    const settings = optimizer.getOptimalSettings();

    console.log('Device settings:', settings);

    // Use settings to configure game
    for (let i = 0; i < settings.maxSprites; i++) {
        const sprite = new PIXI.Sprite(texture);
        // ... create sprites based on limit
    }
})();
```

---

## Advanced Techniques

### 1. Custom Render Texture

Render to texture for post-processing or caching:

```javascript
class RenderTextureEffect {
    constructor(app) {
        this.app = app;

        // Create render texture
        this.renderTexture = PIXI.RenderTexture.create({
            width: app.screen.width,
            height: app.screen.height
        });

        // Sprite to display the rendered texture
        this.outputSprite = new PIXI.Sprite(this.renderTexture);

        // Container for objects to render
        this.sceneContainer = new PIXI.Container();
    }

    render() {
        // Render scene to texture
        this.app.renderer.render({
            container: this.sceneContainer,
            target: this.renderTexture,
            clear: true
        });
    }

    getSprite() {
        return this.outputSprite;
    }

    getContainer() {
        return this.sceneContainer;
    }
}

// Usage - Create trail effect
const effect = new RenderTextureEffect(app);

const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
effect.getContainer().addChild(sprite);

// Display render texture with alpha
const outputSprite = effect.getSprite();
outputSprite.alpha = 0.9;  // Fade effect
app.stage.addChild(outputSprite);

// Move sprite with mouse
app.stage.eventMode = 'static';
app.stage.on('pointermove', (event) => {
    sprite.position.set(event.global.x, event.global.y);
});

// Render each frame
app.ticker.add(() => {
    effect.render();
});
```

### 2. Multi-Pass Shader Effects

Chain multiple shader passes:

```javascript
class MultiPassFilter {
    constructor(app) {
        this.app = app;
        this.passes = [];
        this.renderTextures = [];
    }

    addPass(filter) {
        this.passes.push(filter);

        // Create render texture for this pass
        const rt = PIXI.RenderTexture.create({
            width: this.app.screen.width,
            height: this.app.screen.height
        });
        this.renderTextures.push(rt);
    }

    render(source) {
        let currentSource = source;

        for (let i = 0; i < this.passes.length; i++) {
            const filter = this.passes[i];
            const target = this.renderTextures[i];

            // Apply filter
            currentSource.filters = [filter];

            // Render to texture
            this.app.renderer.render({
                container: currentSource,
                target,
                clear: true
            });

            // Use output as input for next pass
            const sprite = new PIXI.Sprite(target);
            currentSource = sprite;
        }

        return currentSource;
    }
}

// Usage - Blur then chromatic aberration
const multiPass = new MultiPassFilter(app);

const blurFilter = new PIXI.BlurFilter();
blurFilter.strength = 5;

const chromaFilter = new ChromaticAberrationFilter(10);

multiPass.addPass(blurFilter);
multiPass.addPass(chromaFilter);

const scene = new PIXI.Container();
const sprite = new PIXI.Sprite(texture);
sprite.position.set(400, 300);
scene.addChild(sprite);

const result = multiPass.render(scene);
app.stage.addChild(result);
```

### 3. WebWorker Integration

Offload heavy calculations to worker threads:

```javascript
// worker.js
self.onmessage = function(e) {
    const { type, data } = e.data;

    if (type === 'calculateParticles') {
        const { count, width, height } = data;
        const particles = [];

        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2
            });
        }

        self.postMessage({ type: 'particlesCalculated', particles });
    } else if (type === 'updateParticles') {
        const { particles, width, height, deltaTime } = data;

        particles.forEach(p => {
            p.x += p.vx * deltaTime;
            p.y += p.vy * deltaTime;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;
        });

        self.postMessage({ type: 'particlesUpdated', particles });
    }
};

// main.js
const worker = new Worker('worker.js');
const particles = [];
const sprites = [];

worker.onmessage = function(e) {
    const { type, particles: updatedParticles } = e.data;

    if (type === 'particlesCalculated') {
        // Create sprites for particles
        updatedParticles.forEach(p => {
            const sprite = new PIXI.Sprite(texture);
            sprite.position.set(p.x, p.y);
            app.stage.addChild(sprite);
            sprites.push(sprite);
        });

        particles.push(...updatedParticles);
    } else if (type === 'particlesUpdated') {
        // Update sprite positions
        updatedParticles.forEach((p, i) => {
            sprites[i].position.set(p.x, p.y);
        });

        particles.length = 0;
        particles.push(...updatedParticles);
    }
};

// Initial creation
worker.postMessage({
    type: 'calculateParticles',
    data: {
        count: 10000,
        width: 800,
        height: 600
    }
});

// Update loop
app.ticker.add((ticker) => {
    if (particles.length > 0) {
        worker.postMessage({
            type: 'updateParticles',
            data: {
                particles,
                width: 800,
                height: 600,
                deltaTime: ticker.deltaTime
            }
        });
    }
});
```

---

## Conclusion

These examples cover the most common PixiJS patterns and use cases for production applications:

- **Basic Applications**: Foundation for any PixiJS project
- **Interactive Elements**: User input and engagement
- **Particle Systems**: Visual effects and ambiance
- **Filters & Effects**: Visual polish and style
- **Custom Shaders**: Advanced visual customization
- **Animation**: Smooth motion and transitions
- **Performance**: Optimization for 60 FPS
- **Game Development**: Core gameplay mechanics
- **UI Components**: Professional user interfaces
- **Framework Integration**: React, Vue compatibility
- **Mobile Optimization**: Touch controls and adaptive settings
- **Advanced Techniques**: Render textures, multi-pass effects, WebWorkers

For more examples, visit:
- [PixiJS Examples](https://pixijs.com/examples)
- [PixiJS Playground](https://pixijs.io/playground)
- [GitHub PixiJS Demos](https://github.com/pixijs/pixijs/tree/dev/examples)
