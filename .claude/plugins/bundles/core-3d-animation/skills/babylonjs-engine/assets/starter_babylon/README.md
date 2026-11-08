# Babylon.js Starter Template

Production-ready Babylon.js starter with Vite, physics, PBR materials, and interactive features.

## Features

- ⚡️ **Vite** - Fast build tool and dev server
- 🎮 **Babylon.js 7.x** - Latest version with WebGPU support
- 🎯 **Physics Engine** - Havok physics integration
- 🎨 **PBR Materials** - Physically based rendering
- 💡 **Dynamic Lighting** - Hemispheric + Directional with shadows
- 🖱️ **Interactive** - Mesh picking and keyboard controls
- 📊 **FPS Counter** - Performance monitoring
- 🐛 **Inspector** - Built-in debug tools (Shift+Ctrl+Alt+I)

## Quick Start

### Installation

```bash
npm install
# or
yarn
# or
pnpm install
```

### Development

```bash
npm run dev
```

Opens at `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
starter_babylon/
├── index.html              # Entry HTML
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
└── src/
    ├── main.js             # Main application
    └── style.css           # Styles
```

## What's Included

### Scene Setup

- **Camera**: ArcRotateCamera with orbit controls
- **Lights**: Hemispheric ambient + Directional with shadows
- **Ground**: 20x20 plane with physics
- **Meshes**: PBR sphere, standard material box, metallic sphere

### Physics

- **Havok Physics Engine** integrated
- **Realistic gravity** (9.8 m/s²)
- **Collision detection** and response
- **Adjustable restitution** (bounciness)

### Materials

**PBR Material (Sphere 1)**
```javascript
const pbrMaterial = new PBRMaterial('pbrMat', scene);
pbrMaterial.metallic = 1.0;
pbrMaterial.roughness = 0.3;
pbrMaterial.baseColor = new Color3(0.9, 0.1, 0.1);
```

**Standard Material (Box)**
```javascript
const standardMaterial = new StandardMaterial('standardMat', scene);
standardMaterial.diffuseColor = new Color3(0.2, 0.8, 0.3);
standardMaterial.specularPower = 32;
```

### Interactions

- **Mouse Click**: Select and highlight meshes
- **Spacebar**: Add random spheres with physics
- **Camera Controls**: Drag to rotate, scroll to zoom
- **Inspector**: Shift+Ctrl+Alt+I to toggle debug layer

## Customization

### Change Camera

Replace ArcRotateCamera with FreeCamera for FPS-style:

```javascript
import { FreeCamera } from '@babylonjs/core/Cameras/freeCamera.js';

const camera = new FreeCamera('camera', new Vector3(0, 5, -10), scene);
camera.setTarget(Vector3.Zero());
camera.attachControl(canvas, true);
```

### Add More Lights

```javascript
import { PointLight } from '@babylonjs/core/Lights/pointLight.js';

const pointLight = new PointLight('pointLight', new Vector3(0, 10, 0), scene);
pointLight.intensity = 0.5;
pointLight.diffuse = new Color3(1, 0.5, 0);
```

### Load GLTF Models

```javascript
import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader.js';
import '@babylonjs/loaders/glTF';

const result = await SceneLoader.ImportMeshAsync(
  null,
  'https://assets.babylonjs.com/meshes/',
  'village.glb',
  scene
);

console.log('Loaded:', result.meshes);
```

### Add Post-Processing

```javascript
import { DefaultRenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/defaultRenderingPipeline.js';

const pipeline = new DefaultRenderingPipeline('pipeline', true, scene, [camera]);
pipeline.fxaaEnabled = true;
pipeline.samples = 4;

pipeline.bloomEnabled = true;
pipeline.bloomThreshold = 0.8;
pipeline.bloomWeight = 0.5;
```

### Create Custom Meshes

```javascript
import { CreateTorus } from '@babylonjs/core/Meshes/Builders/torusBuilder.js';

const torus = CreateTorus('torus', {
  diameter: 3,
  thickness: 1,
  tessellation: 16
}, scene);

torus.position.y = 2;
```

### Add GUI

```javascript
import { AdvancedDynamicTexture } from '@babylonjs/gui/2D/advancedDynamicTexture.js';
import { Button } from '@babylonjs/gui/2D/controls/button.js';

const advancedTexture = AdvancedDynamicTexture.CreateFullscreenUI('UI');

const button = Button.CreateSimpleButton('button', 'Reset Scene');
button.width = '150px';
button.height = '40px';
button.color = 'white';
button.background = '#4fc3f7';
button.cornerRadius = 8;
button.onPointerUpObservable.add(() => {
  console.log('Reset clicked');
});

advancedTexture.addControl(button);
```

## Performance Tips

1. **Use PBR Materials** - More realistic and efficient than standard materials
2. **Optimize Shadow Maps** - Reduce shadowGenerator size if needed
3. **Freeze World Matrices** - For static meshes: `mesh.freezeWorldMatrix()`
4. **Use Instances** - For repeated meshes: `mesh.createInstance('instance1')`
5. **Optimize Physics** - Set appropriate mass and restitution values
6. **Hardware Scaling** - Reduce resolution if FPS drops: `engine.setHardwareScalingLevel(2)`

## Debugging

### Inspector

Press **Shift+Ctrl+Alt+I** to toggle the Babylon.js Inspector:
- View scene graph
- Inspect mesh properties
- Debug materials
- Analyze performance
- Tweak values in real-time

### Console Logs

The template includes helpful console logs:
- Selected mesh names
- FPS display in top-right corner

### Common Issues

**Physics not working?**
- Ensure Havok is properly initialized with `await HavokPhysics()`
- Check that physics aggregates are created after `scene.enablePhysics()`

**Meshes not visible?**
- Check camera position and target
- Verify mesh positions
- Ensure materials are applied

**Performance issues?**
- Reduce shadow map size
- Disable post-processing
- Use hardware scaling
- Optimize mesh count

## Next Steps

### Add Animations

```javascript
import { Animation } from '@babylonjs/core/Animations/animation.js';

const animation = Animation.CreateAndStartAnimation(
  'rotate',
  mesh,
  'rotation.y',
  30,
  120,
  0,
  Math.PI * 2,
  Animation.ANIMATIONLOOPMODE_CYCLE
);
```

### Enable WebXR (VR/AR)

```javascript
const env = scene.createDefaultEnvironment();
const xr = await scene.createDefaultXRExperienceAsync({
  floorMeshes: [env.ground]
});
```

### Add Particles

```javascript
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem.js';
import { Texture } from '@babylonjs/core/Materials/Textures/texture.js';

const particleSystem = new ParticleSystem('particles', 2000, scene);
particleSystem.particleTexture = new Texture('particle.png', scene);
particleSystem.emitter = new Vector3(0, 5, 0);
particleSystem.start();
```

## Resources

- [Babylon.js Documentation](https://doc.babylonjs.com/)
- [Babylon.js Playground](https://playground.babylonjs.com/)
- [Babylon.js Forum](https://forum.babylonjs.com/)
- [Babylon.js Examples](https://doc.babylonjs.com/examples/)

## License

MIT - Free for personal and commercial use
