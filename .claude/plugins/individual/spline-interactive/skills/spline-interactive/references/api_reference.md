# Spline React API Reference

Complete reference for `@splinetool/react-spline` and Spline Application API.

## Installation

```bash
npm install @splinetool/react-spline @splinetool/runtime
# or
yarn add @splinetool/react-spline @splinetool/runtime
```

## Spline Component

### Import

```jsx
// Standard React
import Spline from '@splinetool/react-spline';

// Next.js (with SSR support)
import Spline from '@splinetool/react-spline/next';
```

### Props

#### `scene` (required)
- **Type**: `string`
- **Description**: URL to the Spline scene file
- **Example**: `"https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode"`

#### `onLoad`
- **Type**: `(spline: Application) => void`
- **Description**: Called once the scene has loaded. Provides Spline Application instance
- **Example**:
  ```jsx
  function onLoad(spline) {
    console.log('Scene loaded', spline);
    const obj = spline.findObjectByName('Cube');
  }

  <Spline scene={sceneUrl} onLoad={onLoad} />
  ```

#### `renderOnDemand`
- **Type**: `boolean`
- **Default**: `true`
- **Description**: Enable on-demand rendering (only renders when scene changes)
- **Example**: `<Spline scene={sceneUrl} renderOnDemand={false} />`

#### `className`
- **Type**: `string`
- **Description**: CSS class name(s) for the canvas container
- **Example**: `<Spline scene={sceneUrl} className="my-scene" />`

#### `style`
- **Type**: `React.CSSProperties`
- **Description**: Inline CSS styles for the canvas container
- **Example**: `<Spline scene={sceneUrl} style={{ width: '100%', height: '600px' }} />`

#### `id`
- **Type**: `string`
- **Description**: HTML id attribute for the canvas element
- **Example**: `<Spline scene={sceneUrl} id="main-scene" />`

#### `ref`
- **Type**: `React.Ref<HTMLDivElement>`
- **Description**: React ref pointing to the container div element
- **Example**:
  ```jsx
  const containerRef = useRef();
  <Spline scene={sceneUrl} ref={containerRef} />
  ```

### Event Handler Props

#### `onSplineMouseDown`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when mouse button is pressed on an object
- **Event Object**:
  - `e.target` - The object that was clicked (contains name, id, position, rotation, scale)
  - `e.target.name` - Object name from Spline editor
  - `e.target.id` - Object UUID
- **Example**:
  ```jsx
  function onSplineMouseDown(e) {
    console.log('Clicked:', e.target.name);
    console.log('Position:', e.target.position);
  }
  ```

#### `onSplineMouseUp`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when mouse button is released
- **Example**:
  ```jsx
  function onSplineMouseUp(e) {
    console.log('Released:', e.target.name);
  }
  ```

#### `onSplineMouseHover`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when mouse hovers over an object
- **Example**:
  ```jsx
  function onSplineMouseHover(e) {
    console.log('Hovering:', e.target.name);
  }
  ```

#### `onSplineKeyDown`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when a keyboard key is pressed
- **Example**:
  ```jsx
  function onSplineKeyDown(e) {
    console.log('Key pressed:', e.key);
  }
  ```

#### `onSplineKeyUp`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when a keyboard key is released

#### `onSplineStart`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when the scene starts (after loading)

#### `onSplineLookAt`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when a camera look-at event occurs

#### `onSplineFollow`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when a camera follow event occurs

#### `onSplineScroll`
- **Type**: `(e: SplineEvent) => void`
- **Description**: Fired when a scroll event occurs in the scene

## Spline Application API

The `Application` object is provided via the `onLoad` callback.

### Methods

#### `emitEvent(eventName, nameOrUuid)`
- **Description**: Triggers a Spline event on an object
- **Parameters**:
  - `eventName` (SplineEventName) - The event to trigger
  - `nameOrUuid` (string) - Object name or UUID
- **Returns**: `void`
- **Example**:
  ```jsx
  spline.emitEvent('mouseHover', 'Button');
  spline.emitEvent('mouseDown', '8E8C2DDD-18B6-4C54-861D-7ED2519DE20E');
  ```

#### `emitEventReverse(eventName, nameOrUuid)`
- **Description**: Triggers a Spline event in reverse (from last state to first)
- **Parameters**:
  - `eventName` (SplineEventName) - The event to trigger
  - `nameOrUuid` (string) - Object name or UUID
- **Returns**: `void`
- **Example**:
  ```jsx
  spline.emitEventReverse('mouseHover', 'Card');
  ```

#### `findObjectById(uuid)`
- **Description**: Finds an object by its UUID
- **Parameters**:
  - `uuid` (string) - Object UUID from Spline editor
- **Returns**: `SPEObject` - The object if found, undefined otherwise
- **Example**:
  ```jsx
  const obj = spline.findObjectById('8E8C2DDD-18B6-4C54-861D-7ED2519DE20E');
  console.log(obj.name, obj.position);
  ```

#### `findObjectByName(name)`
- **Description**: Finds the first object matching the specified name
- **Parameters**:
  - `name` (string) - Object name from Spline editor
- **Returns**: `SPEObject` - The object if found, undefined otherwise
- **Example**:
  ```jsx
  const cube = spline.findObjectByName('Cube');
  cube.position.x += 10;
  ```

#### `setZoom(zoom)`
- **Description**: Sets the camera zoom level
- **Parameters**:
  - `zoom` (number) - Zoom value (1.0 is default, <1.0 zooms out, >1.0 zooms in)
- **Returns**: `void`
- **Example**:
  ```jsx
  spline.setZoom(1.5); // Zoom in
  spline.setZoom(0.7); // Zoom out
  ```

## SplineEventName Type

Available event types for `emitEvent()` and `emitEventReverse()`:

- `'mouseDown'` - Mouse button pressed
- `'mouseHover'` - Mouse hover
- `'mouseUp'` - Mouse button released
- `'keyDown'` - Keyboard key pressed
- `'keyUp'` - Keyboard key released
- `'start'` - Scene start event
- `'lookAt'` - Camera look-at event
- `'follow'` - Camera follow event

## SPEObject Interface

Objects returned by `findObjectById()` and `findObjectByName()` have the following properties:

### Properties

#### `name`
- **Type**: `string`
- **Description**: Object name from Spline editor
- **Example**: `'Cube'`, `'Button'`, `'Product'`

#### `id`
- **Type**: `string`
- **Description**: Object UUID
- **Example**: `'8E8C2DDD-18B6-4C54-861D-7ED2519DE20E'`

#### `position`
- **Type**: `{ x: number, y: number, z: number }`
- **Description**: Object position in 3D space
- **Mutable**: Yes
- **Example**:
  ```jsx
  console.log(obj.position); // { x: 0, y: 100, z: 50 }
  obj.position.x += 10;
  obj.position.y = 200;
  ```

#### `rotation`
- **Type**: `{ x: number, y: number, z: number }`
- **Description**: Object rotation in radians
- **Mutable**: Yes
- **Example**:
  ```jsx
  obj.rotation.y += Math.PI / 4; // Rotate 45 degrees
  obj.rotation.x = Math.PI / 2; // Rotate 90 degrees
  ```

#### `scale`
- **Type**: `{ x: number, y: number, z: number }`
- **Description**: Object scale multiplier
- **Mutable**: Yes
- **Example**:
  ```jsx
  obj.scale.x = 2; // Scale to 2x width
  obj.scale.y = 0.5; // Scale to half height
  obj.scale.z = 1.5;
  ```

#### `material`
- **Type**: `Material`
- **Description**: Object material properties
- **Properties**:
  - `color` - Material color (use `.set()` method)
- **Example**:
  ```jsx
  // Set color using hex value
  obj.material.color.set(0xff6b6b); // Red
  obj.material.color.set(0x4ecdc4); // Cyan
  obj.material.color.set(0xffe66d); // Yellow
  ```

#### `visible`
- **Type**: `boolean`
- **Description**: Object visibility
- **Mutable**: Yes
- **Example**:
  ```jsx
  obj.visible = false; // Hide object
  obj.visible = true;  // Show object
  ```

### Methods

#### `emitEvent(eventName)`
- **Description**: Triggers an event on this specific object
- **Parameters**:
  - `eventName` (SplineEventName) - The event to trigger
- **Returns**: `void`
- **Example**:
  ```jsx
  const button = spline.findObjectByName('Button');
  button.emitEvent('mouseHover'); // Trigger hover animation
  ```

## SplineEvent Interface

Event object passed to event handler callbacks:

### Properties

#### `target`
- **Type**: `SPEObject`
- **Description**: The object that triggered the event
- **Example**:
  ```jsx
  function onSplineMouseDown(e) {
    console.log('Clicked object:', e.target.name);
    console.log('Object ID:', e.target.id);
    console.log('Position:', e.target.position);
  }
  ```

#### `type`
- **Type**: `string`
- **Description**: Event type name
- **Values**: `'mouseDown'`, `'mouseUp'`, `'mouseHover'`, etc.

## Usage Examples

### Complete Component Example

```jsx
import { useRef, useState } from 'react';
import Spline from '@splinetool/react-spline';

export default function InteractiveScene() {
  const splineApp = useRef();
  const [isLoaded, setIsLoaded] = useState(false);

  function onLoad(spline) {
    splineApp.current = spline;
    setIsLoaded(true);
    console.log('Scene loaded');
  }

  function onSplineMouseDown(e) {
    console.log('Clicked:', e.target.name);

    if (e.target.name === 'Button') {
      // Trigger animation
      splineApp.current.emitEvent('mouseHover', 'Card');
    }
  }

  function rotateAllObjects() {
    if (!isLoaded) return;

    const cube = splineApp.current.findObjectByName('Cube');
    const sphere = splineApp.current.findObjectByName('Sphere');

    if (cube) cube.rotation.y += Math.PI / 4;
    if (sphere) sphere.rotation.x += Math.PI / 4;
  }

  return (
    <div>
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
        onSplineMouseDown={onSplineMouseDown}
        style={{ width: '100%', height: '600px' }}
      />

      {isLoaded && (
        <button onClick={rotateAllObjects}>
          Rotate Objects
        </button>
      )}
    </div>
  );
}
```

### Next.js Example

```jsx
// app/components/SplineScene.jsx
'use client';

import Spline from '@splinetool/react-spline/next';

export default function SplineScene() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </div>
  );
}
```

### Lazy Loading Example

```jsx
import React, { Suspense } from 'react';

const Spline = React.lazy(() => import('@splinetool/react-spline'));

export default function LazyScene() {
  return (
    <Suspense fallback={<div>Loading 3D scene...</div>}>
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </Suspense>
  );
}
```

## Color Reference

Common hex color values for `material.color.set()`:

```javascript
// Red tones
0xff0000  // Pure red
0xff6b6b  // Coral red
0xe74c3c  // Soft red

// Blue tones
0x0000ff  // Pure blue
0x3498db  // Sky blue
0x2c3e50  // Dark blue

// Green tones
0x00ff00  // Pure green
0x2ecc71  // Emerald green
0x27ae60  // Dark green

// Yellow/Orange
0xffff00  // Pure yellow
0xffe66d  // Soft yellow
0xf39c12  // Orange

// Purple/Pink
0x9b59b6  // Purple
0xe91e63  // Pink
0xff69b4  // Hot pink

// Cyan/Teal
0x00ffff  // Pure cyan
0x4ecdc4  // Teal
0x1abc9c  // Turquoise

// Grayscale
0xffffff  // White
0xcccccc  // Light gray
0x95a5a6  // Gray
0x7f8c8d  // Dark gray
0x000000  // Black
```

## Math Helpers

Common rotation values (radians):

```javascript
Math.PI / 6   // 30 degrees
Math.PI / 4   // 45 degrees
Math.PI / 3   // 60 degrees
Math.PI / 2   // 90 degrees
Math.PI       // 180 degrees
Math.PI * 2   // 360 degrees

// Convert degrees to radians
const radians = (degrees * Math.PI) / 180;

// Convert radians to degrees
const degrees = (radians * 180) / Math.PI;
```

## Troubleshooting

### Scene Not Loading
- Verify scene URL is correct and complete
- Check that scene is published in Spline editor
- Look for CORS errors in console
- Ensure `@splinetool/runtime` is installed

### Events Not Firing
- Use `onSplineMouseDown` not `onMouseDown`
- Verify object has events configured in Spline editor
- Check object name matches exactly

### Object Not Found
- Verify object name in Spline editor matches exactly (case-sensitive)
- Check that `onLoad` has been called before finding objects
- Use `findObjectById` if name changes frequently

### Performance Issues
- Enable `renderOnDemand={true}`
- Reduce polygon count in Spline editor
- Compress textures
- Create mobile-specific scenes
- Use lazy loading for heavy scenes

## TypeScript Support

```typescript
import { Application, SPEObject, SplineEvent } from '@splinetool/runtime';
import Spline from '@splinetool/react-spline';

interface Props {
  sceneUrl: string;
}

export default function MyScene({ sceneUrl }: Props) {
  const splineApp = useRef<Application | null>(null);

  function onLoad(app: Application): void {
    splineApp.current = app;
  }

  function onSplineMouseDown(e: SplineEvent): void {
    const target: SPEObject = e.target;
    console.log(target.name);
  }

  return (
    <Spline
      scene={sceneUrl}
      onLoad={onLoad}
      onSplineMouseDown={onSplineMouseDown}
    />
  );
}
```
