/**
 * PlayCanvas Starter Project
 * Main application initialization and scene setup
 */

let app;
let cameraController;
let inputManager;
let statsEnabled = true;
let wireframeEnabled = false;

/**
 * Initialize PlayCanvas application
 */
function initApp() {
    const canvas = document.getElementById('application-canvas');

    // Create PlayCanvas application
    app = new pc.Application(canvas, {
        mouse: new pc.Mouse(canvas),
        touch: new pc.TouchDevice(canvas),
        keyboard: new pc.Keyboard(window),
        graphicsDeviceOptions: {
            antialias: true,
            alpha: false
        }
    });

    // Configure application
    app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
    app.setCanvasResolution(pc.RESOLUTION_AUTO);

    // Start application
    app.start();

    // Setup scene
    setupScene();

    // Initialize managers
    inputManager = new InputManager(app);
    cameraController = new CameraController(app, app.root.findByName('Camera'));

    // Setup UI controls
    setupUI();

    // Update loop
    app.on('update', update);

    // Hide loading screen
    setTimeout(() => {
        document.getElementById('loading-screen').classList.add('hidden');
    }, 500);

    // Handle window resize
    window.addEventListener('resize', () => {
        app.resizeCanvas();
    });

    console.log('PlayCanvas application initialized');
}

/**
 * Setup scene with camera, lights, and objects
 */
function setupScene() {
    // Camera
    const camera = new pc.Entity('Camera');
    camera.addComponent('camera', {
        clearColor: new pc.Color(0.1, 0.1, 0.15),
        farClip: 100
    });
    camera.setPosition(0, 5, 10);
    camera.lookAt(0, 0, 0);
    app.root.addChild(camera);

    // Directional Light (Sun)
    const light = new pc.Entity('DirectionalLight');
    light.addComponent('light', {
        type: 'directional',
        color: new pc.Color(1, 1, 1),
        intensity: 1,
        castShadows: true,
        shadowBias: 0.2,
        shadowDistance: 40,
        normalOffsetBias: 0.05
    });
    light.setEulerAngles(45, 30, 0);
    app.root.addChild(light);

    // Ambient Light
    const ambient = new pc.Entity('AmbientLight');
    ambient.addComponent('light', {
        type: 'directional',
        color: new pc.Color(0.4, 0.5, 0.6),
        intensity: 0.3
    });
    ambient.setEulerAngles(-45, 0, 0);
    app.root.addChild(ambient);

    // Ground Plane
    const ground = new pc.Entity('Ground');
    ground.addComponent('model', {
        type: 'plane'
    });
    ground.setLocalScale(20, 1, 20);

    // Ground material
    const groundMaterial = new pc.StandardMaterial();
    groundMaterial.diffuse = new pc.Color(0.3, 0.3, 0.35);
    groundMaterial.metalness = 0.0;
    groundMaterial.gloss = 0.3;
    groundMaterial.update();
    ground.model.material = groundMaterial;

    app.root.addChild(ground);

    // Create demo objects
    createDemoObjects();
}

/**
 * Create demo objects in the scene
 */
function createDemoObjects() {
    const colors = [
        new pc.Color(0.8, 0.3, 0.3),  // Red
        new pc.Color(0.3, 0.8, 0.3),  // Green
        new pc.Color(0.3, 0.3, 0.8),  // Blue
        new pc.Color(0.8, 0.8, 0.3),  // Yellow
        new pc.Color(0.8, 0.3, 0.8)   // Magenta
    ];

    const shapes = ['box', 'sphere', 'cylinder', 'cone', 'capsule'];

    for (let i = 0; i < 5; i++) {
        const entity = new pc.Entity(`Shape_${i}`);

        // Add model component
        entity.addComponent('model', {
            type: shapes[i]
        });

        // Position in a circle
        const angle = (i / 5) * Math.PI * 2;
        const radius = 4;
        entity.setPosition(
            Math.cos(angle) * radius,
            1,
            Math.sin(angle) * radius
        );

        // Create material
        const material = new pc.StandardMaterial();
        material.diffuse = colors[i];
        material.metalness = 0.2 + (i * 0.15);
        material.gloss = 0.7;
        material.update();
        entity.model.material = material;

        // Store rotation speed
        entity.rotationSpeed = new pc.Vec3(
            10 + i * 5,
            20 + i * 5,
            15 + i * 5
        );

        app.root.addChild(entity);
    }
}

/**
 * Main update loop
 */
function update(dt) {
    // Update camera controller
    if (cameraController) {
        cameraController.update(dt);
    }

    // Rotate demo objects
    const shapes = app.root.find((node) => node.name.startsWith('Shape_'));
    shapes.forEach((shape) => {
        if (shape.rotationSpeed) {
            shape.rotate(
                shape.rotationSpeed.x * dt,
                shape.rotationSpeed.y * dt,
                shape.rotationSpeed.z * dt
            );
        }
    });

    // Update stats
    if (statsEnabled) {
        updateStats();
    }
}

/**
 * Update performance stats display
 */
function updateStats() {
    const stats = app.stats;

    document.getElementById('fps').textContent = Math.round(1 / app.dt);
    document.getElementById('draw-calls').textContent = stats.drawCalls.total;
    document.getElementById('triangles').textContent = Math.round(stats.misc.tricount / 1000) + 'k';
}

/**
 * Setup UI controls
 */
function setupUI() {
    // Toggle stats
    document.getElementById('toggle-stats').addEventListener('click', () => {
        statsEnabled = !statsEnabled;
        document.getElementById('stats-panel').classList.toggle('hidden');
    });

    // Toggle wireframe
    document.getElementById('toggle-wireframe').addEventListener('click', () => {
        wireframeEnabled = !wireframeEnabled;

        // Update all materials
        const entities = app.root.find((node) => node.model);
        entities.forEach((entity) => {
            if (entity.model && entity.model.material) {
                // Create new material instance if needed
                if (!entity.model.material.wireframe) {
                    const material = entity.model.material;
                    material.update();
                }
            }
        });

        // Note: Wireframe rendering requires custom shader in PlayCanvas
        console.log('Wireframe mode:', wireframeEnabled);
    });

    // Reset camera
    document.getElementById('reset-camera').addEventListener('click', () => {
        if (cameraController) {
            cameraController.reset();
        }
    });
}

/**
 * Cleanup resources
 */
function cleanup() {
    if (app) {
        app.destroy();
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', cleanup);
