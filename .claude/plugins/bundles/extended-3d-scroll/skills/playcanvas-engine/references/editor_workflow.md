# PlayCanvas Editor Workflow Guide

Complete guide for working with the PlayCanvas Editor and integrating with the engine.

---

## Table of Contents

1. [Editor vs Engine-Only](#editor-vs-engine-only)
2. [Project Setup](#project-setup)
3. [Asset Pipeline](#asset-pipeline)
4. [Scene Management](#scene-management)
5. [Script Workflow](#script-workflow)
6. [Publishing & Deployment](#publishing--deployment)
7. [Editor-Code Integration](#editor-code-integration)

---

## Editor vs Engine-Only

### PlayCanvas Editor (Online)

**Pros**:
- Visual scene editing
- Real-time collaboration
- Built-in asset pipeline
- Instant preview
- Version control
- No build step required

**Cons**:
- Requires online access
- Less control over build process
- Tied to PlayCanvas platform

**Best for**: Game projects, team collaboration, rapid prototyping

---

### Engine-Only (Code-First)

**Pros**:
- Full control over code
- Works offline
- Custom build pipeline
- Version control with Git
- No platform lock-in

**Cons**:
- Manual scene setup
- No visual editor
- Manual asset loading
- More code required

**Best for**: Web apps, embedded 3D, custom workflows

---

## Project Setup

### Creating Editor Project

1. **Sign up** at https://playcanvas.com
2. **Create New Project**
   - Choose template (Blank, First Person, etc.)
   - Set project name
3. **Open Editor**
   - Launch visual editor
   - Scene hierarchy on left
   - Viewport in center
   - Inspector on right

---

### Editor Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  File  Edit  View  Develop  Tools  Help    [Play] [Share]│
├───────┬───────────────────────────────┬─────────────────┤
│       │                               │                 │
│ Scene │        Viewport              │   Inspector     │
│ Tree  │                               │                 │
│       │                               │   Properties    │
│  ├─Camera│     [3D View]              │   for selected  │
│  ├─Light │                            │   entity        │
│  └─Cube  │                            │                 │
│       │                               │                 │
├───────┴───────────────────────────────┴─────────────────┤
│            Assets Panel                                 │
│  [Models] [Materials] [Textures] [Scripts] [Scenes]    │
└─────────────────────────────────────────────────────────┘
```

---

### Project Structure

**Editor Project**:
```
MyProject/
├── assets/
│   ├── models/
│   ├── textures/
│   ├── materials/
│   ├── scripts/
│   └── scenes/
├── scenes/
│   └── Game.json
└── config.json
```

**Exported Project**:
```
build/
├── index.html
├── __game-scripts.js
├── __loading.js
├── __start__.js
├── config.json
├── files/
│   └── assets/
└── styles.css
```

---

## Asset Pipeline

### Uploading Assets

**3D Models**:
- Supported: `.glb`, `.gltf`, `.fbx`, `.obj`
- Drag & drop into Assets panel
- Auto-generates material instances

**Textures**:
- Supported: `.jpg`, `.png`, `.dds`, `.ktx2`, `.basis`
- Automatically creates texture asset
- Compression options available

**Audio**:
- Supported: `.mp3`, `.ogg`, `.wav`
- 3D positional or 2D audio

**Scripts**:
- Create new script in Assets panel
- Opens code editor
- Hot-reload on save

---

### Asset Import Settings

**Model Import**:
```javascript
// In Editor:
// 1. Select model asset
// 2. Inspector shows import options:
// - Preserve mapping (UV mapping)
// - Create materials
// - Create animations
// - Override axis
```

**Texture Import**:
```javascript
// Compression settings:
// - None (original)
// - DXT (Desktop)
// - PVR (iOS)
// - ETC (Android)
// - ASTC (Modern mobile)
// - Basis (Universal)
```

---

### Creating Materials

**In Editor**:
1. Assets Panel → Right-click → New Material
2. Select material
3. Inspector shows material properties:
   - Diffuse color
   - Diffuse map
   - Metalness/Gloss
   - Normal map
   - Emissive
   - Ambient occlusion

**Material Graph** (Advanced):
- Visual node-based material editor
- Custom shader creation
- Real-time preview

---

## Scene Management

### Scene Hierarchy

**Creating Entities**:
```
Right-click in Hierarchy → Add Entity
Options:
- Empty entity
- Box, Sphere, Cylinder, etc.
- Camera
- Light
- Group (empty parent)
```

**Organizing**:
- Drag entities to reparent
- Multi-select with Ctrl/Cmd
- Group related entities
- Use naming conventions:
  ```
  Player
  ├── Model
  ├── Camera
  └── Collider

  Enemies
  ├── Enemy_01
  ├── Enemy_02
  └── Enemy_03
  ```

---

### Components in Editor

**Adding Components**:
1. Select entity
2. Inspector → Add Component
3. Configure properties

**Component Settings**:
- Editable in Inspector
- Color pickers for colors
- Asset pickers for references
- Vector editors for positions

**Example - Camera Component**:
```
Camera Component
├── Clear Color: [Color Picker]
├── FOV: [Slider] 45°
├── Near Clip: [Input] 0.1
├── Far Clip: [Input] 1000
├── Projection: [Dropdown] Perspective
└── Priority: [Input] 0
```

---

### Tags and Layers

**Tags**:
- Add tags to entities for searching
- Use in scripts: `app.root.findByTag('enemy')`

**In Editor**:
1. Select entity
2. Inspector → Tags
3. Add/remove tags

**Layers**:
- Control rendering order
- Separate UI from world
- Custom post-processing per layer

**Default Layers**:
- World (3D objects)
- UI (2D interface)
- Skybox
- Immediate (debug drawing)

---

## Script Workflow

### Creating Scripts in Editor

**New Script**:
1. Assets Panel → New Script
2. Name your script (e.g., `playerController`)
3. Opens code editor

**Script Template**:
```javascript
var PlayerController = pc.createScript('playerController');

// Attributes (editable in Editor)
PlayerController.attributes.add('speed', {
    type: 'number',
    default: 10,
    title: 'Movement Speed'
});

PlayerController.attributes.add('jumpForce', {
    type: 'number',
    default: 5
});

// Initialize
PlayerController.prototype.initialize = function() {
    this.velocity = new pc.Vec3();
};

// Update every frame
PlayerController.prototype.update = function(dt) {
    var forward = this.entity.forward;
    var right = this.entity.right;

    // Movement
    if (this.app.keyboard.isPressed(pc.KEY_W)) {
        this.entity.translate(forward.mulScalar(this.speed * dt));
    }

    if (this.app.keyboard.isPressed(pc.KEY_SPACE)) {
        this.entity.rigidbody.applyImpulse(0, this.jumpForce, 0);
    }
};
```

---

### Attaching Scripts

**In Editor**:
1. Select entity
2. Add Component → Script
3. Add Script → Select your script
4. Configure attributes in Inspector

**Script Attributes in Inspector**:
```
Script Component
└── playerController
    ├── Speed: [10]
    ├── Jump Force: [5]
    └── [Add Script]
```

---

### Script Communication

**Between Scripts**:
```javascript
// In one script
this.entity.script.otherScript.doSomething();

// Fire events
this.app.fire('player:died', playerEntity);

// Listen to events
this.app.on('enemy:spawned', function(enemy) {
    console.log('Enemy spawned:', enemy.name);
});
```

---

### Debugging Scripts

**Console Logging**:
```javascript
console.log('Player position:', this.entity.getPosition());
console.warn('Low health!');
console.error('Failed to load asset');
```

**Launch Tab**:
- Editor → Launch → Opens game in new tab
- F12 for DevTools
- Console shows logs
- Edit scripts in Editor, auto-reloads

---

## Publishing & Deployment

### Publishing from Editor

**Steps**:
1. **Build**
   - Settings → Publishing
   - Configure build settings
   - Click "Publish"

2. **Download Build**
   - Download ZIP
   - Extract files
   - Upload to web server

**Build Settings**:
```javascript
{
  "name": "My Game",
  "version": "1.0.0",
  "scenes": [
    { "url": "game.json" }
  ],
  "use_device_pixel_ratio": true,
  "resolution_mode": "AUTO",
  "fill_mode": "FILL_WINDOW",
  "width": 1280,
  "height": 720
}
```

---

### Hosting Options

**PlayCanvas Hosting**:
- Click "Publish to PlayCanvas"
- Get shareable URL
- Free with watermark
- Premium for custom domain

**Self-Hosting**:
1. Download build
2. Upload to:
   - **Netlify**: Drag & drop
   - **Vercel**: Connect GitHub
   - **GitHub Pages**: Push to gh-pages branch
   - **AWS S3**: Static website hosting
   - **Any web server**: Just upload files

**CORS Considerations**:
```javascript
// If loading assets from different domain
// Server must send CORS headers:
Access-Control-Allow-Origin: *
```

---

### Optimization for Production

**Before Publishing**:

1. **Texture Compression**
   - Use Basis for universal compression
   - Or platform-specific (DXT/PVR/ETC)

2. **Script Concatenation**
   - Editor automatically concatenates scripts
   - Minifies in production builds

3. **Asset Loading**
   - Preload critical assets
   - Lazy load optional content

4. **Scene Settings**
   - Disable debug rendering
   - Set appropriate quality settings

---

## Editor-Code Integration

### Exporting Editor Scenes

**Option 1: REST API**
```javascript
// Download scene JSON via PlayCanvas API
fetch('https://playcanvas.com/api/projects/{id}/scenes/{sceneId}', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
})
.then(res => res.json())
.then(sceneData => {
  console.log('Scene data:', sceneData);
});
```

**Option 2: Download Build**
- Editor → Settings → Publishing → Download
- Extract ZIP
- Use `config.json` and scene files in engine code

---

### Loading Editor Scenes in Code

```javascript
import * as pc from 'playcanvas';

const app = new pc.Application(canvas);

// Load scene from Editor export
fetch('config.json')
  .then(res => res.json())
  .then(config => {
    // Load scene hierarchy
    const sceneUrl = config.scenes[0].url;

    app.scenes.loadSceneHierarchy(sceneUrl, (err, parent) => {
      if (err) {
        console.error('Failed to load scene:', err);
        return;
      }

      console.log('Scene loaded');

      // Find entities
      const player = app.root.findByName('Player');
      const camera = app.root.findByName('Camera');

      // Start application
      app.start();
    });

    // Load scene settings
    app.scenes.loadSceneSettings(config.scenes[0].url, (err) => {
      if (err) console.error('Failed to load settings:', err);
    });
  });
```

---

### Hybrid Workflow

**Editor for Scenes, Code for Logic**:

1. **Design in Editor**
   - Create scene layout
   - Configure entities
   - Set up components

2. **Export Scene**
   - Download build
   - Get scene JSON files

3. **Code Logic**
   - Load scenes in code
   - Add custom game logic
   - Extend with JavaScript

**Example**:
```javascript
// Load Editor scene
app.scenes.loadSceneHierarchy('scene.json', (err, root) => {
  if (err) return;

  // Find Editor entities
  const player = root.findByName('Player');
  const enemies = root.findByTag('enemy');

  // Add code-based logic
  const gameManager = new pc.Entity('GameManager');
  gameManager.addComponent('script');
  gameManager.script.create('gameManager');
  app.root.addChild(gameManager);

  // Start game
  app.start();
  app.fire('game:start');
});
```

---

### Accessing Editor Attributes in Code

**In Editor Script**:
```javascript
var MyScript = pc.createScript('myScript');

MyScript.attributes.add('target', {
  type: 'entity',
  title: 'Target Entity'
});

MyScript.attributes.add('speed', {
  type: 'number',
  default: 10
});
```

**Accessing from Other Scripts**:
```javascript
// Get script instance
const myScript = entity.script.myScript;

// Read attributes
console.log('Target:', myScript.target);
console.log('Speed:', myScript.speed);

// Modify at runtime
myScript.speed = 20;
```

---

## Version Control

### Editor Projects

**Built-in Version Control**:
- Editor → Version Control
- Checkpoint system
- Branch management
- Conflict resolution

**Checkpoints**:
- Create checkpoint before major changes
- Name checkpoints descriptively
- Restore previous versions

---

### Engine-Only Projects

**Git Workflow**:
```bash
git init
git add .
git commit -m "Initial PlayCanvas project"

# .gitignore
node_modules/
build/
*.log
.DS_Store
```

**Structure**:
```
project/
├── src/
│   ├── index.html
│   ├── main.js
│   └── scripts/
├── assets/
│   ├── models/
│   └── textures/
├── package.json
└── README.md
```

---

## Collaboration

### Editor Collaboration

**Real-time Editing**:
- Multiple users in same project
- See others' cursors
- Live updates
- Chat built-in

**Permissions**:
- Owner (full access)
- Admin (edit + manage)
- Write (edit only)
- Read (view only)

---

### Team Workflow

**Best Practices**:

1. **Scene Ownership**
   - One person per scene at a time
   - Use checkpoints before switching

2. **Asset Organization**
   - Consistent naming: `character_player_diffuse.png`
   - Folder structure: `assets/characters/player/`

3. **Script Conventions**
   - camelCase for functions
   - PascalCase for classes
   - Prefix custom scripts: `game_playerController.js`

4. **Communication**
   - Use Editor chat
   - Document major changes
   - Code reviews for critical scripts

---

## Debugging in Editor

### Launch & Debug

**Launch Tab**:
- Editor → Launch
- Opens game in new tab with DevTools

**Debug Options**:
- **Profiler**: Performance metrics
- **Inspector**: Scene graph at runtime
- **Console**: Logs and errors

**Profiler**:
```
Launch → Profiler
Shows:
- FPS
- Draw calls
- Triangle count
- Texture memory
- Script execution time
```

---

### Editor Console

**Accessing Engine in Console**:
```javascript
// In Launch tab console:
pc.app              // Application instance
pc.app.root         // Root entity
pc.app.systems      // Component systems

// Find entities
pc.app.root.findByName('Player')
pc.app.root.findByTag('enemy')

// Inspect entities
const player = pc.app.root.findByName('Player');
console.log('Position:', player.getPosition());
console.log('Components:', player.c);  // All components
```

---

## Tips & Best Practices

### Performance

**In Editor**:
- Use LOD for complex models
- Enable frustum culling
- Batch static objects
- Compress textures

**Scene Organization**:
- Group related entities
- Disable entities instead of destroying
- Use object pooling for bullets/particles

---

### Asset Management

**Naming Conventions**:
```
Models:       char_player.glb
Textures:     char_player_diffuse.png
Materials:    mat_player_body
Scripts:      player_controller.js
Scenes:       level_01.json
```

**Folder Structure**:
```
assets/
├── characters/
│   ├── player/
│   └── enemies/
├── environment/
│   ├── props/
│   └── terrain/
├── fx/
│   ├── particles/
│   └── sounds/
└── ui/
```

---

### Editor Shortcuts

**Navigation**:
- `F`: Frame selected entity
- `W/A/S/D`: Move viewport
- `Q/E`: Up/down
- `Right-click + drag`: Rotate view
- `Middle-click + drag`: Pan view
- `Scroll`: Zoom

**Editing**:
- `Ctrl/Cmd + D`: Duplicate entity
- `Delete`: Delete entity
- `Ctrl/Cmd + Z`: Undo
- `Ctrl/Cmd + Shift + Z`: Redo
- `Ctrl/Cmd + G`: Group entities

**Tools**:
- `1`: Select mode
- `2`: Translate mode
- `3`: Rotate mode
- `4`: Scale mode
- `Space`: Toggle between modes

---

## Resources

- **Editor**: https://playcanvas.com
- **Developer Docs**: https://developer.playcanvas.com
- **API Reference**: https://api.playcanvas.com
- **Tutorials**: https://developer.playcanvas.com/tutorials/
- **Forum**: https://forum.playcanvas.com
- **Examples**: https://playcanvas.github.io

---

## Quick Reference

### Editor Workflow
```
1. Create project
2. Import assets
3. Build scene hierarchy
4. Add components
5. Attach scripts
6. Configure settings
7. Test in Launch tab
8. Publish/Download
```

### Script Workflow
```
1. Assets → New Script
2. Write code in editor
3. Attach to entity
4. Configure attributes
5. Test in Launch tab
6. Debug in console
7. Iterate
```

### Publishing Workflow
```
1. Settings → Publishing
2. Configure build settings
3. Click Publish
4. Download build
5. Upload to hosting
6. Test live site
```

---

This guide covers the complete PlayCanvas Editor workflow from project creation to deployment. Use the Editor for visual scene design and the Engine API for custom code logic.
