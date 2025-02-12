# Energy Estimation Metric Documentation

## Overview

The Energy Estimation Metric is an analytical tool for estimating the energy consumption of Spiking Neural Networks (SNNs) and traditional neural networks. It is based on the research paper "An Analytical Estimation of Spiking Neural Networks Energy Efficiency" (Lemaire et al., ICONIP 2022). This metric provides detailed insights into various energy consumption aspects of your neural network, including memory operations, computational operations, and spike-based calculations.

## How It Works

The Energy Estimation Metric analyzes several key components of energy consumption:

1. **Memory Operations Energy**:
   - Memory potential (mem_pot): Energy for reading/writing neuron potentials
   - Memory weights (mem_weights): Energy for reading weights
   - Memory bias (mem_bias): Energy for reading biases
   - Memory I/O (mem_io): Energy for input/output operations

2. **Computational Operations Energy**:
   - Operations (ops): Energy for synaptic operations
   - Address computation (addr): Energy for event address calculation

3. **Spike-Based Metrics**:
   - Input spike rate: Average spikes per input per timestep
   - Output spike rate: Average spikes per output per timestep

The metric uses configurable energy values based on a 45nm ASIC implementation, with default values from Mark Horowitz's ISSCC 2014 paper.

## Configuration

To add the Energy Estimation Metric to your project, include it in your configuration file (config.toml) under the postprocessing section:

``` toml

[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8  # Memory width in bits
params.fifo_size = 64  # FIFO buffer size
params.total_spikerate_exclude_nonbinary = true

[postprocessing.params.op_estimation_type]
add = "ICONIP"      # Energy estimation method for addition
mul = "saturation"  # Energy estimation method for multiplication

params.sram_estimation_type = "new"  # SRAM estimation algorithm

```

### Configuration Parameters

1. **Required Parameters**:
   - `mem_width`: Bit width for memory operations (e.g., 8 for 8-bit quantization)
   - `fifo_size`: Size of the input/output FIFOs for each layer
   - `total_spikerate_exclude_nonbinary`: Whether to exclude non-binary inputs/outputs from total spike rate computation

2. **Optional Parameters**:
   - `op_estimation_type`: Method for estimating operation energy values
     - Supported types: "ICONIP", "saturation", "linear", "quadratic"
     - Can be specified separately for addition and multiplication
   - `sram_estimation_type`: Algorithm for SRAM energy estimation
     - "old": ICONIP 2022 method (single access per data)
     - "new": T. Louis method (packed data over 64-bit access)

### Energy Estimation Methods

The metric supports four different methods for estimating operation energy:

1. **ICONIP**: Uses fixed 32-bit values from the ICONIP 2022 paper
2. **Saturation**: Uses closest predefined bitwidth values
3. **Linear**: Linear interpolation between 8-bit and 32-bit values
4. **Quadratic**: Quadratic interpolation between reference points

## Usage

The Energy Estimation Metric automatically runs during model evaluation. It will generate two types of output:

1. **Console Output**: A detailed table showing energy consumption per layer
2. **CSV Log**: Detailed metrics saved in `logs/<bench.name>/EnergyEstimationMetric/`

### Reading the Results

The output includes the following metrics for each layer:

```
Layer       | EMemPot | EMemWeights | EMemBias | EMemIO | EMemTotal | EOps | EAddr | EOpsAddr | ETotal | SNN | Input SR | Output SR
------------|---------|-------------|----------|--------|-----------|------|-------|----------|--------|-----|----------|----------
conv1       | 0.0023 | 0.0156      | 0.0012   | 0.0089 | 0.0280    | 0.15 | 0.02  | 0.17     | 0.198  | Yes | 0.142    | 0.086
```

- All energy values are in nanojoules (nJ)
- SR = Spike Rate (average spikes per neuron per timestep)
- SNN indicates if the layer is processed as a spiking layer

### Supported Layer Types

The metric supports analysis of:

1. **Convolutional Layers**:
   - Standard convolutions
   - Spiking convolutions
   - Quantized variants

2. **Dense Layers**:
   - Fully connected layers
   - Spiking dense layers
   - Quantized variants

3. **Additional Layers**:
   - Batch normalization
   - Pooling layers
   - Addition layers (for residual connections)

## Complete Working Example

Let's walk through a complete, practical example using the Google Speech Commands (GSC) dataset. This example demonstrates how to integrate energy estimation into a speech recognition system using a Spiking Neural Network:

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

[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8  # Memory width in bits
params.fifo_size = 64  # FIFO buffer size
params.total_spikerate_exclude_nonbinary = true

[postprocessing.params.op_estimation_type]
add = "ICONIP"      # Energy estimation method for addition
mul = "saturation"  # Energy estimation method for multiplication

params.sram_estimation_type = "new"  # SRAM estimation algorithm

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
params.filters = [16, 16, 32, 64]
params.kernel_sizes = [40, 3, 3, 3]
params.paddings = [20, 1, 1, 1]
params.strides = [8, 1, 1, 1]
params.pool_sizes = [4, 4, 4, 4]
params.postpool = 3
params.dropouts = [0, 0, 0, 0, 0.5]
params.fc_units = []
params.batch_norm = true
disabled = false
```

### Understanding the Example

Let's break down the key components of this configuration:

1. **Energy Estimation Setup**: 
   The energy estimation configuration is tailored for audio processing:
   - The 8-bit memory width matches common hardware implementations for audio processing
   - The 64-entry FIFO buffer provides balanced temporal data handling
   - Different operation estimation types for addition (ICONIP) and multiplication (saturation) reflect the varying complexity of operations
   - Modern SRAM estimation using the T. Louis method optimizes for actual hardware behavior

2. **Network Architecture**:
   The Spiking CNN is designed for efficient audio processing:
   - Four convolutional layers with increasing filter counts [16, 16, 32, 64]
   - Initial large kernel (size 40) for processing audio input
   - Regular pooling operations (size 4) for dimensionality reduction
   - Leaky Integrate-and-Fire neurons with carefully tuned parameters

3. **Temporal Processing**:
   The configuration accounts for the temporal nature of speech:
   - Multi-step processing enabled through SpikingJellyMultiStep
   - Four timesteps for temporal processing
   - Membrane time constant of 2.0 for the LIF neurons

When you run this configuration, the Energy Estimation Metric will analyze:
- The energy impact of temporal audio processing
- Energy consumption patterns across network layers
- The effectiveness of the pooling strategy
- Overall efficiency of the spiking neural implementation

This example serves as a practical template for implementing energy estimation in speech recognition applications, but the principles can be adapted for other types of neural networks and applications.

## Best Practices

1. **Memory Width Selection**:
   - Match `mem_width` to your model's quantization bits
   - Use 32 for full-precision models
   - Use 8 or 16 for quantized models

2. **FIFO Size**:
   - Choose based on your hardware implementation
   - Larger sizes increase memory energy but may improve throughput
   - Common values range from 32 to 128

3. **Energy Estimation Method**:
   - Use "ICONIP" for comparison with the paper results
   - Use "saturation" for more realistic estimates with quantization
   - Use "linear" or "quadratic" for more precise interpolation

4. **SRAM Estimation**:
   - Use "new" for modern hardware implementations
   - Use "old" for comparison with ICONIP 2022 results

## Troubleshooting

Common issues and solutions:

1. **High Energy Consumption**:
   - Check if your model uses appropriate quantization
   - Verify spike rates are reasonable
   - Consider reducing network size or complexity

2. **Unexpected Spike Rates**:
   - Verify neuron thresholds are properly set
   - Check input normalization
   - Ensure correct number of timesteps

3. **Missing Metrics**:
   - Verify all required parameters are set
   - Check if layer types are supported
   - Ensure proper plugin installation

## References

1. Lemaire et al., "An Analytical Estimation of Spiking Neural Networks Energy Efficiency," ICONIP 2022
2. Horowitz, "Computing's Energy Problem (and what we can do about it)," ISSCC 2014