# Getting Started with Qualia
## Introduction
This guide will help you get up and running with Qualia, a modular system for machine learning experimentation and deployment.
We will show you a very simple installation and exemple. If you want more detail about the different part we advice you to seek the answers in the documentation :
- [Installation](Installation)
- [Usage](../UserGuide/Usage)
- [ConfigurationFile](../UserGuide/ConfigurationFile)
- [Components](../UserGuide/Components)

## Prerequisites

Before you begin, ensure you have:
- Python (version 3.9-3.12, recommended: 3.12)
- Git (for cloning repositories)
- Basic familiarity with command line operations

## Installation Options

Please use one of the installation procedure listed in {doc}`Installation` or {doc}`UsingDocker`.

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
2. Extract into `data/` directory
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

### Qualia's commands
#### Data Preprocessing
```bash
qualia config.toml preprocess_data
```

Loads UCI_HAR dataset specified in `[dataset]` section:
```toml
[dataset]
kind = "UCI_HAR"
params.variant = "raw"
params.path = "data/UCI HAR Dataset/"
```

Applies preprocessing steps from `[[preprocessing]]`:
1. DatamodelConverter: Converts activities and subjects into data/label arrays
2. Class2BinMatrix: Converts class numbers to one-hot encoding
```toml
[[preprocessing]]
kind = "DatamodelConverter"

[[preprocessing]]
kind = "Class2BinMatrix"
```

Exports preprocessed NumPy arrays to `out/data/UCI_HAR_raw/`:
- `train_data.npy`, `train_labels.npy`
- `test_data.npy`, `test_labels.npy`

#### Model Training
```bash
qualia config.toml train
```

Uses PyTorch framework defined in `[learningframework]`:
```toml
[learningframework]
kind = "PyTorch"
```

Trains model from `[[model]]` using shared CNN configuration:
```toml
[model_template]
kind = "CNN"
epochs = 10
batch_size = 32

[[model]]
name = "uci-har_cnn_simple"
params.filters = [5, 5]        # Two conv layers
params.kernel_sizes = [2, 2]   # 2x2 kernels
params.pool_sizes = [2, 0]     # First layer pooling
```

Saves trained model in `out/learningmodel/`.

#### Deployment Preparation
```bash
qualia config.toml prepare_deploy
```

Converts trained model to embedded format using `[deploy]` settings:
```toml
[deploy]
target = 'Linux'             # Host CPU
converter.kind = 'QualiaCodeGen'  # C code generator
quantize = ['float32']       # Precision
optimize = ['']              # Optimizations
```

Generates C code and compiles for Linux host in `out/QualiaCodeGen/`.