---
name: rive-interactive
description: State machine-based vector animation with runtime interactivity and web integration. Use this skill when creating interactive animations, state-driven UI, animated components with logic, or designer-created animations with runtime control. Triggers on tasks involving Rive, state machines, interactive vector animations, animation with input handling, ViewModel data binding, or React Rive integration. Alternative to Lottie for animations requiring state machines and two-way interactivity.
---

# Rive Interactive - State Machine-Based Vector Animation

## Overview

Rive is a state machine-based animation platform that enables designers to create interactive vector animations with complex logic and runtime interactivity. Unlike timeline-only animation tools (like Lottie), Rive supports state machines, input handling, and two-way data binding between application code and animations.

**Key Features**:
- State machine system for complex interactive logic
- ViewModel API for two-way data binding
- Input handling (boolean, number, trigger inputs)
- Custom events for animation-to-code communication
- Runtime property control (colors, strings, numbers, enums)
- Cross-platform support (Web, React, React Native, iOS, Android, Flutter)
- Small file sizes with vector graphics

**When to Use This Skill**:
- Creating UI animations with complex state transitions
- Building interactive animated components (buttons, toggles, loaders)
- Implementing game-like UI with state-driven animations
- Binding real-time data to animated visualizations
- Creating animations that respond to user input
- Working with designer-created animations requiring runtime control

**Alternatives**:
- **Lottie** (lottie-animations): For simpler timeline-based animations without state machines
- **Framer Motion** (motion-framer): For code-first React animations with spring physics
- **GSAP** (gsap-scrolltrigger): For timeline-based web animations with precise control

## Core Concepts

### 1. State Machines

State machines define animation behavior with states and transitions:
- **States**: Different animation states (e.g., idle, hover, pressed)
- **Inputs**: Variables that control transitions (boolean, number, trigger)
- **Transitions**: Rules for moving between states
- **Listeners**: React hooks to respond to state changes

### 2. Inputs

Three input types control state machine behavior:
- **Boolean**: On/off states (e.g., isHovered, isActive)
- **Number**: Numeric values (e.g., progress, volume)
- **Trigger**: One-time events (e.g., click, submit)

### 3. ViewModels

Data binding system for dynamic properties:
- **String Properties**: Text content (e.g., username, title)
- **Number Properties**: Numeric data (e.g., stock price, score)
- **Color Properties**: Dynamic colors (hex values)
- **Enum Properties**: Selection from predefined options
- **Trigger Properties**: Animation events

### 4. Events

Custom events emitted from animations:
- **General Events**: Custom named events
- **Event Properties**: Data attached to events
- **Event Listeners**: React hooks to handle events

## Common Patterns

### Pattern 1: Basic Rive Animation

**Use Case**: Display a simple Rive animation in React

**Implementation**:

```bash
# Installation
npm install rive-react
```

```jsx
import Rive from 'rive-react';

export default function SimpleAnimation() {
  return (
    <Rive
      src="animation.riv"
      artboard="Main"
      animations="idle"
      layout={{ fit: "contain", alignment: "center" }}
      style={{ width: '400px', height: '400px' }}
    />
  );
}
```

**Key Points**:
- `src`: Path to .riv file
- `artboard`: Which artboard to display
- `animations`: Which animation timeline to play
- `layout`: How animation fits in container

### Pattern 2: State Machine Control with Inputs

**Use Case**: Control animation states based on user interaction

**Implementation**:

```jsx
import { useRive, useStateMachineInput } from 'rive-react';

export default function InteractiveButton() {
  const { rive, RiveComponent } = useRive({
    src: 'button.riv',
    stateMachines: 'Button State Machine',
    autoplay: true,
  });

  // Get state machine inputs
  const hoverInput = useStateMachineInput(
    rive,
    'Button State Machine',
    'isHovered',
    false
  );

  const clickInput = useStateMachineInput(
    rive,
    'Button State Machine',
    'isClicked',
    false
  );

  return (
    <div
      onMouseEnter={() => hoverInput && (hoverInput.value = true)}
      onMouseLeave={() => hoverInput && (hoverInput.value = false)}
      onClick={() => clickInput && clickInput.fire()} // Trigger input
      style={{ cursor: 'pointer' }}
    >
      <RiveComponent style={{ width: '200px', height: '100px' }} />
    </div>
  );
}
```

**Input Types**:
- Boolean: `input.value = true/false`
- Number: `input.value = 50`
- Trigger: `input.fire()`

### Pattern 3: ViewModel Data Binding

**Use Case**: Bind application data to animation properties

**Implementation**:

```jsx
import { useRive, useViewModel, useViewModelInstance,
         useViewModelInstanceString, useViewModelInstanceNumber } from 'rive-react';
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stockPrice, setStockPrice] = useState(150.0);

  const { rive, RiveComponent } = useRive({
    src: 'dashboard.riv',
    autoplay: true,
    autoBind: false, // Manual binding for ViewModels
  });

  // Get ViewModel and instance
  const viewModel = useViewModel(rive, { name: 'Dashboard' });
  const viewModelInstance = useViewModelInstance(viewModel, { rive });

  // Bind properties
  const { setValue: setTitle } = useViewModelInstanceString(
    'title',
    viewModelInstance
  );

  const { setValue: setPrice } = useViewModelInstanceNumber(
    'stockPrice',
    viewModelInstance
  );

  useEffect(() => {
    if (setTitle) setTitle('Stock Dashboard');
  }, [setTitle]);

  useEffect(() => {
    if (setPrice) setPrice(stockPrice);
  }, [setPrice, stockPrice]);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setStockPrice((prev) => prev + (Math.random() - 0.5) * 10);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <RiveComponent style={{ width: '800px', height: '600px' }} />;
}
```

**ViewModel Property Hooks**:
- `useViewModelInstanceString` - Text properties
- `useViewModelInstanceNumber` - Numeric properties
- `useViewModelInstanceColor` - Color properties (hex)
- `useViewModelInstanceEnum` - Enum selection
- `useViewModelInstanceTrigger` - Animation triggers

### Pattern 4: Handling Rive Events

**Use Case**: React to events emitted from Rive animation

**Implementation**:

```jsx
import { useRive, EventType, RiveEventType } from 'rive-react';
import { useEffect } from 'react';

export default function InteractiveRating() {
  const { rive, RiveComponent } = useRive({
    src: 'rating.riv',
    stateMachines: 'State Machine 1',
    autoplay: true,
    automaticallyHandleEvents: true,
  });

  useEffect(() => {
    if (!rive) return;

    const onRiveEvent = (event) => {
      const eventData = event.data;

      if (eventData.type === RiveEventType.General) {
        console.log('Event:', eventData.name);

        // Access event properties
        const rating = eventData.properties.rating;
        const message = eventData.properties.message;

        if (rating >= 4) {
          alert(`Thanks for ${rating} stars: ${message}`);
        }
      }
    };

    rive.on(EventType.RiveEvent, onRiveEvent);

    return () => {
      rive.off(EventType.RiveEvent, onRiveEvent);
    };
  }, [rive]);

  return <RiveComponent style={{ width: '400px', height: '300px' }} />;
}
```

### Pattern 5: Preloading Rive Files

**Use Case**: Optimize load times by preloading animations

**Implementation**:

```jsx
import { useRiveFile, useRive } from 'rive-react';

export default function PreloadedAnimation() {
  const { riveFile, status } = useRiveFile({
    src: 'large-animation.riv',
  });

  const { RiveComponent } = useRive({
    riveFile: riveFile,
    artboard: 'Main',
    autoplay: true,
  });

  if (status === 'loading') {
    return <div>Loading animation...</div>;
  }

  if (status === 'failed') {
    return <div>Failed to load animation</div>;
  }

  return <RiveComponent style={{ width: '600px', height: '400px' }} />;
}
```

### Pattern 6: Controlled Animation with Refs

**Use Case**: Control animation from parent component

**Implementation**:

```jsx
import { useRive, useViewModel, useViewModelInstance,
         useViewModelInstanceTrigger } from 'rive-react';
import { useImperativeHandle, forwardRef } from 'react';

const AnimatedComponent = forwardRef((props, ref) => {
  const { rive, RiveComponent } = useRive({
    src: 'logo.riv',
    autoplay: true,
    autoBind: false,
  });

  const viewModel = useViewModel(rive, { useDefault: true });
  const viewModelInstance = useViewModelInstance(viewModel, { rive });

  const { trigger: spinTrigger } = useViewModelInstanceTrigger(
    'triggerSpin',
    viewModelInstance
  );

  // Expose methods to parent
  useImperativeHandle(ref, () => ({
    spin: () => spinTrigger && spinTrigger(),
    pause: () => rive && rive.pause(),
    play: () => rive && rive.play(),
  }));

  return <RiveComponent style={{ width: '200px', height: '200px' }} />;
});

export default function App() {
  const animationRef = useRef();

  return (
    <div>
      <AnimatedComponent ref={animationRef} />
      <button onClick={() => animationRef.current?.spin()}>Spin</button>
      <button onClick={() => animationRef.current?.pause()}>Pause</button>
    </div>
  );
}
```

### Pattern 7: Multi-Property ViewModel Updates

**Use Case**: Update multiple animation properties from complex data

**Implementation**:

```jsx
import { useRive, useViewModel, useViewModelInstance,
         useViewModelInstanceString, useViewModelInstanceNumber,
         useViewModelInstanceColor } from 'rive-react';
import { useEffect } from 'react';

export default function UserProfile({ user }) {
  const { rive, RiveComponent } = useRive({
    src: 'profile.riv',
    autoplay: true,
    autoBind: false,
  });

  const viewModel = useViewModel(rive, { useDefault: true });
  const viewModelInstance = useViewModelInstance(viewModel, { rive });

  // Bind all properties
  const { setValue: setName } = useViewModelInstanceString('name', viewModelInstance);
  const { setValue: setScore } = useViewModelInstanceNumber('score', viewModelInstance);
  const { setValue: setColor } = useViewModelInstanceColor('avatarColor', viewModelInstance);

  useEffect(() => {
    if (user && setName && setScore && setColor) {
      setName(user.name);
      setScore(user.score);
      setColor(parseInt(user.color.substring(1), 16)); // Convert hex to number
    }
  }, [user, setName, setScore, setColor]);

  return <RiveComponent style={{ width: '300px', height: '300px' }} />;
}
```

## Integration Patterns

### With Framer Motion (motion-framer)

Animate container while Rive handles interactive content:

```jsx
import { motion } from 'framer-motion';
import Rive from 'rive-react';

export default function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.05 }}
    >
      <Rive
        src="card.riv"
        stateMachines="Card State Machine"
        style={{ width: '300px', height: '400px' }}
      />
    </motion.div>
  );
}
```

### With GSAP ScrollTrigger (gsap-scrolltrigger)

Trigger Rive animations on scroll:

```jsx
import { useRive, useStateMachineInput } from 'rive-react';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function ScrollRive() {
  const containerRef = useRef();
  const { rive, RiveComponent } = useRive({
    src: 'scroll-animation.riv',
    stateMachines: 'State Machine 1',
    autoplay: true,
  });

  const trigger = useStateMachineInput(rive, 'State Machine 1', 'trigger');

  useEffect(() => {
    if (!trigger) return;

    ScrollTrigger.create({
      trigger: containerRef.current,
      start: 'top center',
      onEnter: () => trigger.fire(),
    });
  }, [trigger]);

  return (
    <div ref={containerRef}>
      <RiveComponent style={{ width: '100%', height: '600px' }} />
    </div>
  );
}
```

## Performance Optimization

### 1. Use Off-Screen Renderer

```jsx
<Rive
  src="animation.riv"
  useOffscreenRenderer={true} // Better performance
/>
```

### 2. Optimize Rive Files

**In Rive Editor**:
- Keep artboards under 2MB
- Use vector graphics (avoid raster images when possible)
- Minimize number of bones in skeletal animations
- Reduce complexity of state machines

### 3. Preload Critical Animations

```jsx
const { riveFile } = useRiveFile({ src: 'critical.riv' });
// Preload during app initialization
```

### 4. Disable Automatic Event Handling

```jsx
<Rive
  src="animation.riv"
  automaticallyHandleEvents={false} // Manual control
/>
```

## Common Pitfalls and Solutions

### Pitfall 1: State Machine Input Not Found

**Problem**: `useStateMachineInput` returns null

**Solution**:
```jsx
// ❌ Wrong: Incorrect input name
const input = useStateMachineInput(rive, 'State Machine', 'wrongName');

// ✅ Correct: Match exact name from Rive editor
const input = useStateMachineInput(rive, 'State Machine', 'isHovered');

// Always check if input exists before using
if (input) {
  input.value = true;
}
```

### Pitfall 2: ViewModel Property Not Updating

**Problem**: ViewModel property doesn't update animation

**Solution**:
```jsx
// ❌ Wrong: autoBind enabled
const { rive } = useRive({
  src: 'dashboard.riv',
  autoplay: true,
  // autoBind: true (default)
});

// ✅ Correct: Disable autoBind for ViewModels
const { rive } = useRive({
  src: 'dashboard.riv',
  autoplay: true,
  autoBind: false, // Required for manual ViewModel control
});
```

### Pitfall 3: Event Listener Not Firing

**Problem**: Rive events not triggering callback

**Solution**:
```jsx
// ❌ Wrong: Missing automaticallyHandleEvents
const { rive } = useRive({
  src: 'rating.riv',
  stateMachines: 'State Machine 1',
  autoplay: true,
});

// ✅ Correct: Enable event handling
const { rive } = useRive({
  src: 'rating.riv',
  stateMachines: 'State Machine 1',
  autoplay: true,
  automaticallyHandleEvents: true, // Required for events
});
```

## Resources

### Official Documentation
- **Rive Docs**: https://rive.app/docs
- **React Rive GitHub**: https://github.com/rive-app/rive-react
- **Rive Community**: https://rive.app/community

### Rive Editor
- **Web Editor**: https://rive.app/community
- **Desktop App**: Available for macOS, Windows

### Learning Resources
- **Tutorials**: https://rive.app/learn
- **Examples**: https://rive.app/community/files
- **State Machine Guide**: https://rive.app/docs/state-machine

## Related Skills

- **lottie-animations**: For simpler timeline-based animations without state machines
- **motion-framer**: For code-first React animations with gestures
- **gsap-scrolltrigger**: For scroll-driven animations
- **spline-interactive**: For 3D interactive animations

## Scripts

This skill includes utility scripts:
- `component_generator.py` - Generate Rive React component boilerplate
- `viewmodel_builder.py` - Build ViewModel property bindings

Run scripts from the skill directory:
```bash
./scripts/component_generator.py
./scripts/viewmodel_builder.py
```

## Assets

Starter templates and examples:
- `starter_rive/` - Complete React + Rive template
- `examples/` - Real-world integration patterns
