#!/usr/bin/env python3
"""
AOS HTML Generator

Generates HTML boilerplate with AOS scroll animations.
Creates ready-to-use HTML files with common AOS patterns.

Usage:
    ./aos_generator.py                          # Interactive mode
    ./aos_generator.py --template landing      # Use template
    ./aos_generator.py --template hero --output hero.html
"""

import sys
import argparse
import os

# HTML Templates
TEMPLATES = {
    "hero": {
        "name": "Hero Section",
        "description": "Animated hero section with heading, subtext, and CTA",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Hero Section</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }

    .hero {
      text-align: center;
      padding: 2rem;
      max-width: 800px;
    }

    h1 {
      font-size: 3.5rem;
      font-weight: 800;
      margin-bottom: 1.5rem;
      line-height: 1.2;
    }

    p {
      font-size: 1.25rem;
      margin-bottom: 2rem;
      opacity: 0.9;
    }

    .cta-button {
      display: inline-block;
      padding: 1rem 2.5rem;
      font-size: 1.1rem;
      font-weight: 600;
      color: #667eea;
      background: white;
      border: none;
      border-radius: 50px;
      cursor: pointer;
      text-decoration: none;
      transition: transform 0.2s;
    }

    .cta-button:hover {
      transform: scale(1.05);
    }
  </style>
</head>
<body>
  <section class="hero">
    <h1 data-aos="fade-down" data-aos-duration="800">
      Welcome to the Future
    </h1>

    <p data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">
      Transform your ideas into reality with cutting-edge technology
    </p>

    <a href="#" class="cta-button" data-aos="zoom-in" data-aos-delay="400" data-aos-duration="500">
      Get Started
    </a>
  </section>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true
    });
  </script>
</body>
</html>"""
    },
    "features": {
        "name": "Feature Cards",
        "description": "Grid of animated feature cards",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Feature Cards</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f7fafc;
      padding: 4rem 2rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    h1 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 3rem;
      color: #2d3748;
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
    }

    .feature-card {
      background: white;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s, box-shadow 0.3s;
    }

    .feature-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    h3 {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
      color: #2d3748;
    }

    p {
      color: #718096;
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 data-aos="fade-down">Our Features</h1>

    <div class="features-grid">
      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="0">
        <div class="feature-icon">🚀</div>
        <h3>Fast Performance</h3>
        <p>Lightning-fast load times and smooth interactions for the best user experience.</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="100">
        <div class="feature-icon">🎨</div>
        <h3>Beautiful Design</h3>
        <p>Carefully crafted interfaces that are both functional and aesthetically pleasing.</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="200">
        <div class="feature-icon">🔒</div>
        <h3>Secure</h3>
        <p>Enterprise-grade security to keep your data safe and protected.</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="300">
        <div class="feature-icon">📱</div>
        <h3>Responsive</h3>
        <p>Works perfectly on all devices from mobile phones to desktop computers.</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="400">
        <div class="feature-icon">⚡</div>
        <h3>Easy to Use</h3>
        <p>Intuitive interface that requires no training to get started.</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-duration="600" data-aos-delay="500">
        <div class="feature-icon">🌟</div>
        <h3>Quality Support</h3>
        <p>24/7 customer support ready to help you whenever you need assistance.</p>
      </div>
    </div>
  </div>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true
    });
  </script>
</body>
</html>"""
    },
    "landing": {
        "name": "Landing Page",
        "description": "Complete landing page with multiple sections",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Landing Page</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #2d3748;
      line-height: 1.6;
    }

    section {
      padding: 5rem 2rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Hero */
    .hero {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-align: center;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .hero h1 {
      font-size: 3.5rem;
      margin-bottom: 1.5rem;
    }

    .hero p {
      font-size: 1.25rem;
      margin-bottom: 2rem;
      opacity: 0.9;
    }

    .cta-button {
      display: inline-block;
      padding: 1rem 2.5rem;
      font-size: 1.1rem;
      font-weight: 600;
      color: #667eea;
      background: white;
      border-radius: 50px;
      text-decoration: none;
      transition: transform 0.2s;
    }

    .cta-button:hover {
      transform: scale(1.05);
    }

    /* Features */
    .features {
      background: #f7fafc;
    }

    .features h2 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 3rem;
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
    }

    .feature {
      text-align: center;
      padding: 2rem;
    }

    .feature-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
    }

    /* Testimonials */
    .testimonials {
      background: white;
    }

    .testimonials h2 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 3rem;
    }

    .testimonial {
      background: #f7fafc;
      padding: 2rem;
      border-radius: 12px;
      margin-bottom: 2rem;
    }

    .testimonial p {
      font-size: 1.1rem;
      margin-bottom: 1rem;
      font-style: italic;
    }

    .testimonial cite {
      font-weight: 600;
      color: #667eea;
    }

    /* CTA */
    .cta-section {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-align: center;
    }

    .cta-section h2 {
      font-size: 2.5rem;
      margin-bottom: 1.5rem;
    }
  </style>
</head>
<body>
  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <h1 data-aos="fade-down" data-aos-duration="800">
        Build Something Amazing
      </h1>
      <p data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">
        The most powerful platform for creating extraordinary experiences
      </p>
      <a href="#" class="cta-button" data-aos="zoom-in" data-aos-delay="400">
        Start Free Trial
      </a>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <div class="container">
      <h2 data-aos="fade-down">Why Choose Us</h2>

      <div class="features-grid">
        <div class="feature" data-aos="fade-up" data-aos-delay="0">
          <div class="feature-icon">🚀</div>
          <h3>Lightning Fast</h3>
          <p>Optimized for speed and performance</p>
        </div>

        <div class="feature" data-aos="fade-up" data-aos-delay="100">
          <div class="feature-icon">🎨</div>
          <h3>Beautiful UI</h3>
          <p>Stunning designs that users love</p>
        </div>

        <div class="feature" data-aos="fade-up" data-aos-delay="200">
          <div class="feature-icon">🔒</div>
          <h3>Secure</h3>
          <p>Enterprise-grade security built-in</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials Section -->
  <section class="testimonials">
    <div class="container">
      <h2 data-aos="fade-down">What Our Customers Say</h2>

      <div class="testimonial" data-aos="zoom-in" data-aos-duration="500">
        <p>"This product completely transformed how we work. Incredible!"</p>
        <cite>— Sarah Johnson, CEO at TechCorp</cite>
      </div>

      <div class="testimonial" data-aos="zoom-in" data-aos-duration="500" data-aos-delay="100">
        <p>"Best investment we've made this year. Highly recommended!"</p>
        <cite>— Michael Chen, Founder at StartupXYZ</cite>
      </div>

      <div class="testimonial" data-aos="zoom-in" data-aos-duration="500" data-aos-delay="200">
        <p>"The support team is amazing and the product is even better."</p>
        <cite>— Emma Davis, Designer at CreativeStudio</cite>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta-section">
    <div class="container">
      <h2 data-aos="fade-down">Ready to Get Started?</h2>
      <p data-aos="fade-up" data-aos-delay="200">
        Join thousands of happy customers today
      </p>
      <a href="#" class="cta-button" data-aos="zoom-in" data-aos-delay="400">
        Start Free Trial
      </a>
    </div>
  </section>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true,
      offset: 100
    });
  </script>
</body>
</html>"""
    },
    "gallery": {
        "name": "Image Gallery",
        "description": "Animated image gallery with zoom effects",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Image Gallery</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f7fafc;
      padding: 4rem 2rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    h1 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 3rem;
      color: #2d3748;
    }

    .gallery {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
    }

    .gallery-item {
      position: relative;
      overflow: hidden;
      border-radius: 12px;
      aspect-ratio: 4/3;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      cursor: pointer;
      transition: transform 0.3s;
    }

    .gallery-item:hover {
      transform: scale(1.02);
    }

    .gallery-item::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.3);
      opacity: 0;
      transition: opacity 0.3s;
    }

    .gallery-item:hover::before {
      opacity: 1;
    }

    .gallery-caption {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 1.5rem;
      color: white;
      background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
      transform: translateY(100%);
      transition: transform 0.3s;
    }

    .gallery-item:hover .gallery-caption {
      transform: translateY(0);
    }

    .gallery-caption h3 {
      font-size: 1.25rem;
      margin-bottom: 0.5rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 data-aos="fade-down">Our Portfolio</h1>

    <div class="gallery">
      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="0">
        <div class="gallery-caption">
          <h3>Project Alpha</h3>
          <p>Modern web application</p>
        </div>
      </div>

      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="100">
        <div class="gallery-caption">
          <h3>Project Beta</h3>
          <p>E-commerce platform</p>
        </div>
      </div>

      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="200">
        <div class="gallery-caption">
          <h3>Project Gamma</h3>
          <p>Mobile app design</p>
        </div>
      </div>

      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="300">
        <div class="gallery-caption">
          <h3>Project Delta</h3>
          <p>Brand identity</p>
        </div>
      </div>

      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="400">
        <div class="gallery-caption">
          <h3>Project Epsilon</h3>
          <p>Marketing campaign</p>
        </div>
      </div>

      <div class="gallery-item" data-aos="zoom-in-up" data-aos-duration="800" data-aos-delay="500">
        <div class="gallery-caption">
          <h3>Project Zeta</h3>
          <p>Product photography</p>
        </div>
      </div>
    </div>
  </div>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true
    });
  </script>
</body>
</html>"""
    },
    "timeline": {
        "name": "Timeline",
        "description": "Vertical timeline with alternating content",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Timeline</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f7fafc;
      padding: 4rem 2rem;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
    }

    h1 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 4rem;
      color: #2d3748;
    }

    .timeline {
      position: relative;
      padding-left: 3rem;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 2px;
      background: #667eea;
    }

    .timeline-item {
      position: relative;
      margin-bottom: 3rem;
    }

    .timeline-item::before {
      content: '';
      position: absolute;
      left: -3.5rem;
      top: 0;
      width: 1rem;
      height: 1rem;
      background: #667eea;
      border-radius: 50%;
      border: 3px solid #f7fafc;
    }

    .timeline-content {
      background: white;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .timeline-date {
      color: #667eea;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }

    .timeline-content h3 {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
      color: #2d3748;
    }

    .timeline-content p {
      color: #718096;
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 data-aos="fade-down">Our Journey</h1>

    <div class="timeline">
      <div class="timeline-item" data-aos="slide-right" data-aos-duration="800">
        <div class="timeline-content">
          <div class="timeline-date">January 2020</div>
          <h3>Company Founded</h3>
          <p>Started with a vision to transform the industry and make a difference.</p>
        </div>
      </div>

      <div class="timeline-item" data-aos="slide-right" data-aos-duration="800" data-aos-delay="100">
        <div class="timeline-content">
          <div class="timeline-date">June 2020</div>
          <h3>First Product Launch</h3>
          <p>Released our flagship product to market with overwhelming positive response.</p>
        </div>
      </div>

      <div class="timeline-item" data-aos="slide-right" data-aos-duration="800" data-aos-delay="200">
        <div class="timeline-content">
          <div class="timeline-date">December 2020</div>
          <h3>Reached 10,000 Users</h3>
          <p>Hit a major milestone with rapid user growth and engagement.</p>
        </div>
      </div>

      <div class="timeline-item" data-aos="slide-right" data-aos-duration="800" data-aos-delay="300">
        <div class="timeline-content">
          <div class="timeline-date">March 2021</div>
          <h3>Series A Funding</h3>
          <p>Secured significant investment to scale operations and expand the team.</p>
        </div>
      </div>

      <div class="timeline-item" data-aos="slide-right" data-aos-duration="800" data-aos-delay="400">
        <div class="timeline-content">
          <div class="timeline-date">Present</div>
          <h3>Global Expansion</h3>
          <p>Continuing to grow and serve customers worldwide with innovative solutions.</p>
        </div>
      </div>
    </div>
  </div>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true
    });
  </script>
</body>
</html>"""
    }
}


def list_templates():
    """List all available templates."""
    print("\nAvailable Templates:")
    print("=" * 60)

    for template_id, template in TEMPLATES.items():
        print(f"\n{template_id}")
        print(f"  Name: {template['name']}")
        print(f"  Description: {template['description']}")

    print()


def generate_html(template_name, output_path=None):
    """Generate HTML from template."""
    if template_name not in TEMPLATES:
        print(f"Error: Template '{template_name}' not found")
        print("\nAvailable templates:")
        for tid in TEMPLATES.keys():
            print(f"  - {tid}")
        return False

    template = TEMPLATES[template_name]
    html_content = template["html"]

    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✓ Generated {template['name']}: {output_path}")
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    else:
        # Output to stdout
        print(html_content)
        return True


def interactive_mode():
    """Run interactive HTML generator."""
    print("\nAOS HTML Generator - Interactive Mode")
    print("=" * 60)

    list_templates()

    print("Enter template name:")
    template_name = input("> ").strip().lower()

    if template_name not in TEMPLATES:
        print(f"Error: Template '{template_name}' not found")
        return

    print("\nEnter output filename (or press Enter to print to console):")
    output_path = input("> ").strip()

    if not output_path:
        output_path = None

    generate_html(template_name, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML boilerplate with AOS animations"
    )
    parser.add_argument(
        "--template",
        choices=list(TEMPLATES.keys()),
        help="Template to use"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: print to console)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available templates"
    )

    args = parser.parse_args()

    if args.list:
        list_templates()
    elif args.template:
        generate_html(args.template, args.output)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
