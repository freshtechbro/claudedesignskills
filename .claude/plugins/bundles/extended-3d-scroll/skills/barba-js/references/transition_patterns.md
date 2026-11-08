# Barba.js Transition Patterns Library

Copy-paste transition implementations for common page transition effects.

## Table of Contents

- [Fade Transitions](#fade-transitions)
- [Slide Transitions](#slide-transitions)
- [Scale Transitions](#scale-transitions)
- [Creative Transitions](#creative-transitions)
- [Conditional Transitions](#conditional-transitions)
- [Production Examples](#production-examples)

---

## Fade Transitions

### Simple Fade

Classic fade out → fade in:

```javascript
{
  name: 'fade',

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    });
  },

  async enter({ next }) {
    gsap.set(next.container, { opacity: 0 });

    await gsap.to(next.container, {
      opacity: 1,
      duration: 0.5,
      ease: 'power2.inOut'
    });
  }
}
```

### Crossfade (Sync)

Both pages fade simultaneously:

```javascript
{
  name: 'crossfade',
  sync: true,

  leave({ current }) {
    return gsap.to(current.container, {
      opacity: 0,
      duration: 0.8,
      ease: 'power2.inOut'
    });
  },

  enter({ next }) {
    return gsap.from(next.container, {
      opacity: 0,
      duration: 0.8,
      ease: 'power2.inOut'
    });
  }
}
```

### Fade with Scale

Fade + subtle zoom:

```javascript
{
  name: 'fade-scale',

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      scale: 0.95,
      duration: 0.5,
      ease: 'power2.in'
    });
  },

  async enter({ next }) {
    await gsap.fromTo(next.container,
      {
        opacity: 0,
        scale: 1.05
      },
      {
        opacity: 1,
        scale: 1,
        duration: 0.6,
        ease: 'power2.out'
      }
    );
  }
}
```

---

## Slide Transitions

### Horizontal Slide

Old page slides left, new page slides in from right:

```javascript
{
  name: 'slide-horizontal',
  sync: true,

  leave({ current }) {
    return gsap.to(current.container, {
      x: '-100%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  },

  enter({ next }) {
    gsap.set(next.container, { x: '100%' });

    return gsap.to(next.container, {
      x: '0%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  }
}
```

### Vertical Slide

Old page slides up, new page slides in from bottom:

```javascript
{
  name: 'slide-vertical',
  sync: true,

  leave({ current }) {
    return gsap.to(current.container, {
      y: '-100%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  },

  enter({ next }) {
    gsap.set(next.container, { y: '100%' });

    return gsap.to(next.container, {
      y: '0%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  }
}
```

### Direction-Based Slide

Slide direction based on browser history:

```javascript
{
  name: 'slide-smart',
  sync: true,

  leave({ current }) {
    const direction = barba.history.direction;
    const isBack = direction === 'back';

    return gsap.to(current.container, {
      x: isBack ? '100%' : '-100%',
      duration: 0.6,
      ease: 'power2.inOut'
    });
  },

  enter({ next }) {
    const direction = barba.history.direction;
    const isBack = direction === 'back';

    gsap.set(next.container, {
      x: isBack ? '-100%' : '100%'
    });

    return gsap.to(next.container, {
      x: '0%',
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}
```

**CSS Required** (for sync mode):
```css
[data-barba="wrapper"] {
  position: relative;
  overflow: hidden;
}

[data-barba="container"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}
```

---

## Scale Transitions

### Zoom Out → Zoom In

```javascript
{
  name: 'zoom',

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      scale: 0.8,
      duration: 0.5,
      ease: 'power2.in'
    });
  },

  async enter({ next }) {
    await gsap.fromTo(next.container,
      {
        opacity: 0,
        scale: 1.2
      },
      {
        opacity: 1,
        scale: 1,
        duration: 0.6,
        ease: 'power2.out'
      }
    );
  }
}
```

### Rotate Zoom

3D rotation with zoom:

```javascript
{
  name: 'rotate-zoom',

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      scale: 0.9,
      rotationY: 15,
      duration: 0.6,
      ease: 'power2.in'
    });
  },

  async enter({ next }) {
    await gsap.fromTo(next.container,
      {
        opacity: 0,
        scale: 0.9,
        rotationY: -15
      },
      {
        opacity: 1,
        scale: 1,
        rotationY: 0,
        duration: 0.7,
        ease: 'power2.out'
      }
    );
  }
}
```

**CSS Required**:
```css
[data-barba="wrapper"] {
  perspective: 1000px;
}
```

---

## Creative Transitions

### Curtain Effect

Animated overlay curtain:

```javascript
{
  name: 'curtain',

  async leave({ current }) {
    const curtain = document.querySelector('.transition-curtain');

    // Bring curtain down
    await gsap.fromTo(curtain,
      { yPercent: -100 },
      {
        yPercent: 0,
        duration: 0.6,
        ease: 'power2.inOut'
      }
    );
  },

  async enter({ next }) {
    const curtain = document.querySelector('.transition-curtain');

    // Lift curtain up
    await gsap.to(curtain, {
      yPercent: 100,
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}
```

**HTML Required**:
```html
<div class="transition-curtain"></div>
```

**CSS Required**:
```css
.transition-curtain {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 9999;
  pointer-events: none;
  transform: translateY(-100%);
}
```

### Wipe Effect

Diagonal wipe transition:

```javascript
{
  name: 'wipe',

  async leave({ current }) {
    const wipe = document.querySelector('.transition-wipe');

    await gsap.fromTo(wipe,
      {
        xPercent: -100,
        skewX: -10
      },
      {
        xPercent: 0,
        skewX: 0,
        duration: 0.8,
        ease: 'power2.inOut'
      }
    );
  },

  async enter({ next }) {
    const wipe = document.querySelector('.transition-wipe');

    gsap.set(next.container, { opacity: 1 });

    await gsap.to(wipe, {
      xPercent: 100,
      skewX: 10,
      duration: 0.8,
      ease: 'power2.inOut'
    });
  }
}
```

**HTML Required**:
```html
<div class="transition-wipe"></div>
```

**CSS Required**:
```css
.transition-wipe {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
  z-index: 9999;
  pointer-events: none;
  transform: translateX(-100%);
}
```

### Staggered Elements

Elements animate out/in individually:

```javascript
{
  name: 'stagger',

  async leave({ current }) {
    const tl = gsap.timeline();

    tl.to(current.container.querySelectorAll('.stagger-item'), {
      y: -50,
      opacity: 0,
      duration: 0.5,
      stagger: 0.05,
      ease: 'power2.in'
    })
    .to(current.container, {
      opacity: 0,
      duration: 0.3
    }, '-=0.2');

    await tl.play();
  },

  async enter({ next }) {
    const tl = gsap.timeline();

    gsap.set(next.container.querySelectorAll('.stagger-item'), {
      y: 50,
      opacity: 0
    });

    tl.to(next.container.querySelectorAll('.stagger-item'), {
      y: 0,
      opacity: 1,
      duration: 0.6,
      stagger: 0.05,
      ease: 'power2.out'
    });

    await tl.play();
  }
}
```

**HTML Classes Required**:
```html
<div data-barba="container">
  <h1 class="stagger-item">Title</h1>
  <p class="stagger-item">Paragraph 1</p>
  <p class="stagger-item">Paragraph 2</p>
  <div class="stagger-item">Content</div>
</div>
```

---

## Conditional Transitions

### Different Transition Per Namespace

```javascript
barba.init({
  transitions: [
    // From home: fade
    {
      name: 'from-home',
      from: { namespace: 'home' },

      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          duration: 0.5
        });
      },

      async enter({ next }) {
        await gsap.from(next.container, {
          opacity: 0,
          duration: 0.5
        });
      }
    },

    // To/from product: slide
    {
      name: 'product-transition',
      from: { namespace: 'product' },
      to: { namespace: 'product' },
      sync: true,

      leave({ current }) {
        return gsap.to(current.container, {
          x: '-100%',
          duration: 0.6
        });
      },

      enter({ next }) {
        gsap.set(next.container, { x: '100%' });
        return gsap.to(next.container, {
          x: '0%',
          duration: 0.6
        });
      }
    },

    // Default: crossfade
    {
      name: 'default',
      sync: true,

      leave({ current }) {
        return gsap.to(current.container, {
          opacity: 0,
          duration: 0.4
        });
      },

      enter({ next }) {
        return gsap.from(next.container, {
          opacity: 0,
          duration: 0.4
        });
      }
    }
  ]
});
```

### Custom Rule Based on Data Attribute

```javascript
{
  name: 'article-to-article',
  custom: ({ current, next }) => {
    // Check if both pages have data-article attribute
    return current.container.dataset.article && next.container.dataset.article;
  },

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      scale: 0.95,
      duration: 0.3
    });
  },

  async enter({ next }) {
    await gsap.fromTo(next.container,
      { opacity: 0, scale: 1.05 },
      { opacity: 1, scale: 1, duration: 0.4 }
    );
  }
}
```

---

## Production Examples

### E-commerce Product Pages

Fast transitions between products, slower elsewhere:

```javascript
barba.init({
  transitions: [
    // Product to product: fast slide
    {
      name: 'product-to-product',
      from: { namespace: 'product' },
      to: { namespace: 'product' },
      sync: true,

      leave({ current }) {
        return gsap.to(current.container, {
          x: '-50%',
          opacity: 0,
          duration: 0.4,
          ease: 'power2.inOut'
        });
      },

      enter({ next }) {
        gsap.set(next.container, { x: '50%', opacity: 0 });

        return gsap.to(next.container, {
          x: '0%',
          opacity: 1,
          duration: 0.4,
          ease: 'power2.inOut'
        });
      }
    },

    // Default: elegant fade
    {
      name: 'default',

      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          y: -30,
          duration: 0.6,
          ease: 'power2.in'
        });
      },

      async enter({ next }) {
        await gsap.fromTo(next.container,
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }
        );
      }
    }
  ]
});
```

### Portfolio with Loading Indicator

```javascript
barba.init({
  transitions: [{
    name: 'portfolio',

    async leave({ current }) {
      const loader = document.querySelector('.page-loader');

      // Fade out content
      await gsap.to(current.container, {
        opacity: 0,
        duration: 0.4
      });

      // Show loader
      gsap.to(loader, {
        opacity: 1,
        duration: 0.3
      });
    },

    async enter({ next }) {
      const loader = document.querySelector('.page-loader');

      // Hide loader
      await gsap.to(loader, {
        opacity: 0,
        duration: 0.3
      });

      // Fade in content
      await gsap.from(next.container, {
        opacity: 0,
        duration: 0.5
      });
    }
  }]
});
```

**HTML**:
```html
<div class="page-loader">Loading...</div>
```

**CSS**:
```css
.page-loader {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  opacity: 0;
  z-index: 9998;
  pointer-events: none;
}
```

### Blog with Staggered Content

```javascript
barba.init({
  transitions: [{
    name: 'blog',

    async leave({ current }) {
      const tl = gsap.timeline();

      tl.to(current.container.querySelector('.post-header'), {
        y: -50,
        opacity: 0,
        duration: 0.4
      })
      .to(current.container.querySelectorAll('.post-content > *'), {
        y: -30,
        opacity: 0,
        duration: 0.3,
        stagger: 0.03
      }, '-=0.3')
      .to(current.container, {
        opacity: 0,
        duration: 0.2
      });

      await tl.play();
    },

    async enter({ next }) {
      const tl = gsap.timeline();

      gsap.set(next.container.querySelector('.post-header'), {
        y: 50,
        opacity: 0
      });
      gsap.set(next.container.querySelectorAll('.post-content > *'), {
        y: 30,
        opacity: 0
      });

      tl.to(next.container.querySelector('.post-header'), {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: 'power3.out'
      })
      .to(next.container.querySelectorAll('.post-content > *'), {
        y: 0,
        opacity: 1,
        duration: 0.5,
        stagger: 0.05,
        ease: 'power2.out'
      }, '-=0.4');

      await tl.play();
    }
  }]
});
```

### Agency Site with Parallax Layers

```javascript
barba.init({
  transitions: [{
    name: 'parallax',
    sync: true,

    async leave({ current }) {
      const tl = gsap.timeline();

      // Parallax effect - different speeds
      tl.to(current.container.querySelector('.layer-bg'), {
        y: -50,
        opacity: 0,
        duration: 0.8
      }, 0)
      .to(current.container.querySelector('.layer-mid'), {
        y: -100,
        opacity: 0,
        duration: 0.8
      }, 0)
      .to(current.container.querySelector('.layer-front'), {
        y: -150,
        opacity: 0,
        duration: 0.8
      }, 0);

      await tl.play();
    },

    async enter({ next }) {
      const tl = gsap.timeline();

      gsap.set(next.container.querySelectorAll('[class^="layer-"]'), {
        opacity: 0
      });

      tl.from(next.container.querySelector('.layer-bg'), {
        y: 50,
        opacity: 0,
        duration: 0.8
      }, 0)
      .from(next.container.querySelector('.layer-mid'), {
        y: 100,
        opacity: 0,
        duration: 0.8
      }, 0)
      .from(next.container.querySelector('.layer-front'), {
        y: 150,
        opacity: 0,
        duration: 0.8
      }, 0);

      await tl.play();
    }
  }]
});
```

### SaaS Dashboard with Minimal Transition

Fast, subtle transitions for app-like feel:

```javascript
barba.init({
  transitions: [{
    name: 'dashboard',

    async leave({ current }) {
      await gsap.to(current.container, {
        opacity: 0,
        duration: 0.2,
        ease: 'power1.inOut'
      });
    },

    async enter({ next }) {
      gsap.set(next.container, { opacity: 0 });

      await gsap.to(next.container, {
        opacity: 1,
        duration: 0.2,
        ease: 'power1.inOut'
      });
    }
  }]
});
```

---

## Complete Starter Template

Full implementation with multiple transitions:

```javascript
import barba from '@barba/core';
import gsap from 'gsap';

barba.init({
  transitions: [
    // Initial page load
    {
      name: 'initial-load',
      once: async ({ next }) => {
        const loader = document.querySelector('.page-loader');

        await gsap.to(loader, {
          opacity: 0,
          duration: 0.5,
          delay: 0.5
        });

        gsap.set(loader, { display: 'none' });

        await gsap.from(next.container, {
          opacity: 0,
          y: 50,
          duration: 0.8,
          ease: 'power2.out'
        });
      }
    },

    // Same namespace: fast transition
    {
      name: 'same-namespace',
      custom: ({ current, next }) => current.namespace === next.namespace,

      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          duration: 0.3
        });
      },

      async enter({ next }) {
        await gsap.from(next.container, {
          opacity: 0,
          duration: 0.3
        });
      }
    },

    // Default: elegant fade
    {
      name: 'default',

      async leave({ current }) {
        await gsap.to(current.container, {
          opacity: 0,
          y: -30,
          duration: 0.5,
          ease: 'power2.in'
        });
      },

      async enter({ next }) {
        await gsap.fromTo(next.container,
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }
        );
      }
    }
  ]
});

// Global hooks
barba.hooks.beforeEnter(() => {
  window.scrollTo(0, 0);
});

barba.hooks.after(({ next }) => {
  // Analytics
  if (typeof gtag !== 'undefined') {
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: next.url.path
    });
  }

  // Re-initialize scripts
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }
});
```
