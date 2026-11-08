#!/usr/bin/env python3
"""
PlayCanvas Component Builder
Generates PlayCanvas script components with lifecycle methods and attributes.

Usage:
    Interactive mode:
        python component_builder.py

    CLI mode:
        python component_builder.py --name MyComponent --type basic --output ./
        python component_builder.py -n PlayerController -t character -o ./scripts/
        python component_builder.py -n CameraOrbit -t camera --attributes
"""

import argparse
import os
import sys
from typing import Dict, Tuple, List


# Component templates
def generate_basic_component(name: str, include_attributes: bool = True) -> str:
    """Generate a basic PlayCanvas script component"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    attributes = ""
    if include_attributes:
        attributes = f"""
// Attributes (editable in Editor)
{class_name}.attributes.add('enabled', {{
    type: 'boolean',
    default: true,
    title: 'Enabled'
}});

{class_name}.attributes.add('speed', {{
    type: 'number',
    default: 1.0,
    title: 'Speed',
    description: 'Component speed multiplier'
}});
"""

    return f"""/**
 * {class_name} Component
 * Basic PlayCanvas script component template
 *
 * Usage:
 * 1. Attach to entity via Editor or code
 * 2. Configure attributes in Inspector
 * 3. Access via: entity.script.{script_name}
 */

var {class_name} = pc.createScript('{script_name}');
{attributes}
/**
 * Initialize component
 * Called once when script is enabled
 */
{class_name}.prototype.initialize = function() {{
    console.log('{class_name} initialized');

    // Store references
    this.entity.script.{script_name}.active = true;
}};

/**
 * Update method called every frame
 * @param {{number}} dt - Delta time in seconds
 */
{class_name}.prototype.update = function(dt) {{
    if (!this.enabled) return;

    // Update logic here
}};

/**
 * Post-update method called after all update methods
 * @param {{number}} dt - Delta time in seconds
 */
{class_name}.prototype.postUpdate = function(dt) {{
    // Post-update logic here
}};

/**
 * Swap method called when script is hot-reloaded
 * @param {{object}} old - Old script instance
 */
{class_name}.prototype.swap = function(old) {{
    // Preserve state during hot-reload
    this.enabled = old.enabled;
}};
"""


def generate_interactive_component(name: str) -> str:
    """Generate interactive component with mouse/touch handling"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * Interactive component with mouse and touch input handling
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('hoverColor', {{
    type: 'rgb',
    default: [0.5, 0.8, 1.0],
    title: 'Hover Color'
}});

{class_name}.attributes.add('clickScale', {{
    type: 'number',
    default: 0.9,
    title: 'Click Scale'
}});

{class_name}.prototype.initialize = function() {{
    this.originalColor = null;
    this.originalScale = this.entity.getLocalScale().clone();
    this.isHovered = false;
    this.isPressed = false;

    // Store material reference
    if (this.entity.model) {{
        this.material = this.entity.model.material;
        this.originalColor = this.material.diffuse.clone();
    }}

    // Mouse events
    if (this.app.mouse) {{
        this.app.mouse.on(pc.EVENT_MOUSEDOWN, this.onMouseDown, this);
        this.app.mouse.on(pc.EVENT_MOUSEUP, this.onMouseUp, this);
    }}

    // Touch events
    if (this.app.touch) {{
        this.app.touch.on(pc.EVENT_TOUCHSTART, this.onTouchStart, this);
        this.app.touch.on(pc.EVENT_TOUCHEND, this.onTouchEnd, this);
    }}
}};

{class_name}.prototype.update = function(dt) {{
    if (!this.app.mouse) return;

    // Raycast from mouse
    const camera = this.app.root.findByName('Camera');
    if (!camera) return;

    const ray = camera.camera.screenToWorld(
        this.app.mouse.x,
        this.app.mouse.y,
        camera.camera.farClip
    );

    const from = camera.getPosition();
    const to = ray;

    const result = this.app.systems.rigidbody.raycastFirst(from, to);

    // Check if hovering
    const wasHovered = this.isHovered;
    this.isHovered = result && result.entity === this.entity;

    if (this.isHovered && !wasHovered) {{
        this.onHoverEnter();
    }} else if (!this.isHovered && wasHovered) {{
        this.onHoverExit();
    }}
}};

{class_name}.prototype.onHoverEnter = function() {{
    if (this.material && this.originalColor) {{
        this.material.diffuse.set(
            this.hoverColor[0],
            this.hoverColor[1],
            this.hoverColor[2]
        );
        this.material.update();
    }}
    this.fire('hover:enter');
}};

{class_name}.prototype.onHoverExit = function() {{
    if (this.material && this.originalColor) {{
        this.material.diffuse.copy(this.originalColor);
        this.material.update();
    }}
    this.fire('hover:exit');
}};

{class_name}.prototype.onMouseDown = function(event) {{
    if (!this.isHovered) return;

    this.isPressed = true;
    this.entity.setLocalScale(
        this.originalScale.x * this.clickScale,
        this.originalScale.y * this.clickScale,
        this.originalScale.z * this.clickScale
    );

    this.fire('click', {{ button: event.button }});
}};

{class_name}.prototype.onMouseUp = function(event) {{
    if (!this.isPressed) return;

    this.isPressed = false;
    this.entity.setLocalScale(this.originalScale);

    if (this.isHovered) {{
        this.fire('click:release');
    }}
}};

{class_name}.prototype.onTouchStart = function(event) {{
    this.onMouseDown({{ button: 0 }});
}};

{class_name}.prototype.onTouchEnd = function(event) {{
    this.onMouseUp({{ button: 0 }});
}};
"""


def generate_animation_component(name: str) -> str:
    """Generate component for animation control"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * Controls entity animations with state management
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('idleAnim', {{
    type: 'string',
    default: 'Idle',
    title: 'Idle Animation'
}});

{class_name}.attributes.add('walkAnim', {{
    type: 'string',
    default: 'Walk',
    title: 'Walk Animation'
}});

{class_name}.attributes.add('runAnim', {{
    type: 'string',
    default: 'Run',
    title: 'Run Animation'
}});

{class_name}.attributes.add('blendTime', {{
    type: 'number',
    default: 0.2,
    title: 'Blend Time',
    description: 'Animation blend time in seconds'
}});

{class_name}.prototype.initialize = function() {{
    this.currentState = 'idle';
    this.animComponent = this.entity.anim;

    if (!this.animComponent) {{
        console.warn('{class_name}: No anim component found');
        return;
    }}

    // Play initial animation
    this.setState('idle');
}};

{class_name}.prototype.setState = function(state) {{
    if (this.currentState === state) return;

    const animName = this.getAnimationName(state);
    if (!animName) {{
        console.warn(`{class_name}: Unknown state "${{state}}"`);
        return;
    }}

    // Blend to new animation
    this.animComponent.setBoolean(state, true);

    this.currentState = state;
    this.fire('state:change', {{ from: this.currentState, to: state }});
}};

{class_name}.prototype.getAnimationName = function(state) {{
    switch (state) {{
        case 'idle': return this.idleAnim;
        case 'walk': return this.walkAnim;
        case 'run': return this.runAnim;
        default: return null;
    }}
}};

{class_name}.prototype.playAnimation = function(name, loop = true) {{
    if (!this.animComponent) return;

    const layer = this.animComponent.baseLayer;
    layer.transition(name, this.blendTime);

    if (loop) {{
        this.animComponent.setBoolean('loop', true);
    }}
}};

{class_name}.prototype.update = function(dt) {{
    // Override to add state logic
    // Example: this.setState('walk') based on velocity
}};
"""


def generate_physics_component(name: str) -> str:
    """Generate physics-based component"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * Physics-based component with force and impulse control
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('mass', {{
    type: 'number',
    default: 1.0,
    title: 'Mass'
}});

{class_name}.attributes.add('friction', {{
    type: 'number',
    default: 0.5,
    title: 'Friction'
}});

{class_name}.attributes.add('restitution', {{
    type: 'number',
    default: 0.3,
    title: 'Restitution',
    description: 'Bounciness (0-1)'
}});

{class_name}.attributes.add('linearDamping', {{
    type: 'number',
    default: 0.1,
    title: 'Linear Damping'
}});

{class_name}.attributes.add('angularDamping', {{
    type: 'number',
    default: 0.1,
    title: 'Angular Damping'
}});

{class_name}.prototype.initialize = function() {{
    this.rigidbody = this.entity.rigidbody;

    if (!this.rigidbody) {{
        console.warn('{class_name}: No rigidbody component found');
        return;
    }}

    // Configure physics properties
    this.rigidbody.mass = this.mass;
    this.rigidbody.friction = this.friction;
    this.rigidbody.restitution = this.restitution;
    this.rigidbody.linearDamping = this.linearDamping;
    this.rigidbody.angularDamping = this.angularDamping;

    // Listen to collision events
    this.entity.collision.on('contact', this.onContact, this);
    this.entity.collision.on('collisionstart', this.onCollisionStart, this);
    this.entity.collision.on('collisionend', this.onCollisionEnd, this);
}};

{class_name}.prototype.applyForce = function(force) {{
    if (!this.rigidbody) return;
    this.rigidbody.applyForce(force.x, force.y, force.z);
}};

{class_name}.prototype.applyImpulse = function(impulse) {{
    if (!this.rigidbody) return;
    this.rigidbody.applyImpulse(impulse.x, impulse.y, impulse.z);
}};

{class_name}.prototype.applyTorque = function(torque) {{
    if (!this.rigidbody) return;
    this.rigidbody.applyTorque(torque.x, torque.y, torque.z);
}};

{class_name}.prototype.applyTorqueImpulse = function(torque) {{
    if (!this.rigidbody) return;
    this.rigidbody.applyTorqueImpulse(torque.x, torque.y, torque.z);
}};

{class_name}.prototype.onContact = function(result) {{
    // Called every frame during contact
    this.fire('physics:contact', {{ result: result }});
}};

{class_name}.prototype.onCollisionStart = function(result) {{
    console.log('Collision started with:', result.other.name);
    this.fire('physics:collision:start', {{ result: result }});
}};

{class_name}.prototype.onCollisionEnd = function(other) {{
    console.log('Collision ended with:', other.name);
    this.fire('physics:collision:end', {{ other: other }});
}};

{class_name}.prototype.update = function(dt) {{
    // Access velocity
    const velocity = this.rigidbody.linearVelocity;
    const speed = velocity.length();

    // Example: Apply drag at high speeds
    if (speed > 10) {{
        const drag = velocity.clone().scale(-0.1);
        this.applyForce(drag);
    }}
}};
"""


def generate_character_controller(name: str) -> str:
    """Generate character controller component"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * Third-person character controller with WASD movement
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('speed', {{
    type: 'number',
    default: 5.0,
    title: 'Movement Speed'
}});

{class_name}.attributes.add('jumpForce', {{
    type: 'number',
    default: 10.0,
    title: 'Jump Force'
}});

{class_name}.attributes.add('rotationSpeed', {{
    type: 'number',
    default: 180,
    title: 'Rotation Speed',
    description: 'Degrees per second'
}});

{class_name}.attributes.add('camera', {{
    type: 'entity',
    title: 'Camera Entity'
}});

{class_name}.prototype.initialize = function() {{
    this.velocity = new pc.Vec3();
    this.isGrounded = false;
    this.moveDirection = new pc.Vec3();

    // Collision detection for grounding
    if (this.entity.collision) {{
        this.entity.collision.on('collisionstart', this.onCollisionStart, this);
        this.entity.collision.on('collisionend', this.onCollisionEnd, this);
    }}
}};

{class_name}.prototype.update = function(dt) {{
    this.handleMovement(dt);
    this.handleJump();
    this.handleRotation(dt);
}};

{class_name}.prototype.handleMovement = function(dt) {{
    const keyboard = this.app.keyboard;

    // Get camera forward and right vectors
    const forward = this.camera ?
        this.camera.forward.clone() :
        new pc.Vec3(0, 0, -1);

    const right = this.camera ?
        this.camera.right.clone() :
        new pc.Vec3(1, 0, 0);

    // Flatten to horizontal plane
    forward.y = 0;
    forward.normalize();
    right.y = 0;
    right.normalize();

    // Calculate movement direction
    this.moveDirection.set(0, 0, 0);

    if (keyboard.isPressed(pc.KEY_W)) {{
        this.moveDirection.add(forward);
    }}
    if (keyboard.isPressed(pc.KEY_S)) {{
        this.moveDirection.sub(forward);
    }}
    if (keyboard.isPressed(pc.KEY_A)) {{
        this.moveDirection.sub(right);
    }}
    if (keyboard.isPressed(pc.KEY_D)) {{
        this.moveDirection.add(right);
    }}

    // Normalize and apply speed
    if (this.moveDirection.length() > 0) {{
        this.moveDirection.normalize();
        this.moveDirection.scale(this.speed * dt);

        // Move entity
        const pos = this.entity.getPosition();
        pos.add(this.moveDirection);
        this.entity.setPosition(pos);
    }}
}};

{class_name}.prototype.handleJump = function() {{
    const keyboard = this.app.keyboard;

    if (keyboard.wasPressed(pc.KEY_SPACE) && this.isGrounded) {{
        if (this.entity.rigidbody) {{
            this.entity.rigidbody.applyImpulse(0, this.jumpForce, 0);
        }}
    }}
}};

{class_name}.prototype.handleRotation = function(dt) {{
    if (this.moveDirection.length() > 0) {{
        const targetAngle = Math.atan2(this.moveDirection.x, this.moveDirection.z) * pc.math.RAD_TO_DEG;
        const currentAngles = this.entity.getEulerAngles();

        // Smoothly rotate towards movement direction
        const newY = this.lerpAngle(
            currentAngles.y,
            targetAngle,
            this.rotationSpeed * dt
        );

        this.entity.setEulerAngles(currentAngles.x, newY, currentAngles.z);
    }}
}};

{class_name}.prototype.lerpAngle = function(from, to, t) {{
    let diff = to - from;
    while (diff > 180) diff -= 360;
    while (diff < -180) diff += 360;
    return from + diff * Math.min(t / 180, 1);
}};

{class_name}.prototype.onCollisionStart = function(result) {{
    // Check if collision is below (ground)
    const contact = result.contacts[0];
    if (contact && contact.normal.y > 0.5) {{
        this.isGrounded = true;
    }}
}};

{class_name}.prototype.onCollisionEnd = function(other) {{
    this.isGrounded = false;
}};
"""


def generate_camera_controller(name: str) -> str:
    """Generate orbit camera controller"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * Orbit camera controller with mouse/touch input
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('target', {{
    type: 'entity',
    title: 'Target Entity'
}});

{class_name}.attributes.add('distance', {{
    type: 'number',
    default: 10,
    title: 'Distance'
}});

{class_name}.attributes.add('minDistance', {{
    type: 'number',
    default: 2,
    title: 'Min Distance'
}});

{class_name}.attributes.add('maxDistance', {{
    type: 'number',
    default: 20,
    title: 'Max Distance'
}});

{class_name}.attributes.add('sensitivity', {{
    type: 'number',
    default: 0.3,
    title: 'Sensitivity'
}});

{class_name}.attributes.add('damping', {{
    type: 'number',
    default: 0.1,
    title: 'Damping'
}});

{class_name}.prototype.initialize = function() {{
    this.yaw = 0;
    this.pitch = 0;
    this.currentDistance = this.distance;

    this.targetYaw = 0;
    this.targetPitch = 0;

    // Mouse events
    if (this.app.mouse) {{
        this.app.mouse.on(pc.EVENT_MOUSEMOVE, this.onMouseMove, this);
        this.app.mouse.on(pc.EVENT_MOUSEWHEEL, this.onMouseWheel, this);
    }}

    // Touch events
    if (this.app.touch) {{
        this.app.touch.on(pc.EVENT_TOUCHMOVE, this.onTouchMove, this);
    }}
}};

{class_name}.prototype.update = function(dt) {{
    if (!this.target) return;

    // Smooth damping
    this.yaw = pc.math.lerp(this.yaw, this.targetYaw, this.damping);
    this.pitch = pc.math.lerp(this.pitch, this.targetPitch, this.damping);

    // Clamp pitch
    this.pitch = pc.math.clamp(this.pitch, -89, 89);

    // Calculate camera position
    const targetPos = this.target.getPosition();

    const yawRad = this.yaw * pc.math.DEG_TO_RAD;
    const pitchRad = this.pitch * pc.math.DEG_TO_RAD;

    const x = targetPos.x + this.currentDistance * Math.cos(pitchRad) * Math.sin(yawRad);
    const y = targetPos.y + this.currentDistance * Math.sin(pitchRad);
    const z = targetPos.z + this.currentDistance * Math.cos(pitchRad) * Math.cos(yawRad);

    this.entity.setPosition(x, y, z);
    this.entity.lookAt(targetPos);
}};

{class_name}.prototype.onMouseMove = function(event) {{
    if (!event.buttons[pc.MOUSEBUTTON_LEFT]) return;

    this.targetYaw -= event.dx * this.sensitivity;
    this.targetPitch -= event.dy * this.sensitivity;
}};

{class_name}.prototype.onMouseWheel = function(event) {{
    this.currentDistance -= event.wheelDelta * 0.5;
    this.currentDistance = pc.math.clamp(
        this.currentDistance,
        this.minDistance,
        this.maxDistance
    );
}};

{class_name}.prototype.onTouchMove = function(event) {{
    if (event.touches.length !== 1) return;

    const touch = event.touches[0];
    this.targetYaw -= touch.dx * this.sensitivity;
    this.targetPitch -= touch.dy * this.sensitivity;
}};
"""


def generate_ui_component(name: str) -> str:
    """Generate UI component with screen-space interaction"""
    class_name = name[0].upper() + name[1:]
    script_name = name[0].lower() + name[1:]

    return f"""/**
 * {class_name} Component
 * UI component with button-like behavior
 */

var {class_name} = pc.createScript('{script_name}');

{class_name}.attributes.add('hoverScale', {{
    type: 'number',
    default: 1.1,
    title: 'Hover Scale'
}});

{class_name}.attributes.add('clickScale', {{
    type: 'number',
    default: 0.95,
    title: 'Click Scale'
}});

{class_name}.attributes.add('transitionSpeed', {{
    type: 'number',
    default: 10,
    title: 'Transition Speed'
}});

{class_name}.prototype.initialize = function() {{
    this.originalScale = this.entity.getLocalScale().clone();
    this.targetScale = this.originalScale.clone();
    this.isHovered = false;
    this.isPressed = false;

    // Add element component if not present
    if (!this.entity.element) {{
        console.warn('{class_name}: No element component found');
        return;
    }}

    // Mouse events
    this.entity.element.on('mouseenter', this.onMouseEnter, this);
    this.entity.element.on('mouseleave', this.onMouseLeave, this);
    this.entity.element.on('mousedown', this.onMouseDown, this);
    this.entity.element.on('mouseup', this.onMouseUp, this);
    this.entity.element.on('click', this.onClick, this);

    // Touch events
    this.entity.element.on('touchstart', this.onTouchStart, this);
    this.entity.element.on('touchend', this.onTouchEnd, this);
}};

{class_name}.prototype.update = function(dt) {{
    // Smooth scale transition
    const current = this.entity.getLocalScale();
    const lerped = new pc.Vec3().lerp(
        current,
        this.targetScale,
        this.transitionSpeed * dt
    );
    this.entity.setLocalScale(lerped);
}};

{class_name}.prototype.onMouseEnter = function() {{
    this.isHovered = true;
    this.targetScale.copy(this.originalScale).scale(this.hoverScale);
    this.fire('hover:enter');
}};

{class_name}.prototype.onMouseLeave = function() {{
    this.isHovered = false;
    if (!this.isPressed) {{
        this.targetScale.copy(this.originalScale);
    }}
    this.fire('hover:exit');
}};

{class_name}.prototype.onMouseDown = function() {{
    this.isPressed = true;
    this.targetScale.copy(this.originalScale).scale(this.clickScale);
    this.fire('press');
}};

{class_name}.prototype.onMouseUp = function() {{
    this.isPressed = false;
    if (this.isHovered) {{
        this.targetScale.copy(this.originalScale).scale(this.hoverScale);
    }} else {{
        this.targetScale.copy(this.originalScale);
    }}
    this.fire('release');
}};

{class_name}.prototype.onClick = function() {{
    console.log('{class_name} clicked');
    this.fire('click');
}};

{class_name}.prototype.onTouchStart = function() {{
    this.onMouseDown();
}};

{class_name}.prototype.onTouchEnd = function() {{
    this.onMouseUp();
    this.fire('click');
}};
"""


# Component type registry
COMPONENT_TYPES: Dict[str, Dict] = {{
    'basic': {{
        'name': 'Basic Component',
        'description': 'Simple component with lifecycle methods',
        'generator': generate_basic_component
    }},
    'interactive': {{
        'name': 'Interactive Component',
        'description': 'Mouse and touch interaction handling',
        'generator': lambda name: generate_interactive_component(name)
    }},
    'animation': {{
        'name': 'Animation Controller',
        'description': 'Animation state management',
        'generator': lambda name: generate_animation_component(name)
    }},
    'physics': {{
        'name': 'Physics Component',
        'description': 'Physics-based component with forces',
        'generator': lambda name: generate_physics_component(name)
    }},
    'character': {{
        'name': 'Character Controller',
        'description': 'Third-person character movement',
        'generator': lambda name: generate_character_controller(name)
    }},
    'camera': {{
        'name': 'Camera Controller',
        'description': 'Orbit camera with mouse control',
        'generator': lambda name: generate_camera_controller(name)
    }},
    'ui': {{
        'name': 'UI Component',
        'description': 'Screen-space UI element',
        'generator': lambda name: generate_ui_component(name)
    }}
}}


def interactive_mode():
    """Run interactive component builder"""
    print("\n" + "="*60)
    print("PlayCanvas Component Builder - Interactive Mode")
    print("="*60)

    # Get component name
    while True:
        name = input("\nComponent name (e.g., PlayerController): ").strip()
        if name:
            # Validate name
            if not name[0].isalpha():
                print("Error: Component name must start with a letter")
                continue
            if not name.replace('_', '').isalnum():
                print("Error: Component name can only contain letters, numbers, and underscores")
                continue
            break
        print("Error: Component name is required")

    # Show component types
    print("\nAvailable component types:")
    print("-" * 60)
    for idx, (key, info) in enumerate(COMPONENT_TYPES.items(), 1):
        print(f"{idx}. {info['name']:25} - {info['description']}")

    # Get component type
    while True:
        try:
            choice = input(f"\nSelect component type (1-{len(COMPONENT_TYPES)}): ").strip()
            idx = int(choice)
            if 1 <= idx <= len(COMPONENT_TYPES):
                component_type = list(COMPONENT_TYPES.keys())[idx - 1]
                break
            print(f"Error: Please enter a number between 1 and {len(COMPONENT_TYPES)}")
        except ValueError:
            print("Error: Please enter a valid number")

    # Include attributes for basic component
    include_attributes = True
    if component_type == 'basic':
        attr_choice = input("\nInclude attribute definitions? (y/n): ").strip().lower()
        include_attributes = attr_choice in ['y', 'yes', '']

    # Get output path
    output_dir = input("\nOutput directory (default: current directory): ").strip()
    if not output_dir:
        output_dir = "."

    # Generate component
    print("\n" + "-"*60)
    print("Generating component...")

    try:
        if component_type == 'basic':
            code = generate_basic_component(name, include_attributes)
        else:
            generator = COMPONENT_TYPES[component_type]['generator']
            code = generator(name)

        # Create output file
        script_name = name[0].lower() + name[1:]
        filename = f"{script_name}.js"
        filepath = os.path.join(output_dir, filename)

        # Create directory if needed
        os.makedirs(output_dir, exist_ok=True)

        # Write file
        with open(filepath, 'w') as f:
            f.write(code)

        print(f"\n✓ Component created: {filepath}")
        print(f"\nComponent type: {COMPONENT_TYPES[component_type]['name']}")
        print(f"Lines of code: {len(code.splitlines())}")

        print("\nUsage:")
        print(f"1. Add script to PlayCanvas project")
        print(f"2. Attach to entity via Editor or code:")
        print(f"   entity.addComponent('script');")
        print(f"   entity.script.create('{script_name}');")
        print(f"3. Configure attributes in Inspector")

    except Exception as e:
        print(f"\nError: Failed to generate component: {e}")
        return 1

    return 0


def cli_mode(args):
    """Run CLI component builder"""
    name = args.name
    component_type = args.type
    output_dir = args.output
    include_attributes = args.attributes

    # Validate inputs
    if component_type not in COMPONENT_TYPES:
        print(f"Error: Unknown component type '{component_type}'")
        print(f"Available types: {', '.join(COMPONENT_TYPES.keys())}")
        return 1

    # Generate component
    try:
        if component_type == 'basic':
            code = generate_basic_component(name, include_attributes)
        else:
            generator = COMPONENT_TYPES[component_type]['generator']
            code = generator(name)

        # Create output file
        script_name = name[0].lower() + name[1:]
        filename = f"{script_name}.js"
        filepath = os.path.join(output_dir, filename)

        # Create directory if needed
        os.makedirs(output_dir, exist_ok=True)

        # Write file
        with open(filepath, 'w') as f:
            f.write(code)

        print(f"✓ Component created: {filepath}")
        return 0

    except Exception as e:
        print(f"Error: Failed to generate component: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='PlayCanvas Component Builder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python component_builder.py

  Generate basic component:
    python component_builder.py --name MyComponent --type basic --output ./

  Generate character controller:
    python component_builder.py -n PlayerController -t character -o ./scripts/

  Generate camera controller:
    python component_builder.py -n OrbitCamera -t camera -o ./scripts/

Available component types:
  basic       - Basic component with lifecycle methods
  interactive - Mouse and touch interaction
  animation   - Animation state management
  physics     - Physics-based component
  character   - Third-person character controller
  camera      - Orbit camera controller
  ui          - Screen-space UI element
        """
    )

    parser.add_argument(
        '-n', '--name',
        help='Component name (e.g., PlayerController)'
    )

    parser.add_argument(
        '-t', '--type',
        choices=list(COMPONENT_TYPES.keys()),
        help='Component type'
    )

    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--attributes',
        action='store_true',
        default=True,
        help='Include attribute definitions (for basic type)'
    )

    args = parser.parse_args()

    # Run interactive mode if no arguments
    if not args.name or not args.type:
        return interactive_mode()

    return cli_mode(args)


if __name__ == '__main__':
    sys.exit(main())
