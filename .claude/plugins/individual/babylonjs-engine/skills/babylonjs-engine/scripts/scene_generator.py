#!/usr/bin/env python3
"""
Babylon.js Scene Generator

Generates Babylon.js scene boilerplate with various configurations.
Supports multiple scene types, cameras, lighting setups, and physics.

Usage:
    python3 scene_generator.py --type basic --name MyScene --output scene.js
    python3 scene_generator.py --type physics --camera arc-rotate --typescript
    python3 scene_generator.py --interactive
"""

import argparse
import sys
from pathlib import Path


SCENE_TYPES = {
    'basic': {
        'description': 'Basic scene with camera, light, and ground',
        'includes': ['camera', 'light', 'ground']
    },
    'physics': {
        'description': 'Scene with Havok physics enabled',
        'includes': ['camera', 'light', 'ground', 'physics', 'sphere']
    },
    'pbr': {
        'description': 'PBR materials showcase scene',
        'includes': ['camera', 'light', 'pbr-meshes', 'environment']
    },
    'model-viewer': {
        'description': 'GLTF model loading and viewing',
        'includes': ['arc-camera', 'light', 'model-loader', 'environment']
    },
    'vr': {
        'description': 'WebXR VR scene',
        'includes': ['camera', 'light', 'ground', 'webxr']
    },
    'particles': {
        'description': 'Particle system showcase',
        'includes': ['camera', 'light', 'particles']
    },
    'gui': {
        'description': 'Scene with 2D GUI elements',
        'includes': ['camera', 'light', 'ground', 'gui']
    },
    'post-processing': {
        'description': 'Scene with post-processing effects',
        'includes': ['camera', 'light', 'meshes', 'post-processing']
    }
}

CAMERA_TYPES = {
    'free': 'FreeCamera',
    'arc-rotate': 'ArcRotateCamera',
    'universal': 'UniversalCamera',
    'follow': 'FollowCamera'
}


def generate_imports(scene_type, use_typescript, camera_type):
    """Generate ES6 imports based on scene configuration."""
    if use_typescript:
        imports = [
            "import { Engine } from '@babylonjs/core/Engines/engine';",
            "import { Scene } from '@babylonjs/core/scene';",
            "import { Vector3 } from '@babylonjs/core/Maths/math.vector';",
            "import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight';",
        ]
    else:
        imports = [
            "import { Engine } from '@babylonjs/core/Engines/engine.js';",
            "import { Scene } from '@babylonjs/core/scene.js';",
            "import { Vector3 } from '@babylonjs/core/Maths/math.vector.js';",
            "import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight.js';",
        ]

    # Camera imports
    camera_import_map = {
        'free': "FreeCamera } from '@babylonjs/core/Cameras/freeCamera",
        'arc-rotate': "ArcRotateCamera } from '@babylonjs/core/Cameras/arcRotateCamera",
        'universal': "UniversalCamera } from '@babylonjs/core/Cameras/universalCamera",
        'follow': "FollowCamera } from '@babylonjs/core/Cameras/followCamera"
    }

    camera_import = camera_import_map.get(camera_type, camera_import_map['arc-rotate'])
    imports.append(f"import {{ {camera_import}{'js' if not use_typescript else ''}';}}")

    config = SCENE_TYPES[scene_type]

    # Mesh builders
    if 'ground' in config['includes'] or 'meshes' in config['includes']:
        if use_typescript:
            imports.append("import { CreateGround } from '@babylonjs/core/Meshes/Builders/groundBuilder';")
            imports.append("import { CreateSphere } from '@babylonjs/core/Meshes/Builders/sphereBuilder';")
            imports.append("import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder';")
        else:
            imports.append("import { CreateGround } from '@babylonjs/core/Meshes/Builders/groundBuilder.js';")
            imports.append("import { CreateSphere } from '@babylonjs/core/Meshes/Builders/sphereBuilder.js';")
            imports.append("import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder.js';")

    # Physics
    if 'physics' in config['includes']:
        if use_typescript:
            imports.append("import HavokPhysics from '@babylonjs/havok';")
            imports.append("import { HavokPlugin } from '@babylonjs/core/Physics/v2/Plugins/havokPlugin';")
            imports.append("import { PhysicsAggregate } from '@babylonjs/core/Physics/v2/physicsAggregate';")
            imports.append("import { PhysicsShapeType } from '@babylonjs/core/Physics/v2/IPhysicsEnginePlugin';")
        else:
            imports.append("import HavokPhysics from '@babylonjs/havok';")
            imports.append("import { HavokPlugin } from '@babylonjs/core/Physics/v2/Plugins/havokPlugin.js';")
            imports.append("import { PhysicsAggregate } from '@babylonjs/core/Physics/v2/physicsAggregate.js';")
            imports.append("import { PhysicsShapeType } from '@babylonjs/core/Physics/v2/IPhysicsEnginePlugin.js';")

    # PBR
    if 'pbr-meshes' in config['includes']:
        if use_typescript:
            imports.append("import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';")
        else:
            imports.append("import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial.js';")

    # Environment
    if 'environment' in config['includes']:
        if use_typescript:
            imports.append("import { CubeTexture } from '@babylonjs/core/Materials/Textures/cubeTexture';")
        else:
            imports.append("import { CubeTexture } from '@babylonjs/core/Materials/Textures/cubeTexture.js';")

    # Model loader
    if 'model-loader' in config['includes']:
        if use_typescript:
            imports.append("import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader';")
            imports.append("import '@babylonjs/loaders/glTF';")
        else:
            imports.append("import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader.js';")
            imports.append("import '@babylonjs/loaders/glTF';")

    # WebXR
    if 'webxr' in config['includes']:
        if use_typescript:
            imports.append("import '@babylonjs/core/Helpers/sceneHelpers';")
        else:
            imports.append("import '@babylonjs/core/Helpers/sceneHelpers.js';")

    # GUI
    if 'gui' in config['includes']:
        if use_typescript:
            imports.append("import { AdvancedDynamicTexture } from '@babylonjs/gui/2D/advancedDynamicTexture';")
            imports.append("import { Button } from '@babylonjs/gui/2D/controls/button';")
        else:
            imports.append("import { AdvancedDynamicTexture } from '@babylonjs/gui/2D/advancedDynamicTexture.js';")
            imports.append("import { Button } from '@babylonjs/gui/2D/controls/button.js';")

    # Particles
    if 'particles' in config['includes']:
        if use_typescript:
            imports.append("import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';")
            imports.append("import { Texture } from '@babylonjs/core/Materials/Textures/texture';")
        else:
            imports.append("import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem.js';")
            imports.append("import { Texture } from '@babylonjs/core/Materials/Textures/texture.js';")

    # Post-processing
    if 'post-processing' in config['includes']:
        if use_typescript:
            imports.append("import { DefaultRenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/defaultRenderingPipeline';")
        else:
            imports.append("import { DefaultRenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/defaultRenderingPipeline.js';")

    return '\n'.join(imports)


def generate_camera_code(camera_type, use_typescript):
    """Generate camera setup code."""
    if camera_type == 'free':
        return """  // Create FreeCamera
  const camera = new FreeCamera('camera', new Vector3(0, 5, -10), scene);
  camera.setTarget(Vector3.Zero());
  camera.attachControl(canvas, true);
  camera.speed = 0.5;
  camera.angularSensibility = 2000;"""

    elif camera_type == 'arc-rotate':
        return """  // Create ArcRotateCamera
  const camera = new ArcRotateCamera(
    'camera',
    -Math.PI / 2,
    Math.PI / 2.5,
    10,
    Vector3.Zero(),
    scene
  );
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 5;
  camera.upperRadiusLimit = 50;"""

    elif camera_type == 'universal':
        return """  // Create UniversalCamera
  const camera = new UniversalCamera('camera', new Vector3(0, 5, -10), scene);
  camera.setTarget(Vector3.Zero());
  camera.attachControl(canvas, true);
  camera.checkCollisions = true;
  camera.applyGravity = true;"""

    elif camera_type == 'follow':
        return """  // Create FollowCamera
  const camera = new FollowCamera('camera', new Vector3(0, 10, -10), scene);
  camera.radius = 10;
  camera.heightOffset = 5;
  camera.rotationOffset = 0;
  camera.cameraAcceleration = 0.05;
  camera.maxCameraSpeed = 10;
  camera.attachControl(canvas, true);"""

    return ""


def generate_scene_code(scene_type, camera_type, use_typescript):
    """Generate scene setup code based on type."""
    config = SCENE_TYPES[scene_type]

    code = []

    # Camera
    code.append(generate_camera_code(camera_type, use_typescript))

    # Light
    code.append("""
  // Create light
  const light = new HemisphericLight('light', new Vector3(0, 1, 0), scene);
  light.intensity = 0.7;""")

    # Ground
    if 'ground' in config['includes']:
        code.append("""
  // Create ground
  const ground = CreateGround('ground', { width: 10, height: 10 }, scene);""")

    # Physics
    if 'physics' in config['includes']:
        code.append("""
  // Initialize Havok physics
  const havokInstance = await HavokPhysics();
  const havokPlugin = new HavokPlugin(true, havokInstance);
  scene.enablePhysics(new Vector3(0, -9.8, 0), havokPlugin);

  // Create sphere with physics
  const sphere = CreateSphere('sphere', { diameter: 2 }, scene);
  sphere.position.y = 5;

  const sphereAggregate = new PhysicsAggregate(
    sphere,
    PhysicsShapeType.SPHERE,
    { mass: 1, restitution: 0.75 },
    scene
  );

  const groundAggregate = new PhysicsAggregate(
    ground,
    PhysicsShapeType.BOX,
    { mass: 0 },
    scene
  );""")

    # PBR materials
    if 'pbr-meshes' in config['includes']:
        code.append("""
  // Create PBR materials
  const pbrMaterial = new PBRMaterial('pbr', scene);
  pbrMaterial.metallic = 1.0;
  pbrMaterial.roughness = 0.3;
  pbrMaterial.baseColor = new BABYLON.Color3(0.9, 0.9, 0.9);

  const sphere = CreateSphere('sphere', { diameter: 2 }, scene);
  sphere.position.y = 1;
  sphere.material = pbrMaterial;

  const box = CreateBox('box', { size: 1.5 }, scene);
  box.position.set(3, 0.75, 0);

  const boxMaterial = new PBRMaterial('boxMaterial', scene);
  boxMaterial.metallic = 0.0;
  boxMaterial.roughness = 0.8;
  boxMaterial.baseColor = new BABYLON.Color3(0.8, 0.2, 0.2);
  box.material = boxMaterial;""")

    # Environment
    if 'environment' in config['includes']:
        code.append("""
  // Create default environment
  const env = scene.createDefaultEnvironment({
    createGround: true,
    createSkybox: true,
    skyboxSize: 150
  });""")

    # Model loader
    if 'model-loader' in config['includes']:
        code.append("""
  // Load GLTF model
  const result = await SceneLoader.ImportMeshAsync(
    null,
    'https://assets.babylonjs.com/meshes/',
    'village.glb',
    scene
  );

  console.log('Loaded meshes:', result.meshes.length);""")

    # WebXR
    if 'webxr' in config['includes']:
        code.append("""
  // Enable WebXR
  const env = scene.createDefaultEnvironment();
  const xr = await scene.createDefaultXRExperienceAsync({
    floorMeshes: [env.ground]
  });""")

    # GUI
    if 'gui' in config['includes']:
        code.append("""
  // Create 2D UI
  const advancedTexture = AdvancedDynamicTexture.CreateFullscreenUI('UI');

  const button = Button.CreateSimpleButton('button', 'Click Me');
  button.width = '150px';
  button.height = '40px';
  button.color = 'white';
  button.background = 'green';
  button.onPointerUpObservable.add(() => {
    console.log('Button clicked');
  });

  advancedTexture.addControl(button);""")

    # Particles
    if 'particles' in config['includes']:
        code.append("""
  // Create particle system
  const particleSystem = new ParticleSystem('particles', 2000, scene);
  particleSystem.particleTexture = new Texture('https://assets.babylonjs.com/textures/flare.png', scene);

  particleSystem.emitter = new Vector3(0, 5, 0);
  particleSystem.minEmitBox = new Vector3(-1, 0, 0);
  particleSystem.maxEmitBox = new Vector3(1, 0, 0);

  particleSystem.color1 = new BABYLON.Color4(0.7, 0.8, 1.0, 1.0);
  particleSystem.color2 = new BABYLON.Color4(0.2, 0.5, 1.0, 1.0);
  particleSystem.colorDead = new BABYLON.Color4(0, 0, 0.2, 0.0);

  particleSystem.minSize = 0.1;
  particleSystem.maxSize = 0.5;

  particleSystem.minLifeTime = 0.3;
  particleSystem.maxLifeTime = 1.5;

  particleSystem.emitRate = 1500;
  particleSystem.direction1 = new Vector3(-1, 8, 1);
  particleSystem.direction2 = new Vector3(1, 8, -1);
  particleSystem.gravity = new Vector3(0, -9.81, 0);

  particleSystem.start();""")

    # Post-processing
    if 'post-processing' in config['includes']:
        code.append("""
  // Add post-processing
  const pipeline = new DefaultRenderingPipeline('pipeline', true, scene, [camera]);
  pipeline.fxaaEnabled = true;
  pipeline.samples = 4;

  pipeline.bloomEnabled = true;
  pipeline.bloomThreshold = 0.8;
  pipeline.bloomWeight = 0.5;
  pipeline.bloomKernel = 64;

  // Create some meshes
  const sphere = CreateSphere('sphere', { diameter: 2 }, scene);
  sphere.position.y = 1;

  const box = CreateBox('box', { size: 1.5 }, scene);
  box.position.set(3, 0.75, 0);

  const ground = CreateGround('ground', { width: 10, height: 10 }, scene);""")

    return '\n'.join(code)


def generate_scene_file(scene_type, camera_type, use_typescript, scene_name):
    """Generate complete scene file."""
    ext = 'ts' if use_typescript else 'js'

    imports = generate_imports(scene_type, use_typescript, camera_type)
    scene_code = generate_scene_code(scene_type, camera_type, use_typescript)

    is_async = 'physics' in SCENE_TYPES[scene_type]['includes'] or \
               'model-loader' in SCENE_TYPES[scene_type]['includes'] or \
               'webxr' in SCENE_TYPES[scene_type]['includes']

    template = f"""// {scene_name} - Generated by Babylon.js Scene Generator
{imports}

// Get canvas element
const canvas = document.getElementById('renderCanvas'){' as HTMLCanvasElement' if use_typescript else ''};

// Create engine
const engine = new Engine(canvas, true, {{
  preserveDrawingBuffer: true,
  stencil: true
}});

// Create scene
const createScene = {'async ' if is_async else ''}function(){': Scene' if use_typescript else ''} {{
  const scene = new Scene(engine);

{scene_code}

  return scene;
}};

// Initialize and run
{'(async () => {' if is_async else ''}
const scene = {'await ' if is_async else ''}createScene();

// Run render loop
engine.runRenderLoop(() => {{
  scene.render();
}});

// Handle resize
window.addEventListener('resize', () => {{
  engine.resize();
}});
{'})();' if is_async else ''}
"""

    return template


def interactive_mode():
    """Interactive CLI for scene generation."""
    print("\n🎮 Babylon.js Scene Generator - Interactive Mode\n")

    # Scene type
    print("Select scene type:")
    for i, (key, config) in enumerate(SCENE_TYPES.items(), 1):
        print(f"  {i}. {key}: {config['description']}")

    scene_choice = input("\nEnter number (1-8): ").strip()
    scene_type = list(SCENE_TYPES.keys())[int(scene_choice) - 1]

    # Camera type
    print("\nSelect camera type:")
    for i, (key, value) in enumerate(CAMERA_TYPES.items(), 1):
        print(f"  {i}. {key}: {value}")

    camera_choice = input("\nEnter number (1-4, default 2): ").strip() or "2"
    camera_type = list(CAMERA_TYPES.keys())[int(camera_choice) - 1]

    # TypeScript
    use_typescript = input("\nUse TypeScript? (y/N): ").strip().lower() == 'y'

    # Scene name
    scene_name = input("\nScene name (default: MyScene): ").strip() or "MyScene"

    # Output file
    ext = 'ts' if use_typescript else 'js'
    default_output = f"{scene_name.lower().replace(' ', '_')}.{ext}"
    output_file = input(f"\nOutput file (default: {default_output}): ").strip() or default_output

    # Generate
    print(f"\n✨ Generating {scene_type} scene...")
    code = generate_scene_file(scene_type, camera_type, use_typescript, scene_name)

    Path(output_file).write_text(code)
    print(f"✅ Scene generated: {output_file}")

    # Instructions
    print(f"\n📝 Next steps:")
    print(f"  1. Install dependencies: npm install @babylonjs/core @babylonjs/loaders")
    if 'gui' in SCENE_TYPES[scene_type]['includes']:
        print(f"     npm install @babylonjs/gui")
    if 'physics' in SCENE_TYPES[scene_type]['includes']:
        print(f"     npm install @babylonjs/havok")
    print(f"  2. Create HTML file with <canvas id='renderCanvas'></canvas>")
    print(f"  3. Import this scene file")
    print(f"  4. Run dev server")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Babylon.js scene boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--type',
        choices=list(SCENE_TYPES.keys()),
        help='Scene type'
    )

    parser.add_argument(
        '--camera',
        choices=list(CAMERA_TYPES.keys()),
        default='arc-rotate',
        help='Camera type (default: arc-rotate)'
    )

    parser.add_argument(
        '--typescript',
        action='store_true',
        help='Generate TypeScript instead of JavaScript'
    )

    parser.add_argument(
        '--name',
        default='MyScene',
        help='Scene name (default: MyScene)'
    )

    parser.add_argument(
        '--output',
        help='Output file path'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode'
    )

    parser.add_argument(
        '--list-types',
        action='store_true',
        help='List available scene types'
    )

    args = parser.parse_args()

    # List types
    if args.list_types:
        print("\nAvailable scene types:\n")
        for key, config in SCENE_TYPES.items():
            print(f"  {key}:")
            print(f"    {config['description']}")
            print(f"    Includes: {', '.join(config['includes'])}\n")
        return

    # Interactive mode
    if args.interactive or not args.type:
        interactive_mode()
        return

    # Generate from args
    ext = 'ts' if args.typescript else 'js'
    output_file = args.output or f"{args.name.lower().replace(' ', '_')}.{ext}"

    print(f"✨ Generating {args.type} scene...")
    code = generate_scene_file(args.type, args.camera, args.typescript, args.name)

    Path(output_file).write_text(code)
    print(f"✅ Scene generated: {output_file}")


if __name__ == '__main__':
    main()
