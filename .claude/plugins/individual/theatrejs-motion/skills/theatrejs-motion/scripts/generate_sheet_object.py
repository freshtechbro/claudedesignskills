#!/usr/bin/env python3
"""
Theatre.js Sheet Object Generator

Builds a typed `sheet.object(...)` declaration plus an `onValuesChange` handler
from a compact prop spec, so animatable objects can be scaffolded quickly.

Prop spec syntax (comma-separated name:type[:default] tokens):
    num     -> types.number (default 0, range [-100, 100])
    bool    -> types.boolean (default true)
    str     -> types.string (default "")
    color   -> types.rgba (default opaque white)

Usage:
    ./generate_sheet_object.py --name Logo --props "x:num,y:num,opacity:num:1,visible:bool"
    ./generate_sheet_object.py --name Panel --props "tint:color,label:str" --sheet Intro
    ./generate_sheet_object.py            # interactive mode

Dependencies: Python 3 standard library only.
"""

import argparse
import sys


def _number(default: str) -> str:
    val = default if default else '0'
    return f'types.number({val}, {{ range: [-100, 100] }})'


def _boolean(default: str) -> str:
    val = default if default else 'true'
    return f'types.boolean({val})'


def _string(default: str) -> str:
    val = default if default else ''
    return f"types.string('{val}')"


def _color(_default: str) -> str:
    return 'types.rgba({ r: 1, g: 1, b: 1, a: 1 })'


BUILDERS = {'num': _number, 'bool': _boolean, 'str': _string, 'color': _color}


def parse_props(spec: str):
    """Parse 'name:type[:default]' tokens into (name, type, default) tuples."""
    props = []
    for token in spec.split(','):
        token = token.strip()
        if not token:
            continue
        parts = token.split(':')
        name = parts[0].strip()
        ptype = parts[1].strip() if len(parts) > 1 else 'num'
        default = parts[2].strip() if len(parts) > 2 else ''
        if not name:
            raise ValueError(f"empty property name in token '{token}'")
        if ptype not in BUILDERS:
            raise ValueError(
                f"unknown type '{ptype}' for '{name}' (use: {', '.join(BUILDERS)})"
            )
        props.append((name, ptype, default))
    if not props:
        raise ValueError('no valid properties parsed')
    return props


def render(obj_name: str, sheet: str, props) -> str:
    prop_lines = '\n'.join(
        f'  {name}: {BUILDERS[ptype](default)},' for name, ptype, default in props
    )
    # onValuesChange destructures numeric/bool/string props for direct use
    destructure = ', '.join(name for name, _, _ in props)
    var = obj_name[0].lower() + obj_name[1:] + 'Obj'
    return f'''const {var} = {sheet}.object('{obj_name}', {{
{prop_lines}
}})

{var}.onValuesChange(({{ {destructure} }}) => {{
  // TODO: apply animated values to your target
  // example: target.style.opacity = opacity
}})
'''


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate a Theatre.js sheet object.')
    parser.add_argument('--name', help='Sheet object name (e.g. Logo)')
    parser.add_argument('--props', help='Comma-separated name:type[:default] tokens')
    parser.add_argument('--sheet', default='sheet', help='Sheet variable name')
    parser.add_argument('--output', help='Write to file instead of stdout')
    args = parser.parse_args()

    name = args.name
    props_spec = args.props

    if not name:
        try:
            name = input('Sheet object name [Logo]: ').strip() or 'Logo'
        except (EOFError, KeyboardInterrupt):
            print()
            return 1
    if not props_spec:
        try:
            props_spec = input(
                'Props (name:type[:default], e.g. x:num,opacity:num:1): '
            ).strip() or 'x:num,y:num,opacity:num:1'
        except (EOFError, KeyboardInterrupt):
            print()
            return 1

    try:
        props = parse_props(props_spec)
    except ValueError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1

    code = render(name, args.sheet, props)

    if args.output:
        try:
            with open(args.output, 'w') as fh:
                fh.write(code)
            print(f'Wrote sheet object to {args.output}')
        except OSError as exc:
            print(f'Error writing file: {exc}', file=sys.stderr)
            return 1
    else:
        print(code)
    return 0


if __name__ == '__main__':
    sys.exit(main())
