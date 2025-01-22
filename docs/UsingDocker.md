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

### Using Custom Configs and Datasets
You can mount a volume with Docker or transfer the files using SCP.
#### Option 1: Mount Local Directory

```bash
# Run the container and mounts your current directory to `/workspace` in the container.
docker run -d --gpus all -p 2222:22 -v .:/workspace qualia:cuda
```

#### Option 2: Transfer Files via SCP

```bash
# Copy files TO the container
scp -P 2222 -r data/ root@localhost:/workspace/                  # Copy directory
scp -P 2222 CNN_float32_train.toml root@localhost:/workspace/    # Copy file

# Copy files FROM the container
scp -P 2222 -r root@localhost:/workspace/out/ ./                 # Copy output directory
scp -P 2222 root@localhost:/workspace/out/results.txt ./         # Copy specific file
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

## Additional Resources

For more information on using Qualia, refer to the [Qualia Documentation](link_to_docs).