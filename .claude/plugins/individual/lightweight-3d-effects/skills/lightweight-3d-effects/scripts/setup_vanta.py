#!/usr/bin/env python3
"""
Vanta.js Background Setup Script

Generates Vanta.js animated backgrounds with various effects and configurations.

Usage:
    python setup_vanta.py                      # Interactive mode
    python setup_vanta.py --effect waves       # Generate waves effect
    python setup_vanta.py --list               # List available effects
"""

import argparse
import os
import sys
from pathlib import Path


def create_html_template(title, effect_name, effect_code, css_styles=""):
    """Create complete HTML template with Vanta.js effect"""
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
      overflow-x: hidden;
    }}

    #vanta-bg {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100vh;
      z-index: -1;
    }}

    .container {{
      position: relative;
      z-index: 1;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
      text-align: center;
      padding: 2rem;
    }}

    h1 {{
      font-size: 4rem;
      margin-bottom: 1rem;
      text-shadow: 0 4px 20px rgba(0,0,0,0.3);
      font-weight: 700;
    }}

    .subtitle {{
      font-size: 1.5rem;
      opacity: 0.9;
      margin-bottom: 2rem;
      text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}

    .controls {{
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
      flex-wrap: wrap;
      justify-content: center;
    }}

    button {{
      padding: 1rem 2rem;
      font-size: 1rem;
      background: rgba(255, 255, 255, 0.2);
      color: white;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 50px;
      cursor: pointer;
      transition: all 0.3s;
      backdrop-filter: blur(10px);
      font-weight: 600;
    }}

    button:hover {{
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}

    button:active {{
      transform: translateY(0);
    }}

    .card {{
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      padding: 3rem;
      margin-top: 3rem;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      max-width: 600px;
    }}

    .card h2 {{
      margin-bottom: 1rem;
      font-size: 2rem;
    }}

    .card p {{
      font-size: 1.1rem;
      line-height: 1.6;
      opacity: 0.9;
    }}

    {css_styles}
  </style>
</head>
<body>
  <div id="vanta-bg"></div>

  <div class="container">
    <h1>{title}</h1>
    <div class="subtitle">Animated with Vanta.js {effect_name} effect</div>

    <div class="card">
      <h2>About This Effect</h2>
      <p>This background is powered by Vanta.js, a library for animated 3D backgrounds using WebGL and Three.js.</p>
    </div>

    <div class="controls" id="controls"></div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="{effect_code['cdn']}"></script>
  <script>
    let vantaEffect = {effect_code['init']}

    // Controls
    const controls = document.getElementById('controls');

    const destroyBtn = document.createElement('button');
    destroyBtn.textContent = 'Pause Effect';
    let isDestroyed = false;
    destroyBtn.addEventListener('click', () => {{
      if (!isDestroyed) {{
        vantaEffect.destroy();
        isDestroyed = true;
        destroyBtn.textContent = 'Resume Effect';
      }} else {{
        vantaEffect = {effect_code['init']}
        isDestroyed = false;
        destroyBtn.textContent = 'Pause Effect';
      }}
    }});
    controls.appendChild(destroyBtn);

    {effect_code.get('controls', '')}
  </script>
</body>
</html>"""


def generate_waves():
    """Generate WAVES effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js',
        'init': """VANTA.WAVES({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x23153c,
      shininess: 30.00,
      waveHeight: 15.00,
      waveSpeed: 0.75,
      zoom: 0.65
    });""",
        'controls': """
    const increaseWavesBtn = document.createElement('button');
    increaseWavesBtn.textContent = 'Bigger Waves';
    increaseWavesBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ waveHeight: 25 });
      }
    });
    controls.appendChild(increaseWavesBtn);

    const fasterBtn = document.createElement('button');
    fasterBtn.textContent = 'Faster';
    fasterBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ waveSpeed: 1.5 });
      }
    });
    controls.appendChild(fasterBtn);"""
    }


def generate_clouds():
    """Generate CLOUDS effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.clouds.min.js',
        'init': """VANTA.CLOUDS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      skyColor: 0x68b8d7,
      cloudColor: 0xadc1de,
      cloudShadowColor: 0x183550,
      sunColor: 0xff9919,
      sunGlareColor: 0xff6633,
      sunlightColor: 0xff9933,
      speed: 1.00
    });""",
        'controls': """
    const fasterBtn = document.createElement('button');
    fasterBtn.textContent = 'Faster';
    fasterBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ speed: 2.0 });
      }
    });
    controls.appendChild(fasterBtn);

    const slowerBtn = document.createElement('button');
    slowerBtn.textContent = 'Slower';
    slowerBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ speed: 0.5 });
      }
    });
    controls.appendChild(slowerBtn);"""
    }


def generate_birds():
    """Generate BIRDS effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.birds.min.js',
        'init': """VANTA.BIRDS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      backgroundColor: 0x23153c,
      color1: 0xff0090,
      color2: 0xff6633,
      colorMode: "lerp",
      birdSize: 1.00,
      wingSpan: 20.00,
      speedLimit: 5.00,
      separation: 20.00,
      alignment: 20.00,
      cohesion: 20.00,
      quantity: 3.00
    });""",
        'controls': """
    const moreBirdsBtn = document.createElement('button');
    moreBirdsBtn.textContent = 'More Birds';
    moreBirdsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ quantity: 5.00 });
      }
    });
    controls.appendChild(moreBirdsBtn);

    const biggerBirdsBtn = document.createElement('button');
    biggerBirdsBtn.textContent = 'Bigger Birds';
    biggerBirdsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ birdSize: 1.5, wingSpan: 30 });
      }
    });
    controls.appendChild(biggerBirdsBtn);"""
    }


def generate_net():
    """Generate NET effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js',
        'init': """VANTA.NET({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x3fafff,
      backgroundColor: 0x23153c,
      points: 10.00,
      maxDistance: 20.00,
      spacing: 15.00,
      showDots: true
    });""",
        'controls': """
    const morePointsBtn = document.createElement('button');
    morePointsBtn.textContent = 'More Points';
    morePointsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ points: 15.00 });
      }
    });
    controls.appendChild(morePointsBtn);

    const denseNetBtn = document.createElement('button');
    denseNetBtn.textContent = 'Dense Network';
    denseNetBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ maxDistance: 30.00, spacing: 10.00 });
      }
    });
    controls.appendChild(denseNetBtn);"""
    }


def generate_cells():
    """Generate CELLS effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.cells.min.js',
        'init': """VANTA.CELLS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      color1: 0x18b0c6,
      color2: 0xff6633,
      size: 1.50,
      speed: 1.00
    });""",
        'controls': """
    const biggerCellsBtn = document.createElement('button');
    biggerCellsBtn.textContent = 'Bigger Cells';
    biggerCellsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ size: 2.50 });
      }
    });
    controls.appendChild(biggerCellsBtn);

    const fasterBtn = document.createElement('button');
    fasterBtn.textContent = 'Faster Growth';
    fasterBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ speed: 2.00 });
      }
    });
    controls.appendChild(fasterBtn);"""
    }


def generate_fog():
    """Generate FOG effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js',
        'init': """VANTA.FOG({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      highlightColor: 0xff3f81,
      midtoneColor: 0xff1f51,
      lowlightColor: 0x2d1b46,
      baseColor: 0xffebff,
      blurFactor: 0.60,
      speed: 1.00,
      zoom: 1.00
    });""",
        'controls': """
    const moreBlurBtn = document.createElement('button');
    moreBlurBtn.textContent = 'More Blur';
    moreBlurBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ blurFactor: 0.90 });
      }
    });
    controls.appendChild(moreBlurBtn);

    const fasterBtn = document.createElement('button');
    fasterBtn.textContent = 'Faster';
    fasterBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ speed: 2.00 });
      }
    });
    controls.appendChild(fasterBtn);"""
    }


def generate_globe():
    """Generate GLOBE effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.globe.min.js',
        'init': """VANTA.GLOBE({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x3fafff,
      color2: 0xff6633,
      size: 1.50,
      backgroundColor: 0x23153c
    });""",
        'controls': """
    const biggerGlobeBtn = document.createElement('button');
    biggerGlobeBtn.textContent = 'Bigger Globe';
    biggerGlobeBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ size: 2.00 });
      }
    });
    controls.appendChild(biggerGlobeBtn);"""
    }


def generate_rings():
    """Generate RINGS effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js',
        'init': """VANTA.RINGS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      backgroundColor: 0x23153c,
      color: 0xff3f81
    });""",
        'controls': ''
    }


def generate_dots():
    """Generate DOTS effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.dots.min.js',
        'init': """VANTA.DOTS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0xff3f81,
      color2: 0xffffff,
      backgroundColor: 0x23153c,
      size: 3.00,
      spacing: 35.00
    });""",
        'controls': """
    const biggerDotsBtn = document.createElement('button');
    biggerDotsBtn.textContent = 'Bigger Dots';
    biggerDotsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ size: 5.00 });
      }
    });
    controls.appendChild(biggerDotsBtn);

    const moreDotsBtn = document.createElement('button');
    moreDotsBtn.textContent = 'More Dots';
    moreDotsBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ spacing: 25.00 });
      }
    });
    controls.appendChild(moreDotsBtn);"""
    }


def generate_topology():
    """Generate TOPOLOGY effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.topology.min.js',
        'init': """VANTA.TOPOLOGY({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0xff3f81,
      backgroundColor: 0x23153c
    });""",
        'controls': ''
    }


def generate_trunk():
    """Generate TRUNK effect"""
    return {
        'cdn': 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.trunk.min.js',
        'init': """VANTA.TRUNK({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      backgroundColor: 0x23153c,
      color: 0xff3f81,
      spacing: 2.00,
      chaos: 4.00
    });""",
        'controls': """
    const moreChaosBtn = document.createElement('button');
    moreChaosBtn.textContent = 'More Chaos';
    moreChaosBtn.addEventListener('click', () => {
      if (vantaEffect && vantaEffect.setOptions) {
        vantaEffect.setOptions({ chaos: 8.00 });
      }
    });
    controls.appendChild(moreChaosBtn);"""
    }


VANTA_EFFECTS = {
    'waves': {
        'name': 'Waves',
        'description': 'Animated wave surface with reflections',
        'generator': generate_waves
    },
    'clouds': {
        'name': 'Clouds',
        'description': 'Volumetric cloud effect with sun',
        'generator': generate_clouds
    },
    'birds': {
        'name': 'Birds',
        'description': 'Flocking birds simulation',
        'generator': generate_birds
    },
    'net': {
        'name': 'Network',
        'description': 'Particle network with connecting lines',
        'generator': generate_net
    },
    'cells': {
        'name': 'Cells',
        'description': 'Organic cellular growth pattern',
        'generator': generate_cells
    },
    'fog': {
        'name': 'Fog',
        'description': 'Misty fog effect with depth',
        'generator': generate_fog
    },
    'globe': {
        'name': 'Globe',
        'description': 'Rotating globe with points',
        'generator': generate_globe
    },
    'rings': {
        'name': 'Rings',
        'description': 'Concentric animated rings',
        'generator': generate_rings
    },
    'dots': {
        'name': 'Dots',
        'description': 'Particle dot field effect',
        'generator': generate_dots
    },
    'topology': {
        'name': 'Topology',
        'description': 'Topographic mesh surface',
        'generator': generate_topology
    },
    'trunk': {
        'name': 'Trunk',
        'description': 'Abstract trunk/tree structure',
        'generator': generate_trunk
    }
}


def list_effects():
    """List all available Vanta effects"""
    print("\n✨ Available Vanta.js Effects:\n")
    for key, info in VANTA_EFFECTS.items():
        print(f"  {key:12} - {info['name']}")
        print(f"               {info['description']}")
        print()


def generate_effect(effect_key, output_path):
    """Generate Vanta.js effect"""
    if effect_key not in VANTA_EFFECTS:
        print(f"❌ Error: Unknown effect '{effect_key}'")
        print(f"   Use --list to see available effects")
        return False

    info = VANTA_EFFECTS[effect_key]

    print(f"\n✨ Generating {info['name']} effect...")

    # Generate effect code
    effect_code = info['generator']()

    # Create HTML
    html = create_html_template(
        f"Vanta.js {info['name']}",
        info['name'],
        effect_code
    )

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
    print("  ✨ Vanta.js Background Setup")
    print("="*60)

    print("\nSelect Vanta effect:\n")
    effects_list = list(VANTA_EFFECTS.keys())
    for i, key in enumerate(effects_list, 1):
        info = VANTA_EFFECTS[key]
        print(f"  {i:2}. {info['name']}")
        print(f"      {info['description']}")
        print()

    while True:
        try:
            choice = input("Enter number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return False

            choice_num = int(choice)
            if 1 <= choice_num <= len(effects_list):
                effect_key = effects_list[choice_num - 1]
                break
            else:
                print(f"❌ Please enter 1-{len(effects_list)}")
        except ValueError:
            print("❌ Please enter a valid number")

    # Get output filename
    default_name = f"vanta_{effect_key}.html"
    output_name = input(f"\nOutput filename [{default_name}]: ").strip()
    if not output_name:
        output_name = default_name

    output_path = Path.cwd() / output_name

    return generate_effect(effect_key, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Setup Vanta.js animated backgrounds',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--effect',
        choices=list(VANTA_EFFECTS.keys()),
        help='Vanta effect to generate'
    )

    parser.add_argument(
        '--output',
        default='vanta_background.html',
        help='Output HTML file path (default: vanta_background.html)'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available effects'
    )

    args = parser.parse_args()

    # List effects
    if args.list:
        list_effects()
        return 0

    # Interactive mode
    if not args.effect:
        success = interactive_mode()
        return 0 if success else 1

    # Direct generation
    success = generate_effect(args.effect, args.output)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
