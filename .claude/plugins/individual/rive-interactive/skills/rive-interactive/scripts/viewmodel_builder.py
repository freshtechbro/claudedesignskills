#!/usr/bin/env python3
"""
Rive ViewModel Builder

Generate ViewModel property binding code.

Usage:
    ./viewmodel_builder.py  # Interactive mode
"""

print("""
# Rive ViewModel Template

```jsx
import { useRive, useViewModel, useViewModelInstance,
         useViewModelInstanceString, useViewModelInstanceNumber } from 'rive-react';
import { useEffect } from 'react';

export default function ViewModelComponent({ data }) {
  const { rive, RiveComponent } = useRive({
    src: 'animation.riv',
    autoplay: true,
    autoBind: false, // Required for ViewModels
  });

  const viewModel = useViewModel(rive, { useDefault: true });
  const instance = useViewModelInstance(viewModel, { rive });

  const { setValue: setTitle } = useViewModelInstanceString('title', instance);
  const { setValue: setValue } = useViewModelInstanceNumber('value', instance);

  useEffect(() => {
    if (setTitle && setValue) {
      setTitle(data.title);
      setValue(data.value);
    }
  }, [data, setTitle, setValue]);

  return <RiveComponent style={{ width: '600px', height: '400px' }} />;
}
```

Visit https://rive.app/docs/viewmodel for more information.
""")
