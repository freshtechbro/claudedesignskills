# PixiJS Starter Template

A modern, production-ready PixiJS starter template with interactive sprites, real-time performance monitoring, and responsive UI controls.

## Features

- **High-Performance Rendering**: Uses PixiJS v8+ with WebGL/WebGPU
- **Interactive Sprites**: Click to change colors, drag and interact
- **Physics Simulation**: Bouncing sprites with velocity and collision detection
- **Performance Monitoring**: Real-time FPS, sprite count, and draw call tracking
- **Responsive Design**: Mobile-friendly UI with glassmorphism effects
- **Modern UI**: Clean, professional interface with gradient accents
- **Easy Customization**: Well-structured code for quick modifications

## Quick Start

### 1. Local Development

Simply open `index.html` in a modern web browser:

```bash
# Using Python's built-in server (recommended)
python3 -m http.server 8000

# Or using Node.js http-server
npx http-server -p 8000

# Then open http://localhost:8000
```

### 2. Live Server (VS Code)

If using VS Code with the Live Server extension:

1. Right-click on `index.html`
2. Select "Open with Live Server"

### 3. Production Deployment

For production, serve the files through any static hosting:

- **Vercel**: `vercel --prod`
- **Netlify**: Drag and drop the folder
- **GitHub Pages**: Push to repository and enable Pages
- **AWS S3**: Upload as static website

## Project Structure

```
starter_pixijs/
├── index.html          # Main HTML structure
├── styles.css          # Responsive styling with glassmorphism
├── main.js             # PixiJS application logic
└── README.md           # This file
```

## Usage

### Controls

- **Toggle Stats**: Show/hide performance statistics panel
- **Add Sprites**: Add 20 random sprites to the canvas
- **Clear**: Remove all sprites from the canvas

### Interactions

- **Click Sprites**: Change sprite color randomly
- **Watch Physics**: Sprites bounce off edges automatically

## Customization

### Change Background Color

In `main.js` line 10:

```javascript
await app.init({
    backgroundColor: 0x1a1a2e,  // Change this hex color
    // ...
});
```

### Modify Sprite Colors

In `main.js` lines 35-40, edit the color palette:

```javascript
const textures = [
    createSpriteTexture(0xe74c3c),  // Red
    createSpriteTexture(0x3498db),  // Blue
    createSpriteTexture(0x2ecc71),  // Green
    createSpriteTexture(0xf39c12),  // Orange
    createSpriteTexture(0x9b59b6)   // Purple
];
```

### Adjust Sprite Size

In `main.js` line 31, change the circle radius:

```javascript
graphics.circle(25, 25, 25).fill(color);  // Last parameter is radius
```

### Change Initial Sprite Count

In `main.js` line 140:

```javascript
addSprites(50);  // Change from 50 to your desired count
```

### Modify Physics Behavior

In `main.js` lines 57-58, adjust velocity ranges:

```javascript
sprite.vx = (Math.random() - 0.5) * 2;  // Horizontal speed
sprite.vy = (Math.random() - 0.5) * 2;  // Vertical speed
```

### Disable Rotation

In `main.js`, comment out or remove line 124:

```javascript
// sprite.rotation += 0.01 * ticker.deltaTime;
```

## Advanced Customization

### Add Sprite Textures from Images

Replace the procedural graphics with image textures:

```javascript
// Load texture from image
const texture = await PIXI.Assets.load('path/to/sprite.png');

// Create sprite
const sprite = new PIXI.Sprite(texture);
```

### Add Filters and Effects

Apply blur, glow, or other effects:

```javascript
import { BlurFilter } from 'pixi.js';

const blurFilter = new BlurFilter();
blurFilter.strength = 8;

sprite.filters = [blurFilter];
```

### Implement Sprite Pooling

For better performance with many sprites:

```javascript
class SpritePool {
    constructor(texture, size = 100) {
        this.available = [];
        this.active = [];

        for (let i = 0; i < size; i++) {
            const sprite = new PIXI.Sprite(texture);
            sprite.visible = false;
            this.available.push(sprite);
        }
    }

    spawn(x, y) {
        let sprite = this.available.pop();
        if (!sprite) {
            sprite = new PIXI.Sprite(this.texture);
        }

        sprite.position.set(x, y);
        sprite.visible = true;
        this.active.push(sprite);
        return sprite;
    }

    despawn(sprite) {
        sprite.visible = false;
        const index = this.active.indexOf(sprite);
        if (index > -1) {
            this.active.splice(index, 1);
            this.available.push(sprite);
        }
    }
}

const pool = new SpritePool(texture);
const sprite = pool.spawn(100, 100);
// Later: pool.despawn(sprite);
```

### Add Particle Effects

Use ParticleContainer for thousands of sprites:

```javascript
const particles = new PIXI.ParticleContainer(10000, {
    position: true,
    rotation: true,
    scale: true,
    tint: true
});

for (let i = 0; i < 10000; i++) {
    const particle = new PIXI.Sprite(texture);
    particle.x = Math.random() * app.screen.width;
    particle.y = Math.random() * app.screen.height;
    particles.addChild(particle);
}

app.stage.addChild(particles);
```

### Add Custom Shaders

Create custom visual effects with GLSL:

```javascript
import { Filter, GlProgram } from 'pixi.js';

const fragment = `
    in vec2 vTextureCoord;
    uniform sampler2D uTexture;
    uniform float uTime;

    void main() {
        vec2 coord = vTextureCoord;
        coord.x += sin(coord.y * 10.0 + uTime) * 0.01;
        gl_FragColor = texture(uTexture, coord);
    }
`;

const waveFilter = new Filter({
    glProgram: new GlProgram({ fragment }),
    resources: {
        waveUniforms: {
            uTime: { value: 0, type: 'f32' }
        }
    }
});

// Update in ticker
app.ticker.add(() => {
    waveFilter.resources.waveUniforms.uniforms.uTime += 0.1;
});

sprite.filters = [waveFilter];
```

## Performance Tips

### For Desktop (High-End)

- Increase sprite count for stress testing
- Enable antialiasing for smoother edges
- Use higher resolution textures
- Add complex filters and effects

```javascript
await app.init({
    antialias: true,
    resolution: 2,  // Higher resolution
    // ...
});

addSprites(500);  // More sprites
```

### For Mobile (Low-End)

- Reduce sprite count
- Disable antialiasing
- Use lower resolution
- Avoid heavy filters

```javascript
await app.init({
    antialias: false,
    resolution: 1,
    // ...
});

addSprites(50);  // Fewer sprites
```

### General Optimization

1. **Use ParticleContainer** for static sprites (10x faster)
2. **Enable cacheAsBitmap** for complex static graphics
3. **Minimize draw calls** with texture atlases
4. **Cull off-screen objects** for large scenes
5. **Pool objects** to avoid garbage collection
6. **Limit filters** to specific areas with `filterArea`

## Troubleshooting

### Issue: Black screen or no rendering

**Solution**: Check browser console for errors. Ensure:
- PixiJS CDN is loading correctly
- No JavaScript errors in console
- Browser supports WebGL (check `https://get.webgl.org/`)

### Issue: Low FPS on mobile

**Solution**: Reduce sprite count and disable antialiasing:

```javascript
await app.init({
    antialias: false,
    resolution: 1
});

addSprites(25);  // Fewer sprites
```

### Issue: Sprites disappearing at edges

**Solution**: Ensure sprites are kept within bounds (lines 120-121 in main.js handle this)

### Issue: Memory leaks over time

**Solution**: Properly destroy sprites when clearing:

```javascript
function clearSprites() {
    sprites.forEach(sprite => {
        sprite.destroy({ texture: false });  // Keep texture
    });
    sprites.length = 0;
    spriteContainer.removeChildren();
}
```

## Browser Support

- **Chrome/Edge**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support (iOS 15+)
- **Mobile browsers**: Supported with reduced features

Requires WebGL support. Check compatibility at [caniuse.com/webgl](https://caniuse.com/webgl).

## Next Steps

### Learning Resources

- [PixiJS Official Documentation](https://pixijs.com/docs)
- [PixiJS Examples](https://pixijs.com/examples)
- [PixiJS Playground](https://pixijs.io/playground)
- [WebGL Fundamentals](https://webglfundamentals.org/)

### Extend the Template

1. **Add Sprite Sheet Animations**: Use `AnimatedSprite` for frame-based animation
2. **Implement Collision Detection**: Check sprite overlaps and interactions
3. **Add Sound Effects**: Integrate Howler.js or Web Audio API
4. **Create Game Logic**: Add scoring, levels, or gameplay mechanics
5. **Integrate with React**: Use `@pixi/react` for component-based approach

### Example Extensions

**Collision Detection**:
```javascript
function checkCollision(sprite1, sprite2) {
    const bounds1 = sprite1.getBounds();
    const bounds2 = sprite2.getBounds();

    return bounds1.x < bounds2.x + bounds2.width &&
           bounds1.x + bounds1.width > bounds2.x &&
           bounds1.y < bounds2.y + bounds2.height &&
           bounds1.y + bounds1.height > bounds2.y;
}

app.ticker.add(() => {
    for (let i = 0; i < sprites.length; i++) {
        for (let j = i + 1; j < sprites.length; j++) {
            if (checkCollision(sprites[i], sprites[j])) {
                // Handle collision
            }
        }
    }
});
```

**Sprite Sheet Animation**:
```javascript
// Load sprite sheet
const sheet = await PIXI.Assets.load('spritesheet.json');

// Create animated sprite
const animatedSprite = new PIXI.AnimatedSprite(sheet.animations['run']);
animatedSprite.animationSpeed = 0.1;
animatedSprite.play();

app.stage.addChild(animatedSprite);
```

**React Integration**:
```javascript
import { Stage, Container, Sprite } from '@pixi/react';

function App() {
    return (
        <Stage width={800} height={600}>
            <Container>
                <Sprite texture={texture} x={100} y={100} />
            </Container>
        </Stage>
    );
}
```

## Deployment

### Static Hosting

**Vercel**:
```bash
npm install -g vercel
vercel --prod
```

**Netlify**:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir .
```

**GitHub Pages**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main

# Enable Pages in repository settings
```

### CDN Considerations

The template uses PixiJS from CDN:
```html
<script src="https://pixijs.download/release/pixi.js"></script>
```

For production, consider:
1. **Self-hosting** for better caching and control
2. **npm installation** for bundled builds
3. **Specific version** to avoid breaking changes

**npm approach**:
```bash
npm install pixi.js
```

```javascript
// main.js
import * as PIXI from 'pixi.js';

// Use bundler like Vite or Webpack
```

## License

This starter template is provided as-is for learning and development purposes.

PixiJS is MIT licensed. See [PixiJS GitHub](https://github.com/pixijs/pixijs) for details.

## Support

For PixiJS questions:
- [PixiJS Discord](https://discord.gg/CPTjeb28nH)
- [PixiJS GitHub Discussions](https://github.com/pixijs/pixijs/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/pixi.js)

---

**Happy Coding!** 🎨✨
