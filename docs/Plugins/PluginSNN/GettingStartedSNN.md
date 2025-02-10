# Getting Started with Qualia-SNN

## Introduction
This guide will walk you through creating your first Spiking Neural Network (SNN) project using Qualia-SNN. We'll build a speech recognition system using the Google Speech Commands (GSC) dataset, converting the audio data into spike-based representations that can be processed by our SNN.

## Prerequisites

Before starting, ensure you have:
- Python (version 3.9-3.12, recommended: 3.12)
- Git installed

## Installation and Project Setup

Let's set up our environment:

```bash
# Create a project directory
mkdir qualia-snn-gsc
cd qualia-snn-gsc

# Download and extract GSC dataset to a dedicated directory
mkdir -p data
cd data
wget https://storage.googleapis.com/download.tensorflow.org/data/speech_commands_v0.02.tar.gz
mkdir speech_commands
tar -xf speech_commands_v0.02.tar.gz -C speech_commands
cd ../..
```

After these commands, your project structure should look like this:
```
qualia-snn-gsc/
├── data/
│   └── speech_commands/
│       ├── testing_list.txt
│       ├── validation_list.txt
│       ├── zero/
│       ├── one/
│       └── ... (other word directories)
├── qualia-plugin-snn/
└── config.toml              # We'll create this next
```

## Creating the Configuration File

Create a new file named `config.toml` in your project root directory with the following content:

```toml
[bench]
name = "GSC_SNN_example"
seed = 42
first_run = 1
last_run = 1
plugins = ["qualia_plugin_snn"]  # Enable SNN support

[learningframework]
kind = "SpikingJellyMultiStep"  # Multi-step processing for efficiency

[deploy]
target = "Linux"
converter.kind = "QualiaCodeGen"
quantize = ["float32"]
optimize = [""]
compress = [1]

[dataset]
kind = "GSC"
params.path = "data/speech_commands"  # Path to extracted dataset
params.variant = "v2"
params.subset = "digits"
params.train_valid_split = true

[[preprocessing]]
kind = "Class2BinMatrix"

# Model configuration
[model_template]
kind = "SCNN"  # Spiking CNN
params.dims = 1
epochs = 8
batch_size = 512
params.timesteps = 4  # Number of timesteps for temporal processing

# Spiking neuron configuration
[model_template.params.neuron]
kind = "LIFNode"  # Leaky Integrate-and-Fire neuron
params.tau = 2.0  # Membrane time constant
params.v_threshold = 1.0
params.v_reset = false  # Soft reset
params.detach_reset = true
params.step_mode = "m"  # Multi-step mode
params.backend = "torch"  # Use GPU acceleration if available

[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

[[model]]
name = "gsc_cnn_m5_smaller"
params.filters 		= [16, 16, 32, 64]
params.kernel_sizes	= [40, 3, 3, 3]
params.paddings		= [20, 1, 1, 1]
params.strides		= [8, 1, 1, 1]
params.pool_sizes	= [4, 4, 4, 4]
params.postpool		= 3
params.dropouts     = [0, 0, 0, 0, 0.5]
params.fc_units		= []
params.batch_norm	= true
disabled = false
```

## Understanding the Configuration

Let's break down the key components of our SNN configuration:

The learning framework uses SpikingJelly's multi-step mode, which processes all timesteps at once for efficient training. Our Leaky Integrate-and-Fire (LIF) neurons are configured with soft reset behavior, meaning they subtract the threshold value when firing instead of resetting to zero. This often leads to better training performance.

The preprocessing pipeline converts audio into a format suitable for spiking networks:
1. MFCC transforms raw audio into mel-frequency cepstral coefficients, which capture important audio features
2. DatamodelConverter prepares the data structure for our SNN
3. Class2BinMatrix converts our class labels into one-hot encoded vectors

Our SNN architecture is a three-layer convolutional network with pooling layers and batch normalization, which helps stabilize training with spiking neurons.

## Running the Experiment

Now let's train our spiking neural network:

```bash
# First, preprocess the audio data
qualia config.toml preprocess_data

# Then train the network
qualia config.toml train

# Prepare deploy
qualia ./config.toml prepare_deploy

# Deploy the networks and evaluate
qualia ./config.toml deploy_and_evaluate
```

## Monitoring Results

You can find your experiment outputs in these locations:
- Training logs: `logs/GSC_SNN_example/learningmodel/`
- Trained model weights: `out/learningmodel/`
- Processed dataset: `out/data/GSC/`

## Analyzing Network Behavior

To understand how your SNN is performing, you can add energy estimation analysis by adding this to your configuration:

```toml
[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8
params.fifo_size = 64
params.total_spikerate_exclude_nonbinary = true
```

This will provide insights into your network's behavior, including average spike rates per layer and estimated energy consumption.

## Next Steps

Once you've successfully run this basic example, you can explore:

1. Different neuron types: Try IF (Integrate-and-Fire) or ATIF (Adaptive Threshold) neurons
2. Alternative architectures: Experiment with SResNet for deeper networks
3. Quantization: Reduce energy consumption by quantizing weights and activations
4. Advanced preprocessing: Test different MFCC parameters or alternative audio features

The Qualia-SNN framework offers many possibilities for experimentation and optimization. You can refer to the Qualia-SNN configuration guide for more advanced features and options to enhance your SNN's performance.

Remember that training SNNs often requires more patience than traditional neural networks, as the discrete nature of spikes can make learning more challenging. Don't be discouraged if you need to adjust learning rates or training duration to achieve optimal results.