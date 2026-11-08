# Blender Web Pipeline Assets

Template files and resources for Blender to web workflows.

## Included Assets

### export_template.blend
Pre-configured Blender template with:
- Optimized export settings
- PBR material setup
- LOD examples
- Proper UV unwrapping

### shader_library/
Collection of web-optimized PBR shaders:
- Basic PBR material
- Emissive material
- Transparent material
- Metallic material

## Usage

1. Open `export_template.blend` in Blender
2. Replace placeholder geometry with your models
3. Use pre-configured materials from shader_library
4. Export using File → Export → glTF 2.0 (.glb)
5. Test in web viewer before deploying

## Quick Start

```bash
# Open template
blender export_template.blend

# Or use as base for new projects
blender --factory-startup export_template.blend --save-as mynewproject.blend
```
