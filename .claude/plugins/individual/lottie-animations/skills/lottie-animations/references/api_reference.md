# Lottie API Reference

Complete API documentation for lottie-web, lottie-react, dotlottie-web, and dotlottie-react libraries.

## dotlottie-web API

### DotLottie Constructor

```javascript
import { DotLottie } from '@lottiefiles/dotlottie-web';

const dotLottie = new DotLottie(config);
```

**Config Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `canvas` | HTMLCanvasElement | **required** | The canvas element to render the animation |
| `src` | string | **required** | URL to .lottie or .json file |
| `autoplay` | boolean | `true` | Auto-start animation on load |
| `loop` | boolean | `true` | Loop animation continuously |
| `speed` | number | `1.0` | Playback speed multiplier (0.5 = half speed, 2 = double speed) |
| `mode` | string | `'forward'` | Playback mode: `'forward'`, `'reverse'`, `'bounce'`, `'reverse-bounce'` |
| `backgroundColor` | string | `null` | Canvas background color |
| `renderConfig` | object | `{}` | Rendering configuration |
| `data` | string \| ArrayBuffer | `null` | Inline animation data (alternative to src) |
| `marker` | string | `null` | Named marker to play |
| `segment` | [number, number] | `null` | Frame range to play [startFrame, endFrame] |
| `useFrameInterpolation` | boolean | `true` | Smooth frame transitions |

**Render Config Options:**

```javascript
renderConfig: {
  devicePixelRatio: window.devicePixelRatio || 1, // Pixel density
  freezeOnOffscreen: false, // Pause when not visible
  imageRendering: 'auto' // 'auto', 'crisp-edges', 'pixelated'
}
```

### DotLottie Methods

**Playback Control:**

```javascript
dotLottie.play();              // Play animation
dotLottie.pause();             // Pause animation
dotLottie.stop();              // Stop and reset to frame 0
dotLottie.setSpeed(speed);     // Set playback speed (e.g., 2 for double speed)
dotLottie.setLoop(loop);       // Enable/disable looping
dotLottie.setMode(mode);       // Set playback mode ('forward', 'reverse', 'bounce')
```

**Frame Navigation:**

```javascript
dotLottie.setFrame(frame);               // Seek to specific frame (0-indexed)
dotLottie.goToAndPlay(frame, isFrame);   // Jump to frame/time and play
dotLottie.goToAndStop(frame, isFrame);   // Jump to frame/time and stop
dotLottie.playSegments(segments, forceFlag); // Play frame range
```

**Animation Management:**

```javascript
dotLottie.loadAnimation(animationId);    // Load specific animation (multi-animation files)
dotLottie.setTheme(themeId);             // Set theme (multi-theme files)
dotLottie.resize();                      // Resize to canvas dimensions
dotLottie.destroy();                     // Cleanup and destroy instance
```

**State Machine (Interactive Lottie):**

```javascript
dotLottie.loadStateMachine(stateMachineId); // Load state machine
dotLottie.startStateMachine();              // Start state machine
dotLottie.stopStateMachine();               // Stop state machine
dotLottie.postStateMachineEvent(event);     // Post event to state machine
```

**State Machine Events:**

```javascript
dotLottie.postStateMachineEvent("Bool: true");
dotLottie.postStateMachineEvent("Bool: false");
dotLottie.postStateMachineEvent("String: example");
dotLottie.postStateMachineEvent("Numeric: 42.5");
dotLottie.postStateMachineEvent("OnPointerDown: 100 200");  // x, y
dotLottie.postStateMachineEvent("OnPointerUp: 100 200");
dotLottie.postStateMachineEvent("OnPointerMove: 100 200");
dotLottie.postStateMachineEvent("OnPointerEnter: 100 200");
dotLottie.postStateMachineEvent("OnPointerExit: 100 200");
dotLottie.postStateMachineEvent("OnComplete");
```

**Layer Information:**

```javascript
const boundingBox = dotLottie.getLayerBoundingBox(layerName);
// Returns: { x, y, width, height } or null
```

### DotLottie Properties

```javascript
dotLottie.currentFrame;          // Current frame number (read-only)
dotLottie.totalFrames;           // Total number of frames (read-only)
dotLottie.duration;              // Animation duration in seconds (read-only)
dotLottie.isPlaying;             // Boolean: is currently playing (read-only)
dotLottie.isLoaded;              // Boolean: animation loaded (read-only)
dotLottie.manifest;              // Manifest object (animations, themes) (read-only)
dotLottie.activeAnimationId;     // Current animation ID (read-only)
dotLottie.activeThemeId;         // Current theme ID (read-only)
```

### DotLottie Events

```javascript
// Add event listeners
dotLottie.addEventListener('load', onLoad);
dotLottie.addEventListener('play', onPlay);
dotLottie.addEventListener('pause', onPause);
dotLottie.addEventListener('stop', onStop);
dotLottie.addEventListener('complete', onComplete);
dotLottie.addEventListener('loopComplete', onLoopComplete);
dotLottie.addEventListener('frame', onFrame);
dotLottie.addEventListener('render', onRender);
dotLottie.addEventListener('destroy', onDestroy);

// Remove event listeners
dotLottie.removeEventListener('load', onLoad);
```

**Event Callbacks:**

```javascript
function onLoad() {
  console.log('Animation loaded');
}

function onPlay() {
  console.log('Animation started');
}

function onPause() {
  console.log('Animation paused');
}

function onStop() {
  console.log('Animation stopped');
}

function onComplete() {
  console.log('Animation completed');
}

function onLoopComplete() {
  console.log('Loop completed');
}

function onFrame({ currentFrame }) {
  console.log('Current frame:', currentFrame);
}

function onRender() {
  console.log('Frame rendered');
}

function onDestroy() {
  console.log('Instance destroyed');
}
```

---

## DotLottieWorker API

**Purpose:** Offload animation rendering to a Web Worker for better performance.

```javascript
import { DotLottieWorker } from '@lottiefiles/dotlottie-web';

new DotLottieWorker({
  canvas: document.getElementById('canvas'),
  src: 'animation.lottie',
  autoplay: true,
  loop: true,
  workerId: 'worker-1' // Optional: group multiple animations by worker
});
```

**Config:** Same as `DotLottie`, plus:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `workerId` | string | auto-generated | Worker ID for grouping animations |

**Use Case:** Complex animations that cause main thread lag.

---

## dotlottie-react API

### DotLottieReact Component

```jsx
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

<DotLottieReact
  src="animation.lottie"
  loop
  autoplay
  speed={1}
  mode="forward"
  backgroundColor="#ffffff"
  style={{ height: 400, width: 400 }}
  className="lottie-animation"
  dotLottieRefCallback={(instance) => setDotLottie(instance)}
  animationId="animation-1"
  themeId="light"
  marker="intro"
  segment={[0, 60]}
  useFrameInterpolation
  data={inlineData}
  renderConfig={{ devicePixelRatio: 2 }}
/>
```

**Props:**

All `DotLottie` config options are available as props, plus:

| Prop | Type | Description |
|------|------|-------------|
| `dotLottieRefCallback` | function | Callback to get dotLottie instance |
| `style` | object | Inline styles for wrapper div |
| `className` | string | CSS class for wrapper div |

**Getting Instance Reference:**

```jsx
const [dotLottie, setDotLottie] = useState(null);

<DotLottieReact
  src="animation.lottie"
  dotLottieRefCallback={setDotLottie}
/>

// Use instance
useEffect(() => {
  if (dotLottie) {
    dotLottie.play();
  }
}, [dotLottie]);
```

---

## lottie-web API (Original Library)

### lottie.loadAnimation()

```javascript
import lottie from 'lottie-web';

const animation = lottie.loadAnimation({
  container: document.getElementById('lottie-container'), // Required
  renderer: 'svg', // 'svg', 'canvas', 'html'
  loop: true,
  autoplay: true,
  path: 'animation.json', // URL to animation
  // OR
  animationData: jsonData, // Inline JSON data
  name: 'my-animation', // Optional name
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
    progressiveLoad: false,
    hideOnTransparent: true,
    className: 'lottie-svg', // SVG class
    scaleMode: 'noScale' // 'noScale', 'fill', 'fit'
  }
});
```

### lottie-web Methods

**Playback:**

```javascript
animation.play();
animation.pause();
animation.stop();
animation.setSpeed(speed);        // 1 = normal, 0.5 = half speed
animation.setDirection(direction); // 1 = forward, -1 = reverse
animation.goToAndPlay(frame, isFrame);
animation.goToAndStop(frame, isFrame);
animation.playSegments(segments, forceFlag);
```

**Segments:**

```javascript
// Play frames 0-30 only
animation.playSegments([0, 30], false);

// Play multiple segments
animation.playSegments([[0, 30], [60, 90]], false);
```

**Properties:**

```javascript
animation.totalFrames;
animation.currentFrame;
animation.frameRate;
animation.isLoaded;
animation.isPaused;
animation.renderer;    // 'svg', 'canvas', 'html'
animation.name;
```

**Utility:**

```javascript
animation.resize();
animation.setSubframe(useSubframes); // Smooth subframe rendering
animation.getDuration(inFrames);     // Duration in frames or seconds
animation.destroy();
```

### lottie-web Events

```javascript
animation.addEventListener('DOMLoaded', onDOMLoaded);
animation.addEventListener('data_ready', onDataReady);
animation.addEventListener('config_ready', onConfigReady);
animation.addEventListener('complete', onComplete);
animation.addEventListener('loopComplete', onLoopComplete);
animation.addEventListener('enterFrame', onEnterFrame);
animation.addEventListener('segmentStart', onSegmentStart);
animation.addEventListener('destroy', onDestroy);

animation.removeEventListener('complete', onComplete);
```

**Event Callbacks:**

```javascript
function onEnterFrame(event) {
  console.log('Current frame:', event.currentTime);
  console.log('Direction:', event.direction); // 1 or -1
}

function onLoopComplete(event) {
  console.log('Loop completed:', event.currentLoop);
}
```

### lottie Global Methods

```javascript
lottie.play(name);            // Play animation by name
lottie.pause(name);           // Pause animation by name
lottie.stop(name);            // Stop animation by name
lottie.setSpeed(speed, name); // Set speed for named animation
lottie.setDirection(direction, name);
lottie.destroy(name);         // Destroy animation by name
lottie.loadAnimation(config); // Load new animation
lottie.searchAnimations();    // Auto-detect and load animations
```

---

## lottie-react API

### Lottie Component

```jsx
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie
  animationData={animationData}  // Required
  loop={true}
  autoplay={true}
  initialSegment={[0, 60]}
  onComplete={onComplete}
  onLoopComplete={onLoopComplete}
  onEnterFrame={onEnterFrame}
  onSegmentStart={onSegmentStart}
  onConfigReady={onConfigReady}
  onDataReady={onDataReady}
  onDataFailed={onDataFailed}
  onLoadedImages={onLoadedImages}
  onDOMLoaded={onDOMLoaded}
  onDestroy={onDestroy}
  style={{ height: 400 }}
  className="lottie-animation"
  lottieRef={lottieRef}
  interactivity={interactivityConfig}
/>
```

**Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `animationData` | object | **required** | Lottie JSON data |
| `loop` | boolean \| number | `true` | Loop animation (true = infinite, number = loop count) |
| `autoplay` | boolean | `true` | Auto-start on load |
| `initialSegment` | [number, number] | `null` | Start frame range |
| `onComplete` | function | `null` | Callback on animation complete |
| `onLoopComplete` | function | `null` | Callback on loop complete |
| `onEnterFrame` | function | `null` | Callback on each frame |
| `onSegmentStart` | function | `null` | Callback on segment start |
| `onConfigReady` | function | `null` | Callback on config ready |
| `onDataReady` | function | `null` | Callback on data ready |
| `onDataFailed` | function | `null` | Callback on data load failure |
| `onLoadedImages` | function | `null` | Callback on images loaded |
| `onDOMLoaded` | function | `null` | Callback on DOM loaded |
| `onDestroy` | function | `null` | Callback on destroy |
| `style` | object | `{}` | Inline styles |
| `className` | string | `''` | CSS class |
| `lottieRef` | React.RefObject | `null` | Ref to lottie instance |
| `interactivity` | object | `null` | Interactivity config (scroll/cursor) |

### Using lottieRef

```jsx
const lottieRef = useRef();

<Lottie animationData={animationData} lottieRef={lottieRef} />

// Access instance
useEffect(() => {
  if (lottieRef.current) {
    lottieRef.current.setSpeed(2);
    lottieRef.current.goToAndPlay(30, true);
  }
}, []);
```

### Interactivity Config

**Scroll Mode:**

```javascript
const interactivity = {
  mode: 'scroll',
  actions: [
    {
      visibility: [0, 0.3],  // When 0-30% visible
      type: 'stop',
      frames: [0]
    },
    {
      visibility: [0.3, 1],  // When 30-100% visible
      type: 'seek',
      frames: [0, 60]
    }
  ]
};
```

**Cursor Mode:**

```javascript
const interactivity = {
  mode: 'cursor',
  actions: [
    {
      position: { x: [0, 1], y: [0, 1] }, // Inside container
      type: 'loop',
      frames: [0, 60]
    },
    {
      position: { x: -1, y: -1 }, // Outside container
      type: 'stop',
      frames: [0]
    }
  ]
};
```

**Action Types:**

- `'stop'` - Stop at specified frame
- `'play'` - Play from current frame
- `'loop'` - Loop specified segment
- `'seek'` - Scrub through frames based on scroll/cursor position

---

## useLottie Hook

```javascript
import { useLottie } from 'lottie-react';
import animationData from './animation.json';

const { View, play, pause, stop, setSpeed, goToAndPlay, goToAndStop } = useLottie({
  animationData: animationData,
  loop: true,
  autoplay: true,
  initialSegment: [0, 60]
}, style);
```

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `View` | React.Element | Rendered Lottie component |
| `play` | function | Play animation |
| `pause` | function | Pause animation |
| `stop` | function | Stop animation |
| `setSpeed` | function | Set playback speed |
| `setDirection` | function | Set direction (1 or -1) |
| `goToAndPlay` | function | Jump to frame and play |
| `goToAndStop` | function | Jump to frame and stop |
| `playSegments` | function | Play specific segments |
| `setSubframe` | function | Enable subframe rendering |
| `getDuration` | function | Get animation duration |
| `destroy` | function | Destroy instance |

---

## useLottieInteractivity Hook

```javascript
import { useLottie, useLottieInteractivity } from 'lottie-react';

const lottieObj = useLottie({ animationData });

const Animation = useLottieInteractivity({
  lottieObj,
  mode: 'scroll', // or 'cursor'
  actions: [
    {
      visibility: [0, 1],
      type: 'seek',
      frames: [0, 60]
    }
  ]
});

return Animation;
```

---

## Best Practices

1. **Always destroy instances on unmount:**
   ```javascript
   useEffect(() => {
     return () => {
       dotLottie?.destroy();
     };
   }, [dotLottie]);
   ```

2. **Use dotLottie format (.lottie) for production** - smaller file sizes

3. **Prefer Canvas renderer for complex animations** - better performance

4. **Use Web Workers (DotLottieWorker) for heavy animations** - offload from main thread

5. **Lazy load animations** - only load when visible (IntersectionObserver)

6. **Clean up event listeners:**
   ```javascript
   useEffect(() => {
     const handler = () => {};
     dotLottie?.addEventListener('complete', handler);
     return () => dotLottie?.removeEventListener('complete', handler);
   }, [dotLottie]);
   ```

7. **Use animationData prop (not path) for bundled animations** - faster, no network request
