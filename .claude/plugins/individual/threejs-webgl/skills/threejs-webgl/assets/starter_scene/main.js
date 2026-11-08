import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);
scene.fog = new THREE.Fog(0x1a1a2e, 10, 50);

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(5, 3, 8);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 3;
controls.maxDistance = 20;
controls.maxPolarAngle = Math.PI / 2;
controls.target.set(0, 1, 0);

// Lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
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
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
scene.add(directionalLight);

// Add point light for accent
const pointLight = new THREE.PointLight(0x00ffff, 0.5, 15);
pointLight.position.set(-3, 3, -3);
scene.add(pointLight);

// Floor
const floorGeometry = new THREE.PlaneGeometry(20, 20);
const floorMaterial = new THREE.MeshStandardMaterial({
  color: 0x2a2a4a,
  roughness: 0.8,
  metalness: 0.2
});
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

// Grid Helper
const gridHelper = new THREE.GridHelper(20, 20, 0x444466, 0x222244);
gridHelper.position.y = 0.01;
scene.add(gridHelper);

// Demo Objects
const objectsGroup = new THREE.Group();
scene.add(objectsGroup);

// Spinning cube
const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
const cubeMaterial = new THREE.MeshStandardMaterial({
  color: 0xff6b6b,
  roughness: 0.3,
  metalness: 0.7
});
const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
cube.position.set(-2, 1, 0);
cube.castShadow = true;
cube.receiveShadow = true;
objectsGroup.add(cube);

// Sphere
const sphereGeometry = new THREE.SphereGeometry(0.7, 32, 32);
const sphereMaterial = new THREE.MeshStandardMaterial({
  color: 0x4ecdc4,
  roughness: 0.2,
  metalness: 0.8
});
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
sphere.position.set(0, 1.2, 0);
sphere.castShadow = true;
sphere.receiveShadow = true;
objectsGroup.add(sphere);

// Torus
const torusGeometry = new THREE.TorusGeometry(0.6, 0.25, 16, 32);
const torusMaterial = new THREE.MeshStandardMaterial({
  color: 0xffe66d,
  roughness: 0.4,
  metalness: 0.6
});
const torus = new THREE.Mesh(torusGeometry, torusMaterial);
torus.position.set(2, 1, 0);
torus.castShadow = true;
torus.receiveShadow = true;
objectsGroup.add(torus);

// Animation Loop
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();
  const elapsedTime = clock.getElapsedTime();

  // Animate objects
  cube.rotation.y += deltaTime * 0.5;
  cube.rotation.x += deltaTime * 0.25;

  sphere.position.y = 1.2 + Math.sin(elapsedTime * 2) * 0.3;

  torus.rotation.x += deltaTime * 0.3;
  torus.rotation.y += deltaTime * 0.5;

  // Animate point light
  pointLight.position.x = Math.sin(elapsedTime * 0.5) * 5;
  pointLight.position.z = Math.cos(elapsedTime * 0.5) * 5;

  // Update controls
  controls.update();

  // Render
  renderer.render(scene, camera);
}

// Handle Resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Hide loading screen and start animation
document.getElementById('loading').classList.add('hidden');
animate();
