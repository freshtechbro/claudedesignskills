// A-Frame Starter Template - Main JavaScript

console.log('A-Frame scene initialized');

// Wait for scene to load
const scene = document.querySelector('a-scene');

scene.addEventListener('loaded', () => {
  console.log('Scene loaded and ready');

  // Get interactive objects
  const box = document.querySelector('#box1');
  const sphere = document.querySelector('#sphere1');
  const cylinder = document.querySelector('#cylinder1');

  // Add click handlers
  box.addEventListener('click', (evt) => {
    console.log('Box clicked at:', evt.detail.intersection.point);
    // Randomize color
    box.setAttribute('color', `#${Math.floor(Math.random()*16777215).toString(16)}`);
  });

  sphere.addEventListener('click', (evt) => {
    console.log('Sphere clicked');
    // Scale animation
    sphere.setAttribute('animation__scale', {
      property: 'scale',
      to: '1.5 1.5 1.5',
      dur: 500,
      dir: 'alternate',
      loop: 1
    });
  });

  cylinder.addEventListener('click', (evt) => {
    console.log('Cylinder clicked');
    // Rotate animation
    const rotation = cylinder.getAttribute('rotation');
    cylinder.setAttribute('animation__spin', {
      property: 'rotation',
      to: `${rotation.x} ${rotation.y + 360} ${rotation.z}`,
      dur: 1000
    });
  });
});

// VR mode events
scene.addEventListener('enter-vr', () => {
  console.log('Entered VR mode');
  // Hide desktop UI if needed
  document.querySelector('#info').style.display = 'none';
});

scene.addEventListener('exit-vr', () => {
  console.log('Exited VR mode');
  // Show desktop UI
  document.querySelector('#info').style.display = 'block';
});

// Keyboard shortcuts
document.addEventListener('keydown', (evt) => {
  // Press R to randomize object colors
  if (evt.key === 'r' || evt.key === 'R') {
    const interactiveObjects = document.querySelectorAll('.interactive');
    interactiveObjects.forEach(el => {
      const randomColor = `#${Math.floor(Math.random()*16777215).toString(16)}`;
      el.setAttribute('color', randomColor);
    });
    console.log('Randomized colors');
  }

  // Press I to toggle inspector (Ctrl+Alt+I also works)
  if ((evt.key === 'i' || evt.key === 'I') && evt.ctrlKey && evt.altKey) {
    // Inspector toggle is built-in to A-Frame
    console.log('Inspector toggled');
  }
});
