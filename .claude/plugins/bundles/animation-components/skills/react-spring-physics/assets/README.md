# React Spring Physics - Assets

This directory contains starter templates and example documentation for React Spring animations.

## Contents

### Starter Template (Recommended)

For a complete React + Vite starter template with React Spring examples, use the official template:

```bash
# Create new project with Vite
npm create vite@latest my-spring-app -- --template react

# Navigate and install
cd my-spring-app
npm install

# Add React Spring
npm install @react-spring/web

# Optional: Add gesture library
npm install @use-gesture/react
```

### Official Examples

The React Spring team maintains excellent examples at:
- **Documentation**: https://react-spring.dev
- **Examples**: https://react-spring.dev/examples
- **CodeSandbox**: https://codesandbox.io/examples/package/@react-spring/web

### Recommended Examples by Category

**Basic Animations:**
- Spring basics: https://codesandbox.io/s/react-spring-spring-vqqd5
- Trails: https://codesandbox.io/s/react-spring-trail-q0zq5
- Transitions: https://codesandbox.io/s/react-spring-transition-njgm6

**Gesture Integration:**
- Draggable cards: https://codesandbox.io/s/react-spring-draggable-list-xhqod
- Viewpager: https://codesandbox.io/s/react-spring-viewpager-8tsle
- Gesture examples: https://use-gesture.netlify.app/docs/examples/

**Scroll Animations:**
- Scroll progress: https://codesandbox.io/s/react-spring-scroll-progress-8nqwt
- Parallax: https://codesandbox.io/s/react-spring-parallax-sticky-xhdn7
- useScroll hook: https://react-spring.dev/docs/components/use-scroll

**3D Integration (React Three Fiber):**
- Spring animations in 3D: https://codesandbox.io/s/react-spring-3d-ijdj2
- Interactive 3D: https://docs.pmnd.rs/react-three-fiber/tutorials/v8-migration-guide#spring

**Advanced Patterns:**
- Chained animations: https://codesandbox.io/s/react-spring-chain-dxqgq
- Auto-height accordion: https://codesandbox.io/s/react-spring-auto-height-accordion-r4qku
- Masonry grid: https://codesandbox.io/s/react-spring-masonry-5bw7y

## Quick Start Template

Minimal React Spring setup:

### package.json
```json
{
  "name": "react-spring-starter",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@react-spring/web": "^9.7.3",
    "@use-gesture/react": "^10.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }
}
```

### src/App.jsx
```jsx
import { useSpring, animated, config } from '@react-spring/web'
import './App.css'

function App() {
  const [springs, api] = useSpring(() => ({
    from: { y: -50, opacity: 0 }
  }), [])

  const handleClick = () => {
    api.start({
      from: { y: -50, opacity: 0 },
      to: { y: 0, opacity: 1 },
      config: config.wobbly
    })
  }

  return (
    <div className="app">
      <animated.h1 style={springs}>
        React Spring Physics
      </animated.h1>

      <button onClick={handleClick}>
        Animate
      </button>

      <div className="examples">
        <ExampleClick />
        <ExampleTrail />
      </div>
    </div>
  )
}

function ExampleClick() {
  const [springs, api] = useSpring(() => ({
    scale: 1,
    config: { tension: 300, friction: 10 }
  }), [])

  return (
    <animated.div
      className="box"
      onClick={() => api.start({ scale: 1.2 })}
      style={{
        transform: springs.scale.to(s => `scale(${s})`)
      }}
    >
      Click Me
    </animated.div>
  )
}

function ExampleTrail() {
  const items = ['React', 'Spring', 'Physics']
  const trails = useTrail(items.length, {
    from: { opacity: 0, x: -20 },
    to: { opacity: 1, x: 0 },
    config: config.gentle
  })

  return (
    <div className="trail">
      {trails.map((style, i) => (
        <animated.div key={i} style={style} className="trail-item">
          {items[i]}
        </animated.div>
      ))}
    </div>
  )
}

export default App
```

### src/App.css
```css
.app {
  text-align: center;
  padding: 2rem;
}

.examples {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}

.box {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.trail {
  display: flex;
  gap: 1rem;
}

.trail-item {
  padding: 1rem 2rem;
  background: #f0f0f0;
  border-radius: 8px;
  font-weight: 500;
}
```

## Common Patterns

### Pattern 1: Scroll-Triggered Animation

```jsx
import { useInView, animated } from '@react-spring/web'

function ScrollReveal({ children }) {
  const [ref, springs] = useInView(
    () => ({
      from: { opacity: 0, y: 50 },
      to: { opacity: 1, y: 0 }
    }),
    { rootMargin: '-20% 0%' }
  )

  return (
    <animated.div ref={ref} style={springs}>
      {children}
    </animated.div>
  )
}
```

### Pattern 2: List Transitions

```jsx
import { useTransition, animated } from '@react-spring/web'

function AnimatedList({ items }) {
  const transitions = useTransition(items, {
    keys: item => item.id,
    from: { opacity: 0, transform: 'translateX(-20px)' },
    enter: { opacity: 1, transform: 'translateX(0px)' },
    leave: { opacity: 0, transform: 'translateX(20px)' }
  })

  return transitions((style, item) => (
    <animated.div style={style}>
      {item.text}
    </animated.div>
  ))
}
```

### Pattern 3: Gesture-Driven Drag

```jsx
import { useSpring, animated } from '@react-spring/web'
import { useDrag } from '@use-gesture/react'

function DraggableCard() {
  const [{ x, y }, api] = useSpring(() => ({ x: 0, y: 0 }))

  const bind = useDrag(({ down, movement: [mx, my] }) => {
    api.start({
      x: down ? mx : 0,
      y: down ? my : 0,
      immediate: down
    })
  })

  return (
    <animated.div
      {...bind()}
      style={{ x, y, touchAction: 'none' }}
    />
  )
}
```

## TypeScript Support

For TypeScript projects, install types:

```bash
npm install --save-dev @types/react @types/react-dom
```

React Spring is fully typed - no additional @types package needed.

## Testing

For testing with React Spring, disable animations:

```jsx
import { Globals } from '@react-spring/web'

beforeAll(() => {
  Globals.assign({ skipAnimation: true })
})

afterAll(() => {
  Globals.assign({ skipAnimation: false })
})
```

## Additional Resources

- **React Spring Docs**: https://react-spring.dev
- **API Reference**: https://react-spring.dev/docs
- **Discord Community**: https://discord.com/invite/poimandres
- **GitHub**: https://github.com/pmndrs/react-spring
- **Use Gesture**: https://use-gesture.netlify.app (for drag/gesture support)
- **Leva**: https://github.com/pmndrs/leva (for live config tuning)

## Performance Tips

1. **Use function config** for imperative control
2. **Set appropriate precision** to reduce updates
3. **Use useSprings** for batching similar animations
4. **Avoid animating layout** - prefer transforms and opacity
5. **Enable skipAnimation** for tests and accessibility
6. **Monitor with React DevTools Profiler**

---

For more examples and patterns, refer to the skill's references:
- `react_spring_api.md` - Complete API documentation
- `popmotion_api.md` - Low-level physics utilities
- `physics_guide.md` - Spring tuning deep dive
