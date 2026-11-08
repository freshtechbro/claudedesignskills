#!/usr/bin/env python3
"""
A-Frame Component Builder

Generates custom A-Frame component boilerplate for various use cases:
- Basic components
- Interactive components (hover, click)
- Animation components
- Physics-based components
- Networked components
- VR controller components

Usage:
    python component_builder.py basic my-component
    python component_builder.py interactive clickable-box
    python component_builder.py animation rotating-cube
    python component_builder.py --interactive
"""

import argparse
import sys
from pathlib import Path

# Component templates
COMPONENT_TEMPLATES = {
    'basic': {
        'description': 'Basic component with schema and lifecycle',
        'schema_props': ['enabled: boolean', 'speed: number'],
        'has_tick': False
    },
    'interactive': {
        'description': 'Component with mouse/VR interaction events',
        'schema_props': ['hoverColor: color', 'clickColor: color'],
        'has_tick': False
    },
    'animation': {
        'description': 'Component with tick() for continuous animation',
        'schema_props': ['speed: number', 'axis: string'],
        'has_tick': True
    },
    'physics': {
        'description': 'Component for physics interactions',
        'schema_props': ['force: number', 'direction: vec3'],
        'has_tick': True
    },
    'controller': {
        'description': 'VR controller interaction component',
        'schema_props': ['hand: string', 'button: string'],
        'has_tick': False
    },
    'networked': {
        'description': 'Networked component for multi-user scenes',
        'schema_props': ['syncInterval: number', 'owner: string'],
        'has_tick': True
    },
    'loader': {
        'description': 'Asset loading component',
        'schema_props': ['src: string', 'onLoad: string'],
        'has_tick': False
    }
}

def generate_basic_component(name):
    """Generate basic component template"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Basic A-Frame component with schema and lifecycle methods

AFRAME.registerComponent('{component_name}', {{
  // Component schema (configuration properties)
  schema: {{
    enabled: {{ type: 'boolean', default: true }},
    speed: {{ type: 'number', default: 1 }},
    color: {{ type: 'color', default: '#FFF' }}
  }},

  // Initialize (called once when component is attached)
  init: function() {{
    console.log('{component_name} initialized');

    // Store references
    this.el; // The entity element
    this.data; // Component data from schema
    this.el.sceneEl; // The scene element

    // Setup code here
  }},

  // Update (called when component properties change)
  update: function(oldData) {{
    // this.data contains new values
    // oldData contains previous values

    if (this.data.enabled !== oldData.enabled) {{
      console.log('Enabled changed to:', this.data.enabled);
    }}

    if (this.data.speed !== oldData.speed) {{
      console.log('Speed changed to:', this.data.speed);
    }}
  }},

  // Remove (called when component is removed from entity)
  remove: function() {{
    // Cleanup code here
    console.log('{component_name} removed');
  }},

  // Pause (called when entity/scene pauses)
  pause: function() {{
    console.log('{component_name} paused');
  }},

  // Play (called when entity/scene plays)
  play: function() {{
    console.log('{component_name} playing');
  }}
}});

// Usage:
// <a-entity {component_name}="enabled: true; speed: 2; color: #FF0000"></a-entity>
'''

def generate_interactive_component(name):
    """Generate interactive component with events"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Interactive component with mouse and VR controller events

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    hoverColor: {{ type: 'color', default: '#FFFF00' }},
    clickColor: {{ type: 'color', default: '#FF0000' }},
    enabled: {{ type: 'boolean', default: true }}
  }},

  init: function() {{
    const el = this.el;
    const data = this.data;

    // Store original color
    this.originalColor = el.getAttribute('material').color;

    // Bind event handlers (important for proper 'this' context)
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseLeave = this.onMouseLeave.bind(this);
    this.onClick = this.onClick.bind(this);

    // Add event listeners
    el.addEventListener('mouseenter', this.onMouseEnter);
    el.addEventListener('mouseleave', this.onMouseLeave);
    el.addEventListener('click', this.onClick);

    // VR controller events
    el.addEventListener('triggerdown', this.onClick);
  }},

  update: function(oldData) {{
    // Update behavior based on enabled state
    if (!this.data.enabled && oldData.enabled) {{
      // Reset to original color when disabled
      this.el.setAttribute('material', 'color', this.originalColor);
    }}
  }},

  onMouseEnter: function(evt) {{
    if (!this.data.enabled) return;

    console.log('Mouse entered');
    this.el.setAttribute('material', 'color', this.data.hoverColor);
    this.el.setAttribute('scale', {{
      x: 1.1,
      y: 1.1,
      z: 1.1
    }});
  }},

  onMouseLeave: function(evt) {{
    if (!this.data.enabled) return;

    console.log('Mouse left');
    this.el.setAttribute('material', 'color', this.originalColor);
    this.el.setAttribute('scale', {{
      x: 1,
      y: 1,
      z: 1
    }});
  }},

  onClick: function(evt) {{
    if (!this.data.enabled) return;

    console.log('Clicked!', evt.detail);
    this.el.setAttribute('material', 'color', this.data.clickColor);

    // Emit custom event
    this.el.emit('{component_name}-clicked', {{
      position: evt.detail.intersection ? evt.detail.intersection.point : null
    }});

    // Reset color after 500ms
    setTimeout(() => {{
      this.el.setAttribute('material', 'color', this.originalColor);
    }}, 500);
  }},

  remove: function() {{
    // Remove event listeners
    const el = this.el;
    el.removeEventListener('mouseenter', this.onMouseEnter);
    el.removeEventListener('mouseleave', this.onMouseLeave);
    el.removeEventListener('click', this.onClick);
    el.removeEventListener('triggerdown', this.onClick);
  }}
}});

// Usage:
// <a-camera>
//   <a-cursor raycaster="objects: .interactive"></a-cursor>
// </a-camera>
// <a-box class="interactive" {component_name}="hoverColor: yellow; clickColor: red"></a-box>
'''

def generate_animation_component(name):
    """Generate animation component with tick()"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Animation component using tick() for continuous updates

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    speed: {{ type: 'number', default: 1 }},
    axis: {{ type: 'string', default: 'y', oneOf: ['x', 'y', 'z'] }},
    enabled: {{ type: 'boolean', default: true }}
  }},

  init: function() {{
    // Store rotation state
    this.rotation = {{
      x: 0,
      y: 0,
      z: 0
    }};
  }},

  // tick() is called every frame
  tick: function(time, timeDelta) {{
    if (!this.data.enabled) return;

    // timeDelta is time since last frame (milliseconds)
    // Use it for frame-rate independent animation
    const rotationAmount = this.data.speed * (timeDelta / 1000);

    // Update rotation based on axis
    this.rotation[this.data.axis] += rotationAmount;

    // Apply rotation to entity
    this.el.object3D.rotation[this.data.axis] = this.rotation[this.data.axis];
  }},

  pause: function() {{
    // Stop animation when paused
  }},

  play: function() {{
    // Resume animation when playing
  }}
}});

// Usage:
// <a-box {component_name}="speed: 2; axis: y"></a-box>
// <a-sphere {component_name}="speed: 0.5; axis: x; enabled: false"></a-sphere>
'''

def generate_physics_component(name):
    """Generate physics-based component"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Physics-based component (requires aframe-physics-system)

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    force: {{ type: 'number', default: 10 }},
    direction: {{ type: 'vec3', default: {{ x: 0, y: 1, z: 0 }} }},
    trigger: {{ type: 'string', default: 'click' }}
  }},

  dependencies: ['dynamic-body'], // Requires physics body

  init: function() {{
    const el = this.el;
    const data = this.data;

    // Wait for physics body to be ready
    el.addEventListener('body-loaded', () => {{
      this.body = el.body; // Access Ammo.js physics body
    }});

    // Bind trigger event
    this.applyForce = this.applyForce.bind(this);

    if (data.trigger === 'click') {{
      el.addEventListener('click', this.applyForce);
    }} else if (data.trigger === 'mouseenter') {{
      el.addEventListener('mouseenter', this.applyForce);
    }}
  }},

  applyForce: function(evt) {{
    if (!this.body) return;

    const force = this.data.force;
    const direction = this.data.direction;

    // Apply impulse force
    const impulse = new Ammo.btVector3(
      direction.x * force,
      direction.y * force,
      direction.z * force
    );

    const position = new Ammo.btVector3(0, 0, 0);

    this.body.applyImpulse(impulse, position);

    console.log('Force applied:', force);

    // Clean up Ammo.js objects
    Ammo.destroy(impulse);
    Ammo.destroy(position);
  }},

  tick: function(time, timeDelta) {{
    // Optional: Add continuous forces or check physics state
  }},

  remove: function() {{
    const el = this.el;
    if (this.data.trigger === 'click') {{
      el.removeEventListener('click', this.applyForce);
    }} else if (this.data.trigger === 'mouseenter') {{
      el.removeEventListener('mouseenter', this.applyForce);
    }}
  }}
}});

// Usage (requires aframe-physics-system):
// <a-scene physics>
//   <a-sphere
//     dynamic-body
//     {component_name}="force: 20; direction: 0 1 0; trigger: click"
//     position="0 2 -3">
//   </a-sphere>
// </a-scene>
'''

def generate_controller_component(name):
    """Generate VR controller component"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// VR controller interaction component

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    hand: {{ type: 'string', default: 'right', oneOf: ['left', 'right'] }},
    button: {{ type: 'string', default: 'trigger', oneOf: ['trigger', 'grip', 'thumbstick', 'abutton', 'bbutton'] }}
  }},

  init: function() {{
    const el = this.el;
    const data = this.data;

    console.log(`Initializing controller component for ${{data.hand}} hand`);

    // Bind event handlers
    this.onButtonDown = this.onButtonDown.bind(this);
    this.onButtonUp = this.onButtonUp.bind(this);
    this.onButtonChanged = this.onButtonChanged.bind(this);

    // Listen to button events
    const buttonDownEvent = data.button + 'down';
    const buttonUpEvent = data.button + 'up';
    const buttonChangedEvent = data.button + 'changed';

    el.addEventListener(buttonDownEvent, this.onButtonDown);
    el.addEventListener(buttonUpEvent, this.onButtonUp);
    el.addEventListener(buttonChangedEvent, this.onButtonChanged);

    // Controller-specific events
    el.addEventListener('controllerconnected', (evt) => {{
      console.log('Controller connected:', evt.detail.name);
    }});
  }},

  onButtonDown: function(evt) {{
    console.log(`${{this.data.button}} pressed on ${{this.data.hand}} hand`);

    // Example: Raycast from controller
    const raycaster = this.el.components.raycaster;
    if (raycaster) {{
      const intersections = raycaster.intersections;
      if (intersections.length > 0) {{
        const target = intersections[0].object.el;
        console.log('Hit:', target);

        // Emit event on hit object
        target.emit('controller-hit', {{
          hand: this.data.hand,
          button: this.data.button,
          intersection: intersections[0]
        }});
      }}
    }}
  }},

  onButtonUp: function(evt) {{
    console.log(`${{this.data.button}} released on ${{this.data.hand}} hand`);
  }},

  onButtonChanged: function(evt) {{
    // For analog buttons (triggers, thumbsticks)
    const state = evt.detail.state;
    console.log(`${{this.data.button}} state:`, state);
  }},

  remove: function() {{
    const el = this.el;
    const data = this.data;

    const buttonDownEvent = data.button + 'down';
    const buttonUpEvent = data.button + 'up';
    const buttonChangedEvent = data.button + 'changed';

    el.removeEventListener(buttonDownEvent, this.onButtonDown);
    el.removeEventListener(buttonUpEvent, this.onButtonUp);
    el.removeEventListener(buttonChangedEvent, this.onButtonChanged);
  }}
}});

// Usage:
// <a-entity hand-controls="hand: right"
//           laser-controls
//           {component_name}="hand: right; button: trigger">
// </a-entity>
'''

def generate_networked_component(name):
    """Generate networked component"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Networked component for multi-user synchronization (requires networked-aframe)

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    syncInterval: {{ type: 'number', default: 50 }}, // milliseconds
    owner: {{ type: 'string', default: '' }}
  }},

  init: function() {{
    const el = this.el;

    // Check if this is the local player's entity
    this.isLocal = NAF.utils.isMine(el);

    console.log('Networked component init:', this.isLocal ? 'LOCAL' : 'REMOTE');

    // Last sync time
    this.lastSync = 0;

    // Custom networked data
    this.networkData = {{
      customProperty: 'value'
    }};

    // Listen to networked events
    el.addEventListener('connected', () => {{
      console.log('Entity connected to network');
    }});

    el.addEventListener('disconnected', () => {{
      console.log('Entity disconnected from network');
    }});

    // Listen to ownership changes
    NAF.utils.getNetworkedEntity(el).then(networkedEl => {{
      networkedEl.addEventListener('ownership-gained', () => {{
        console.log('Gained ownership');
        this.isLocal = true;
      }});

      networkedEl.addEventListener('ownership-lost', () => {{
        console.log('Lost ownership');
        this.isLocal = false;
      }});
    }});
  }},

  tick: function(time, timeDelta) {{
    if (!this.isLocal) return;

    // Sync at specified interval
    if (time - this.lastSync >= this.data.syncInterval) {{
      this.syncState();
      this.lastSync = time;
    }}
  }},

  syncState: function() {{
    // Broadcast custom state to other clients
    const el = this.el;

    // Update networked components
    NAF.utils.getNetworkedEntity(el).then(networkedEl => {{
      // Sync custom data
      networkedEl.emit('sync-data', this.networkData);
    }});
  }},

  // Call this to take ownership of the entity
  takeOwnership: function() {{
    NAF.utils.takeOwnership(this.el);
  }},

  remove: function() {{
    console.log('Networked component removed');
  }}
}});

// Usage (requires networked-aframe):
// <a-scene networked-scene="room: myRoom; adapter: wseasyrtc">
//   <a-entity networked="template: #avatar-template"
//             {component_name}="syncInterval: 100">
//   </a-entity>
// </a-scene>
'''

def generate_loader_component(name):
    """Generate asset loading component"""
    component_name = name.replace('_', '-')
    return f'''// {component_name} Component
// Asset loading component with progress and error handling

AFRAME.registerComponent('{component_name}', {{
  schema: {{
    src: {{ type: 'string', default: '' }},
    onLoad: {{ type: 'string', default: '' }}, // Event name to emit
    showProgress: {{ type: 'boolean', default: true }}
  }},

  init: function() {{
    const el = this.el;
    const data = this.data;

    if (!data.src) {{
      console.warn('{component_name}: No src specified');
      return;
    }}

    this.loading = true;
    this.loaded = false;

    // Start loading
    this.loadAsset(data.src);
  }},

  update: function(oldData) {{
    // Reload if src changes
    if (this.data.src !== oldData.src && this.data.src) {{
      this.loadAsset(this.data.src);
    }}
  }},

  loadAsset: function(src) {{
    const el = this.el;
    const data = this.data;

    console.log('Loading asset:', src);

    // Determine asset type from extension
    const extension = src.split('.').pop().toLowerCase();

    if (['gltf', 'glb'].includes(extension)) {{
      this.loadModel(src);
    }} else if (['jpg', 'jpeg', 'png', 'gif'].includes(extension)) {{
      this.loadImage(src);
    }} else {{
      console.warn('Unsupported asset type:', extension);
    }}
  }},

  loadModel: function(src) {{
    const el = this.el;

    // Use A-Frame's asset system
    const loader = new THREE.GLTFLoader();

    loader.load(
      src,
      // onLoad
      (gltf) => {{
        console.log('Model loaded:', src);
        this.onAssetLoaded(gltf);
        el.setObject3D('mesh', gltf.scene);
      }},
      // onProgress
      (xhr) => {{
        const percentComplete = (xhr.loaded / xhr.total * 100);
        if (this.data.showProgress) {{
          console.log(`Loading: ${{percentComplete.toFixed(2)}}%`);
        }}
        el.emit('loading-progress', {{ percent: percentComplete }});
      }},
      // onError
      (error) => {{
        console.error('Error loading model:', error);
        this.onAssetError(error);
      }}
    );
  }},

  loadImage: function(src) {{
    const el = this.el;

    const textureLoader = new THREE.TextureLoader();

    textureLoader.load(
      src,
      // onLoad
      (texture) => {{
        console.log('Image loaded:', src);
        this.onAssetLoaded(texture);
        el.setAttribute('material', 'src', texture);
      }},
      // onProgress
      (xhr) => {{
        const percentComplete = (xhr.loaded / xhr.total * 100);
        if (this.data.showProgress) {{
          console.log(`Loading: ${{percentComplete.toFixed(2)}}%`);
        }}
        el.emit('loading-progress', {{ percent: percentComplete }});
      }},
      // onError
      (error) => {{
        console.error('Error loading image:', error);
        this.onAssetError(error);
      }}
    );
  }},

  onAssetLoaded: function(asset) {{
    this.loading = false;
    this.loaded = true;

    // Emit custom event
    if (this.data.onLoad) {{
      this.el.emit(this.data.onLoad, {{ asset: asset }});
    }}

    // Emit standard event
    this.el.emit('asset-loaded', {{ asset: asset }});
  }},

  onAssetError: function(error) {{
    this.loading = false;
    this.loaded = false;

    this.el.emit('asset-error', {{ error: error }});
  }}
}});

// Usage:
// <a-entity {component_name}="src: model.gltf; onLoad: model-ready; showProgress: true"></a-entity>
// <a-entity {component_name}="src: texture.jpg"></a-entity>
'''

def generate_component(component_type, name):
    """Generate component based on type"""
    generators = {
        'basic': generate_basic_component,
        'interactive': generate_interactive_component,
        'animation': generate_animation_component,
        'physics': generate_physics_component,
        'controller': generate_controller_component,
        'networked': generate_networked_component,
        'loader': generate_loader_component
    }

    return generators[component_type](name)

def interactive_mode():
    """Interactive component builder"""
    print("\n=== A-Frame Component Builder (Interactive Mode) ===\n")

    print("Available component types:")
    for i, (comp_type, config) in enumerate(COMPONENT_TEMPLATES.items(), 1):
        print(f"  {i}. {comp_type:12} - {config['description']}")

    while True:
        try:
            choice = input("\nSelect component type (1-7): ").strip()
            component_type = list(COMPONENT_TEMPLATES.keys())[int(choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a number between 1 and 7.")

    name = input("Enter component name (e.g., my-component): ").strip()
    if not name:
        print("Error: Component name is required")
        return

    output_file = input("Enter output filename (default: component.js): ").strip() or "component.js"

    save_component(component_type, name, output_file)

def save_component(component_type, name, output_file):
    """Save generated component to file"""
    component_code = generate_component(component_type, name)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(component_code)

    print(f"\n✅ Generated {component_type} component: {output_path}")
    print(f"📝 Component name: {name.replace('_', '-')}")
    print(f"🎯 Template: {COMPONENT_TEMPLATES[component_type]['description']}")
    print(f"\n🚀 To use:")
    print(f"   1. Include in HTML: <script src=\"{output_file}\"></script>")
    print(f"   2. Attach to entity: <a-entity {name.replace('_', '-')}></a-entity>")

def main():
    parser = argparse.ArgumentParser(
        description='Generate A-Frame custom component boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python component_builder.py basic my-component
  python component_builder.py interactive clickable-box --output components/
  python component_builder.py animation rotating-object
  python component_builder.py --interactive

Component Types:
  basic       - Basic component with schema
  interactive - Mouse/VR interaction events
  animation   - Continuous animation with tick()
  physics     - Physics-based interactions
  controller  - VR controller component
  networked   - Multi-user synchronization
  loader      - Asset loading with progress
        '''
    )

    parser.add_argument(
        'component_type',
        nargs='?',
        choices=list(COMPONENT_TEMPLATES.keys()),
        help='Type of component to generate'
    )

    parser.add_argument(
        'name',
        nargs='?',
        help='Name of the component (e.g., my-component)'
    )

    parser.add_argument(
        '-o', '--output',
        default='component.js',
        help='Output filename (default: component.js)'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available component types'
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Component Types:\n")
        for comp_type, config in COMPONENT_TEMPLATES.items():
            print(f"  {comp_type:12} - {config['description']}")
            print(f"                 Schema props: {', '.join(config['schema_props'])}")
            print(f"                 Has tick(): {'Yes' if config['has_tick'] else 'No'}\n")
        sys.exit(0)

    if args.interactive or not args.component_type or not args.name:
        interactive_mode()
    else:
        save_component(args.component_type, args.name, args.output)

if __name__ == '__main__':
    main()
