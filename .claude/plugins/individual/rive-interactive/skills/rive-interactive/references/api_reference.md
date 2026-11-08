# Rive React API Reference

Complete API reference for `rive-react` library.

## Installation

```bash
npm install rive-react
```

## Hooks

### useRive

Main hook for initializing Rive animations.

```typescript
const { rive, RiveComponent } = useRive(options);
```

**Options**:
- `src` (string): Path to .riv file
- `riveFile` (File): Preloaded Rive file
- `artboard` (string): Artboard name
- `animations` (string | string[]): Animations to play
- `stateMachines` (string | string[]): State machines to activate
- `layout` (Layout): Fit and alignment options
- `autoplay` (boolean): Auto-play animations (default: true)
- `autoBind` (boolean): Auto-bind ViewModels (default: true)
- `automaticallyHandleEvents` (boolean): Handle Rive events
- `useOffscreenRenderer` (boolean): Use off-screen renderer
- `shouldResizeCanvasToContainer` (boolean): Auto-resize canvas

### useStateMachineInput

Get state machine input reference.

```typescript
const input = useStateMachineInput(rive, stateMachineName, inputName, initialValue);
```

**Input Types**:
- Boolean: `input.value = true/false`
- Number: `input.value = 50`
- Trigger: `input.fire()`

### useViewModel

Get ViewModel reference.

```typescript
const viewModel = useViewModel(rive, { name: 'ViewModelName' });
// Or use default ViewModel
const viewModel = useViewModel(rive, { useDefault: true });
```

### useViewModelInstance

Get or create ViewModel instance.

```typescript
// Get default instance
const instance = useViewModelInstance(viewModel, { rive });

// Get named instance
const instance = useViewModelInstance(viewModel, { name: 'Instance1' });

// Create new instance
const instance = useViewModelInstance(viewModel, { useNew: true, rive });
```

### useViewModelInstanceString

Bind string property.

```typescript
const { value, setValue } = useViewModelInstanceString('propertyName', instance);
```

### useViewModelInstanceNumber

Bind number property.

```typescript
const { value, setValue } = useViewModelInstanceNumber('propertyName', instance);
```

### useViewModelInstanceColor

Bind color property (hex number).

```typescript
const { value, setValue } = useViewModelInstanceColor('propertyName', instance);

// Set color
setValue(0xff6b6b); // Hex number, no #
```

### useViewModelInstanceEnum

Bind enum property.

```typescript
const { value, setValue } = useViewModelInstanceEnum('propertyName', instance);
```

### useViewModelInstanceTrigger

Fire or listen to trigger events.

```typescript
// Fire trigger
const { trigger } = useViewModelInstanceTrigger('triggerName', instance);
trigger();

// Listen to trigger
useViewModelInstanceTrigger('triggerName', instance, {
  onTrigger: () => console.log('Triggered!')
});
```

### useRiveFile

Preload Rive file.

```typescript
const { riveFile, status } = useRiveFile({ src: 'animation.riv' });
// status: 'loading' | 'success' | 'failed'
```

## Components

### Rive Component

Declarative component for simple use cases.

```jsx
import Rive from 'rive-react';

<Rive
  src="animation.riv"
  artboard="Main"
  animations="idle"
  stateMachines="State Machine 1"
  layout={{ fit: "contain", alignment: "center" }}
  useOffscreenRenderer={true}
  shouldResizeCanvasToContainer={true}
  automaticallyHandleEvents={false}
  style={{ width: '400px', height: '400px' }}
/>
```

### RiveComponent (from useRive)

Component returned by useRive hook.

```jsx
const { RiveComponent } = useRive({ src: 'animation.riv' });

<RiveComponent style={{ width: '400px', height: '400px' }} />
```

## Events

### EventType

```typescript
import { EventType } from 'rive-react';

EventType.Load          // Rive file loaded
EventType.Play          // Animation started
EventType.Pause         // Animation paused
EventType.Stop          // Animation stopped
EventType.Loop          // Animation looped
EventType.Draw          // Frame drawn
EventType.RiveEvent     // Custom Rive event
```

### RiveEventType

```typescript
import { RiveEventType } from 'rive-react';

RiveEventType.General   // General custom event
RiveEventType.OpenUrl   // Open URL event
```

### Event Listening

```jsx
useEffect(() => {
  if (!rive) return;

  const onRiveEvent = (event) => {
    const eventData = event.data;

    if (eventData.type === RiveEventType.General) {
      console.log('Event:', eventData.name);
      console.log('Properties:', eventData.properties);
    }
  };

  rive.on(EventType.RiveEvent, onRiveEvent);

  return () => {
    rive.off(EventType.RiveEvent, onRiveEvent);
  };
}, [rive]);
```

## Layout Options

```typescript
interface Layout {
  fit?: 'contain' | 'cover' | 'fill' | 'fitWidth' | 'fitHeight' | 'none' | 'scaleDown';
  alignment?: 'center' | 'topLeft' | 'topCenter' | 'topRight' | 'centerLeft' |
              'centerRight' | 'bottomLeft' | 'bottomCenter' | 'bottomRight';
}
```

## Rive Instance Methods

From `useRive` hook:

```typescript
rive.play()                          // Play animation
rive.pause()                         // Pause animation
rive.stop()                          // Stop animation
rive.reset()                         // Reset animation
rive.cleanup()                       // Cleanup resources
rive.resizeDrawingSurfaceToCanvas()  // Resize canvas
```

## TypeScript Support

```typescript
import { useRive, useStateMachineInput, Layout } from 'rive-react';

interface Props {
  animationSrc: string;
}

const MyComponent: React.FC<Props> = ({ animationSrc }) => {
  const { rive, RiveComponent } = useRive({
    src: animationSrc,
    autoplay: true,
  });

  const hoverInput = useStateMachineInput(
    rive,
    'State Machine',
    'isHovered',
    false
  );

  return <RiveComponent />;
};
```

## Common Patterns

### Dynamic Animation Switching

```jsx
const [animation, setAnimation] = useState('idle');

const { RiveComponent } = useRive({
  src: 'character.riv',
  animations: animation,
  autoplay: true,
});

// Change animation
<button onClick={() => setAnimation('walk')}>Walk</button>
```

### Multiple State Machines

```jsx
const { rive, RiveComponent } = useRive({
  src: 'animation.riv',
  stateMachines: ['State Machine 1', 'State Machine 2'],
  autoplay: true,
});
```

### Responsive Layout

```jsx
const layout = {
  fit: window.innerWidth < 768 ? 'fitWidth' : 'contain',
  alignment: 'center'
};

<Rive src="animation.riv" layout={layout} />
```

## Error Handling

```jsx
const { rive, RiveComponent } = useRive({
  src: 'animation.riv',
  autoplay: true,
});

if (!rive) {
  return <div>Loading animation...</div>;
}

return <RiveComponent />;
```

## Performance Tips

1. **Use Off-Screen Renderer**:
   ```jsx
   <Rive useOffscreenRenderer={true} />
   ```

2. **Preload Files**:
   ```jsx
   const { riveFile } = useRiveFile({ src: 'animation.riv' });
   ```

3. **Disable Auto-Resize**:
   ```jsx
   <Rive shouldResizeCanvasToContainer={false} />
   ```

4. **Manual Event Handling**:
   ```jsx
   <Rive automaticallyHandleEvents={false} />
   ```
