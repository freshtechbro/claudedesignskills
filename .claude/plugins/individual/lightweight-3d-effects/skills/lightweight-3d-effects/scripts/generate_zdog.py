#!/usr/bin/env python3
"""
Zdog Illustration Generator

Generates Zdog pseudo-3D illustrations with various shapes, animations, and complexity levels.

Usage:
    python generate_zdog.py                    # Interactive mode
    python generate_zdog.py --type cube        # Generate cube
    python generate_zdog.py --list             # List available types
"""

import argparse
import os
import sys
from pathlib import Path


def create_html_template(title, zdog_code, css_styles=""):
    """Create complete HTML template with Zdog"""
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
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
    }}

    .container {{
      text-align: center;
      padding: 2rem;
    }}

    h1 {{
      font-size: 2.5rem;
      margin-bottom: 1rem;
      text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}

    .canvas-wrapper {{
      background: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 2rem;
      backdrop-filter: blur(10px);
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      margin: 2rem auto;
      display: inline-block;
    }}

    canvas {{
      display: block;
      cursor: grab;
    }}

    canvas:active {{
      cursor: grabbing;
    }}

    .info {{
      font-size: 1rem;
      opacity: 0.9;
      margin-top: 1rem;
    }}

    .controls {{
      margin-top: 2rem;
      display: flex;
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }}

    button {{
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      background: rgba(255, 255, 255, 0.2);
      color: white;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s;
      backdrop-filter: blur(10px);
    }}

    button:hover {{
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}

    button:active {{
      transform: translateY(0);
    }}

    {css_styles}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    <div class="canvas-wrapper">
      <canvas class="zdog-canvas" width="480" height="480"></canvas>
    </div>
    <div class="info">
      Drag to rotate • Click controls to interact
    </div>
    <div class="controls" id="controls"></div>
  </div>

  <script src="https://unpkg.com/zdog@1/dist/zdog.dist.min.js"></script>
  <script>
{zdog_code}
  </script>
</body>
</html>"""


def generate_basic_shapes():
    """Generate basic Zdog shapes"""
    code = """    // Create illustration
    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 4,
      dragRotate: true,
      onDragStart: function() {
        isSpinning = false;
      }
    });

    let isSpinning = true;

    // Ellipse
    new Zdog.Ellipse({
      addTo: illo,
      diameter: 20,
      translate: { x: -60, y: -40 },
      stroke: 5,
      color: '#636',
    });

    // Rectangle
    new Zdog.Rect({
      addTo: illo,
      width: 20,
      height: 20,
      translate: { x: 0, y: -40 },
      stroke: 3,
      color: '#E62',
      fill: true,
    });

    // Rounded Rectangle
    new Zdog.RoundedRect({
      addTo: illo,
      width: 20,
      height: 20,
      cornerRadius: 5,
      translate: { x: 60, y: -40 },
      stroke: 3,
      color: '#EA0',
      fill: true,
    });

    // Polygon (Triangle)
    new Zdog.Polygon({
      addTo: illo,
      sides: 3,
      radius: 12,
      translate: { x: -60, y: 0 },
      stroke: 3,
      color: '#19F',
      fill: true,
    });

    // Polygon (Pentagon)
    new Zdog.Polygon({
      addTo: illo,
      sides: 5,
      radius: 12,
      translate: { x: 0, y: 0 },
      stroke: 3,
      color: '#C25',
      fill: true,
    });

    // Polygon (Hexagon)
    new Zdog.Polygon({
      addTo: illo,
      sides: 6,
      radius: 12,
      translate: { x: 60, y: 0 },
      stroke: 3,
      color: '#4A9',
      fill: true,
    });

    // Hemisphere
    new Zdog.Hemisphere({
      addTo: illo,
      diameter: 20,
      translate: { x: -60, y: 40 },
      stroke: 5,
      color: '#636',
      fill: true,
    });

    // Cylinder
    new Zdog.Cylinder({
      addTo: illo,
      diameter: 16,
      length: 10,
      translate: { x: 0, y: 40 },
      stroke: 3,
      color: '#E62',
      fill: true,
    });

    // Cone
    new Zdog.Cone({
      addTo: illo,
      diameter: 16,
      length: 16,
      translate: { x: 60, y: 40 },
      stroke: 3,
      color: '#EA0',
      fill: true,
    });

    // Animation
    function animate() {
      if (isSpinning) {
        illo.rotate.y += 0.03;
      }
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const playBtn = document.createElement('button');
    playBtn.textContent = 'Pause';
    playBtn.addEventListener('click', () => {
      isSpinning = !isSpinning;
      playBtn.textContent = isSpinning ? 'Pause' : 'Play';
    });
    controls.appendChild(playBtn);

    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset';
    resetBtn.addEventListener('click', () => {
      illo.rotate.x = 0;
      illo.rotate.y = 0;
      illo.rotate.z = 0;
    });
    controls.appendChild(resetBtn);"""

    return code


def generate_3d_cube():
    """Generate animated 3D cube"""
    code = """    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 4,
      dragRotate: true,
    });

    let isSpinning = true;

    // Cube using Box
    let cube = new Zdog.Box({
      addTo: illo,
      width: 40,
      height: 40,
      depth: 40,
      stroke: 2,
      color: '#C25',
      fill: true,
      frontFace: '#EA0',
      rearFace: '#E62',
      leftFace: '#636',
      rightFace: '#C25',
      topFace: '#4A9',
      bottomFace: '#19F'
    });

    function animate() {
      if (isSpinning) {
        cube.rotate.x += 0.02;
        cube.rotate.y += 0.03;
      }
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const playBtn = document.createElement('button');
    playBtn.textContent = 'Pause';
    playBtn.addEventListener('click', () => {
      isSpinning = !isSpinning;
      playBtn.textContent = isSpinning ? 'Pause' : 'Play';
    });
    controls.appendChild(playBtn);

    const randomizeBtn = document.createElement('button');
    randomizeBtn.textContent = 'Randomize Colors';
    randomizeBtn.addEventListener('click', () => {
      const randomColor = () => '#' + Math.floor(Math.random()*16777215).toString(16);
      cube.frontFace = randomColor();
      cube.rearFace = randomColor();
      cube.leftFace = randomColor();
      cube.rightFace = randomColor();
      cube.topFace = randomColor();
      cube.bottomFace = randomColor();
    });
    controls.appendChild(randomizeBtn);"""

    return code


def generate_robot():
    """Generate robot character"""
    code = """    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 3,
      dragRotate: true,
    });

    let isSpinning = true;

    // Robot anchor
    let robot = new Zdog.Anchor({
      addTo: illo,
      translate: { y: -20 }
    });

    // Head
    new Zdog.Box({
      addTo: robot,
      width: 30,
      height: 30,
      depth: 30,
      stroke: 2,
      color: '#636',
      topFace: '#EA0',
      bottomFace: '#E62',
      fill: true
    });

    // Eyes
    [-1, 1].forEach(xSide => {
      new Zdog.Ellipse({
        addTo: robot,
        diameter: 6,
        translate: { x: xSide * 8, y: -4, z: 15 },
        stroke: 2,
        color: '#19F',
        fill: true
      });
    });

    // Antenna
    new Zdog.Shape({
      addTo: robot,
      path: [
        { y: -15 },
        { y: -25 }
      ],
      stroke: 2,
      color: '#EA0'
    });

    new Zdog.Ellipse({
      addTo: robot,
      diameter: 6,
      translate: { y: -25 },
      stroke: 2,
      color: '#E62',
      fill: true
    });

    // Body
    new Zdog.Box({
      addTo: robot,
      translate: { y: 35 },
      width: 35,
      height: 40,
      depth: 25,
      stroke: 2,
      color: '#636',
      fill: true
    });

    // Arms
    [-1, 1].forEach(xSide => {
      let arm = new Zdog.Anchor({
        addTo: robot,
        translate: { x: xSide * 25, y: 25 }
      });

      new Zdog.Box({
        addTo: arm,
        translate: { y: 15 },
        width: 12,
        height: 40,
        depth: 12,
        stroke: 2,
        color: '#C25',
        fill: true
      });

      // Hand
      new Zdog.Ellipse({
        addTo: arm,
        diameter: 10,
        translate: { y: 38 },
        stroke: 2,
        color: '#EA0',
        fill: true
      });
    });

    // Legs
    [-1, 1].forEach(xSide => {
      let leg = new Zdog.Anchor({
        addTo: robot,
        translate: { x: xSide * 10, y: 55 }
      });

      new Zdog.Box({
        addTo: leg,
        translate: { y: 20 },
        width: 12,
        height: 40,
        depth: 12,
        stroke: 2,
        color: '#C25',
        fill: true
      });

      // Foot
      new Zdog.Box({
        addTo: leg,
        translate: { y: 42, z: 5 },
        width: 12,
        height: 8,
        depth: 20,
        stroke: 2,
        color: '#EA0',
        fill: true
      });
    });

    function animate() {
      if (isSpinning) {
        robot.rotate.y += 0.02;
      }
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const playBtn = document.createElement('button');
    playBtn.textContent = 'Pause';
    playBtn.addEventListener('click', () => {
      isSpinning = !isSpinning;
      playBtn.textContent = isSpinning ? 'Pause' : 'Play';
    });
    controls.appendChild(playBtn);

    const waveBtn = document.createElement('button');
    waveBtn.textContent = 'Wave';
    let waving = false;
    waveBtn.addEventListener('click', () => {
      if (!waving) {
        waving = true;
        // Simple wave animation would go here
        setTimeout(() => waving = false, 1000);
      }
    });
    controls.appendChild(waveBtn);"""

    return code


def generate_icon_grid():
    """Generate grid of animated icons"""
    code = """    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 3,
      dragRotate: true,
    });

    const icons = [];
    const colors = ['#636', '#E62', '#EA0', '#19F', '#C25', '#4A9'];
    let time = 0;

    // Create icon grid
    for (let x = -60; x <= 60; x += 40) {
      for (let y = -60; y <= 60; y += 40) {
        const iconGroup = new Zdog.Anchor({
          addTo: illo,
          translate: { x, y }
        });

        // Random icon type
        const iconType = Math.floor(Math.random() * 3);

        if (iconType === 0) {
          // Star
          new Zdog.Polygon({
            addTo: iconGroup,
            sides: 5,
            radius: 8,
            stroke: 2,
            color: colors[Math.floor(Math.random() * colors.length)],
            fill: true
          });
        } else if (iconType === 1) {
          // Heart
          new Zdog.Ellipse({
            addTo: iconGroup,
            diameter: 8,
            translate: { x: -4, y: -2 },
            stroke: 2,
            color: '#E62',
            fill: true
          });
          new Zdog.Ellipse({
            addTo: iconGroup,
            diameter: 8,
            translate: { x: 4, y: -2 },
            stroke: 2,
            color: '#E62',
            fill: true
          });
        } else {
          // Diamond
          new Zdog.Polygon({
            addTo: iconGroup,
            sides: 4,
            radius: 8,
            stroke: 2,
            color: colors[Math.floor(Math.random() * colors.length)],
            fill: true
          });
        }

        icons.push({
          group: iconGroup,
          baseY: y,
          phase: Math.random() * Math.PI * 2
        });
      }
    }

    function animate() {
      time += 0.03;

      // Animate each icon with sine wave
      icons.forEach(icon => {
        icon.group.translate.z = Math.sin(time + icon.phase) * 10;
        icon.group.rotate.z = Math.sin(time + icon.phase) * 0.5;
      });

      illo.rotate.y += 0.01;
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset View';
    resetBtn.addEventListener('click', () => {
      illo.rotate.x = 0;
      illo.rotate.y = 0;
      illo.rotate.z = 0;
    });
    controls.appendChild(resetBtn);"""

    return code


def generate_particle_system():
    """Generate particle system"""
    code = """    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 2,
      dragRotate: true,
    });

    const particles = [];
    const particleCount = 50;

    // Create particles
    for (let i = 0; i < particleCount; i++) {
      const particle = new Zdog.Ellipse({
        addTo: illo,
        diameter: 4,
        stroke: 2,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`,
        fill: true
      });

      particles.push({
        shape: particle,
        velocity: {
          x: (Math.random() - 0.5) * 3,
          y: (Math.random() - 0.5) * 3,
          z: (Math.random() - 0.5) * 3
        },
        rotation: {
          x: (Math.random() - 0.5) * 0.1,
          y: (Math.random() - 0.5) * 0.1,
          z: (Math.random() - 0.5) * 0.1
        }
      });
    }

    const bounds = 100;

    function animate() {
      particles.forEach(p => {
        // Update position
        p.shape.translate.x += p.velocity.x;
        p.shape.translate.y += p.velocity.y;
        p.shape.translate.z += p.velocity.z;

        // Update rotation
        p.shape.rotate.x += p.rotation.x;
        p.shape.rotate.y += p.rotation.y;
        p.shape.rotate.z += p.rotation.z;

        // Bounce off boundaries
        if (Math.abs(p.shape.translate.x) > bounds) {
          p.velocity.x *= -1;
        }
        if (Math.abs(p.shape.translate.y) > bounds) {
          p.velocity.y *= -1;
        }
        if (Math.abs(p.shape.translate.z) > bounds) {
          p.velocity.z *= -1;
        }
      });

      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset Particles';
    resetBtn.addEventListener('click', () => {
      particles.forEach(p => {
        p.shape.translate.x = 0;
        p.shape.translate.y = 0;
        p.shape.translate.z = 0;
      });
    });
    controls.appendChild(resetBtn);

    const speedUpBtn = document.createElement('button');
    speedUpBtn.textContent = 'Speed Up';
    speedUpBtn.addEventListener('click', () => {
      particles.forEach(p => {
        p.velocity.x *= 1.2;
        p.velocity.y *= 1.2;
        p.velocity.z *= 1.2;
      });
    });
    controls.appendChild(speedUpBtn);

    const slowDownBtn = document.createElement('button');
    slowDownBtn.textContent = 'Slow Down';
    slowDownBtn.addEventListener('click', () => {
      particles.forEach(p => {
        p.velocity.x *= 0.8;
        p.velocity.y *= 0.8;
        p.velocity.z *= 0.8;
      });
    });
    controls.appendChild(slowDownBtn);"""

    return code


def generate_spiral():
    """Generate spiral animation"""
    code = """    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 2,
      dragRotate: true,
    });

    let isSpinning = true;
    const spiral = new Zdog.Anchor({ addTo: illo });
    const spheres = [];

    // Create spiral
    const turns = 5;
    const sphereCount = 50;

    for (let i = 0; i < sphereCount; i++) {
      const progress = i / sphereCount;
      const angle = progress * Math.PI * 2 * turns;
      const radius = progress * 60;

      const hue = progress * 360;

      const sphere = new Zdog.Ellipse({
        addTo: spiral,
        diameter: 6,
        translate: {
          x: Math.cos(angle) * radius,
          y: progress * 80 - 40,
          z: Math.sin(angle) * radius
        },
        stroke: 3,
        color: `hsl(${hue}, 70%, 60%)`,
        fill: true
      });

      spheres.push({ shape: sphere, angle: angle, radius: radius });
    }

    let time = 0;

    function animate() {
      time += 0.02;

      if (isSpinning) {
        spiral.rotate.y += 0.02;
      }

      // Animate each sphere
      spheres.forEach((s, i) => {
        const progress = i / sphereCount;
        const wave = Math.sin(time + progress * Math.PI * 2) * 5;
        s.shape.translate.z = Math.sin(s.angle) * s.radius + wave;
      });

      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }

    animate();

    // Controls
    const controls = document.getElementById('controls');

    const playBtn = document.createElement('button');
    playBtn.textContent = 'Pause';
    playBtn.addEventListener('click', () => {
      isSpinning = !isSpinning;
      playBtn.textContent = isSpinning ? 'Pause' : 'Play';
    });
    controls.appendChild(playBtn);

    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset View';
    resetBtn.addEventListener('click', () => {
      illo.rotate.x = 0;
      illo.rotate.y = 0;
      illo.rotate.z = 0;
    });
    controls.appendChild(resetBtn);"""

    return code


ILLUSTRATION_TYPES = {
    'shapes': {
        'name': 'Basic Shapes',
        'description': 'Grid of all basic Zdog shapes',
        'generator': generate_basic_shapes
    },
    'cube': {
        'name': '3D Cube',
        'description': 'Animated 3D cube with colored faces',
        'generator': generate_3d_cube
    },
    'robot': {
        'name': 'Robot Character',
        'description': 'Complex robot model with multiple parts',
        'generator': generate_robot
    },
    'icons': {
        'name': 'Icon Grid',
        'description': 'Grid of animated icons with wave effect',
        'generator': generate_icon_grid
    },
    'particles': {
        'name': 'Particle System',
        'description': 'Bouncing particle system',
        'generator': generate_particle_system
    },
    'spiral': {
        'name': 'Spiral Animation',
        'description': 'Rotating spiral with wave animation',
        'generator': generate_spiral
    }
}


def list_types():
    """List all available illustration types"""
    print("\n📦 Available Zdog Illustration Types:\n")
    for key, info in ILLUSTRATION_TYPES.items():
        print(f"  {key:12} - {info['name']}")
        print(f"               {info['description']}")
        print()


def generate_illustration(type_key, output_path):
    """Generate Zdog illustration"""
    if type_key not in ILLUSTRATION_TYPES:
        print(f"❌ Error: Unknown type '{type_key}'")
        print(f"   Use --list to see available types")
        return False

    info = ILLUSTRATION_TYPES[type_key]

    print(f"\n🎨 Generating {info['name']}...")

    # Generate code
    code = info['generator']()

    # Create HTML
    html = create_html_template(info['name'], code)

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
    print("  🎨 Zdog Illustration Generator")
    print("="*60)

    print("\nSelect illustration type:\n")
    types_list = list(ILLUSTRATION_TYPES.keys())
    for i, key in enumerate(types_list, 1):
        info = ILLUSTRATION_TYPES[key]
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
    default_name = f"zdog_{type_key}.html"
    output_name = input(f"\nOutput filename [{default_name}]: ").strip()
    if not output_name:
        output_name = default_name

    output_path = Path.cwd() / output_name

    return generate_illustration(type_key, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Zdog pseudo-3D illustrations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--type',
        choices=list(ILLUSTRATION_TYPES.keys()),
        help='Illustration type to generate'
    )

    parser.add_argument(
        '--output',
        default='zdog_illustration.html',
        help='Output HTML file path (default: zdog_illustration.html)'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available illustration types'
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
    success = generate_illustration(args.type, args.output)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
