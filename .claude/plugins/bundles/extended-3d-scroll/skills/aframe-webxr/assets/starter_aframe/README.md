# A-Frame Starter Template

Production-ready A-Frame starter template with interactive objects, animations, and VR support.

## Features

- 🎮 **Interactive Objects** - Click and hover interactions
- ✨ **Animations** - Rotation, position, and scale animations
- 🎯 **Cursor Controls** - Mouse and gaze-based interaction
- 🌐 **VR Ready** - Works with all WebXR headsets
- 💡 **Lighting & Shadows** - Ambient + directional lights
- 📱 **Responsive** - Works on desktop and mobile

## Quick Start

### View Locally

Simply open `index.html` in a web browser.

**Note**: For full VR features, you need HTTPS. Use a local server:

```bash
# Python 3
python -m http.server 8000

# Node.js (http-server)
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`

### VR Mode

1. Open on a VR-capable device (Quest, PC + headset, etc.)
2. Click the "Enter VR" button in the bottom-right
3. Use controllers to interact with objects

## Project Structure

```
starter_aframe/
├── index.html        # Main HTML file with A-Frame scene
├── style.css         # Styling for info panel
├── main.js           # JavaScript for interactions
└── README.md         # This file
```

## What's Included

### Scene Setup

- **Environment**: Sky + ground plane
- **Lighting**: Ambient light + directional light with shadows
- **Camera**: Desktop (WASD + mouse) and VR controls
- **Cursor**: Raycaster-based interaction

### Interactive Objects

**Box** (Blue)
- Continuous rotation animation
- Click to randomize color
- Hover to scale

**Sphere** (Red)
- Bouncing position animation
- Click to scale pulse
- Hover effects

**Cylinder** (Yellow)
- Click to spin 360°
- Hover color change

## Keyboard Shortcuts

- **WASD** - Move camera
- **Mouse** - Look around
- **R** - Randomize all object colors
- **Ctrl+Alt+I** - Toggle A-Frame Inspector

## Customization

### Change Colors

```html
<a-box color="#FF0000" position="0 1 -3"></a-box>
```

### Add New Objects

```html
<!-- Add to <a-scene> -->
<a-sphere
  class="interactive"
  position="2 1 -4"
  radius="0.5"
  color="#00FF00"
  shadow="cast: true"
  event-set__click="color: blue">
</a-sphere>
```

### Modify Animations

```html
<!-- Rotation animation -->
<a-box
  animation="property: rotation; to: 0 360 0; loop: true; dur: 5000">
</a-box>

<!-- Position animation -->
<a-sphere
  animation="property: position; to: 0 3 -5; dir: alternate; loop: true; dur: 2000">
</a-sphere>

<!-- Multiple animations -->
<a-cylinder
  animation__rotate="property: rotation; to: 0 360 0; loop: true; dur: 10000"
  animation__scale="property: scale; to: 1.5 1.5 1.5; dir: alternate; loop: true; dur: 3000">
</a-cylinder>
```

### Add Textures

```html
<a-assets>
  <img id="wood" src="textures/wood.jpg">
</a-assets>

<a-box material="src: #wood" position="0 1 -3"></a-box>
```

### Load 3D Models

```html
<a-assets>
  <a-asset-item id="tree" src="models/tree.gltf"></a-asset-item>
</a-assets>

<a-entity gltf-model="#tree" position="3 0 -5" scale="0.5 0.5 0.5"></a-entity>
```

## Adding VR Controllers

Replace the camera with a VR rig:

```html
<!-- Remove simple camera, add VR rig -->
<a-entity id="rig" position="0 0 0">
  <!-- Camera -->
  <a-entity
    id="camera"
    camera
    look-controls
    position="0 1.6 0">
  </a-entity>

  <!-- Left Hand Controller -->
  <a-entity
    hand-controls="hand: left"
    laser-controls="hand: left">
  </a-entity>

  <!-- Right Hand Controller -->
  <a-entity
    hand-controls="hand: right"
    laser-controls="hand: right"
    raycaster="objects: .interactive">
  </a-entity>
</a-entity>
```

## Performance Tips

1. **Limit Draw Calls** - Use fewer, simpler geometries
2. **Optimize Textures** - Use power-of-2 sizes (256, 512, 1024)
3. **Reduce Shadows** - Only cast shadows on key objects
4. **Use Fog** - Hide distant objects: `<a-scene fog="type: linear; color: #AAA">`
5. **Mobile Optimization** - Lower poly count for mobile devices

## Debugging

### A-Frame Inspector

Press **Ctrl+Alt+I** to open the visual scene inspector:
- View scene graph
- Edit entity properties in real-time
- Test materials and lighting
- Debug positioning

### Console Logs

The template includes console logs for:
- Scene load events
- Object interactions
- VR mode changes

Open browser DevTools (F12) to view logs.

## Common Issues

### VR Button Not Appearing

- **Solution**: Use HTTPS (required for WebXR)
- Run a local server with SSL or deploy to HTTPS host

### Objects Not Clickable

- **Solution**: Ensure cursor raycaster targets correct objects
```html
<a-cursor raycaster="objects: .interactive"></a-cursor>
```

### Performance Issues

- **Solution**: Reduce geometry complexity
```html
<!-- Low poly (faster) -->
<a-sphere segments-width="8" segments-height="6"></a-sphere>

<!-- High poly (slower) -->
<a-sphere segments-width="32" segments-height="32"></a-sphere>
```

## Next Steps

### Add Physics

```html
<script src="https://cdn.jsdelivr.net/npm/aframe-physics-system@4.2.2/dist/aframe-physics-system.min.js"></script>

<a-scene physics>
  <a-plane static-body></a-plane>
  <a-box dynamic-body position="0 5 -3"></a-box>
</a-scene>
```

### Add Environment

```html
<script src="https://cdn.jsdelivr.net/npm/aframe-environment-component@1.3.3/dist/aframe-environment-component.min.js"></script>

<a-entity environment="preset: forest"></a-entity>
```

### Add Particles

```html
<script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-particle-system-component@1.2.x/dist/aframe-particle-system-component.min.js"></script>

<a-entity particle-system="preset: snow"></a-entity>
```

## Resources

- [A-Frame Documentation](https://aframe.io/docs/)
- [A-Frame School](https://aframe.io/school/)
- [A-Frame Examples](https://aframe.io/examples/)
- [A-Frame Community Components](https://github.com/c-frame)
- [WebXR Guide](https://immersiveweb.dev/)

## License

MIT - Free for personal and commercial use
