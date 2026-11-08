#!/usr/bin/env python3
"""
PixiJS Particle Builder
Generates high-performance particle systems using ParticleContainer.

Usage:
    Interactive mode:
        python particle_builder.py

    CLI mode:
        python particle_builder.py --type fountain --count 5000 --output ./
        python particle_builder.py -t fire -c 2000 -o ./my-project/
"""

import argparse
import os
import sys
from typing import Dict, Tuple


def generate_fountain_particles(count: int = 5000) -> str:
    """Generate fountain particle system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Fountain Particles</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #0a0a0a;
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>Fountain Particles</h3>
        <p>Particles: {count}</p>
        <p>FPS: <span id="fps">--</span></p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {{
            const app = new PIXI.Application();

            await app.init({{
                width: 800,
                height: 600,
                backgroundColor: 0x0a0a0a,
                antialias: true
            }});

            document.body.appendChild(app.canvas);

            // Create particle texture
            const graphics = new PIXI.Graphics();
            graphics.circle(5, 5, 5).fill(0xffffff);
            const particleTexture = app.renderer.generateTexture(graphics);

            // Create particle container
            const particles = new PIXI.ParticleContainer({{
                maxSize: {count},
                dynamicProperties: {{
                    position: true,
                    scale: true,
                    rotation: false,
                    color: true
                }}
            }});

            app.stage.addChild(particles);

            // Particle data
            const particleData = [];

            for (let i = 0; i < {count}; i++) {{
                const particle = new PIXI.Particle({{
                    texture: particleTexture,
                    x: 400,
                    y: 550
                }});

                particles.addParticle(particle);

                particleData.push({{
                    particle,
                    vx: (Math.random() - 0.5) * 8,
                    vy: -(Math.random() * 12 + 8),
                    life: 1.0,
                    gravity: 0.2
                }});
            }}

            // Update loop
            app.ticker.add((ticker) => {{
                particleData.forEach(data => {{
                    // Physics
                    data.particle.x += data.vx * ticker.deltaTime;
                    data.particle.y += data.vy * ticker.deltaTime;
                    data.vy += data.gravity * ticker.deltaTime;

                    // Fade out
                    data.life -= 0.01 * ticker.deltaTime;

                    if (data.life > 0) {{
                        const color = Math.floor(data.life * 255);
                        data.particle.tint = (color << 16) | (color << 8) | 255;
                        data.particle.alpha = data.life;
                    }} else {{
                        // Reset particle
                        data.particle.x = 400;
                        data.particle.y = 550;
                        data.vx = (Math.random() - 0.5) * 8;
                        data.vy = -(Math.random() * 12 + 8);
                        data.life = 1.0;
                    }}
                }});

                // Update FPS
                document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            }});
        }})();
    </script>
</body>
</html>"""


def generate_fire_particles(count: int = 2000) -> str:
    """Generate fire particle system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Fire Particles</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a0a00;
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>Fire Particles</h3>
        <p>Particles: {count}</p>
        <p>FPS: <span id="fps">--</span></p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {{
            const app = new PIXI.Application();

            await app.init({{
                width: 800,
                height: 600,
                backgroundColor: 0x1a0a00,
                antialias: true
            }});

            document.body.appendChild(app.canvas);

            // Create particle texture
            const graphics = new PIXI.Graphics();
            graphics.circle(8, 8, 8).fill(0xffffff);
            const particleTexture = app.renderer.generateTexture(graphics);

            // Create particle container
            const particles = new PIXI.ParticleContainer({{
                maxSize: {count},
                dynamicProperties: {{
                    position: true,
                    scale: true,
                    rotation: true,
                    color: true
                }}
            }});

            app.stage.addChild(particles);

            // Particle data
            const particleData = [];

            for (let i = 0; i < {count}; i++) {{
                const particle = new PIXI.Particle({{
                    texture: particleTexture,
                    x: 400,
                    y: 550
                }});

                particles.addParticle(particle);

                particleData.push({{
                    particle,
                    vx: (Math.random() - 0.5) * 2,
                    vy: -(Math.random() * 3 + 2),
                    life: Math.random(),
                    maxLife: Math.random() * 0.5 + 0.5
                }});
            }}

            // Update loop
            app.ticker.add((ticker) => {{
                particleData.forEach(data => {{
                    // Physics
                    data.particle.x += data.vx * ticker.deltaTime;
                    data.particle.y += data.vy * ticker.deltaTime;

                    // Wind
                    data.vx += (Math.random() - 0.5) * 0.1 * ticker.deltaTime;

                    // Rise
                    data.vy -= 0.05 * ticker.deltaTime;

                    // Fade
                    data.life -= 0.01 * ticker.deltaTime;

                    if (data.life > 0) {{
                        const t = data.life / data.maxLife;

                        // Color gradient: yellow -> orange -> red -> black
                        let r, g, b;
                        if (t > 0.66) {{
                            // Yellow to orange
                            const localT = (t - 0.66) / 0.34;
                            r = 255;
                            g = Math.floor(255 * localT);
                            b = 0;
                        }} else if (t > 0.33) {{
                            // Orange to red
                            const localT = (t - 0.33) / 0.33;
                            r = 255;
                            g = Math.floor(128 * localT);
                            b = 0;
                        }} else {{
                            // Red to black
                            r = Math.floor(255 * (t / 0.33));
                            g = 0;
                            b = 0;
                        }}

                        data.particle.tint = (r << 16) | (g << 8) | b;
                        data.particle.alpha = t;
                        data.particle.scaleX = t * 1.5;
                        data.particle.scaleY = t * 1.5;
                        data.particle.rotation += 0.1 * ticker.deltaTime;
                    }} else {{
                        // Reset particle
                        data.particle.x = 400 + (Math.random() - 0.5) * 100;
                        data.particle.y = 550;
                        data.vx = (Math.random() - 0.5) * 2;
                        data.vy = -(Math.random() * 3 + 2);
                        data.life = data.maxLife;
                    }}
                }});

                document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            }});
        }})();
    </script>
</body>
</html>"""


def generate_snow_particles(count: int = 3000) -> str:
    """Generate snow particle system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Snow Particles</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: linear-gradient(to bottom, #2c3e50, #34495e);
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>Snow Particles</h3>
        <p>Particles: {count}</p>
        <p>FPS: <span id="fps">--</span></p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {{
            const app = new PIXI.Application();

            await app.init({{
                width: 800,
                height: 600,
                backgroundAlpha: 0,
                antialias: true
            }});

            document.body.appendChild(app.canvas);

            // Create snowflake texture
            const graphics = new PIXI.Graphics();
            graphics.circle(3, 3, 3).fill(0xffffff);
            const snowTexture = app.renderer.generateTexture(graphics);

            // Create particle container
            const particles = new PIXI.ParticleContainer({{
                maxSize: {count},
                dynamicProperties: {{
                    position: true,
                    scale: true,
                    rotation: true,
                    color: false
                }}
            }});

            app.stage.addChild(particles);

            // Particle data
            const particleData = [];

            for (let i = 0; i < {count}; i++) {{
                const particle = new PIXI.Particle({{
                    texture: snowTexture,
                    x: Math.random() * 800,
                    y: Math.random() * 600,
                    scaleX: Math.random() * 0.5 + 0.5,
                    scaleY: Math.random() * 0.5 + 0.5,
                    alpha: Math.random() * 0.5 + 0.5
                }});

                particles.addParticle(particle);

                particleData.push({{
                    particle,
                    speed: Math.random() * 1 + 0.5,
                    sway: Math.random() * Math.PI * 2,
                    swaySpeed: Math.random() * 0.02 + 0.01
                }});
            }}

            // Update loop
            app.ticker.add((ticker) => {{
                particleData.forEach(data => {{
                    // Fall down
                    data.particle.y += data.speed * ticker.deltaTime;

                    // Sway left and right
                    data.sway += data.swaySpeed * ticker.deltaTime;
                    data.particle.x += Math.sin(data.sway) * 0.5 * ticker.deltaTime;

                    // Rotate
                    data.particle.rotation += 0.01 * ticker.deltaTime;

                    // Reset if below screen
                    if (data.particle.y > 600) {{
                        data.particle.y = -10;
                        data.particle.x = Math.random() * 800;
                    }}
                }});

                document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            }});
        }})();
    </script>
</body>
</html>"""


def generate_explosion_particles(count: int = 1000) -> str:
    """Generate explosion particle system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Explosion Particles</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #0a0a0a;
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>Explosion Particles</h3>
        <p>Click to explode</p>
        <p>FPS: <span id="fps">--</span></p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {{
            const app = new PIXI.Application();

            await app.init({{
                width: 800,
                height: 600,
                backgroundColor: 0x0a0a0a,
                antialias: true
            }});

            document.body.appendChild(app.canvas);

            // Create particle texture
            const graphics = new PIXI.Graphics();
            graphics.circle(4, 4, 4).fill(0xffffff);
            const particleTexture = app.renderer.generateTexture(graphics);

            // Create particle container
            const particles = new PIXI.ParticleContainer({{
                maxSize: {count},
                dynamicProperties: {{
                    position: true,
                    scale: true,
                    rotation: false,
                    color: true
                }}
            }});

            app.stage.addChild(particles);

            // Particle pool
            const particleData = [];

            for (let i = 0; i < {count}; i++) {{
                const particle = new PIXI.Particle({{
                    texture: particleTexture,
                    x: -100,
                    y: -100
                }});

                particle.alpha = 0;
                particles.addParticle(particle);

                particleData.push({{
                    particle,
                    vx: 0,
                    vy: 0,
                    life: 0,
                    active: false
                }});
            }}

            // Explosion function
            function explode(x, y) {{
                let spawned = 0;

                particleData.forEach(data => {{
                    if (!data.active && spawned < 100) {{
                        const angle = Math.random() * Math.PI * 2;
                        const speed = Math.random() * 8 + 4;

                        data.particle.x = x;
                        data.particle.y = y;
                        data.vx = Math.cos(angle) * speed;
                        data.vy = Math.sin(angle) * speed;
                        data.life = 1.0;
                        data.active = true;
                        data.particle.alpha = 1;

                        spawned++;
                    }}
                }});
            }}

            // Click to explode
            app.canvas.addEventListener('click', (e) => {{
                const rect = app.canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                explode(x, y);
            }});

            // Update loop
            app.ticker.add((ticker) => {{
                particleData.forEach(data => {{
                    if (data.active) {{
                        // Physics
                        data.particle.x += data.vx * ticker.deltaTime;
                        data.particle.y += data.vy * ticker.deltaTime;

                        // Gravity
                        data.vy += 0.2 * ticker.deltaTime;

                        // Drag
                        data.vx *= 0.98;
                        data.vy *= 0.98;

                        // Fade
                        data.life -= 0.02 * ticker.deltaTime;

                        if (data.life > 0) {{
                            // Color: white -> yellow -> orange -> red
                            let r, g, b;
                            if (data.life > 0.75) {{
                                r = 255;
                                g = 255;
                                b = 255;
                            }} else if (data.life > 0.5) {{
                                r = 255;
                                g = 255;
                                b = Math.floor((data.life - 0.5) * 4 * 255);
                            }} else if (data.life > 0.25) {{
                                r = 255;
                                g = Math.floor((data.life - 0.25) * 4 * 255);
                                b = 0;
                            }} else {{
                                r = Math.floor(data.life * 4 * 255);
                                g = 0;
                                b = 0;
                            }}

                            data.particle.tint = (r << 16) | (g << 8) | b;
                            data.particle.alpha = data.life;
                            data.particle.scaleX = data.life;
                            data.particle.scaleY = data.life;
                        }} else {{
                            data.active = false;
                            data.particle.alpha = 0;
                        }}
                    }}
                }});

                document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            }});

            // Initial explosion
            explode(400, 300);
        }})();
    </script>
</body>
</html>"""


def generate_stars_particles(count: int = 5000) -> str:
    """Generate starfield particle system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Starfield</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #000000;
        }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>Starfield</h3>
        <p>Stars: {count}</p>
        <p>FPS: <span id="fps">--</span></p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {{
            const app = new PIXI.Application();

            await app.init({{
                width: 800,
                height: 600,
                backgroundColor: 0x000000,
                antialias: true
            }});

            document.body.appendChild(app.canvas);

            // Create star texture
            const graphics = new PIXI.Graphics();
            graphics.circle(2, 2, 2).fill(0xffffff);
            const starTexture = app.renderer.generateTexture(graphics);

            // Create particle container
            const particles = new PIXI.ParticleContainer({{
                maxSize: {count},
                dynamicProperties: {{
                    position: true,
                    scale: true,
                    rotation: false,
                    color: false
                }}
            }});

            app.stage.addChild(particles);

            // Particle data
            const particleData = [];

            for (let i = 0; i < {count}; i++) {{
                const particle = new PIXI.Particle({{
                    texture: starTexture,
                    x: Math.random() * 800,
                    y: Math.random() * 600,
                    scaleX: Math.random(),
                    scaleY: Math.random(),
                    alpha: Math.random()
                }});

                particles.addParticle(particle);

                particleData.push({{
                    particle,
                    z: Math.random() * 1000,
                    speed: Math.random() * 2 + 1
                }});
            }}

            // Update loop
            const centerX = 400;
            const centerY = 300;

            app.ticker.add((ticker) => {{
                particleData.forEach(data => {{
                    // Move toward camera
                    data.z -= data.speed * ticker.deltaTime;

                    if (data.z <= 0) {{
                        data.z = 1000;
                    }}

                    // Project 3D to 2D
                    const scale = 1000 / data.z;
                    const x = (data.particle.x - centerX) * scale + centerX;
                    const y = (data.particle.y - centerY) * scale + centerY;

                    data.particle.x = x;
                    data.particle.y = y;
                    data.particle.scaleX = scale;
                    data.particle.scaleY = scale;
                    data.particle.alpha = Math.min(scale, 1);

                    // Reset if off screen
                    if (x < 0 || x > 800 || y < 0 || y > 600) {{
                        data.particle.x = Math.random() * 800;
                        data.particle.y = Math.random() * 600;
                        data.z = 1000;
                    }}
                }});

                document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            }});
        }})();
    </script>
</body>
</html>"""


# Particle type registry
PARTICLE_TYPES: Dict[str, Dict] = {
    'fountain': {
        'name': 'Fountain',
        'description': 'Particles shooting upward with gravity',
        'default_count': 5000,
        'generator': generate_fountain_particles
    },
    'fire': {
        'name': 'Fire',
        'description': 'Fire effect with color gradient',
        'default_count': 2000,
        'generator': generate_fire_particles
    },
    'snow': {
        'name': 'Snow',
        'description': 'Falling snowflakes with sway',
        'default_count': 3000,
        'generator': generate_snow_particles
    },
    'explosion': {
        'name': 'Explosion',
        'description': 'Click-triggered explosions',
        'default_count': 1000,
        'generator': generate_explosion_particles
    },
    'stars': {
        'name': 'Starfield',
        'description': '3D starfield effect',
        'default_count': 5000,
        'generator': generate_stars_particles
    }
}


def interactive_mode():
    """Run interactive particle builder"""
    print("\n" + "="*60)
    print("PixiJS Particle Builder - Interactive Mode")
    print("="*60)

    # Show particle types
    print("\nAvailable particle systems:")
    print("-" * 60)
    for idx, (key, info) in enumerate(PARTICLE_TYPES.items(), 1):
        print(f"{idx}. {info['name']:15} - {info['description']} ({info['default_count']} particles)")

    # Get particle type
    while True:
        try:
            choice = input(f"\nSelect particle type (1-{len(PARTICLE_TYPES)}): ").strip()
            idx = int(choice)
            if 1 <= idx <= len(PARTICLE_TYPES):
                particle_type = list(PARTICLE_TYPES.keys())[idx - 1]
                break
            print(f"Error: Please enter a number between 1 and {len(PARTICLE_TYPES)}")
        except ValueError:
            print("Error: Please enter a valid number")

    # Get particle count
    default_count = PARTICLE_TYPES[particle_type]['default_count']
    count_input = input(f"\nParticle count (default: {default_count}): ").strip()
    count = int(count_input) if count_input else default_count

    # Get output directory
    output_dir = input("\nOutput directory (default: current directory): ").strip()
    if not output_dir:
        output_dir = "."

    # Generate particles
    print("\n" + "-"*60)
    print("Generating particle system...")

    try:
        generator = PARTICLE_TYPES[particle_type]['generator']
        html = generator(count)

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Write HTML file
        filename = f"{particle_type}_particles.html"
        html_path = os.path.join(output_dir, filename)

        with open(html_path, 'w') as f:
            f.write(html)

        print(f"\n✓ Particle system created: {html_path}")
        print(f"\nParticle type: {PARTICLE_TYPES[particle_type]['name']}")
        print(f"Particle count: {count}")
        print(f"Lines of code: {len(html.splitlines())}")

        print("\nTo view:")
        print(f"  Open {html_path} in a web browser")
        print(f"  Or run: python -m http.server 8000")

    except Exception as e:
        print(f"\nError: Failed to generate particle system: {e}")
        return 1

    return 0


def cli_mode(args):
    """Run CLI particle builder"""
    particle_type = args.type
    count = args.count
    output_dir = args.output

    # Validate particle type
    if particle_type not in PARTICLE_TYPES:
        print(f"Error: Unknown particle type '{particle_type}'")
        print(f"Available types: {', '.join(PARTICLE_TYPES.keys())}")
        return 1

    # Use default count if not specified
    if count is None:
        count = PARTICLE_TYPES[particle_type]['default_count']

    # Generate particles
    try:
        generator = PARTICLE_TYPES[particle_type]['generator']
        html = generator(count)

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Write HTML file
        filename = f"{particle_type}_particles.html"
        html_path = os.path.join(output_dir, filename)

        with open(html_path, 'w') as f:
            f.write(html)

        print(f"✓ Particle system created: {html_path}")
        return 0

    except Exception as e:
        print(f"Error: Failed to generate particle system: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='PixiJS Particle Builder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python particle_builder.py

  Generate fountain particles:
    python particle_builder.py --type fountain --count 5000 --output ./

  Generate fire particles:
    python particle_builder.py -t fire -c 2000 -o ./effects/

  Generate snow particles:
    python particle_builder.py -t snow -c 3000

Available particle types:
  fountain   - Particles shooting upward with gravity
  fire       - Fire effect with color gradient
  snow       - Falling snowflakes with sway
  explosion  - Click-triggered explosions
  stars      - 3D starfield effect
        """
    )

    parser.add_argument(
        '-t', '--type',
        choices=list(PARTICLE_TYPES.keys()),
        help='Particle system type'
    )

    parser.add_argument(
        '-c', '--count',
        type=int,
        help='Number of particles'
    )

    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory (default: current directory)'
    )

    args = parser.parse_args()

    # Run interactive mode if no particle type specified
    if not args.type:
        return interactive_mode()

    return cli_mode(args)


if __name__ == '__main__':
    sys.exit(main())
