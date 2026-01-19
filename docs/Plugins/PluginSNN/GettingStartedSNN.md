# Getting Started with Qualia-SNN

## Introduction
This guide will walk you through creating your first Spiking Neural Network (SNN) project using Qualia-SNN. We'll build a speech recognition system using the Google Speech Commands V2 (GSC) dataset, converting the audio data into spike-based representations that can be processed by our SNN.

## Prerequisites

Before starting, ensure you have:
- Qualia-core and have followed the [Installation](../../GettingStarted/Installation)
- Python (version 3.9-3.12, recommended: 3.12)
- Git installed
## Installation
After installing Qualia-core, follow the [Installation of the SNN plugin](./InstallationSNN).

## Project Setup
Let's set up our working environment:  
For each Qualia project, we recommend working in a dedicated project directory.


```bash
# Create a project directory 'qualia-snn-gsc' where you want.
mkdir -p qualia-snn-gsc/data/speech_commands
cd qualia-snn-gsc/data

# Download and extract GSC dataset to a dedicated directory
wget https://storage.googleapis.com/download.tensorflow.org/data/speech_commands_v0.02.tar.gz
tar -xf speech_commands_v0.02.tar.gz -C speech_commands
cd ../
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
└── config.toml              # We'll create this next
```

*Tips:* You can use symbolic links in your working folders to point toward a 'dataset' folder with: 
```bash
ln -sf {path-to-your-dataset-folder}/speech_commands data/
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
converter.params.timestep_mode = "duplicate" 
quantize = ["int16"]
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

[[preprocessing]]
kind = "Normalize"
params.method = "z-score"

[[preprocessing]]
kind = "MFCC"
params.sample_rate = 16_000
params.n_mfcc = 10
params.log_mels = true
params.melkwargs.n_fft = 1_024
params.melkwargs.n_mels = 40
params.melkwargs.win_length = 640
params.melkwargs.hop_length = 320
params.melkwargs.f_min = 20
params.melkwargs.f_max = 4_000
params.melkwargs.pad = 320
params.melkwargs.center = false

# Model configuration
[model_template]
kind = "SCNN"  # Spiking CNN
params.dims      = 1
epochs           = 8
batch_size       = 512
params.timesteps = 4  # Number of timesteps for temporal processing
params.input_shape  = [ 49, 10 ]

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
name = "gsc_scnn_tutorial"
params.filters 		= [24, 32, 48, 64]
params.kernel_sizes	= [5, 5, 5, 5]
params.paddings		= [2, 2, 2, 2]
params.strides		= [2, 2, 2, 2]
params.pool_sizes	= [0, 0, 0, 0]
params.dropouts     = [0, 0, 0, 0]
params.fc_units		= []
params.gsp          = true
params.batch_norm	= true
disabled = false
```

## Understanding the Configuration

Let's break down the key components of our SNN configuration:

The learning framework uses SpikingJelly's multi-step mode, which processes all timesteps at once for efficient training. Our Leaky Integrate-and-Fire (LIF) neurons are configured with soft reset behavior, meaning they subtract the threshold value when firing instead of resetting to zero. This often leads to better training performance.

The preprocessing pipeline converts audio into a format suitable for spiking networks:
1. MFCC transforms raw audio into mel-frequency cepstral coefficients, which capture important audio features.
2. DatamodelConverter prepares the data structure for our SNN.
3. Class2BinMatrix converts our class labels into one-hot encoded vectors 
4. In the [model_template] "kind" you must refer to a SNN architecture class.
5. SNN models need a timesteps parameter and spiking [neuron] configuration.
6. 'gsp' stands for Global Sum Pooling, which means that after applying convolution, we sum over the remaining spatial dimension(s) to match the desired output dimension.

Our SNN architecture is a four-layer convolutional network with batch normalization, which helps stabilize training with spiking neurons.

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

At the end, you should reach around 91% accuracy with this 28.8k parameter network after 8 epochs.

## Monitoring Results

You can find your experiment outputs in these locations:
- Training logs: `logs/GSC_SNN_example/learningmodel/`
- Trained model weights: `out/learningmodel/`
- Processed dataset: `out/data/GSC/`

## Analyzing Network Behavior

To understand how your SNN is performing as if it were on neuromorphic hardware, you can add an operation counter and an energy estimation analysis by adding this to your configuration:

```toml
[[postprocessing]]
kind = "FuseBatchNorm"
export = true

[[postprocessing]]
kind = "QuantizationAwareTraining"
export = true
params.epochs       = 0     # 0 for PTQ, some epochs for QAT 
params.batch_size   = 512

[postprocessing.params.model.params]
quant_params.bits           = 16
quant_params.force_q        = 8
quant_params.quantype       = "fxp"
quant_params.roundtype      = "floor"
quant_params.range_setting  = "minmax"
quant_params.LSQ            = false
quant_params.input.quant_enable = false

[[postprocessing]]
kind = "OperationCounter"

[[postprocessing]]
kind = "EnergyEstimationMetric"
params.mem_width = 8
params.fifo_size = 64
params.total_spikerate_exclude_nonbinary = true
```

1. The 'timestep_mode' used in the converter helps to indicate how the data will be used in the timesteps. The 'duplicate' mode will duplicate the same input or all timesteps will the 'iterate' mode will iterate on the data for different inputs at each timestep.
2. The "FuseBatchNorm" [postprocessing] allows you to fuse Batch normalization layers with convolution layers, allowing SNN deployment on hardware (by removing the float computation between these layers).
3. We use here the [postprocessing] "QuantizationAwareTraining" to quantize our network in 16-bit fixed point.
4. The [postprocessing] "OperationCounter" will output the analysis of the operations in our network after a `qualia config.toml train` command.
5. The [postprocessing] "EnergyEstimationMetric" will provide insights into your network's behavior, including average spike rates per layer and estimated energy consumption after a `qualia config.toml train` command.


*Tips:* You can load and test only a model by adding load and train options in the model section like:
```
[[model]]
name = "gsc_scnn_tutorial"
load    = true
train   = false
...
```
These options will load the previously trained weights and test only, without training the model.

All the information will be available in the following folders:
- Fused and Quantized model weights: `out/learningmodel/`
- OperationCounter logs: `logs/GSC_SNN_example/OperationCounter/`
- EnergyEstimationMetric logs: `logs/GSC_SNN_example/EnergyEstimationMetric/`

## Next Steps

Once you've successfully run this basic example, you can explore:

1. Different neuron types: Try IF (Integrate-and-Fire) or ATIF (Adaptive Threshold) neurons.
2. Alternative architectures: Experiment with SResNet for deeper networks.
3. Quantization: Reduce energy consumption by quantizing weights and activations.
4. Advanced preprocessing: Test different MFCC parameters or alternative audio features.

The Qualia-SNN framework offers many possibilities for experimentation and optimization. You can refer to the Qualia-SNN configuration guide for more advanced features and options to enhance your SNN's performance.

Remember that training SNNs often requires more patience than traditional neural networks, as the discrete nature of spikes can make learning more challenging. Don't be discouraged if you need to adjust learning rates or training duration to achieve optimal results.

You can also deploy and evaluate your SNNs on our Qualia-Bench online platform to share and compare your results deployed on neuromorphic hardware with our Benchmark.  
[QualianBench Neuromorphic Benchmark](GettingStatedQualiabench.md)