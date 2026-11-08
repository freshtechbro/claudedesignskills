---
name: spline-interactive
description: Browser-based 3D design tool with visual editor, animation, and web export. Use this skill when creating 3D scenes without code, designing interactive web experiences, prototyping 3D UI, exporting to React/web, or building designer-friendly 3D content. Triggers on tasks involving Spline, no-code 3D, visual 3D editor, 3D animation, state-based interactions, React Spline integration, or scene export. Alternative to Three.js for designers who prefer visual tools over code.
---

# Spline Interactive - Browser-Based 3D Design and Animation

## Overview

Spline is a browser-based 3D design and animation platform that enables creators to build interactive 3D experiences without requiring code or specialized software knowledge. It provides a collaborative visual editor for designing, animating, and exporting 3D scenes across multiple platforms.

**Key Features**:
- Visual 3D modeling with parametric shapes, extrusion, and boolean operations
- State-based animation system with timeline controls
- Interactive event system (mouse, keyboard, collision, scroll)
- Multiple export options (React components, web code, public URLs)
- Real-time collaboration with team libraries
- AI-powered generation (3D from text, textures, style transfer)
- Built-in physics and particle systems

**When to Use This Skill**:
- Creating 3D web experiences without writing Three.js code
- Designing interactive product showcases or configurators
- Prototyping 3D UI/UX concepts visually
- Building marketing pages with 3D elements
- Collaborating with designers on 3D content
- Exporting scenes for React or vanilla JS integration

**Alternatives**:
- **Three.js** (threejs-webgl): For developers who prefer code-first approach and need maximum control
- **Babylon.js** (babylonjs-engine): For game-focused projects with built-in physics
- **React Three Fiber** (react-three-fiber): For React developers who want to build 3D with JSX

## Core Concepts

### 1. Scene Structure

Spline organizes projects into scenes containing:
- **Objects**: 3D models, shapes, text, images
- **Lights**: Directional, point, spot lights
- **Cameras**: Orbital, perspective, orthographic
- **Events**: Interaction triggers
- **States**: Animation keyframes

### 2. Components System

Reusable elements that can be:
- Created from any object or group
- Instantiated multiple times
- Updated across all instances
- Overridden per instance

### 3. State-Based Animation

Animations are defined as transitions between states:
- **Default State**: Initial appearance
- **Additional States**: Target appearances
- **Events**: Triggers that cause state transitions
- **Transitions**: Duration, easing, properties

### 4. Interactivity Model

Event-driven system with:
- **Events**: User actions or scene triggers
- **Conditions**: Logic gates (if/else)
- **Actions**: State changes, audio, scene switches
- **Variables**: Dynamic data from APIs or user input

### 5. Export Options

Multiple deployment methods:
- **Public URL**: Direct shareable link
- **Code Export**: React component or vanilla JS
- **Spline Viewer**: Embedded iframe
- **Self-Hosted**: Download and host independently

## Common Patterns

### Pattern 1: Basic React Integration

**Use Case**: Embed a Spline scene in a React application

**Implementation**:

```bash
# Installation
npm install @splinetool/react-spline @splinetool/runtime
```

```jsx
import Spline from '@splinetool/react-spline';

export default function Hero() {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </div>
  );
}
```

**Key Points**:
- Scene URL comes from Spline export dialog
- Component fills parent container
- Automatically handles loading and rendering

### Pattern 2: Event Handling and Object Interaction

**Use Case**: Respond to user clicks on specific objects

**Implementation**:

```jsx
import Spline from '@splinetool/react-spline';

export default function InteractiveScene() {
  function onSplineMouseDown(e) {
    // Check if clicked object is the button
    if (e.target.name === 'Button') {
      console.log('Button clicked!');

      // Get object properties
      console.log('Position:', e.target.position);
      console.log('Rotation:', e.target.rotation);
      console.log('Scale:', e.target.scale);
    }
  }

  function onSplineMouseHover(e) {
    if (e.target.name === 'Button') {
      console.log('Hovering over button');
    }
  }

  return (
    <Spline
      scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
      onSplineMouseDown={onSplineMouseDown}
      onSplineMouseHover={onSplineMouseHover}
    />
  );
}
```

**Available Event Handlers**:
- `onSplineMouseDown` - Mouse press on object
- `onSplineMouseUp` - Mouse release
- `onSplineMouseHover` - Mouse over object
- `onSplineKeyDown` - Keyboard press
- `onSplineKeyUp` - Keyboard release
- `onSplineStart` - Scene loaded and started
- `onSplineLookAt` - Camera look-at event
- `onSplineFollow` - Camera follow event
- `onSplineScroll` - Scroll event

### Pattern 3: Programmatic Object Control

**Use Case**: Modify object properties from React code

**Implementation**:

```jsx
import { useRef } from 'react';
import Spline from '@splinetool/react-spline';

export default function ProductViewer() {
  const cube = useRef();
  const splineApp = useRef();

  function onLoad(spline) {
    // Save Spline instance
    splineApp.current = spline;

    // Find object by name
    const obj = spline.findObjectByName('Product');
    // Or by ID
    // const obj = spline.findObjectById('8E8C2DDD-18B6-4C54-861D-7ED2519DE20E');

    cube.current = obj;
  }

  function rotateProduct() {
    if (cube.current) {
      // Rotate 45 degrees around Y axis
      cube.current.rotation.y += Math.PI / 4;
    }
  }

  function changeColor() {
    if (cube.current) {
      // Change material color (hex color)
      cube.current.material.color.set(0xff6b6b);
    }
  }

  function moveProduct() {
    if (cube.current) {
      cube.current.position.x += 50;
      cube.current.position.y += 10;
    }
  }

  return (
    <div>
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
      />
      <div style={{ position: 'absolute', top: 20, left: 20 }}>
        <button onClick={rotateProduct}>Rotate</button>
        <button onClick={changeColor}>Change Color</button>
        <button onClick={moveProduct}>Move</button>
      </div>
    </div>
  );
}
```

**Object Properties You Can Modify**:
- `position` - { x, y, z }
- `rotation` - { x, y, z } (radians)
- `scale` - { x, y, z }
- `material.color` - Color hex value
- `visible` - Boolean

### Pattern 4: Triggering Spline Animations

**Use Case**: Trigger animations defined in Spline from React

**Implementation**:

```jsx
import { useRef } from 'react';
import Spline from '@splinetool/react-spline';

export default function AnimatedCard() {
  const splineApp = useRef();

  function onLoad(app) {
    splineApp.current = app;
  }

  function triggerHoverAnimation() {
    // Emit mouseHover event on 'Card' object
    splineApp.current.emitEvent('mouseHover', 'Card');
  }

  function triggerClickAnimation() {
    // Emit mouseDown event on 'Button' object
    splineApp.current.emitEvent('mouseDown', 'Button');
  }

  function reverseAnimation() {
    // Play animation in reverse
    splineApp.current.emitEventReverse('mouseHover', 'Card');
  }

  return (
    <div>
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
      />
      <button onClick={triggerHoverAnimation}>Hover Effect</button>
      <button onClick={triggerClickAnimation}>Click Effect</button>
      <button onClick={reverseAnimation}>Reverse</button>
    </div>
  );
}
```

**Available Event Types**:
- `mouseDown` - Mouse press
- `mouseHover` - Hover effect
- `mouseUp` - Mouse release
- `keyDown` - Key press
- `keyUp` - Key release
- `start` - Start event
- `lookAt` - Look at camera
- `follow` - Follow camera

### Pattern 5: Next.js Integration with SSR

**Use Case**: Use Spline in Next.js with server-side rendering benefits

**Implementation**:

```jsx
// app/page.js (Next.js 13+ App Router)
import Spline from '@splinetool/react-spline/next';

export default function Home() {
  return (
    <main>
      <div style={{ width: '100vw', height: '100vh' }}>
        <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
      </div>
    </main>
  );
}
```

**Benefits**:
- Placeholder image shown during SSR
- Faster perceived load times
- Better SEO with fallback content

### Pattern 6: Lazy Loading for Performance

**Use Case**: Defer Spline loading until needed

**Implementation**:

```jsx
import React, { Suspense } from 'react';

// Dynamically import Spline
const Spline = React.lazy(() => import('@splinetool/react-spline'));

export default function LazyScene() {
  return (
    <div>
      <h1>My Page Content</h1>

      <Suspense fallback={<div>Loading 3D scene...</div>}>
        <div style={{ width: '100%', height: '500px' }}>
          <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
        </div>
      </Suspense>

      <p>More content below</p>
    </div>
  );
}
```

**Benefits**:
- Reduces initial bundle size
- Improves page load performance
- Shows custom loading UI

### Pattern 7: Responsive Spline Scenes

**Use Case**: Make Spline scenes adapt to different screen sizes

**Implementation**:

```jsx
import Spline from '@splinetool/react-spline';
import { useState, useEffect } from 'react';

export default function ResponsiveScene() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div style={{
      width: '100%',
      height: isMobile ? '400px' : '600px'
    }}>
      <Spline
        scene={
          isMobile
            ? "https://prod.spline.design/YOUR-MOBILE-SCENE/scene.splinecode"
            : "https://prod.spline.design/YOUR-DESKTOP-SCENE/scene.splinecode"
        }
      />
    </div>
  );
}
```

**Alternative Approach** (Single Scene):

```jsx
import Spline from '@splinetool/react-spline';
import { useRef, useEffect } from 'react';

export default function ResponsiveScene() {
  const splineApp = useRef();

  function onLoad(app) {
    splineApp.current = app;
    adjustForScreenSize();
  }

  function adjustForScreenSize() {
    if (!splineApp.current) return;

    const camera = splineApp.current.findObjectByName('Camera');
    const isMobile = window.innerWidth < 768;

    if (isMobile) {
      // Zoom out on mobile
      splineApp.current.setZoom(0.7);
      // Adjust camera position
      camera.position.z = 1500;
    }
  }

  useEffect(() => {
    window.addEventListener('resize', adjustForScreenSize);
    return () => window.removeEventListener('resize', adjustForScreenSize);
  }, []);

  return (
    <Spline
      scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
      onLoad={onLoad}
    />
  );
}
```

## Integration Patterns

### With Three.js (threejs-webgl)

For advanced use cases, combine Spline-designed assets with Three.js code:

1. **Export from Spline**: Use GLTF/GLB export
2. **Import in Three.js**: Load using GLTFLoader
3. **Enhance with code**: Add custom shaders, physics, or effects

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const loader = new GLTFLoader();
loader.load('spline-model.glb', (gltf) => {
  scene.add(gltf.scene);
  // Add custom behaviors
});
```

### With GSAP (gsap-scrolltrigger)

Trigger Spline animations on scroll:

```jsx
import { useEffect, useRef } from 'react';
import Spline from '@splinetool/react-spline';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function ScrollAnimated() {
  const splineApp = useRef();

  function onLoad(app) {
    splineApp.current = app;

    ScrollTrigger.create({
      trigger: '.scene-container',
      start: 'top center',
      onEnter: () => {
        app.emitEvent('mouseHover', 'Product');
      }
    });
  }

  return (
    <div className="scene-container">
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
      />
    </div>
  );
}
```

### With Framer Motion (motion-framer)

Animate container while Spline handles 3D:

```jsx
import { motion } from 'framer-motion';
import Spline from '@splinetool/react-spline';

export default function AnimatedContainer() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      style={{ width: '100%', height: '600px' }}
    >
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </motion.div>
  );
}
```

## Performance Optimization

### 1. Enable On-Demand Rendering

Render only when scene changes, not every frame:

```jsx
<Spline
  scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
  renderOnDemand={true} // Default is true
/>
```

### 2. Optimize Scene in Spline Editor

**In Spline**:
- Reduce polygon count (use decimation)
- Compress textures (lower resolution, use JPG over PNG)
- Limit lights (2-3 lights maximum)
- Use simple materials when possible
- Enable LOD (Level of Detail) for distant objects

### 3. Lazy Load Heavy Scenes

Use React.lazy() as shown in Pattern 6

### 4. Preload Critical Scenes

```jsx
import { useEffect } from 'react';
import Spline from '@splinetool/react-spline';

export default function PreloadedScene() {
  useEffect(() => {
    // Preload scene assets
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = 'https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode';
    document.head.appendChild(link);
  }, []);

  return (
    <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
  );
}
```

### 5. Mobile Optimizations

- Create separate mobile scenes with lower detail
- Reduce canvas resolution on mobile
- Disable shadows and reflections
- Use simpler materials

```jsx
<Spline
  scene={isMobile ? mobileSceneUrl : desktopSceneUrl}
  style={{
    width: '100%',
    height: isMobile ? '300px' : '600px'
  }}
/>
```

## Common Pitfalls and Solutions

### Pitfall 1: Scene Not Loading

**Problem**: Spline component renders but scene doesn't appear

**Solutions**:
```jsx
// ❌ Wrong: Invalid scene URL
<Spline scene="my-scene.splinecode" />

// ✅ Correct: Full URL from Spline export
<Spline scene="https://prod.spline.design/KFonZGtsoUXP-qx7/scene.splinecode" />

// Check for errors
function onLoad(app) {
  console.log('Scene loaded successfully', app);
}

<Spline scene={sceneUrl} onLoad={onLoad} />
```

**Also Check**:
- Scene is published in Spline editor
- Network tab shows successful file downloads
- No CORS errors in console

### Pitfall 2: Object References Lost After Re-render

**Problem**: Object refs become undefined after component updates

**Solution**:
```jsx
// ❌ Wrong: Storing objects without proper refs
let myObject;

function onLoad(spline) {
  myObject = spline.findObjectByName('Cube'); // Lost on re-render
}

// ✅ Correct: Use React refs
const myObject = useRef();

function onLoad(spline) {
  myObject.current = spline.findObjectByName('Cube');
}
```

### Pitfall 3: Performance Issues on Mobile

**Problem**: Scene runs slowly on mobile devices

**Solutions**:
```jsx
// Create mobile-optimized version in Spline editor
// - Fewer polygons (< 50k triangles)
// - Smaller textures (512x512 or less)
// - No shadows or reflections
// - Simpler materials

// Load appropriate version
const isMobile = window.innerWidth < 768;
const sceneUrl = isMobile
  ? 'https://prod.spline.design/MOBILE-SCENE/scene.splinecode'
  : 'https://prod.spline.design/DESKTOP-SCENE/scene.splinecode';

<Spline scene={sceneUrl} renderOnDemand={true} />
```

### Pitfall 4: Events Not Firing

**Problem**: Click or hover events don't trigger

**Solutions**:
```jsx
// ❌ Wrong: Using wrong event name
<Spline onMouseDown={handler} /> // Not a Spline prop

// ✅ Correct: Use Spline event props
<Spline onSplineMouseDown={handler} />

// Also ensure object has events in Spline editor:
// 1. Select object in Spline
// 2. Add event in "Events" panel
// 3. Assign state transition or action
```

### Pitfall 5: Animation Not Triggering Programmatically

**Problem**: `emitEvent()` doesn't trigger animation

**Solutions**:
```jsx
// ❌ Wrong: Calling before scene loads
function triggerAnimation() {
  splineApp.current.emitEvent('mouseHover', 'Button'); // Error if not loaded
}

// ✅ Correct: Ensure scene is loaded
const [isLoaded, setIsLoaded] = useState(false);

function onLoad(app) {
  splineApp.current = app;
  setIsLoaded(true);
}

function triggerAnimation() {
  if (isLoaded && splineApp.current) {
    splineApp.current.emitEvent('mouseHover', 'Button');
  }
}

// Also verify in Spline editor:
// - Object has the correct name ('Button')
// - mouseHover event is configured
// - Event has action (state transition, etc.)
```

### Pitfall 6: Hydration Errors in Next.js

**Problem**: Mismatch between server and client render

**Solution**:
```jsx
// ❌ Wrong: Using standard import in Next.js
import Spline from '@splinetool/react-spline';

// ✅ Correct: Use Next.js-specific import
import Spline from '@splinetool/react-spline/next';

// Or use dynamic import with ssr: false
import dynamic from 'next/dynamic';

const Spline = dynamic(
  () => import('@splinetool/react-spline'),
  { ssr: false }
);
```

## Resources

### Official Documentation
- **Spline Docs**: https://docs.spline.design
- **React Spline GitHub**: https://github.com/splinetool/react-spline
- **Spline Community**: https://spline.community

### Spline Editor
- **Web App**: https://app.spline.design
- **Desktop App**: Available for macOS, Windows, Linux

### Learning Resources
- **Tutorials**: https://spline.design/tutorials
- **YouTube Channel**: Official Spline tutorials
- **Examples Gallery**: https://spline.design/community

### Export Formats
- React component (via `@splinetool/react-spline`)
- Vanilla JavaScript (Web Code API)
- GLTF/GLB (for Three.js, Babylon.js)
- USDZ (for Apple AR)
- STL (for 3D printing)
- Video/GIF (for marketing)

## Related Skills

- **threejs-webgl**: For code-first 3D development with more control
- **react-three-fiber**: For building 3D scenes with React and JSX
- **babylonjs-engine**: Alternative 3D engine with editor workflow
- **motion-framer**: For animating Spline containers and UI elements
- **gsap-scrolltrigger**: For scroll-driven Spline animations
- **figma-dev-mode**: For design-to-code workflow (similar visual approach)

## Scripts

This skill includes utility scripts:
- `project_generator.py` - Generate Spline + React starter projects
- `component_builder.py` - Build Spline component wrappers with events

Run scripts from the skill directory:
```bash
./scripts/project_generator.py
./scripts/component_builder.py
```

## Assets

Starter templates and examples:
- `starter_spline/` - Complete React + Spline template
- `examples/` - Real-world integration patterns
