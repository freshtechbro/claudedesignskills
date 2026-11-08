---
name: web3d-integration-patterns
description: Meta-skill for combining Three.js, GSAP ScrollTrigger, React Three Fiber, Motion, and React Spring for complex 3D web experiences. Use when building applications that integrate multiple 3D and animation libraries, requiring architecture patterns, state management, and performance optimization across the stack. Triggers on tasks involving library integration, multi-library architectures, scroll-driven 3D experiences, physics-based 3D animations, or complex interactive 3D applications.
---

# Web 3D Integration Patterns

## Overview

This meta-skill provides architectural patterns, best practices, and integration strategies for combining multiple 3D and animation libraries in web applications. It synthesizes knowledge from the threejs-webgl, gsap-scrolltrigger, react-three-fiber, motion-framer, and react-spring-physics skills into cohesive patterns for building complex, performant 3D web experiences.

**When to use this skill:**
- Building complex 3D applications that combine multiple libraries
- Creating scroll-driven 3D experiences with animation orchestration
- Implementing physics-based interactions with 3D scenes
- Managing state across 3D rendering and UI animations
- Optimizing performance in multi-library architectures
- Designing reusable component architectures for 3D applications
- Migrating between or combining animation approaches

**Core Integration Combinations:**
1. **Three.js + GSAP** - Scroll-driven 3D animations, timeline orchestration
2. **React Three Fiber + Motion** - State-based 3D with declarative animations
3. **React Three Fiber + GSAP** - Complex 3D sequences in React
4. **React Three Fiber + React Spring** - Physics-based 3D interactions
5. **Three.js + GSAP + React** - Hybrid imperative/declarative 3D

## Architecture Patterns

### Pattern 1: Layered Separation (Three.js + GSAP + React UI)

**Use case:** 3D scene with overlaid UI, scroll-driven animations

**Architecture:**
```
├── 3D Layer (Three.js)
│   ├── Scene management
│   ├── Camera controls
│   └── Render loop
├── Animation Layer (GSAP)
│   ├── ScrollTrigger for 3D properties
│   ├── Timelines for sequences
│   └── UI transitions
└── UI Layer (React + Motion)
    ├── HTML overlays
    ├── State management
    └── User interactions
```

**Implementation:**

```javascript
// App.jsx - React root
import { useEffect, useRef } from 'react'
import { initThreeScene } from './three/scene'
import { initScrollAnimations } from './animations/scroll'
import { motion } from 'framer-motion'

function App() {
  const canvasRef = useRef()
  const sceneRef = useRef()

  useEffect(() => {
    // Initialize Three.js scene
    sceneRef.current = initThreeScene(canvasRef.current)

    // Initialize GSAP ScrollTrigger animations
    initScrollAnimations(sceneRef.current)

    // Cleanup
    return () => {
      sceneRef.current.dispose()
    }
  }, [])

  return (
    <div className="app">
      <canvas ref={canvasRef} />

      <motion.div
        className="overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <section className="hero">
          <h1>3D Experience</h1>
        </section>
        <section className="content">
          {/* Scrollable content */}
        </section>
      </motion.div>
    </div>
  )
}
```

```javascript
// three/scene.js - Three.js setup
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

export function initThreeScene(canvas) {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })

  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

  const controls = new OrbitControls(camera, canvas)
  controls.enableDamping = true

  // Setup scene objects
  const geometry = new THREE.BoxGeometry(2, 2, 2)
  const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 })
  const cube = new THREE.Mesh(geometry, material)
  scene.add(cube)

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)

  camera.position.set(0, 2, 5)

  // Animation loop
  function animate() {
    requestAnimationFrame(animate)
    controls.update()
    renderer.render(scene, camera)
  }
  animate()

  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  })

  return { scene, camera, renderer, cube }
}
```

```javascript
// animations/scroll.js - GSAP ScrollTrigger integration
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export function initScrollAnimations(sceneRefs) {
  const { camera, cube } = sceneRefs

  // Animate camera on scroll
  gsap.to(camera.position, {
    x: 5,
    y: 3,
    z: 10,
    scrollTrigger: {
      trigger: '.content',
      start: 'top top',
      end: 'bottom center',
      scrub: 1,
      onUpdate: () => camera.lookAt(cube.position)
    }
  })

  // Animate mesh rotation
  gsap.to(cube.rotation, {
    y: Math.PI * 2,
    x: Math.PI,
    scrollTrigger: {
      trigger: '.content',
      start: 'top bottom',
      end: 'bottom top',
      scrub: true
    }
  })

  // Animate material properties
  gsap.to(cube.material, {
    opacity: 0.3,
    scrollTrigger: {
      trigger: '.content',
      start: 'top center',
      end: 'center center',
      scrub: 1
    }
  })
}
```

**Benefits:**
- Clear separation of concerns
- Easy to reason about data flow
- Performance optimization per layer
- Independent testing of layers

**Trade-offs:**
- More boilerplate
- Manual synchronization between layers
- State management complexity

---

### Pattern 2: Unified React Component (React Three Fiber + Motion)

**Use case:** React-first architecture with declarative 3D and animations

**Architecture:**
```
React Component Tree
├── <Canvas> (R3F)
│   ├── 3D Scene Components
│   ├── Lights
│   ├── Camera
│   └── Effects
└── <motion.div> (UI overlays)
    ├── HTML content
    └── Animations
```

**Implementation:**

```jsx
// App.jsx - Unified React approach
import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'
import { motion } from 'framer-motion'
import { Scene } from './components/Scene'
import { Loader } from './components/Loader'

function App() {
  return (
    <div className="app">
      <Canvas
        camera={{ position: [0, 2, 5], fov: 75 }}
        dpr={[1, 2]}
        shadows
      >
        <Suspense fallback={<Loader />}>
          <Scene />
        </Suspense>
      </Canvas>

      <motion.div
        className="ui-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <h1>React-First 3D Experience</h1>
      </motion.div>
    </div>
  )
}
```

```jsx
// components/Scene.jsx - R3F scene
import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import { motion } from 'framer-motion-3d'

export function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 10, 7.5]} castShadow />

      <AnimatedCube />
      <Floor />

      <OrbitControls enableDamping dampingFactor={0.05} />
      <Environment preset="sunset" />
    </>
  )
}

function AnimatedCube() {
  const [hovered, setHovered] = useState(false)
  const [active, setActive] = useState(false)

  return (
    <motion.mesh
      scale={active ? 1.5 : 1}
      onClick={() => setActive(!active)}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      animate={{
        rotateY: hovered ? Math.PI * 2 : 0
      }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}
    >
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </motion.mesh>
  )
}

function Floor() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]} receiveShadow>
      <planeGeometry args={[100, 100]} />
      <meshStandardMaterial color="#222" />
    </mesh>
  )
}
```

**Benefits:**
- Declarative, React-first approach
- Unified state management
- Component reusability
- Easy testing with React tools

**Trade-offs:**
- R3F learning curve
- Less control over render loop
- Potential React re-render issues

---

### Pattern 3: Hybrid Approach (R3F + GSAP Timelines)

**Use case:** Complex animation sequences with React state management

**Implementation:**

```jsx
// components/AnimatedScene.jsx
import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import gsap from 'gsap'

export function AnimatedScene() {
  const groupRef = useRef()
  const timelineRef = useRef()

  useEffect(() => {
    // Create GSAP timeline for complex sequence
    const tl = gsap.timeline({ repeat: -1, yoyo: true })

    tl.to(groupRef.current.position, {
      y: 2,
      duration: 1,
      ease: 'power2.inOut'
    })
    .to(groupRef.current.rotation, {
      y: Math.PI * 2,
      duration: 2,
      ease: 'none'
    }, 0) // Start at same time

    timelineRef.current = tl

    return () => tl.kill()
  }, [])

  return (
    <group ref={groupRef}>
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="cyan" />
      </mesh>
    </group>
  )
}
```

---

### Pattern 4: Physics-Based 3D (R3F + React Spring)

**Use case:** Natural, physics-driven 3D interactions

**Implementation:**

```jsx
// components/PhysicsCube.jsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useSpring, animated, config } from '@react-spring/three'

const AnimatedMesh = animated('mesh')

export function PhysicsCube() {
  const [springs, api] = useSpring(() => ({
    scale: 1,
    position: [0, 0, 0],
    config: config.wobbly
  }), [])

  const handleClick = () => {
    api.start({
      scale: 1.5,
      position: [0, 2, 0]
    })

    // Return to original after delay
    setTimeout(() => {
      api.start({
        scale: 1,
        position: [0, 0, 0]
      })
    }, 1000)
  }

  return (
    <AnimatedMesh
      scale={springs.scale}
      position={springs.position}
      onClick={handleClick}
    >
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </AnimatedMesh>
  )
}
```

---

## Common Integration Patterns

### 1. Scroll-Driven Camera Movement

**Three.js + GSAP:**

```javascript
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

// Smooth camera path through multiple points
const cameraPath = [
  { x: 0, y: 2, z: 5, lookAt: { x: 0, y: 0, z: 0 } },
  { x: 5, y: 3, z: 10, lookAt: { x: 0, y: 0, z: 0 } },
  { x: -3, y: 1, z: 8, lookAt: { x: 0, y: 0, z: 0 } }
]

const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '#container',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1,
    pin: true
  }
})

cameraPath.forEach((point, i) => {
  tl.to(camera.position, {
    x: point.x,
    y: point.y,
    z: point.z,
    duration: 1,
    onUpdate: () => camera.lookAt(point.lookAt.x, point.lookAt.y, point.lookAt.z)
  }, i)
})
```

**R3F + ScrollControls (Drei):**

```jsx
import { ScrollControls, Scroll, useScroll } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'

function CameraRig() {
  const scroll = useScroll()

  useFrame((state) => {
    const offset = scroll.offset

    state.camera.position.x = Math.sin(offset * Math.PI * 2) * 5
    state.camera.position.z = Math.cos(offset * Math.PI * 2) * 5
    state.camera.lookAt(0, 0, 0)
  })

  return null
}

export function App() {
  return (
    <Canvas>
      <ScrollControls pages={3} damping={0.5}>
        <CameraRig />
        <Scroll>
          <Scene />
        </Scroll>
      </ScrollControls>
    </Canvas>
  )
}
```

### 2. Gesture-Driven 3D Manipulation

**R3F + Motion (Framer Motion 3D):**

```jsx
import { motion } from 'framer-motion-3d'

function DraggableObject() {
  return (
    <motion.mesh
      drag
      dragElastic={0.1}
      dragConstraints={{ left: -5, right: 5, top: 5, bottom: -5 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      animate={{
        rotateY: [0, Math.PI * 2],
        transition: { repeat: Infinity, duration: 4, ease: 'linear' }
      }}
    >
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial color="hotpink" />
    </motion.mesh>
  )
}
```

### 3. State-Synchronized Animations

**R3F + Zustand + GSAP:**

```jsx
// store.js
import create from 'zustand'

export const useStore = create((set) => ({
  selectedObject: null,
  cameraMode: 'orbit',
  setSelectedObject: (obj) => set({ selectedObject: obj }),
  setCameraMode: (mode) => set({ cameraMode: mode })
}))
```

```jsx
// components/InteractiveObject.jsx
import { useRef, useEffect } from 'react'
import { useStore } from '../store'
import gsap from 'gsap'

export function InteractiveObject({ id }) {
  const meshRef = useRef()
  const selectedObject = useStore((state) => state.selectedObject)
  const setSelectedObject = useStore((state) => state.setSelectedObject)

  const isSelected = selectedObject === id

  useEffect(() => {
    if (isSelected) {
      gsap.to(meshRef.current.scale, {
        x: 1.2,
        y: 1.2,
        z: 1.2,
        duration: 0.3,
        ease: 'back.out'
      })
      gsap.to(meshRef.current.material, {
        emissiveIntensity: 0.5,
        duration: 0.3
      })
    } else {
      gsap.to(meshRef.current.scale, {
        x: 1,
        y: 1,
        z: 1,
        duration: 0.3,
        ease: 'power2.inOut'
      })
      gsap.to(meshRef.current.material, {
        emissiveIntensity: 0,
        duration: 0.3
      })
    }
  }, [isSelected])

  return (
    <mesh
      ref={meshRef}
      onClick={() => setSelectedObject(isSelected ? null : id)}
    >
      <boxGeometry />
      <meshStandardMaterial color="cyan" emissive="cyan" />
    </mesh>
  )
}
```

---

## State Management Strategies

### 1. Zustand for Global 3D State

**Best for:** Shared state across 3D scene and UI

```javascript
// store/scene.js
import create from 'zustand'

export const useSceneStore = create((set, get) => ({
  // State
  camera: { position: [0, 2, 5], target: [0, 0, 0] },
  objects: {},
  selectedId: null,
  isAnimating: false,

  // Actions
  updateCamera: (updates) => set((state) => ({
    camera: { ...state.camera, ...updates }
  })),

  addObject: (id, object) => set((state) => ({
    objects: { ...state.objects, [id]: object }
  })),

  selectObject: (id) => set({ selectedId: id }),

  setAnimating: (isAnimating) => set({ isAnimating })
}))
```

**Usage in R3F:**

```jsx
import { useSceneStore } from '../store/scene'

function Object3D({ id }) {
  const selectedId = useSceneStore((state) => state.selectedId)
  const selectObject = useSceneStore((state) => state.selectObject)

  const isSelected = selectedId === id

  return (
    <mesh onClick={() => selectObject(id)}>
      <boxGeometry />
      <meshStandardMaterial color={isSelected ? 'hotpink' : 'orange'} />
    </mesh>
  )
}
```

---

## Performance Optimization

### Cross-Library Performance Patterns

#### 1. Render Loop Optimization

**Coordinate render loops between Three.js and animation libraries:**

```javascript
// Unified render loop with conditional rendering
import { Clock } from 'three'

const clock = new Clock()
let needsRender = true

function animate() {
  requestAnimationFrame(animate)

  const delta = clock.getDelta()
  const elapsed = clock.getElapsedTime()

  // Only render when needed
  if (needsRender || controls.enabled) {
    // Update GSAP animations (handled automatically)

    // Update Three.js
    controls.update()
    renderer.render(scene, camera)

    // Reset flag
    needsRender = false
  }
}

// Trigger re-render on interactions
ScrollTrigger.addEventListener('update', () => {
  needsRender = true
})
```

#### 2. On-Demand Rendering (R3F)

```jsx
import { Canvas } from '@react-three/fiber'

function App() {
  return (
    <Canvas
      frameloop="demand" // Only renders when needed
      dpr={[1, 2]} // Adaptive pixel ratio
    >
      <Scene />
    </Canvas>
  )
}

function Scene() {
  const invalidate = useThree((state) => state.invalidate)

  // Trigger render on state change
  const handleClick = () => {
    // Update state...
    invalidate() // Manually trigger render
  }

  return <mesh onClick={handleClick}>...</mesh>
}
```

---

## Common Pitfalls

### 1. Animation Conflicts

**Problem:** Multiple libraries trying to animate the same property

```jsx
// ❌ Wrong: GSAP and React Spring both animating position
gsap.to(meshRef.current.position, { x: 5 })
api.start({ position: [10, 0, 0] }) // Conflict!
```

**Solution:** Choose one library per property or coordinate timing

```jsx
// ✅ Correct: Separate properties
gsap.to(meshRef.current.position, { x: 5 }) // GSAP handles position
api.start({ scale: 1.5 }) // Spring handles scale
```

### 2. State Synchronization Issues

**Problem:** React state out of sync with Three.js scene

```jsx
// ❌ Wrong: Updating Three.js without updating React state
mesh.position.x = 5 // Three.js updated
// But React state still shows old value!
```

**Solution:** Use refs or state management

```jsx
// ✅ Correct: Update both
const updatePosition = (x) => {
  mesh.position.x = x
  setPosition(x) // Update React state
}
```

### 3. Memory Leaks from Abandoned Animations

**Problem:** Not cleaning up animations on unmount

```jsx
// ❌ Wrong: No cleanup
useEffect(() => {
  gsap.to(meshRef.current.rotation, { y: Math.PI * 2, repeat: -1 })
}, [])
```

**Solution:** Always cleanup in useEffect return

```jsx
// ✅ Correct: Cleanup on unmount
useEffect(() => {
  const tween = gsap.to(meshRef.current.rotation, { y: Math.PI * 2, repeat: -1 })

  return () => {
    tween.kill()
  }
}, [])
```

---

## Decision Matrix

### When to Use Which Combination

| Use Case | Recommended Stack | Rationale |
|----------|------------------|-----------|
| Marketing landing page with scroll-driven 3D | Three.js + GSAP + React UI | GSAP excels at scroll orchestration |
| React app with interactive 3D product viewer | R3F + Motion | Declarative, state-driven, component-based |
| Complex animation sequences (timeline-based) | R3F + GSAP | GSAP timeline control with R3F components |
| Physics-based interactions (drag, momentum) | R3F + React Spring | Spring physics feel natural for gestures |
| High-performance particle systems | Three.js + GSAP | Imperative control, instancing, minimal overhead |
| Rapid prototyping, quick iterations | R3F + Drei + Motion | High-level abstractions, fast development |
| Game-like experiences with physics | R3F + React Spring + Cannon (physics) | Physics engine + spring-based UI feedback |

---

## Resources

This skill includes bundled resources for multi-library integration:

### references/
- `architecture_patterns.md` - Detailed architectural patterns and trade-offs
- `performance_optimization.md` - Performance strategies across the stack
- `state_management.md` - State management patterns for 3D applications

### scripts/
- `integration_helper.py` - Generate integration boilerplate for library combinations
- `pattern_generator.py` - Scaffold common integration patterns

### assets/
- `starter_unified/` - Complete starter template combining R3F + GSAP + Motion
- `examples/` - Real-world integration examples

---

## Related Skills

**Foundation Skills** (use these for library-specific details):
- **threejs-webgl** - Three.js fundamentals, scene setup, rendering
- **gsap-scrolltrigger** - GSAP animations, ScrollTrigger, timelines
- **react-three-fiber** - R3F components, hooks, Drei helpers
- **motion-framer** - Motion components, gestures, layout animations
- **react-spring-physics** - Spring physics, React Spring hooks

**When to Reference Foundation Skills:**
- Three.js-specific API questions → `threejs-webgl`
- ScrollTrigger syntax → `gsap-scrolltrigger`
- R3F hooks and patterns → `react-three-fiber`
- Motion gesture handling → `motion-framer`
- Spring configuration → `react-spring-physics`

**This Meta-Skill Covers:**
- Architecture patterns for combining libraries
- State management across libraries
- Performance optimization strategies
- Common integration pitfalls
- Decision-making frameworks

---

**Use this skill when building complex 3D web applications that integrate multiple animation and rendering libraries. For library-specific implementation details, reference the individual foundation skills.**
