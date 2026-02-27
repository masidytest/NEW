# plugin_loader.py
# Dynamic plugin loading system

import importlib.util
import pathlib
from typing import Optional

def load_plugins(cap_registry, folder: str = "plugins"):
    """
    Load all plugins from the plugins folder.
    Each plugin should have a register(cap_registry) function.
    """
    plugin_folder = pathlib.Path(folder)
    
    if not plugin_folder.exists():
        print(f"[plugin_loader] Plugin folder '{folder}' not found, skipping")
        return
    
    loaded_count = 0
    error_count = 0
    
    for path in plugin_folder.glob("*.py"):
        if path.stem.startswith("_"):
            continue  # Skip files starting with underscore
        
        try:
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if spec is None or spec.loader is None:
                print(f"[plugin_loader] Could not load spec for {path.name}")
                error_count += 1
                continue
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "register"):
                module.register(cap_registry)
                loaded_count += 1
                print(f"[plugin_loader] ✓ Loaded plugin: {path.stem}")
            else:
                print(f"[plugin_loader] ⚠ Plugin {path.stem} has no register() function")
                error_count += 1
        
        except Exception as e:
            print(f"[plugin_loader] ✗ Error loading {path.stem}: {e}")
            error_count += 1
    
    print(f"[plugin_loader] Loaded {loaded_count} plugins ({error_count} errors)")
