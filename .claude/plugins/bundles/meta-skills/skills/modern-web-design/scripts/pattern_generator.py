#!/usr/bin/env python3
"""
Modern Web Design Pattern Generator

Generates boilerplate code for common modern web design patterns including:
- Hero sections
- Card layouts
- Navigation patterns
- Form patterns
- Animation patterns

Usage:
    ./pattern_generator.py                          # Interactive mode
    ./pattern_generator.py --pattern hero           # Generate specific pattern
    ./pattern_generator.py --pattern card --output card.html  # Output to file
"""

import sys
import argparse
from pathlib import Path

# Pattern templates
PATTERNS = {
    'hero': {
        'name': 'Immersive Hero Section',
        'description': 'Full-viewport hero with animated background',
        'html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .hero {
            position: relative;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .hero__bg {
            position: absolute;
            inset: 0;
            opacity: 0.3;
        }

        .hero__content {
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            max-width: 800px;
            padding: 2rem;
        }

        .hero__title {
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 700;
            line-height: 0.95;
            letter-spacing: -0.03em;
            margin-bottom: 1.5rem;
            animation: fadeInUp 0.8s ease;
        }

        .hero__subtitle {
            font-size: clamp(1.25rem, 2.5vw, 1.75rem);
            margin-bottom: 2rem;
            opacity: 0.9;
            animation: fadeInUp 0.8s ease 0.2s backwards;
        }

        .hero__cta {
            display: inline-block;
            padding: 1rem 2.5rem;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 1.125rem;
            transition: transform 0.2s, box-shadow 0.2s;
            animation: fadeInUp 0.8s ease 0.4s backwards;
        }

        .hero__cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .scroll-indicator {
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            opacity: 0.7;
            animation: bounce 2s infinite;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes bounce {
            0%, 100% { transform: translateX(-50%) translateY(0); }
            50% { transform: translateX(-50%) translateY(-10px); }
        }

        /* Respect reduced motion preference */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero__bg" id="bg"></div>
        <div class="hero__content">
            <h1 class="hero__title">Modern Design</h1>
            <p class="hero__subtitle">Performance meets beauty in every pixel</p>
            <a href="#content" class="hero__cta">Explore</a>
        </div>
        <div class="scroll-indicator">
            <span>↓ Scroll</span>
        </div>
    </section>

    <section id="content" style="padding: 4rem 2rem; text-align: center;">
        <h2>Your content here</h2>
    </section>
</body>
</html>'''
    },

    'card': {
        'name': 'Interactive Card Grid',
        'description': 'Responsive card grid with hover effects',
        'html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Grid</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
            padding: 4rem 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }

        .card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }

        .card__image {
            width: 100%;
            aspect-ratio: 16 / 9;
            object-fit: cover;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .card__content {
            padding: 1.5rem;
        }

        .card__title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: #1a1a1a;
        }

        .card__description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .card__link {
            display: inline-flex;
            align-items: center;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: transform 0.2s;
        }

        .card__link:hover {
            transform: translateX(4px);
        }

        /* Accessibility */
        .card:focus-within {
            outline: 3px solid #667eea;
            outline-offset: 2px;
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="margin-bottom: 3rem; font-size: 2.5rem;">Featured Content</h1>

        <div class="card-grid">
            <article class="card">
                <img class="card__image" src="" alt="Card image" aria-hidden="true">
                <div class="card__content">
                    <h2 class="card__title">Card Title 1</h2>
                    <p class="card__description">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                        Sed do eiusmod tempor incididunt ut labore.
                    </p>
                    <a href="#" class="card__link">
                        Learn more →
                    </a>
                </div>
            </article>

            <article class="card">
                <img class="card__image" src="" alt="Card image" aria-hidden="true">
                <div class="card__content">
                    <h2 class="card__title">Card Title 2</h2>
                    <p class="card__description">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                        Sed do eiusmod tempor incididunt ut labore.
                    </p>
                    <a href="#" class="card__link">
                        Learn more →
                    </a>
                </div>
            </article>

            <article class="card">
                <img class="card__image" src="" alt="Card image" aria-hidden="true">
                <div class="card__content">
                    <h2 class="card__title">Card Title 3</h2>
                    <p class="card__description">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                        Sed do eiusmod tempor incididunt ut labore.
                    </p>
                    <a href="#" class="card__link">
                        Learn more →
                    </a>
                </div>
            </article>
        </div>
    </div>
</body>
</html>'''
    },

    'navigation': {
        'name': 'Responsive Navigation',
        'description': 'Mobile-friendly navigation with hamburger menu',
        'html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            z-index: 100;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .nav__logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
            text-decoration: none;
        }

        .nav__toggle {
            display: none;
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.5rem;
        }

        .nav__toggle span {
            display: block;
            width: 25px;
            height: 3px;
            background: #333;
            margin: 5px 0;
            transition: transform 0.3s, opacity 0.3s;
        }

        .nav__toggle.active span:nth-child(1) {
            transform: translateY(8px) rotate(45deg);
        }

        .nav__toggle.active span:nth-child(2) {
            opacity: 0;
        }

        .nav__toggle.active span:nth-child(3) {
            transform: translateY(-8px) rotate(-45deg);
        }

        .nav__menu {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav__link {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }

        .nav__link:hover {
            color: #667eea;
        }

        .nav__link:focus-visible {
            outline: 3px solid #667eea;
            outline-offset: 4px;
            border-radius: 4px;
        }

        @media (max-width: 768px) {
            .nav__toggle {
                display: block;
            }

            .nav__menu {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                flex-direction: column;
                background: white;
                padding: 1rem;
                gap: 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transform: translateY(-100%);
                opacity: 0;
                pointer-events: none;
                transition: transform 0.3s, opacity 0.3s;
            }

            .nav__menu.active {
                transform: translateY(0);
                opacity: 1;
                pointer-events: all;
            }

            .nav__menu li {
                border-bottom: 1px solid #eee;
            }

            .nav__menu li:last-child {
                border-bottom: none;
            }

            .nav__link {
                display: block;
                padding: 1rem;
            }
        }

        .main {
            margin-top: 80px;
            padding: 4rem 2rem;
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav" role="navigation" aria-label="Main">
            <a href="#" class="nav__logo">Logo</a>

            <button class="nav__toggle" aria-label="Toggle navigation" aria-expanded="false">
                <span></span>
                <span></span>
                <span></span>
            </button>

            <ul class="nav__menu" id="navMenu">
                <li><a href="#" class="nav__link">Home</a></li>
                <li><a href="#" class="nav__link">About</a></li>
                <li><a href="#" class="nav__link">Services</a></li>
                <li><a href="#" class="nav__link">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main class="main">
        <h1>Main Content</h1>
        <p>Your content goes here...</p>
    </main>

    <script>
        const toggle = document.querySelector('.nav__toggle');
        const menu = document.querySelector('.nav__menu');

        toggle.addEventListener('click', () => {
            const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

            toggle.classList.toggle('active');
            menu.classList.toggle('active');
            toggle.setAttribute('aria-expanded', !isExpanded);
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menu.classList.contains('active')) {
                toggle.classList.remove('active');
                menu.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.focus();
            }
        });
    </script>
</body>
</html>'''
    },

    'form': {
        'name': 'Accessible Form',
        'description': 'Form with validation and accessibility features',
        'html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
            padding: 4rem 2rem;
        }

        .form-container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            margin-bottom: 2rem;
            color: #1a1a1a;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #333;
        }

        .required {
            color: #ef4444;
            margin-left: 0.25rem;
        }

        input, textarea {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.2s;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        input[aria-invalid="true"], textarea[aria-invalid="true"] {
            border-color: #ef4444;
        }

        .help-text {
            font-size: 0.875rem;
            color: #666;
            margin-top: 0.25rem;
        }

        .error-message {
            color: #ef4444;
            font-size: 0.875rem;
            margin-top: 0.25rem;
            display: none;
        }

        .error-message.visible {
            display: block;
        }

        .success-message {
            color: #10b981;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }

        button {
            background: #667eea;
            color: white;
            padding: 0.875rem 2rem;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s;
            min-height: 44px;
        }

        button:hover {
            background: #5568d3;
            transform: translateY(-1px);
        }

        button:active {
            transform: translateY(0);
        }

        button:focus-visible {
            outline: 3px solid #667eea;
            outline-offset: 2px;
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Contact Us</h1>

        <form id="contactForm" novalidate>
            <div class="form-group">
                <label for="name">
                    Full Name
                    <abbr class="required" title="required" aria-label="required">*</abbr>
                </label>
                <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    aria-required="true"
                    aria-describedby="name-error"
                >
                <div id="name-error" class="error-message" role="alert">
                    Please enter your name
                </div>
            </div>

            <div class="form-group">
                <label for="email">
                    Email Address
                    <abbr class="required" title="required" aria-label="required">*</abbr>
                </label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    aria-required="true"
                    aria-describedby="email-help email-error"
                >
                <p id="email-help" class="help-text">
                    We'll never share your email
                </p>
                <div id="email-error" class="error-message" role="alert">
                    Please enter a valid email address
                </div>
            </div>

            <div class="form-group">
                <label for="message">
                    Message
                    <abbr class="required" title="required" aria-label="required">*</abbr>
                </label>
                <textarea
                    id="message"
                    name="message"
                    rows="5"
                    required
                    aria-required="true"
                    aria-describedby="message-error"
                ></textarea>
                <div id="message-error" class="error-message" role="alert">
                    Please enter a message
                </div>
            </div>

            <button type="submit">Send Message</button>
        </form>
    </div>

    <script>
        const form = document.getElementById('contactForm');

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            let isValid = true;

            // Validate name
            const name = document.getElementById('name');
            const nameError = document.getElementById('name-error');
            if (!name.value.trim()) {
                nameError.classList.add('visible');
                name.setAttribute('aria-invalid', 'true');
                isValid = false;
            } else {
                nameError.classList.remove('visible');
                name.setAttribute('aria-invalid', 'false');
            }

            // Validate email
            const email = document.getElementById('email');
            const emailError = document.getElementById('email-error');
            const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
            if (!emailRegex.test(email.value)) {
                emailError.classList.add('visible');
                email.setAttribute('aria-invalid', 'true');
                isValid = false;
            } else {
                emailError.classList.remove('visible');
                email.setAttribute('aria-invalid', 'false');
            }

            // Validate message
            const message = document.getElementById('message');
            const messageError = document.getElementById('message-error');
            if (!message.value.trim()) {
                messageError.classList.add('visible');
                message.setAttribute('aria-invalid', 'true');
                isValid = false;
            } else {
                messageError.classList.remove('visible');
                message.setAttribute('aria-invalid', 'false');
            }

            if (isValid) {
                alert('Form submitted successfully!');
                form.reset();
            } else {
                // Focus first invalid field
                const firstInvalid = form.querySelector('[aria-invalid="true"]');
                if (firstInvalid) firstInvalid.focus();
            }
        });

        // Real-time validation
        ['name', 'email', 'message'].forEach(id => {
            const field = document.getElementById(id);
            field.addEventListener('blur', () => {
                // Trigger validation on blur
                form.dispatchEvent(new Event('submit'));
            });
        });
    </script>
</body>
</html>'''
    }
}


def list_patterns():
    """List all available patterns."""
    print("\nAvailable patterns:\n")
    for key, pattern in PATTERNS.items():
        print(f"  {key:<15} - {pattern['name']}")
        print(f"  {'':<15}   {pattern['description']}\n")


def generate_pattern(pattern_key, output_file=None):
    """Generate pattern code."""
    if pattern_key not in PATTERNS:
        print(f"Error: Pattern '{pattern_key}' not found.")
        print("\nRun './pattern_generator.py --list' to see available patterns.")
        sys.exit(1)

    pattern = PATTERNS[pattern_key]
    code = pattern['html']

    if output_file:
        output_path = Path(output_file)
        output_path.write_text(code)
        print(f"✅ Generated '{pattern['name']}' pattern")
        print(f"   Saved to: {output_path}")
    else:
        print(f"\n{'='*60}")
        print(f"{pattern['name']}")
        print(f"{'='*60}\n")
        print(code)


def interactive_mode():
    """Interactive pattern generation."""
    print("\n" + "="*60)
    print("Modern Web Design Pattern Generator")
    print("="*60)

    list_patterns()

    pattern_key = input("Select a pattern (or 'q' to quit): ").strip().lower()

    if pattern_key == 'q':
        print("Goodbye!")
        sys.exit(0)

    if pattern_key not in PATTERNS:
        print(f"Error: '{pattern_key}' is not a valid pattern.")
        sys.exit(1)

    save = input("\nSave to file? (y/n): ").strip().lower()

    if save == 'y':
        filename = input("Enter filename (e.g., hero.html): ").strip()
        if not filename:
            filename = f"{pattern_key}.html"
        generate_pattern(pattern_key, filename)
    else:
        generate_pattern(pattern_key)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate modern web design pattern boilerplate'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        help='Pattern to generate (hero, card, navigation, form)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available patterns'
    )

    args = parser.parse_args()

    if args.list:
        list_patterns()
        sys.exit(0)

    if args.pattern:
        generate_pattern(args.pattern, args.output)
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
