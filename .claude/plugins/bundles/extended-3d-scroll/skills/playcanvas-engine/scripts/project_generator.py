#!/usr/bin/env python3
"""
PlayCanvas Project Generator

Generates PlayCanvas project boilerplate with various configurations.

Usage:
    python project_generator.py                    # Interactive mode
    python project_generator.py --type basic       # Generate basic scene
    python project_generator.py --list             # List available types
"""

import argparse
import os
import sys
from pathlib import Path


def create_html_template(title, scene_code, additional_scripts=""):
    """Create complete HTML template for PlayCanvas"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      overflow: hidden;
      background: #000;
    }}

    canvas {{
      display: block;
      width: 100%;
      height: 100vh;
    }}

    #info {{
      position: absolute;
      top: 10px;
      left: 10px;
      color: white;
      background: rgba(0, 0, 0, 0.7);
      padding: 10px 15px;
      border-radius: 5px;
      font-size: 14px;
      font-family: monospace;
      pointer-events: none;
      z-index: 100;
    }}

    #controls {{
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      z-index: 100;
    }}

    button {{
      padding: 10px 20px;
      font-size: 14px;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.3s;
      backdrop-filter: blur(10px);
    }}

    button:hover {{
      background: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
    }}

    button:active {{
      transform: translateY(0);
    }}
  </style>
</head>
<body>
  <div id="info">
    <div id="fps">FPS: --</div>
    <div id="drawCalls">Draw Calls: --</div>
  </div>

  <div id="controls"></div>

  <canvas id="application-canvas"></canvas>

  <!-- PlayCanvas Engine -->
  <script src="https://cdn.jsdelivr.net/npm/playcanvas@1.70.0/build/playcanvas.min.js"></script>

  {additional_scripts}

  <script type="module">
{scene_code}
  </script>
</body>
</html>"""


def generate_basic_scene():
    """Generate basic PlayCanvas scene"""
    code = """    // Create canvas
    const canvas = document.getElementById('application-canvas');

    // Create application
    const app = new pc.Application(canvas, {{
      keyboard: new pc.Keyboard(window),
      mouse: new pc.Mouse(canvas)
    }});

    // Configure canvas
    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);

    // Handle resize
    window.addEventListener('resize', () => app.resizeCanvas());

    // Create camera
    const camera = new pc.Entity('camera');
    camera.addComponent('camera', {{
      clearColor: new pc.Color(0.2, 0.3, 0.4)
    }});
    camera.setPosition(0, 2, 5);
    camera.lookAt(0, 0, 0);
    app.root.addChild(camera);

    // Create directional light
    const light = new pc.Entity('light');
    light.addComponent('light', {{
      type: pc.LIGHTTYPE_DIRECTIONAL,
      color: new pc.Color(1, 1, 1),
      castShadows: true
    }});
    light.setEulerAngles(45, 30, 0);
    app.root.addChild(light);

    // Create ground
    const ground = new pc.Entity('ground');
    ground.addComponent('model', {{
      type: 'plane',
      castShadows: false,
      receiveShadows: true
    }});
    ground.setLocalScale(10, 1, 10);
    app.root.addChild(ground);

    // Create cube
    const cube = new pc.Entity('cube');
    cube.addComponent('model', {{
      type: 'box',
      castShadows: true
    }});
    cube.setPosition(0, 0.5, 0);
    app.root.addChild(cube);

    // Animation
    let isRotating = true;

    app.on('update', (dt) => {{
      if (isRotating) {{
        cube.rotate(10 * dt, 20 * dt, 30 * dt);
      }

      // Update stats
      document.getElementById('fps').textContent = `FPS: ${{Math.round(1 / dt)}}`;
      document.getElementById('drawCalls').textContent = `Draw Calls: ${{app.stats?.drawCalls?.total || 0}}`;
    }});

    // Controls
    const controls = document.getElementById('controls');

    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = 'Pause Rotation';
    toggleBtn.addEventListener('click', () => {{
      isRotating = !isRotating;
      toggleBtn.textContent = isRotating ? 'Pause Rotation' : 'Resume Rotation';
    }});
    controls.appendChild(toggleBtn);

    // Start application
    app.start();

    console.log('PlayCanvas application started');"""

    return code


def generate_physics_scene():
    """Generate scene with physics simulation"""
    additional_scripts = """
  <!-- Ammo.js Physics Engine -->
  <script src="https://cdn.jsdelivr.net/npm/ammo.js@0.0.10/ammo.js"></script>"""

    code = """    const canvas = document.getElementById('application-canvas');
    const app = new pc.Application(canvas, {{
      keyboard: new pc.Keyboard(window),
      mouse: new pc.Mouse(canvas)
    }});

    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);
    window.addEventListener('resize', () => app.resizeCanvas());

    // Load Ammo.js
    Ammo().then((AmmoLib) => {{
      window.Ammo = AmmoLib;

      // Camera
      const camera = new pc.Entity('camera');
      camera.addComponent('camera', {{
        clearColor: new pc.Color(0.2, 0.3, 0.4)
      }});
      camera.setPosition(0, 5, 10);
      camera.lookAt(0, 0, 0);
      app.root.addChild(camera);

      // Light
      const light = new pc.Entity('light');
      light.addComponent('light', {{
        type: pc.LIGHTTYPE_DIRECTIONAL,
        castShadows: true
      }});
      light.setEulerAngles(45, 30, 0);
      app.root.addChild(light);

      // Static ground
      const ground = new pc.Entity('ground');
      ground.addComponent('model', {{
        type: 'box',
        castShadows: false,
        receiveShadows: true
      }});
      ground.setLocalScale(20, 1, 20);

      ground.addComponent('rigidbody', {{
        type: pc.BODYTYPE_STATIC
      }});

      ground.addComponent('collision', {{
        type: 'box',
        halfExtents: new pc.Vec3(10, 0.5, 10)
      }});

      app.root.addChild(ground);

      // Dynamic cubes
      const cubes = [];

      function spawnCube() {{
        const cube = new pc.Entity('cube');
        cube.addComponent('model', {{
          type: 'box',
          castShadows: true
        }});

        cube.setPosition(
          (Math.random() - 0.5) * 4,
          5 + Math.random() * 5,
          (Math.random() - 0.5) * 4
        );

        cube.setEulerAngles(
          Math.random() * 360,
          Math.random() * 360,
          Math.random() * 360
        );

        cube.addComponent('rigidbody', {{
          type: pc.BODYTYPE_DYNAMIC,
          mass: 1,
          friction: 0.5,
          restitution: 0.3
        }});

        cube.addComponent('collision', {{
          type: 'box',
          halfExtents: new pc.Vec3(0.5, 0.5, 0.5)
        }});

        app.root.addChild(cube);
        cubes.push(cube);

        // Limit total cubes
        if (cubes.length > 50) {{
          const old = cubes.shift();
          old.destroy();
        }}
      }}

      // Update stats
      app.on('update', (dt) => {{
        document.getElementById('fps').textContent = `FPS: ${{Math.round(1 / dt)}}`;
        document.getElementById('drawCalls').textContent = `Cubes: ${{cubes.length}}`;
      }});

      // Controls
      const controls = document.getElementById('controls');

      const spawnBtn = document.createElement('button');
      spawnBtn.textContent = 'Spawn Cube';
      spawnBtn.addEventListener('click', spawnCube);
      controls.appendChild(spawnBtn);

      const resetBtn = document.createElement('button');
      resetBtn.textContent = 'Reset All';
      resetBtn.addEventListener('click', () => {{
        cubes.forEach(cube => cube.destroy());
        cubes.length = 0;
      }});
      controls.appendChild(resetBtn);

      // Auto-spawn
      setInterval(spawnCube, 1000);

      app.start();
    }});"""

    return code, additional_scripts


def generate_model_viewer():
    """Generate 3D model viewer"""
    code = """    const canvas = document.getElementById('application-canvas');
    const app = new pc.Application(canvas, {{
      keyboard: new pc.Keyboard(window),
      mouse: new pc.Mouse(canvas)
    }});

    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);
    window.addEventListener('resize', () => app.resizeCanvas());

    // Camera
    const camera = new pc.Entity('camera');
    camera.addComponent('camera', {{
      clearColor: new pc.Color(0.1, 0.1, 0.15)
    }});
    camera.setPosition(0, 2, 5);
    camera.lookAt(0, 1, 0);
    app.root.addChild(camera);

    // Lights
    const light1 = new pc.Entity('light1');
    light1.addComponent('light', {{
      type: pc.LIGHTTYPE_DIRECTIONAL,
      color: new pc.Color(1, 1, 1),
      intensity: 1,
      castShadows: true
    }});
    light1.setEulerAngles(45, 30, 0);
    app.root.addChild(light1);

    const light2 = new pc.Entity('light2');
    light2.addComponent('light', {{
      type: pc.LIGHTTYPE_POINT,
      color: new pc.Color(0.5, 0.7, 1),
      intensity: 0.5
    }});
    light2.setPosition(-3, 2, 3);
    app.root.addChild(light2);

    // Ground
    const ground = new pc.Entity('ground');
    ground.addComponent('model', {{
      type: 'plane',
      castShadows: false,
      receiveShadows: true
    }});
    ground.setLocalScale(10, 1, 10);
    app.root.addChild(ground);

    // Model (placeholder - user should replace with their model)
    const model = new pc.Entity('model');
    model.addComponent('model', {{
      type: 'box',
      castShadows: true
    }});
    model.setPosition(0, 1, 0);
    app.root.addChild(model);

    // Rotation controls
    let autoRotate = true;
    let rotationSpeed = 20;

    // Mouse interaction
    let isDragging = false;
    let lastMouseX = 0;
    let lastMouseY = 0;

    app.mouse.on(pc.EVENT_MOUSEDOWN, (event) => {{
      isDragging = true;
      lastMouseX = event.x;
      lastMouseY = event.y;
      autoRotate = false;
    }});

    app.mouse.on(pc.EVENT_MOUSEUP, () => {{
      isDragging = false;
    }});

    app.mouse.on(pc.EVENT_MOUSEMOVE, (event) => {{
      if (isDragging) {{
        const dx = event.x - lastMouseX;
        const dy = event.y - lastMouseY;

        model.rotate(0, dx * 0.5, 0);
        camera.rotate(dy * 0.2, 0, 0);

        lastMouseX = event.x;
        lastMouseY = event.y;
      }}
    }});

    // Zoom with mouse wheel
    app.mouse.on(pc.EVENT_MOUSEWHEEL, (event) => {{
      const zoom = event.wheelDelta * 0.1;
      const pos = camera.getPosition();
      const distance = pos.length();

      if (distance + zoom > 2 && distance + zoom < 20) {{
        camera.translate(0, 0, zoom);
      }}
    }});

    // Update loop
    app.on('update', (dt) => {{
      if (autoRotate) {{
        model.rotate(0, rotationSpeed * dt, 0);
      }}

      document.getElementById('fps').textContent = `FPS: ${{Math.round(1 / dt)}}`;
      document.getElementById('drawCalls').textContent = 'Drag to rotate • Scroll to zoom';
    }});

    // Controls
    const controls = document.getElementById('controls');

    const autoRotateBtn = document.createElement('button');
    autoRotateBtn.textContent = 'Toggle Auto-Rotate';
    autoRotateBtn.addEventListener('click', () => {{
      autoRotate = !autoRotate;
    }});
    controls.appendChild(autoRotateBtn);

    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset View';
    resetBtn.addEventListener('click', () => {{
      camera.setPosition(0, 2, 5);
      camera.lookAt(0, 1, 0);
      model.setEulerAngles(0, 0, 0);
      autoRotate = true;
    }});
    controls.appendChild(resetBtn);

    app.start();"""

    return code


def generate_first_person():
    """Generate first-person controller"""
    code = """    const canvas = document.getElementById('application-canvas');
    const app = new pc.Application(canvas, {{
      keyboard: new pc.Keyboard(window),
      mouse: new pc.Mouse(canvas)
    }});

    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);
    window.addEventListener('resize', () => app.resizeCanvas());

    // Lock pointer on click
    canvas.addEventListener('click', () => {{
      canvas.requestPointerLock();
    }});

    // Camera
    const camera = new pc.Entity('camera');
    camera.addComponent('camera', {{
      clearColor: new pc.Color(0.5, 0.7, 0.9),
      farClip: 1000
    }});
    camera.setPosition(0, 1.6, 5);
    app.root.addChild(camera);

    // Light
    const light = new pc.Entity('light');
    light.addComponent('light', {{
      type: pc.LIGHTTYPE_DIRECTIONAL,
      castShadows: true
    }});
    light.setEulerAngles(45, 30, 0);
    app.root.addChild(light);

    // Ground
    const ground = new pc.Entity('ground');
    ground.addComponent('model', {{
      type: 'plane',
      castShadows: false,
      receiveShadows: true
    }});
    ground.setLocalScale(50, 1, 50);
    app.root.addChild(ground);

    // Some boxes for reference
    for (let i = 0; i < 20; i++) {{
      const box = new pc.Entity('box');
      box.addComponent('model', {{
        type: 'box',
        castShadows: true
      }});
      box.setPosition(
        (Math.random() - 0.5) * 40,
        0.5,
        (Math.random() - 0.5) * 40
      );
      box.setLocalScale(1, Math.random() * 3 + 1, 1);
      app.root.addChild(box);
    }}

    // First-person controls
    const moveSpeed = 5;
    const lookSpeed = 0.2;
    let pitch = 0;
    let yaw = 0;

    // Mouse look
    app.mouse.on(pc.EVENT_MOUSEMOVE, (event) => {{
      if (document.pointerLockElement === canvas) {{
        yaw -= event.dx * lookSpeed;
        pitch -= event.dy * lookSpeed;
        pitch = pc.math.clamp(pitch, -90, 90);

        camera.setLocalEulerAngles(pitch, yaw, 0);
      }}
    }});

    // Movement
    app.on('update', (dt) => {{
      const forward = camera.forward;
      const right = camera.right;

      if (app.keyboard.isPressed(pc.KEY_W)) {{
        camera.translate(forward.mulScalar(moveSpeed * dt));
      }}
      if (app.keyboard.isPressed(pc.KEY_S)) {{
        camera.translate(forward.mulScalar(-moveSpeed * dt));
      }}
      if (app.keyboard.isPressed(pc.KEY_A)) {{
        camera.translate(right.mulScalar(-moveSpeed * dt));
      }}
      if (app.keyboard.isPressed(pc.KEY_D)) {{
        camera.translate(right.mulScalar(moveSpeed * dt));
      }}

      // Keep camera above ground
      const pos = camera.getPosition();
      if (pos.y < 1.6) {{
        pos.y = 1.6;
        camera.setPosition(pos);
      }}

      document.getElementById('fps').textContent = `FPS: ${{Math.round(1 / dt)}}`;
      document.getElementById('drawCalls').textContent = 'WASD to move • Mouse to look';
    }});

    app.start();

    // Instructions
    setTimeout(() => {{
      alert('Click canvas to enable mouse look\\nWASD to move\\nESC to release mouse');
    }}, 100);"""

    return code


def generate_particle_system():
    """Generate particle system demo"""
    code = """    const canvas = document.getElementById('application-canvas');
    const app = new pc.Application(canvas);

    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);
    window.addEventListener('resize', () => app.resizeCanvas());

    // Camera
    const camera = new pc.Entity('camera');
    camera.addComponent('camera', {{
      clearColor: new pc.Color(0.05, 0.05, 0.1)
    }});
    camera.setPosition(0, 5, 15);
    camera.lookAt(0, 0, 0);
    app.root.addChild(camera);

    // Particles
    const particles = [];
    const particleCount = 1000;

    for (let i = 0; i < particleCount; i++) {{
      const particle = new pc.Entity('particle');
      particle.addComponent('model', {{
        type: 'sphere',
        castShadows: false
      }});

      particle.setLocalScale(0.1, 0.1, 0.1);
      particle.setPosition(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      );

      // Create colored material
      const material = new pc.StandardMaterial();
      const hue = (i / particleCount) * 360;
      material.emissive = new pc.Color().fromString(`hsl(${{hue}}, 70%, 60%)`);
      material.update();

      particle.model.meshInstances[0].material = material;

      app.root.addChild(particle);

      particles.push({{
        entity: particle,
        velocity: new pc.Vec3(
          (Math.random() - 0.5) * 2,
          (Math.random() - 0.5) * 2,
          (Math.random() - 0.5) * 2
        ),
        originalPos: particle.getPosition().clone()
      }});
    }}

    // Animation
    let time = 0;
    const bounds = 8;

    app.on('update', (dt) => {{
      time += dt;

      particles.forEach((p, i) => {{
        const pos = p.entity.getPosition();

        // Update position
        pos.add(p.velocity.clone().mulScalar(dt));

        // Bounce off bounds
        if (Math.abs(pos.x) > bounds) p.velocity.x *= -1;
        if (Math.abs(pos.y) > bounds) p.velocity.y *= -1;
        if (Math.abs(pos.z) > bounds) p.velocity.z *= -1;

        // Wave effect
        const wave = Math.sin(time * 2 + i * 0.1) * 0.5;
        pos.y += wave * dt;

        p.entity.setPosition(pos);

        // Rotate
        p.entity.rotate(dt * 50, dt * 100, dt * 150);
      }});

      document.getElementById('fps').textContent = `FPS: ${{Math.round(1 / dt)}}`;
      document.getElementById('drawCalls').textContent = `Particles: ${{particleCount}}`;
    }});

    // Rotate camera
    app.on('update', (dt) => {{
      camera.rotate(0, dt * 10, 0);
    }});

    app.start();"""

    return code


PROJECT_TYPES = {
    'basic': {
        'name': 'Basic Scene',
        'description': 'Simple scene with camera, light, and rotating cube',
        'generator': lambda: (generate_basic_scene(), "")
    },
    'physics': {
        'name': 'Physics Simulation',
        'description': 'Dynamic physics with Ammo.js and falling cubes',
        'generator': generate_physics_scene
    },
    'viewer': {
        'name': '3D Model Viewer',
        'description': 'Interactive model viewer with orbit controls',
        'generator': lambda: (generate_model_viewer(), "")
    },
    'fps': {
        'name': 'First-Person Controller',
        'description': 'WASD + mouse look first-person movement',
        'generator': lambda: (generate_first_person(), "")
    },
    'particles': {
        'name': 'Particle System',
        'description': 'Animated particle system with 1000 particles',
        'generator': lambda: (generate_particle_system(), "")
    }
}


def list_types():
    """List all available project types"""
    print("\n🎮 Available PlayCanvas Project Types:\n")
    for key, info in PROJECT_TYPES.items():
        print(f"  {key:12} - {info['name']}")
        print(f"               {info['description']}")
        print()


def generate_project(type_key, output_path):
    """Generate PlayCanvas project"""
    if type_key not in PROJECT_TYPES:
        print(f"❌ Error: Unknown type '{type_key}'")
        print(f"   Use --list to see available types")
        return False

    info = PROJECT_TYPES[type_key]

    print(f"\n🎮 Generating {info['name']}...")

    # Generate code
    result = info['generator']()
    if isinstance(result, tuple):
        code, additional_scripts = result
    else:
        code, additional_scripts = result, ""

    # Create HTML
    html = create_html_template(info['name'], code, additional_scripts)

    # Write file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✅ Generated: {output_file}")
    print(f"   Open in browser to view")

    return True


def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "="*60)
    print("  🎮 PlayCanvas Project Generator")
    print("="*60)

    print("\nSelect project type:\n")
    types_list = list(PROJECT_TYPES.keys())
    for i, key in enumerate(types_list, 1):
        info = PROJECT_TYPES[key]
        print(f"  {i}. {info['name']}")
        print(f"     {info['description']}")
        print()

    while True:
        try:
            choice = input("Enter number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return False

            choice_num = int(choice)
            if 1 <= choice_num <= len(types_list):
                type_key = types_list[choice_num - 1]
                break
            else:
                print(f"❌ Please enter 1-{len(types_list)}")
        except ValueError:
            print("❌ Please enter a valid number")

    # Get output filename
    default_name = f"playcanvas_{type_key}.html"
    output_name = input(f"\nOutput filename [{default_name}]: ").strip()
    if not output_name:
        output_name = default_name

    output_path = Path.cwd() / output_name

    return generate_project(type_key, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate PlayCanvas project boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--type',
        choices=list(PROJECT_TYPES.keys()),
        help='Project type to generate'
    )

    parser.add_argument(
        '--output',
        default='playcanvas_project.html',
        help='Output HTML file path (default: playcanvas_project.html)'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available project types'
    )

    args = parser.parse_args()

    # List types
    if args.list:
        list_types()
        return 0

    # Interactive mode
    if not args.type:
        success = interactive_mode()
        return 0 if success else 1

    # Direct generation
    success = generate_project(args.type, args.output)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
