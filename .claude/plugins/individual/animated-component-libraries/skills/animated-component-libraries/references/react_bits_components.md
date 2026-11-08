# React Bits Component Library Reference

Complete reference for React Bits - 90+ animated React components with minimal dependencies.

## Installation

React Bits uses a copy-paste installation model. Visit [reactbits.dev](https://reactbits.dev), browse components, and copy the code directly into your project.

**Common Dependencies**:
```bash
npm install framer-motion  # For animation-heavy components
npm install ogl           # For WebGL components (Particles, Plasma, Aurora)
npm install react-icons   # For icon components (Dock)
```

## Text Animation Components

### BlurText

Text reveal animation with blur effect, triggered by viewport intersection.

**Props**:
- `text` (string, required): Text to animate
- `delay` (number): Delay between characters/words in ms, default 50
- `animateBy` ("characters" | "words"): Animation unit, default "words"
- `direction` ("top" | "bottom" | "left" | "right"): Animation direction, default "top"
- `threshold` (number): Intersection Observer threshold, default 0.1
- `rootMargin` (string): Intersection Observer root margin, default "0px"
- `stepDuration` (number): Duration per step in seconds, default 0.06
- `animationFrom` (object): Initial animation state, default `{ filter: 'blur(10px)', opacity: 0, y: -50 }`
- `animationTo` (object | array): Final animation state(s)
- `easing` (function): Custom easing function
- `onAnimationComplete` (function): Callback when animation completes
- `className` (string): Additional CSS classes

**Usage**:
```jsx
// Basic word-by-word reveal
<BlurText
  text="Transform your ideas into reality"
  delay={100}
  animateBy="words"
  direction="top"
  className="text-5xl font-bold"
/>

// Character-by-character with custom animation
<BlurText
  text="Pixel-perfect animations"
  delay={50}
  animateBy="characters"
  direction="bottom"
  threshold={0.3}
  animationFrom={{ filter: 'blur(20px)', opacity: 0, y: 50, scale: 0.8 }}
  animationTo={{ filter: 'blur(0px)', opacity: 1, y: 0, scale: 1 }}
  easing={(t) => t * t * (3 - 2 * t)} // Smoothstep
  className="text-2xl"
/>
```

### CircularText

Arranges text in a circular path with optional rotation.

**Props**:
- `text` (string, required): Text to display
- `radius` (number): Circle radius in pixels, default 100
- `fontSize` (number): Font size in pixels, default 16
- `rotateText` (boolean): Enable rotation, default false
- `rotationSpeed` (number): Rotation speed, default 1
- `direction` ("clockwise" | "counterclockwise"): Rotation direction, default "clockwise"
- `className` (string): Additional CSS classes

**Usage**:
```jsx
// Static circular text
<CircularText
  text="REACT BITS • REACT BITS • "
  radius={100}
  fontSize={16}
  className="text-blue-500"
/>

// Rotating circular badge
<div className="relative">
  <CircularText
    text="★ NEW FEATURE ★ AVAILABLE NOW ★ "
    radius={80}
    fontSize={14}
    rotateText={true}
    rotationSpeed={0.5}
    direction="clockwise"
    className="text-yellow-400 font-bold"
  />
  <div className="absolute inset-0 flex items-center justify-center">
    <span className="text-2xl font-bold">NEW</span>
  </div>
</div>
```

### CountUp

Animates numbers from start to end value with formatting options.

**Props**:
- `start` (number): Starting number, default 0
- `end` (number, required): Ending number
- `duration` (number): Animation duration in seconds, default 2
- `decimals` (number): Decimal places, default 0
- `prefix` (string): Text before number, default ""
- `suffix` (string): Text after number, default ""
- `separator` (string): Thousands separator, default ""
- `threshold` (number): Intersection Observer threshold, default 0.1
- `rootMargin` (string): Intersection Observer root margin, default "0px"
- `className` (string): Additional CSS classes

**Usage**:
```jsx
// Revenue counter
<CountUp
  start={0}
  end={1000000}
  duration={3}
  separator=","
  prefix="$"
  className="text-6xl font-bold text-blue-600"
/>

// Percentage counter
<CountUp
  end={99.9}
  duration={2.5}
  decimals={1}
  suffix="%"
  className="text-5xl font-bold text-green-600"
/>

// Simple counter
<CountUp
  end={10000}
  duration={2}
  separator=","
  className="text-6xl font-bold"
/>
```

### SpinningText

Similar to CircularText but from React Bits (verify exact component name in library).

## Interactive Components

### Magnet

Creates magnetic pull effect on child elements when cursor is nearby.

**Props**:
- `magnitude` (number): Pull strength, default 0.3
- `maxDistance` (number): Max distance for effect in pixels, default 150
- `damping` (number): Spring damping, default 25
- `stiffness` (number): Spring stiffness, default 200
- `className` (string): Additional CSS classes
- `children` (ReactNode, required): Element to apply effect to

**Usage**:
```jsx
// Magnetic button
<Magnet>
  <button className="px-8 py-3 bg-blue-600 text-white rounded-lg">
    Click Me
  </button>
</Magnet>

// Customized magnetic pull
<Magnet
  magnitude={0.5}
  maxDistance={200}
  damping={20}
  stiffness={150}
>
  <div className="card p-6">
    <h3>Hover to feel the pull</h3>
  </div>
</Magnet>
```

### Dock

macOS-style dock with magnification effect.

**Props**:
- `items` (array, required): Array of dock items
  - Each item: `{ icon: ReactNode, label: string, onClick: function, className?: string }`
- `spring` (object): Spring physics `{ mass, stiffness, damping }`, default `{ mass: 0.1, stiffness: 150, damping: 12 }`
- `magnification` (number): Magnification amount in pixels, default 60
- `distance` (number): Activation distance in pixels, default 140
- `panelHeight` (number): Dock panel height, default 60
- `baseItemSize` (number): Base icon size, default 48
- `dockHeight` (number): Max dock height, default 250
- `className` (string): Additional CSS classes

**Usage**:
```jsx
import Dock from './components/Dock'
import { VscHome, VscArchive, VscAccount } from 'react-icons/vsc'

const dockItems = [
  {
    icon: <VscHome size={24} />,
    label: 'Dashboard',
    onClick: () => navigate('/dashboard')
  },
  {
    icon: <VscArchive size={24} />,
    label: 'Projects',
    onClick: () => navigate('/projects')
  },
  {
    icon: <VscAccount size={24} />,
    label: 'Profile',
    onClick: () => navigate('/profile')
  }
]

<Dock
  items={dockItems}
  spring={{ mass: 0.15, stiffness: 200, damping: 15 }}
  magnification={80}
  distance={250}
  className="dock-custom"
/>
```

### Stepper

Multi-step form/wizard component with navigation.

**Props**:
- `initialStep` (number): Starting step (1-indexed), default 1
- `onStepChange` (function): Callback when step changes `(step: number) => void`
- `onFinalStepCompleted` (function): Callback when final step is completed
- `stepCircleContainerClassName` (string): Step indicator container styles
- `stepContainerClassName` (string): Individual step indicator styles
- `contentClassName` (string): Content area styles
- `footerClassName` (string): Footer area styles
- `backButtonText` (string): Back button text, default "Back"
- `nextButtonText` (string): Next button text, default "Next"
- `backButtonProps` (object): Props for back button
- `nextButtonProps` (object): Props for next button
- `renderStepIndicator` (function): Custom indicator renderer
- `disableStepIndicators` (boolean): Hide step indicators, default false
- `children` (Step components, required): Step content

**Step Component Props**:
- `children` (ReactNode, required): Step content

**Usage**:
```jsx
import Stepper, { Step } from './components/Stepper'

// Basic stepper
<Stepper
  initialStep={1}
  onStepChange={(step) => console.log('Step:', step)}
  onFinalStepCompleted={() => console.log('Complete!')}
>
  <Step>
    <h2>Step 1: Welcome</h2>
    <p>Getting started content</p>
  </Step>
  <Step>
    <h2>Step 2: Profile</h2>
    <input type="text" placeholder="Name" />
  </Step>
  <Step>
    <h2>Step 3: Preferences</h2>
    <label><input type="checkbox" /> Enable notifications</label>
  </Step>
</Stepper>

// Custom styled stepper
<Stepper
  initialStep={1}
  stepContainerClassName="custom-indicators"
  contentClassName="p-8"
  footerClassName="border-t"
  backButtonText="Previous"
  nextButtonText="Continue"
  backButtonProps={{ className: 'btn-secondary' }}
  nextButtonProps={{ className: 'btn-primary' }}
>
  {/* Steps */}
</Stepper>
```

### MagicButton

Button component with special visual effects (verify exact implementation in library).

## Layout Components

### AnimatedList

List container with staggered entrance animations for children.

**Props**:
- `stagger` (number): Delay between items in seconds, default 0.1
- `duration` (number): Animation duration per item in seconds, default 0.5
- `initial` (object): Initial animation state, default `{ opacity: 0, y: 20 }`
- `animate` (object): Final animation state, default `{ opacity: 1, y: 0 }`
- `exit` (object): Exit animation state, default `{ opacity: 0, y: -20 }`
- `className` (string): Additional CSS classes
- `children` (ReactNode, required): List items

**Usage**:
```jsx
// Basic animated list
<AnimatedList className="space-y-4">
  {notifications.map((notif) => (
    <div key={notif.id} className="notification-item">
      <p>{notif.text}</p>
      <span>{notif.time}</span>
    </div>
  ))}
</AnimatedList>

// Custom animation
<AnimatedList
  stagger={0.15}
  duration={0.6}
  initial={{ opacity: 0, x: -50, scale: 0.8 }}
  animate={{ opacity: 1, x: 0, scale: 1 }}
  exit={{ opacity: 0, x: 50, scale: 0.8 }}
>
  {items.map((item) => (
    <div key={item.id}>{item.content}</div>
  ))}
</AnimatedList>
```

## Background & Visual Effects

### Particles

WebGL-powered 3D particle system.

**Props**:
- `particleCount` (number): Number of particles, default 200
- `particleColors` (string[]): Particle colors array, default `['#ffffff']`
- `particleSpread` (number): Spread factor, default 10
- `speed` (number): Movement speed, default 0.1
- `moveParticlesOnHover` (boolean): Mouse interaction, default false
- `particleHoverFactor` (number): Hover effect strength, default 1
- `disableRotation` (boolean): Disable auto-rotation, default false
- `particleBaseSize` (number): Base particle size, default 100
- `sizeRandomness` (number): Size variation factor, default 1
- `alphaParticles` (boolean): Enable transparency, default false
- `cameraDistance` (number): Camera distance, default 20
- `className` (string): Container CSS classes

**Usage**:
```jsx
// Basic particle background
<section style={{ position: 'relative', height: '100vh' }}>
  <Particles className="absolute inset-0" />
  <div className="relative z-10">
    <h1>Content with particles</h1>
  </div>
</section>

// Customized branded particles
<Particles
  particleCount={300}
  particleColors={['#FF6B6B', '#4ECDC4', '#45B7D1']}
  particleSpread={12}
  speed={0.15}
  moveParticlesOnHover={true}
  particleHoverFactor={2}
  particleBaseSize={120}
  sizeRandomness={1.5}
  alphaParticles={true}
  cameraDistance={25}
/>
```

### Plasma

Organic plasma effect using WebGL.

**Props**:
- `color1` (string): First color, default varies
- `color2` (string): Second color, default varies
- `color3` (string): Third color, default varies
- `speed` (number): Animation speed, default 1
- `blur` (number): Blur amount in pixels, default 50
- `className` (string): Additional CSS classes

**Usage**:
```jsx
// Default plasma
<div className="relative min-h-screen">
  <Plasma />
  <div className="relative z-10 p-8">Content</div>
</div>

// Custom colors and speed
<Plasma
  color1="#FF0080"
  color2="#7928CA"
  color3="#00DFD8"
  speed={0.8}
  blur={30}
  className="plasma-bg"
/>
```

### Aurora

Dynamic gradient aurora effect.

**Props**:
- `colors` (string[]): Color array, default varies
- `speed` (number): Animation speed, default 1
- `blur` (number): Blur amount in pixels, default 50
- `className` (string): Additional CSS classes

**Usage**:
```jsx
// Basic aurora
<div style={{ position: 'relative', minHeight: '100vh' }}>
  <Aurora />
  <main style={{ position: 'relative', zIndex: 1 }}>Content</main>
</div>

// Custom aurora colors
<Aurora
  colors={['#FF00FF', '#00FFFF', '#FFFF00']}
  speed={0.5}
  blur={80}
/>
```

### BlobCursor

Custom cursor with blob trail effect.

**Props**:
- `blobType` ("circle" | "square"): Blob shape, default "circle"
- `fillColor` (string): Blob color, default "#5227FF"
- `trailCount` (number): Number of trail blobs, default 3
- `sizes` (number[]): Blob sizes array, default `[40, 80, 120]`
- Additional customization props

**Usage**:
```jsx
<BlobCursor
  blobType="circle"
  fillColor="#5227FF"
  trailCount={3}
  sizes={[60, 125, 75]}
/>
```

## Performance Optimization

### WebGL Components (Particles, Plasma, Aurora)

1. **Reduce Particle Count on Low-End Devices**:
```jsx
const particleCount = navigator.hardwareConcurrency > 4 ? 300 : 150

<Particles particleCount={particleCount} speed={0.1} />
```

2. **Conditional Loading**:
```jsx
const [enableWebGL, setEnableWebGL] = useState(false)

useEffect(() => {
  const isHighEnd = !navigator.userAgent.includes('Mobile') &&
                   navigator.hardwareConcurrency > 4
  setEnableWebGL(isHighEnd)
}, [])

return enableWebGL ? <Particles /> : <div className="gradient-bg" />
```

### Text Animations

1. **Respect Reduced Motion**:
```jsx
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

<BlurText
  text="Accessible text"
  delay={prefersReducedMotion ? 0 : 100}
  animateBy={prefersReducedMotion ? "none" : "words"}
/>
```

2. **Use RequestIdleCallback**:
```jsx
useEffect(() => {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      // Initialize non-critical animations
    })
  }
}, [])
```

## Common Component Combinations

### Hero with Particles + Text Animation
```jsx
<section style={{ position: 'relative', height: '100vh' }}>
  <Particles
    particleCount={200}
    particleColors={['#4ECDC4']}
    className="absolute inset-0"
  />
  <div className="relative z-10 flex items-center justify-center h-full">
    <BlurText
      text="Welcome to the Future"
      delay={100}
      animateBy="words"
      className="text-7xl font-bold"
    />
  </div>
</section>
```

### Dashboard Stats
```jsx
<div className="grid grid-cols-3 gap-8">
  <div className="text-center">
    <CountUp end={10000} separator="," className="text-5xl font-bold" />
    <p>Users</p>
  </div>
  <div className="text-center">
    <CountUp end={99.9} decimals={1} suffix="%" className="text-5xl font-bold" />
    <p>Uptime</p>
  </div>
  <div className="text-center">
    <CountUp end={1000000} prefix="$" separator="," className="text-5xl font-bold" />
    <p>Revenue</p>
  </div>
</div>
```

### Onboarding Flow
```jsx
<Stepper
  initialStep={1}
  onFinalStepCompleted={() => navigate('/dashboard')}
>
  <Step>
    <BlurText text="Welcome!" className="text-4xl font-bold mb-4" />
    <p>Let's get started</p>
  </Step>
  <Step>
    <h2>Profile Setup</h2>
    <form>{/* Form fields */}</form>
  </Step>
  <Step>
    <h2>All Set!</h2>
    <CountUp end={100} suffix="%" />
  </Step>
</Stepper>
```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- WebGL support required for Particles, Plasma, Aurora
- Intersection Observer support required for BlurText, CountUp
- Framer Motion browser requirements apply

## TypeScript Support

React Bits components include TypeScript definitions. Extend interfaces as needed:

```typescript
interface CustomBlurTextProps extends React.HTMLAttributes<HTMLDivElement> {
  customProp?: string
}
```
