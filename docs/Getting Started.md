# Getting Started with Qualia

This guide will help you get up and running with Qualia, a modular system for machine learning experimentation and deployment.
We will show you a very simple installation and exemple. If you want more detail about the different part we advice you to seek the answers in the documentation :
- [[Installation]]
- [[Usage]]
- [[ConfigurationFile]]
- [[Components]]

## Prerequisites

Before you begin, ensure you have:
- Python (version 3.9-3.12, recommended: 3.11)
- Git (for cloning repositories)
- Basic familiarity with command line operations

## Installation Options

We provide three installation methods, listed from most recommended to simplest:

### Option 1: Using uv (Recommended for Best Performance)

[uv](https://github.com/astral-sh/uv) is a new, extremely fast Python package installer and resolver. It's an excellent choice for modern Python development.

```bash
# Install uv
pip install uv

# Create and activate a virtual environment
uv venv qualia_env
source qualia_env/bin/activate  # On Unix/macOS
qualia_env\Scripts\activate     # On Windows

# Install Qualia with PyTorch support
uv pip install qualia-core[pytorch]
```

### Option 2: Using PDM (Recommended for Advanced Users)

[PDM](https://pdm.fming.dev/) is a modern Python package manager that provides robust dependency management.

```bash
# Install PDM
# On Ubuntu 24.10 or newer:
sudo apt install python3-pdm
# Or using pip:
pip install pdm

# Create and activate a virtual environment
pdm venv create -n qualia_env
$(pdm venv activate qualia_env)

# Install Qualia with PyTorch support
pdm add qualia-core[pytorch]
```

### Option 3: Using pip (Simple Option)

For a quick setup using standard Python tools:

```bash
# Create a virtual environment
python -m venv qualia_env
source qualia_env/bin/activate  # On Unix/macOS
qualia_env\Scripts\activate     # On Windows

# Install Qualia
pip install -U qualia-core[pytorch]
```

## Tutorial: Your First Qualia Project

Let's create a practical example using the UCI Human Activity Recognition (HAR) dataset.

### 1. Project Setup

First, create a new project directory:

```bash
mkdir qualia-project
cd qualia-project
```

### 2. Dataset Preparation

1. Download the UCI HAR dataset from [UCI HAR](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)
2. Extract the downloaded file
3. Create the following directory structure:
```
qualia-project/
├── data/
│   └── UCI HAR Dataset/  # Place extracted dataset here
│       ├── train/
│       └── test/
└── config.toml           # We'll create this next
```

### 3. Configuration

Create `config.toml` with the following content:

```toml
[bench]
name = "UCI-HAR_CNN_example"
seed = 2
first_run = 1
last_run = 1

[learningframework]
kind = "PyTorch"

[dataset]
kind = "UCI_HAR"
params.variant = "raw"
params.path = "data/UCI HAR Dataset/"

# Data preprocessing steps
[[preprocessing]]
kind = "DatamodelConverter"

[[preprocessing]]
kind = "Class2BinMatrix"

# Model configuration
[model_template]
kind = "CNN"
epochs = 10
batch_size = 32
params.batch_norm = true

[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

# CNN architecture
[[model]]
name = "uci-har_cnn_simple"
params.filters = [5, 5]        # Two conv layers with 5 filters each
params.kernel_sizes = [2, 2]   # 2x2 kernels
params.pool_sizes = [2, 0]     # Pooling after first conv layer

# Optional: Deployment configuration
[deploy]
target = 'Linux'
converter.kind = 'QualiaCodeGen'
quantize = ['float32']
optimize = ['']
limit = 50
```

### 4. Running the Experiment

Execute these commands in order:

```bash
# 1. Preprocess the dataset
qualia config.toml preprocess_data

# 2. Train the model
qualia config.toml train

# Optional: Deploy and evaluate
qualia config.toml prepare_deploy
qualia config.toml deploy_and_evaluate
```

### Understanding the Output

- Processed dataset: `out/data/<dataset_name>/`
- Model weights: `out/learningmodel/`
- Training logs: `log/<bench_name>/learningmodel/`
- Deployment files: `out/<converter>/`
- Evaluation results: `log/<bench_name>/evaluate/`

## Optional Features

Enhance your installation with additional features:

```bash
# Using uv
uv pip install "qualia-core[pytorch,visualize,clearml,tests]"

# Using PDM
pdm add "qualia-core[pytorch,visualize,clearml,tests]"

# Using pip
pip install "qualia-core[pytorch,visualize,clearml,tests]"
```

Available features:
- `visualize`: Plotting and visualization tools
- `clearml`: Experiment tracking
- `tests`: Testing utilities
- `lint`: Code quality tools
- `docs`: Documentation tools
- `tensorflow`: TensorFlow support
- And more to discover in [[Installation]] !

## Best Practices

1. **Virtual Environments**: Always use a virtual environment for each project
2. **Dependencies**: Keep track of your dependencies (uv and PDM handle this automatically)
3. **Configuration**: Store different experiments in separate configuration files
4. **Version Control**: Use git to track your configurations and custom code

## Troubleshooting

If you encounter issues:

1. **Environment Issues**:
   ```bash
   # Check Python version
   python --version  # Should be 3.9-3.12 (3.11 recommended)
   
   # Verify Qualia installation
   pip show qualia-core
   ```

2. **Dataset Issues**:
   - Verify the dataset path in `config.toml` matches your directory structure
   - Ensure all dataset files are present and readable

3. **Training Issues**:
   - Check GPU availability (if using)
   - Monitor system resources
   - Review training logs in `log/<bench_name>/learningmodel/`

## Getting Help

- Check error messages carefully
- Verify your Python version (3.11 recommended)
- Ensure your virtual environment is activated
- Validate all dependencies are installed correctly

Remember to activate your environment before using Qualia:
```bash
# For uv:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# For PDM:
$(pdm venv activate qualia_env)

# For pip:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows
```