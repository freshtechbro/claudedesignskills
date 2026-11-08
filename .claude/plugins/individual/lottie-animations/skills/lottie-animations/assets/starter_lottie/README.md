# Lottie Starter Template

Complete React + Vite starter template with Lottie examples.

## Features

- React 18+ with TypeScript support
- Vite for fast development
- DotLottie React integration
- Example animations with controls
- Responsive design
- Production-ready configuration

## Installation

```bash
# Install dependencies
npm install

# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
starter_lottie/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── App.css
│   └── components/
│       ├── BasicAnimation.jsx
│       └── InteractiveAnimation.jsx
├── public/
│   └── animations/
│       └── example.lottie
└── README.md
```

## Usage Examples

### Basic Animation

```jsx
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

<DotLottieReact
  src="/animations/example.lottie"
  loop
  autoplay
  style={{ height: 400 }}
/>
```

### Interactive Animation

```jsx
const [dotLottie, setDotLottie] = useState(null);

<DotLottieReact
  src="/animations/example.lottie"
  loop
  autoplay={false}
  dotLottieRefCallback={setDotLottie}
/>

<button onClick={() => dotLottie?.play()}>Play</button>
```

## Configuration

### vite.config.js

Optimized for production builds with:
- Code splitting
- Asset optimization
- Gzip compression support

### package.json

Includes essential dependencies:
- `@lottiefiles/dotlottie-react`
- `react` and `react-dom`
- Development tools

## Deployment

Build optimized bundle:

```bash
npm run build
```

Output in `dist/` folder ready for deployment to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Any static hosting

## License

MIT
