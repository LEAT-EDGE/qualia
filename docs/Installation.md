# Installing Qualia

## Introduction

Welcome to the Qualia installation guide. Qualia is a modular system composed of multiple components that work together. There are three main ways to set up Qualia:

1. **User Setup**: For using Qualia as is or developing independent plugins. Choose between three package managers:
   - uv (Recommended for best performance)
   - PDM (Recommended for advanced dependency management)
   - pip (Simple option)
2. **Developer Setup**: For modifying Qualia's core components.
3. **Docker Setup**: For a containerized environment with GPU support.

## Before You Begin

### System Requirements
- Python >= 3.9, <= 3.12 (recommended: 3.11)
- Git
- For GPU support: NVIDIA GPU with appropriate drivers

### Understanding Virtual Environments

Virtual environments provide isolated spaces for Python packages, preventing conflicts between different projects and making your setup more reproducible. We'll use them throughout this guide.

## User Setup

### Option 1: Using uv (Recommended for Performance)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

```bash
# Install uv
pip install uv

# Create and activate a virtual environment
uv venv qualia_env
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# Install Qualia with PyTorch support
uv pip install qualia-core[pytorch]
```

### Option 2: Using PDM (Recommended for Dependency Management)

[PDM](https://pdm.fming.dev/) is a modern Python package manager with robust dependency management.

```bash
# Install PDM
# On Ubuntu 24.10 or newer:
sudo apt install python3-pdm
# Or using pip:
pip install pdm

# Create and set up project
pdm venv create -n qualia_env
$(pdm venv activate qualia_env)

# Install Qualia
pdm add qualia-core[pytorch]
```

### Option 3: Using pip (Simple Option)

For a straightforward setup using standard Python tools:

```bash
# Create virtual environment
python -m venv qualia_env
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# Install Qualia
pip install -U qualia-core[pytorch]
```

## Developer Setup

For modifying Qualia's source code, follow these steps using either uv or PDM:

### Using uv for Development

```bash
# Clone repositories
git clone https://your-gitlab-server/qualia.git
cd qualia

# Create development environment
uv venv qualia_env
source qualia_env/bin/activate

# Install dependencies
uv pip install -e ./qualia-core[pytorch,clearml] --dev

# For additional components
git clone git@your-gitlab-server:qualia-core.git
uv pip install -e ./qualia-core[pytorch,clearml] --dev
```

### Using PDM for Development

```bash
# Clone repositories
git clone https://your-gitlab-server/qualia.git
cd qualia

# Create development environment
pdm venv create -n qualia_env
pdm use "$(pwd)/qualia_env/bin/python"

# Install dependencies
pdm add -e ./qualia-core[pytorch,clearml] --dev

# For additional components
git clone git@your-gitlab-server:qualia-core.git
pdm add -e ./qualia-core[pytorch,clearml] --dev
```

The `-e` flag enables "editable" mode, allowing source code changes to take effect without reinstalling.

## Docker Setup

For a ready-to-use environment with GPU support, use our Docker container.

### Prerequisites
- Ubuntu Linux (tested on Ubuntu 22.04 and 24.04)
- NVIDIA GPU with drivers
- Docker Engine and NVIDIA Container Toolkit

[Detailed Docker setup instructions continue as in the original document...]

## Optional Dependencies

Qualia uses a modular system. Add features by including them in brackets:

```bash
# Using uv
uv pip install "qualia-core[pytorch,clearml,visualize]"

# Using PDM
pdm add "qualia-core[pytorch,clearml,visualize]"

# Using pip
pip install "qualia-core[pytorch,clearml,visualize]"
```

Available options:
- Machine Learning: `[pytorch]`, `[tensorflow]`
- Development: `[codegen]`, `[tests]`, `[lint]`, `[typecheck]`, `[docs]`
- Visualization: `[visualize]`, `[clearml]`
- Datasets: `[gtsrb]`, `[gsc]`, `[pytorch3drotation]`, `[dataaugmentation_image]`
- Deployment: `[deployment-sparkfunedge]`, `[evaluation-host-tflite]`, `[evaluation-target-qualia]`

## Common Issues and Solutions

### Package Installation Errors

You may need to install additional dependencies:

```bash
# Python packages
uv pip install --upgrade pip virtualenv graphviz tensorflow torch-optimizer matplotlib numpy pydot
# or with PDM
pdm add pip virtualenv graphviz tensorflow torch-optimizer matplotlib numpy pydot

# System packages (Ubuntu/Debian)
sudo apt install cmake ninja-build git gcc
```

### Environment Issues

```bash
# Check Python version
python --version  # Should be 3.9-3.12 (3.11 recommended)

# Verify Qualia installation
pip show qualia-core

# If using wrong Python version
uv venv qualia_env --python=3.11
# or with PDM
pdm venv create -n qualia_env --python=3.11
```

## Getting Help

If you encounter issues:
1. Check error messages carefully
2. Verify Python version (3.11 recommended)
3. Ensure virtual environment is activated
4. Check all dependencies are installed

Remember to activate your environment before using Qualia:
```bash
# For uv and pip:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# For PDM:
$(pdm venv activate qualia_env)
```