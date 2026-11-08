#!/usr/bin/env python3
"""
PixiJS Sprite Generator
Generates PixiJS sprite-based applications with various templates.

Usage:
    Interactive mode:
        python sprite_generator.py

    CLI mode:
        python sprite_generator.py --type basic --output ./
        python sprite_generator.py -t interactive -o ./my-project/
        python sprite_generator.py -t animated --name MySprite
"""

import argparse
import os
import sys
from typing import Dict, Tuple


def generate_basic_sprite() -> Tuple[str, str]:
    """Generate basic sprite example"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Basic Sprite</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a2e;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h3>Basic Sprite</h3>
        <p>Click the sprite to change color</p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            // Create application
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x1a1a2e,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Create sprite
            const graphics = new PIXI.Graphics();
            graphics.rect(0, 0, 100, 100).fill(0x3498db);

            const texture = app.renderer.generateTexture(graphics);
            const sprite = new PIXI.Sprite(texture);

            sprite.anchor.set(0.5);
            sprite.position.set(400, 300);
            sprite.eventMode = 'static';
            sprite.cursor = 'pointer';

            app.stage.addChild(sprite);

            // Rotate animation
            app.ticker.add((ticker) => {
                sprite.rotation += 0.01 * ticker.deltaTime;
            });

            // Click event
            const colors = [0x3498db, 0xe74c3c, 0x2ecc71, 0xf39c12, 0x9b59b6];
            let colorIndex = 0;

            sprite.on('pointerdown', () => {
                colorIndex = (colorIndex + 1) % colors.length;

                const newGraphics = new PIXI.Graphics();
                newGraphics.rect(0, 0, 100, 100).fill(colors[colorIndex]);
                sprite.texture = app.renderer.generateTexture(newGraphics);
            });
        })();
    </script>
</body>
</html>"""

    js = """// Standalone JavaScript version
import { Application, Sprite, Graphics } from 'pixi.js';

(async () => {
    const app = new Application();

    await app.init({
        width: 800,
        height: 600,
        backgroundColor: 0x1a1a2e,
        antialias: true
    });

    document.body.appendChild(app.canvas);

    // Create sprite
    const graphics = new Graphics();
    graphics.rect(0, 0, 100, 100).fill(0x3498db);

    const texture = app.renderer.generateTexture(graphics);
    const sprite = new Sprite(texture);

    sprite.anchor.set(0.5);
    sprite.position.set(400, 300);
    sprite.eventMode = 'static';
    sprite.cursor = 'pointer';

    app.stage.addChild(sprite);

    // Rotate animation
    app.ticker.add((ticker) => {
        sprite.rotation += 0.01 * ticker.deltaTime;
    });

    // Click event
    const colors = [0x3498db, 0xe74c3c, 0x2ecc71, 0xf39c12, 0x9b59b6];
    let colorIndex = 0;

    sprite.on('pointerdown', () => {
        colorIndex = (colorIndex + 1) % colors.length;

        const newGraphics = new Graphics();
        newGraphics.rect(0, 0, 100, 100).fill(colors[colorIndex]);
        sprite.texture = app.renderer.generateTexture(newGraphics);
    });
})();
"""

    return html, js


def generate_interactive_sprite() -> Tuple[str, str]:
    """Generate interactive sprite with drag and hover"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Interactive Sprite</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #0f0f23;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h3>Interactive Sprite</h3>
        <p>Drag to move • Hover to scale</p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x0f0f23,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Create draggable sprite
            function createDraggableSprite(x, y, color) {
                const graphics = new PIXI.Graphics();
                graphics.circle(50, 50, 50).fill(color);

                const texture = app.renderer.generateTexture(graphics);
                const sprite = new PIXI.Sprite(texture);

                sprite.anchor.set(0.5);
                sprite.position.set(x, y);
                sprite.eventMode = 'static';
                sprite.cursor = 'pointer';

                // Drag state
                sprite.dragging = false;
                sprite.dragData = null;
                sprite.originalScale = 1.0;

                // Pointer events
                sprite.on('pointerdown', onDragStart);
                sprite.on('pointerup', onDragEnd);
                sprite.on('pointerupoutside', onDragEnd);
                sprite.on('pointermove', onDragMove);
                sprite.on('pointerover', onHoverStart);
                sprite.on('pointerout', onHoverEnd);

                function onDragStart(event) {
                    sprite.dragging = true;
                    sprite.dragData = event.data;
                    sprite.alpha = 0.7;
                }

                function onDragEnd() {
                    sprite.dragging = false;
                    sprite.dragData = null;
                    sprite.alpha = 1.0;
                }

                function onDragMove() {
                    if (sprite.dragging) {
                        const newPosition = sprite.dragData.global;
                        sprite.position.set(newPosition.x, newPosition.y);
                    }
                }

                function onHoverStart() {
                    app.canvas.style.cursor = 'grab';
                    if (!sprite.dragging) {
                        sprite.scale.set(1.2);
                    }
                }

                function onHoverEnd() {
                    app.canvas.style.cursor = 'default';
                    if (!sprite.dragging) {
                        sprite.scale.set(sprite.originalScale);
                    }
                }

                return sprite;
            }

            // Create multiple draggable sprites
            const colors = [0xe74c3c, 0x3498db, 0x2ecc71, 0xf39c12, 0x9b59b6];

            for (let i = 0; i < 5; i++) {
                const x = 150 + i * 120;
                const y = 300;
                const sprite = createDraggableSprite(x, y, colors[i]);
                app.stage.addChild(sprite);
            }
        })();
    </script>
</body>
</html>"""

    js = ""  # Standalone JS same as embedded
    return html, js


def generate_animated_sprite() -> Tuple[str, str]:
    """Generate sprite sheet animation"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Animated Sprite</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #2c3e50;
        }
        #controls {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
        button {
            margin: 5px;
            padding: 5px 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="controls">
        <h3>Animated Sprite</h3>
        <button id="play">Play</button>
        <button id="stop">Stop</button>
        <button id="faster">Faster</button>
        <button id="slower">Slower</button>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x2c3e50,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Generate sprite sheet frames
            const frames = [];
            for (let i = 0; i < 12; i++) {
                const graphics = new PIXI.Graphics();

                // Animate a growing/shrinking circle
                const scale = 0.5 + Math.sin(i / 12 * Math.PI * 2) * 0.5;
                const radius = 50 * scale;

                graphics.circle(50, 50, radius).fill(0x3498db);

                const texture = app.renderer.generateTexture(graphics);
                frames.push(texture);
            }

            // Create animated sprite
            const animation = new PIXI.AnimatedSprite(frames);
            animation.anchor.set(0.5);
            animation.position.set(400, 300);
            animation.animationSpeed = 0.16;
            animation.play();

            app.stage.addChild(animation);

            // Controls
            document.getElementById('play').addEventListener('click', () => {
                animation.play();
            });

            document.getElementById('stop').addEventListener('click', () => {
                animation.stop();
            });

            document.getElementById('faster').addEventListener('click', () => {
                animation.animationSpeed *= 1.5;
            });

            document.getElementById('slower').addEventListener('click', () => {
                animation.animationSpeed /= 1.5;
            });

            // Rotate animation
            app.ticker.add((ticker) => {
                animation.rotation += 0.01 * ticker.deltaTime;
            });
        })();
    </script>
</body>
</html>"""

    js = ""
    return html, js


def generate_tiled_sprites() -> Tuple[str, str]:
    """Generate tiled sprite pattern"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Tiled Sprites</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #34495e;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h3>Tiled Sprites</h3>
        <p>Scrolling background pattern</p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x34495e,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Create tile texture
            const graphics = new PIXI.Graphics();
            graphics.rect(0, 0, 64, 64).fill(0x3498db);
            graphics.rect(4, 4, 56, 56).fill(0x2980b9);

            const tileTexture = app.renderer.generateTexture(graphics);

            // Create tiling sprite
            const tilingSprite = new PIXI.TilingSprite({
                texture: tileTexture,
                width: app.screen.width,
                height: app.screen.height
            });

            app.stage.addChild(tilingSprite);

            // Scroll animation
            app.ticker.add((ticker) => {
                tilingSprite.tilePosition.x += 1 * ticker.deltaTime;
                tilingSprite.tilePosition.y += 0.5 * ticker.deltaTime;
            });
        })();
    </script>
</body>
</html>"""

    js = ""
    return html, js


def generate_spritesheet_atlas() -> Tuple[str, str]:
    """Generate sprite sheet with texture atlas"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Sprite Sheet</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #1a1a2e;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h3>Sprite Sheet Atlas</h3>
        <p>Multiple sprites from texture atlas</p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x1a1a2e,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Create texture atlas (sprite sheet)
            const atlas = {};
            const shapes = ['circle', 'square', 'triangle', 'star', 'hexagon'];
            const colors = [0xe74c3c, 0x3498db, 0x2ecc71, 0xf39c12, 0x9b59b6];

            shapes.forEach((shape, index) => {
                const graphics = new PIXI.Graphics();

                switch(shape) {
                    case 'circle':
                        graphics.circle(25, 25, 25).fill(colors[index]);
                        break;
                    case 'square':
                        graphics.rect(0, 0, 50, 50).fill(colors[index]);
                        break;
                    case 'triangle':
                        graphics.poly([25, 0, 50, 50, 0, 50]).fill(colors[index]);
                        break;
                    case 'star':
                        graphics.star(25, 25, 5, 25).fill(colors[index]);
                        break;
                    case 'hexagon':
                        graphics.poly([
                            25, 0, 45, 12.5, 45, 37.5, 25, 50, 5, 37.5, 5, 12.5
                        ]).fill(colors[index]);
                        break;
                }

                atlas[shape] = app.renderer.generateTexture(graphics);
            });

            // Create sprites from atlas
            shapes.forEach((shape, index) => {
                const sprite = new PIXI.Sprite(atlas[shape]);
                sprite.anchor.set(0.5);
                sprite.position.set(150 + index * 120, 300);
                sprite.eventMode = 'static';
                sprite.cursor = 'pointer';

                // Hover effect
                sprite.on('pointerover', () => {
                    sprite.scale.set(1.2);
                });

                sprite.on('pointerout', () => {
                    sprite.scale.set(1.0);
                });

                // Click to rotate
                sprite.on('pointerdown', () => {
                    sprite.rotation += Math.PI / 4;
                });

                app.stage.addChild(sprite);

                // Floating animation
                const startY = sprite.y;
                app.ticker.add(() => {
                    sprite.y = startY + Math.sin(Date.now() * 0.001 + index) * 20;
                });
            });
        })();
    </script>
</body>
</html>"""

    js = ""
    return html, js


def generate_masked_sprite() -> Tuple[str, str]:
    """Generate sprite with mask"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PixiJS Masked Sprite</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #2c3e50;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h3>Masked Sprite</h3>
        <p>Circular mask reveals gradient</p>
    </div>

    <script src="https://pixijs.download/release/pixi.js"></script>
    <script>
        (async () => {
            const app = new PIXI.Application();

            await app.init({
                width: 800,
                height: 600,
                backgroundColor: 0x2c3e50,
                antialias: true
            });

            document.body.appendChild(app.canvas);

            // Create gradient texture
            const canvas = document.createElement('canvas');
            canvas.width = 400;
            canvas.height = 400;
            const ctx = canvas.getContext('2d');

            const gradient = ctx.createLinearGradient(0, 0, 400, 400);
            gradient.addColorStop(0, '#e74c3c');
            gradient.addColorStop(0.5, '#3498db');
            gradient.addColorStop(1, '#2ecc71');

            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, 400, 400);

            const gradientTexture = PIXI.Texture.from(canvas);
            const sprite = new PIXI.Sprite(gradientTexture);
            sprite.anchor.set(0.5);
            sprite.position.set(400, 300);

            // Create circular mask
            const mask = new PIXI.Graphics();
            mask.circle(400, 300, 150).fill(0xffffff);

            sprite.mask = mask;

            app.stage.addChild(mask, sprite);

            // Animate mask
            let growing = true;
            let radius = 150;

            app.ticker.add((ticker) => {
                sprite.rotation += 0.01 * ticker.deltaTime;

                // Pulse mask
                if (growing) {
                    radius += 1;
                    if (radius > 200) growing = false;
                } else {
                    radius -= 1;
                    if (radius < 100) growing = true;
                }

                mask.clear();
                mask.circle(400, 300, radius).fill(0xffffff);
            });
        })();
    </script>
</body>
</html>"""

    js = ""
    return html, js


# Sprite type registry
SPRITE_TYPES: Dict[str, Dict] = {
    'basic': {
        'name': 'Basic Sprite',
        'description': 'Simple rotating sprite with color change on click',
        'generator': generate_basic_sprite
    },
    'interactive': {
        'name': 'Interactive Sprite',
        'description': 'Draggable sprites with hover effects',
        'generator': generate_interactive_sprite
    },
    'animated': {
        'name': 'Animated Sprite',
        'description': 'Sprite sheet animation with playback controls',
        'generator': generate_animated_sprite
    },
    'tiled': {
        'name': 'Tiled Sprite',
        'description': 'Scrolling background with tiling sprite',
        'generator': generate_tiled_sprites
    },
    'atlas': {
        'name': 'Sprite Sheet Atlas',
        'description': 'Multiple sprites from texture atlas',
        'generator': generate_spritesheet_atlas
    },
    'masked': {
        'name': 'Masked Sprite',
        'description': 'Sprite with animated circular mask',
        'generator': generate_masked_sprite
    }
}


def interactive_mode():
    """Run interactive sprite generator"""
    print("\n" + "="*60)
    print("PixiJS Sprite Generator - Interactive Mode")
    print("="*60)

    # Show sprite types
    print("\nAvailable sprite types:")
    print("-" * 60)
    for idx, (key, info) in enumerate(SPRITE_TYPES.items(), 1):
        print(f"{idx}. {info['name']:25} - {info['description']}")

    # Get sprite type
    while True:
        try:
            choice = input(f"\nSelect sprite type (1-{len(SPRITE_TYPES)}): ").strip()
            idx = int(choice)
            if 1 <= idx <= len(SPRITE_TYPES):
                sprite_type = list(SPRITE_TYPES.keys())[idx - 1]
                break
            print(f"Error: Please enter a number between 1 and {len(SPRITE_TYPES)}")
        except ValueError:
            print("Error: Please enter a valid number")

    # Get output directory
    output_dir = input("\nOutput directory (default: current directory): ").strip()
    if not output_dir:
        output_dir = "."

    # Get filename
    filename = input("\nFilename (default: sprite.html): ").strip()
    if not filename:
        filename = "sprite.html"

    if not filename.endswith('.html'):
        filename += '.html'

    # Generate sprite
    print("\n" + "-"*60)
    print("Generating sprite...")

    try:
        generator = SPRITE_TYPES[sprite_type]['generator']
        html, js = generator()

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Write HTML file
        html_path = os.path.join(output_dir, filename)
        with open(html_path, 'w') as f:
            f.write(html)

        print(f"\n✓ Sprite created: {html_path}")
        print(f"\nSprite type: {SPRITE_TYPES[sprite_type]['name']}")
        print(f"Lines of code: {len(html.splitlines())}")

        print("\nTo view:")
        print(f"  Open {html_path} in a web browser")
        print(f"  Or run: python -m http.server 8000")

    except Exception as e:
        print(f"\nError: Failed to generate sprite: {e}")
        return 1

    return 0


def cli_mode(args):
    """Run CLI sprite generator"""
    sprite_type = args.type
    output_dir = args.output
    name = args.name or 'sprite'

    # Validate sprite type
    if sprite_type not in SPRITE_TYPES:
        print(f"Error: Unknown sprite type '{sprite_type}'")
        print(f"Available types: {', '.join(SPRITE_TYPES.keys())}")
        return 1

    # Generate sprite
    try:
        generator = SPRITE_TYPES[sprite_type]['generator']
        html, js = generator()

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Write HTML file
        filename = f"{name}.html"
        html_path = os.path.join(output_dir, filename)

        with open(html_path, 'w') as f:
            f.write(html)

        print(f"✓ Sprite created: {html_path}")
        return 0

    except Exception as e:
        print(f"Error: Failed to generate sprite: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='PixiJS Sprite Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python sprite_generator.py

  Generate basic sprite:
    python sprite_generator.py --type basic --output ./

  Generate interactive sprite:
    python sprite_generator.py -t interactive -o ./my-project/

  Generate animated sprite:
    python sprite_generator.py -t animated --name MyAnimation

Available sprite types:
  basic       - Simple rotating sprite with color change
  interactive - Draggable sprites with hover effects
  animated    - Sprite sheet animation with controls
  tiled       - Scrolling background pattern
  atlas       - Multiple sprites from texture atlas
  masked      - Sprite with animated mask
        """
    )

    parser.add_argument(
        '-t', '--type',
        choices=list(SPRITE_TYPES.keys()),
        help='Sprite type'
    )

    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '-n', '--name',
        help='Output filename (default: sprite)'
    )

    args = parser.parse_args()

    # Run interactive mode if no sprite type specified
    if not args.type:
        return interactive_mode()

    return cli_mode(args)


if __name__ == '__main__':
    sys.exit(main())
