# Theatre.js Starter

Minimal Vite project wired for Theatre.js core + Studio (dev-only).

## Setup

```bash
npm install
npm run dev
```

The Studio editor appears in the corner during `npm run dev`. Keyframe the
`.box` element's props on the timeline, then scrub or play.

## Structure

- `src/main.js` — Theatre.js project/sheet/object + `onValuesChange` handler
- `src/style.css` — styles for the animated element
- `index.html` — entry point
- `vite.config.js` — minimal Vite config

## Production

`@theatre/studio` is a dev dependency and is guarded behind a dev check, so it
is excluded from `npm run build`. To replay authored animation in production:

1. Export the project state from Studio to `state.json`.
2. Load it: `getProject('Theatre Starter', { state })`.
3. `await project.ready` before the first `play()`.
