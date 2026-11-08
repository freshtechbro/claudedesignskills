# Barba.js Assets

This directory contains information about assets and starter templates for Barba.js projects.

## Starter Templates

Complete Barba.js starter templates are generated automatically by the `project_setup.py` script.

### Usage

Run the project setup script to generate a complete Barba.js project:

```bash
../scripts/project_setup.py
```

Or in CLI mode:

```bash
../scripts/project_setup.py --name my-project --transition fade
```

### Generated Project Structure

The script creates a complete project with:

```
my-project/
├── index.html              # Home page with Barba structure
├── about.html              # Example about page
├── contact.html            # Example contact page
├── src/
│   ├── main.js            # Barba.js initialization with transitions
│   └── style.css          # Complete styling with transition support
├── package.json            # Dependencies (@barba/core, gsap, vite)
├── vite.config.js          # Vite configuration for multi-page app
└── README.md               # Project-specific documentation
```

### Available Transition Types

The generated project includes one of these transitions:

1. **fade** - Simple fade in/out
2. **slide** - Horizontal slide transition
3. **scale** - Zoom with fade effect
4. **stagger** - Staggered element animations
5. **curtain** - Curtain overlay effect

### Features

Generated projects include:

- Complete HTML structure with proper `data-barba` attributes
- Responsive navigation that persists across page transitions
- GSAP-powered animations
- Loading indicator
- Transition curtain element
- Mobile-responsive styling
- Vite dev server and build setup
- Example pages demonstrating namespace-based routing

### Customization

After generating a project:

1. Modify transitions in `src/main.js`
2. Add custom styles in `src/style.css`
3. Create additional pages following the same structure
4. Update `vite.config.js` to include new pages in build

### Example HTML Structure

All generated pages follow this structure:

```html
<body data-barba="wrapper">
  <!-- Persistent header (outside container) -->
  <header class="site-header">
    <nav><!-- Navigation links --></nav>
  </header>

  <!-- Dynamic content (inside container) -->
  <main data-barba="container" data-barba-namespace="page-name">
    <!-- Page content that transitions -->
  </main>

  <!-- Persistent footer (outside container) -->
  <footer class="site-footer"><!-- Footer content --></footer>

  <!-- Transition elements -->
  <div class="page-loader">Loading...</div>
  <div class="transition-curtain"></div>

  <script type="module" src="/src/main.js"></script>
</body>
```

### Development Workflow

1. Generate project: `../scripts/project_setup.py --name my-site`
2. Navigate to project: `cd my-site`
3. Install dependencies: `npm install` (auto-run unless `--no-install`)
4. Start dev server: `npm run dev`
5. Open browser: `http://localhost:5173`
6. Build for production: `npm run build`

### Additional Examples

For custom transition code snippets, use the transition generator:

```bash
../scripts/transition_generator.py
```

This generates just the JavaScript transition code that you can copy into your project.

## Manual Setup (Without Scripts)

If you prefer to set up manually:

### 1. Install Dependencies

```bash
npm install --save-dev @barba/core gsap
```

### 2. Create HTML Structure

Add Barba attributes to your HTML:

```html
<body data-barba="wrapper">
  <main data-barba="container" data-barba-namespace="home">
    <!-- Your content -->
  </main>
</body>
```

### 3. Initialize Barba

Create JavaScript file:

```javascript
import barba from '@barba/core';
import gsap from 'gsap';

barba.init({
  transitions: [{
    name: 'fade',
    async leave({ current }) {
      await gsap.to(current.container, { opacity: 0 });
    },
    async enter({ next }) {
      await gsap.from(next.container, { opacity: 0 });
    }
  }]
});
```

### 4. Add to HTML

```html
<script type="module" src="/path/to/your/script.js"></script>
```

## Resources

- **SKILL.md** - Complete Barba.js guide with patterns and examples
- **references/api_reference.md** - Full API documentation
- **references/hooks_guide.md** - Lifecycle hooks reference
- **references/gsap_integration.md** - GSAP animation patterns
- **references/transition_patterns.md** - Ready-to-use transition code
- **scripts/transition_generator.py** - Generate custom transition code
- **scripts/project_setup.py** - Generate complete starter projects
