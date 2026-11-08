# PlayCanvas Starter Template

Production-ready PlayCanvas starter project with best practices, utilities, and interactive demo.

---

## Features

✨ **Complete Setup**
- PlayCanvas engine integration
- Camera orbit controls
- Input management system
- Performance stats display
- Responsive UI overlay
- Mobile-friendly touch controls

🎨 **Demo Scene**
- 5 interactive 3D shapes
- Dynamic lighting (directional + ambient)
- PBR materials with varied metalness
- Smooth animations
- Ground plane with shadows

⚡ **Performance**
- Optimized rendering
- Real-time FPS, draw calls, triangle count
- Canvas auto-resizing
- Anti-aliasing enabled

📱 **Responsive**
- Desktop (mouse + keyboard)
- Mobile (touch + pinch-to-zoom)
- Tablet support

---

## Quick Start

### 1. Download Template

```bash
# Copy starter template to your project
cp -r .claude/skills/playcanvas-engine/assets/starter_playcanvas ./my-playcanvas-project
cd my-playcanvas-project
```

### 2. Serve Locally

**Using Python:**
```bash
python3 -m http.server 8000
```

**Using Node.js:**
```bash
npx http-server -p 8000
```

**Using PHP:**
```bash
php -S localhost:8000
```

### 3. Open in Browser

Navigate to `http://localhost:8000`

---

## Project Structure

```
starter_playcanvas/
├── index.html              # Main HTML file
├── styles.css              # UI styling
├── scripts/
│   ├── app.js             # Main application logic
│   ├── camera-controller.js  # Orbit camera
│   └── input-manager.js   # Input handling
└── README.md              # This file
```

---

## Usage Guide

### Camera Controls

**Desktop:**
- **Left-click + drag**: Rotate camera
- **Right-click + drag**: Rotate camera
- **Scroll wheel**: Zoom in/out

**Mobile:**
- **Single finger drag**: Rotate camera
- **Pinch gesture**: Zoom in/out

### UI Controls

**Toggle Stats**: Show/hide performance statistics
**Wireframe**: Toggle wireframe rendering (console only)
**Reset Camera**: Return camera to initial position

---

## Customization

### Change Scene Background

Edit `app.js`:

```javascript
camera.addComponent('camera', {
    clearColor: new pc.Color(0.1, 0.1, 0.15), // RGB values 0-1
    farClip: 100
});
```

### Add New Objects

```javascript
// Create entity
const cube = new pc.Entity('MyCube');

// Add model component
cube.addComponent('model', {
    type: 'box'  // box, sphere, cylinder, cone, capsule, plane
});

// Position it
cube.setPosition(0, 2, 0);

// Create material
const material = new pc.StandardMaterial();
material.diffuse = new pc.Color(1, 0, 0);  // Red
material.metalness = 0.5;
material.gloss = 0.7;
material.update();
cube.model.material = material;

// Add to scene
app.root.addChild(cube);
```

### Load 3D Models

```javascript
// Load GLTF/GLB model
app.assets.loadFromUrl('model.glb', 'container', (err, asset) => {
    if (err) {
        console.error('Failed to load model:', err);
        return;
    }

    const entity = asset.resource.instantiateRenderEntity();
    entity.setPosition(0, 0, 0);
    app.root.addChild(entity);
});
```

### Add Physics

```javascript
// Add rigidbody component
entity.addComponent('rigidbody', {
    type: 'dynamic',  // dynamic, static, kinematic
    mass: 1,
    friction: 0.5,
    restitution: 0.3
});

// Add collision component
entity.addComponent('collision', {
    type: 'box'  // box, sphere, capsule, cylinder, mesh
});
```

### Custom Scripts

Create script component:

```javascript
var MyScript = pc.createScript('myScript');

MyScript.prototype.initialize = function() {
    console.log('Script initialized');
};

MyScript.prototype.update = function(dt) {
    // Update logic
    this.entity.rotate(0, 10 * dt, 0);
};

// Attach to entity
entity.addComponent('script');
entity.script.create('myScript');
```

---

## Input Manager API

The included `InputManager` class provides centralized input handling:

```javascript
// Access input manager (already instantiated in app.js)
const input = inputManager;

// Keyboard
if (input.isKeyPressed(pc.KEY_SPACE)) {
    console.log('Space pressed');
}

// WASD input
const moveVector = input.getWASDInput();  // Returns Vec2

// Mouse
const mousePos = input.getMousePosition();
const mouseDelta = input.getMouseDelta();
const wheel = input.getMouseWheel();

// Raycast from mouse
const camera = app.root.findByName('Camera');
const ray = input.getMouseRay(camera);
if (ray) {
    const result = input.raycast(ray.origin, ray.end);
    if (result) {
        console.log('Hit:', result.entity.name);
    }
}

// Touch
const touchCount = input.getTouchCount();
const touch = input.getTouch(0);  // First touch
```

---

## Camera Controller API

The `CameraController` class provides orbit camera functionality:

```javascript
// Access camera controller (already instantiated in app.js)
const camera = cameraController;

// Set target
camera.setTarget(new pc.Vec3(0, 5, 0));

// Or focus on entity
const player = app.root.findByName('Player');
camera.focusOn(player, 10);  // entity, distance

// Set rotation
camera.setYaw(45);    // Horizontal rotation
camera.setPitch(30);  // Vertical rotation

// Set distance
camera.setDistance(15);

// Animate camera
camera.animateTo(
    90,    // yaw
    20,    // pitch
    12,    // distance
    2.0    // duration in seconds
);

// Reset to initial position
camera.reset();

// Get camera vectors
const forward = camera.getForwardVector();
const right = camera.getRightVector();
const up = camera.getUpVector();
```

---

## Performance Optimization

### Reduce Draw Calls

```javascript
// Batch static objects with same material
const material = new pc.StandardMaterial();

entities.forEach(entity => {
    entity.model.material = material;  // Share material
});
```

### Use LOD (Level of Detail)

```javascript
// Add LOD levels
entity.addComponent('model', {
    type: 'asset',
    asset: highPolyModel
});

// Configure LOD
entity.model.meshInstances[0].lod = {
    levels: [
        { distance: 10, mesh: highPolyMesh },
        { distance: 50, mesh: lowPolyMesh }
    ]
};
```

### Frustum Culling

Frustum culling is enabled by default. Ensure entities have proper bounding boxes:

```javascript
// Update bounding box after scale changes
entity.model.meshInstances[0]._aabb.compute();
```

### Texture Compression

Use compressed texture formats for production:
- **Desktop**: DXT (DDS)
- **iOS**: PVR
- **Android**: ETC
- **Universal**: Basis

---

## Deployment

### Build for Production

1. **Minify JavaScript**:
```bash
# Using terser
npx terser scripts/app.js -o scripts/app.min.js
npx terser scripts/camera-controller.js -o scripts/camera-controller.min.js
npx terser scripts/input-manager.js -o scripts/input-manager.min.js
```

2. **Update index.html** to use minified files

3. **Compress Assets**:
- Optimize textures (use tools like TinyPNG)
- Compress 3D models (use glTF-Pipeline)
- Enable gzip on server

### Hosting Options

**GitHub Pages:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# Enable GitHub Pages in repo settings
```

**Netlify:**
- Drag & drop project folder to Netlify
- Or connect GitHub repo for auto-deploy

**Vercel:**
```bash
npm i -g vercel
vercel
```

**AWS S3:**
- Create S3 bucket
- Enable static website hosting
- Upload files
- Configure CloudFront CDN (optional)

---

## Browser Compatibility

**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**WebGL Requirements:**
- WebGL 2.0 (recommended)
- WebGL 1.0 (fallback)

**Mobile:**
- iOS Safari 14+
- Chrome Mobile 90+
- Samsung Internet 14+

---

## Troubleshooting

**Canvas not filling window:**
```javascript
// Ensure these are called
app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
app.setCanvasResolution(pc.RESOLUTION_AUTO);
```

**Assets not loading (CORS errors):**
- Serve from local server (not file://)
- Check CORS headers on asset server

**Poor performance on mobile:**
```javascript
// Reduce resolution for mobile
if (isMobile()) {
    app.graphicsDevice.maxPixelRatio = 1;
}

// Disable shadows
light.light.castShadows = false;
```

**Touch controls not working:**
```javascript
// Ensure touch device is initialized
app.touch = new pc.TouchDevice(canvas);
```

---

## Next Steps

1. **Add More Objects**: Experiment with different shapes and materials
2. **Load Models**: Import your own 3D models (GLTF/GLB)
3. **Add Physics**: Create interactive physics simulations
4. **Custom Scripts**: Write gameplay logic with script components
5. **UI Elements**: Add 2D UI with element components
6. **Particles**: Create visual effects with particle systems
7. **Audio**: Add sound effects and music

---

## Resources

- **PlayCanvas Engine**: https://github.com/playcanvas/engine
- **API Documentation**: https://api.playcanvas.com
- **Examples**: https://playcanvas.github.io
- **Forum**: https://forum.playcanvas.com
- **Editor**: https://playcanvas.com (for visual scene editing)

---

## License

This starter template is provided as-is for educational and commercial use.

PlayCanvas Engine is licensed under MIT License.

---

## Support

For issues or questions:
1. Check the [PlayCanvas Forum](https://forum.playcanvas.com)
2. Review [API documentation](https://api.playcanvas.com)
3. Search [examples](https://playcanvas.github.io)

---

Happy coding! 🚀
