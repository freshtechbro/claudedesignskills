/**
 * Camera Controller
 * Orbit camera with mouse/touch controls
 */

class CameraController {
    constructor(app, cameraEntity, options = {}) {
        this.app = app;
        this.camera = cameraEntity;

        // Configuration
        this.target = options.target || new pc.Vec3(0, 0, 0);
        this.distance = options.distance || 10;
        this.minDistance = options.minDistance || 2;
        this.maxDistance = options.maxDistance || 50;
        this.sensitivity = options.sensitivity || 0.3;
        this.damping = options.damping || 0.15;
        this.zoomSpeed = options.zoomSpeed || 0.5;

        // State
        this.yaw = options.initialYaw || 0;
        this.pitch = options.initialPitch || 20;
        this.targetYaw = this.yaw;
        this.targetPitch = this.pitch;
        this.currentDistance = this.distance;
        this.targetDistance = this.distance;

        // Input tracking
        this.isDragging = false;
        this.lastMouseX = 0;
        this.lastMouseY = 0;

        // Touch tracking
        this.lastTouchDistance = 0;

        // Initial camera position
        this.initialYaw = this.yaw;
        this.initialPitch = this.pitch;
        this.initialDistance = this.distance;

        this.init();
    }

    init() {
        const canvas = this.app.graphicsDevice.canvas;

        // Mouse events
        if (this.app.mouse) {
            canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
            canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
            canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
            canvas.addEventListener('wheel', this.onMouseWheel.bind(this));
        }

        // Touch events
        if (this.app.touch) {
            canvas.addEventListener('touchstart', this.onTouchStart.bind(this));
            canvas.addEventListener('touchmove', this.onTouchMove.bind(this));
            canvas.addEventListener('touchend', this.onTouchEnd.bind(this));
        }

        // Prevent context menu on right-click
        canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    }

    // Mouse Events
    onMouseDown(event) {
        if (event.button === 0 || event.button === 2) { // Left or right button
            this.isDragging = true;
            this.lastMouseX = event.clientX;
            this.lastMouseY = event.clientY;
        }
    }

    onMouseMove(event) {
        if (this.isDragging) {
            const deltaX = event.clientX - this.lastMouseX;
            const deltaY = event.clientY - this.lastMouseY;

            this.targetYaw -= deltaX * this.sensitivity;
            this.targetPitch -= deltaY * this.sensitivity;

            // Clamp pitch
            this.targetPitch = Math.max(-89, Math.min(89, this.targetPitch));

            this.lastMouseX = event.clientX;
            this.lastMouseY = event.clientY;
        }
    }

    onMouseUp(event) {
        if (event.button === 0 || event.button === 2) {
            this.isDragging = false;
        }
    }

    onMouseWheel(event) {
        event.preventDefault();

        const delta = event.deltaY > 0 ? 1 : -1;
        this.targetDistance += delta * this.zoomSpeed;
        this.targetDistance = Math.max(
            this.minDistance,
            Math.min(this.maxDistance, this.targetDistance)
        );
    }

    // Touch Events
    onTouchStart(event) {
        if (event.touches.length === 1) {
            // Single touch - rotate
            this.isDragging = true;
            this.lastMouseX = event.touches[0].clientX;
            this.lastMouseY = event.touches[0].clientY;
        } else if (event.touches.length === 2) {
            // Two finger touch - zoom
            this.lastTouchDistance = this.getTouchDistance(event.touches);
        }
    }

    onTouchMove(event) {
        event.preventDefault();

        if (event.touches.length === 1 && this.isDragging) {
            // Single touch - rotate
            const deltaX = event.touches[0].clientX - this.lastMouseX;
            const deltaY = event.touches[0].clientY - this.lastMouseY;

            this.targetYaw -= deltaX * this.sensitivity;
            this.targetPitch -= deltaY * this.sensitivity;

            this.targetPitch = Math.max(-89, Math.min(89, this.targetPitch));

            this.lastMouseX = event.touches[0].clientX;
            this.lastMouseY = event.touches[0].clientY;
        } else if (event.touches.length === 2) {
            // Two finger touch - zoom
            const distance = this.getTouchDistance(event.touches);
            const delta = this.lastTouchDistance - distance;

            this.targetDistance += delta * 0.01;
            this.targetDistance = Math.max(
                this.minDistance,
                Math.min(this.maxDistance, this.targetDistance)
            );

            this.lastTouchDistance = distance;
        }
    }

    onTouchEnd(event) {
        if (event.touches.length === 0) {
            this.isDragging = false;
        } else if (event.touches.length === 2) {
            this.lastTouchDistance = this.getTouchDistance(event.touches);
        }
    }

    getTouchDistance(touches) {
        const dx = touches[0].clientX - touches[1].clientX;
        const dy = touches[0].clientY - touches[1].clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // Update Loop
    update(dt) {
        if (!this.camera) return;

        // Smooth damping
        this.yaw += (this.targetYaw - this.yaw) * this.damping;
        this.pitch += (this.targetPitch - this.pitch) * this.damping;
        this.currentDistance += (this.targetDistance - this.currentDistance) * this.damping;

        // Calculate camera position
        const yawRad = this.yaw * pc.math.DEG_TO_RAD;
        const pitchRad = this.pitch * pc.math.DEG_TO_RAD;

        const x = this.target.x + this.currentDistance * Math.cos(pitchRad) * Math.sin(yawRad);
        const y = this.target.y + this.currentDistance * Math.sin(pitchRad);
        const z = this.target.z + this.currentDistance * Math.cos(pitchRad) * Math.cos(yawRad);

        this.camera.setPosition(x, y, z);
        this.camera.lookAt(this.target);
    }

    // Control Methods
    setTarget(target) {
        if (target instanceof pc.Vec3) {
            this.target.copy(target);
        } else if (target instanceof pc.Entity) {
            this.target.copy(target.getPosition());
        }
    }

    setDistance(distance) {
        this.targetDistance = Math.max(
            this.minDistance,
            Math.min(this.maxDistance, distance)
        );
    }

    setYaw(yaw) {
        this.targetYaw = yaw;
    }

    setPitch(pitch) {
        this.targetPitch = Math.max(-89, Math.min(89, pitch));
    }

    reset() {
        this.targetYaw = this.initialYaw;
        this.targetPitch = this.initialPitch;
        this.targetDistance = this.initialDistance;
    }

    focusOn(entity, distance = null) {
        if (entity instanceof pc.Entity) {
            this.setTarget(entity.getPosition());
        } else if (entity instanceof pc.Vec3) {
            this.setTarget(entity);
        }

        if (distance !== null) {
            this.setDistance(distance);
        }
    }

    // Animation
    animateTo(yaw, pitch, distance, duration = 1.0) {
        // Simple tween implementation
        const startYaw = this.yaw;
        const startPitch = this.pitch;
        const startDistance = this.currentDistance;

        const startTime = Date.now();

        const animate = () => {
            const elapsed = (Date.now() - startTime) / 1000;
            const t = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - t, 3);

            this.targetYaw = startYaw + (yaw - startYaw) * eased;
            this.targetPitch = startPitch + (pitch - startPitch) * eased;
            this.targetDistance = startDistance + (distance - startDistance) * eased;

            if (t < 1) {
                requestAnimationFrame(animate);
            }
        };

        animate();
    }

    // Utility
    getForwardVector() {
        return this.camera.forward.clone();
    }

    getRightVector() {
        return this.camera.right.clone();
    }

    getUpVector() {
        return this.camera.up.clone();
    }

    // Cleanup
    destroy() {
        // Remove event listeners if needed
        this.camera = null;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CameraController;
}
