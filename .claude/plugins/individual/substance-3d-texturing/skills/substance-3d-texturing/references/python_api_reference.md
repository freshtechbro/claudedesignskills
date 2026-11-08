# Substance 3D Painter Python API Reference

Complete reference for automating Substance 3D Painter workflows with Python.

## API Overview

The Substance 3D Painter Python API provides programmatic access to:
- **Export System** - Texture export configuration and execution
- **Project Management** - Open, save, close projects
- **Texture Sets** - Access and modify texture sets
- **Resource Management** - Access materials, brushes, presets
- **Event System** - React to application events
- **UI System** - Add custom menu items and dialogs

## Core Modules

### substance_painter.export

Texture export functionality.

#### Functions

**export_project_textures(json_config: dict) → ExportResult**

Exports project textures according to JSON configuration.

**Parameters:**
- `json_config` (dict) - Export configuration object

**Returns:**
- `ExportResult` with status, message, and list of exported files

**Raises:**
- `ProjectError` - No project is open
- `ValueError` - Invalid configuration

**Example:**
```python
import substance_painter.export

config = {
    "exportPath": "C:/export",
    "defaultExportPreset": "starter_assets://PBR Metallic Roughness",
    "exportList": [{"rootPath": "TextureSetName"}],
    "exportParameters": [{
        "parameters": {
            "fileFormat": "png",
            "bitDepth": "8",
            "sizeLog2": 10
        }
    }]
}

result = substance_painter.export.export_project_textures(config)

if result.status == substance_painter.export.ExportStatus.Success:
    print(f"Exported {len(result.textures)} texture sets")
```

---

**list_project_textures(json_config: dict) → Dict[Tuple[str, str], List[str]]**

Lists textures that would be exported without actually exporting.

**Parameters:**
- `json_config` (dict) - Export configuration

**Returns:**
- Dictionary mapping (texture_set, stack) to list of file paths

**Example:**
```python
texture_list = substance_painter.export.list_project_textures(config)

for stack, files in texture_list.items():
    print(f"Stack {stack}:")
    for file in files:
        print(f"  - {file}")
```

#### Classes

**ExportStatus (Enum)**

Export operation status codes:
- `Success` - Export completed successfully
- `Error` - Export failed

**ExportResult**

Result object returned by `export_project_textures()`.

**Attributes:**
- `status` (ExportStatus) - Status code
- `message` (str) - Human-readable status message
- `textures` (Dict[Tuple[str, str], List[str]]) - Exported files grouped by stack

#### Events

**ExportTexturesAboutToStart**

Triggered before export begins.

**Attributes:**
- `textures` (Dict[Tuple[str, str], List[str]]) - Files to be exported

**Example:**
```python
import substance_painter.event

def on_export_start(event):
    print(f"Exporting {len(event.textures)} texture sets")

substance_painter.event.DISPATCHER.connect(
    substance_painter.event.ExportTexturesAboutToStart,
    on_export_start
)
```

**ExportTexturesEnded**

Triggered after export completes.

**Attributes:**
- `status` (ExportStatus) - Export status
- `message` (str) - Status message
- `textures` (Dict[Tuple[str, str], List[str]]) - Exported files

### substance_painter.project

Project management operations.

#### Functions

**is_open() → bool**

Check if a project is currently open.

**Example:**
```python
if substance_painter.project.is_open():
    print("Project is open")
```

---

**open(file_path: str) → None**

Open an existing Substance project (.spp).

**Parameters:**
- `file_path` (str) - Absolute path to .spp file

**Example:**
```python
substance_painter.project.open("C:/projects/MyProject.spp")
```

---

**save() → None**

Save the current project.

---

**save_as(file_path: str) → None**

Save project to a new file path.

---

**close() → None**

Close the current project.

---

**file_path() → str**

Get the current project's file path.

**Returns:**
- Absolute path to .spp file, or empty string if no project open

**Example:**
```python
project_path = substance_painter.project.file_path()
export_path = project_path.replace('.spp', '_textures')
```

---

**name() → str**

Get the current project's name (filename without extension).

#### Events

**ProjectOpened**

Triggered when a project is opened.

**ProjectAboutToClose**

Triggered before project closes.

**ProjectAboutToSave**

Triggered before project saves.

**ProjectSaved**

Triggered after project saves.

**Example: Auto-export on save**
```python
import substance_painter.event
import substance_painter.project
import substance_painter.export

def auto_export(event):
    if not substance_painter.project.is_open():
        return

    # Export textures when project saves
    config = {
        "exportPath": substance_painter.project.file_path().replace('.spp', '_export'),
        # ... rest of config
    }
    substance_painter.export.export_project_textures(config)

substance_painter.event.DISPATCHER.connect(
    substance_painter.event.ProjectSaved,
    auto_export
)
```

### substance_painter.textureset

Access texture sets and UV tiles.

#### Functions

**all_texture_sets() → List[TextureSet]**

Get all texture sets in the project.

**Returns:**
- List of TextureSet objects

**Example:**
```python
import substance_painter.textureset

for ts in substance_painter.textureset.all_texture_sets():
    print(f"Texture Set: {ts.name()}")
    print(f"  Layered: {ts.is_layered_material()}")
    print(f"  Resolution: {ts.get_resolution()}")
```

---

**all_uv_tiles() → List[UVTile]**

Get all UV tiles in the project (for UDIM workflows).

**Returns:**
- List of UVTile objects

**Example:**
```python
for tile in substance_painter.textureset.all_uv_tiles():
    print(f"Tile ({tile.u}, {tile.v}): {tile.get_resolution()}")
```

---

**set_uvtiles_resolution(resolutions: Dict[UVTile, Resolution]) → None**

Set resolution for multiple UV tiles.

**Parameters:**
- `resolutions` (dict) - Mapping of UVTile to Resolution

**Example:**
```python
from substance_painter.textureset import Resolution

# Set all tiles in first row to 2K
row0 = [tile for tile in all_uv_tiles() if tile.v == 0]
resolution_2k = Resolution(2048, 2048)
substance_painter.textureset.set_uvtiles_resolution({
    tile: resolution_2k for tile in row0
})
```

#### Classes

**TextureSet**

Represents a texture set (material slot).

**Methods:**
- `name() → str` - Get texture set name
- `is_layered_material() → bool` - Check if uses layer stacks
- `get_resolution() → Resolution` - Get texture resolution
- `get_stack() → Stack` - Get layer stack (if layered)

**Stack**

Represents a layer stack in a texture set.

**Methods:**
- `material() → TextureSet` - Get parent texture set
- `get_channel(channel_type: ChannelType) → Channel` - Get specific channel

**Channel**

Represents a texture channel (baseColor, normal, etc.).

**Methods:**
- `is_color() → bool` - Check if channel contains color data

**ChannelType (Enum)**

Available texture channels:
- `BaseColor`
- `Normal`
- `Metallic`
- `Roughness`
- `Height`
- `Opacity`
- `Emissive`
- `AmbientOcclusion`

**Resolution**

Texture resolution container.

**Attributes:**
- `width` (int) - Width in pixels
- `height` (int) - Height in pixels

**Constructor:**
```python
from substance_painter.textureset import Resolution

res = Resolution(2048, 2048)  # 2K
```

**UVTile**

Represents a UV tile in UDIM workflow.

**Attributes:**
- `u` (int) - U coordinate (0-based)
- `v` (int) - V coordinate (0-based)

**Methods:**
- `get_resolution() → Resolution` - Get tile resolution
- `set_resolution(resolution: Resolution) → None` - Set tile resolution

### substance_painter.resource

Access and manage resources (materials, brushes, presets).

#### Classes

**ResourceID**

Identifier for a resource.

**Constructor:**
```python
resource = substance_painter.resource.ResourceID(
    context="starter_assets",  # Library name
    name="PBR Metallic Roughness"  # Resource name
)
```

**Methods:**
- `url() → str` - Get resource URL (e.g., "starter_assets://PBR Metallic Roughness")

**Example: Use export preset**
```python
export_preset = substance_painter.resource.ResourceID(
    context="starter_assets",
    name="Unity HDRP (Lit)"
)

config = {
    "defaultExportPreset": export_preset.url(),
    # ...
}
```

### substance_painter.ui

UI customization and menu integration.

#### Enums

**ApplicationMenu**

Available application menus:
- `File`
- `Edit`
- `Mode`
- `View`
- `Viewport`
- `Shader`
- `Window`
- `Help`

#### Functions

**add_action(menu: ApplicationMenu, action: QtWidgets.QAction) → None**

Add menu item to application menu.

**Parameters:**
- `menu` (ApplicationMenu) - Target menu
- `action` (QAction) - Qt action to add

**Example:**
```python
from PySide2 import QtWidgets
import substance_painter.ui

def my_function():
    print("Menu item clicked!")

action = QtWidgets.QAction("My Custom Command", triggered=my_function)
substance_painter.ui.add_action(substance_painter.ui.ApplicationMenu.File, action)
```

---

**delete_ui_element(element) → None**

Remove UI element (cleanup when plugin closes).

---

**get_main_window() → QtWidgets.QMainWindow**

Get main application window (for parenting dialogs).

**Example: File dialog**
```python
from PySide2 import QtWidgets

export_path = QtWidgets.QFileDialog.getExistingDirectory(
    substance_painter.ui.get_main_window(),
    "Choose export directory"
)
```

### substance_painter.event

Event system for reacting to application events.

#### Event Dispatcher

**DISPATCHER**

Global event dispatcher object.

**Methods:**
- `connect(event_type, callback)` - Register event handler
- `disconnect(event_type, callback)` - Unregister event handler

**Example:**
```python
import substance_painter.event

def on_project_opened(event):
    print("Project opened!")

substance_painter.event.DISPATCHER.connect(
    substance_painter.event.ProjectOpened,
    on_project_opened
)
```

#### Available Events

**Project Events:**
- `ProjectOpened`
- `ProjectAboutToClose`
- `ProjectAboutToSave`
- `ProjectSaved`

**Export Events:**
- `ExportTexturesAboutToStart`
- `ExportTexturesEnded`

**Shader Events:**
- `ShaderAdded`
- `ShaderRemoved`

**Texture Set Events:**
- `TextureSetAdded`
- `TextureSetRemoved`

## Export Configuration Schema

Complete JSON schema for `export_project_textures()` config parameter.

### Root Configuration Object

```python
{
    "exportPath": str,              # Required: Output directory path
    "exportShaderParams": bool,     # Optional: Export shader params to JSON (default: false)
    "defaultExportPreset": str,     # Optional: Default preset URL
    "exportPresets": list,          # Optional: Custom export presets
    "exportList": list,             # Required: Texture sets to export
    "exportParameters": list        # Optional: Export parameter overrides
}
```

### Export List Item

```python
{
    "rootPath": str,                # Required: Texture set name (or "TextureSet/Stack" for layered)
    "exportPreset": str,            # Optional: Override preset for this item
    "filter": {                     # Optional: Filter which maps/tiles to export
        "outputMaps": list,         # List of map names (e.g., ["$textureSet_baseColor"])
        "uvTiles": list             # List of [u, v] tile coordinates (e.g., [[1,1], [1,2]])
    }
}
```

### Export Parameters Item

```python
{
    "filter": {                     # Optional: Match specific files
        "dataPaths": list,          # Texture set/stack names
        "outputMaps": list,         # Map name patterns
        "uvTiles": list             # UV tile coordinates
    },
    "parameters": {                 # Optional: Override export settings
        "fileFormat": str,          # "png", "jpeg", "tga", "exr", etc.
        "bitDepth": str,            # "8", "16", "32"
        "dithering": bool,          # Enable dithering
        "sizeLog2": int,            # Texture size: 9=512, 10=1024, 11=2048, 12=4096
        "paddingAlgorithm": str,    # "passthrough", "color", "transparent", "diffusion", "infinite"
        "dilationDistance": int     # Padding distance in pixels (required for some padding modes)
    }
}
```

### Custom Export Preset

```python
{
    "name": str,                    # Preset name
    "maps": [                       # List of texture maps to export
        {
            "fileName": str,        # Output filename pattern (e.g., "$textureSet_baseColor")
            "channels": [           # Channel mapping
                {
                    "destChannel": str,      # "R", "G", "B", "A"
                    "srcChannel": str,       # "R", "G", "B", "A"
                    "srcMapType": str,       # "documentMap"
                    "srcMapName": str        # "baseColor", "normal", "metallic", etc.
                }
            ],
            "parameters": {         # Optional: Per-map export parameters
                "fileFormat": str,
                "bitDepth": str,
                "sizeLog2": int
            }
        }
    ]
}
```

### Filename Patterns

Variables available in `fileName` patterns:
- `$textureSet` - Texture set name
- `$project` - Project name
- `$mesh` - Mesh name
- `$udim` - UDIM tile number (e.g., 1001)

**Examples:**
- `$textureSet_baseColor` → "MyAsset_baseColor.png"
- `$project_$textureSet_color` → "MyProject_MyAsset_color.png"

## Complete Examples

### Example 1: Basic Batch Export

Export all texture sets with standard settings:

```python
import substance_painter.export
import substance_painter.resource
import substance_painter.textureset

# Define preset
preset = substance_painter.resource.ResourceID(
    context="starter_assets",
    name="PBR Metallic Roughness"
)

# Build config
config = {
    "exportPath": "C:/export",
    "defaultExportPreset": preset.url(),
    "exportList": [
        {"rootPath": ts.name()}
        for ts in substance_painter.textureset.all_texture_sets()
    ],
    "exportParameters": [{
        "parameters": {
            "fileFormat": "png",
            "bitDepth": "8",
            "sizeLog2": 10,
            "paddingAlgorithm": "infinite"
        }
    }]
}

# Export
result = substance_painter.export.export_project_textures(config)
print(f"Status: {result.status}")
```

### Example 2: Selective Export with Filters

Export only baseColor at high resolution, other maps at lower resolution:

```python
config = {
    "exportPath": "C:/export",
    "defaultExportPreset": preset.url(),
    "exportList": [{"rootPath": "CharacterBody"}],
    "exportParameters": [
        {
            "filter": {"outputMaps": ["$textureSet_baseColor"]},
            "parameters": {"sizeLog2": 12}  # 4096 for baseColor
        },
        {
            "filter": {"outputMaps": ["$textureSet_normal", "$textureSet_metallicRoughness"]},
            "parameters": {"sizeLog2": 11}  # 2048 for other maps
        }
    ]
}
```

### Example 3: Custom Preset with Channel Packing

Create ORM (Occlusion-Roughness-Metallic) packed texture:

```python
custom_preset = {
    "exportPresets": [{
        "name": "WebGL_ORM",
        "maps": [
            {
                "fileName": "$textureSet_baseColor",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ]
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"}
                ]
            },
            {
                "fileName": "$textureSet_ORM",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"},
                    {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                    {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ]
            }
        ]
    }]
}

config = {
    "exportPath": "C:/export",
    "exportPresets": custom_preset["exportPresets"],
    "exportList": [{"rootPath": "MyAsset", "exportPreset": "WebGL_ORM"}],
    "exportParameters": [{
        "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
    }]
}
```

### Example 4: UDIM Export

Export specific UV tiles with different resolutions:

```python
from substance_painter.textureset import Resolution

# Set tile 1001 to 4K, others to 2K
tile_1001 = next((t for t in all_uv_tiles() if t.u == 0 and t.v == 0), None)
if tile_1001:
    tile_1001.set_resolution(Resolution(4096, 4096))

config = {
    "exportPath": "C:/export",
    "defaultExportPreset": preset.url(),
    "exportList": [
        {
            "rootPath": "UDIMAsset",
            "filter": {"uvTiles": [[0, 0], [1, 0], [2, 0]]}  # Export first row
        }
    ]
}
```

## Plugin Development

### Creating a Plugin

**Directory structure:**
```
plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

**plugin.py:**
```python
import substance_painter.ui
from PySide2 import QtWidgets

plugin_widgets = []

def my_command():
    print("Plugin command executed!")

def start_plugin():
    """Called when plugin loads"""
    action = QtWidgets.QAction("My Command", triggered=my_command)
    substance_painter.ui.add_action(substance_painter.ui.ApplicationMenu.File, action)
    plugin_widgets.append(action)

def close_plugin():
    """Called when plugin unloads"""
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()

if __name__ == "__main__":
    start_plugin()
```

### Plugin Best Practices

1. **Store UI elements** in module-level list for cleanup
2. **Check project state** before operations:
   ```python
   if not substance_painter.project.is_open():
       return
   ```
3. **Handle errors gracefully**:
   ```python
   try:
       result = substance_painter.export.export_project_textures(config)
   except ValueError as e:
       print(f"Export failed: {e}")
   ```
4. **Use absolute paths** for file operations
5. **Clean up resources** in `close_plugin()`

## Troubleshooting

### Common Issues

**Import Error: No module named 'substance_painter'**
- API only available when running inside Substance 3D Painter
- Use File → Scripts → Run Script to execute Python code

**ProjectError: No project is open**
- Check `substance_painter.project.is_open()` before API calls

**ValueError: Invalid export configuration**
- Verify all required fields in export config
- Check `exportPath` exists and is writable
- Ensure `exportList` is not empty

**ResourceID not found**
- Verify `context` (library name) is correct
- Check resource `name` matches exactly (case-sensitive)
- Use Substance UI to find resource names

### Debugging Tips

**Print configuration:**
```python
import json
print(json.dumps(config, indent=2))
```

**List available texture sets:**
```python
for ts in substance_painter.textureset.all_texture_sets():
    print(f"Texture Set: {ts.name()}")
```

**Preview export list without exporting:**
```python
preview = substance_painter.export.list_project_textures(config)
for stack, files in preview.items():
    print(f"{stack}: {files}")
```

## Resources

- **Official Python API Docs:** https://helpx.adobe.com/substance-3d-painter-python/api/
- **Substance 3D Community:** https://community.adobe.com/t5/substance-3d-painter/ct-p/ct-substance-3d-painter
- **Python Plugin Examples:** Included in Substance installation under `python/examples/`
