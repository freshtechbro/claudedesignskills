# Theatre.js API Reference

Comprehensive reference for `@theatre/core`, `@theatre/studio`, and `@theatre/r3f`.

> Package versions move quickly. Confirm current signatures at
> https://www.theatrejs.com/docs/latest/api/core before relying on edge behavior.

## Installation

```bash
# Core runtime (ships to production)
npm install @theatre/core

# Visual editor (dev-only)
npm install --save-dev @theatre/studio

# React Three Fiber extension (optional)
npm install @theatre/r3f
```

## @theatre/core

### getProject(name, config?)

Returns a memoized `Project` for `name`. Calling twice with the same name returns the same instance.

```js
import { getProject } from '@theatre/core'

const project = getProject('My Project')
// With persisted state exported from Studio:
const project2 = getProject('My Project', { state: importedStateJson })
```

- `name: string` — unique project identifier
- `config.state` — JSON state exported from Studio (production playback)
- `project.ready: Promise<void>` — resolves once initial values are applied
- `project.isReady: boolean`
- `project.address` — identifying address object

### project.sheet(name, instanceId?)

Creates or returns a `Sheet`. Optional `instanceId` allows multiple independent instances of the same sheet.

```js
const sheet = project.sheet('Scene')
const sheet2 = project.sheet('Scene', 'instance-2')
```

### sheet.object(key, props, options?)

Declares a `Sheet Object` with animatable props. Returns the object; re-calling with the same key returns the existing object (props must match).

```js
const obj = sheet.object('Logo', {
  x: 0,
  opacity: types.number(1, { range: [0, 1] }),
})
```

- `obj.value` — current values snapshot
- `obj.props` — prop pointers (used by Studio APIs)
- `obj.onValuesChange(cb)` — subscribe to value changes; returns an unsubscribe function
- `options.reconfigure: true` — replace props on an existing object

```js
const unsubscribe = obj.onValuesChange((v) => applyToDom(v))
// later
unsubscribe()
```

### sheet.sequence

The timeline for a sheet.

| Member | Description |
| --- | --- |
| `sequence.play(opts?)` | Returns `Promise<boolean>` (true = finished, false = interrupted) |
| `sequence.pause()` | Pause playback |
| `sequence.position` | Get/set current position in seconds |
| `sequence.pointer` | Pointer for subscribing to `position`/`length` |
| `sequence.attachAudio(opts)` | Sync sequence to a Web Audio source |

**play options**:

```js
sheet.sequence.play({
  rate: 1,                 // speed multiplier (negative = reverse)
  range: [0, 3],           // [start, end] seconds
  iterationCount: 1,       // Infinity to loop
  direction: 'normal',     // 'normal' | 'reverse' | 'alternate' | 'alternateReverse'
})
```

**Subscribe to position** (e.g., to render on demand):

```js
import { onChange } from '@theatre/core'
onChange(sheet.sequence.pointer.position, (pos) => {
  // runs whenever the sequence position changes
})
```

### types

| Type | Signature | Notes |
| --- | --- | --- |
| `types.number(default, opts?)` | `{ range?: [min,max], nudgeMultiplier?: number }` | Numeric slider |
| `types.boolean(default)` | — | Checkbox |
| `types.string(default)` | — | Text field |
| `types.stringLiteral(default, options, opts?)` | `options: { key: label }` | Dropdown/switch |
| `types.rgba(default)` | `{ r, g, b, a }` each 0–1 | Color picker |
| `types.compound(props)` | nested object of props | Groups related props |

```js
import { types } from '@theatre/core'

sheet.object('Panel', {
  size: types.compound({
    w: types.number(100, { range: [0, 500] }),
    h: types.number(100, { range: [0, 500] }),
  }),
  theme: types.stringLiteral('light', { light: 'Light', dark: 'Dark' }),
  tint: types.rgba({ r: 0.2, g: 0.4, b: 1, a: 1 }),
})
```

### onChange(pointer, callback)

Low-level subscription to any prop/sequence pointer. Returns an unsubscribe function.

### val(pointer)

Reads the current value of a pointer imperatively.

## @theatre/studio

Dev-only visual editor. Never initialize in production.

```js
import studio from '@theatre/studio'

if (process.env.NODE_ENV !== 'production') {
  studio.initialize()
}
```

| Method | Description |
| --- | --- |
| `studio.initialize(opts?)` | Mount the editor UI |
| `studio.extend(extension)` | Register an extension (e.g., R3F) |
| `studio.ui.hide()` / `studio.ui.restore()` | Toggle editor visibility |
| `studio.transaction(fn)` | Programmatically set values via `api.set(obj.props.x, 5)` |
| `studio.createContentOfSaveFile(projectId)` | Export project state for production |

**Exporting state**: In the Studio UI, use the project's export, or:

```js
const json = studio.createContentOfSaveFile('My Project')
// save json to state.json and load via getProject('My Project', { state })
```

## @theatre/r3f

React Three Fiber bindings.

```jsx
import { SheetProvider, editable as e, PerspectiveCamera } from '@theatre/r3f'
import extension from '@theatre/r3f/dist/extension'
```

| Export | Description |
| --- | --- |
| `SheetProvider` | Wrap R3F children; takes a `sheet` prop |
| `editable` (alias `e`) | `e.mesh`, `e.group`, `e.pointLight`, etc. Each needs a unique `theatreKey` |
| `PerspectiveCamera` / `OrthographicCamera` | Sequenceable cameras; `theatreKey` + `makeDefault` |
| `extension` | Pass to `studio.extend()` for the on-canvas editor panel |

```jsx
<SheetProvider sheet={sheet}>
  <PerspectiveCamera theatreKey="Camera" makeDefault position={[0, 0, 6]} />
  <e.mesh theatreKey="Box">
    <boxGeometry />
    <meshStandardMaterial />
  </e.mesh>
</SheetProvider>
```

**editable props**: Standard R3F props plus `theatreKey` (required, unique) and
`editableType` when wrapping custom components via `editable(Component, 'mesh')`.

## Production Checklist

1. `@theatre/studio` is a dev dependency and guarded out of the bundle.
2. Project loads with `{ state: importedJson }`.
3. `await project.ready` before first render / first `play()`.
4. Each `theatreKey` and project name is unique.
5. Scroll mapping uses the authored sequence length.
