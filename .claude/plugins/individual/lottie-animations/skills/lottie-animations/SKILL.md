---
name: lottie-animations
description: After Effects animation rendering for web and React applications. Use this skill when implementing Lottie animations, JSON vector animations, interactive animated icons, micro-interactions, or loading animations. Triggers on tasks involving Lottie, lottie-web, lottie-react, dotLottie, After Effects JSON export, bodymovin, animated SVG alternatives, or designer-created animations. Complements GSAP ScrollTrigger and Framer Motion for scroll-driven and interactive animations.
---

# Lottie Animations

## Overview

Lottie is a library for rendering After Effects animations in real-time on web, iOS, Android, and React Native. Created by Airbnb, it allows designers to ship animations as easily as shipping static assets. Animations are exported from After Effects as JSON files using the Bodymovin plugin, then rendered natively with minimal performance overhead.

**When to use Lottie:**
- Designer-created animations that need pixel-perfect fidelity
- Complex animated icons and micro-interactions
- Loading animations and progress indicators
- Onboarding sequences and tutorial animations
- Marketing animations and promotional content
- Alternative to GIF/video with smaller file sizes and scalability

**Key advantages:**
- Vector-based (scalable without quality loss)
- Significantly smaller file sizes than GIF or video
- Editable at runtime (colors, speed, segments)
- Full designer control via After Effects
- Cross-platform rendering consistency
- Interactive controls (play, pause, seek, loop)

## Core Concepts

### Lottie Format Types

**1. JSON Lottie (.json)**
- Original Lottie format
- Exported from After Effects via Bodymovin plugin
- Human-readable JSON structure
- Larger file sizes (not compressed)
- Widely supported across all platforms

**2. dotLottie (.lottie)**
- Modern compressed format
- ZIP archive containing JSON + assets
- Supports multiple animations and themes in one file
- Smaller file sizes (up to 90% reduction)
- Recommended for production use

### Library Options

**lottie-web** (original library):
```javascript
import lottie from 'lottie-web';

lottie.loadAnimation({
  container: document.getElementById('lottie-container'),
  renderer: 'svg', // or 'canvas', 'html'
  loop: true,
  autoplay: true,
  path: 'animation.json' // or animationData: jsonData
});
```

**@lottiefiles/dotlottie-web** (modern, recommended):
```javascript
import { DotLottie } from '@lottiefiles/dotlottie-web';

new DotLottie({
  canvas: document.getElementById('canvas'),
  src: 'animation.lottie',
  autoplay: true,
  loop: true
});
```

**@lottiefiles/dotlottie-react** (React integration):
```jsx
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

<DotLottieReact
  src="animation.lottie"
  loop
  autoplay
  style={{ height: 300 }}
/>
```

**lottie-react** (alternative React wrapper):
```jsx
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie animationData={animationData} loop={true} />
```

### Animation Data Sources

**1. LottieFiles** (lottie.host)
- 100,000+ free animations
- Direct URL embedding
- CDN hosting

**2. Local JSON/dotLottie files**
- Bundled with application
- Better performance (no network request)
- Version control friendly

**3. After Effects export**
- Custom designer animations
- Bodymovin plugin required
- Export settings critical for file size

## Common Patterns

### 1. Basic HTML Integration with dotLottie-web

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    #canvas {
      width: 400px;
      height: 400px;
    }
  </style>
</head>
<body>
  <canvas id="canvas"></canvas>

  <script type="module">
    import { DotLottie } from 'https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm';

    new DotLottie({
      canvas: document.getElementById('canvas'),
      src: 'https://lottie.host/4db68bbd-31f6-4cd8-84eb-189de081159a/IGmMCqhzpt.lottie',
      autoplay: true,
      loop: true
    });
  </script>
</body>
</html>
```

### 2. React Component with Controls

```jsx
import React from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const AnimatedButton = () => {
  const [dotLottie, setDotLottie] = React.useState(null);

  const handlePlay = () => dotLottie?.play();
  const handlePause = () => dotLottie?.pause();
  const handleStop = () => dotLottie?.stop();
  const handleSeek = (frame) => dotLottie?.setFrame(frame);

  return (
    <div>
      <DotLottieReact
        src="button-animation.lottie"
        loop
        autoplay={false}
        dotLottieRefCallback={setDotLottie}
        style={{ height: 200 }}
      />

      <div>
        <button onClick={handlePlay}>Play</button>
        <button onClick={handlePause}>Pause</button>
        <button onClick={handleStop}>Stop</button>
        <button onClick={() => handleSeek(30)}>Seek to frame 30</button>
      </div>
    </div>
  );
};
```

### 3. Event Listeners and Lifecycle Hooks

```jsx
import React, { useEffect } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const EventDrivenAnimation = () => {
  const [dotLottie, setDotLottie] = React.useState(null);

  useEffect(() => {
    if (!dotLottie) return;

    const onLoad = () => console.log('Animation loaded');
    const onPlay = () => console.log('Animation started');
    const onPause = () => console.log('Animation paused');
    const onComplete = () => console.log('Animation completed');
    const onFrame = ({ currentFrame }) => console.log('Frame:', currentFrame);

    dotLottie.addEventListener('load', onLoad);
    dotLottie.addEventListener('play', onPlay);
    dotLottie.addEventListener('pause', onPause);
    dotLottie.addEventListener('complete', onComplete);
    dotLottie.addEventListener('frame', onFrame);

    return () => {
      dotLottie.removeEventListener('load', onLoad);
      dotLottie.removeEventListener('play', onPlay);
      dotLottie.removeEventListener('pause', onPause);
      dotLottie.removeEventListener('complete', onComplete);
      dotLottie.removeEventListener('frame', onFrame);
    };
  }, [dotLottie]);

  return (
    <DotLottieReact
      src="animation.lottie"
      loop
      autoplay
      dotLottieRefCallback={setDotLottie}
    />
  );
};
```

### 4. Scroll-Driven Animation with lottie-react

```jsx
import Lottie from 'lottie-react';
import robotAnimation from './robot.json';

const ScrollAnimation = () => {
  const interactivity = {
    mode: 'scroll',
    actions: [
      {
        visibility: [0, 0.2],
        type: 'stop',
        frames: [0]
      },
      {
        visibility: [0.2, 0.45],
        type: 'seek',
        frames: [0, 45]
      },
      {
        visibility: [0.45, 1.0],
        type: 'loop',
        frames: [45, 60]
      }
    ]
  };

  return (
    <Lottie
      animationData={robotAnimation}
      style={{ height: 300 }}
      interactivity={interactivity}
    />
  );
};
```

### 5. Hover-Triggered Segment Playback

```jsx
import { useLottie, useLottieInteractivity } from 'lottie-react';
import likeButton from './like-button.json';

const HoverAnimation = () => {
  const lottieObj = useLottie({
    animationData: likeButton
  });

  const Animation = useLottieInteractivity({
    lottieObj,
    mode: 'cursor',
    actions: [
      {
        position: { x: [0, 1], y: [0, 1] },
        type: 'loop',
        frames: [45, 60]
      },
      {
        position: { x: -1, y: -1 },
        type: 'stop',
        frames: [45]
      }
    ]
  });

  return <div style={{ height: 300, border: '2px solid black' }}>{Animation}</div>;
};
```

### 6. Multi-Animation and Theme Support

```jsx
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import React, { useState, useEffect } from 'react';

const ThemedAnimation = () => {
  const [dotLottie, setDotLottie] = useState(null);
  const [animations, setAnimations] = useState([]);
  const [themes, setThemes] = useState([]);
  const [currentAnimationId, setCurrentAnimationId] = useState('');
  const [currentThemeId, setCurrentThemeId] = useState('');

  useEffect(() => {
    if (!dotLottie) return;

    const onLoad = () => {
      setAnimations(dotLottie.manifest.animations || []);
      setThemes(dotLottie.manifest.themes || []);
      setCurrentAnimationId(dotLottie.activeAnimationId);
      setCurrentThemeId(dotLottie.activeThemeId);
    };

    dotLottie.addEventListener('load', onLoad);
    return () => dotLottie.removeEventListener('load', onLoad);
  }, [dotLottie]);

  return (
    <div>
      <DotLottieReact
        src="multi-animation.lottie"
        dotLottieRefCallback={setDotLottie}
        animationId={currentAnimationId}
        themeId={currentThemeId}
      />

      {themes.length > 0 && (
        <select value={currentThemeId} onChange={(e) => setCurrentThemeId(e.target.value)}>
          {themes.map((theme) => (
            <option key={theme.id} value={theme.id}>{theme.id}</option>
          ))}
        </select>
      )}

      {animations.length > 0 && (
        <select value={currentAnimationId} onChange={(e) => setCurrentAnimationId(e.target.value)}>
          {animations.map((anim) => (
            <option key={anim.id} value={anim.id}>{anim.id}</option>
          ))}
        </select>
      )}
    </div>
  );
};
```

### 7. Web Worker for Performance (DotLottieWorker)

```javascript
import { DotLottieWorker } from '@lottiefiles/dotlottie-web';

// Offload animation rendering to a web worker
new DotLottieWorker({
  canvas: document.getElementById('canvas'),
  src: 'heavy-animation.lottie',
  autoplay: true,
  loop: true,
  workerId: 'worker-1' // Group multiple animations by worker
});

// Multiple animations in separate workers
new DotLottieWorker({
  canvas: document.getElementById('canvas-2'),
  src: 'animation-2.lottie',
  autoplay: true,
  loop: true,
  workerId: 'worker-2'
});
```

## Integration Patterns

### With GSAP ScrollTrigger

```jsx
import Lottie from 'lottie-react';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
import animationData from './animation.json';

gsap.registerPlugin(ScrollTrigger);

const GSAPLottieIntegration = () => {
  const lottieRef = React.useRef();

  React.useEffect(() => {
    const anim = lottieRef.current;
    if (!anim) return;

    // Sync Lottie with scroll
    gsap.to(anim, {
      scrollTrigger: {
        trigger: '#animation-section',
        start: 'top center',
        end: 'bottom center',
        scrub: 1,
        onUpdate: (self) => {
          const frame = Math.floor(self.progress * (anim.totalFrames - 1));
          anim.goToAndStop(frame, true);
        }
      }
    });
  }, []);

  return (
    <div id="animation-section" style={{ height: '200vh' }}>
      <Lottie
        lottieRef={lottieRef}
        animationData={animationData}
        autoplay={false}
        loop={false}
      />
    </div>
  );
};
```

### With Framer Motion

```jsx
import { motion } from 'framer-motion';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const MotionLottie = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6 }}
    >
      <DotLottieReact
        src="animation.lottie"
        loop
        autoplay
        style={{ height: 400 }}
      />
    </motion.div>
  );
};
```

### Vue 3 Integration

```vue
<script setup>
import { DotLottieVue } from '@lottiefiles/dotlottie-vue';
</script>

<template>
  <DotLottieVue
    style="height: 500px; width: 500px"
    autoplay
    loop
    src="https://path-to-animation.lottie"
  />
</template>
```

### Svelte Integration

```svelte
<script lang="ts">
  import { DotLottieSvelte } from '@lottiefiles/dotlottie-svelte';
  import type { DotLottie } from '@lottiefiles/dotlottie-svelte';

  let dotLottie: DotLottie | null = null;

  function play() {
    dotLottie?.play();
  }
</script>

<DotLottieSvelte
  src="animation.lottie"
  loop={true}
  autoplay={true}
  dotLottieRefCallback={(ref) => dotLottie = ref}
/>

<button on:click={play}>Play</button>
```

## Performance Optimization

### File Size Optimization

**1. Export Settings in After Effects:**
- Enable "Skip images that aren't used"
- Use "Glyphs" instead of fonts when possible
- Simplify paths (reduce points in illustrator)
- Avoid effects that create large data (particles, noise)
- Use shape layers instead of vector layers

**2. Compression:**
- Use dotLottie format (.lottie) for automatic compression
- Run JSON through Lottie optimizer tools
- Remove unnecessary metadata

**3. Lazy Loading:**
```jsx
const LazyLottie = () => {
  const [shouldLoad, setShouldLoad] = React.useState(false);

  React.useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        setShouldLoad(true);
      }
    });

    observer.observe(document.getElementById('lottie-trigger'));
    return () => observer.disconnect();
  }, []);

  return (
    <div id="lottie-trigger">
      {shouldLoad && <DotLottieReact src="animation.lottie" loop autoplay />}
    </div>
  );
};
```

### Runtime Performance

**1. Renderer Selection:**
```javascript
// SVG: Best quality, slower for complex animations
// Canvas: Better performance, rasterized
// HTML: Limited support, use only for simple animations

// For complex animations, prefer canvas
new DotLottie({
  canvas: document.getElementById('canvas'),
  src: 'animation.lottie',
  autoplay: true,
  loop: true,
  renderConfig: {
    devicePixelRatio: window.devicePixelRatio || 1
  }
});
```

**2. Web Workers:**
```javascript
// Offload to worker for heavy animations
import { DotLottieWorker } from '@lottiefiles/dotlottie-web';

new DotLottieWorker({
  canvas: document.getElementById('canvas'),
  src: 'heavy-animation.lottie',
  autoplay: true,
  loop: true
});
```

**3. Mobile Optimization:**
```javascript
// Reduce quality on mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

new DotLottie({
  canvas: document.getElementById('canvas'),
  src: isMobile ? 'animation-low.lottie' : 'animation-high.lottie',
  autoplay: true,
  loop: true,
  renderConfig: {
    devicePixelRatio: isMobile ? 1 : window.devicePixelRatio
  }
});
```

## Common Pitfalls

### 1. Memory Leaks from Improper Cleanup

**Problem:** Not destroying Lottie instances when components unmount.

**Solution:**
```jsx
const SafeAnimation = () => {
  const [dotLottie, setDotLottie] = React.useState(null);

  React.useEffect(() => {
    return () => {
      // Always destroy instance on unmount
      dotLottie?.destroy();
    };
  }, [dotLottie]);

  return <DotLottieReact src="animation.lottie" dotLottieRefCallback={setDotLottie} />;
};
```

### 2. Event Listener Cleanup

**Problem:** Event listeners not removed, causing multiple handlers.

**Solution:**
```jsx
useEffect(() => {
  if (!dotLottie) return;

  const handleComplete = () => console.log('Complete');
  dotLottie.addEventListener('complete', handleComplete);

  // MUST return cleanup function
  return () => {
    dotLottie.removeEventListener('complete', handleComplete);
  };
}, [dotLottie]);
```

### 3. Large File Sizes

**Problem:** Exported JSON files are 500KB+ for simple animations.

**Solutions:**
- Simplify After Effects composition (reduce layers, keyframes)
- Use dotLottie format for compression
- Check Bodymovin export settings (disable "Include expressions" if not needed)
- Remove unused assets before export
- Use Lottie optimizer tools: https://lottiefiles.com/tools/lottie-editor

### 4. Animation Performance Issues

**Problem:** Animation stutters or drops frames.

**Solutions:**
- Switch from SVG to Canvas renderer
- Use `DotLottieWorker` for web worker rendering
- Reduce complexity in After Effects (fewer layers, simpler shapes)
- Lower devicePixelRatio on mobile
- Avoid animating too many properties simultaneously

### 5. Incorrect Path/URL References

**Problem:** Animation doesn't load due to CORS or incorrect paths.

**Solution:**
```jsx
// Use animationData for local imports (best for bundled apps)
import animationData from './animation.json';
<Lottie animationData={animationData} />

// OR use path for external URLs (requires CORS headers)
<DotLottieReact src="https://example.com/animation.lottie" />

// For Next.js, place in public/ folder
<DotLottieReact src="/animations/animation.lottie" />
```

### 6. After Effects Export Compatibility

**Problem:** Some After Effects features don't export to Lottie.

**Unsupported features:**
- Layer effects (drop shadows, glows) - use shape layers instead
- Blending modes (limited support)
- 3D layers
- Expressions (partial support)
- Track mattes (partial support)

**Solution:**
- Test export early and often
- Use LottieFiles preview before exporting
- Check Bodymovin compatibility: https://airbnb.io/lottie/#/supported-features
- Convert effects to shapes when possible

## Resources

This skill includes:

### scripts/
- `generate_lottie_component.py` - Generate React/Vue/Svelte Lottie component boilerplate
- `optimize_lottie.py` - Optimize Lottie JSON file size

### references/
- `api_reference.md` - Complete API documentation for lottie-web, lottie-react, and dotlottie-web
- `after_effects_export.md` - Guide for exporting animations from After Effects
- `performance_guide.md` - Detailed performance optimization strategies

### assets/
- `starter_lottie/` - Complete React + Vite starter template with Lottie examples
- `examples/` - Real-world Lottie animation patterns and use cases

## Related Skills

- **gsap-scrolltrigger** - For scroll-driven Lottie animations synchronized with page scroll
- **motion-framer** - Combine with Framer Motion for layout animations wrapping Lottie
- **animated-component-libraries** - Pre-built components that may include Lottie animations
- **threejs-webgl** - For 3D animations beyond Lottie's 2D capabilities
- **react-three-fiber** - Alternative for complex 3D animated scenes
