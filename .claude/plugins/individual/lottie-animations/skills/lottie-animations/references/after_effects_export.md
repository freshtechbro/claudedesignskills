# After Effects to Lottie Export Guide

Complete guide for exporting Lottie animations from After Effects using the Bodymovin plugin.

## Prerequisites

1. **Adobe After Effects** (CC 2015 or later)
2. **Bodymovin Plugin** - Install from:
   - **Recommended:** AEsc scripts panel (Extension Manager)
   - Manual: https://aescripts.com/bodymovin/
   - LottieFiles plugin: https://lottiefiles.com/plugins/after-effects

## Installation

### Method 1: ZXP Installer (Recommended)

1. Download ZXP Installer: https://aescripts.com/learn/zxp-installer/
2. Download Bodymovin ZXP file
3. Drag ZXP file to ZXP Installer
4. Restart After Effects
5. Open Window → Extensions → Bodymovin

### Method 2: Manual Installation

1. Download Bodymovin
2. Extract to:
   - **Mac:** `/Applications/Adobe After Effects [version]/Scripts/ScriptUI Panels/`
   - **Windows:** `C:\Program Files\Adobe\Adobe After Effects [version]\Support Files\Scripts\ScriptUI Panels\`
3. Restart After Effects

## Export Settings

### Basic Export

1. Open Window → Extensions → Bodymovin
2. Select composition(s) to export
3. Click "Settings" icon (gear)
4. Configure options (see below)
5. Choose destination folder
6. Click "Render"

### Recommended Settings for Web

**Essential:**
- ✅ **Glyphs** - Convert text to shapes (reduces file size)
- ✅ **Hidden** - Skip hidden layers
- ✅ **Skip images that aren't used**
- ✅ **Compress JSON** - Minify output (smaller file)
- ⬜ **Export Mode: Demo** (uncheck for production)

**Advanced:**
- **Export Format:** JSON or dotLottie (.lottie)
- **dotLottie:** Recommended for production (90% smaller)
- **Segments:** Export specific frame ranges
- **Image Quality:** 80% (balance size vs quality)

### File Size Optimization Settings

```
✅ Glyphs (text as shapes)
✅ Compress JSON
✅ Skip images that aren't used
✅ Merge Paths (when possible)
⬜ Pretty Print JSON (development only)
⬜ Include in JSON (embed images - increases size)
```

**Expected File Sizes:**
- Simple icon animation: 5-20 KB
- Complex character animation: 50-150 KB
- Heavy illustration animation: 150-500 KB
- **If >500 KB:** Optimize composition (see below)

## Supported Features

### ✅ Fully Supported

**Shapes:**
- Shape layers (rect, ellipse, polygon, star)
- Paths and bezier curves
- Stroke and fill
- Trim paths
- Merge paths
- Repeaters

**Transforms:**
- Position, scale, rotation, opacity
- Anchor points
- Parenting

**Effects:**
- Stroke (via shape layers)
- Fill (via shape layers)
- Trim paths
- Merge paths

**Masks:**
- Shape masks
- Alpha mattes
- Luma mattes (partial)

**Text:**
- As glyphs (converted to shapes)
- Character animation (requires glyphs)

### ⚠️ Partial Support

**Expressions:**
- Simple expressions work
- Complex expressions may fail
- Test thoroughly after export

**Blending Modes:**
- Limited support
- Normal, Add, Multiply work best
- Others may render incorrectly

**Track Mattes:**
- Alpha mattes: Good support
- Luma mattes: Limited support
- Inverted mattes: May fail

### ❌ Not Supported

**Layer Effects:**
- Drop Shadow → Use shape layer shadow
- Glow → Use shape layer glow
- Bevel & Emboss → Pre-render as image
- All built-in effects → Convert to shapes

**3D Layers:**
- 3D transforms
- Cameras (except 2D camera moves)
- Lights

**Advanced:**
- Adjustment layers
- Time remapping
- Frame blending
- Motion blur (partial)
- Gradient strokes (use solid color)

## Optimization Techniques

### 1. Composition Setup

**Before Animating:**
- Work at 1920x1080 or smaller
- Use round numbers for dimensions
- 30 fps or 60 fps (avoid 23.976, 29.97)
- Keep composition under 5 seconds when possible

**Comp Settings:**
```
Width: 1920px (or target size)
Height: 1080px
Frame Rate: 30 fps
Duration: 2-5 seconds
```

### 2. Shape Layer Optimization

**DO:**
```
✅ Use Shape Layers (not vector layers from AI)
✅ Combine shapes with Merge Paths
✅ Use simple gradients (2-3 colors)
✅ Minimize anchor points (simplify paths)
✅ Use solid fills over gradients when possible
```

**DON'T:**
```
❌ Import AI files directly (convert to shapes)
❌ Use too many shapes (>50 layers = slow)
❌ Animate every property (only what's needed)
❌ Use gradient strokes (solid only)
```

### 3. Image Optimization

**Embedded Images:**
- Resize to actual displayed size
- Use JPG for photos (not PNG)
- Compress before import (TinyPNG)
- Avoid embedding if possible

**Alternative:**
- Use shape layers instead
- Pre-render complex elements
- Load images separately in code

### 4. Text Optimization

**Recommended Approach:**
```
1. Create text layer
2. Enable "Glyphs" in Bodymovin settings
3. Text converts to shapes automatically
```

**Manual Alternative:**
```
1. Select text layer
2. Right-click → Create Shapes from Text
3. Delete original text layer
4. Animate shape layers
```

**Benefits:**
- No font loading required
- Smaller file size
- Guaranteed consistent rendering

### 5. Animation Optimization

**Keyframe Reduction:**
```javascript
// After Effects: Select keyframes
// Right-click → Keyframe Assistant → Reduce Keys
// Threshold: 0.5-1.0 pixels
```

**Simplify Paths:**
```javascript
// Illustrator/After Effects
// Object → Path → Simplify
// Target: 85-90% of original points
```

**Limit Properties:**
```
Only animate:
  Position, Scale, Rotation, Opacity
  (Most performant)

Avoid animating:
  Anchor Point, Shape Path
  (More expensive)
```

## Common Export Issues

### Issue 1: Huge File Size (>500 KB)

**Causes:**
- Embedded images
- Too many keyframes
- Complex paths
- Text not converted to glyphs

**Solutions:**
```
1. Enable "Glyphs" setting
2. Enable "Skip images that aren't used"
3. Reduce keyframes (Keyframe Assistant → Reduce Keys)
4. Simplify paths in Illustrator
5. Remove unused layers
6. Export as dotLottie format
```

### Issue 2: Animation Doesn't Match Preview

**Causes:**
- Unsupported features used
- Expression errors
- Blending mode issues

**Solutions:**
```
1. Check Bodymovin console for warnings
2. Replace unsupported features
3. Simplify expressions
4. Use Normal blending mode
5. Test export immediately
```

### Issue 3: Text Rendering Incorrectly

**Causes:**
- Font not supported
- Glyphs not enabled
- Special characters

**Solutions:**
```
1. Enable "Glyphs" in Bodymovin settings
2. OR manually: Create Shapes from Text
3. Avoid special Unicode characters
4. Use web-safe fonts if not using glyphs
```

### Issue 4: Colors Look Different

**Causes:**
- Color space mismatch
- Blending mode issues
- Opacity calculation differences

**Solutions:**
```
1. Work in sRGB color space
2. Use Normal blending mode
3. Check opacity values (0-100%)
4. Avoid nested transparency
```

## Testing Workflow

### 1. Export & Preview

```bash
1. Export from After Effects
2. Preview on LottieFiles:
   https://lottiefiles.com/preview
3. Check file size (aim for <100 KB)
4. Test on target devices
```

### 2. Integration Testing

```javascript
// Quick HTML test
<!DOCTYPE html>
<html>
<body>
  <div id="lottie"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
  <script>
    lottie.loadAnimation({
      container: document.getElementById('lottie'),
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: 'animation.json'
    });
  </script>
</body>
</html>
```

### 3. Performance Testing

```javascript
// Monitor FPS
const animation = lottie.loadAnimation({...});

let lastTime = performance.now();
let frameCount = 0;

animation.addEventListener('enterFrame', () => {
  frameCount++;
  const currentTime = performance.now();
  if (currentTime - lastTime >= 1000) {
    console.log('FPS:', frameCount);
    frameCount = 0;
    lastTime = currentTime;
  }
});

// Target: 60 FPS on desktop, 30 FPS on mobile
```

## Best Practices

### Pre-Export Checklist

```
☐ Composition is 1920x1080 or smaller
☐ Frame rate is 30 or 60 fps
☐ Duration is under 10 seconds
☐ All layers are named descriptively
☐ Unused layers are deleted
☐ Text is converted to shapes/glyphs enabled
☐ Images are optimized/removed
☐ No unsupported effects used
☐ Tested in Bodymovin preview
☐ File size is under 100 KB (target)
```

### Export Settings Checklist

```
☐ Format: JSON or dotLottie (.lottie)
☐ Glyphs: Enabled
☐ Hidden: Checked
☐ Skip unused images: Checked
☐ Compress JSON: Enabled
☐ Pretty Print: Disabled (production)
☐ Image Quality: 80%
☐ Export Mode: Standard (not Demo)
```

### Post-Export Checklist

```
☐ Preview on LottieFiles.com
☐ Check file size (<100 KB ideal)
☐ Test in target browser/device
☐ Verify animation timing
☐ Check colors/rendering
☐ Test playback controls
☐ Verify loop behavior
☐ Test on mobile devices
```

## Resources

- **LottieFiles Preview:** https://lottiefiles.com/preview
- **Supported Features:** https://airbnb.io/lottie/#/supported-features
- **Bodymovin Plugin:** https://aescripts.com/bodymovin/
- **LottieFiles Plugin:** https://lottiefiles.com/plugins/after-effects
- **File Size Optimizer:** https://lottiefiles.com/tools/lottie-editor

## Troubleshooting

### Bodymovin Panel Not Showing

```
1. Check installation path is correct
2. Restart After Effects completely
3. Enable "Allow Scripts to Write Files"
   (Edit → Preferences → Scripting & Expressions)
4. Reinstall using ZXP Installer
```

### Export Fails/Crashes

```
1. Update to latest After Effects version
2. Update Bodymovin plugin
3. Simplify composition (remove complex features)
4. Export smaller sections separately
5. Check After Effects error log
```

### Animation Too Large

```
1. Export as dotLottie (90% smaller)
2. Reduce composition dimensions
3. Simplify paths (fewer anchor points)
4. Remove embedded images
5. Reduce keyframe count
6. Use solid colors over gradients
```
