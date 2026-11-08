#!/usr/bin/env python3
"""
Motion/Framer Motion Animation Generator
=========================================

Generate Motion component boilerplate for common animation patterns.

Usage:
    python3 animation_generator.py --type hover --name Button --output Button.jsx
    python3 animation_generator.py --type exit --name Modal --typescript
    python3 animation_generator.py --type drag --name Card --constraints
    python3 animation_generator.py --type layout --name Grid --shared-id

Animation Types:
    - hover: Hover animation with whileHover
    - tap: Tap animation with whileTap
    - drag: Draggable component with constraints
    - exit: Exit animation with AnimatePresence
    - layout: Layout animation with layout prop
    - scroll: Scroll-triggered animation with whileInView
    - spring: Spring physics animation
    - stagger: Staggered children animation
    - gesture: Combined gestures (hover + tap + drag)
    - variant: Variant-based animation system
    - custom: Custom template

Options:
    --type: Animation type (required)
    --name: Component name (default: Component)
    --output: Output file path (default: stdout)
    --typescript: Generate TypeScript component
    --constraints: Add drag constraints (for drag type)
    --shared-id: Add layoutId for shared animations
    --spring: Use spring physics for transitions
"""

import argparse
import sys
from typing import Optional, List


class MotionAnimationGenerator:
    """Generate Motion/Framer Motion animation boilerplate."""

    def __init__(
        self,
        animation_type: str,
        name: str = "Component",
        typescript: bool = False,
        constraints: bool = False,
        shared_id: Optional[str] = None,
        spring: bool = False,
    ):
        self.animation_type = animation_type
        self.name = name
        self.typescript = typescript
        self.constraints = constraints
        self.shared_id = shared_id
        self.spring = spring

    def generate(self) -> str:
        """Generate animation component code."""
        generators = {
            'hover': self._generate_hover,
            'tap': self._generate_tap,
            'drag': self._generate_drag,
            'exit': self._generate_exit,
            'layout': self._generate_layout,
            'scroll': self._generate_scroll,
            'spring': self._generate_spring,
            'stagger': self._generate_stagger,
            'gesture': self._generate_gesture,
            'variant': self._generate_variant,
            'custom': self._generate_custom,
        }

        generator = generators.get(self.animation_type)
        if not generator:
            raise ValueError(f"Unknown animation type: {self.animation_type}")

        return generator()

    def _get_imports(self, needs_presence: bool = False, needs_hooks: bool = False) -> str:
        """Generate import statements."""
        imports = ["import { motion"]

        if needs_presence:
            imports[0] += ", AnimatePresence"

        imports[0] += " } from 'framer-motion'"

        if needs_hooks:
            imports.append("import { useState } from 'react'")

        if self.typescript:
            imports.append("import type { Variants } from 'framer-motion'")

        return "\n".join(imports)

    def _get_props_interface(self) -> str:
        """Generate TypeScript props interface."""
        if not self.typescript:
            return ""

        return f"""
interface {self.name}Props {{
  children?: React.ReactNode
}}
"""

    def _generate_hover(self) -> str:
        """Generate hover animation component."""
        imports = self._get_imports()
        props_interface = self._get_props_interface()
        props_sig = f"({{ children }}: {self.name}Props)" if self.typescript else "({ children })"

        transition = "{ type: 'spring', stiffness: 300, damping: 20 }" if self.spring else "{ duration: 0.2 }"

        return f"""{imports}
{props_interface}
export function {self.name}{props_sig} {{
  return (
    <motion.div
      whileHover={{{{
        scale: 1.05,
        transition: {transition}
      }}}}
      transition={{{{ duration: 0.3 }}}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

    def _generate_tap(self) -> str:
        """Generate tap animation component."""
        imports = self._get_imports()
        props_interface = self._get_props_interface()
        props_sig = f"({{ children }}: {self.name}Props)" if self.typescript else "({ children })"

        return f"""{imports}
{props_interface}
export function {self.name}{props_sig} {{
  return (
    <motion.button
      whileHover={{{{ scale: 1.05 }}}}
      whileTap={{{{ scale: 0.95, rotate: 2 }}}}
      transition={{{{ type: 'spring', stiffness: 400, damping: 17 }}}}
    >
      {{children}}
    </motion.button>
  )
}}
"""

    def _generate_drag(self) -> str:
        """Generate drag animation component."""
        imports = self._get_imports()
        props_interface = self._get_props_interface()
        props_sig = f"({{ children }}: {self.name}Props)" if self.typescript else "({ children })"

        constraints_code = ""
        if self.constraints:
            constraints_code = """
      dragConstraints={{{{ left: -100, right: 100, top: -100, bottom: 100 }}}}
      dragElastic={{0.1}}"""

        return f"""{imports}
{props_interface}
export function {self.name}{props_sig} {{
  return (
    <motion.div
      drag{constraints_code}
      whileDrag={{{{
        scale: 1.1,
        cursor: 'grabbing',
        boxShadow: '0px 10px 30px rgba(0, 0, 0, 0.3)'
      }}}}
      dragTransition={{{{ bounceStiffness: 600, bounceDamping: 20 }}}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

    def _generate_exit(self) -> str:
        """Generate exit animation with AnimatePresence."""
        imports = self._get_imports(needs_presence=True, needs_hooks=True)
        props_interface = self._get_props_interface()

        return f"""{imports}
{props_interface}
export function {self.name}({{ children }}{': ' + self.name + 'Props' if self.typescript else ''}) {{
  const [isVisible, setIsVisible] = useState(true)

  return (
    <>
      <button onClick={{() => setIsVisible(!isVisible)}}>
        Toggle
      </button>

      <AnimatePresence mode="wait">
        {{isVisible && (
          <motion.div
            key="content"
            initial={{{{ opacity: 0, y: 20 }}}}
            animate={{{{ opacity: 1, y: 0 }}}}
            exit={{{{ opacity: 0, y: -20 }}}}
            transition={{{{ duration: 0.3 }}}}
          >
            {{children}}
          </motion.div>
        )}}
      </AnimatePresence>
    </>
  )
}}
"""

    def _generate_layout(self) -> str:
        """Generate layout animation component."""
        imports = self._get_imports(needs_hooks=True)
        props_interface = self._get_props_interface()

        layout_id = f'layoutId="{self.shared_id}"' if self.shared_id else ""

        return f"""{imports}
{props_interface}
export function {self.name}({{ children }}{': ' + self.name + 'Props' if self.typescript else ''}) {{
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      layout
      {layout_id}
      onClick={{() => setIsExpanded(!isExpanded)}}
      style={{{{
        width: isExpanded ? '400px' : '200px',
        height: isExpanded ? '300px' : '150px',
        borderRadius: '12px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        cursor: 'pointer',
        padding: '20px'
      }}}}
      transition={{{{
        layout: {{{{ duration: 0.3, ease: 'easeInOut' }}}}
      }}}}
    >
      <motion.div layout="position">
        {{children}}
      </motion.div>
    </motion.div>
  )
}}
"""

    def _generate_scroll(self) -> str:
        """Generate scroll-triggered animation."""
        imports = self._get_imports()
        props_interface = self._get_props_interface()
        props_sig = f"({{ children }}: {self.name}Props)" if self.typescript else "({ children })"

        return f"""{imports}
{props_interface}
export function {self.name}{props_sig} {{
  return (
    <motion.div
      initial={{{{ opacity: 0, y: 50 }}}}
      whileInView={{{{ opacity: 1, y: 0 }}}}
      viewport={{{{ once: true, amount: 0.3 }}}}
      transition={{{{ duration: 0.5, ease: 'easeOut' }}}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

    def _generate_spring(self) -> str:
        """Generate spring physics animation."""
        imports = self._get_imports(needs_hooks=True)
        props_interface = self._get_props_interface()

        return f"""{imports}
{props_interface}
export function {self.name}({{ children }}{': ' + self.name + 'Props' if self.typescript else ''}) {{
  const [isActive, setIsActive] = useState(false)

  return (
    <motion.div
      animate={{{{
        scale: isActive ? 1.2 : 1,
        rotate: isActive ? 5 : 0
      }}}}
      transition={{{{
        type: 'spring',
        stiffness: 300,
        damping: 20,
        mass: 1
      }}}}
      onClick={{() => setIsActive(!isActive)}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

    def _generate_stagger(self) -> str:
        """Generate staggered children animation."""
        imports = self._get_imports()
        if self.typescript:
            imports = self._get_imports() + "\nimport type { Variants } from 'framer-motion'"

        variants = "Variants" if self.typescript else ""

        return f"""{imports}

const container{': ' + variants if variants else ''} = {{
  hidden: {{{{ opacity: 0 }}}},
  visible: {{{{
    opacity: 1,
    transition: {{{{
      staggerChildren: 0.1,
      delayChildren: 0.2
    }}}}
  }}}}
}}

const item{': ' + variants if variants else ''} = {{
  hidden: {{{{ opacity: 0, y: 20 }}}},
  visible: {{{{
    opacity: 1,
    y: 0,
    transition: {{{{ duration: 0.5 }}}}
  }}}}
}}

export function {self.name}() {{
  const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']

  return (
    <motion.ul
      variants={{container}}
      initial="hidden"
      animate="visible"
      style={{{{ listStyle: 'none', padding: 0 }}}}
    >
      {{items.map((text, index) => (
        <motion.li
          key={{index}}
          variants={{item}}
          style={{{{
            padding: '20px',
            marginBottom: '10px',
            background: '#f0f0f0',
            borderRadius: '8px'
          }}}}
        >
          {{text}}
        </motion.li>
      ))}}
    </motion.ul>
  )
}}
"""

    def _generate_gesture(self) -> str:
        """Generate combined gesture component."""
        imports = self._get_imports(needs_hooks=True)
        props_interface = self._get_props_interface()

        return f"""{imports}
{props_interface}
export function {self.name}({{ children }}{': ' + self.name + 'Props' if self.typescript else ''}) {{
  const [isDragging, setIsDragging] = useState(false)

  return (
    <motion.div
      drag
      dragConstraints={{{{ left: 0, right: 300, top: 0, bottom: 300 }}}}
      whileHover={{{{ scale: 1.05 }}}}
      whileTap={{{{ scale: 0.95 }}}}
      whileDrag={{{{ scale: 1.1, cursor: 'grabbing' }}}}
      onDragStart={{() => setIsDragging(true)}}
      onDragEnd={{() => setIsDragging(false)}}
      style={{{{
        width: '150px',
        height: '150px',
        background: isDragging ? '#667eea' : '#764ba2',
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'grab',
        userSelect: 'none'
      }}}}
    >
      {{children}}
    </motion.div>
  )
}}
"""

    def _generate_variant(self) -> str:
        """Generate variant-based animation system."""
        imports = self._get_imports(needs_hooks=True)
        if self.typescript:
            imports += "\nimport type { Variants } from 'framer-motion'"

        variants_type = ": Variants" if self.typescript else ""

        return f"""{imports}

const variants{variants_type} = {{
  inactive: {{
    scale: 1,
    backgroundColor: '#cccccc',
    transition: {{{{ duration: 0.3 }}}}
  }},
  active: {{
    scale: 1.1,
    backgroundColor: '#667eea',
    transition: {{{{ type: 'spring', stiffness: 300, damping: 20 }}}}
  }},
  complete: {{
    scale: 1,
    backgroundColor: '#10b981',
    transition: {{{{ duration: 0.3 }}}}
  }}
}}

export function {self.name}() {{
  const [status, setStatus] = useState<'inactive' | 'active' | 'complete'>('inactive')

  const handleClick = () => {{
    if (status === 'inactive') {{
      setStatus('active')
      setTimeout(() => setStatus('complete'), 1000)
    }} else {{
      setStatus('inactive')
    }}
  }}

  return (
    <motion.div
      variants={{variants}}
      animate={{status}}
      onClick={{handleClick}}
      style={{{{
        width: '200px',
        height: '60px',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        color: 'white',
        fontWeight: 'bold'
      }}}}
    >
      {{status.toUpperCase()}}
    </motion.div>
  )
}}
"""

    def _generate_custom(self) -> str:
        """Generate custom template."""
        imports = self._get_imports()
        props_interface = self._get_props_interface()
        props_sig = f"({{ children }}: {self.name}Props)" if self.typescript else "({ children })"

        return f"""{imports}
{props_interface}
export function {self.name}{props_sig} {{
  return (
    <motion.div
      initial={{{{ opacity: 0 }}}}
      animate={{{{ opacity: 1 }}}}
      transition={{{{ duration: 0.5 }}}}
    >
      {{children}}
    </motion.div>
  )
}}
"""


def main():
    parser = argparse.ArgumentParser(
        description='Generate Motion/Framer Motion animation boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--type',
        required=True,
        choices=['hover', 'tap', 'drag', 'exit', 'layout', 'scroll',
                 'spring', 'stagger', 'gesture', 'variant', 'custom'],
        help='Animation type to generate'
    )

    parser.add_argument(
        '--name',
        default='Component',
        help='Component name (default: Component)'
    )

    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--typescript',
        action='store_true',
        help='Generate TypeScript component'
    )

    parser.add_argument(
        '--constraints',
        action='store_true',
        help='Add drag constraints (for drag type)'
    )

    parser.add_argument(
        '--shared-id',
        help='Add layoutId for shared animations'
    )

    parser.add_argument(
        '--spring',
        action='store_true',
        help='Use spring physics for transitions'
    )

    args = parser.parse_args()

    # Generate animation
    generator = MotionAnimationGenerator(
        animation_type=args.type,
        name=args.name,
        typescript=args.typescript,
        constraints=args.constraints,
        shared_id=args.shared_id,
        spring=args.spring,
    )

    try:
        code = generator.generate()

        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"✅ Generated {args.name} component → {args.output}")
        else:
            print(code)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
