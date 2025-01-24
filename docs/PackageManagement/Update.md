# Update

## User Setup

### Option 1: Using uv (Recommended for Performance)

Activate your environment:
```bash
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows
```

Update Qualia and its dependencies:
```bash
# Basic update with PyTorch support
uv pip install -U qualia-core[pytorch]

# With additional dependencies
uv pip install -U "qualia-core[pytorch,visualize,test]"

# Update every package in the environnement
uv pip freeze | cut -d= -f1 | xargs uv pip install -U
```

### Option 2: Using PDM (Recommended for Dependency Management)

Activate your environment:
```bash
$(pdm venv activate qualia_env)
```

Update Qualia and all dependencies:
```bash
# Update all packages in the environment
pdm update --update-all

# Update specific package with dependencies
pdm update qualia-core
```

### Option 3: Using pip

Pip will only update the specified Qualia components and install new dependencies when required.

```bash
# Basic update with PyTorch support
pip install -U qualia-core[pytorch]

# With additional dependencies
pip install -U "qualia-core[pytorch,visualize,test]"
```

## Developer Setup

### Update Qualia's Components

For developer setups, first update the source code:

Update the source code from the git repositories:
```bash
# Activate environment
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# Update repositories
cd qualia
git pull
```

Repeat for any additional Qualia components you're using.

### Update Third-party Dependencies

#### Option 1: Using uv

```bash
cd qualia
source qualia_env/bin/activate

# Update all dependencies
uv pip freeze | cut -d= -f1 | xargs uv pip install -U

# Development installation
cd qualia
uv pip install -U -e ./qualia-core[pytorch,clearml]

# Component-specific
cd qualia-core
uv pip install -U -e .[pytorch,clearml]
```

#### Option 2: Using PDM

```bash
cd qualia
$(pdm venv activate)

# Update all dependencies
pdm update --update-all

# Update specific component and its dependencies
pdm update qualia-core
```

#### Option 3: Using pip

Note: pip only updates dependencies when explicitly required.

Update the development installation:
```bash
pip install -U -e .[pytorch]
```

Repeat for additional components, following the dependency graph order (see [Components](../UserGuide/Components)).
