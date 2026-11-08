# Rive Interactive - Assets

Starter templates and examples for Rive + React integration.

## Quick Start

```bash
npm install rive-react
```

## Basic Usage

```jsx
import Rive from 'rive-react';

<Rive
  src="animation.riv"
  stateMachines="State Machine 1"
  style={{ width: '400px', height: '400px' }}
/>
```

## State Machine Example

```jsx
import { useRive, useStateMachineInput } from 'rive-react';

export default function InteractiveButton() {
  const { rive, RiveComponent } = useRive({
    src: 'button.riv',
    stateMachines: 'Button State Machine',
    autoplay: true,
  });

  const hoverInput = useStateMachineInput(rive, 'Button State Machine', 'isHovered', false);

  return (
    <div
      onMouseEnter={() => hoverInput && (hoverInput.value = true)}
      onMouseLeave={() => hoverInput && (hoverInput.value = false)}
    >
      <RiveComponent style={{ width: '200px', height: '100px' }} />
    </div>
  );
}
```

## ViewModel Example

```jsx
import { useRive, useViewModel, useViewModelInstance,
         useViewModelInstanceString } from 'rive-react';
import { useEffect } from 'react';

export default function Dashboard({ title }) {
  const { rive, RiveComponent } = useRive({
    src: 'dashboard.riv',
    autoplay: true,
    autoBind: false,
  });

  const viewModel = useViewModel(rive, { useDefault: true });
  const instance = useViewModelInstance(viewModel, { rive });
  const { setValue: setTitle } = useViewModelInstanceString('title', instance);

  useEffect(() => {
    if (setTitle) setTitle(title);
  }, [title, setTitle]);

  return <RiveComponent style={{ width: '800px', height: '600px' }} />;
}
```

## Resources

- [Rive Documentation](https://rive.app/docs)
- [React Rive GitHub](https://github.com/rive-app/rive-react)
- [Rive Community](https://rive.app/community)
- [State Machine Guide](https://rive.app/docs/state-machine)
