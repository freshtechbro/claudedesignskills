import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,
    open: true
  },
  build: {
    target: 'esnext',
    minify: 'terser'
  },
  optimizeDeps: {
    exclude: ['@babylonjs/havok']
  }
});
