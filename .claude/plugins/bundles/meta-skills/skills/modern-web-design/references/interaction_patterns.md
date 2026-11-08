# Micro-Interaction Patterns Catalog

## Overview

Comprehensive catalog of micro-interactions for modern web interfaces. Each pattern includes implementation code, accessibility considerations, and performance notes.

Micro-interactions are small, purposeful animations that provide feedback, guide users, and enhance perceived performance.

---

## Table of Contents

1. [Button Interactions](#button-interactions)
2. [Form & Input Interactions](#form--input-interactions)
3. [Loading States](#loading-states)
4. [Navigation Interactions](#navigation-interactions)
5. [Hover Effects](#hover-effects)
6. [Toggle & Switch Interactions](#toggle--switch-interactions)
7. [Card Interactions](#card-interactions)
8. [Scroll Interactions](#scroll-interactions)
9. [Modal & Dialog Interactions](#modal--dialog-interactions)
10. [Toast & Notification Interactions](#toast--notification-interactions)

---

## Button Interactions

### 1.1 Hover Lift

**Effect**: Button lifts up slightly on hover, creating depth.

**Implementation** (CSS):
```css
.button-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.button-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button-lift:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

**Framer Motion**:
```jsx
<motion.button
  whileHover={{ y: -2, boxShadow: "0 4px 12px rgba(0,0,0,0.15)" }}
  whileTap={{ y: 0, boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>
```

**Accessibility**: Preserve for keyboard focus states.

---

### 1.2 Ripple Effect

**Effect**: Material Design-style ripple on click.

**Implementation** (JavaScript):
```javascript
function createRipple(event) {
  const button = event.currentTarget;
  const ripple = document.createElement('span');
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = event.clientX - rect.left - size / 2;
  const y = event.clientY - rect.top - size / 2;

  ripple.style.width = ripple.style.height = `${size}px`;
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;
  ripple.classList.add('ripple');

  button.appendChild(ripple);

  setTimeout(() => ripple.remove(), 600);
}

document.querySelectorAll('.button-ripple').forEach(button => {
  button.addEventListener('click', createRipple);
});
```

**CSS**:
```css
.button-ripple {
  position: relative;
  overflow: hidden;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  transform: scale(0);
  animation: ripple-animation 0.6s ease-out;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

**Performance**: Use `will-change: transform` sparingly.

---

### 1.3 Magnetic Button

**Effect**: Button magnetically attracts cursor on proximity.

**Implementation** (GSAP):
```javascript
const button = document.querySelector('.magnetic-button');
const magneticStrength = 0.3;

button.addEventListener('mousemove', (e) => {
  const rect = button.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const distanceX = (e.clientX - centerX) * magneticStrength;
  const distanceY = (e.clientY - centerY) * magneticStrength;

  gsap.to(button, {
    x: distanceX,
    y: distanceY,
    duration: 0.3,
    ease: "power2.out"
  });
});

button.addEventListener('mouseleave', () => {
  gsap.to(button, {
    x: 0,
    y: 0,
    duration: 0.5,
    ease: "elastic.out(1, 0.3)"
  });
});
```

**Accessibility**: Disable on mobile/touch devices.

---

### 1.4 Loading Button State

**Effect**: Button morphs into loading spinner.

**Framer Motion**:
```jsx
function LoadingButton() {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <motion.button
      onClick={() => setIsLoading(true)}
      animate={isLoading ? "loading" : "idle"}
      disabled={isLoading}
      style={{ position: 'relative', overflow: 'hidden' }}
    >
      <motion.span
        variants={{
          idle: { opacity: 1 },
          loading: { opacity: 0 }
        }}
      >
        Submit
      </motion.span>

      <motion.div
        className="spinner"
        variants={{
          idle: { opacity: 0, scale: 0 },
          loading: { opacity: 1, scale: 1 }
        }}
        style={{ position: 'absolute', inset: 0 }}
      >
        <Spinner />
      </motion.div>
    </motion.button>
  );
}
```

**Accessibility**: Announce loading state to screen readers.

---

## Form & Input Interactions

### 2.1 Floating Label

**Effect**: Label floats up when input is focused or filled.

**Implementation**:
```css
.input-wrapper {
  position: relative;
  margin: 1rem 0;
}

.input-field {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
}

.input-label {
  position: absolute;
  left: 1rem;
  top: 1rem;
  pointer-events: none;
  transition: all 0.2s ease;
  color: #666;
}

.input-field:focus + .input-label,
.input-field:not(:placeholder-shown) + .input-label {
  top: -0.5rem;
  left: 0.75rem;
  font-size: 0.75rem;
  background: white;
  padding: 0 0.25rem;
  color: #3b82f6;
}
```

**HTML**:
```html
<div class="input-wrapper">
  <input
    class="input-field"
    type="text"
    placeholder=" "
    required
  />
  <label class="input-label">Email address</label>
</div>
```

---

### 2.2 Input Validation Feedback

**Effect**: Instant feedback on validation state.

**React + Framer Motion**:
```jsx
function ValidatedInput({ label, validator }) {
  const [value, setValue] = useState('');
  const [isValid, setIsValid] = useState(null);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
    setIsValid(validator(newValue));
  };

  return (
    <div className="input-wrapper">
      <motion.input
        value={value}
        onChange={handleChange}
        animate={{
          borderColor: isValid === null ? '#ccc' :
                      isValid ? '#10b981' : '#ef4444'
        }}
        transition={{ duration: 0.2 }}
      />

      <AnimatePresence>
        {isValid === true && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="success-icon"
          >
            ✓
          </motion.div>
        )}

        {isValid === false && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="error-icon"
          >
            ✗
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

**Accessibility**: Provide error messages, not just icons.

---

### 2.3 Password Strength Indicator

**Effect**: Visual indicator of password strength.

**Implementation**:
```jsx
function PasswordStrengthIndicator({ password }) {
  const strength = calculateStrength(password);

  const variants = {
    weak: { width: '33%', backgroundColor: '#ef4444' },
    medium: { width: '66%', backgroundColor: '#f59e0b' },
    strong: { width: '100%', backgroundColor: '#10b981' }
  };

  return (
    <div className="strength-bar-container">
      <motion.div
        className="strength-bar"
        variants={variants}
        animate={strength}
        transition={{ duration: 0.3 }}
      />
      <p className="strength-label">
        Password strength: <strong>{strength}</strong>
      </p>
    </div>
  );
}

function calculateStrength(password) {
  if (password.length < 6) return 'weak';
  if (password.length < 10) return 'medium';
  return 'strong';
}
```

---

### 2.4 Character Count with Progress

**Effect**: Shows remaining characters with visual indicator.

**Implementation**:
```jsx
function TextareaWithCount({ maxLength = 280 }) {
  const [text, setText] = useState('');
  const remaining = maxLength - text.length;
  const percentage = (text.length / maxLength) * 100;

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxLength={maxLength}
      />

      <div className="count-indicator">
        <motion.svg
          width="40"
          height="40"
          style={{ transform: 'rotate(-90deg)' }}
        >
          <circle
            cx="20"
            cy="20"
            r="16"
            stroke="#e5e7eb"
            strokeWidth="3"
            fill="none"
          />
          <motion.circle
            cx="20"
            cy="20"
            r="16"
            stroke={remaining < 20 ? '#ef4444' : '#3b82f6'}
            strokeWidth="3"
            fill="none"
            strokeDasharray={`${2 * Math.PI * 16}`}
            animate={{
              strokeDashoffset: (1 - percentage / 100) * (2 * Math.PI * 16)
            }}
          />
        </motion.svg>
        <span className="count-text">{remaining}</span>
      </div>
    </div>
  );
}
```

---

## Loading States

### 3.1 Skeleton Screen

**Effect**: Content placeholder that mimics layout.

**Implementation**:
```css
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text {
  height: 1rem;
  margin-bottom: 0.5rem;
}

.skeleton-title {
  height: 2rem;
  width: 60%;
  margin-bottom: 1rem;
}

.skeleton-image {
  width: 100%;
  aspect-ratio: 16 / 9;
}
```

**React Component**:
```jsx
function SkeletonCard() {
  return (
    <div className="card">
      <div className="skeleton skeleton-image" />
      <div className="skeleton skeleton-title" />
      <div className="skeleton skeleton-text" />
      <div className="skeleton skeleton-text" style={{ width: '80%' }} />
    </div>
  );
}
```

---

### 3.2 Progress Bar

**Effect**: Linear progress indicator.

**Framer Motion**:
```jsx
function ProgressBar({ progress }) {
  return (
    <div className="progress-container">
      <motion.div
        className="progress-bar"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />
    </div>
  );
}
```

**CSS**:
```css
.progress-container {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 9999px;
}
```

---

### 3.3 Spinner

**Effect**: Rotating loading indicator.

**CSS**:
```css
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(59, 130, 246, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**Framer Motion (Advanced)**:
```jsx
function Spinner() {
  return (
    <motion.div
      className="spinner-container"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
    >
      <motion.div
        className="spinner"
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      />
    </motion.div>
  );
}
```

---

## Navigation Interactions

### 4.1 Hamburger Menu Animation

**Effect**: Hamburger transforms into X on click.

**CSS**:
```css
.hamburger {
  width: 30px;
  height: 20px;
  position: relative;
  cursor: pointer;
}

.hamburger span {
  display: block;
  position: absolute;
  height: 3px;
  width: 100%;
  background: #333;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.hamburger span:nth-child(1) { top: 0; }
.hamburger span:nth-child(2) { top: 50%; transform: translateY(-50%); }
.hamburger span:nth-child(3) { bottom: 0; }

.hamburger.active span:nth-child(1) {
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  bottom: 50%;
  transform: translateY(50%) rotate(-45deg);
}
```

---

### 4.2 Dropdown Menu Reveal

**Effect**: Dropdown slides down with stagger.

**Framer Motion**:
```jsx
const menuVariants = {
  closed: {
    opacity: 0,
    y: -20,
    transition: { staggerChildren: 0.05, staggerDirection: -1 }
  },
  open: {
    opacity: 1,
    y: 0,
    transition: { staggerChildren: 0.07, delayChildren: 0.1 }
  }
};

const itemVariants = {
  closed: { opacity: 0, x: -20 },
  open: { opacity: 1, x: 0 }
};

function DropdownMenu({ isOpen }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.ul
          className="dropdown"
          variants={menuVariants}
          initial="closed"
          animate="open"
          exit="closed"
        >
          {items.map((item) => (
            <motion.li key={item} variants={itemVariants}>
              {item}
            </motion.li>
          ))}
        </motion.ul>
      )}
    </AnimatePresence>
  );
}
```

---

### 4.3 Active Link Indicator

**Effect**: Animated underline follows active link.

**Framer Motion**:
```jsx
function TabNavigation() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <nav className="tabs">
      {tabs.map((tab, index) => (
        <button
          key={tab}
          onClick={() => setActiveTab(index)}
          className={activeTab === index ? 'active' : ''}
        >
          {tab}
          {activeTab === index && (
            <motion.div
              className="active-indicator"
              layoutId="activeTab"
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            />
          )}
        </button>
      ))}
    </nav>
  );
}
```

**CSS**:
```css
.tabs {
  display: flex;
  gap: 2rem;
  border-bottom: 2px solid #e5e7eb;
}

.tabs button {
  position: relative;
  padding: 1rem 0;
  background: none;
  border: none;
  cursor: pointer;
}

.active-indicator {
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #3b82f6;
}
```

---

## Hover Effects

### 5.1 Image Zoom on Hover

**Effect**: Image scales up slightly on hover.

**CSS**:
```css
.image-container {
  overflow: hidden;
  border-radius: 8px;
}

.image-container img {
  transition: transform 0.3s ease;
  display: block;
  width: 100%;
}

.image-container:hover img {
  transform: scale(1.05);
}
```

---

### 5.2 Tilt Effect

**Effect**: Card tilts based on mouse position.

**Vanilla-Tilt**:
```javascript
VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
  max: 15,
  speed: 400,
  glare: true,
  "max-glare": 0.3
});
```

**Manual Implementation**:
```javascript
const card = document.querySelector('.tilt-card');

card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const centerX = rect.width / 2;
  const centerY = rect.height / 2;

  const rotateX = (y - centerY) / 10;
  const rotateY = (centerX - x) / 10;

  card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});

card.addEventListener('mouseleave', () => {
  card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
});
```

---

### 5.3 Reveal on Hover

**Effect**: Content reveals on hover with slide/fade.

**CSS**:
```css
.card {
  position: relative;
  overflow: hidden;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(100%);
  transition: all 0.3s ease;
}

.card:hover .card-overlay {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Toggle & Switch Interactions

### 6.1 Toggle Switch

**Effect**: Smooth toggle with spring animation.

**Framer Motion**:
```jsx
function ToggleSwitch({ enabled, setEnabled }) {
  return (
    <motion.div
      className="switch"
      data-enabled={enabled}
      onClick={() => setEnabled(!enabled)}
      animate={{ backgroundColor: enabled ? '#3b82f6' : '#d1d5db' }}
    >
      <motion.div
        className="switch-handle"
        layout
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
        style={{ justifyContent: enabled ? 'flex-end' : 'flex-start' }}
      />
    </motion.div>
  );
}
```

**CSS**:
```css
.switch {
  width: 50px;
  height: 28px;
  border-radius: 14px;
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.switch-handle {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
```

---

## Card Interactions

### 7.1 Card Expand

**Effect**: Card expands to full screen on click.

**Framer Motion with `layout`**:
```jsx
function ExpandableCard() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      layout
      className={isExpanded ? 'card-expanded' : 'card'}
      onClick={() => setIsExpanded(!isExpanded)}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <motion.h2 layout="position">Title</motion.h2>
      <motion.p layout="position">Content</motion.p>

      {isExpanded && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          Additional content...
        </motion.div>
      )}
    </motion.div>
  );
}
```

---

## Scroll Interactions

### 8.1 Fade In on Scroll

**Effect**: Elements fade in as they enter viewport.

**Framer Motion + `useInView`**:
```jsx
function FadeInSection({ children }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6 }}
    >
      {children}
    </motion.div>
  );
}
```

---

### 8.2 Scroll Progress Indicator

**Effect**: Shows reading progress.

**Implementation**:
```jsx
function ScrollProgress() {
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const updateProgress = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.scrollY / scrollHeight) * 100;
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', updateProgress);
    return () => window.removeEventListener('scroll', updateProgress);
  }, []);

  return (
    <motion.div
      className="progress-bar"
      style={{ scaleX: scrollProgress / 100, transformOrigin: 'left' }}
    />
  );
}
```

---

## Modal & Dialog Interactions

### 9.1 Modal Fade & Scale

**Effect**: Modal fades in and scales up.

**Framer Motion**:
```jsx
function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="modal-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          <motion.div
            className="modal"
            initial={{ opacity: 0, scale: 0.8, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50 }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

**Accessibility**: Trap focus, close on Escape key, focus first element.

---

## Toast & Notification Interactions

### 10.1 Toast Notification

**Effect**: Toast slides in from top/bottom with auto-dismiss.

**Framer Motion**:
```jsx
function Toast({ message, type, onDismiss }) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <motion.div
      className={`toast toast-${type}`}
      initial={{ opacity: 0, y: -50, scale: 0.8 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.8 }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
    >
      {message}
      <button onClick={onDismiss}>×</button>
    </motion.div>
  );
}
```

---

## Accessibility Checklist

For all micro-interactions:

- [ ] **Respect `prefers-reduced-motion`**: Disable or simplify animations
- [ ] **Keyboard accessible**: All interactions work without mouse
- [ ] **Focus indicators**: Visible focus states
- [ ] **Screen reader friendly**: Announce state changes with `aria-live`
- [ ] **Touch targets**: Minimum 44x44px for mobile
- [ ] **Escape key**: Close modals/overlays
- [ ] **Loading states**: Indicate when actions are processing
- [ ] **Error states**: Clear error messages, not just visual indicators

---

## Performance Checklist

- [ ] **GPU-accelerated properties**: Use `transform` and `opacity` only
- [ ] **Avoid layout thrash**: Batch DOM reads/writes
- [ ] **RequestAnimationFrame**: For JavaScript animations
- [ ] **Will-change sparingly**: Only during active animations
- [ ] **Debounce scroll/resize**: Avoid excessive repaints
- [ ] **Lazy load**: Defer non-critical animations
- [ ] **Test on low-end devices**: Ensure 60 FPS

---

*This catalog is a living document. Patterns are updated based on modern web standards and user research.*
