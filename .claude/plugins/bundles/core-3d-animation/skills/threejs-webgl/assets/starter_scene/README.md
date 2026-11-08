# Three.js Starter Scene

A complete, production-ready Three.js boilerplate project with modern best practices.

## Features

✅ WebGL renderer with antialiasing
✅ PBR materials (MeshStandardMaterial)
✅ Shadow mapping
✅ Tone mapping (ACES Filmic)
✅ Orbit controls with damping
✅ Responsive design
✅ Loading screen
✅ Animated demo objects
✅ Performance optimizations

## Quick Start

### Option 1: Local Development

```bash
# Serve with any static server
python -m http.server 8000
# Or
npx serve
```

Open `http://localhost:8000` in your browser.

### Option 2: Add to Existing Project

Copy `index.html` and `main.js` to your project and customize as needed.

## Project Structure

```
starter_scene/
├── index.html    # HTML with embedded styles and import map
├── main.js       # Main Three.js scene setup
└── README.md     # This file
```

## Customization

### Change Background Color

```javascript
// In main.js
scene.background = new THREE.Color(0x1a1a2e); // Change hex color
```

### Add Your Own Objects

```javascript
// After existing objects in main.js
const myGeometry = new THREE.BoxGeometry(1, 1, 1);
const myMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const myMesh = new THREE.Mesh(myGeometry, myMaterial);
myMesh.position.set(x, y, z);
myMesh.castShadow = true;
scene.add(myMesh);
```

### Load 3D Models

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

### Adjust Performance

```javascript
// Reduce pixel ratio for better performance
renderer.setPixelRatio(1);

// Disable shadows
renderer.shadowMap.enabled = false;

// Simplify materials
material.roughness = 1.0; // More matte = faster
```

## Built-in Demo

The starter scene includes:
- **Red Cube**: Rotating on multiple axes
- **Cyan Sphere**: Bobbing up and down
- **Yellow Torus**: Rotating ring
- **Animated Point Light**: Orbiting the scene
- **Grid Floor**: With shadows

## Controls

- **Left Click + Drag**: Orbit camera
- **Scroll**: Zoom in/out
- **Right Click + Drag**: Pan (if enabled)

## Browser Compatibility

- Chrome/Edge: ✅ Excellent
- Firefox: ✅ Excellent
- Safari: ✅ Good (WebGL only)

## Performance Tips

1. Reduce `renderer.setPixelRatio()` to 1 on mobile
2. Lower shadow map size for better FPS
3. Use simpler materials (MeshLambertMaterial) on mobile
4. Implement LOD for complex scenes
5. Use `InstancedMesh` for repeated objects

## Next Steps

1. Replace demo objects with your own content
2. Add textures and materials
3. Implement raycasting for interactivity
4. Add post-processing effects
5. Optimize for production

## Resources

- [Three.js Documentation](https://threejs.org/docs/)
- [Three.js Examples](https://threejs.org/examples/)
- [Three.js Fundamentals](https://threejsfundamentals.org/)

## License

This starter template is provided as-is for use in any project.
