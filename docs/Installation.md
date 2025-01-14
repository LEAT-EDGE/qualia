# Installing Qualia on your machine

```{contents} Table of Contents
---
depth: 3
---
```
## Introduction
Welcome to the Qualia installation guide. Qualia is a modular system composed of multiple components that work together. Before diving into installation, let's understand the two main ways you can set up Qualia based on your needs:

1. User Setup: Choose this if you plan to use Qualia as is or develop independent plugins. This setup is simpler.
2. Developer Setup: Choose this if you need to modify Qualia's core components. This setup gives you access to the source code but requires more configuration.

## Before You Begin

### System Requirements
- Python >= 3.9, <= 3.12 ; recommended: 3.11
- Pip
- (Optional) PDM to create a virtual environments
- (Optional) Conda if the system's Python version is not suitable

### Understanding Virtual Environments

Throughout this guide, we'll be using virtual environments. Think of a virtual environment as a separate, isolated space on your computer where you can install Python packages without affecting your system's Python installation. This isolation helps prevent conflicts between different projects and makes your setup more reproducible.

## User Setup

If you're new to Qualia or plan to use it without modifying its core components, follow this section. We'll cover two approaches: using pip (simpler) or PDM (virtual environment).

### Option 1: Using Pip with an Existing Environment

This is the quickest way to get started if you're already familiar with Python and pip.

-  Install Qualia components using pip. For example, to install Qualia-Core with PyTorch and ClearML support:
```bash
pip install -U qualia-core[pytorch,clearml]
```

The brackets after the package name indicate optional features you want to include. You can mix and match these based on your needs.

### Option 2: Using PDM (Recommended for New Projects)

PDM is a modern Python package manager that provides more robust dependency management. Here's how to use it:

1. Install PDM first:
```bash
# On Ubuntu 24.10 or newer:
sudo apt install python3-pdm
# Or using pip:
pip install pdm
```

2. Set up your project:
```bash
# Create a virtual environment named qualia-env with Python 3.11
pdm venv create -n qualia-env # Using system Python 3.11
# or
pdm venv create -n qualia-env -w conda 3.11 # Using Conda if needed

# Use the newly created environment 
pdm use qualia-env
```

3. Activate your environment (do this each time you open a new terminal):
```bash
$(pdm venv activate qualia-env)
```

4. Install Qualia components:
```bash
pdm add qualia-core[pytorch,clearml]
```

## Developer Setup

If you need to modify Qualia's source code, follow this section. This setup gives you direct access to the code while maintaining a proper development environment.

### Setting Up Your Development Environment

1. Clone the base Qualia repository:
```bash
git clone https://your-gitlab-server/qualia.git
cd qualia
```

2. Create a development environment:
```bash
pdm venv create -w conda 3.11
pdm use "$(pwd)/.venv/bin/python"
```

3. For each Qualia component you want to modify:
```bash
# Clone the component repository
git clone git@your-gitlab-server:qualia-core.git

# Install it in development mode
pdm add -e ./qualia-core[pytorch,clearml] --dev
```

The `-e` flag installs the package in "editable" mode, meaning changes to the source code take effect immediately without reinstalling.

## Component Dependencies

Qualia is built as a modular system where components may depend on each other. When installing multiple components, install them in order from the most basic to the most dependent. For example, if component B depends on component A, install A first, then B.

## Troubleshooting Common Issues

### Python Version Conflicts

If you see errors about Python version incompatibility, verify your Python version:
```bash
python --version
```

If it's not 3.11, you can create a new Conda environment with the correct version:
```bash
conda create -n qualia-env python=3.11
conda activate qualia-env
```

### PDM Command Not Found

If PDM commands fail, ensure it's properly installed:
```bash
pip show pdm
```

If not found, reinstall it:
```bash
pip install -U pdm
```

### Package Installation Errors

If you encounter errors during package installation or utilisation of Qualia you may need to add one of those:
```bash
# Pip package
pip install --upgrade pip
pip install --upgrade virtualenv
pip install --upgrade pdm
pip install --upgrade pdm-backend
pip install --upgrade graphviz
pip install --upgrade tensorflow
pip install --upgrade torch-optimizer
pip install --upgrade matplotlib
pip install --upgrade numpy
pip install --upgrade pydot

#Apt package
sudo apt install cmake \
ninja-build \
git \
gcc
```

## Getting Help

If you encounter issues not covered in this guide:
1. Check the error message carefully - it often contains hints about what went wrong
2. Verify you're using the recommended Python version (3.11)
3. Ensure your virtual environment is activated

Remember to always activate your virtual environment before running Qualia-related commands:
```bash
# For pip-based setups:
source qualia-env/bin/activate  # Unix/macOS
qualia-env\Scripts\activate     # Windows

# For PDM-based setups:
$(pdm venv activate in-project)
```
# Qualia Docker Environment

This container provides a ready-to-use environment with all dependencies pre-installed for Qualia development and deployment. It includes CUDA support for GPU acceleration.

## Prerequisites

- Ubuntu Linux (tested on Ubuntu 22.04 and 24.04)
- NVIDIA GPU with appropriate drivers installed
- Sudo privileges

## Installation Steps

### 1. Install Docker Engine

```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
# Install Docker packages
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

### 2. Install NVIDIA Container Toolkit

```bash
# Add NVIDIA Container Toolkit repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install and configure
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### 3. Build and Run Qualia Docker Image

```bash
# Clone the repository
git clone https://naixtech.unice.fr/gitlab/qualia/qualia.git
cd qualia/docker

# Build the image (this may take several minutes)
sudo docker build -f qualia-opensource-cuda -t qualia:cuda .

# Run the container with GPU support
sudo docker run -d --gpus all -p 2222:22 qualia:cuda
```

## Using the Container

### SSH Access

```bash
# Connect to the container
ssh -p 2222 root@localhost  # password: root

# If you get a host key error, reset the SSH fingerprint using either:
# Method 1 (using $HOME):
ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[localhost]:2222"
# Method 2 (using explicit path):
ssh-keygen -f '/home/$USER/.ssh/known_hosts' -R '[localhost]:2222'
# Both commands do the same thing, just using different ways to reference your home directory
```

### File Transfer

Transfer files to and from the container using SCP:

```bash
# Copy files TO the container
scp -P 2222 -r data/ root@localhost:/app/                  # Copy directory
scp -P 2222 CNN_float32_train.toml root@localhost:/app/    # Copy file

# Copy files FROM the container
scp -P 2222 -r root@localhost:/app/out/ ./                 # Copy output directory
scp -P 2222 root@localhost:/app/out/results.txt ./         # Copy specific file
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Stop the container
docker stop <container_id>

# Start a stopped container
docker start <container_id>

# Remove a container
docker rm <container_id>
```

## Troubleshooting

1. If SSH connection fails:
   - Verify the container is running: `docker ps`
   - Check if port 2222 is already in use: `netstat -tuln | grep 2222`

2. If GPU is not detected:
   - Verify NVIDIA drivers are installed: `nvidia-smi`
   - Check container GPU access: `docker exec <container_id> nvidia-smi`

# Optional Dependencies in Qualia

Qualia uses a modular system where you can install extra features as needed. Here are the available options:

## Machine Learning Frameworks

- `[pytorch]`: For PyTorch-based projects
    - Includes PyTorch, PyTorch Lightning, and tabulate
- `[tensorflow]`: For TensorFlow-based projects
    - Includes TensorFlow, Keras, and pydot

## Development Tools

- `[codegen]`: For code generation
    - Includes qualia_codegen_core
- `[tests]`: For testing
    - Includes pytest and related plugins
- `[lint]`: For code style checking
    - Includes ruff
- `[typecheck]`: For type checking
    - Includes mypy and pyright
- `[docs]`: For documentation
    - Includes Sphinx with ReadTheDocs theme

## Data and Visualization

- `[visualize]`: For creating plots and PDFs
    - Includes matplotlib and pypdf
- `[clearml]`: For tracking experiments
    - Includes clearml and tensorboard

## Dataset Processing

- `[gtsrb]`: For traffic sign recognition
    - Includes imageio and scikit-image
- `[gsc]`: For speech commands
    - Includes torchaudio
- `[pytorch3drotation]`: For 3D vision
    - Includes pytorch3d
- `[dataaugmentation_image]`: For image processing
    - Includes torchvision

## Deployment and Evaluation

- `[deployment-sparkfunedge]`: For edge deployment
    - Includes pycryptodome
- `[evaluation-host-tflite]`: For TFLite evaluation
    - Includes scikit-learn
- `[evaluation-target-qualia]`: For hardware targets
    - Includes pyserial

To use multiple options, combine them with commas:

```bash
pip install qualia-core[pytorch,clearml,visualize]
```

Tip: Only install what you need to keep your environment light and avoid conflicts.