#!/usr/bin/env python3
"""
Spline Component Wrapper Generator

Generates reusable Spline component wrappers with event handling.

Usage:
    ./component_builder.py                        # Interactive mode
    ./component_builder.py --name ProductViewer   # CLI mode
"""

import argparse
import sys
from pathlib import Path


COMPONENT_TEMPLATES = {
    'basic': '''import Spline from '@splinetool/react-spline';

export default function {name}({{ sceneUrl }}) {{
  return (
    <div style={{{{ width: '100%', height: '600px' }}}}>
      <Spline scene={{sceneUrl}} />
    </div>
  );
}}
''',

    'interactive': '''import {{ useRef, useState }} from 'react';
import Spline from '@splinetool/react-spline';

export default function {name}({{ sceneUrl, onObjectClick }}) {{
  const splineApp = useRef();
  const [isLoaded, setIsLoaded] = useState(false);

  function onLoad(spline) {{
    splineApp.current = spline;
    setIsLoaded(true);
  }}

  function onSplineMouseDown(e) {{
    console.log('Clicked:', e.target.name);
    if (onObjectClick) {{
      onObjectClick(e.target);
    }}
  }}

  return (
    <Spline
      scene={{sceneUrl}}
      onLoad={{onLoad}}
      onSplineMouseDown={{onSplineMouseDown}}
    />
  );
}}
''',

    'animated': '''import {{ useRef }} from 'react';
import Spline from '@splinetool/react-spline';

export default function {name}({{ sceneUrl, animationTrigger }}) {{
  const splineApp = useRef();

  function onLoad(spline) {{
    splineApp.current = spline;
  }}

  // Expose animation controls
  const triggerAnimation = (objectName, eventType = 'mouseHover') => {{
    if (splineApp.current) {{
      splineApp.current.emitEvent(eventType, objectName);
    }}
  }};

  const reverseAnimation = (objectName, eventType = 'mouseHover') => {{
    if (splineApp.current) {{
      splineApp.current.emitEventReverse(eventType, objectName);
    }}
  }};

  return (
    <Spline
      scene={{sceneUrl}}
      onLoad={{onLoad}}
    />
  );
}}
''',

    'controlled': '''import {{ useRef, useImperativeHandle, forwardRef }} from 'react';
import Spline from '@splinetool/react-spline';

const {name} = forwardRef(({{ sceneUrl }}, ref) => {{
  const splineApp = useRef();

  function onLoad(spline) {{
    splineApp.current = spline;
  }}

  // Expose methods to parent component
  useImperativeHandle(ref, () => ({{
    findObject: (name) => {{
      return splineApp.current?.findObjectByName(name);
    }},
    emitEvent: (eventName, objectName) => {{
      splineApp.current?.emitEvent(eventName, objectName);
    }},
    setZoom: (zoom) => {{
      splineApp.current?.setZoom(zoom);
    }},
    getApp: () => splineApp.current
  }}));

  return (
    <Spline
      scene={{sceneUrl}}
      onLoad={{onLoad}}
    />
  );
}});

export default {name};
''',

    'responsive': '''import {{ useRef, useEffect, useState }} from 'react';
import Spline from '@splinetool/react-spline';

export default function {name}({{ mobileSceneUrl, desktopSceneUrl }}) {{
  const splineApp = useRef();
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {{
    const checkMobile = () => {{
      setIsMobile(window.innerWidth < 768);
    }};

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }}, []);

  function onLoad(spline) {{
    splineApp.current = spline;

    // Adjust for mobile
    if (isMobile) {{
      spline.setZoom(0.7);
    }}
  }}

  const sceneUrl = isMobile ? mobileSceneUrl : desktopSceneUrl;

  return (
    <div style={{{{
      width: '100%',
      height: isMobile ? '400px' : '600px'
    }}}}>
      <Spline
        scene={{sceneUrl}}
        onLoad={{onLoad}}
      />
    </div>
  );
}}
''',

    'lazy': '''import React, {{ Suspense }} from 'react';

const Spline = React.lazy(() => import('@splinetool/react-spline'));

export default function {name}({{ sceneUrl, fallback }}) {{
  return (
    <Suspense fallback={{fallback || <div>Loading 3D scene...</div>}}>
      <div style={{{{ width: '100%', height: '600px' }}}}>
        <Spline scene={{sceneUrl}} />
      </div>
    </Suspense>
  );
}}
'''
}


def generate_component(name, component_type, output_path=None):
    """Generate component code"""

    if component_type not in COMPONENT_TEMPLATES:
        print(f"❌ Unknown component type: {component_type}")
        print(f"Available types: {', '.join(COMPONENT_TEMPLATES.keys())}")
        sys.exit(1)

    template = COMPONENT_TEMPLATES[component_type]
    code = template.format(name=name)

    # Output to file or stdout
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(code)
        print(f"✅ Component created: {output_file}")
    else:
        print("\n" + "=" * 60)
        print(f"// {name}.jsx")
        print("=" * 60)
        print(code)
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Spline component wrappers'
    )
    parser.add_argument(
        '--name',
        type=str,
        help='Component name (e.g., ProductViewer)'
    )
    parser.add_argument(
        '--type',
        type=str,
        choices=list(COMPONENT_TEMPLATES.keys()),
        help='Component type'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: print to stdout)'
    )

    args = parser.parse_args()

    # Interactive mode
    if not args.name or not args.type:
        print("🎨 Spline Component Builder\n")

        if not args.name:
            name = input("Component name (e.g., ProductViewer): ").strip()
            if not name:
                print("❌ Component name is required")
                sys.exit(1)
        else:
            name = args.name

        if not args.type:
            print("\nComponent types:")
            for i, comp_type in enumerate(COMPONENT_TEMPLATES.keys(), 1):
                print(f"  {i}. {comp_type}")

            choice = input("\nSelect type (1-6): ").strip()
            try:
                comp_type = list(COMPONENT_TEMPLATES.keys())[int(choice) - 1]
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                sys.exit(1)
        else:
            comp_type = args.type

        output_path = args.output
    else:
        name = args.name
        comp_type = args.type
        output_path = args.output

    # Generate component
    generate_component(name, comp_type, output_path)


if __name__ == '__main__':
    main()
