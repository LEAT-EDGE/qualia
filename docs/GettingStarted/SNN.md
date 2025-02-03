# Getting Started with Spiking Neural Networks in Qualia
## Introduction

This guide will help you get up and running with Spiking Neural Networks (SNN) in Qualia. SNNs are biologically inspired neural networks that process information through discrete spikes rather than continuous values. We will demonstrate using the UCI Human Activity Recognition (HAR) dataset as an example.

## Prerequisites

Before you begin, ensure you have:
- Qualia installed with Python (version 3.9-3.12, recommended: 3.12)
- The qualia-plugin-snn package installed

## Installation

1. First, install the SNN plugin:
```bash
pip install qualia-plugin-snn
```

2. Create a new project directory:
```bash
mkdir qualia-snn-project
cd qualia-snn-project
```

## Dataset Preparation

1. Download the UCI HAR dataset from [UCI HAR](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)
2. Extract into `data/` directory:
```
qualia-snn-project/
├── data/
│   └── UCI HAR Dataset/  # Place extracted dataset here
│       ├── train/
│       └── test/
└── config.toml           # We'll create this next
```

## Understanding SNN Components

Before configuring the network, let's understand the key components of an SNN in Qualia:

### 1. Neuron Models
Qualia supports several spiking neuron models:
- IF (Integrate-and-Fire): Basic model that accumulates input and fires when threshold is reached
- LIF (Leaky Integrate-and-Fire): Adds leak current to IF model
- ALIF (Adaptive LIF): Adds adaptive threshold mechanism

### 2. Spike Encoding
Methods to convert continuous input data to spikes:
- Rate coding: Input magnitude determines spike frequency
- Temporal coding: Input magnitude determines spike timing
- Population coding: Input encoded across multiple neurons

### 3. Surrogate Gradients
Since spike functions are non-differentiable, surrogate gradients are used for training:
- Sigmoid approximation
- Triangle approximation
- Rectangle approximation

## Configuration File

Create `config.toml` with these sections:

### 1. Basic Setup and Plugin
```toml
[bench]
name = "UCI-HAR_SNN_example"
seed = 2
first_run = 1
last_run = 1
plugins = ["qualia_plugin_snn"]  # Enable SNN functionality
```

### 2. Learning Framework
```toml
[learningframework]
kind = "SNN"
params.timesteps = 100     # Number of simulation timesteps
params.encoding = "rate"   # Spike encoding method
params.backend = "torch"   # Computational backend
```

### 3. Dataset Configuration
```toml
[dataset]
kind = "UCI_HAR"
params.variant = "raw"
params.path = "data/UCI HAR Dataset/"
```

### 4. Preprocessing Steps
```toml
# Convert data format
[[preprocessing]]
kind = "DatamodelConverter"

# Convert labels to binary matrix
[[preprocessing]]
kind = "Class2BinMatrix"

# Normalize data for spike encoding
[[preprocessing]]
kind = "Normalize"
params.method = "minmax"
params.min_val = 0
params.max_val = 1
```

### 5. Model Configuration
```toml
[model_template]
kind = "SCNN"              # Spiking CNN
epochs = 50
batch_size = 32

# Neuron parameters
params.neuron_type = "LIF"
params.threshold = 1.0
params.tau_mem = 10.0      # Membrane time constant
params.tau_syn = 5.0       # Synaptic time constant
params.reset_method = "zero"
params.surrogate = "sigmoid"
params.surrogate_slope = 10.0

# Training parameters
[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

# Network architecture
[[model]]
name = "uci-har_scnn_simple"
params.filters = [16, 32]       # Conv layer filters
params.kernel_sizes = [3, 3]    # Kernel sizes
params.pool_sizes = [2, 2]      # Pooling layers
params.fc_units = [256, 6]      # Fully connected layers
```

## Running the Experiment

Execute these commands in sequence:

```bash
# 1. Preprocess the dataset
qualia config.toml preprocess_data

# 2. Train the SNN
qualia config.toml train

# 3. Optional: Deploy
qualia config.toml prepare_deploy
qualia config.toml deploy_and_evaluate
```

## Understanding the Output

### Training Metrics
The training process will generate several metrics specific to SNNs:
- Spike rate: Average number of spikes per neuron
- Membrane potential statistics
- Classification accuracy
- Energy efficiency metrics

Find these in:
```
log/<bench_name>/learningmodel/metrics.json
```

### Spike Visualization
Qualia provides tools to visualize spike patterns:
```toml
[[postprocessing]]
kind = "VisualizeSpikes"
params.save_plots = true
params.num_samples = 10
```

Visualizations will be saved in:
```
out/spike_viz/<model_name>/
```

## Advanced Features

### 1. Homeostatic Plasticity
Enable homeostatic mechanisms to maintain stable firing rates:
```toml
[model_template.params]
homeostatic_plasticity = true
target_rate = 0.1
adaptation_rate = 0.01
```

### 2. STDP Learning
Configure Spike-Timing-Dependent Plasticity:
```toml
[model_template.params]
learning_rule = "STDP"
stdp_window = 20
stdp_lr = 0.0001
```

### 3. Multi-compartment Neurons
Define more complex neuron models:
```toml
[model_template.params]
neuron_type = "MultiCompartmentLIF"
compartments = ["soma", "dendrite"]
coupling_strengths = [0.5]
```

## Best Practices

1. **Spike Encoding**
   - Start with rate coding for simpler problems
   - Use temporal coding for precise timing information
   - Consider population coding for robust representation

2. **Neuron Parameters**
   - Begin with LIF neurons for most applications
   - Tune time constants based on input dynamics
   - Adjust threshold for desired spike rates

3. **Training**
   - Use smaller learning rates than ANN training
   - Monitor spike rates to avoid saturation
   - Consider gradient scaling for stable training

4. **Memory Usage**
   - Balance timesteps with batch size
   - Monitor memory usage during training
   - Use appropriate data types for efficiency

## Common Issues and Solutions

1. **Silent Networks**
   - Problem: Neurons not spiking
   - Solutions:
     - Lower threshold values
     - Increase input scaling
     - Check normalization

2. **Exploding Activity**
   - Problem: Excessive spiking
   - Solutions:
     - Increase threshold
     - Add refractory period
     - Implement homeostatic plasticity

3. **Training Instability**
   - Problem: Unstable learning
   - Solutions:
     - Reduce learning rate
     - Adjust surrogate gradient parameters
     - Implement gradient clipping

## Next Steps

4. Experiment with different neuron models
5. Try various spike encoding schemes
6. Implement advanced learning rules
7. Explore deployment options

For more detailed information about specific components, refer to the Qualia SNN plugin documentation.