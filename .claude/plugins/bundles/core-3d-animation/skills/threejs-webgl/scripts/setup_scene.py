#!/usr/bin/env python3
"""
Three.js Scene Setup Generator

Generates boilerplate Three.js scene code with customizable options.
"""

import argparse
import os
from pathlib import Path


TEMPLATES = {
    "basic": """import * as THREE from 'three';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color({background_color});

// Camera
const camera = new THREE.PerspectiveCamera(
  {fov},
  window.innerWidth / window.innerHeight,
  {near},
  {far}
);
camera.position.set({camera_x}, {camera_y}, {camera_z});

// Renderer
const renderer = new THREE.WebGLRenderer({{ antialias: {antialias} }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
{shadow_setup}document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Lights
{lights}

// Animation Loop
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();
  controls.update();

  renderer.render(scene, camera);
}}

animate();

// Handle Resize
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});
""",

    "webgpu": """import * as THREE from 'three/webgpu';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color({background_color});

// Camera
const camera = new THREE.PerspectiveCamera(
  {fov},
  window.innerWidth / window.innerHeight,
  {near},
  {far}
);
camera.position.set({camera_x}, {camera_y}, {camera_z});

// Renderer (WebGPU)
const renderer = new THREE.WebGPURenderer({{ antialias: {antialias} }});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setAnimationLoop(animate);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Lights
{lights}

// Animation Loop
const clock = new THREE.Clock();

function animate() {{
  const deltaTime = clock.getDelta();
  controls.update();
}}

// Handle Resize
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});
"""
}

LIGHT_SETUPS = {
    "basic": """const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
scene.add(directionalLight);
""",

    "shadows": """const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.left = -10;
directionalLight.shadow.camera.right = 10;
directionalLight.shadow.camera.top = 10;
directionalLight.shadow.camera.bottom = -10;
scene.add(directionalLight);
""",

    "physical": """const hemiLight = new THREE.HemisphereLight(0xddeeff, 0x0f0e0d, 0.02);
scene.add(hemiLight);

const bulbLight = new THREE.PointLight(0xffee88, 1, 100, 2);
bulbLight.power = 1700; // 100W bulb
bulbLight.position.set(0, 2, 0);
bulbLight.castShadow = true;
scene.add(bulbLight);
"""
}


def generate_scene(args):
    """Generate Three.js scene code based on arguments."""

    # Select template
    template = TEMPLATES.get(args.renderer, TEMPLATES["basic"])

    # Select light setup
    lights = LIGHT_SETUPS.get(args.lighting, LIGHT_SETUPS["basic"])

    # Shadow setup
    shadow_setup = ""
    if args.shadows:
        shadow_setup = """renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
"""

    # Fill template
    code = template.format(
        background_color=args.background,
        fov=args.fov,
        near=args.near,
        far=args.far,
        camera_x=args.camera[0],
        camera_y=args.camera[1],
        camera_z=args.camera[2],
        antialias=str(args.antialias).lower(),
        shadow_setup=shadow_setup,
        lights=lights
    )

    return code


def main():
    parser = argparse.ArgumentParser(
        description='Generate Three.js scene boilerplate code'
    )

    # Renderer type
    parser.add_argument(
        '--renderer',
        choices=['basic', 'webgpu'],
        default='basic',
        help='Renderer type (default: basic)'
    )

    # Camera settings
    parser.add_argument(
        '--fov',
        type=int,
        default=75,
        help='Camera field of view (default: 75)'
    )

    parser.add_argument(
        '--near',
        type=float,
        default=0.1,
        help='Camera near plane (default: 0.1)'
    )

    parser.add_argument(
        '--far',
        type=int,
        default=1000,
        help='Camera far plane (default: 1000)'
    )

    parser.add_argument(
        '--camera',
        nargs=3,
        type=float,
        default=[0, 2, 5],
        metavar=('X', 'Y', 'Z'),
        help='Camera position (default: 0 2 5)'
    )

    # Scene settings
    parser.add_argument(
        '--background',
        default='0x000000',
        help='Background color hex (default: 0x000000)'
    )

    parser.add_argument(
        '--lighting',
        choices=['basic', 'shadows', 'physical'],
        default='basic',
        help='Lighting setup (default: basic)'
    )

    parser.add_argument(
        '--shadows',
        action='store_true',
        help='Enable shadow rendering'
    )

    parser.add_argument(
        '--antialias',
        action='store_true',
        default=True,
        help='Enable antialiasing (default: True)'
    )

    # Output
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: print to stdout)'
    )

    args = parser.parse_args()

    # Generate code
    code = generate_scene(args)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code)
        print(f"✅ Generated scene code: {output_path}")
    else:
        print(code)


if __name__ == '__main__':
    main()
