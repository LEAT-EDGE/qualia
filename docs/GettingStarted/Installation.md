# Installing Qualia

## Introduction

Welcome to the Qualia installation guide. Qualia is a modular system composed of multiple components that work together. There are three main ways to set up Qualia:

1. **User Setup**: For using Qualia as is or developing independent plugins
2. **Developer Setup**: For modifying Qualia's core components. You will need to install Qualia in developer setup
	- If you need to add a new dataset
	- If architecture
	- fonctionnalité
	- cible hardware
3. **Docker Setup**: For a containerized environment with GPU support. It's the user setup but in a Docker container for ease of use.

## Before You Begin

### System Requirements
- Python >= 3.9, <= 3.12 (recommended: 3.12) if you want to use system python.
- Git
- For GPU support: NVIDIA GPU with appropriate drivers

### Understanding Virtual Environments

Virtual environments provide isolated spaces for Python packages, preventing conflicts between different projects and making your setup more reproducible. We'll use them throughout this guide.

## User Setup
Brackets enable specifying optional dependency groups at installation, see the "Optional Dependencies" section below for more information.

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

```bash
# Install uv
pip install uv

# Create and activate a virtual environment
uv venv qualia_env --python 3.12
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# Install Qualia with PyTorch support
uv pip install qualia-core[pytorch]

# Install Qualia Codegen if you want to generate code
uv pip install qualia-codegen-core
```

## Developer Setup

For modifying Qualia's source code, follow these steps using either uv or PDM:

```bash
qualia
├── qualia_env          # The qualia venv created using uv
├── qualia-codegen-core # The qualia core codegen directory
├── qualia-core         # The qualia core codegen directory
```

Using uv :
```bash
# Install uv
pip install uv

# Clone repositories
git clone https://github.com/LEAT-EDGE/qualia-core.git
cd qualia-core

# Create and activate your development environment
uv venv qualia_env --python 3.12
source qualia_env/bin/activate

# Install dependencies
uv pip install -e .

# For additional components
uv pip install -e .[pytorch]

# For all available components
uv pip install -e .[codegen,tensorflow,pytorch,gtsrb,gsc,dataaugmentation_image,clearml,visualize,deployment-sparkfunedge,evaluation-host-tflite,evaluation-target-qualia,tests,lint,typecheck,docs]
```

You may also need to install those packages:
```bash
sudo apt install cmake ninja-build git gcc
```

Cmake ninja-build gcc are used for compiling C code. Cmake need to be at least >3.28, if not and your Ubuntu version is not 24 then you can install it using :
```bash
uv pip install cmake
```
## Docker Setup

For a ready-to-use environment with GPU support, use our Docker container. 

[Detailed Docker setup instructions continue as in the original document...](../PackageManagement/UsingDocker.md)

## Optional Dependencies

Qualia uses a modular system. Add features by including them in brackets:

```bash
uv pip install "qualia-core[pytorch,clearml,visualize]"
```

Available options:
- Machine Learning: `[pytorch]`, `[tensorflow]`
- Development: `[codegen]`, `[tests]`, `[lint]`, `[typecheck]`, `[docs]`
- Visualization: `[visualize]`, `[clearml]`
- Datasets: `[gtsrb]`, `[gsc]`, `[pytorch3drotation]`, `[dataaugmentation_image]`
- Deployment: `[deployment-sparkfunedge]`, `[evaluation-host-tflite]`, `[evaluation-target-qualia]`

## Qualia components
If you want to take a look at all the available components here is the link [Optional Components](Components.md).
