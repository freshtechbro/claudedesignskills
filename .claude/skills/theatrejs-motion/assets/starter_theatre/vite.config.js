import { defineConfig } from 'vite'

// Minimal Vite config for the Theatre.js starter.
// @theatre/studio is a dev dependency and is guarded out of production in src/main.js.
export default defineConfig({
  server: { open: true },
})
