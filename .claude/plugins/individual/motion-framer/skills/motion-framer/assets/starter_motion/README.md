# Motion Starter Template

A minimal, production-ready starter template for building animated React applications with Framer Motion.

## Features

- ⚡️ **Vite** - Fast build tool and dev server
- ⚛️ **React 18** - Latest React with concurrent features
- 🎨 **Framer Motion** - Production-ready animation library
- 🎮 **Interactive Components** - Hover, tap, and drag interactions
- 📤 **Exit Animations** - AnimatePresence examples
- 🔄 **Layout Animations** - Smooth layout transitions
- 📜 **Stagger Effects** - Coordinated child animations

## Quick Start

### Installation

```bash
npm install
# or
yarn
# or
pnpm install
```

### Development

```bash
npm run dev
```

Opens at `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
starter_motion/
├── index.html           # Entry HTML
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
└── src/
    ├── main.jsx         # React root
    ├── App.jsx          # Main App with examples
    ├── App.css          # Styles
    └── components/
        ├── HoverCard.jsx       # Hover animation example
        ├── DraggableBox.jsx    # Drag interaction example
        └── StaggerList.jsx     # Staggered animation example
```

## Included Examples

### 1. Hover Animations (HoverCard)

Demonstrates `whileHover` for interactive cards:
- Scale on hover
- Shadow effects
- Smooth transitions
- Combined with `whileTap`

### 2. Drag Interactions (DraggableBox)

Shows drag functionality:
- Drag constraints
- Visual feedback (`whileDrag`)
- Drag events (`onDragStart`, `onDragEnd`)
- Elastic boundaries

### 3. Staggered Animations (StaggerList)

Illustrates variant propagation:
- Container/item variant pattern
- `staggerChildren` for sequential animations
- `delayChildren` for initial delay
- Combined with hover effects

### 4. Exit Animations (Modal)

Demonstrates AnimatePresence:
- Exit animations with `exit` prop
- Modal backdrop fade
- Modal enter/exit with spring physics
- Proper cleanup

## Common Patterns

### Basic Animation

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

### Hover Effect

```jsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>
```

### Drag Interaction

```jsx
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  whileDrag={{ scale: 1.1 }}
>
  Drag me
</motion.div>
```

### Exit Animation

```jsx
<AnimatePresence>
  {show && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

### Variants with Stagger

```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="visible">
  <motion.li variants={item}>Item 1</motion.li>
  <motion.li variants={item}>Item 2</motion.li>
</motion.ul>
```

## Customization

### Add New Components

Create new components in `src/components/`:

```jsx
// src/components/MyComponent.jsx
import { motion } from 'framer-motion'

export default function MyComponent() {
  return (
    <motion.div
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
    >
      My Content
    </motion.div>
  )
}
```

Import in App.jsx:
```jsx
import MyComponent from './components/MyComponent'

// In App component:
<MyComponent />
```

### Change Transition Physics

```jsx
// Duration-based
<motion.div
  animate={{ x: 100 }}
  transition={{ duration: 0.5, ease: "easeInOut" }}
/>

// Spring-based (natural, bouncy)
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
/>
```

### Add Scroll Animations

```jsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.3 }}
  transition={{ duration: 0.5 }}
>
  Scroll to reveal
</motion.div>
```

### Layout Animations

```jsx
<motion.div layout>
  {/* Content that changes size/position */}
</motion.div>
```

### Shared Element Transitions

```jsx
// Tab indicator
{tabs.map(tab => (
  <div key={tab.id}>
    {tab.label}
    {activeTab === tab.id && (
      <motion.div layoutId="underline" />
    )}
  </div>
))}
```

## Performance Tips

1. **Use transform properties** - Animate `x`, `y`, `scale`, `rotate` (hardware accelerated)
2. **Avoid layout properties** - Don't animate `width`, `height`, `top`, `left`
3. **Reduce motion** - Respect accessibility preferences:
   ```jsx
   import { useReducedMotion } from "framer-motion"

   const shouldReduceMotion = useReducedMotion()
   ```
4. **Use `will-change` CSS** - For complex animations
5. **Optimize variants** - Reuse variant objects
6. **Lazy load heavy components** - Use React.lazy() for code splitting

## TypeScript Support

To add TypeScript:

```bash
npm install -D typescript @types/react @types/react-dom
```

Rename files to `.tsx`:
```bash
mv src/main.jsx src/main.tsx
mv src/App.jsx src/App.tsx
```

Add `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

## Resources

- [Framer Motion Docs](https://www.framer.com/motion/) - Official documentation
- [Motion Dev](https://motion.dev/) - New Motion library docs
- [Examples](https://www.framer.com/motion/examples/) - Interactive examples
- [API Reference](https://www.framer.com/motion/component/) - Complete API

## Troubleshooting

### Animations Not Working

- Ensure component is wrapped in `<motion.*>` not regular HTML
- Check that `initial` and `animate` props are set
- Verify transition configuration

### Exit Animations Not Working

- Wrap component in `<AnimatePresence>`
- Ensure component has unique `key` prop
- Add `exit` prop to motion component

### Performance Issues

- Use transform properties (x, y, scale, rotate)
- Avoid animating layout properties
- Reduce number of animated elements
- Use `layout="position"` instead of `layout={true}` when possible

### Drag Not Working

- Check `dragConstraints` are set properly
- Ensure parent has defined dimensions
- Verify `drag` prop is set to true or "x"/"y"

## License

MIT - Use freely for personal and commercial projects.
