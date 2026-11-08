# Spline Interactive - Assets

This directory contains starter templates and examples for Spline + React integration.

## Using the Project Generator

The easiest way to get started is using the `project_generator.py` script:

```bash
# Interactive mode
./scripts/project_generator.py

# CLI mode
./scripts/project_generator.py --name my-spline-app

# Next.js project
./scripts/project_generator.py --name my-spline-app --nextjs
```

This automatically generates a complete project with:
- package.json with all dependencies
- Vite or Next.js configuration
- React components with Spline integration
- Example event handlers
- Starter CSS
- README with setup instructions

## Project Structure

Generated projects have this structure:

```
my-spline-app/
├── package.json
├── vite.config.js (or next.config.js)
├── index.html (Vite only)
├── README.md
├── src/
│   ├── main.jsx (Vite only)
│   ├── App.jsx
│   └── App.css
└── app/ (Next.js only)
    └── page.jsx
```

## Component Templates

Use `component_builder.py` to generate reusable Spline components:

```bash
# Interactive mode
./scripts/component_builder.py

# Generate specific component
./scripts/component_builder.py --name ProductViewer --type interactive

# Save to file
./scripts/component_builder.py --name ProductViewer --type interactive --output src/components/ProductViewer.jsx
```

### Available Component Types

1. **basic** - Simple Spline scene wrapper
2. **interactive** - With click/hover event handling
3. **animated** - With animation trigger methods
4. **controlled** - Exposes methods via ref for parent control
5. **responsive** - Adapts to mobile/desktop screen sizes
6. **lazy** - Lazy-loaded with React.lazy()

## Example Integrations

### With GSAP ScrollTrigger

```jsx
import { useRef, useEffect } from 'react';
import Spline from '@splinetool/react-spline';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function ScrollSpline() {
  const splineApp = useRef();

  function onLoad(app) {
    splineApp.current = app;

    ScrollTrigger.create({
      trigger: '.scene',
      start: 'top center',
      onEnter: () => app.emitEvent('mouseHover', 'Product')
    });
  }

  return (
    <div className="scene">
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
      />
    </div>
  );
}
```

### With Framer Motion

```jsx
import { motion } from 'framer-motion';
import Spline from '@splinetool/react-spline';

export default function AnimatedSpline() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8 }}
      style={{ width: '100%', height: '600px' }}
    >
      <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
    </motion.div>
  );
}
```

### Product Configurator

```jsx
import { useRef, useState } from 'react';
import Spline from '@splinetool/react-spline';

export default function ProductConfigurator() {
  const product = useRef();
  const splineApp = useRef();
  const [color, setColor] = useState('#ff6b6b');

  function onLoad(spline) {
    splineApp.current = spline;
    product.current = spline.findObjectByName('Product');
  }

  function changeColor(newColor) {
    setColor(newColor);
    if (product.current) {
      product.current.material.color.set(parseInt(newColor.substring(1), 16));
    }
  }

  function rotate() {
    if (product.current) {
      product.current.rotation.y += Math.PI / 4;
    }
  }

  return (
    <div>
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={onLoad}
      />

      <div className="controls">
        <button onClick={() => changeColor('#ff6b6b')}>Red</button>
        <button onClick={() => changeColor('#4ecdc4')}>Cyan</button>
        <button onClick={() => changeColor('#ffe66d')}>Yellow</button>
        <button onClick={rotate}>Rotate</button>
      </div>
    </div>
  );
}
```

### Multi-Scene Viewer

```jsx
import { useState } from 'react';
import Spline from '@splinetool/react-spline';

const scenes = {
  scene1: 'https://prod.spline.design/SCENE-1/scene.splinecode',
  scene2: 'https://prod.spline.design/SCENE-2/scene.splinecode',
  scene3: 'https://prod.spline.design/SCENE-3/scene.splinecode'
};

export default function SceneSwitcher() {
  const [currentScene, setCurrentScene] = useState('scene1');

  return (
    <div>
      <Spline scene={scenes[currentScene]} />

      <div className="tabs">
        <button onClick={() => setCurrentScene('scene1')}>Scene 1</button>
        <button onClick={() => setCurrentScene('scene2')}>Scene 2</button>
        <button onClick={() => setCurrentScene('scene3')}>Scene 3</button>
      </div>
    </div>
  );
}
```

## Getting Your Spline Scene URL

1. Open your scene in Spline editor (https://app.spline.design)
2. Click the "Export" button (top right)
3. Select "Code Export" → "React"
4. Copy the scene URL (format: `https://prod.spline.design/[ID]/scene.splinecode`)
5. Replace `YOUR-SCENE-ID` in the templates with your actual scene URL

## Common Use Cases

### Marketing Hero Section

```jsx
import Spline from '@splinetool/react-spline';
import './Hero.css';

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>Welcome to Our Product</h1>
        <p>Experience 3D interaction</p>
        <button>Get Started</button>
      </div>

      <div className="hero-scene">
        <Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
      </div>
    </section>
  );
}
```

### Interactive Portfolio

```jsx
import { useRef } from 'react';
import Spline from '@splinetool/react-spline';

export default function Portfolio() {
  const splineApp = useRef();

  function showProject(projectName) {
    splineApp.current?.emitEvent('mouseHover', projectName);
  }

  return (
    <div className="portfolio">
      <nav>
        <button onClick={() => showProject('Project1')}>Project 1</button>
        <button onClick={() => showProject('Project2')}>Project 2</button>
        <button onClick={() => showProject('Project3')}>Project 3</button>
      </nav>

      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        onLoad={(app) => (splineApp.current = app)}
      />
    </div>
  );
}
```

## Performance Tips

1. **Use On-Demand Rendering** (enabled by default):
   ```jsx
   <Spline scene={sceneUrl} renderOnDemand={true} />
   ```

2. **Lazy Load Heavy Scenes**:
   ```jsx
   const Spline = React.lazy(() => import('@splinetool/react-spline'));
   ```

3. **Optimize in Spline Editor**:
   - Reduce polygon count
   - Compress textures
   - Limit lights to 2-3
   - Use simple materials

4. **Create Mobile Versions**:
   - Lower detail meshes
   - Smaller textures (512x512)
   - No shadows/reflections

## Troubleshooting

### Scene Not Loading
- Verify scene URL is complete and correct
- Check scene is published in Spline editor
- Look for CORS errors in browser console
- Ensure both `@splinetool/react-spline` and `@splinetool/runtime` are installed

### Events Not Working
- Use `onSplineMouseDown` not `onMouseDown`
- Verify objects have events configured in Spline editor
- Check object names match exactly (case-sensitive)

### Performance Issues
- Enable renderOnDemand
- Create mobile-specific scenes with lower detail
- Use lazy loading for heavy scenes
- Profile with Chrome DevTools

## Additional Resources

- [Spline Documentation](https://docs.spline.design)
- [React Spline GitHub](https://github.com/splinetool/react-spline)
- [Spline Community](https://spline.community)
- [Spline Tutorials](https://spline.design/tutorials)
