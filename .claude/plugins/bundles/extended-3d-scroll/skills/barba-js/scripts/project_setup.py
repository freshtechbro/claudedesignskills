#!/usr/bin/env python3
"""
Barba.js Project Setup Script

Initializes a new Barba.js project with boilerplate HTML, CSS, and JavaScript files.

Usage:
    ./project_setup.py                       # Interactive mode
    ./project_setup.py --name my-project     # Create project in ./my-project
    ./project_setup.py --name my-project --transition fade
    ./project_setup.py --name my-project --minimal  # Minimal setup without examples

Options:
    --name NAME           Project directory name (required in CLI mode)
    --transition TYPE     Transition type (fade, slide, scale, stagger, curtain)
    --minimal             Create minimal setup without example pages
    --no-install          Skip npm install step
    --output-dir DIR      Parent directory for project (default: current directory)
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def create_package_json(project_name: str) -> str:
    """Generate package.json content."""
    return f'''{{
  "name": "{project_name}",
  "version": "1.0.0",
  "description": "Barba.js page transition project",
  "main": "src/main.js",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "keywords": ["barba", "page-transitions", "gsap"],
  "author": "",
  "license": "MIT",
  "devDependencies": {{
    "@barba/core": "^2.9.7",
    "gsap": "^3.12.5",
    "vite": "^5.0.0"
  }}
}}
'''


def create_index_html(minimal: bool = False) -> str:
    """Generate index.html content."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Home - Barba.js Project</title>
  <meta name="description" content="Home page with Barba.js transitions">
  <link rel="stylesheet" href="/src/style.css">
</head>
<body data-barba="wrapper">
  <header class="site-header">
    <nav>
      <a href="/" class="logo">Barba.js</a>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main data-barba="container" data-barba-namespace="home">
    <div class="hero">
      <h1 class="stagger-item">Welcome to Barba.js</h1>
      <p class="stagger-item">Smooth page transitions without full page reloads</p>
      <a href="/about.html" class="btn stagger-item">Learn More</a>
    </div>

    <section class="features">
      <div class="feature stagger-item">
        <h2>Fast</h2>
        <p>No page reloads, instant transitions</p>
      </div>
      <div class="feature stagger-item">
        <h2>Smooth</h2>
        <p>Beautiful GSAP-powered animations</p>
      </div>
      <div class="feature stagger-item">
        <h2>Easy</h2>
        <p>Simple API, powerful results</p>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>&copy; 2025 Barba.js Project</p>
  </footer>

  <div class="page-loader">Loading...</div>
  <div class="transition-curtain"></div>

  <script type="module" src="/src/main.js"></script>
</body>
</html>
'''


def create_about_html() -> str:
    """Generate about.html content."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About - Barba.js Project</title>
  <meta name="description" content="About page with Barba.js transitions">
  <link rel="stylesheet" href="/src/style.css">
</head>
<body data-barba="wrapper">
  <header class="site-header">
    <nav>
      <a href="/" class="logo">Barba.js</a>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main data-barba="container" data-barba-namespace="about">
    <div class="content-page">
      <h1 class="stagger-item">About Barba.js</h1>
      <p class="stagger-item">Barba.js is a small (7kb minified and compressed) library that helps you create fluid and smooth transitions between your website's pages.</p>
      <p class="stagger-item">It helps reduce the delay between your pages, minimize browser HTTP requests and enhance your user's web experience.</p>
      <a href="/contact.html" class="btn stagger-item">Get in Touch</a>
    </div>
  </main>

  <footer class="site-footer">
    <p>&copy; 2025 Barba.js Project</p>
  </footer>

  <div class="page-loader">Loading...</div>
  <div class="transition-curtain"></div>

  <script type="module" src="/src/main.js"></script>
</body>
</html>
'''


def create_contact_html() -> str:
    """Generate contact.html content."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contact - Barba.js Project</title>
  <meta name="description" content="Contact page with Barba.js transitions">
  <link rel="stylesheet" href="/src/style.css">
</head>
<body data-barba="wrapper">
  <header class="site-header">
    <nav>
      <a href="/" class="logo">Barba.js</a>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main data-barba="container" data-barba-namespace="contact">
    <div class="content-page">
      <h1 class="stagger-item">Contact Us</h1>
      <p class="stagger-item">Get in touch to learn more about Barba.js.</p>
      <form class="contact-form stagger-item">
        <input type="text" placeholder="Name" required>
        <input type="email" placeholder="Email" required>
        <textarea placeholder="Message" rows="5" required></textarea>
        <button type="submit" class="btn">Send Message</button>
      </form>
    </div>
  </main>

  <footer class="site-footer">
    <p>&copy; 2025 Barba.js Project</p>
  </footer>

  <div class="page-loader">Loading...</div>
  <div class="transition-curtain"></div>

  <script type="module" src="/src/main.js"></script>
</body>
</html>
'''


def create_css() -> str:
    """Generate style.css content."""
    return '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  line-height: 1.6;
  color: #333;
}

/* Header */
.site-header {
  background: #667eea;
  color: white;
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.site-header nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.site-header .logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.site-header ul {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.site-header a {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.site-header a:hover {
  opacity: 0.8;
}

/* Container */
[data-barba="container"] {
  min-height: calc(100vh - 60px - 80px);
}

/* Hero */
.hero {
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

/* Features */
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature {
  padding: 2rem;
  background: #f5f5f5;
  border-radius: 8px;
  text-align: center;
}

.feature h2 {
  margin-bottom: 1rem;
  color: #667eea;
}

/* Content Page */
.content-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.content-page h1 {
  margin-bottom: 2rem;
  color: #667eea;
}

.content-page p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

/* Contact Form */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.contact-form input,
.contact-form textarea {
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.contact-form input:focus,
.contact-form textarea:focus {
  outline: none;
  border-color: #667eea;
}

/* Button */
.btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #5568d3;
}

/* Footer */
.site-footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 2rem;
}

/* Page Loader */
.page-loader {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  color: #667eea;
  opacity: 0;
  z-index: 9998;
  pointer-events: none;
}

/* Transition Curtain */
.transition-curtain {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 9999;
  pointer-events: none;
  transform: translateY(-100%);
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .site-header ul {
    gap: 1rem;
  }
}
'''


def create_main_js(transition_type: str = 'fade') -> str:
    """Generate main.js content with specified transition."""
    transitions_code = {
        'fade': '''    {
      name: 'fade',
      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          duration: 0.5,
          ease: 'power2.inOut'
        });
      },
      async enter({ next }) {
        gsap.set(next.container, { opacity: 0 });
        await gsap.to(next.container, {
          opacity: 1,
          duration: 0.5,
          ease: 'power2.inOut'
        });
      }
    }''',

        'slide': '''    {
      name: 'slide',
      sync: true,
      leave({ current }) {
        return gsap.to(current.container, {
          x: '-100%',
          duration: 0.7,
          ease: 'power3.inOut'
        });
      },
      enter({ next }) {
        gsap.set(next.container, { x: '100%' });
        return gsap.to(next.container, {
          x: '0%',
          duration: 0.7,
          ease: 'power3.inOut'
        });
      }
    }''',

        'scale': '''    {
      name: 'scale-fade',
      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          scale: 0.95,
          duration: 0.5,
          ease: 'power2.in'
        });
      },
      async enter({ next }) {
        await gsap.fromTo(next.container,
          { opacity: 0, scale: 1.05 },
          { opacity: 1, scale: 1, duration: 0.6, ease: 'power2.out' }
        );
      }
    }''',

        'stagger': '''    {
      name: 'stagger',
      async leave({ current }) {
        const tl = gsap.timeline();
        tl.to(current.container.querySelectorAll('.stagger-item'), {
          y: -50,
          opacity: 0,
          duration: 0.5,
          stagger: 0.05,
          ease: 'power2.in'
        })
        .to(current.container, {
          opacity: 0,
          duration: 0.3
        }, '-=0.2');
        await tl.play();
      },
      async enter({ next }) {
        const tl = gsap.timeline();
        gsap.set(next.container.querySelectorAll('.stagger-item'), {
          y: 50,
          opacity: 0
        });
        tl.to(next.container.querySelectorAll('.stagger-item'), {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.05,
          ease: 'power2.out'
        });
        await tl.play();
      }
    }''',

        'curtain': '''    {
      name: 'curtain',
      async leave({ current }) {
        const curtain = document.querySelector('.transition-curtain');
        await gsap.fromTo(curtain,
          { yPercent: -100 },
          { yPercent: 0, duration: 0.6, ease: 'power2.inOut' }
        );
      },
      async enter({ next }) {
        const curtain = document.querySelector('.transition-curtain');
        await gsap.to(curtain, {
          yPercent: 100,
          duration: 0.6,
          ease: 'power2.inOut'
        });
      }
    }'''
    }

    transition_code = transitions_code.get(transition_type, transitions_code['fade'])

    return f'''import barba from '@barba/core';
import gsap from 'gsap';

// Initialize Barba.js
barba.init({{
  transitions: [
{transition_code}
  ]
}});

// Global hooks
barba.hooks.beforeEnter(() => {{
  // Reset scroll position
  window.scrollTo(0, 0);
}});

barba.hooks.before(() => {{
  // Show loader
  gsap.to('.page-loader', {{ opacity: 1, duration: 0.3 }});
}});

barba.hooks.after(() => {{
  // Hide loader
  gsap.to('.page-loader', {{ opacity: 0, duration: 0.3 }});
}});

// Contact form handler (demo)
document.addEventListener('submit', (e) => {{
  if (e.target.classList.contains('contact-form')) {{
    e.preventDefault();
    alert('Form submission would happen here!');
  }}
}});
'''


def create_vite_config() -> str:
    """Generate vite.config.js content."""
    return '''import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        about: 'about.html',
        contact: 'contact.html'
      }
    }
  }
});
'''


def create_readme(project_name: str) -> str:
    """Generate README.md content."""
    return f'''# {project_name}

Barba.js page transition project with GSAP animations.

## Setup

Install dependencies:

```bash
npm install
```

## Development

Start development server:

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## Build

Build for production:

```bash
npm run build
```

Output will be in `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
{project_name}/
├── index.html              # Home page
├── about.html              # About page
├── contact.html            # Contact page
├── src/
│   ├── main.js            # Barba.js initialization
│   └── style.css          # Global styles
├── package.json
├── vite.config.js
└── README.md
```

## Customization

### Change Transition

Edit `src/main.js` and modify the transition in `barba.init()`.

See available transition types in the Barba.js documentation.

### Add More Pages

1. Create new HTML file (e.g., `services.html`)
2. Add `data-barba="container"` to main content
3. Add `data-barba-namespace="services"` to identify the page
4. Add link to navigation
5. Update `vite.config.js` to include the new page in build

## Resources

- [Barba.js Documentation](https://barba.js.org)
- [GSAP Documentation](https://greensock.com/docs/)
- [Vite Documentation](https://vitejs.dev)
'''


def create_project(
    name: str,
    output_dir: str = '.',
    transition: str = 'fade',
    minimal: bool = False,
    no_install: bool = False
) -> None:
    """Create Barba.js project structure."""
    project_path = Path(output_dir) / name

    # Check if directory exists
    if project_path.exists():
        print(f"❌ Error: Directory '{project_path}' already exists")
        sys.exit(1)

    print(f"🎬 Creating Barba.js project: {name}")
    print(f"📁 Location: {project_path}")
    print()

    # Create directories
    project_path.mkdir(parents=True)
    (project_path / 'src').mkdir()

    print("✅ Created project directory")

    # Create files
    files = {
        'package.json': create_package_json(name),
        'index.html': create_index_html(minimal),
        'src/style.css': create_css(),
        'src/main.js': create_main_js(transition),
        'vite.config.js': create_vite_config(),
        'README.md': create_readme(name)
    }

    if not minimal:
        files['about.html'] = create_about_html()
        files['contact.html'] = create_contact_html()

    for file_path, content in files.items():
        full_path = project_path / file_path
        full_path.write_text(content)
        print(f"✅ Created {file_path}")

    print()
    print("=" * 50)
    print("✅ Project created successfully!")
    print()
    print("Next steps:")
    print(f"  1. cd {name}")

    if not no_install:
        print("  2. Running npm install...")
        print()
        try:
            subprocess.run(['npm', 'install'], cwd=project_path, check=True)
            print()
            print("✅ Dependencies installed!")
            print()
            print("To start development:")
            print(f"  cd {name}")
            print("  npm run dev")
        except subprocess.CalledProcessError:
            print("❌ npm install failed. Run manually:")
            print(f"  cd {name}")
            print("  npm install")
            print("  npm run dev")
        except FileNotFoundError:
            print("⚠️  npm not found. Install dependencies manually:")
            print(f"  cd {name}")
            print("  npm install")
            print("  npm run dev")
    else:
        print("  2. npm install")
        print("  3. npm run dev")

    print()


def interactive_mode():
    """Run setup in interactive mode with prompts."""
    print("🎬 Barba.js Project Setup")
    print("=" * 50)
    print()

    # Project name
    name = input("Project name: ").strip()
    if not name:
        print("❌ Project name is required")
        sys.exit(1)

    # Transition type
    print()
    print("Available transition types:")
    print("  1. fade (simple fade)")
    print("  2. slide (horizontal slide)")
    print("  3. scale (zoom with fade)")
    print("  4. stagger (staggered elements)")
    print("  5. curtain (curtain overlay)")
    print()
    transition_choice = input("Select transition (1-5, default: 1): ").strip()

    transitions = ['fade', 'slide', 'scale', 'stagger', 'curtain']
    try:
        transition_idx = int(transition_choice) - 1 if transition_choice else 0
        transition = transitions[transition_idx]
    except (ValueError, IndexError):
        transition = 'fade'

    # Minimal setup
    print()
    minimal_input = input("Minimal setup? (no example pages) [y/N]: ").strip().lower()
    minimal = minimal_input in ['y', 'yes']

    # Install dependencies
    print()
    no_install_input = input("Skip npm install? [y/N]: ").strip().lower()
    no_install = no_install_input in ['y', 'yes']

    print()
    print("=" * 50)
    print()

    # Create project
    create_project(name, '.', transition, minimal, no_install)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Initialize a new Barba.js project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--name',
        help='Project directory name'
    )

    parser.add_argument(
        '--transition',
        choices=['fade', 'slide', 'scale', 'stagger', 'curtain'],
        default='fade',
        help='Transition type (default: fade)'
    )

    parser.add_argument(
        '--minimal',
        action='store_true',
        help='Create minimal setup without example pages'
    )

    parser.add_argument(
        '--no-install',
        action='store_true',
        help='Skip npm install step'
    )

    parser.add_argument(
        '--output-dir',
        default='.',
        help='Parent directory for project (default: current directory)'
    )

    args = parser.parse_args()

    # Interactive mode if no name specified
    if not args.name:
        interactive_mode()
        return

    # CLI mode
    create_project(
        args.name,
        args.output_dir,
        args.transition,
        args.minimal,
        args.no_install
    )


if __name__ == '__main__':
    main()
