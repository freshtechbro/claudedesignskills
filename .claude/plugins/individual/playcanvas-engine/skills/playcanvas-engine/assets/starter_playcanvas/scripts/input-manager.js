/**
 * Input Manager
 * Centralized input handling for keyboard, mouse, and touch
 */

class InputManager {
    constructor(app) {
        this.app = app;
        this.keyboard = app.keyboard;
        this.mouse = app.mouse;
        this.touch = app.touch;

        // Input state
        this.keys = {};
        this.mouseButtons = {};
        this.mousePosition = new pc.Vec2();
        this.mouseDelta = new pc.Vec2();
        this.mouseWheel = 0;

        // Touch state
        this.touches = [];
        this.touchCount = 0;

        this.init();
    }

    init() {
        // Keyboard events
        if (this.keyboard) {
            this.keyboard.on(pc.EVENT_KEYDOWN, this.onKeyDown.bind(this));
            this.keyboard.on(pc.EVENT_KEYUP, this.onKeyUp.bind(this));
        }

        // Mouse events
        if (this.mouse) {
            this.mouse.on(pc.EVENT_MOUSEDOWN, this.onMouseDown.bind(this));
            this.mouse.on(pc.EVENT_MOUSEUP, this.onMouseUp.bind(this));
            this.mouse.on(pc.EVENT_MOUSEMOVE, this.onMouseMove.bind(this));
            this.mouse.on(pc.EVENT_MOUSEWHEEL, this.onMouseWheel.bind(this));
        }

        // Touch events
        if (this.touch) {
            this.touch.on(pc.EVENT_TOUCHSTART, this.onTouchStart.bind(this));
            this.touch.on(pc.EVENT_TOUCHEND, this.onTouchEnd.bind(this));
            this.touch.on(pc.EVENT_TOUCHMOVE, this.onTouchMove.bind(this));
            this.touch.on(pc.EVENT_TOUCHCANCEL, this.onTouchCancel.bind(this));
        }
    }

    // Keyboard Methods
    onKeyDown(event) {
        this.keys[event.key] = true;
    }

    onKeyUp(event) {
        this.keys[event.key] = false;
    }

    isKeyPressed(key) {
        return this.keys[key] === true;
    }

    wasKeyPressed(key) {
        if (this.keyboard) {
            return this.keyboard.wasPressed(key);
        }
        return false;
    }

    wasKeyReleased(key) {
        if (this.keyboard) {
            return this.keyboard.wasReleased(key);
        }
        return false;
    }

    // Mouse Methods
    onMouseDown(event) {
        this.mouseButtons[event.button] = true;
    }

    onMouseUp(event) {
        this.mouseButtons[event.button] = false;
    }

    onMouseMove(event) {
        this.mousePosition.set(event.x, event.y);
        this.mouseDelta.set(event.dx, event.dy);
    }

    onMouseWheel(event) {
        this.mouseWheel = event.wheel;
    }

    isMouseButtonPressed(button) {
        return this.mouseButtons[button] === true;
    }

    getMousePosition() {
        if (this.mouse) {
            return new pc.Vec2(this.mouse.x, this.mouse.y);
        }
        return this.mousePosition.clone();
    }

    getMouseDelta() {
        return this.mouseDelta.clone();
    }

    getMouseWheel() {
        return this.mouseWheel;
    }

    // Touch Methods
    onTouchStart(event) {
        this.updateTouches(event);
    }

    onTouchEnd(event) {
        this.updateTouches(event);
    }

    onTouchMove(event) {
        this.updateTouches(event);
    }

    onTouchCancel(event) {
        this.touches = [];
        this.touchCount = 0;
    }

    updateTouches(event) {
        if (!this.touch) return;

        this.touches = [];
        this.touchCount = event.touches.length;

        for (let i = 0; i < event.touches.length; i++) {
            const touch = event.touches[i];
            this.touches.push({
                id: touch.id,
                x: touch.x,
                y: touch.y,
                dx: touch.dx || 0,
                dy: touch.dy || 0
            });
        }
    }

    getTouchCount() {
        return this.touchCount;
    }

    getTouch(index) {
        if (index >= 0 && index < this.touches.length) {
            return this.touches[index];
        }
        return null;
    }

    getTouches() {
        return this.touches;
    }

    // Utility Methods
    getInputVector(upKey, downKey, leftKey, rightKey) {
        const vector = new pc.Vec2(0, 0);

        if (this.isKeyPressed(upKey)) vector.y += 1;
        if (this.isKeyPressed(downKey)) vector.y -= 1;
        if (this.isKeyPressed(leftKey)) vector.x -= 1;
        if (this.isKeyPressed(rightKey)) vector.x += 1;

        // Normalize diagonal movement
        if (vector.length() > 0) {
            vector.normalize();
        }

        return vector;
    }

    getWASDInput() {
        return this.getInputVector(
            pc.KEY_W,
            pc.KEY_S,
            pc.KEY_A,
            pc.KEY_D
        );
    }

    getArrowKeysInput() {
        return this.getInputVector(
            pc.KEY_UP,
            pc.KEY_DOWN,
            pc.KEY_LEFT,
            pc.KEY_RIGHT
        );
    }

    // Raycast from screen position
    screenToWorldRay(screenX, screenY, camera) {
        if (!camera || !camera.camera) return null;

        const worldPos = camera.camera.screenToWorld(
            screenX,
            screenY,
            camera.camera.farClip
        );

        return {
            origin: camera.getPosition(),
            direction: worldPos.clone().sub(camera.getPosition()).normalize(),
            end: worldPos
        };
    }

    // Get raycast from mouse
    getMouseRay(camera) {
        if (!this.mouse || !camera) return null;

        return this.screenToWorldRay(
            this.mouse.x,
            this.mouse.y,
            camera
        );
    }

    // Perform raycast
    raycast(from, to) {
        return this.app.systems.rigidbody.raycastFirst(from, to);
    }

    raycastAll(from, to) {
        return this.app.systems.rigidbody.raycastAll(from, to);
    }

    // Cleanup
    destroy() {
        this.keys = {};
        this.mouseButtons = {};
        this.touches = [];
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InputManager;
}
