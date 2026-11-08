#!/usr/bin/env python3
"""
Spline + React Project Generator

Generates boilerplate React projects with Spline integration.

Usage:
    ./project_generator.py                    # Interactive mode
    ./project_generator.py --name my-project  # CLI mode
"""

import argparse
import json
import os
import sys
from pathlib import Path


def create_project_structure(project_name, include_nextjs=False):
    """Create complete project structure with all necessary files"""

    base_path = Path(project_name)

    # Create directories
    directories = [
        base_path,
        base_path / 'src',
        base_path / 'public',
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": project_name,
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@splinetool/react-spline": "^2.2.6",
            "@splinetool/runtime": "^0.9.508"
        },
        "devDependencies": {
            "@vitejs/plugin-react": "^4.0.0",
            "vite": "^4.3.9"
        },
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        }
    }

    if include_nextjs:
        package_json["dependencies"]["next"] = "^14.0.0"
        package_json["scripts"] = {
            "dev": "next dev",
            "build": "next build",
            "start": "next start"
        }

    with open(base_path / 'package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # vite.config.js (if not Next.js)
    if not include_nextjs:
        vite_config = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
});
"""
        with open(base_path / 'vite.config.js', 'w') as f:
            f.write(vite_config)

    # index.html (if not Next.js)
    if not include_nextjs:
        index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Spline React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        with open(base_path / 'index.html', 'w') as f:
            f.write(index_html)

    # src/main.jsx (if not Next.js)
    if not include_nextjs:
        main_jsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
        with open(base_path / 'src' / 'main.jsx', 'w') as f:
            f.write(main_jsx)

    # src/App.jsx or app/page.jsx
    if include_nextjs:
        app_dir = base_path / 'app'
        app_dir.mkdir(exist_ok=True)

        page_jsx = """'use client';

import Spline from '@splinetool/react-spline/next';
import { useRef } from 'react';

export default function Home() {
  const splineApp = useRef();

  function onLoad(spline) {
    splineApp.current = spline;
    console.log('Spline scene loaded');
  }

  function onSplineMouseDown(e) {
    console.log('Clicked:', e.target.name);
  }

  return (
    <main style={{ width: '100vw', height: '100vh' }}>
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
        onSplineMouseDown={onSplineMouseDown}
      />
    </main>
  );
}
"""
        with open(app_dir / 'page.jsx', 'w') as f:
            f.write(page_jsx)
    else:
        app_jsx = """import { useRef, useState } from 'react';
import Spline from '@splinetool/react-spline';

export default function App() {
  const splineApp = useRef();
  const [isLoaded, setIsLoaded] = useState(false);

  function onLoad(spline) {
    splineApp.current = spline;
    setIsLoaded(true);
    console.log('Spline scene loaded');
  }

  function onSplineMouseDown(e) {
    console.log('Clicked:', e.target.name);

    if (e.target.name === 'Button') {
      splineApp.current.emitEvent('mouseHover', 'Card');
    }
  }

  return (
    <div className="app">
      <div className="scene-container">
        <Spline
          scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
          onLoad={onLoad}
          onSplineMouseDown={onSplineMouseDown}
        />
      </div>

      {isLoaded && (
        <div className="controls">
          <button onClick={() => splineApp.current.setZoom(1.5)}>
            Zoom In
          </button>
          <button onClick={() => splineApp.current.setZoom(0.7)}>
            Zoom Out
          </button>
        </div>
      )}
    </div>
  );
}
"""
        with open(base_path / 'src' / 'App.jsx', 'w') as f:
            f.write(app_jsx)

    # CSS
    if not include_nextjs:
        app_css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.scene-container {
  width: 100%;
  height: 100%;
}

.controls {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 10px;
  z-index: 10;
}

button {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

button:hover {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

button:active {
  transform: scale(0.98);
}
"""
        with open(base_path / 'src' / 'App.css', 'w') as f:
            f.write(app_css)

    # README.md
    readme = f"""# {project_name}

Spline + React project

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Visit http://localhost:3000

## Update Scene URL

Replace `YOUR-SCENE-ID` in the code with your actual Spline scene ID.

Get your scene URL from Spline:
1. Open your scene in Spline editor
2. Click "Export" button
3. Select "Code Export" > "React"
4. Copy the scene URL

## Build

```bash
npm run build
```

## Learn More

- [Spline Documentation](https://docs.spline.design)
- [React Spline GitHub](https://github.com/splinetool/react-spline)
"""
    with open(base_path / 'README.md', 'w') as f:
        f.write(readme)

    print(f"\n✅ Project '{project_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  npm install")
    print(f"  npm run dev")
    print(f"\n📝 Don't forget to update the Spline scene URL!")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Spline + React project boilerplate'
    )
    parser.add_argument(
        '--name',
        type=str,
        help='Project name'
    )
    parser.add_argument(
        '--nextjs',
        action='store_true',
        help='Use Next.js instead of Vite'
    )

    args = parser.parse_args()

    # Interactive mode
    if not args.name:
        print("🚀 Spline + React Project Generator\n")
        project_name = input("Project name: ").strip()

        if not project_name:
            print("❌ Project name is required")
            sys.exit(1)

        use_nextjs = input("Use Next.js? (y/N): ").strip().lower() == 'y'
    else:
        project_name = args.name
        use_nextjs = args.nextjs

    # Create project
    create_project_structure(project_name, use_nextjs)


if __name__ == '__main__':
    main()
