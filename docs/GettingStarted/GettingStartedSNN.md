# Getting Started with Qualia-Plugin-SNN: UCI HAR Example

## Introduction

This guide demonstrates how to use Qualia-Plugin-SNN with the UCI Human Activity Recognition (HAR) dataset. Unlike the event-based DVS128 Gesture dataset, UCI HAR provides traditional sensor data from smartphone accelerometers and gyroscopes. We'll show how to convert this time-series data into a format suitable for spiking neural networks, demonstrating the versatility of SNNs beyond neuromorphic sensors.

## Installation

Before we can work with sensor data using spiking neural networks, we need to set up our development environment. The installation process ensures we have all the necessary components for processing time-series data with SNNs.

### Step 1: Clone the Repository

First, let's get the latest version of Qualia-Plugin-SNN. This gives us access to all the SNN components we'll need for processing sensor data:

```bash
git clone https://github.com/LEAT-EDGE/qualia-plugin-snn.git
cd qualia-plugin-snn
```

### Step 2: Install the Plugin

Now we'll install the plugin in development mode. This approach is particularly useful when working with different datasets like UCI HAR, as it allows you to modify preprocessing steps if needed:

```bash
# Using pip
pip install -e .

# Or using uv (a faster alternative to pip)
uv pip install -e .
```

The `-e` flag creates an "editable" installation, meaning Python will use the code directly from your cloned repository. This is especially helpful if you want to experiment with different preprocessing approaches for the sensor data.

### Step 3: Create Your Project

Let's create a dedicated directory for our HAR (Human Activity Recognition) project:

```bash
mkdir qualia-snn-har
cd qualia-snn-har
```

### Step 4: Enable the Plugin

In your project's configuration file, we need to enable the plugin. Create a `config.toml` file and add:

```toml
[bench]
name = "uci-har-snn"
plugins = ["qualia_plugin_snn"]  # Enable the SNN plugin
```

### Verification

Let's verify our installation by importing the necessary components in Python:

```python
import qualia_plugin_snn
from qualia_plugin_snn.preprocessing import Split2TimeSteps  # We'll use this for sensor data
```

If no errors occur, we're ready to start processing sensor data with spiking neural networks. The successful import of `Split2TimeSteps` is particularly important as we'll use it to convert our continuous sensor signals into discrete timesteps for the SNN.

## Dataset Preparation

The UCI HAR dataset contains readings from smartphone sensors while subjects performed various activities like walking, sitting, and climbing stairs.

### Downloading the Dataset

1. Download the dataset from the UCI Machine Learning Repository:
   - Visit [https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones)
   - Click "Download" to get the ZIP file

2. Set up your project structure:
```bash
mkdir qualia-snn-har
cd qualia-snn-har
mkdir -p data/UCI_HAR
```

1. Extract the dataset:
```bash
unzip UCI\ HAR\ Dataset.zip -d data/UCI_HAR/
```

Your directory structure should look like this:
```
qualia-snn-har/
├── data/
│   └── UCI_HAR/
│       └── UCI HAR Dataset/
│           ├── train/
│           │   ├── Inertial Signals/
│           │   ├── X_train.txt
│           │   ├── y_train.txt
│           │   └── subject_train.txt
│           ├── test/
│           │   ├── Inertial Signals/
│           │   ├── X_test.txt
│           │   ├── y_test.txt
│           │   └── subject_test.txt
│           └── README.txt
└── config.toml          # We'll create this next
```

### Understanding the Data

The dataset provides:
- Raw signals from accelerometer and gyroscope (in Inertial Signals/)
- Pre-processed 561-feature vectors (X_train.txt, X_test.txt)
- Activity labels (y_train.txt, y_test.txt)
- Six activities: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING
- 30 subjects performing activities
- Data collected at 50Hz sampling rate

## Configuration

Create a `config.toml` file with the following content:

```toml
[bench]
name = "UCI-HAR_SCNN_example"
seed = 42
first_run = 1
last_run = 1
plugins = ["qualia_plugin_snn"]

[learningframework]
kind = "SpikingJelly"

[dataset]
kind = "UCI_HAR"
params.path = "data/UCI_HAR/UCI HAR Dataset/"
params.variant = "raw"  # Use raw sensor data instead of features

# Convert sliding windows into timesteps
[[preprocessing]]
kind = "Split2TimeSteps"
params.chunks = 16     # Split each window into 16 timesteps

[model_template]
kind = "SCNN"
epochs = 100
batch_size = 32
params.dims = 1        # Use 1D convolutions for time series

# Configure spiking neuron
params.neuron.kind = "LIFNode"             # Leaky Integrate-and-Fire neuron
params.neuron.params.v_threshold = 1.0     # Firing threshold
params.neuron.params.tau = 2.0             # Membrane time constant
params.neuron.params.v_reset = None        # Soft reset mode
params.neuron.params.detach_reset = true   
params.neuron.params.step_mode = "m"       # Multi-step mode
params.timesteps = 16                      # Match preprocessing chunks

# Configure the optimizer
[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

# Learning rate scheduler
[model_template.optimizer.scheduler]
kind = "CosineAnnealingLR"
params.T_max = 100

# 1D-SCNN architecture
[[model]]
name = "uci-har_scnn"
# First layer processes raw sensor data (9 channels: acc_xyz, gyro_xyz, total_acc_xyz)
params.filters = [64, 128, 128]            # Number of filters per layer
params.kernel_sizes = [7, 5, 3]            # Decreasing kernel sizes
params.paddings = [3, 2, 1]                # Same padding
params.strides = [1, 1, 1]                 # No striding
params.pool_sizes = [2, 2, 2]              # Temporal pooling
params.fc_units = [256]                    # One hidden FC layer
params.batch_norm = true                   # Use batch normalization

# Energy estimation
[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8
params.fifo_size = 256

# Optional: Deployment configuration
[deploy]
target = "Linux"
converter.kind = "QualiaCodeGen"
quantize = ["int8"]
```

### Key Configuration Points

Let's examine some important aspects of this configuration:

2. **Raw Data Processing**: We use `params.variant = "raw"` to work with raw sensor signals instead of pre-computed features. This gives us more control over the learning process and better matches neuromorphic principles.

3. **Time Window to Timesteps**: The `Split2TimeSteps` preprocessor divides each sliding window of sensor data into discrete timesteps that our SNN can process. This converts traditional time-series data into a format suitable for spiking networks.

4. **1D Convolutions**: We set `params.dims = 1` since we're working with time-series data. The convolution kernels will slide along the time dimension while processing all sensor channels.

5. **LIF Neurons**: We use Leaky Integrate-and-Fire neurons (`LIFNode`) which are well-suited for processing continuous sensor data due to their temporal integration properties. The leak helps prevent signal accumulation from continuous sensor streams.

6. **Architecture Design**: The network uses:
   - Large initial kernel (size 7) to capture temporal patterns
   - Decreasing kernel sizes for hierarchical feature extraction
   - Regular pooling to reduce temporal dimension
   - Batch normalization to handle varying sensor intensities

## Running the Experiment

Execute these commands in sequence:

```bash
# 1. Preprocess the dataset
qualia config.toml preprocess_data

# 2. Train the spiking neural network
qualia config.toml train

# Optional: Analyze energy consumption
qualia config.toml postprocess

# Optional: Deploy and evaluate
qualia config.toml prepare_deploy
qualia config.toml deploy_and_evaluate
```

## Understanding the Results

You can find various outputs in these locations:
- Processed dataset: `out/data/UCI_HAR_raw/`
- Model weights: `out/learningmodel/`
- Training logs: `log/UCI-HAR_SCNN_example/learningmodel/`
- Energy metrics: `log/UCI-HAR_SCNN_example/EnergyEstimationMetric/`
- Deployment files: `out/QualiaCodeGen/`

The energy metrics will show how this approach compares to traditional deep learning in terms of computational efficiency.

## Next Steps

Try experimenting with:
7. Different neuron types (IF, ATIF) to compare performance
8. Various temporal encoding schemes in the preprocessing
9. Architecture modifications like skip connections
10. Different sensor channel combinations
11. Quantization for more efficient deployment

This example demonstrates how SNNs can be applied to traditional sensor data, opening up possibilities for energy-efficient processing of IoT and wearable device data.