#!/usr/bin/env python3
"""
A-Frame Scene Generator

Generates A-Frame scene boilerplate for different use cases:
- Basic 3D scenes
- VR experiences with controllers
- AR experiences with hit testing
- 360° photo/video viewers
- Multi-user networked scenes

Usage:
    python scene_generator.py basic MyScene
    python scene_generator.py vr VRProject
    python scene_generator.py ar ARFurniture
    python scene_generator.py 360 Gallery360
    python scene_generator.py --interactive
"""

import argparse
import sys
import os
from pathlib import Path

# Scene type configurations
SCENE_TYPES = {
    'basic': {
        'description': 'Basic 3D scene with primitives and camera',
        'features': ['primitives', 'lighting', 'sky', 'camera'],
        'filename': 'index.html'
    },
    'vr': {
        'description': 'VR scene with hand controllers and interactions',
        'features': ['vr-rig', 'controllers', 'teleportation', 'interactive-objects'],
        'filename': 'index.html'
    },
    'ar': {
        'description': 'AR scene with hit testing and object placement',
        'features': ['ar-hit-test', 'dom-overlay', 'models'],
        'filename': 'index.html'
    },
    '360': {
        'description': '360° photo/video gallery viewer',
        'features': ['360-sky', 'thumbnails', 'navigation'],
        'filename': 'index.html'
    },
    'networked': {
        'description': 'Multi-user networked scene with avatars',
        'features': ['networked-aframe', 'avatars', 'voice-chat'],
        'filename': 'index.html'
    },
    'physics': {
        'description': 'Scene with physics simulation',
        'features': ['physics', 'dynamic-objects', 'interactive'],
        'filename': 'index.html'
    },
    'environment': {
        'description': 'Procedural environment with effects',
        'features': ['environment', 'particles', 'effects'],
        'filename': 'index.html'
    }
}

def generate_basic_scene(name):
    """Generate basic 3D scene"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - A-Frame Basic Scene</title>
    <meta name="description" content="{name} - A-Frame VR">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <style>
      body {{ margin: 0; }}
      #info {{
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-family: sans-serif;
        font-size: 14px;
      }}
    </style>
  </head>
  <body>
    <a-scene>
      <!-- Assets -->
      <a-assets>
        <!-- Preload assets here -->
      </a-assets>

      <!-- Environment -->
      <a-sky color="#ECECEC"></a-sky>
      <a-plane
        rotation="-90 0 0"
        width="20"
        height="20"
        color="#7BC8A4">
      </a-plane>

      <!-- Lighting -->
      <a-entity light="type: ambient; color: #888; intensity: 0.5"></a-entity>
      <a-entity light="type: directional; color: #FFF; intensity: 0.8" position="2 4 2"></a-entity>

      <!-- Objects -->
      <a-box
        position="-1 0.5 -3"
        rotation="0 45 0"
        color="#4CC3D9"
        shadow>
      </a-box>

      <a-sphere
        position="0 1.25 -5"
        radius="1.25"
        color="#EF2D5E"
        shadow>
      </a-sphere>

      <a-cylinder
        position="1 0.75 -3"
        radius="0.5"
        height="1.5"
        color="#FFC65D"
        shadow>
      </a-cylinder>

      <!-- Camera -->
      <a-camera position="0 1.6 0" look-controls wasd-controls>
        <a-cursor></a-cursor>
      </a-camera>
    </a-scene>

    <div id="info">
      <strong>{name}</strong><br>
      WASD - Move | Mouse - Look
    </div>
  </body>
</html>'''

def generate_vr_scene(name):
    """Generate VR scene with controllers"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - A-Frame VR Experience</title>
    <meta name="description" content="{name} - VR Experience">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/aframe-blink-controls/dist/aframe-blink-controls.min.js"></script>
    <style>
      body {{ margin: 0; }}
    </style>
  </head>
  <body>
    <a-scene>
      <!-- Assets -->
      <a-assets>
        <audio id="click-sound" src="https://cdn.aframe.io/360-image-gallery-boilerplate/audio/click.ogg"></audio>
      </a-assets>

      <!-- Environment -->
      <a-sky color="#87CEEB"></a-sky>
      <a-plane
        class="ground"
        rotation="-90 0 0"
        width="50"
        height="50"
        color="#3D5E1F"
        shadow="receive: true">
      </a-plane>

      <!-- Lighting -->
      <a-entity light="type: ambient; color: #BBB; intensity: 0.6"></a-entity>
      <a-entity light="type: directional; color: #FFF; intensity: 0.5; castShadow: true" position="5 10 5"></a-entity>

      <!-- Interactive Objects -->
      <a-box
        class="interactive"
        position="-1 0.5 -3"
        color="#4CC3D9"
        event-set__mouseenter="scale: 1.2 1.2 1.2"
        event-set__mouseleave="scale: 1 1 1"
        sound="on: click; src: #click-sound"
        shadow="cast: true">
      </a-box>

      <a-sphere
        class="interactive"
        position="1 1.25 -3"
        radius="0.5"
        color="#EF2D5E"
        event-set__click="color: orange; scale: 1.5 1.5 1.5"
        sound="on: click; src: #click-sound"
        shadow="cast: true">
      </a-sphere>

      <!-- VR Camera Rig -->
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
          id="leftHand"
          hand-controls="hand: left"
          blink-controls="cameraRig: #rig; teleportOrigin: #camera; collisionEntities: .ground"
          laser-controls="hand: left">
        </a-entity>

        <!-- Right Hand Controller -->
        <a-entity
          id="rightHand"
          hand-controls="hand: right"
          laser-controls="hand: right"
          raycaster="objects: .interactive">
        </a-entity>
      </a-entity>
    </a-scene>

    <script>
      // VR session events
      const scene = document.querySelector('a-scene');

      scene.addEventListener('enter-vr', () => {{
        console.log('Entered VR mode');
      }});

      scene.addEventListener('exit-vr', () => {{
        console.log('Exited VR mode');
      }});

      // Controller events
      const rightHand = document.querySelector('#rightHand');

      rightHand.addEventListener('triggerdown', () => {{
        console.log('Trigger pressed');
      }});

      rightHand.addEventListener('gripdown', () => {{
        console.log('Grip pressed');
      }});
    </script>
  </body>
</html>'''

def generate_ar_scene(name):
    """Generate AR scene with hit testing"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - A-Frame AR Experience</title>
    <meta name="description" content="{name} - AR Experience">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <style>
      body {{ margin: 0; }}
      #overlay {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        font-family: sans-serif;
        font-size: 14px;
        text-align: center;
        z-index: 1000;
      }}
      #overlay button {{
        margin-top: 10px;
        padding: 10px 20px;
        background: #4CC3D9;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        cursor: pointer;
      }}
      #overlay button:hover {{
        background: #3BA0B5;
      }}
    </style>
  </head>
  <body>
    <a-scene
      webxr="optionalFeatures: hit-test, dom-overlay; overlayElement: #overlay"
      ar-hit-test="target: #model; type: footprint">

      <!-- Assets -->
      <a-assets>
        <!-- Replace with your GLTF model -->
        <a-asset-item id="model-asset" src="https://cdn.aframe.io/test-models/models/virtualcity/VC.gltf"></a-asset-item>
      </a-assets>

      <!-- AR Object to Place -->
      <a-entity
        id="model"
        gltf-model="#model-asset"
        scale="0.1 0.1 0.1"
        visible="false">
      </a-entity>

      <!-- AR Lighting -->
      <a-entity
        light="type: ambient; intensity: 0.8">
      </a-entity>

      <a-entity
        id="dirlight"
        light="type: directional; intensity: 0.5; castShadow: true"
        position="1 2 1">
      </a-entity>
    </a-scene>

    <!-- AR UI Overlay -->
    <div id="overlay">
      <p id="instructions">Tap to enter AR mode</p>
      <button id="clearBtn" style="display: none;">Clear Objects</button>
    </div>

    <script>
      const scene = document.querySelector('a-scene');
      const instructions = document.getElementById('instructions');
      const clearBtn = document.getElementById('clearBtn');
      const model = document.querySelector('#model');
      let placedObjects = [];

      // AR session events
      scene.addEventListener('enter-vr', function() {{
        if (this.is('ar-mode')) {{
          instructions.textContent = '';

          // Hit testing started
          this.addEventListener('ar-hit-test-start', function() {{
            instructions.innerHTML = 'Scanning environment...<br>Finding surfaces';
          }}, {{ once: true }});

          // Surface detected
          this.addEventListener('ar-hit-test-achieved', function() {{
            instructions.innerHTML = 'Tap to place object';
          }}, {{ once: true }});

          // Object placed
          this.addEventListener('ar-hit-test-select', function(evt) {{
            // Clone model for multiple placements
            const clone = model.cloneNode(true);
            clone.removeAttribute('id');
            clone.setAttribute('visible', true);

            const position = evt.detail.position;
            clone.setAttribute('position', position);

            scene.appendChild(clone);
            placedObjects.push(clone);

            instructions.innerHTML = 'Object placed! Tap to place another';
            clearBtn.style.display = 'block';
          }});
        }}
      }});

      scene.addEventListener('exit-vr', function() {{
        instructions.textContent = 'Tap to enter AR mode';
        clearBtn.style.display = 'none';
      }});

      // Clear all placed objects
      clearBtn.addEventListener('click', () => {{
        placedObjects.forEach(obj => obj.parentNode.removeChild(obj));
        placedObjects = [];
        instructions.innerHTML = 'Objects cleared! Tap to place';
      }});
    </script>
  </body>
</html>'''

def generate_360_scene(name):
    """Generate 360° photo/video gallery"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - 360° Gallery</title>
    <meta name="description" content="{name} - 360° Gallery">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://unpkg.com/aframe-event-set-component@5.0.0/dist/aframe-event-set-component.min.js"></script>
    <style>
      body {{ margin: 0; }}
      #info {{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-family: sans-serif;
        font-size: 14px;
        text-align: center;
      }}
    </style>
  </head>
  <body>
    <a-scene>
      <!-- Assets -->
      <a-assets>
        <!-- Replace with your 360 images -->
        <img id="city" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/city.jpg" crossorigin="anonymous">
        <img id="forest" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/cubes.jpg" crossorigin="anonymous">
        <img id="space" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/sechelt.jpg" crossorigin="anonymous">

        <!-- Thumbnails -->
        <img id="city-thumb" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/thumb-city.jpg" crossorigin="anonymous">
        <img id="forest-thumb" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/thumb-cubes.jpg" crossorigin="anonymous">
        <img id="space-thumb" src="https://cdn.aframe.io/360-image-gallery-boilerplate/img/thumb-sechelt.jpg" crossorigin="anonymous">

        <audio id="click-sound" src="https://cdn.aframe.io/360-image-gallery-boilerplate/audio/click.ogg"></audio>
      </a-assets>

      <!-- 360 Sky -->
      <a-sky id="image-360" src="#city" rotation="0 -130 0"></a-sky>

      <!-- Thumbnail Menu -->
      <a-entity id="menu" position="0 1.6 -2.5" layout="type: line; margin: 1.5" rotation="0 0 0">
        <!-- City Thumbnail -->
        <a-entity class="link"
          geometry="primitive: plane; width: 1; height: 1"
          material="shader: flat; src: #city-thumb"
          sound="on: click; src: #click-sound"
          event-set__mouseenter="scale: 1.2 1.2 1"
          event-set__mouseleave="scale: 1 1 1"
          event-set__click="_target: #image-360; material.src: #city">
        </a-entity>

        <!-- Forest Thumbnail -->
        <a-entity class="link"
          geometry="primitive: plane; width: 1; height: 1"
          material="shader: flat; src: #forest-thumb"
          sound="on: click; src: #click-sound"
          event-set__mouseenter="scale: 1.2 1.2 1"
          event-set__mouseleave="scale: 1 1 1"
          event-set__click="_target: #image-360; material.src: #forest">
        </a-entity>

        <!-- Space Thumbnail -->
        <a-entity class="link"
          geometry="primitive: plane; width: 1; height: 1"
          material="shader: flat; src: #space-thumb"
          sound="on: click; src: #click-sound"
          event-set__mouseenter="scale: 1.2 1.2 1"
          event-set__mouseleave="scale: 1 1 1"
          event-set__click="_target: #image-360; material.src: #space">
        </a-entity>
      </a-entity>

      <!-- Camera with Cursor -->
      <a-camera>
        <a-cursor
          raycaster="objects: .link"
          fuse="true"
          fuse-timeout="1500">
        </a-cursor>
      </a-camera>
    </a-scene>

    <div id="info">
      <strong>360° Gallery</strong><br>
      Gaze at thumbnails to switch views
    </div>
  </body>
</html>'''

def generate_physics_scene(name):
    """Generate scene with physics"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - A-Frame Physics Scene</title>
    <meta name="description" content="{name} - Physics Simulation">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/aframe-physics-system@4.2.2/dist/aframe-physics-system.min.js"></script>
    <style>
      body {{ margin: 0; }}
    </style>
  </head>
  <body>
    <a-scene physics="debug: false; gravity: -9.8">
      <!-- Environment -->
      <a-sky color="#87CEEB"></a-sky>

      <!-- Static Ground -->
      <a-plane
        static-body
        rotation="-90 0 0"
        width="20"
        height="20"
        color="#7BC8A4"
        shadow="receive: true">
      </a-plane>

      <!-- Lighting -->
      <a-entity light="type: ambient; intensity: 0.6"></a-entity>
      <a-entity light="type: directional; intensity: 0.5; castShadow: true" position="2 8 2"></a-entity>

      <!-- Dynamic Physics Objects -->
      <a-box
        dynamic-body="mass: 5"
        position="-2 5 -5"
        rotation="45 45 0"
        color="#4CC3D9"
        shadow="cast: true">
      </a-box>

      <a-sphere
        dynamic-body="mass: 3"
        position="0 7 -5"
        radius="0.5"
        color="#EF2D5E"
        shadow="cast: true">
      </a-sphere>

      <a-cylinder
        dynamic-body="mass: 4"
        position="2 6 -5"
        radius="0.3"
        height="1"
        color="#FFC65D"
        shadow="cast: true">
      </a-cylinder>

      <!-- Walls -->
      <a-box
        static-body
        position="-10 2.5 -5"
        width="0.5"
        height="5"
        depth="20"
        color="#888">
      </a-box>

      <a-box
        static-body
        position="10 2.5 -5"
        width="0.5"
        height="5"
        depth="20"
        color="#888">
      </a-box>

      <!-- Camera -->
      <a-camera position="0 1.6 5" look-controls wasd-controls></a-camera>
    </a-scene>

    <script>
      // Spawn new objects on keypress
      document.addEventListener('keydown', (evt) => {{
        if (evt.key === ' ') {{
          const scene = document.querySelector('a-scene');
          const sphere = document.createElement('a-sphere');

          sphere.setAttribute('dynamic-body', 'mass: 2');
          sphere.setAttribute('position', {{
            x: Math.random() * 4 - 2,
            y: 10,
            z: -5
          }});
          sphere.setAttribute('radius', 0.5);
          sphere.setAttribute('color', `#${{Math.floor(Math.random()*16777215).toString(16)}}`);
          sphere.setAttribute('shadow', 'cast: true');

          scene.appendChild(sphere);
        }}
      }});
    </script>
  </body>
</html>'''

def generate_environment_scene(name):
    """Generate scene with procedural environment"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - A-Frame Environment</title>
    <meta name="description" content="{name} - Procedural Environment">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/aframe-environment-component@1.3.3/dist/aframe-environment-component.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-particle-system-component@1.2.x/dist/aframe-particle-system-component.min.js"></script>
    <style>
      body {{ margin: 0; }}
    </style>
  </head>
  <body>
    <a-scene>
      <!-- Procedural Environment -->
      <a-entity environment="
        preset: forest;
        seed: 42;
        skyType: gradient;
        skyColor: #4A90E2;
        horizonColor: #87CEEB;
        lighting: distant;
        lightPosition: 1 1 -2;
        fog: 0.7;
        ground: hills;
        groundColor: #5A7F32;
        groundColor2: #3D5E1F;
        dressing: trees;
        dressingAmount: 30;
        dressingColor: #228B22;
        dressingScale: 5;
        grid: none
      "></a-entity>

      <!-- Particle Effects -->
      <a-entity particle-system="
        preset: dust;
        particleCount: 1000;
        color: #FFF;
        size: 0.3;
        maxAge: 3
      " position="0 2 -5">
      </a-entity>

      <!-- Objects in Scene -->
      <a-box
        position="0 0.5 -5"
        rotation="0 45 0"
        color="#4CC3D9"
        animation="property: rotation; to: 0 405 0; loop: true; dur: 10000">
      </a-box>

      <!-- Camera -->
      <a-camera position="0 1.6 0" look-controls wasd-controls></a-camera>
    </a-scene>
  </body>
</html>'''

def generate_networked_scene(name):
    """Generate networked multi-user scene"""
    return f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{name} - Networked A-Frame</title>
    <meta name="description" content="{name} - Multi-user VR">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/networked-aframe@^0.11.0/dist/networked-aframe.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js"></script>
    <script>
      // NAF schema for networked avatars
      window.addEventListener('load', () => {{
        NAF.schemas.add({{
          template: '#avatar-template',
          components: [
            'position',
            'rotation'
          ]
        }});
      }});
    </script>
    <style>
      body {{ margin: 0; }}
    </style>
  </head>
  <body>
    <a-scene networked-scene="
      room: {name.lower().replace(' ', '-')};
      adapter: wseasyrtc;
      audio: true;
      debug: false
    ">
      <!-- Assets -->
      <a-assets>
        <!-- Avatar Template -->
        <template id="avatar-template">
          <a-entity class="avatar">
            <a-sphere class="head" color="#5985ff" scale="0.2 0.22 0.2"></a-sphere>
            <a-entity class="face" position="0 0.05 0">
              <a-sphere class="eye" color="#FFF" position="0.06 0.05 -0.16" scale="0.04 0.04 0.04">
                <a-sphere class="pupil" color="#000" position="0 0 -1" scale="0.5 0.5 0.5"></a-sphere>
              </a-sphere>
              <a-sphere class="eye" color="#FFF" position="-0.06 0.05 -0.16" scale="0.04 0.04 0.04">
                <a-sphere class="pupil" color="#000" position="0 0 -1" scale="0.5 0.5 0.5"></a-sphere>
              </a-sphere>
            </a-entity>
          </a-entity>
        </template>
      </a-assets>

      <!-- Environment -->
      <a-sky color="#87CEEB"></a-sky>
      <a-plane rotation="-90 0 0" width="50" height="50" color="#7BC8A4"></a-plane>

      <!-- Lighting -->
      <a-entity light="type: ambient; intensity: 0.7"></a-entity>
      <a-entity light="type: directional; intensity: 0.4" position="2 4 2"></a-entity>

      <!-- Shared Objects -->
      <a-box position="-1 0.5 -3" color="#4CC3D9"></a-box>
      <a-sphere position="1 1.25 -3" radius="0.5" color="#EF2D5E"></a-sphere>

      <!-- Player Rig -->
      <a-entity id="rig" position="0 0 0">
        <a-entity id="camera" camera look-controls wasd-controls position="0 1.6 0"
                  networked="template: #avatar-template; attachTemplateToLocal: false">
        </a-entity>
      </a-entity>
    </a-scene>
  </body>
</html>'''

def interactive_mode():
    """Interactive scene generator"""
    print("\n=== A-Frame Scene Generator (Interactive Mode) ===\n")

    print("Available scene types:")
    for i, (scene_type, config) in enumerate(SCENE_TYPES.items(), 1):
        print(f"  {i}. {scene_type:12} - {config['description']}")

    while True:
        try:
            choice = input("\nSelect scene type (1-7): ").strip()
            scene_type = list(SCENE_TYPES.keys())[int(choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a number between 1 and 7.")

    name = input("Enter scene name (default: MyScene): ").strip() or "MyScene"
    output_dir = input("Enter output directory (default: current): ").strip() or "."

    generate_scene(scene_type, name, output_dir)

def generate_scene(scene_type, name, output_dir="."):
    """Generate scene based on type"""
    if scene_type not in SCENE_TYPES:
        print(f"Error: Unknown scene type '{scene_type}'")
        print(f"Available types: {', '.join(SCENE_TYPES.keys())}")
        sys.exit(1)

    # Generate HTML content
    generators = {
        'basic': generate_basic_scene,
        'vr': generate_vr_scene,
        'ar': generate_ar_scene,
        '360': generate_360_scene,
        'physics': generate_physics_scene,
        'environment': generate_environment_scene,
        'networked': generate_networked_scene
    }

    html_content = generators[scene_type](name)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write file
    filename = SCENE_TYPES[scene_type]['filename']
    file_path = output_path / filename

    with open(file_path, 'w') as f:
        f.write(html_content)

    print(f"\n✅ Generated {scene_type} scene: {file_path}")
    print(f"📝 Scene name: {name}")
    print(f"🎯 Features: {', '.join(SCENE_TYPES[scene_type]['features'])}")
    print(f"\n🚀 To view: Open {file_path} in a web browser")
    print("   Note: Some features require HTTPS (use a local server)")

def main():
    parser = argparse.ArgumentParser(
        description='Generate A-Frame scene boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python scene_generator.py basic MyScene
  python scene_generator.py vr VRProject --output ./my-scenes
  python scene_generator.py ar ARFurniture
  python scene_generator.py --interactive

Scene Types:
  basic       - Basic 3D scene with primitives
  vr          - VR scene with controllers
  ar          - AR scene with hit testing
  360         - 360° photo/video gallery
  physics     - Scene with physics simulation
  environment - Procedural environment
  networked   - Multi-user networked scene
        '''
    )

    parser.add_argument(
        'scene_type',
        nargs='?',
        choices=list(SCENE_TYPES.keys()),
        help='Type of scene to generate'
    )

    parser.add_argument(
        'name',
        nargs='?',
        default='MyScene',
        help='Name of the scene (default: MyScene)'
    )

    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available scene types'
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Scene Types:\n")
        for scene_type, config in SCENE_TYPES.items():
            print(f"  {scene_type:12} - {config['description']}")
            print(f"                 Features: {', '.join(config['features'])}\n")
        sys.exit(0)

    if args.interactive or not args.scene_type:
        interactive_mode()
    else:
        generate_scene(args.scene_type, args.name, args.output)

if __name__ == '__main__':
    main()
