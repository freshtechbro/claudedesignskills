# Motion / Framer Motion Examples

Comprehensive collection of real-world animation patterns, production-ready components, and advanced techniques for building animated React applications.

## Table of Contents

- [Page Transitions](#page-transitions)
- [Route Animations](#route-animations)
- [Complex Gestures](#complex-gestures)
- [Scroll-Based Animations](#scroll-based-animations)
- [Advanced Layout Animations](#advanced-layout-animations)
- [Shared Element Transitions](#shared-element-transitions)
- [Modal & Dialog Patterns](#modal--dialog-patterns)
- [Form Animations](#form-animations)
- [Loading States](#loading-states)
- [List Animations](#list-animations)
- [Image Galleries](#image-galleries)
- [Navigation Menus](#navigation-menus)
- [Performance Optimization](#performance-optimization)

---

## Page Transitions

### Full Page Fade

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation } from 'react-router-dom'

function PageTransition({ children }) {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Slide Transition

```jsx
function SlidePageTransition({ children }) {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ x: 300, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: -300, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 260, damping: 20 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Depth Transition (Scale + Blur)

```jsx
function DepthPageTransition({ children }) {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ scale: 0.8, opacity: 0, filter: 'blur(10px)' }}
        animate={{ scale: 1, opacity: 1, filter: 'blur(0px)' }}
        exit={{ scale: 1.2, opacity: 0, filter: 'blur(10px)' }}
        transition={{ duration: 0.5 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Stack Navigation

```jsx
import { useState } from 'react'

function StackNavigation() {
  const [stack, setStack] = useState([{ id: 0, component: 'Home' }])

  const push = (component) => {
    setStack([...stack, { id: stack.length, component }])
  }

  const pop = () => {
    if (stack.length > 1) {
      setStack(stack.slice(0, -1))
    }
  }

  const currentPage = stack[stack.length - 1]

  return (
    <div style={{ position: 'relative', overflow: 'hidden' }}>
      <AnimatePresence mode="popLayout">
        {stack.map((page, index) => (
          <motion.div
            key={page.id}
            initial={{ x: '100%' }}
            animate={{
              x: index === stack.length - 1 ? 0 : '-20%',
              scale: index === stack.length - 1 ? 1 : 0.95,
              opacity: index === stack.length - 1 ? 1 : 0.5
            }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            style={{
              position: index === stack.length - 1 ? 'relative' : 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0
            }}
          >
            <PageComponent name={page.component} onPush={push} onPop={pop} />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
```

---

## Route Animations

### Custom Route Transition with Direction Detection

```jsx
import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'

const routeOrder = ['/', '/about', '/services', '/contact']

function DirectionalRouteTransition({ children }) {
  const location = useLocation()
  const [direction, setDirection] = useState(0)

  useEffect(() => {
    const currentIndex = routeOrder.indexOf(location.pathname)
    const prevIndex = routeOrder.indexOf(sessionStorage.getItem('prevPath') || '/')

    setDirection(currentIndex > prevIndex ? 1 : -1)
    sessionStorage.setItem('prevPath', location.pathname)
  }, [location])

  return (
    <AnimatePresence mode="wait" custom={direction}>
      <motion.div
        key={location.pathname}
        custom={direction}
        initial={(direction) => ({
          x: direction > 0 ? 300 : -300,
          opacity: 0
        })}
        animate={{ x: 0, opacity: 1 }}
        exit={(direction) => ({
          x: direction > 0 ? -300 : 300,
          opacity: 0
        })}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Multi-Stage Route Transition

```jsx
function MultiStageTransition({ children }) {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 20 }}
        animate={{
          opacity: [0, 1, 1],
          y: [20, 0, 0],
          scale: [0.95, 1.02, 1]
        }}
        exit={{
          opacity: [1, 0],
          scale: [1, 0.95]
        }}
        transition={{
          duration: 0.6,
          times: [0, 0.5, 1]
        }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

---

## Complex Gestures

### Multi-Direction Swipe Handler

```jsx
import { motion, useMotionValue, useTransform, PanInfo } from 'framer-motion'

function SwipeCard() {
  const x = useMotionValue(0)
  const y = useMotionValue(0)

  const rotateX = useTransform(y, [-200, 200], [15, -15])
  const rotateY = useTransform(x, [-200, 200], [-15, 15])

  function handleDragEnd(event: MouseEvent, info: PanInfo) {
    const threshold = 100

    if (Math.abs(info.offset.x) > threshold) {
      // Swipe left or right
      console.log(info.offset.x > 0 ? 'Swiped right' : 'Swiped left')
    } else if (Math.abs(info.offset.y) > threshold) {
      // Swipe up or down
      console.log(info.offset.y > 0 ? 'Swiped down' : 'Swiped up')
    }
  }

  return (
    <motion.div
      drag
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
      dragElastic={0.7}
      onDragEnd={handleDragEnd}
      style={{
        x,
        y,
        rotateX,
        rotateY,
        width: 300,
        height: 400,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: 20,
        cursor: 'grab'
      }}
      whileTap={{ cursor: 'grabbing' }}
    />
  )
}
```

### Long Press Gesture

```jsx
import { motion } from 'framer-motion'
import { useState, useRef } from 'react'

function LongPressButton({ onLongPress, children }) {
  const [isPressed, setIsPressed] = useState(false)
  const timerRef = useRef(null)

  const handlePressStart = () => {
    setIsPressed(true)
    timerRef.current = setTimeout(() => {
      onLongPress()
      setIsPressed(false)
    }, 800)
  }

  const handlePressEnd = () => {
    setIsPressed(false)
    if (timerRef.current) {
      clearTimeout(timerRef.current)
    }
  }

  return (
    <motion.button
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
      onMouseLeave={handlePressEnd}
      onTouchStart={handlePressStart}
      onTouchEnd={handlePressEnd}
      animate={{
        scale: isPressed ? 0.95 : 1,
        boxShadow: isPressed
          ? '0 0 0 4px rgba(99, 102, 241, 0.3)'
          : '0 0 0 0px rgba(99, 102, 241, 0)'
      }}
      transition={{ duration: 0.2 }}
      style={{
        padding: '12px 24px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        border: 'none',
        borderRadius: 8,
        cursor: 'pointer',
        position: 'relative'
      }}
    >
      {children}
      {isPressed && (
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.8 }}
          style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            height: 3,
            background: 'white',
            transformOrigin: 'left'
          }}
        />
      )}
    </motion.button>
  )
}
```

### Pinch to Zoom

```jsx
import { motion, useMotionValue, useTransform } from 'framer-motion'
import { useEffect, useRef } from 'react'

function PinchZoomImage({ src }) {
  const scale = useMotionValue(1)
  const x = useMotionValue(0)
  const y = useMotionValue(0)

  const containerRef = useRef(null)

  useEffect(() => {
    const element = containerRef.current
    if (!element) return

    let initialDistance = 0

    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 2) {
        const touch1 = e.touches[0]
        const touch2 = e.touches[1]
        initialDistance = Math.hypot(
          touch2.clientX - touch1.clientX,
          touch2.clientY - touch1.clientY
        )
      }
    }

    const handleTouchMove = (e: TouchEvent) => {
      if (e.touches.length === 2) {
        e.preventDefault()
        const touch1 = e.touches[0]
        const touch2 = e.touches[1]
        const currentDistance = Math.hypot(
          touch2.clientX - touch1.clientX,
          touch2.clientY - touch1.clientY
        )

        const newScale = (currentDistance / initialDistance) * scale.get()
        scale.set(Math.min(Math.max(newScale, 0.5), 3))
      }
    }

    element.addEventListener('touchstart', handleTouchStart)
    element.addEventListener('touchmove', handleTouchMove)

    return () => {
      element.removeEventListener('touchstart', handleTouchStart)
      element.removeEventListener('touchmove', handleTouchMove)
    }
  }, [])

  return (
    <div ref={containerRef} style={{ overflow: 'hidden', touchAction: 'none' }}>
      <motion.img
        src={src}
        drag
        dragConstraints={containerRef}
        style={{
          scale,
          x,
          y,
          maxWidth: '100%',
          cursor: 'grab'
        }}
        whileTap={{ cursor: 'grabbing' }}
      />
    </div>
  )
}
```

---

## Scroll-Based Animations

### Parallax Scrolling

```jsx
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

function ParallaxSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start']
  })

  const y = useTransform(scrollYProgress, [0, 1], ['-20%', '20%'])
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0])

  return (
    <div ref={ref} style={{ height: '100vh', position: 'relative', overflow: 'hidden' }}>
      <motion.div
        style={{
          y,
          opacity,
          position: 'absolute',
          inset: 0,
          backgroundImage: 'url(/hero-bg.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      <div style={{ position: 'relative', zIndex: 1 }}>
        <h1>Parallax Content</h1>
      </div>
    </div>
  )
}
```

### Scroll Progress Indicator

```jsx
import { motion, useScroll } from 'framer-motion'

function ScrollProgressBar() {
  const { scrollYProgress } = useScroll()

  return (
    <motion.div
      style={{
        scaleX: scrollYProgress,
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: 4,
        background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
        transformOrigin: 'left',
        zIndex: 9999
      }}
    />
  )
}
```

### Scroll-Triggered Animation Sequence

```jsx
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

function ScrollSequence() {
  const containerRef = useRef(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start end', 'end start']
  })

  const scale1 = useTransform(scrollYProgress, [0, 0.3], [0.8, 1])
  const scale2 = useTransform(scrollYProgress, [0.2, 0.5], [0.8, 1])
  const scale3 = useTransform(scrollYProgress, [0.4, 0.7], [0.8, 1])
  const scale4 = useTransform(scrollYProgress, [0.6, 0.9], [0.8, 1])

  const opacity1 = useTransform(scrollYProgress, [0, 0.3], [0, 1])
  const opacity2 = useTransform(scrollYProgress, [0.2, 0.5], [0, 1])
  const opacity3 = useTransform(scrollYProgress, [0.4, 0.7], [0, 1])
  const opacity4 = useTransform(scrollYProgress, [0.6, 0.9], [0, 1])

  return (
    <div ref={containerRef} style={{ minHeight: '200vh', padding: '50vh 0' }}>
      <motion.div style={{ scale: scale1, opacity: opacity1 }}>
        <h2>Step 1</h2>
      </motion.div>
      <motion.div style={{ scale: scale2, opacity: opacity2 }}>
        <h2>Step 2</h2>
      </motion.div>
      <motion.div style={{ scale: scale3, opacity: opacity3 }}>
        <h2>Step 3</h2>
      </motion.div>
      <motion.div style={{ scale: scale4, opacity: opacity4 }}>
        <h2>Step 4</h2>
      </motion.div>
    </div>
  )
}
```

### Scroll-Based Counter

```jsx
import { motion, useScroll, useTransform, useSpring } from 'framer-motion'
import { useRef } from 'react'

function AnimatedCounter({ from = 0, to = 100 }) {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end center']
  })

  const count = useTransform(scrollYProgress, [0, 1], [from, to])
  const roundedCount = useTransform(count, Math.round)
  const smoothCount = useSpring(roundedCount, { stiffness: 100, damping: 20 })

  return (
    <div ref={ref} style={{ minHeight: '50vh', display: 'flex', alignItems: 'center' }}>
      <motion.span style={{ fontSize: '4rem', fontWeight: 'bold' }}>
        {smoothCount}
      </motion.span>
    </div>
  )
}
```

### Sticky Scroll Sections

```jsx
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

function StickyScrollSection() {
  const containerRef = useRef(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end end']
  })

  const sections = [
    { title: 'Introduction', color: '#667eea' },
    { title: 'Features', color: '#764ba2' },
    { title: 'Benefits', color: '#f093fb' },
    { title: 'Conclusion', color: '#f5576c' }
  ]

  return (
    <div ref={containerRef} style={{ height: '400vh', position: 'relative' }}>
      <div style={{ position: 'sticky', top: 0, height: '100vh' }}>
        {sections.map((section, index) => {
          const start = index / sections.length
          const end = (index + 1) / sections.length

          const opacity = useTransform(
            scrollYProgress,
            [start, start + 0.05, end - 0.05, end],
            [0, 1, 1, 0]
          )

          return (
            <motion.div
              key={section.title}
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: section.color,
                opacity
              }}
            >
              <h1 style={{ fontSize: '5rem', color: 'white' }}>{section.title}</h1>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
```

---

## Advanced Layout Animations

### Masonry Grid with Layout Animation

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function MasonryGrid() {
  const [items, setItems] = useState([
    { id: 1, height: 200 },
    { id: 2, height: 300 },
    { id: 3, height: 250 },
    { id: 4, height: 180 },
    { id: 5, height: 280 },
    { id: 6, height: 220 }
  ])

  const removeItem = (id) => {
    setItems(items.filter(item => item.id !== id))
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
      gap: 16,
      padding: 20
    }}>
      <AnimatePresence>
        {items.map(item => (
          <motion.div
            key={item.id}
            layout
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{
              layout: { type: 'spring', stiffness: 300, damping: 30 },
              opacity: { duration: 0.2 }
            }}
            style={{
              height: item.height,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: 12,
              cursor: 'pointer'
            }}
            onClick={() => removeItem(item.id)}
            whileHover={{ scale: 1.05 }}
          />
        ))}
      </AnimatePresence>
    </div>
  )
}
```

### Expandable Card

```jsx
import { motion } from 'framer-motion'
import { useState } from 'react'

function ExpandableCard({ title, content }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      style={{
        background: 'white',
        borderRadius: 16,
        padding: 20,
        cursor: 'pointer',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}
    >
      <motion.h3 layout="position">{title}</motion.h3>
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <p>{content}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
```

### Accordion with Layout Animation

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function Accordion({ items }) {
  const [expandedIndex, setExpandedIndex] = useState(null)

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      {items.map((item, index) => {
        const isExpanded = index === expandedIndex

        return (
          <motion.div
            key={item.id}
            layout
            style={{
              background: 'white',
              borderRadius: 12,
              marginBottom: 8,
              overflow: 'hidden',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}
          >
            <motion.div
              layout="position"
              onClick={() => setExpandedIndex(isExpanded ? null : index)}
              style={{
                padding: 20,
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <h3>{item.title}</h3>
              <motion.div
                animate={{ rotate: isExpanded ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                ▼
              </motion.div>
            </motion.div>

            <AnimatePresence initial={false}>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  style={{ overflow: 'hidden' }}
                >
                  <div style={{ padding: '0 20px 20px' }}>
                    <p>{item.content}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )
      })}
    </div>
  )
}
```

### Grid to List View Toggle

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ViewToggle() {
  const [isGrid, setIsGrid] = useState(true)
  const items = Array.from({ length: 12 }, (_, i) => ({ id: i + 1, title: `Item ${i + 1}` }))

  return (
    <div>
      <button onClick={() => setIsGrid(!isGrid)}>
        Toggle {isGrid ? 'List' : 'Grid'} View
      </button>

      <motion.div
        layout
        style={{
          display: 'grid',
          gridTemplateColumns: isGrid ? 'repeat(4, 1fr)' : '1fr',
          gap: 16,
          padding: 20,
          transition: 'grid-template-columns 0.3s'
        }}
      >
        {items.map(item => (
          <motion.div
            key={item.id}
            layout
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            style={{
              height: isGrid ? 150 : 80,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: 12,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold'
            }}
          >
            {item.title}
          </motion.div>
        ))}
      </motion.div>
    </div>
  )
}
```

---

## Shared Element Transitions

### Image Gallery with Shared Layout

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function SharedLayoutGallery() {
  const [selectedId, setSelectedId] = useState(null)

  const images = [
    { id: 1, src: '/image1.jpg', title: 'Image 1' },
    { id: 2, src: '/image2.jpg', title: 'Image 2' },
    { id: 3, src: '/image3.jpg', title: 'Image 3' },
    { id: 4, src: '/image4.jpg', title: 'Image 4' }
  ]

  return (
    <>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
        {images.map(image => (
          <motion.div
            key={image.id}
            layoutId={`image-${image.id}`}
            onClick={() => setSelectedId(image.id)}
            style={{
              borderRadius: 12,
              overflow: 'hidden',
              cursor: 'pointer'
            }}
            whileHover={{ scale: 1.05 }}
          >
            <img src={image.src} alt={image.title} style={{ width: '100%', display: 'block' }} />
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedId && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedId(null)}
              style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0, 0, 0, 0.8)',
                zIndex: 999,
                cursor: 'pointer'
              }}
            />

            <motion.div
              layoutId={`image-${selectedId}`}
              style={{
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                maxWidth: '90vw',
                maxHeight: '90vh',
                zIndex: 1000,
                borderRadius: 12,
                overflow: 'hidden'
              }}
            >
              <img
                src={images.find(img => img.id === selectedId)?.src}
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
```

### Tab Indicator

```jsx
import { motion } from 'framer-motion'
import { useState } from 'react'

function TabsWithIndicator() {
  const [activeTab, setActiveTab] = useState('home')

  const tabs = [
    { id: 'home', label: 'Home' },
    { id: 'about', label: 'About' },
    { id: 'services', label: 'Services' },
    { id: 'contact', label: 'Contact' }
  ]

  return (
    <div style={{ display: 'flex', gap: 8, background: '#f3f4f6', borderRadius: 12, padding: 4 }}>
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          style={{
            position: 'relative',
            padding: '12px 24px',
            border: 'none',
            background: 'transparent',
            cursor: 'pointer',
            fontWeight: activeTab === tab.id ? 600 : 400,
            color: activeTab === tab.id ? 'white' : '#6b7280',
            zIndex: 1
          }}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="tab-indicator"
              style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: 8,
                zIndex: -1
              }}
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
          {tab.label}
        </button>
      ))}
    </div>
  )
}
```

### Card Expansion with Shared Layout

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ExpandingCardList() {
  const [selectedId, setSelectedId] = useState(null)

  const items = [
    { id: 1, title: 'Card 1', subtitle: 'Subtitle 1', description: 'Full description...' },
    { id: 2, title: 'Card 2', subtitle: 'Subtitle 2', description: 'Full description...' },
    { id: 3, title: 'Card 3', subtitle: 'Subtitle 3', description: 'Full description...' }
  ]

  return (
    <>
      <div style={{ display: 'grid', gap: 16, padding: 20 }}>
        {items.map(item => (
          <motion.div
            key={item.id}
            layoutId={`card-${item.id}`}
            onClick={() => setSelectedId(item.id)}
            style={{
              background: 'white',
              borderRadius: 16,
              padding: 20,
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}
            whileHover={{ scale: 1.02 }}
          >
            <motion.h2 layoutId={`title-${item.id}`}>{item.title}</motion.h2>
            <motion.p layoutId={`subtitle-${item.id}`}>{item.subtitle}</motion.p>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedId && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedId(null)}
              style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0, 0, 0, 0.5)',
                zIndex: 999
              }}
            />

            <motion.div
              layoutId={`card-${selectedId}`}
              style={{
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '90%',
                maxWidth: 600,
                background: 'white',
                borderRadius: 16,
                padding: 32,
                zIndex: 1000
              }}
            >
              <motion.h2 layoutId={`title-${selectedId}`}>
                {items.find(i => i.id === selectedId)?.title}
              </motion.h2>
              <motion.p layoutId={`subtitle-${selectedId}`}>
                {items.find(i => i.id === selectedId)?.subtitle}
              </motion.p>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <p>{items.find(i => i.id === selectedId)?.description}</p>
              </motion.div>
              <button onClick={() => setSelectedId(null)}>Close</button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
```

---

## Modal & Dialog Patterns

### Smooth Modal with Backdrop

```jsx
import { motion, AnimatePresence } from 'framer-motion'

function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.6)',
              backdropFilter: 'blur(4px)',
              zIndex: 999,
              cursor: 'pointer'
            }}
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            style={{
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              background: 'white',
              borderRadius: 16,
              padding: 32,
              maxWidth: 500,
              width: '90%',
              zIndex: 1000,
              boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Drawer / Side Panel

```jsx
import { motion, AnimatePresence } from 'framer-motion'

function Drawer({ isOpen, onClose, position = 'right', children }) {
  const variants = {
    right: {
      initial: { x: '100%' },
      animate: { x: 0 },
      exit: { x: '100%' }
    },
    left: {
      initial: { x: '-100%' },
      animate: { x: 0 },
      exit: { x: '-100%' }
    },
    top: {
      initial: { y: '-100%' },
      animate: { y: 0 },
      exit: { y: '-100%' }
    },
    bottom: {
      initial: { y: '100%' },
      animate: { y: 0 },
      exit: { y: '100%' }
    }
  }

  const positionStyles = {
    right: { top: 0, right: 0, bottom: 0, width: '400px' },
    left: { top: 0, left: 0, bottom: 0, width: '400px' },
    top: { top: 0, left: 0, right: 0, height: '400px' },
    bottom: { bottom: 0, left: 0, right: 0, height: '400px' }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              zIndex: 999
            }}
          />

          <motion.div
            initial={variants[position].initial}
            animate={variants[position].animate}
            exit={variants[position].exit}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            style={{
              position: 'fixed',
              ...positionStyles[position],
              background: 'white',
              zIndex: 1000,
              boxShadow: '-4px 0 20px rgba(0, 0, 0, 0.1)',
              overflowY: 'auto'
            }}
          >
            <div style={{ padding: 32 }}>
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Bottom Sheet (Mobile)

```jsx
import { motion, AnimatePresence, useDragControls, PanInfo } from 'framer-motion'
import { useRef } from 'react'

function BottomSheet({ isOpen, onClose, children }) {
  const dragControls = useDragControls()
  const constraintsRef = useRef(null)

  const handleDragEnd = (event: MouseEvent, info: PanInfo) => {
    if (info.offset.y > 100) {
      onClose()
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              zIndex: 999
            }}
          />

          <motion.div
            ref={constraintsRef}
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            drag="y"
            dragControls={dragControls}
            dragConstraints={{ top: 0, bottom: 0 }}
            dragElastic={{ top: 0, bottom: 0.5 }}
            onDragEnd={handleDragEnd}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            style={{
              position: 'fixed',
              bottom: 0,
              left: 0,
              right: 0,
              background: 'white',
              borderTopLeftRadius: 24,
              borderTopRightRadius: 24,
              maxHeight: '90vh',
              zIndex: 1000,
              boxShadow: '0 -4px 20px rgba(0, 0, 0, 0.1)'
            }}
          >
            <div
              style={{
                padding: '16px 0',
                display: 'flex',
                justifyContent: 'center',
                cursor: 'grab'
              }}
              onPointerDown={(e) => dragControls.start(e)}
            >
              <div style={{
                width: 40,
                height: 4,
                background: '#d1d5db',
                borderRadius: 2
              }} />
            </div>

            <div style={{ padding: '0 24px 24px', overflowY: 'auto' }}>
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Confirmation Dialog with Shake

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ConfirmDialog({ isOpen, onConfirm, onCancel, title, message }) {
  const [isShaking, setIsShaking] = useState(false)

  const handleConfirm = () => {
    setIsShaking(true)
    setTimeout(() => {
      setIsShaking(false)
      onConfirm()
    }, 600)
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              zIndex: 999
            }}
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{
              opacity: 1,
              scale: 1,
              x: isShaking ? [-10, 10, -10, 10, 0] : 0
            }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{
              scale: { type: 'spring', stiffness: 300, damping: 30 },
              x: { duration: 0.5 }
            }}
            style={{
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              background: 'white',
              borderRadius: 16,
              padding: 32,
              maxWidth: 400,
              width: '90%',
              zIndex: 1000
            }}
          >
            <h3>{title}</h3>
            <p>{message}</p>
            <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onCancel}
                style={{
                  flex: 1,
                  padding: '12px 24px',
                  border: '1px solid #d1d5db',
                  background: 'white',
                  borderRadius: 8,
                  cursor: 'pointer'
                }}
              >
                Cancel
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleConfirm}
                style={{
                  flex: 1,
                  padding: '12px 24px',
                  border: 'none',
                  background: '#ef4444',
                  color: 'white',
                  borderRadius: 8,
                  cursor: 'pointer'
                }}
              >
                Confirm
              </motion.button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

---

## Form Animations

### Floating Label Input

```jsx
import { motion } from 'framer-motion'
import { useState } from 'react'

function FloatingLabelInput({ label, type = 'text', ...props }) {
  const [isFocused, setIsFocused] = useState(false)
  const [hasValue, setHasValue] = useState(false)

  const isFloating = isFocused || hasValue

  return (
    <div style={{ position: 'relative', marginBottom: 24 }}>
      <motion.label
        animate={{
          y: isFloating ? -24 : 0,
          scale: isFloating ? 0.85 : 1,
          color: isFocused ? '#667eea' : '#6b7280'
        }}
        transition={{ duration: 0.2 }}
        style={{
          position: 'absolute',
          left: 12,
          top: 12,
          transformOrigin: 'left',
          pointerEvents: 'none',
          fontWeight: 500
        }}
      >
        {label}
      </motion.label>

      <motion.input
        type={type}
        onFocus={() => setIsFocused(true)}
        onBlur={(e) => {
          setIsFocused(false)
          setHasValue(e.target.value !== '')
        }}
        animate={{
          borderColor: isFocused ? '#667eea' : '#d1d5db'
        }}
        transition={{ duration: 0.2 }}
        style={{
          width: '100%',
          padding: '12px',
          paddingTop: isFloating ? 24 : 12,
          border: '2px solid',
          borderRadius: 8,
          fontSize: '1rem',
          outline: 'none'
        }}
        {...props}
      />
    </div>
  )
}
```

### Multi-Step Form with Progress

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function MultiStepForm() {
  const [step, setStep] = useState(0)
  const [direction, setDirection] = useState(1)

  const steps = [
    { title: 'Personal Info', fields: ['name', 'email'] },
    { title: 'Address', fields: ['street', 'city'] },
    { title: 'Confirmation', fields: [] }
  ]

  const nextStep = () => {
    setDirection(1)
    setStep(Math.min(step + 1, steps.length - 1))
  }

  const prevStep = () => {
    setDirection(-1)
    setStep(Math.max(step - 1, 0))
  }

  const progress = ((step + 1) / steps.length) * 100

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 40 }}>
      {/* Progress Bar */}
      <div style={{ marginBottom: 40 }}>
        <div style={{
          height: 4,
          background: '#e5e7eb',
          borderRadius: 2,
          overflow: 'hidden'
        }}>
          <motion.div
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
            style={{
              height: '100%',
              background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)'
            }}
          />
        </div>
      </div>

      {/* Step Content */}
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={step}
          custom={direction}
          initial={(direction) => ({
            x: direction > 0 ? 300 : -300,
            opacity: 0
          })}
          animate={{ x: 0, opacity: 1 }}
          exit={(direction) => ({
            x: direction > 0 ? -300 : 300,
            opacity: 0
          })}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        >
          <h2>{steps[step].title}</h2>
          <div style={{ marginTop: 24 }}>
            {steps[step].fields.map(field => (
              <FloatingLabelInput key={field} label={field} />
            ))}
            {step === steps.length - 1 && (
              <div>
                <p>Review your information and submit.</p>
              </div>
            )}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div style={{ display: 'flex', gap: 12, marginTop: 32 }}>
        {step > 0 && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={prevStep}
            style={{
              padding: '12px 24px',
              border: '1px solid #d1d5db',
              background: 'white',
              borderRadius: 8,
              cursor: 'pointer'
            }}
          >
            Previous
          </motion.button>
        )}
        {step < steps.length - 1 ? (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={nextStep}
            style={{
              flex: 1,
              padding: '12px 24px',
              border: 'none',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              borderRadius: 8,
              cursor: 'pointer'
            }}
          >
            Next
          </motion.button>
        ) : (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              flex: 1,
              padding: '12px 24px',
              border: 'none',
              background: '#10b981',
              color: 'white',
              borderRadius: 8,
              cursor: 'pointer'
            }}
          >
            Submit
          </motion.button>
        )}
      </div>
    </div>
  )
}
```

### Form Validation with Animation

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function ValidatedInput({ label, validation, ...props }) {
  const [value, setValue] = useState('')
  const [error, setError] = useState('')
  const [touched, setTouched] = useState(false)

  const handleBlur = () => {
    setTouched(true)
    if (validation) {
      const errorMessage = validation(value)
      setError(errorMessage)
    }
  }

  const hasError = touched && error

  return (
    <div style={{ marginBottom: 24 }}>
      <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
        {label}
      </label>

      <motion.input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={handleBlur}
        animate={{
          borderColor: hasError ? '#ef4444' : '#d1d5db',
          x: hasError ? [-10, 10, -10, 10, 0] : 0
        }}
        transition={{
          borderColor: { duration: 0.2 },
          x: { duration: 0.4 }
        }}
        style={{
          width: '100%',
          padding: 12,
          border: '2px solid',
          borderRadius: 8,
          fontSize: '1rem',
          outline: 'none'
        }}
        {...props}
      />

      <AnimatePresence>
        {hasError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            style={{
              marginTop: 8,
              color: '#ef4444',
              fontSize: '0.875rem'
            }}
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Usage
function ContactForm() {
  return (
    <form>
      <ValidatedInput
        label="Email"
        type="email"
        validation={(value) => {
          if (!value) return 'Email is required'
          if (!/\S+@\S+\.\S+/.test(value)) return 'Invalid email format'
          return ''
        }}
      />
      <ValidatedInput
        label="Password"
        type="password"
        validation={(value) => {
          if (!value) return 'Password is required'
          if (value.length < 8) return 'Password must be at least 8 characters'
          return ''
        }}
      />
    </form>
  )
}
```

---

## Loading States

### Skeleton Loading

```jsx
import { motion } from 'framer-motion'

function Skeleton({ width, height, borderRadius = 8 }) {
  return (
    <motion.div
      animate={{
        opacity: [0.5, 1, 0.5]
      }}
      transition={{
        duration: 1.5,
        repeat: Infinity,
        ease: 'easeInOut'
      }}
      style={{
        width,
        height,
        borderRadius,
        background: 'linear-gradient(90deg, #e5e7eb 0%, #f3f4f6 50%, #e5e7eb 100%)',
        backgroundSize: '200% 100%'
      }}
    />
  )
}

function SkeletonCard() {
  return (
    <div style={{ padding: 20, background: 'white', borderRadius: 16 }}>
      <Skeleton width="100%" height={200} />
      <div style={{ marginTop: 16 }}>
        <Skeleton width="70%" height={24} />
      </div>
      <div style={{ marginTop: 12 }}>
        <Skeleton width="100%" height={16} />
        <div style={{ marginTop: 8 }}>
          <Skeleton width="90%" height={16} />
        </div>
      </div>
    </div>
  )
}
```

### Spinner with Variants

```jsx
import { motion } from 'framer-motion'

function Spinner({ size = 40, color = '#667eea' }) {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{
        duration: 1,
        repeat: Infinity,
        ease: 'linear'
      }}
      style={{
        width: size,
        height: size,
        border: `4px solid rgba(102, 126, 234, 0.2)`,
        borderTopColor: color,
        borderRadius: '50%'
      }}
    />
  )
}

function DotsSpinner() {
  return (
    <div style={{ display: 'flex', gap: 8 }}>
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            delay: index * 0.2
          }}
          style={{
            width: 12,
            height: 12,
            borderRadius: '50%',
            background: '#667eea'
          }}
        />
      ))}
    </div>
  )
}
```

### Progress Bar with Pulse

```jsx
import { motion } from 'framer-motion'

function ProgressBar({ progress }) {
  return (
    <div style={{
      width: '100%',
      height: 8,
      background: '#e5e7eb',
      borderRadius: 4,
      overflow: 'hidden',
      position: 'relative'
    }}>
      <motion.div
        animate={{ width: `${progress}%` }}
        transition={{ type: 'spring', stiffness: 100, damping: 20 }}
        style={{
          height: '100%',
          background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
          position: 'relative'
        }}
      >
        <motion.div
          animate={{
            x: ['-100%', '100%']
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: 'linear'
          }}
          style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)'
          }}
        />
      </motion.div>
    </div>
  )
}
```

### Content Fade In

```jsx
import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'

function AsyncContent({ fetchData }) {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchData().then((result) => {
      setData(result)
      setIsLoading(false)
    })
  }, [])

  return (
    <AnimatePresence mode="wait">
      {isLoading ? (
        <motion.div
          key="loading"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <Spinner />
        </motion.div>
      ) : (
        <motion.div
          key="content"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          {data && <div>{/* Render your data */}</div>}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

---

## List Animations

### Animated List with Add/Remove

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function AnimatedList() {
  const [items, setItems] = useState([
    { id: 1, text: 'Item 1' },
    { id: 2, text: 'Item 2' },
    { id: 3, text: 'Item 3' }
  ])
  const [nextId, setNextId] = useState(4)

  const addItem = () => {
    setItems([...items, { id: nextId, text: `Item ${nextId}` }])
    setNextId(nextId + 1)
  }

  const removeItem = (id) => {
    setItems(items.filter(item => item.id !== id))
  }

  return (
    <div>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={addItem}
        style={{
          marginBottom: 20,
          padding: '12px 24px',
          background: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: 8,
          cursor: 'pointer'
        }}
      >
        Add Item
      </motion.button>

      <AnimatePresence>
        {items.map((item, index) => (
          <motion.div
            key={item.id}
            layout
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 50 }}
            transition={{
              layout: { type: 'spring', stiffness: 300, damping: 30 },
              opacity: { duration: 0.2 },
              x: { duration: 0.2 }
            }}
            style={{
              padding: 20,
              marginBottom: 12,
              background: 'white',
              borderRadius: 12,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}
          >
            <span>{item.text}</span>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => removeItem(item.id)}
              style={{
                padding: '8px 16px',
                background: '#ef4444',
                color: 'white',
                border: 'none',
                borderRadius: 6,
                cursor: 'pointer'
              }}
            >
              Remove
            </motion.button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
```

### Reorderable List (Drag to Reorder)

```jsx
import { motion, Reorder } from 'framer-motion'
import { useState } from 'react'

function ReorderableList() {
  const [items, setItems] = useState([
    { id: 1, text: 'Item 1' },
    { id: 2, text: 'Item 2' },
    { id: 3, text: 'Item 3' },
    { id: 4, text: 'Item 4' }
  ])

  return (
    <Reorder.Group axis="y" values={items} onReorder={setItems}>
      {items.map((item) => (
        <Reorder.Item key={item.id} value={item}>
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileDrag={{ scale: 1.05, boxShadow: '0 10px 30px rgba(0,0,0,0.2)' }}
            style={{
              padding: 20,
              marginBottom: 12,
              background: 'white',
              borderRadius: 12,
              cursor: 'grab',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              userSelect: 'none'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ fontSize: '1.5rem' }}>☰</span>
              <span>{item.text}</span>
            </div>
          </motion.div>
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

### Staggered Grid

```jsx
import { motion } from 'framer-motion'

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const item = {
  hidden: { opacity: 0, scale: 0.8, y: 20 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 24
    }
  }
}

function StaggeredGrid() {
  const items = Array.from({ length: 12 }, (_, i) => ({ id: i + 1 }))

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: 16,
        padding: 20
      }}
    >
      {items.map((gridItem) => (
        <motion.div
          key={gridItem.id}
          variants={item}
          whileHover={{ scale: 1.05, transition: { duration: 0.2 } }}
          style={{
            height: 150,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            borderRadius: 12,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: '2rem',
            fontWeight: 'bold'
          }}
        >
          {gridItem.id}
        </motion.div>
      ))}
    </motion.div>
  )
}
```

---

## Image Galleries

### Lightbox Gallery

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function LightboxGallery({ images }) {
  const [selectedIndex, setSelectedIndex] = useState(null)

  const handlePrevious = () => {
    setSelectedIndex((selectedIndex - 1 + images.length) % images.length)
  }

  const handleNext = () => {
    setSelectedIndex((selectedIndex + 1) % images.length)
  }

  return (
    <>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
        gap: 16,
        padding: 20
      }}>
        {images.map((image, index) => (
          <motion.div
            key={image.id}
            whileHover={{ scale: 1.05 }}
            onClick={() => setSelectedIndex(index)}
            style={{
              aspectRatio: '1',
              borderRadius: 12,
              overflow: 'hidden',
              cursor: 'pointer'
            }}
          >
            <img
              src={image.thumbnail}
              alt={image.alt}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedIndex !== null && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedIndex(null)}
              style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0, 0, 0, 0.9)',
                zIndex: 999,
                cursor: 'pointer'
              }}
            />

            <motion.div
              key={selectedIndex}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              style={{
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                maxWidth: '90vw',
                maxHeight: '90vh',
                zIndex: 1000
              }}
            >
              <img
                src={images[selectedIndex].full}
                alt={images[selectedIndex].alt}
                style={{
                  maxWidth: '100%',
                  maxHeight: '90vh',
                  borderRadius: 12
                }}
              />
            </motion.div>

            <button
              onClick={(e) => {
                e.stopPropagation()
                handlePrevious()
              }}
              style={{
                position: 'fixed',
                left: 20,
                top: '50%',
                transform: 'translateY(-50%)',
                zIndex: 1001,
                padding: 16,
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                borderRadius: 8,
                cursor: 'pointer',
                fontSize: '2rem',
                color: 'white'
              }}
            >
              ‹
            </button>

            <button
              onClick={(e) => {
                e.stopPropagation()
                handleNext()
              }}
              style={{
                position: 'fixed',
                right: 20,
                top: '50%',
                transform: 'translateY(-50%)',
                zIndex: 1001,
                padding: 16,
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                borderRadius: 8,
                cursor: 'pointer',
                fontSize: '2rem',
                color: 'white'
              }}
            >
              ›
            </button>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
```

### Carousel with Swipe

```jsx
import { motion, AnimatePresence, PanInfo } from 'framer-motion'
import { useState } from 'react'

function Carousel({ images }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [direction, setDirection] = useState(0)

  const slideVariants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 1000 : -1000,
      opacity: 0
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 1000 : -1000,
      opacity: 0
    })
  }

  const swipeConfidenceThreshold = 10000
  const swipePower = (offset: number, velocity: number) => {
    return Math.abs(offset) * velocity
  }

  const paginate = (newDirection: number) => {
    setDirection(newDirection)
    setCurrentIndex((currentIndex + newDirection + images.length) % images.length)
  }

  const handleDragEnd = (e: MouseEvent, { offset, velocity }: PanInfo) => {
    const swipe = swipePower(offset.x, velocity.x)

    if (swipe < -swipeConfidenceThreshold) {
      paginate(1)
    } else if (swipe > swipeConfidenceThreshold) {
      paginate(-1)
    }
  }

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: 400,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      overflow: 'hidden'
    }}>
      <AnimatePresence initial={false} custom={direction}>
        <motion.img
          key={currentIndex}
          src={images[currentIndex]}
          custom={direction}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{
            x: { type: 'spring', stiffness: 300, damping: 30 },
            opacity: { duration: 0.2 }
          }}
          drag="x"
          dragConstraints={{ left: 0, right: 0 }}
          dragElastic={1}
          onDragEnd={handleDragEnd}
          style={{
            position: 'absolute',
            maxWidth: '100%',
            maxHeight: '100%',
            borderRadius: 12
          }}
        />
      </AnimatePresence>

      <button
        onClick={() => paginate(-1)}
        style={{
          position: 'absolute',
          left: 10,
          zIndex: 2,
          padding: 12,
          background: 'rgba(255, 255, 255, 0.8)',
          border: 'none',
          borderRadius: 8,
          cursor: 'pointer'
        }}
      >
        ‹
      </button>

      <button
        onClick={() => paginate(1)}
        style={{
          position: 'absolute',
          right: 10,
          zIndex: 2,
          padding: 12,
          background: 'rgba(255, 255, 255, 0.8)',
          border: 'none',
          borderRadius: 8,
          cursor: 'pointer'
        }}
      >
        ›
      </button>

      <div style={{
        position: 'absolute',
        bottom: 20,
        display: 'flex',
        gap: 8
      }}>
        {images.map((_, index) => (
          <div
            key={index}
            onClick={() => {
              setDirection(index > currentIndex ? 1 : -1)
              setCurrentIndex(index)
            }}
            style={{
              width: 10,
              height: 10,
              borderRadius: '50%',
              background: index === currentIndex ? 'white' : 'rgba(255, 255, 255, 0.5)',
              cursor: 'pointer'
            }}
          />
        ))}
      </div>
    </div>
  )
}
```

---

## Navigation Menus

### Animated Dropdown Menu

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function DropdownMenu({ trigger, items }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div style={{ position: 'relative' }}>
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        style={{
          padding: '12px 24px',
          background: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: 8,
          cursor: 'pointer'
        }}
      >
        {trigger}
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              style={{
                position: 'fixed',
                inset: 0,
                zIndex: 998
              }}
            />

            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                marginTop: 8,
                minWidth: 200,
                background: 'white',
                borderRadius: 12,
                boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
                overflow: 'hidden',
                zIndex: 999
              }}
            >
              {items.map((item, index) => (
                <motion.div
                  key={index}
                  whileHover={{ background: '#f3f4f6' }}
                  onClick={() => {
                    item.onClick?.()
                    setIsOpen(false)
                  }}
                  style={{
                    padding: '12px 20px',
                    cursor: 'pointer'
                  }}
                >
                  {item.label}
                </motion.div>
              ))}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
```

### Mega Menu

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function MegaMenu() {
  const [activeMenu, setActiveMenu] = useState(null)

  const menus = {
    products: {
      sections: [
        {
          title: 'Category 1',
          items: ['Product 1', 'Product 2', 'Product 3']
        },
        {
          title: 'Category 2',
          items: ['Product 4', 'Product 5', 'Product 6']
        }
      ]
    },
    solutions: {
      sections: [
        {
          title: 'For Business',
          items: ['Enterprise', 'Small Business']
        },
        {
          title: 'For Developers',
          items: ['API', 'Documentation']
        }
      ]
    }
  }

  return (
    <nav style={{ background: 'white', padding: '16px 0', borderBottom: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', gap: 32, maxWidth: 1200, margin: '0 auto', padding: '0 20px' }}>
        {Object.keys(menus).map((menuKey) => (
          <div
            key={menuKey}
            onMouseEnter={() => setActiveMenu(menuKey)}
            onMouseLeave={() => setActiveMenu(null)}
            style={{ position: 'relative' }}
          >
            <button
              style={{
                padding: '8px 16px',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontWeight: 500,
                textTransform: 'capitalize'
              }}
            >
              {menuKey}
            </button>

            <AnimatePresence>
              {activeMenu === menuKey && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    marginTop: 8,
                    background: 'white',
                    borderRadius: 12,
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
                    padding: 32,
                    display: 'flex',
                    gap: 48,
                    minWidth: 600,
                    zIndex: 999
                  }}
                >
                  {menus[menuKey].sections.map((section, index) => (
                    <div key={index}>
                      <h4 style={{ marginBottom: 16, fontWeight: 600 }}>{section.title}</h4>
                      <ul style={{ listStyle: 'none', padding: 0 }}>
                        {section.items.map((item, itemIndex) => (
                          <motion.li
                            key={itemIndex}
                            whileHover={{ x: 4, color: '#667eea' }}
                            style={{
                              padding: '8px 0',
                              cursor: 'pointer',
                              transition: 'color 0.2s'
                            }}
                          >
                            {item}
                          </motion.li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </nav>
  )
}
```

### Mobile Hamburger Menu

```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

function HamburgerMenu() {
  const [isOpen, setIsOpen] = useState(false)

  const menuItems = [
    { label: 'Home', href: '/' },
    { label: 'About', href: '/about' },
    { label: 'Services', href: '/services' },
    { label: 'Contact', href: '/contact' }
  ]

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 6,
          background: 'transparent',
          border: 'none',
          cursor: 'pointer',
          padding: 8
        }}
      >
        <motion.span
          animate={isOpen ? { rotate: 45, y: 9 } : { rotate: 0, y: 0 }}
          style={{
            width: 30,
            height: 3,
            background: '#1f2937',
            borderRadius: 2
          }}
        />
        <motion.span
          animate={isOpen ? { opacity: 0 } : { opacity: 1 }}
          style={{
            width: 30,
            height: 3,
            background: '#1f2937',
            borderRadius: 2
          }}
        />
        <motion.span
          animate={isOpen ? { rotate: -45, y: -9 } : { rotate: 0, y: 0 }}
          style={{
            width: 30,
            height: 3,
            background: '#1f2937',
            borderRadius: 2
          }}
        />
      </button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              style={{
                position: 'fixed',
                inset: 0,
                background: 'rgba(0, 0, 0, 0.5)',
                zIndex: 998
              }}
            />

            <motion.nav
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              style={{
                position: 'fixed',
                top: 0,
                right: 0,
                bottom: 0,
                width: '80%',
                maxWidth: 400,
                background: 'white',
                zIndex: 999,
                padding: 40
              }}
            >
              {menuItems.map((item, index) => (
                <motion.a
                  key={item.href}
                  href={item.href}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ x: 8, color: '#667eea' }}
                  style={{
                    display: 'block',
                    padding: '16px 0',
                    fontSize: '1.25rem',
                    textDecoration: 'none',
                    color: '#1f2937'
                  }}
                >
                  {item.label}
                </motion.a>
              ))}
            </motion.nav>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
```

---

## Performance Optimization

### useReducedMotion Hook

```jsx
import { useReducedMotion } from 'framer-motion'

function AccessibleAnimation() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: shouldReduceMotion ? 0.01 : 0.5
      }}
    >
      Content that respects user preferences
    </motion.div>
  )
}
```

### Lazy Motion Component

```jsx
import { lazy } from 'react'
import { LazyMotion, domAnimation, m } from 'framer-motion'

// Use 'm' instead of 'motion' with LazyMotion for smaller bundle
function OptimizedComponent() {
  return (
    <LazyMotion features={domAnimation}>
      <m.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        style={{ width: 200, height: 200, background: '#667eea' }}
      />
    </LazyMotion>
  )
}
```

### will-change Optimization

```jsx
function OptimizedAnimatedBox() {
  return (
    <motion.div
      whileHover={{ scale: 1.1 }}
      style={{
        width: 200,
        height: 200,
        background: '#667eea',
        // Hint to browser that this property will change
        willChange: 'transform'
      }}
    />
  )
}
```

### Reuse Variant Objects

```jsx
// ✅ Good - reused variants
const fadeVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

function ComponentA() {
  return <motion.div variants={fadeVariants} initial="hidden" animate="visible" />
}

function ComponentB() {
  return <motion.div variants={fadeVariants} initial="hidden" animate="visible" />
}

// ❌ Bad - recreating variants
function ComponentC() {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0 },
        visible: { opacity: 1 }
      }}
      initial="hidden"
      animate="visible"
    />
  )
}
```

### Throttle Scroll Events

```jsx
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'
import { useThrottle } from './useThrottle'

function ThrottledScroll() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({ target: ref })

  // Throttle scroll updates to 60fps max
  const throttledProgress = useThrottle(scrollYProgress, 16)
  const y = useTransform(throttledProgress, [0, 1], [0, -100])

  return (
    <motion.div ref={ref} style={{ y }}>
      Optimized scroll animation
    </motion.div>
  )
}
```

### Exit Before Enter (Reduce Simultaneous Animations)

```jsx
import { AnimatePresence } from 'framer-motion'

// ✅ Good - "wait" mode reduces simultaneous animations
function OptimizedPageTransition() {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      />
    </AnimatePresence>
  )
}
```

---

## Best Practices Summary

### 1. Use Transform Properties

```jsx
// ✅ Good - hardware accelerated
<motion.div animate={{ x: 100, scale: 1.2 }} />

// ❌ Bad - triggers layout reflow
<motion.div animate={{ left: 100, width: 200 }} />
```

### 2. Respect Accessibility

```jsx
import { useReducedMotion } from 'framer-motion'

function AccessibleComponent() {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.div
      animate={{
        scale: prefersReducedMotion ? 1 : 1.2,
        transition: { duration: prefersReducedMotion ? 0 : 0.5 }
      }}
    />
  )
}
```

### 3. Optimize Bundle Size

```jsx
import { LazyMotion, domAnimation, m } from 'framer-motion'

function SmallBundle() {
  return (
    <LazyMotion features={domAnimation}>
      <m.div animate={{ opacity: 1 }} />
    </LazyMotion>
  )
}
```

### 4. Clean Up Animations

```jsx
import { useAnimation } from 'framer-motion'
import { useEffect } from 'react'

function CleanupExample() {
  const controls = useAnimation()

  useEffect(() => {
    controls.start({ opacity: 1 })

    // Cleanup on unmount
    return () => {
      controls.stop()
    }
  }, [])

  return <motion.div animate={controls} />
}
```

### 5. Debounce/Throttle Expensive Operations

```jsx
import { motion, useMotionValue } from 'framer-motion'
import { useDebounce } from './useDebounce'

function DebouncedInput() {
  const inputValue = useMotionValue('')
  const debouncedValue = useDebounce(inputValue, 300)

  return (
    <motion.input
      onChange={(e) => inputValue.set(e.target.value)}
    />
  )
}
```

---

## Additional Resources

- [Framer Motion Official Docs](https://www.framer.com/motion/)
- [Motion Dev](https://motion.dev/) - New Motion library
- [Motion Examples](https://www.framer.com/motion/examples/)
- [Motion API Reference](https://www.framer.com/motion/component/)
- [Animation Best Practices](https://web.dev/animations/)

---

## License

MIT - Free for personal and commercial use
