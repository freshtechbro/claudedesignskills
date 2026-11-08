# PixiJS Filters & Visual Effects Guide

Comprehensive guide to using and creating visual effects with PixiJS filters and shaders.

---

## Table of Contents

1. [Filter Basics](#filter-basics)
2. [Built-in Filters](#built-in-filters)
3. [Custom Filters](#custom-filters)
4. [Shader Programming](#shader-programming)
5. [Effect Combinations](#effect-combinations)
6. [Performance Tips](#performance-tips)

---

## Filter Basics

### Applying Filters

Filters are WebGL/WebGPU shader programs applied to display objects after rendering.

```javascript
import { BlurFilter, Sprite } from 'pixi.js';

const sprite = Sprite.from('image.png');

// Single filter
sprite.filters = [new BlurFilter()];

// Multiple filters (applied in order)
sprite.filters = [
  new BlurFilter({ strength: 4 }),
  new ColorMatrixFilter()
];

// Remove filters
sprite.filters = null;
```

### Filter Area Optimization

```javascript
import { Rectangle } from 'pixi.js';

// Specify filter bounds for performance
sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);

// PixiJS won't need to measure bounds at runtime
```

### Filter on Containers

```javascript
import { Container } from 'pixi.js';

const container = new Container();
container.addChild(sprite1, sprite2, sprite3);

// Filter applied to entire container
container.filters = [new BlurFilter()];
```

---

## Built-in Filters

### BlurFilter

Gaussian blur effect for depth of field, motion blur, or soft focus.

```javascript
import { BlurFilter } from 'pixi.js';

const blur = new BlurFilter({
  strength: 8,      // Blur radius (default: 8)
  quality: 4,       // Number of passes (1-5, default: 4)
  kernelSize: 5     // Sample size: 5, 7, 9, 11, 13, 15 (default: 5)
});

sprite.filters = [blur];

// Adjust blur dynamically
app.ticker.add(() => {
  blur.blur = 5 + Math.sin(Date.now() * 0.001) * 5;  // Pulsing blur
});
```

**Use Cases**:
- Depth of field effects
- Focus/unfocus transitions
- Motion blur
- Background blur (foreground sharp)

**Performance**: Higher quality and kernelSize = slower. Use lower values for real-time effects.

---

### ColorMatrixFilter

Transform colors using matrix multiplication. Includes preset effects.

```javascript
import { ColorMatrixFilter } from 'pixi.js';

const colorMatrix = new ColorMatrixFilter();

// Grayscale
colorMatrix.greyscale(0.5);  // 0 = color, 1 = full grayscale

// Sepia tone
colorMatrix.sepia();

// Black and white
colorMatrix.blackAndWhite();

// Adjust contrast
colorMatrix.contrast(1.5);  // >1 = more contrast

// Adjust saturation
colorMatrix.saturate(0.5);  // <1 = desaturate, >1 = supersaturate

// Adjust brightness
colorMatrix.brightness(1.2);  // >1 = brighter

// Hue rotation
colorMatrix.hue(45);  // Rotate hue in degrees

// Negative (invert)
colorMatrix.negative();

// Vintage film effects
colorMatrix.kodachrome();
colorMatrix.technicolor();
colorMatrix.polaroid();
colorMatrix.vintage();

sprite.filters = [colorMatrix];
```

**Chaining Effects**:
```javascript
colorMatrix.greyscale(0.3).contrast(1.2).brightness(1.1);
```

**Custom Color Matrix**:
```javascript
// 5x4 color matrix [R, G, B, A, offset]
const matrix = [
  1, 0, 0, 0, 0,  // Red
  0, 1, 0, 0, 0,  // Green
  0, 0, 1, 0, 0,  // Blue
  0, 0, 0, 1, 0   // Alpha
];

colorMatrix.matrix = matrix;
```

**Use Cases**:
- Photo filters (Instagram-style)
- Color grading
- Night vision effect
- Damage/flash effects

---

### DisplacementFilter

Warp/distort pixels based on a displacement map texture.

```javascript
import { DisplacementFilter, Sprite } from 'pixi.js';

// Create displacement sprite (usually perlin noise or cloud texture)
const displacementSprite = Sprite.from('displacement.jpg');
displacementSprite.texture.baseTexture.wrapMode = WRAP_MODES.REPEAT;

const displacementFilter = new DisplacementFilter({
  sprite: displacementSprite,
  scale: 50  // Displacement amount
});

sprite.filters = [displacementFilter];
app.stage.addChild(displacementSprite);

// Animate displacement
app.ticker.add(() => {
  displacementSprite.x += 1;
  displacementSprite.y += 0.5;
});
```

**Parameters**:
- `sprite`: Displacement map (red channel = X offset, green channel = Y offset)
- `scale`: Displacement intensity (default: 20)

**Use Cases**:
- Water ripple effects
- Heat distortion
- Portal effects
- Liquid/jelly animations
- Flag waving

**Creating Displacement Maps**:
```javascript
// Generate noise texture
const canvas = document.createElement('canvas');
canvas.width = 256;
canvas.height = 256;
const ctx = canvas.getContext('2d');

// Draw perlin noise or clouds
// ... (use simplex-noise library or draw manually)

const displacementTexture = Texture.from(canvas);
const displacementSprite = new Sprite(displacementTexture);
```

---

### AlphaFilter

Flatten alpha across all children in a container.

```javascript
import { AlphaFilter, Container } from 'pixi.js';

const container = new Container();
container.addChild(sprite1, sprite2, sprite3);

const alphaFilter = new AlphaFilter(0.5);  // 50% opacity
container.filters = [alphaFilter];

// Without filter: each sprite has individual alpha
// With filter: entire container rendered at 50% alpha
```

**Use Cases**:
- Fade entire UI panel
- Composite transparency
- Layer blending

---

### NoiseFilter

Add random grain/noise for film grain or static effects.

```javascript
import { NoiseFilter } from 'pixi.js';

const noise = new NoiseFilter({
  noise: 0.5,  // Amount (0-1, default: 0.5)
  seed: Math.random()  // Random seed
});

sprite.filters = [noise];

// Animated noise
app.ticker.add(() => {
  noise.seed = Math.random();
});
```

**Use Cases**:
- Film grain
- Old TV static
- Analog distortion
- Glitch effects

---

### FXAAFilter

Fast approximate anti-aliasing for smooth edges.

```javascript
import { FXAAFilter } from 'pixi.js';

const fxaa = new FXAAFilter();
sprite.filters = [fxaa];
```

**Use Cases**:
- Smooth jagged edges
- Improve visual quality on low-res displays
- Reduce aliasing artifacts

---

## Custom Filters

### Creating a Custom Filter

Custom filters use GLSL shaders for GPU-accelerated effects.

```javascript
import { Filter, GlProgram } from 'pixi.js';

const vertex = `
  in vec2 aPosition;
  out vec2 vTextureCoord;

  uniform vec4 uInputSize;
  uniform vec4 uOutputFrame;
  uniform vec4 uOutputTexture;

  vec4 filterVertexPosition() {
    vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
    position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
    position.y = position.y * (2.0*uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;
    return vec4(position, 0.0, 1.0);
  }

  vec2 filterTextureCoord() {
    return aPosition * (uOutputFrame.zw * uInputSize.zw);
  }

  void main() {
    gl_Position = filterVertexPosition();
    vTextureCoord = filterTextureCoord();
  }
`;

const fragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform float uTime;

  void main() {
    vec2 uv = vTextureCoord;

    // Wave distortion
    float wave = sin(uv.y * 10.0 + uTime) * 0.05;
    vec4 color = texture(uTexture, vec2(uv.x + wave, uv.y));

    gl_FragColor = color;
  }
`;

const waveFilter = new Filter({
  glProgram: new GlProgram({ vertex, fragment }),
  resources: {
    timeUniforms: {
      uTime: { value: 0.0, type: 'f32' }
    }
  }
});

sprite.filters = [waveFilter];

// Update uniform
app.ticker.add((ticker) => {
  waveFilter.resources.timeUniforms.uniforms.uTime += 0.04 * ticker.deltaTime;
});
```

---

### Example: Pixelate Filter

```javascript
const pixelateVertex = `
  in vec2 aPosition;
  out vec2 vTextureCoord;

  uniform vec4 uInputSize;
  uniform vec4 uOutputFrame;
  uniform vec4 uOutputTexture;

  vec4 filterVertexPosition() {
    vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
    position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
    position.y = position.y * (2.0*uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;
    return vec4(position, 0.0, 1.0);
  }

  vec2 filterTextureCoord() {
    return aPosition * (uOutputFrame.zw * uInputSize.zw);
  }

  void main() {
    gl_Position = filterVertexPosition();
    vTextureCoord = filterTextureCoord();
  }
`;

const pixelateFragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform vec2 uSize;
  uniform float uPixelSize;

  void main() {
    vec2 coord = vTextureCoord * uSize;
    vec2 pixelCoord = floor(coord / uPixelSize) * uPixelSize;
    vec2 pixelUV = pixelCoord / uSize;

    gl_FragColor = texture(uTexture, pixelUV);
  }
`;

class PixelateFilter extends Filter {
  constructor(pixelSize = 10) {
    super({
      glProgram: new GlProgram({
        vertex: pixelateVertex,
        fragment: pixelateFragment
      }),
      resources: {
        pixelateUniforms: {
          uSize: { value: new Float32Array([800, 600]), type: 'vec2<f32>' },
          uPixelSize: { value: pixelSize, type: 'f32' }
        }
      }
    });
  }

  get pixelSize() {
    return this.resources.pixelateUniforms.uniforms.uPixelSize;
  }

  set pixelSize(value) {
    this.resources.pixelateUniforms.uniforms.uPixelSize = value;
  }
}

// Usage
const pixelate = new PixelateFilter(5);
sprite.filters = [pixelate];

// Animate
app.ticker.add(() => {
  pixelate.pixelSize = 5 + Math.sin(Date.now() * 0.001) * 4;
});
```

---

### Example: Chromatic Aberration

```javascript
const chromaticFragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform float uAmount;

  void main() {
    vec2 uv = vTextureCoord;

    // Offset RGB channels
    float r = texture(uTexture, uv + vec2(uAmount, 0.0)).r;
    float g = texture(uTexture, uv).g;
    float b = texture(uTexture, uv - vec2(uAmount, 0.0)).b;

    gl_FragColor = vec4(r, g, b, 1.0);
  }
`;

class ChromaticAberrationFilter extends Filter {
  constructor(amount = 0.005) {
    super({
      glProgram: new GlProgram({
        vertex: defaultVertex,  // Use default vertex shader
        fragment: chromaticFragment
      }),
      resources: {
        chromaticUniforms: {
          uAmount: { value: amount, type: 'f32' }
        }
      }
    });
  }

  get amount() {
    return this.resources.chromaticUniforms.uniforms.uAmount;
  }

  set amount(value) {
    this.resources.chromaticUniforms.uniforms.uAmount = value;
  }
}

// Usage
const chromatic = new ChromaticAberrationFilter(0.01);
sprite.filters = [chromatic];
```

---

### Example: Vignette Filter

```javascript
const vignetteFragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform float uIntensity;
  uniform float uSoftness;

  void main() {
    vec4 color = texture(uTexture, vTextureCoord);
    vec2 uv = vTextureCoord - 0.5;
    float dist = length(uv);
    float vignette = smoothstep(uIntensity, uIntensity - uSoftness, dist);

    gl_FragColor = vec4(color.rgb * vignette, color.a);
  }
`;

class VignetteFilter extends Filter {
  constructor(intensity = 0.5, softness = 0.3) {
    super({
      glProgram: new GlProgram({
        vertex: defaultVertex,
        fragment: vignetteFragment
      }),
      resources: {
        vignetteUniforms: {
          uIntensity: { value: intensity, type: 'f32' },
          uSoftness: { value: softness, type: 'f32' }
        }
      }
    });
  }

  get intensity() {
    return this.resources.vignetteUniforms.uniforms.uIntensity;
  }

  set intensity(value) {
    this.resources.vignetteUniforms.uniforms.uIntensity = value;
  }

  get softness() {
    return this.resources.vignetteUniforms.uniforms.uSoftness;
  }

  set softness(value) {
    this.resources.vignetteUniforms.uniforms.uSoftness = value;
  }
}
```

---

## Shader Programming

### GLSL Basics

**Data Types**:
```glsl
float x = 1.0;
vec2 position = vec2(0.5, 0.5);
vec3 color = vec3(1.0, 0.0, 0.0);  // RGB
vec4 rgba = vec4(1.0, 0.0, 0.0, 1.0);  // RGBA

sampler2D texture;  // Texture sampler
```

**Built-in Functions**:
```glsl
// Math
sin(x), cos(x), tan(x)
abs(x), sign(x)
floor(x), ceil(x), fract(x)
min(a, b), max(a, b), clamp(x, min, max)
mix(a, b, t)  // Linear interpolation
smoothstep(edge0, edge1, x)  // Smooth interpolation

// Vector
length(v)  // Vector length
distance(a, b)  // Distance between vectors
dot(a, b)  // Dot product
normalize(v)  // Unit vector

// Texture sampling
texture(sampler, uv)  // Sample texture at UV coordinates
```

**Vertex Shader Template**:
```glsl
in vec2 aPosition;
out vec2 vTextureCoord;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform vec4 uOutputTexture;

void main() {
  gl_Position = filterVertexPosition();
  vTextureCoord = filterTextureCoord();
}
```

**Fragment Shader Template**:
```glsl
in vec2 vTextureCoord;
uniform sampler2D uTexture;

void main() {
  vec4 color = texture(uTexture, vTextureCoord);

  // Modify color
  color.rgb *= 0.5;  // Darken

  gl_FragColor = color;
}
```

---

### Uniforms

Pass data from JavaScript to shaders.

```javascript
const filter = new Filter({
  glProgram: new GlProgram({ vertex, fragment }),
  resources: {
    customUniforms: {
      uTime: { value: 0.0, type: 'f32' },
      uColor: { value: [1.0, 0.0, 0.0], type: 'vec3<f32>' },
      uPosition: { value: new Float32Array([0.5, 0.5]), type: 'vec2<f32>' },
      uTexture2: { value: secondTexture, type: 'sampler2D' }
    }
  }
});

// Access uniforms
filter.resources.customUniforms.uniforms.uTime = 5.0;
filter.resources.customUniforms.uniforms.uColor = [0.0, 1.0, 0.0];
```

**In Shader**:
```glsl
uniform float uTime;
uniform vec3 uColor;
uniform vec2 uPosition;
uniform sampler2D uTexture2;

void main() {
  // Use uniforms
  float wave = sin(vTextureCoord.y * 10.0 + uTime);
  vec4 color = texture(uTexture, vTextureCoord) * vec4(uColor, 1.0);
  gl_FragColor = color;
}
```

---

### Multi-Pass Filters

Apply multiple shader passes for complex effects.

```javascript
class MultiPassFilter extends Filter {
  constructor() {
    // First pass: Blur horizontal
    const pass1 = new Filter({
      glProgram: new GlProgram({ vertex: defaultVertex, fragment: blurHorizontalFragment })
    });

    // Second pass: Blur vertical
    const pass2 = new Filter({
      glProgram: new GlProgram({ vertex: defaultVertex, fragment: blurVerticalFragment })
    });

    // Combine passes
    super({
      glProgram: new GlProgram({ vertex: defaultVertex, fragment: combineFragment }),
      resources: {
        pass1Texture: { value: null, type: 'sampler2D' },
        pass2Texture: { value: null, type: 'sampler2D' }
      }
    });
  }
}
```

---

## Effect Combinations

### Glow Effect

Blur + Additive Blend

```javascript
import { BlurFilter, BLEND_MODES } from 'pixi.js';

// Original sprite
const sprite = Sprite.from('star.png');

// Glow sprite (blurred copy)
const glowSprite = new Sprite(sprite.texture);
glowSprite.filters = [new BlurFilter({ strength: 15 })];
glowSprite.blendMode = BLEND_MODES.ADD;
glowSprite.alpha = 0.8;

const container = new Container();
container.addChild(glowSprite, sprite);  // Glow behind

app.stage.addChild(container);
```

---

### Outline Effect

Multiple displacement passes

```javascript
const outlineFragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform float uThickness;
  uniform vec3 uColor;

  void main() {
    vec4 color = texture(uTexture, vTextureCoord);
    float alpha = color.a;

    // Sample neighboring pixels
    alpha += texture(uTexture, vTextureCoord + vec2(uThickness, 0.0)).a;
    alpha += texture(uTexture, vTextureCoord - vec2(uThickness, 0.0)).a;
    alpha += texture(uTexture, vTextureCoord + vec2(0.0, uThickness)).a;
    alpha += texture(uTexture, vTextureCoord - vec2(0.0, uThickness)).a;

    // Create outline
    float outline = step(0.1, alpha) * (1.0 - color.a);

    vec3 finalColor = mix(color.rgb, uColor, outline);
    float finalAlpha = max(color.a, outline);

    gl_FragColor = vec4(finalColor, finalAlpha);
  }
`;

class OutlineFilter extends Filter {
  constructor(thickness = 0.01, color = [1, 1, 1]) {
    super({
      glProgram: new GlProgram({ vertex: defaultVertex, fragment: outlineFragment }),
      resources: {
        outlineUniforms: {
          uThickness: { value: thickness, type: 'f32' },
          uColor: { value: color, type: 'vec3<f32>' }
        }
      }
    });
  }
}
```

---

### CRT Monitor Effect

Scanlines + chromatic aberration + curve

```javascript
const crtFragment = `
  in vec2 vTextureCoord;
  uniform sampler2D uTexture;
  uniform float uTime;

  void main() {
    vec2 uv = vTextureCoord;

    // Curve screen
    uv = uv * 2.0 - 1.0;
    uv *= 1.0 + 0.1 * dot(uv, uv);
    uv = (uv + 1.0) * 0.5;

    // Chromatic aberration
    float r = texture(uTexture, uv + vec2(0.002, 0.0)).r;
    float g = texture(uTexture, uv).g;
    float b = texture(uTexture, uv - vec2(0.002, 0.0)).b;

    // Scanlines
    float scanline = sin(uv.y * 800.0) * 0.1 + 0.9;

    // Flicker
    float flicker = sin(uTime * 50.0) * 0.02 + 0.98;

    vec3 color = vec3(r, g, b) * scanline * flicker;

    gl_FragColor = vec4(color, 1.0);
  }
`;
```

---

### Film Grain + Vignette

```javascript
sprite.filters = [
  new NoiseFilter({ noise: 0.2 }),
  new VignetteFilter(0.5, 0.3),
  new ColorMatrixFilter().sepia()
];
```

---

## Performance Tips

### 1. Minimize Filter Count

```javascript
// ❌ BAD: Too many filters
sprite.filters = [blur1, blur2, colorMatrix, noise, vignette];

// ✅ GOOD: Combine into single custom filter
sprite.filters = [combinedFilter];
```

---

### 2. Set Filter Area

```javascript
sprite.filters = [blurFilter];
sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);
```

---

### 3. Bake Static Filters

```javascript
// Apply filter once, generate texture
const filteredTexture = renderer.filters.generateFilteredTexture({
  texture: originalTexture,
  filters: [blurFilter, colorMatrix]
});

const sprite = new Sprite(filteredTexture);
// No runtime filter cost
```

---

### 4. Use Lower Quality

```javascript
const blur = new BlurFilter({
  strength: 8,
  quality: 2,  // Lower = faster (1-5)
  kernelSize: 5  // Smaller = faster
});
```

---

### 5. Toggle Filters Based on Performance

```javascript
let filtersEnabled = true;

app.ticker.add(() => {
  const fps = Math.round(1000 / app.ticker.deltaMS);

  if (fps < 30 && filtersEnabled) {
    sprite.filters = null;  // Disable filters
    filtersEnabled = false;
  } else if (fps > 55 && !filtersEnabled) {
    sprite.filters = [blurFilter];  // Re-enable
    filtersEnabled = true;
  }
});
```

---

## Filter Examples Library

### Glass/Frosted Effect
```javascript
sprite.filters = [
  new BlurFilter({ strength: 10 }),
  new ColorMatrixFilter().brightness(1.2)
];
sprite.alpha = 0.8;
```

### Night Vision
```javascript
const nightVision = new ColorMatrixFilter();
nightVision.greyscale(1);
nightVision.contrast(1.5);
nightVision.brightness(1.5);
sprite.filters = [nightVision];
sprite.tint = 0x00ff00;  // Green tint
```

### X-Ray
```javascript
const xray = new ColorMatrixFilter();
xray.negative();
xray.contrast(2);
sprite.filters = [xray];
```

### Underwater
```javascript
sprite.filters = [
  new DisplacementFilter({ sprite: waveSprite, scale: 20 }),
  new ColorMatrixFilter().saturate(0.7)
];
sprite.tint = 0x88ccff;
```

---

This guide provides comprehensive coverage of PixiJS filters, from built-in options to custom shader programming for advanced visual effects.
