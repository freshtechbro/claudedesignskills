#!/usr/bin/env python3
"""
Modern Web Design Auditor

Audits HTML/CSS code for:
- Accessibility compliance (WCAG)
- Performance best practices
- Modern design pattern usage
- SEO basics

Usage:
    ./design_audit.py                              # Interactive mode
    ./design_audit.py --file index.html            # Audit specific file
    ./design_audit.py --file index.html --report audit.txt  # Save report
"""

import sys
import argparse
import re
from pathlib import Path
from collections import defaultdict


class DesignAuditor:
    """Audits web design code for best practices."""

    def __init__(self, html_content):
        self.html = html_content
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.passes = defaultdict(list)

    def audit(self):
        """Run all audits."""
        self.audit_accessibility()
        self.audit_performance()
        self.audit_seo()
        self.audit_responsive()
        self.audit_modern_practices()

    def audit_accessibility(self):
        """Audit for accessibility issues."""
        category = 'Accessibility'

        # Check for alt attributes on images
        imgs_without_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', self.html, re.IGNORECASE)
        if imgs_without_alt:
            self.issues[category].append(
                f"Found {len(imgs_without_alt)} images without alt attributes"
            )
        else:
            self.passes[category].append("All images have alt attributes")

        # Check for lang attribute
        if not re.search(r'<html[^>]+lang=', self.html, re.IGNORECASE):
            self.issues[category].append("Missing lang attribute on <html> element")
        else:
            self.passes[category].append("HTML lang attribute present")

        # Check for semantic HTML
        if '<div class="header"' in self.html or '<div id="header"' in self.html:
            self.warnings[category].append("Consider using <header> instead of div with class/id 'header'")

        if '<div class="nav"' in self.html or '<div id="nav"' in self.html:
            self.warnings[category].append("Consider using <nav> instead of div with class/id 'nav'")

        if '<div class="footer"' in self.html or '<div id="footer"' in self.html:
            self.warnings[category].append("Consider using <footer> instead of div with class/id 'footer'")

        # Check for proper heading hierarchy
        h1_count = len(re.findall(r'<h1[^>]*>', self.html, re.IGNORECASE))
        if h1_count == 0:
            self.issues[category].append("No <h1> element found")
        elif h1_count > 1:
            self.warnings[category].append(f"Multiple <h1> elements found ({h1_count}). Consider using only one per page")

        # Check for aria-labels on icon buttons
        button_pattern = r'<button[^>]*>[\s]*<(?:svg|i|span)[^>]*>[\s]*</(?:svg|i|span)>[\s]*</button>'
        icon_buttons = re.findall(button_pattern, self.html, re.IGNORECASE)
        for button in icon_buttons:
            if 'aria-label' not in button:
                self.warnings[category].append("Icon button found without aria-label")
                break

        # Check for form labels
        inputs = re.findall(r'<input[^>]*>', self.html, re.IGNORECASE)
        for input_tag in inputs:
            if 'id=' in input_tag:
                input_id = re.search(r'id="([^"]+)"', input_tag)
                if input_id:
                    label_pattern = f'for="{input_id.group(1)}"'
                    if label_pattern not in self.html:
                        self.warnings[category].append(f"Input with id='{input_id.group(1)}' has no associated label")

        # Check for skip links
        if not re.search(r'skip to (main |)content', self.html, re.IGNORECASE):
            self.warnings[category].append("Consider adding a skip link for keyboard navigation")

    def audit_performance(self):
        """Audit for performance issues."""
        category = 'Performance'

        # Check for inline styles (should be minimal)
        inline_styles = re.findall(r'style="[^"]*"', self.html)
        if len(inline_styles) > 10:
            self.warnings[category].append(
                f"Found {len(inline_styles)} inline styles. Consider moving to external CSS."
            )

        # Check for lazy loading
        imgs = re.findall(r'<img[^>]*>', self.html, re.IGNORECASE)
        lazy_imgs = [img for img in imgs if 'loading="lazy"' in img or "loading='lazy'" in img]
        if imgs and not lazy_imgs:
            self.warnings[category].append(
                "Consider adding loading='lazy' to below-fold images"
            )

        # Check for modern image formats
        if re.search(r'<img[^>]+src="[^"]+\.(jpg|jpeg|png)"', self.html, re.IGNORECASE):
            if not re.search(r'<picture>|<source[^>]+type="image/webp"', self.html, re.IGNORECASE):
                self.warnings[category].append(
                    "Consider using modern image formats (WebP/AVIF) with <picture> element"
                )

        # Check for preload/prefetch
        if re.search(r'<link[^>]+rel="preload"', self.html, re.IGNORECASE):
            self.passes[category].append("Using preload for critical resources")

        # Check for async/defer on scripts
        scripts = re.findall(r'<script[^>]*src="[^"]*"[^>]*>', self.html, re.IGNORECASE)
        scripts_without_async_defer = [s for s in scripts if 'async' not in s and 'defer' not in s]
        if scripts_without_async_defer:
            self.warnings[category].append(
                f"Found {len(scripts_without_async_defer)} script tags without async or defer attributes"
            )

        # Check for width/height on images (prevents CLS)
        imgs_without_dimensions = [
            img for img in imgs
            if not ('width=' in img and 'height=' in img)
            and 'aspect-ratio' not in self.html
        ]
        if imgs_without_dimensions:
            self.warnings[category].append(
                f"Found {len(imgs_without_dimensions)} images without explicit dimensions (width/height). This can cause Cumulative Layout Shift."
            )

    def audit_seo(self):
        """Audit for SEO basics."""
        category = 'SEO'

        # Check for title tag
        if not re.search(r'<title>[^<]+</title>', self.html, re.IGNORECASE):
            self.issues[category].append("Missing <title> tag")
        else:
            title = re.search(r'<title>([^<]+)</title>', self.html, re.IGNORECASE)
            if title and len(title.group(1)) < 10:
                self.warnings[category].append("Title tag is too short (< 10 characters)")
            else:
                self.passes[category].append("Title tag present and sufficient length")

        # Check for meta description
        if not re.search(r'<meta[^>]+name="description"', self.html, re.IGNORECASE):
            self.warnings[category].append("Missing meta description tag")
        else:
            self.passes[category].append("Meta description present")

        # Check for viewport meta tag
        if not re.search(r'<meta[^>]+name="viewport"', self.html, re.IGNORECASE):
            self.issues[category].append("Missing viewport meta tag (required for mobile)")
        else:
            self.passes[category].append("Viewport meta tag present")

        # Check for charset
        if not re.search(r'<meta[^>]+charset=', self.html, re.IGNORECASE):
            self.warnings[category].append("Missing charset declaration")
        else:
            self.passes[category].append("Charset declaration present")

    def audit_responsive(self):
        """Audit for responsive design."""
        category = 'Responsive Design'

        # Check for viewport meta tag
        if re.search(r'<meta[^>]+name="viewport"', self.html, re.IGNORECASE):
            self.passes[category].append("Viewport meta tag present")
        else:
            self.issues[category].append("Missing viewport meta tag")

        # Check for media queries in CSS
        if re.search(r'@media[^{]+{', self.html, re.IGNORECASE):
            self.passes[category].append("Media queries found (responsive CSS)")
        else:
            self.warnings[category].append("No media queries found. Consider adding responsive styles.")

        # Check for clamp() or min/max functions (modern responsive approach)
        if re.search(r'clamp\(|min\(|max\(', self.html, re.IGNORECASE):
            self.passes[category].append("Using modern CSS functions (clamp/min/max) for fluid sizing")

    def audit_modern_practices(self):
        """Audit for modern design practices."""
        category = 'Modern Practices'

        # Check for CSS custom properties
        if re.search(r'--[a-z-]+:', self.html, re.IGNORECASE):
            self.passes[category].append("Using CSS custom properties (variables)")

        # Check for CSS Grid or Flexbox
        if re.search(r'display:\s*(grid|flex)', self.html, re.IGNORECASE):
            self.passes[category].append("Using modern layout (Grid or Flexbox)")

        # Check for prefers-reduced-motion
        if re.search(r'prefers-reduced-motion', self.html, re.IGNORECASE):
            self.passes[category].append("Respecting prefers-reduced-motion preference")
        else:
            if re.search(r'animation:|transition:', self.html, re.IGNORECASE):
                self.warnings[category].append(
                    "Animations found but no @media (prefers-reduced-motion) rule detected"
                )

        # Check for semantic HTML5 elements
        semantic_elements = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        found_semantic = [el for el in semantic_elements if f'<{el}' in self.html.lower()]
        if found_semantic:
            self.passes[category].append(f"Using semantic HTML5 elements: {', '.join(found_semantic)}")
        else:
            self.warnings[category].append("No semantic HTML5 elements found. Consider using <header>, <nav>, <main>, etc.")

        # Check for focus-visible
        if ':focus-visible' in self.html:
            self.passes[category].append("Using :focus-visible for keyboard navigation")
        elif ':focus' in self.html:
            self.passes[category].append("Using :focus styles (consider upgrading to :focus-visible)")

    def generate_report(self):
        """Generate audit report."""
        report = []
        report.append("=" * 70)
        report.append("Modern Web Design Audit Report")
        report.append("=" * 70)
        report.append("")

        # Summary
        total_issues = sum(len(v) for v in self.issues.values())
        total_warnings = sum(len(v) for v in self.warnings.values())
        total_passes = sum(len(v) for v in self.passes.values())

        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"❌ Issues: {total_issues}")
        report.append(f"⚠️  Warnings: {total_warnings}")
        report.append(f"✅ Passes: {total_passes}")
        report.append("")

        # Score calculation
        score = (total_passes / (total_passes + total_warnings + total_issues)) * 100 if (total_passes + total_warnings + total_issues) > 0 else 0
        report.append(f"Overall Score: {score:.1f}/100")
        report.append("")

        # Detailed results
        categories = set(list(self.issues.keys()) + list(self.warnings.keys()) + list(self.passes.keys()))

        for category in sorted(categories):
            report.append(f"\n{category}")
            report.append("-" * 70)

            if category in self.issues:
                report.append("\n❌ ISSUES (must fix):")
                for issue in self.issues[category]:
                    report.append(f"   • {issue}")

            if category in self.warnings:
                report.append("\n⚠️  WARNINGS (should fix):")
                for warning in self.warnings[category]:
                    report.append(f"   • {warning}")

            if category in self.passes:
                report.append("\n✅ PASSES:")
                for passing in self.passes[category]:
                    report.append(f"   • {passing}")

            report.append("")

        # Recommendations
        report.append("\nRECOMMENDATIONS")
        report.append("-" * 70)

        if total_issues > 0:
            report.append("1. Address all ISSUES first (accessibility and critical SEO)")
        if total_warnings > 5:
            report.append("2. Review WARNINGS and implement fixes where applicable")
        if score < 70:
            report.append("3. Consider a comprehensive design review")
        else:
            report.append("Good job! Your design follows many modern best practices.")

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)


def audit_file(filepath, output_file=None):
    """Audit a specific file."""
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    if not path.suffix in ['.html', '.htm']:
        print(f"Warning: File '{filepath}' is not an HTML file.")

    print(f"Auditing: {path}")
    print("Please wait...\n")

    html_content = path.read_text()
    auditor = DesignAuditor(html_content)
    auditor.audit()
    report = auditor.generate_report()

    if output_file:
        output_path = Path(output_file)
        output_path.write_text(report)
        print(f"✅ Audit complete!")
        print(f"   Report saved to: {output_path}")
    else:
        print(report)


def interactive_mode():
    """Interactive audit mode."""
    print("\n" + "="*70)
    print("Modern Web Design Auditor")
    print("="*70)
    print("\nThis tool audits HTML files for:")
    print("  • Accessibility (WCAG compliance)")
    print("  • Performance best practices")
    print("  • SEO basics")
    print("  • Responsive design")
    print("  • Modern CSS/HTML practices")
    print("")

    filepath = input("Enter path to HTML file: ").strip()

    if not filepath:
        print("Error: No file path provided.")
        sys.exit(1)

    save_report = input("\nSave report to file? (y/n): ").strip().lower()

    if save_report == 'y':
        output_file = input("Enter output filename (e.g., audit-report.txt): ").strip()
        if not output_file:
            output_file = "audit-report.txt"
        audit_file(filepath, output_file)
    else:
        audit_file(filepath)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Audit web design code for best practices'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='HTML file to audit'
    )
    parser.add_argument(
        '--report',
        type=str,
        help='Output file for audit report'
    )

    args = parser.parse_args()

    if args.file:
        audit_file(args.file, args.report)
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
