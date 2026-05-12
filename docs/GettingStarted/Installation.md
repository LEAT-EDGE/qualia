# Installing Qualia

## Introduction

Welcome to the Qualia installation guide.  
Qualia is an end-to-end training, quantization, and deployment framework for deep neural networks on embedded devices.
It's a modular system composed of multiple components or plugins that work together. There are three main ways to set up Qualia:

1. **User Setup**: For using Qualia as-is or developing independent plugins.

2. **Developer Setup**: _(Recommended)_ For using and modifying Qualia's components. If you want to:
    - Add datasets not yet supported.
    - Add new model architectures.
    - Upgrade or add functionality (metrics, quantization, etc.).
    - Add hardware targets that are not yet supported.

3. **Docker Setup**: For a containerized environment with GPU support. This is similar to the User Setup, but within a Docker container for ease of use.

## Before You Begin

### System Requirements
- Python >= 3.9, <= 3.14 (recommended: >= 3.11) if you want to use system Python.
- CMake >= 3.24
- Git
- For GPU support: NVIDIA GPU with appropriate drivers

## Working Directory & Virtual Environment
In this part, we will see how to prepare your environment setup before the installation. 

### Working Directory Tree
To properly work with Qualia, we suggest using the following project tree. 
We will create your work directory 'qualia' and inside create the virtual environment (see below) and the core and plugins folders.
After the installation, you will have the following directory tree: 

```bash
qualia/
├── qualia_env/          # The Qualia venv created using uv 
├── qualia-codegen-core/ # The Qualia codegen core directory 
├── qualia-core/         # The Qualia core directory 
├── qualia-plugin-{...}/ # The Qualia plugins (optional)
```

### Understanding Virtual Environments

Virtual environments provide isolated spaces for Python packages, preventing conflicts between different projects and making your setup more reproducible. We'll use them throughout this guide.  
To work with Qualia, it's recommended to use a 'uv'-managed virtual environment. 

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

```bash
# Install uv
pip install uv

mkdir qualia && cd qualia

# Create and activate a virtual environment
uv venv qualia_env --python 3.12

source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows
```

## Developer Setup

_(Recommended)_ For using and modifying Qualia's components, follow these steps in the qualia folder:

```bash
# Clone Qualia Core repository 
git clone https://github.com/LEAT-EDGE/qualia-core.git

# Install dependencies
cd qualia-core
# (choice) For basic components:
uv pip install -e .

# (choice) For additional components:
uv pip install -e .[pytorch]

# (choice) For all available components:
uv pip install -e .[tensorflow,pytorch,gtsrb,gsc,dataaugmentation_image,clearml,visualize,deployment-sparkfunedge,evaluation-host-tflite,evaluation-target-qualia,tests,lint,typecheck,docs]

# Repeat the above steps for Qualia Codegen Core
# Return to qualia folder
cd ..

# Clone Qualia Codegen Core repository 
git clone https://github.com/LEAT-EDGE/qualia-codegen-core.git

# Install dependencies
cd qualia-codegen-core
# For basic components:
uv pip install -e .
# Return to qualia folder
cd ..
```

You may also need to install these packages:
```bash
sudo apt install cmake ninja-build git gcc
```

CMake, ninja-build, and gcc are used for compiling C code. CMake needs to be at least version 3.15 (3.28 or newer recommended). If your Ubuntu version is lower than 24.04 and CMake is not at least 3.15:

```bash
uv pip install cmake
```

You should now have the following directory tree: 
```bash
qualia/
├── qualia_env/          # The Qualia venv created using uv 
├── qualia-codegen-core/ # The Qualia codegen core directory 
├── qualia-core/         # The Qualia core directory
```

Done! More information in [Optional Dependencies](#optional-dependencies).

## User Setup
For using Qualia as-is or developing independent plugins.

```bash
# Install uv
pip install uv

# Install Qualia with PyTorch support
uv pip install qualia-core[pytorch]

# Install Qualia Codegen if you want to generate code
uv pip install qualia-codegen-core
```

## Docker Setup

For a ready-to-use environment with GPU support, use our Docker container.

[Detailed Docker setup instructions continue as in the original document...](../PackageManagement/UsingDocker.md)

## Optional Dependencies

Qualia uses a modular system. Add features by including them in brackets:

```bash
uv pip install "qualia-core[codegen,tensorflow,pytorch,gtsrb,gsc,dataaugmentation_image,clearml,visualize,deployment-sparkfunedge,evaluation-host-tflite,evaluation-target-qualia,tests,lint,typecheck,docs]"
```

Available options:
- Machine Learning: `[pytorch]`, `[tensorflow]`
- Development: `[codegen]`, `[tests]`, `[lint]`, `[typecheck]`, `[docs]`
- Visualization: `[visualize]`, `[clearml]`
- Datasets: `[gtsrb]`, `[gsc]`, `[pytorch3drotation]`, `[dataaugmentation_image]`
- Deployment: `[deployment-sparkfunedge]`, `[evaluation-host-tflite]`, `[evaluation-target-qualia]`

## Qualia Components
If you want to take a look at all the available components, here is the link: [Optional Components](Components.md).

If you want to use Qualia for Spiking Neural Networks (SNN), here is the link: [Plugins SNN](../Plugins/PluginSNN/GettingStartedSNN.md).
