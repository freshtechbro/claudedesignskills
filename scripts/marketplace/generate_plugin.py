#!/usr/bin/env python3
"""
Plugin Generator for Claude Code

Converts a Claude skill into a complete plugin with:
- Plugin manifest (plugin.json)
- Skill content (copied from .claude/skills/)
- Slash commands (auto-generated from skill scripts)
- Agent definitions (domain experts based on skill context)

Usage:
    ./generate_plugin.py <skill-name>
    ./generate_plugin.py threejs-webgl

    # Generate all plugins
    ./generate_plugin.py --all
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional

# Skill categories for metadata
SKILL_CATEGORIES = {
    # Core 3D & Animation (5)
    "threejs-webgl": {"category": "3d-graphics", "tags": ["webgl", "threejs", "3d", "graphics", "webgpu"]},
    "gsap-scrolltrigger": {"category": "animation", "tags": ["gsap", "animation", "scroll", "scrolltrigger"]},
    "react-three-fiber": {"category": "3d-graphics", "tags": ["react", "threejs", "3d", "r3f", "webgl"]},
    "motion-framer": {"category": "animation", "tags": ["motion", "framer-motion", "react", "animation"]},
    "babylonjs-engine": {"category": "3d-graphics", "tags": ["babylonjs", "3d", "webgl", "game-engine"]},

    # Extended 3D & Scroll (6)
    "aframe-webxr": {"category": "3d-graphics", "tags": ["aframe", "webxr", "vr", "ar", "3d"]},
    "lightweight-3d-effects": {"category": "3d-graphics", "tags": ["zdog", "vanta", "vanilla-tilt", "lightweight", "3d"]},
    "playcanvas-engine": {"category": "3d-graphics", "tags": ["playcanvas", "webgl", "game-engine", "3d"]},
    "pixijs-2d": {"category": "2d-graphics", "tags": ["pixijs", "2d", "webgl", "canvas", "sprites"]},
    "locomotive-scroll": {"category": "scroll", "tags": ["locomotive", "smooth-scroll", "parallax", "scroll"]},
    "barba-js": {"category": "transitions", "tags": ["barba", "page-transitions", "routing", "spa"]},

    # Animation & Components (5)
    "react-spring-physics": {"category": "animation", "tags": ["react-spring", "physics", "animation", "spring"]},
    "animated-component-libraries": {"category": "components", "tags": ["magic-ui", "react-bits", "components", "animation"]},
    "scroll-reveal-libraries": {"category": "scroll", "tags": ["aos", "scroll-reveal", "animation", "scroll"]},
    "animejs": {"category": "animation", "tags": ["animejs", "timeline", "svg", "animation"]},
    "lottie-animations": {"category": "animation", "tags": ["lottie", "after-effects", "json", "animation"]},

    # 3D Authoring & Motion (4)
    "blender-web-pipeline": {"category": "3d-authoring", "tags": ["blender", "gltf", "export", "pipeline", "3d"]},
    "spline-interactive": {"category": "3d-authoring", "tags": ["spline", "no-code", "3d", "visual-editor"]},
    "rive-interactive": {"category": "animation", "tags": ["rive", "interactive", "state-machine", "animation"]},
    "substance-3d-texturing": {"category": "3d-authoring", "tags": ["substance", "texturing", "pbr", "materials"]},

    # Meta-Skills (2)
    "web3d-integration-patterns": {"category": "integration", "tags": ["integration", "patterns", "3d", "animation"]},
    "modern-web-design": {"category": "design", "tags": ["design", "trends", "ux", "web"]},

    # Additional
    "theatrejs-motion": {"category": "animation", "tags": ["theatrejs", "animation", "sequencing", "keyframes", "motion-design"]},
}

# Command templates for different skill types
COMMAND_TEMPLATES = {
    "setup": {
        "name": "setup",
        "description": "Initialize {skill_title} project with boilerplate code",
        "type": "initialization"
    },
    "generate": {
        "name": "generate",
        "description": "Generate {skill_title} components or code snippets",
        "type": "generation"
    },
    "optimize": {
        "name": "optimize",
        "description": "Optimize {skill_title} code for performance",
        "type": "optimization"
    }
}


class PluginGenerator:
    def __init__(self, skill_name: str, repo_root: Path):
        self.skill_name = skill_name
        self.repo_root = repo_root
        self.skill_dir = repo_root / ".claude" / "skills" / skill_name
        self.plugin_dir = repo_root / ".claude" / "plugins" / "individual" / skill_name

        # Load skill metadata
        self.skill_metadata = self._load_skill_metadata()

    def _load_skill_metadata(self) -> Dict:
        """Load SKILL.md and extract YAML frontmatter"""
        skill_md = self.skill_dir / "SKILL.md"

        if not skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found in {self.skill_dir}")

        with open(skill_md, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            raise ValueError(f"No YAML frontmatter found in {skill_md}")

        yaml_content = match.group(1)
        metadata = {}
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        return metadata

    def generate(self):
        """Generate complete plugin from skill"""
        print(f"\n🔧 Generating plugin: {self.skill_name}")
        print(f"   Source: {self.skill_dir}")
        print(f"   Target: {self.plugin_dir}")

        # Create plugin directory structure
        self._create_plugin_structure()

        # Generate plugin manifest
        self._generate_manifest()

        # Copy skill content
        self._copy_skill_content()

        # Generate slash commands
        self._generate_commands()

        # Generate agents
        self._generate_agents()

        print(f"✅ Plugin generated: {self.skill_name}\n")

    def _create_plugin_structure(self):
        """Create plugin directory structure"""
        directories = [
            self.plugin_dir,
            self.plugin_dir / ".claude-plugin",
            self.plugin_dir / "skills",
            self.plugin_dir / "commands",
            self.plugin_dir / "agents",
        ]

        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)

    def _generate_manifest(self):
        """Generate plugin.json manifest"""
        skill_title = self.skill_metadata.get('name', self.skill_name)
        description = self.skill_metadata.get('description', f'{skill_title} skill for Claude Code')

        # Get category and tags
        metadata = SKILL_CATEGORIES.get(self.skill_name, {
            "category": "general",
            "tags": [self.skill_name]
        })

        manifest = {
            "name": self.skill_name,
            "version": "1.0.0",
            "description": description,
            "author": "Claude Design Skillstack",
            "license": "Apache-2.0",
            "homepage": "https://github.com/freshtechbro/claudedesignskills",
            "repository": {
                "type": "git",
                "url": "https://github.com/freshtechbro/claudedesignskills.git"
            },
            "keywords": metadata["tags"],
            "category": metadata["category"],
            "skills": "skills/",
            "commands": "commands/",
            "agents": "agents/"
        }

        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"   📄 Created: plugin.json")

    def _copy_skill_content(self):
        """Copy skill directory to plugin/skills/"""
        src = self.skill_dir
        dst = self.plugin_dir / "skills" / self.skill_name

        if dst.exists():
            shutil.rmtree(dst)

        # Copy entire skill directory
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*.zip', '.DS_Store'))

        print(f"   📦 Copied: skill content")

    def _generate_commands(self):
        """Generate slash commands based on skill scripts"""
        commands_dir = self.plugin_dir / "commands"
        scripts_dir = self.skill_dir / "scripts"

        # Get skill title for commands
        skill_title = self._format_skill_title()
        command_prefix = self.skill_name

        # Check if skill has scripts
        if scripts_dir.exists() and list(scripts_dir.glob("*.py")):
            script_files = list(scripts_dir.glob("*.py"))

            # Generate commands based on script files
            for script_file in script_files:
                script_name = script_file.stem
                command_name = f"{script_name}"

                # Create command markdown
                command_content = self._create_command_markdown(
                    command_name=command_name,
                    command_prefix=command_prefix,
                    skill_title=skill_title,
                    script_name=script_name
                )

                command_file = commands_dir / f"{command_name}.md"
                with open(command_file, 'w') as f:
                    f.write(command_content)

                print(f"   🔨 Created: /{command_prefix}-{command_name} command")
        else:
            # Generate generic commands
            self._generate_generic_commands(commands_dir, command_prefix, skill_title)

    def _create_command_markdown(self, command_name: str, command_prefix: str,
                                  skill_title: str, script_name: str) -> str:
        """Create command markdown file"""
        full_command = f"{command_prefix}-{command_name}"

        return f"""# /{full_command}

{skill_title} - {command_name.replace('_', ' ').title()}

## Description

Executes the {command_name} script for {skill_title}.

## Usage

```bash
/{full_command}
```

## Implementation

This command runs the `{script_name}.py` script from the {skill_title} skill, which provides automated assistance for {command_name.replace('_', ' ')}.

## Notes

- This command leverages the skill's built-in automation scripts
- For interactive mode, the script will prompt for required information
- Check the skill documentation for detailed script usage
"""

    def _generate_generic_commands(self, commands_dir: Path, command_prefix: str, skill_title: str):
        """Generate generic commands for skills without scripts"""
        # Setup command
        setup_content = f"""# /{command_prefix}-setup

Initialize {skill_title} project

## Description

Provides setup guidance and boilerplate code for starting a new {skill_title} project.

## Usage

```bash
/{command_prefix}-setup
```

## What it does

- Analyzes your project structure
- Provides installation instructions
- Generates boilerplate code
- Offers configuration guidance
"""

        setup_file = commands_dir / "setup.md"
        with open(setup_file, 'w') as f:
            f.write(setup_content)

        print(f"   🔨 Created: /{command_prefix}-setup command")

        # Help command
        help_content = f"""# /{command_prefix}-help

Get help with {skill_title}

## Description

Provides comprehensive help and documentation for {skill_title}.

## Usage

```bash
/{command_prefix}-help
```

## What it does

- Shows common patterns and examples
- Links to official documentation
- Provides troubleshooting guidance
- Explains key concepts
"""

        help_file = commands_dir / "help.md"
        with open(help_file, 'w') as f:
            f.write(help_content)

        print(f"   🔨 Created: /{command_prefix}-help command")

    def _generate_agents(self):
        """Generate specialized agents for the skill domain"""
        agents_dir = self.plugin_dir / "agents"
        skill_title = self._format_skill_title()

        # Determine agent types based on skill category
        metadata = SKILL_CATEGORIES.get(self.skill_name, {})
        category = metadata.get("category", "general")

        if category in ["3d-graphics", "2d-graphics"]:
            self._create_graphics_agent(agents_dir, skill_title)
        elif category == "animation":
            self._create_animation_agent(agents_dir, skill_title)
        elif category == "3d-authoring":
            self._create_authoring_agent(agents_dir, skill_title)
        else:
            self._create_generic_agent(agents_dir, skill_title)

    def _create_graphics_agent(self, agents_dir: Path, skill_title: str):
        """Create 3D/2D graphics specialist agent"""
        agent_name = f"{self.skill_name}-architect"

        content = f"""# {skill_title} Architect

## Role

Expert 3D/graphics architect specializing in {skill_title} scene design, optimization, and best practices.

## Expertise

- Scene architecture and organization
- Performance optimization techniques
- Material and lighting setup
- Asset management and loading strategies
- Rendering optimization
- Cross-browser compatibility

## When to use

Activate this agent when working on:
- Complex 3D scene architecture
- Performance optimization challenges
- Advanced rendering techniques
- Large-scale 3D applications
- Graphics pipeline optimization

## Approach

1. Analyze scene requirements and constraints
2. Design optimal architecture for performance
3. Implement best practices from {skill_title} ecosystem
4. Optimize for target platforms and devices
5. Provide detailed implementation guidance

## Tools

This agent has access to:
- {skill_title} skill knowledge
- Optimization checklists and patterns
- Performance profiling guidance
- Asset pipeline recommendations
"""

        agent_file = agents_dir / f"{agent_name}.md"
        with open(agent_file, 'w') as f:
            f.write(content)

        print(f"   🤖 Created: {agent_name} agent")

    def _create_animation_agent(self, agents_dir: Path, skill_title: str):
        """Create animation choreographer agent"""
        agent_name = f"{self.skill_name}-choreographer"

        content = f"""# {skill_title} Animation Choreographer

## Role

Expert animation choreographer specializing in {skill_title} animation design, timing, and orchestration.

## Expertise

- Animation timing and easing
- Timeline sequencing
- Performance-optimized animations
- Cross-library animation integration
- Interactive animation patterns
- Scroll-driven animation design

## When to use

Activate this agent when working on:
- Complex animation sequences
- Multi-element choreography
- Scroll-triggered animations
- Interactive animation systems
- Animation performance optimization

## Approach

1. Understand animation goals and user experience
2. Design animation timing and sequencing
3. Implement using {skill_title} best practices
4. Optimize for smooth 60fps performance
5. Test across devices and browsers

## Tools

This agent has access to:
- {skill_title} skill knowledge
- Animation pattern libraries
- Performance optimization techniques
- Timeline management strategies
"""

        agent_file = agents_dir / f"{agent_name}.md"
        with open(agent_file, 'w') as f:
            f.write(content)

        print(f"   🤖 Created: {agent_name} agent")

    def _create_authoring_agent(self, agents_dir: Path, skill_title: str):
        """Create 3D authoring pipeline agent"""
        agent_name = f"{self.skill_name}-pipeline"

        content = f"""# {skill_title} Pipeline Specialist

## Role

Expert pipeline specialist for {skill_title} workflows, asset optimization, and web integration.

## Expertise

- Asset export and optimization
- Web-ready format conversion
- Texture and material optimization
- Automated pipeline workflows
- Quality assurance and validation
- Cross-platform compatibility

## When to use

Activate this agent when working on:
- Asset export pipelines
- Batch processing workflows
- Optimization for web delivery
- Integration with web frameworks
- Automated quality checks

## Approach

1. Analyze asset requirements and constraints
2. Design optimal export pipeline
3. Implement automation scripts
4. Optimize for web performance
5. Validate output quality

## Tools

This agent has access to:
- {skill_title} skill knowledge
- Pipeline automation scripts
- Optimization guidelines
- Quality validation checklists
"""

        agent_file = agents_dir / f"{agent_name}.md"
        with open(agent_file, 'w') as f:
            f.write(content)

        print(f"   🤖 Created: {agent_name} agent")

    def _create_generic_agent(self, agents_dir: Path, skill_title: str):
        """Create generic specialist agent"""
        agent_name = f"{self.skill_name}-specialist"

        content = f"""# {skill_title} Specialist

## Role

Expert specialist in {skill_title} implementation, patterns, and best practices.

## Expertise

- {skill_title} core concepts and patterns
- Integration with other libraries and frameworks
- Performance optimization
- Common pitfalls and solutions
- Best practices and conventions

## When to use

Activate this agent when working on:
- {skill_title} implementation challenges
- Integration with other technologies
- Performance optimization
- Troubleshooting and debugging
- Architecture decisions

## Approach

1. Understand project requirements and context
2. Apply {skill_title} best practices
3. Recommend optimal implementation patterns
4. Identify and solve common issues
5. Provide detailed guidance and examples

## Tools

This agent has access to:
- {skill_title} skill knowledge
- Pattern libraries and examples
- Troubleshooting guides
- Integration patterns
"""

        agent_file = agents_dir / f"{agent_name}.md"
        with open(agent_file, 'w') as f:
            f.write(content)

        print(f"   🤖 Created: {agent_name} agent")

    def _format_skill_title(self) -> str:
        """Format skill name as title (e.g., 'threejs-webgl' -> 'Three.js WebGL')"""
        # Special cases
        special_cases = {
            "threejs-webgl": "Three.js WebGL",
            "gsap-scrolltrigger": "GSAP ScrollTrigger",
            "react-three-fiber": "React Three Fiber",
            "motion-framer": "Framer Motion",
            "babylonjs-engine": "Babylon.js",
            "aframe-webxr": "A-Frame WebXR",
            "playcanvas-engine": "PlayCanvas",
            "pixijs-2d": "PixiJS 2D",
            "locomotive-scroll": "Locomotive Scroll",
            "barba-js": "Barba.js",
            "react-spring-physics": "React Spring",
            "animejs": "Anime.js",
            "lottie-animations": "Lottie",
            "blender-web-pipeline": "Blender Web Pipeline",
            "spline-interactive": "Spline",
            "rive-interactive": "Rive",
            "substance-3d-texturing": "Substance 3D",
            "theatrejs-motion": "Theatre.js",
        }

        return special_cases.get(self.skill_name, self.skill_name.replace('-', ' ').title())


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: ./generate_plugin.py <skill-name>")
        print("   or: ./generate_plugin.py --all")
        sys.exit(1)

    # Find repository root
    repo_root = Path(__file__).parent.parent.parent

    if sys.argv[1] == "--all":
        # Generate all plugins
        skills_dir = repo_root / ".claude" / "skills"
        skills = [d.name for d in skills_dir.iterdir()
                 if d.is_dir() and d.name != "skill-creator" and not d.name.startswith('.')]

        print(f"\n🚀 Generating {len(skills)} plugins...\n")

        for skill_name in sorted(skills):
            try:
                generator = PluginGenerator(skill_name, repo_root)
                generator.generate()
            except Exception as e:
                print(f"❌ Error generating {skill_name}: {e}\n")
                continue

        print(f"\n✅ Generated {len(skills)} plugins successfully!\n")
    else:
        skill_name = sys.argv[1]
        generator = PluginGenerator(skill_name, repo_root)
        generator.generate()


if __name__ == "__main__":
    main()
