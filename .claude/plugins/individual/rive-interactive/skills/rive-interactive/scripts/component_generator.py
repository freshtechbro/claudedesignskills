#!/usr/bin/env python3
"""
Rive Component Generator

Generate Rive React component boilerplate.

Usage:
    ./component_generator.py  # Interactive mode
"""

print("""
# Rive Component Template

```jsx
import { useRive, useStateMachineInput } from 'rive-react';

export default function RiveComponent() {
  const { rive, RiveComponent } = useRive({
    src: 'animation.riv',
    stateMachines: 'State Machine 1',
    autoplay: true,
  });

  const input = useStateMachineInput(
    rive,
    'State Machine 1',
    'inputName',
    false
  );

  return (
    <RiveComponent style={{ width: '400px', height: '400px' }} />
  );
}
```

Visit https://rive.app/docs for more information.
""")
