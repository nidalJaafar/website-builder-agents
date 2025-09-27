#!/usr/bin/env python3
"""Command-line utilities for the JSON Parser project."""

import shutil
import os
import sys
from pathlib import Path


def clean_project():
    """Clean up __pycache__ directories and other build artifacts."""
    project_root = Path(__file__).parent
    print(project_root)
    cache_dirs = [
        "__pycache__",
        "src/__pycache__",
        "src/json_parser.egg-info"
    ]
    
    for cache_dir in cache_dirs:
        cache_path = project_root / cache_dir
        if cache_path.exists():
            if cache_path.is_dir():
                print(f"Removing directory: {cache_path}")
                shutil.rmtree(cache_path, ignore_errors=True)
            else:
                print(f"Removing file: {cache_path}")
                cache_path.unlink(missing_ok=True)
    
    print("Project cleanup completed!")


def setup_project():
    """Set up the project environment."""
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    env_example = project_root / ".env.example"
    env_file = project_root / ".env"
    
    print("JSON Parser Project Setup")
    print("=" * 40)
    
    if env_example.exists() and not env_file.exists():
        print("Creating .env file from .env.example...")
        shutil.copy(env_example, env_file)
        print(f"Created {env_file}")
        print("\nIMPORTANT: Edit .env and configure your API keys!")
    elif env_file.exists():
        print("\nEnvironment setup complete!")


def start_api():
    """Start the FastAPI server."""
    import uvicorn
    import os
    from pathlib import Path
    
    # Change to project root (so api.py is importable)
    project_root = Path(__file__).resolve().parent
    print(project_root)
    os.chdir(project_root)
    
    print("Starting JSON Parser API server...")
    uvicorn.run("website_builder.api.json_api:app", host="0.0.0.0", port=8000, reload=True)


    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "clean":
            clean_project()
        elif cmd == "setup":
            setup_project()
        elif cmd == "api":
            start_api()
        else:
            print(f"Unknown command: {cmd}")
            print("Available commands: clean, setup, api")
    else:
        print("Available commands: clean, setup, api")