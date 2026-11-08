import { Engine } from '@babylonjs/core/Engines/engine.js';
import { Scene } from '@babylonjs/core/scene.js';
import { ArcRotateCamera } from '@babylonjs/core/Cameras/arcRotateCamera.js';
import { Vector3, Color3, Color4 } from '@babylonjs/core/Maths/math.js';
import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight.js';
import { DirectionalLight } from '@babylonjs/core/Lights/directionalLight.js';
import { ShadowGenerator } from '@babylonjs/core/Lights/Shadows/shadowGenerator.js';
import { CreateGround } from '@babylonjs/core/Meshes/Builders/groundBuilder.js';
import { CreateSphere } from '@babylonjs/core/Meshes/Builders/sphereBuilder.js';
import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder.js';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial.js';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial.js';
import HavokPhysics from '@babylonjs/havok';
import { HavokPlugin } from '@babylonjs/core/Physics/v2/Plugins/havokPlugin.js';
import { PhysicsAggregate } from '@babylonjs/core/Physics/v2/physicsAggregate.js';
import { PhysicsShapeType } from '@babylonjs/core/Physics/v2/IPhysicsEnginePlugin.js';

// Import side effects for picking
import '@babylonjs/core/Culling/ray.js';
import '@babylonjs/core/Collisions/collisionCoordinator.js';

const canvas = document.getElementById('renderCanvas');
const engine = new Engine(canvas, true, {
  preserveDrawingBuffer: true,
  stencil: true
});

const createScene = async function() {
  const scene = new Scene(engine);
  scene.clearColor = new Color4(0.1, 0.1, 0.15, 1.0);

  // Camera
  const camera = new ArcRotateCamera(
    'camera',
    -Math.PI / 2,
    Math.PI / 3,
    15,
    Vector3.Zero(),
    scene
  );
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 5;
  camera.upperRadiusLimit = 50;
  camera.wheelPrecision = 50;

  // Lights
  const hemiLight = new HemisphericLight('hemiLight', new Vector3(0, 1, 0), scene);
  hemiLight.intensity = 0.5;

  const dirLight = new DirectionalLight('dirLight', new Vector3(-1, -2, -1), scene);
  dirLight.position = new Vector3(20, 40, 20);
  dirLight.intensity = 0.7;

  // Shadows
  const shadowGenerator = new ShadowGenerator(1024, dirLight);
  shadowGenerator.useExponentialShadowMap = true;

  // Ground
  const ground = CreateGround('ground', { width: 20, height: 20 }, scene);
  const groundMaterial = new StandardMaterial('groundMat', scene);
  groundMaterial.diffuseColor = new Color3(0.3, 0.3, 0.35);
  groundMaterial.specularColor = new Color3(0.1, 0.1, 0.1);
  ground.material = groundMaterial;
  ground.receiveShadows = true;

  // Initialize physics
  const havokInstance = await HavokPhysics();
  const havokPlugin = new HavokPlugin(true, havokInstance);
  scene.enablePhysics(new Vector3(0, -9.8, 0), havokPlugin);

  // Ground physics
  const groundAggregate = new PhysicsAggregate(
    ground,
    PhysicsShapeType.BOX,
    { mass: 0 },
    scene
  );

  // Create PBR sphere
  const sphere1 = CreateSphere('sphere1', { diameter: 2 }, scene);
  sphere1.position = new Vector3(-3, 3, 0);

  const pbrMaterial = new PBRMaterial('pbrMat', scene);
  pbrMaterial.metallic = 1.0;
  pbrMaterial.roughness = 0.3;
  pbrMaterial.baseColor = new Color3(0.9, 0.1, 0.1);
  sphere1.material = pbrMaterial;

  shadowGenerator.addShadowCaster(sphere1);

  const sphere1Aggregate = new PhysicsAggregate(
    sphere1,
    PhysicsShapeType.SPHERE,
    { mass: 1, restitution: 0.8 },
    scene
  );

  // Create standard material box
  const box1 = CreateBox('box1', { size: 1.5 }, scene);
  box1.position = new Vector3(3, 3, 0);

  const standardMaterial = new StandardMaterial('standardMat', scene);
  standardMaterial.diffuseColor = new Color3(0.2, 0.8, 0.3);
  standardMaterial.specularColor = new Color3(0.5, 0.5, 0.5);
  standardMaterial.specularPower = 32;
  box1.material = standardMaterial;

  shadowGenerator.addShadowCaster(box1);

  const box1Aggregate = new PhysicsAggregate(
    box1,
    PhysicsShapeType.BOX,
    { mass: 1, restitution: 0.5 },
    scene
  );

  // Create metallic sphere
  const sphere2 = CreateSphere('sphere2', { diameter: 1.8 }, scene);
  sphere2.position = new Vector3(0, 5, 2);

  const metallicMaterial = new PBRMaterial('metallicMat', scene);
  metallicMaterial.metallic = 0.9;
  metallicMaterial.roughness = 0.1;
  metallicMaterial.baseColor = new Color3(0.8, 0.8, 0.9);
  sphere2.material = metallicMaterial;

  shadowGenerator.addShadowCaster(sphere2);

  const sphere2Aggregate = new PhysicsAggregate(
    sphere2,
    PhysicsShapeType.SPHERE,
    { mass: 1, restitution: 0.9 },
    scene
  );

  // Picking
  let selectedMesh = null;

  scene.onPointerDown = function(evt, pickResult) {
    if (pickResult.hit && pickResult.pickedMesh !== ground) {
      // Deselect previous
      if (selectedMesh && selectedMesh.material) {
        selectedMesh.material.emissiveColor = new Color3(0, 0, 0);
      }

      // Select new
      selectedMesh = pickResult.pickedMesh;
      if (selectedMesh.material) {
        selectedMesh.material.emissiveColor = new Color3(0.2, 0.2, 0);
      }

      console.log('Selected:', selectedMesh.name);
    }
  };

  // Add sphere on spacebar
  let sphereCount = 3;
  window.addEventListener('keydown', (evt) => {
    if (evt.code === 'Space') {
      const newSphere = CreateSphere('sphere' + sphereCount, { diameter: 1.5 }, scene);
      newSphere.position = new Vector3(
        Math.random() * 6 - 3,
        8,
        Math.random() * 6 - 3
      );

      const randomMaterial = new PBRMaterial('mat' + sphereCount, scene);
      randomMaterial.metallic = Math.random();
      randomMaterial.roughness = Math.random() * 0.5 + 0.2;
      randomMaterial.baseColor = new Color3(
        Math.random(),
        Math.random(),
        Math.random()
      );
      newSphere.material = randomMaterial;

      shadowGenerator.addShadowCaster(newSphere);

      new PhysicsAggregate(
        newSphere,
        PhysicsShapeType.SPHERE,
        { mass: 1, restitution: 0.7 },
        scene
      );

      sphereCount++;
    }
  });

  // FPS counter
  let fpsDisplay = document.createElement('div');
  fpsDisplay.style.position = 'absolute';
  fpsDisplay.style.top = '10px';
  fpsDisplay.style.right = '10px';
  fpsDisplay.style.color = 'white';
  fpsDisplay.style.fontFamily = 'monospace';
  fpsDisplay.style.fontSize = '14px';
  fpsDisplay.style.background = 'rgba(0, 0, 0, 0.5)';
  fpsDisplay.style.padding = '8px 12px';
  fpsDisplay.style.borderRadius = '4px';
  document.body.appendChild(fpsDisplay);

  scene.onBeforeRenderObservable.add(() => {
    fpsDisplay.textContent = `FPS: ${engine.getFps().toFixed(0)}`;
  });

  return scene;
};

// Create scene and start render loop
createScene().then(scene => {
  engine.runRenderLoop(() => {
    scene.render();
  });
});

// Handle resize
window.addEventListener('resize', () => {
  engine.resize();
});

// Optional: Debug layer (Shift+Ctrl+Alt+I)
window.addEventListener('keydown', (ev) => {
  if (ev.shiftKey && ev.ctrlKey && ev.altKey && (ev.key === 'I' || ev.key === 'i')) {
    import('@babylonjs/core/Debug/debugLayer.js').then(() => {
      import('@babylonjs/inspector').then(() => {
        if (engine.scenes[0].debugLayer.isVisible()) {
          engine.scenes[0].debugLayer.hide();
        } else {
          engine.scenes[0].debugLayer.show();
        }
      });
    });
  }
});
