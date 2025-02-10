# Qualia-SNN Configuration Guide

## Overview 

Qualia-SNN extends Qualia's TOML configuration system to support Spiking Neural Networks (SNNs). This guide covers the SNN-specific configuration options and additions.

## Basic Structure for SNNs

Here's a minimal example for an SNN configuration:

```toml
[bench]
name = "snn_experiment"
seed = 42
first_run = 1
last_run = 1
plugins = ["qualia_plugin_snn"]  # Required for SNN support

[learningframework] 
kind = "SpikingJelly"  # SNN-specific framework

[dataset]
kind = "MNIST"

[model_template]
kind = "SCNN"  # Spiking CNN
epochs = 10
params.timesteps = 4  # Number of timesteps for spiking simulation

# SCNN architecture
[[model]]
name = "simple_scnn"
params.filters = [16, 32]
params.kernel_sizes = [3, 3]
params.pool_sizes = [2, 2]

[model.params.neuron]
kind = "IFNode"  # Integrate-and-Fire neuron
params.v_threshold = 1.0  # Firing threshold
```

## SNN-Specific Components

### 1. Learning Frameworks

```toml
[learningframework]
kind = "SpikingJelly"  # Base single-step framework
```

Supported SNN frameworks:
- `"SpikingJelly"`: Base single-step framework
- `"SpikingJellyMultiStep"`: Multi-step processing
- `"SpikingJellyTimeStepsInData"`: For data with timesteps dimension
- `"SpikingJellyMultiStepTimeStepsInData"`: Multi-step with timesteps in data

### 2. Model Architectures

```toml
[model_template]
kind = "SCNN"  # or "SResNet"
params.timesteps = 4  # Required for all SNN models
```

Supported SNN architectures:
- `"SCNN"`: Spiking Convolutional Neural Network
- `"SResNet"`: Spiking Residual Network
- `"QuantizedSCNN"`: Quantized Spiking CNN
- `"QuantizedSResNet"`: Quantized Spiking ResNet

### 3. Neuron Configuration

All SNN models require neuron configuration:

```toml
[model_template.params.neuron]
kind = "IFNode"  # Neuron type
params.v_threshold = 1.0  # Firing threshold
params.v_reset = false   # Soft reset
params.detach_reset = true
params.step_mode = "m"  # Multi-step mode
params.backend = "cupy"  # Backend for computation
```

Supported neuron types:
- `"IFNode"`: Integrate-and-Fire
- `"LIFNode"`: Leaky Integrate-and-Fire  
- `"ATIF"`: Adaptive Threshold IF
- `"QuantizedIFNode"`: Quantized IF
- `"QuantizedLIFNode"`: Quantized LIF
- `"QuantizedATIF"`: Quantized Adaptive Threshold IF

#### Detailed Neuron Parameters

IFNode/QuantizedIFNode:
```toml
[model_template.params.neuron]
kind = "IFNode"  # or "QuantizedIFNode" 
params.v_threshold = 1.0   # Membrane potential threshold
params.v_reset = false     # false for soft reset (subtract threshold)
                          # or float value for hard reset
params.detach_reset = true # Detach reset from computational graph
params.step_mode = "m"     # "s" for single-step, "m" for multi-step
params.backend = "cupy"    # "torch" or "cupy" backend
```

LIFNode/QuantizedLIFNode:
```toml
[model_template.params.neuron]
kind = "LIFNode"  # or "QuantizedLIFNode"
params.tau = 2.0           # Membrane time constant
params.decay_input = true  # Whether input should decay
# Plus all IFNode parameters above
```

ATIF/QuantizedATIF:
```toml
[model_template.params.neuron]
kind = "ATIF"  # or "QuantizedATIF"
params.v_threshold = 1.0
params.vth_init_l = 0.8  # Lower bound for threshold init
params.vth_init_h = 1.0  # Upper bound for threshold init
params.alpha = 1.0       # Sigmoid surrogate scale factor
# Plus all IFNode parameters above
```

### 4. SNN-Specific Preprocessing

Additional preprocessing modules for event-based data:

```toml
[[preprocessing]]
kind = "IntegrateEventsByFixedDuration"
params.duration = 1000  # Integration window

[[preprocessing]]
kind = "Split2TimeSteps"
params.chunks = 4  # Number of timesteps

[[preprocessing]]
kind = "Group2TimeStepsBySample"
params.timesteps = 4  # Timesteps per sample
```

SNN preprocessing modules:
- `"IntegrateEventsByFixedDuration"`: Converts event data to frames
- `"Split2TimeSteps"`: Splits data into timesteps
- `"Group2TimeStepsBySample"`: Groups frames by sample into timesteps

### 5. SNN-Specific Postprocessing

```toml
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

Energy estimation methods:
- `"ICONIP"`: Uses fixed 32-bit values (from ICONIP 2022 paper)
- `"saturation"`: Uses closest predefined bitwidth values
- `"linear"`: Linear interpolation between 8-bit and 32-bit values
- `"quadratic"`: Quadratic interpolation

SRAM estimation types:
- `"old"`: ICONIP 2022 method (single access per data)
- `"new"`: T. Louis method (packed data over 64-bit access)

## Step Modes and Learning Frameworks

The relationship between step modes and learning frameworks is important:

### 1. Single-Step Mode (`"s"`):
```toml
[learningframework]
kind = "SpikingJelly"

[model_template.params.neuron]
params.step_mode = "s"
```
- Processes one timestep at a time
- Lower memory usage
- More suitable for deployment

### 2. Multi-Step Mode (`"m"`):
```toml
[learningframework]
kind = "SpikingJellyMultiStep"

[model_template.params.neuron]
params.step_mode = "m"
```
- Processes all timesteps at once
- Faster training
- Higher memory usage

### 3. TimeSteps in Data:
```toml
[learningframework]
kind = "SpikingJellyTimeStepsInData"  # or "SpikingJellyMultiStepTimeStepsInData"

[model_template.params]
timesteps = 4  # Must match data timesteps
```
- For pre-processed data with timestep dimension
- Compatible with both single and multi-step processing

## Event-Based Data Processing

For event-based datasets like DVS128 Gesture, here's a complete preprocessing pipeline:

```toml
# First convert events to frames
[[preprocessing]]
kind = "IntegrateEventsByFixedDuration"
params.duration = 1000  # Integration window in timestamp units

# Then organize frames into timesteps
[[preprocessing]]
kind = "Group2TimeStepsBySample"
params.timesteps = 4   # Number of timesteps per sample

# Configure appropriate learning framework
[learningframework]
kind = "SpikingJellyTimeStepsInData"

# Model must match timesteps
[model_template]
params.timesteps = 4  # Must match preprocessing
```

## Quantization-Specific Configuration

For quantized SNNs, additional configuration is needed:

```toml
[model_template]
kind = "QuantizedSCNN"  # or "QuantizedSResNet"

[model_template.params.quant_params]
bits = 8               # Bit width
force_q = true         # Force quantization
LSQ = false           # Use LSQ quantization
roundtype = "floor"   # Rounding mode

# Quantized neurons must be used
[model_template.params.neuron]
kind = "QuantizedIFNode"  # or "QuantizedLIFNode", "QuantizedATIF"

# Post-processing for analysis
[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8  # Must match quantization bits
```

## Common Architecture Configurations

### 1. SCNN for Classification:
```toml
[model_template]
kind = "SCNN"
params.filters = [64, 64, 128, 128, 256, 256, 256]
params.kernel_sizes = [3, 3, 3, 3, 3, 3, 3]
params.paddings = [1, 1, 1, 1, 1, 1, 1]
params.strides = [1, 1, 1, 1, 1, 1, 1]
params.pool_sizes = [0, 2, 0, 2, 0, 0, 2]
params.dropouts = 0
params.fc_units = [4096, 4096]
params.batch_norm = true
```

### 2. SResNet for Deep Architecture:
```toml
[model_template]
kind = "SResNet"
params.filters = [64, 64, 128, 256, 512]
params.kernel_sizes = [7, 3, 3, 3, 3]
params.paddings = [3, 1, 1, 1, 1]
params.strides = [2, 1, 1, 1, 1]
params.num_blocks = [2, 2, 2, 2]
params.prepool = 1
params.postpool = "max"
params.batch_norm = true
params.force_projection_with_stride = true
```

## Best Practices

1. Choose appropriate number of timesteps based on your task
2. Consider using batch normalization with SNNs
3. Start with single-step mode for development, then move to multi-step if needed
4. Monitor spike rates during training
5. When using quantization, test different bit widths and thresholds
6. Consider energy estimation for deployment scenarios
7. Use preprocessing modules appropriate for your data type (event-based vs frame-based)