# Update

```{contents} Table of Contents
---
depth: 3
---
```

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

1. Update the git repositories:
```bash
cd qualia
git pull
```

Repeat for any additional Qualia components you're using.

### Update Third-party Dependencies

#### Option 1: Using uv

```bash
cd qualia
source qualia_env/bin/activate

# Update development installation
uv pip install -U -e ./qualia-core[pytorch,clearml] --dev

# For additional components
cd qualia-core
uv pip install -U -e .[pytorch,clearml] --dev
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

Move into the Qualia component directory:
```bash
cd qualia-core
```

Update the development installation:
```bash
pip install -U -e .[pytorch]
```

Repeat for additional components, following the dependency graph order (see <project:User/Components.md>).

## Available Optional Dependencies

When updating, you can include additional features by adding them in brackets:

- Machine Learning: `[pytorch]`, `[tensorflow]`
- Development: `[codegen]`, `[tests]`, `[lint]`, `[typecheck]`, `[docs]`
- Visualization: `[visualize]`, `[clearml]`
- Datasets: `[gtsrb]`, `[gsc]`, `[pytorch3drotation]`, `[dataaugmentation_image]`
- Deployment: `[deployment-sparkfunedge]`, `[evaluation-host-tflite]`, `[evaluation-target-qualia]`

The list above may not be up to date. You can verify in [[Installation]].

Remember to include all required dependencies when updating. For example:
```bash
# Using uv
uv pip install -U "qualia-core[pytorch,visualize,clearml]"

# Using PDM
pdm update "qualia-core[pytorch,visualize,clearml]"

# Using pip
pip install -U "qualia-core[pytorch,visualize,clearml]"
```