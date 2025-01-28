# Qualia Configuration Guide
## Overview

Qualia uses TOML configuration files to define machine learning experiments. This guide explains each configuration section and its available options.

## Basic Structure

A configuration file consists of several sections. Here's a minimal example:

```toml
[bench]
name = "my_experiment"
seed = 42
first_run = 1
last_run = 1

[learningframework]
kind = "PyTorch"

[dataset]
kind = "UCI_HAR"

[model_template]
kind = "CNN"
epochs = 10

# CNN architecture
[[model]]
name = "uci-har_cnn_simple"
params.filters = [5, 5]        # Two conv layers with 5 filters each
params.kernel_sizes = [2, 2]   # 2x2 kernels
params.pool_sizes = [2, 0]     # Pooling after first conv layer
```

## Required Sections

### 1. Bench Settings

```toml
[bench]
name = "my_experiment"
seed = 42
first_run = 1
last_run = 1
plugins = ["qualia_plugin_snn"]  # Optional
```

Available settings:
- `name`: String, experiment name for logging
- `seed`: Integer, random seed for reproducibility
- `first_run/last_run`: Integer, to run multiple training sessions of the same models for statistical purposes
- `plugins`: Optional list of plugin names
	- `"qualia_plugin_snn"`
	- `"qualia_plugin_som"`
	- `"qualia_plugin_spleat"`
### 2. Learning Framework

```toml
[learningframework]
kind = "PyTorch"
```

Supported frameworks:
- `"PyTorch"`
- `"Keras"`

### 3. Dataset Configuration

```toml
# UCI_HAR example
[dataset]
kind = "UCI_HAR"
params.variant = "raw"
params.path = "data/UCI HAR Dataset/"
```

```toml
# CIFAR-10 example
[dataset]
kind = "CIFAR10"
params.path = "data/cifar10/"
params.dtype = "float32"
```

```toml
# CORe50 example
[dataset]
kind = "CORe50"
params.path = "data/core50/"
params.variant = "category"
```

```toml
# GSC example
[dataset]
kind = "GSC"
params.path = "data/speech_commands/"
params.variant = "v2"
params.subset = "digits"
params.train_valid_split = true
```

```toml
# WSMNIST example
[dataset]
kind = "WSMNIST"
params.path = "data/wsmnist/"
params.variant = "spoken"
```

```toml
# BrainMIX example
[dataset]
kind = "BrainMIX"
params.path = "data/brainmix/"
```

Supported dataset:

- `"BrainMIX"`: Brain dataset ([more information](https://arxiv.org/abs/2405.02308))
    - `path`: Directory containing:
        - `traindata48_shuffled.pickle`
        - `valid48.pickle`
    - Data: Signal and truth values
    - Note: Does not support validation set

- `"CIFAR10"`: CIFAR-10 image dataset
    - `path`: Directory containing CIFAR-10 data batches:
        - `data_batch_1` through `data_batch_5`
        - `test_batch`
    - `dtype`: Data type for arrays (default: 'float32')
    - Data: 32x32x3 RGB images
    - Note: Does not support validation set

- `"CORe50"`: Core50 object recognition dataset
    - `path`: Path to dataset directory containing:
        - `core50_imgs.npz`
        - `paths.pkl`
    - `variant`: One of:
        - `"object"`: 50 object classes
        - `"category"`: 10 category classes
    - `sessions`: Optional list of sessions to include in training (default: all except test sessions)
    - Note: Uses sessions s3, s7, s10 for testing

- `"EZBirds"`: Bird sound recognition dataset
    - `path`: Directory containing:
        - WAV files
        - `labels.json`
    - Data: Audio samples
    - Note: Uses 48000 samples per record

- `"EllcieHAR"`: UCA-EHAR Human Activity Recognition dataset ([link 1](https://zenodo.org/records/5659336) and [link 2](https://www.mdpi.com/2076-3417/12/8/3849))
    - `path`: Path to dataset directory (CSV files)
    - `variant`: One of:
        - `"PACK-2"`
        - `"UCA-EHAR"`
    - `files`: Optional list of files to include
    - Data: Accelerometer (Ax,Ay,Az), Gyroscope (Gx,Gy,Gz), Barometer (P)
    - Activities: STANDING, STAND_TO_SIT, SITTING, SIT_TO_STAND, WALKING, SIT_TO_LIE, LYING, LIE_TO_SIT, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, RUNNING, DRINKING, DRIVING
    - Note: Does not support validation set

- `"GSC"`: Google Speech Commands dataset
    - `path`: Directory containing WAV files
    - `variant`: Only `"v2"` supported
    - `subset`: One of:
        - `"digits"`: Only digit commands (0-9)
        - `"no_background_noise"`: All commands except background noise
    - `train_valid_split`: Boolean, whether to use validation set (default: False)
    - `record_length`: Number of samples per record (default: 16000)
    - Data: Audio samples
    - Note: For `no_background_noise`: includes 35 commands (backward, bed, bird, cat, dog, down, etc.)

- `"GTSRB"`: German Traffic Sign Recognition Benchmark
    - `path`: Directory containing:
        - `Final_Training/Images/`: Training images (.ppm)
        - `Final_Test/Images/`: Test images (.ppm)
        - `GT-final_test.csv`: Test ground truth
    - `width`: Target image width (default: 32)
    - `height`: Target image height (default: 32)
    - Data: RGB images resized to specified dimensions
    - Note: Does not support validation set

- `"HD"`: Heidelberg Digits audio dataset
    - `path`: Directory containing:
        - `audio/`: FLAC audio files
        - `test_filenames.txt`: List of test files (for default variant)
    - `variant`: Optional, one of:
        - Not specified: Uses test_filenames.txt
        - `"by-subject"`: Split by speaker IDs
    - `test_subjects`: List of subject IDs (required when variant="by-subject")
    - Data: Audio samples, zero-padded to longest sample
    - Note: Does not support validation set

- `"UCI_HAR"`: UCI Human Activity Recognition dataset
    - `path`: Directory containing UCI HAR Dataset
    - `variant`: One of:
        - `"features"`: Preprocessed features
        - `"raw"`: Raw sensor data from Inertial Signals
    - Data: 
        - Raw: Body acceleration, gyroscope, total acceleration (x,y,z)
        - Features: Preprocessed feature vectors
    - Activities: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LYING
    - Note: Does not support validation set

- `"WSMNIST"`: Written and Spoken MNIST dataset
    - `path`: Directory containing:
        - For spoken variant:
            - `data_sp_train.npy`
            - `data_sp_test.npy`
            - `labels_train.npy`
            - `labels_test.npy`
        - For written variant:
            - `data_wr_train.npy`
            - `data_wr_test.npy`
            - `labels_train.npy`
            - `labels_test.npy`
    - `variant`: One of:
        - `"spoken"`: Spoken digit data (39x13 features)
        - `"written"`: Written digit data (28x28x1 images)
    - Note: Does not support validation set

### 4. Model Configuration
The model configuration consists of a model template section and at least one model variant section. While the model template (`[model_template]`) defines default settings that can be shared across models, at least one model variant (`[[model]]`) must be specified for Qualia to function. The available model architectures depend on your chosen learning framework and can be found in either the learningmodel/pytorch or learningmodel/keras subdirectories.
Parameter lists must be completely specified and full for all layers to be generated correctly.
```toml
[model_template]
kind = "CNN"
epochs = 10
batch_size = 32

[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

[model_template.optimizer.scheduler]  # Optional
kind = "StepLR"
params.step_size = 30
```

Supported model architectures:
- `"CNN"`: Convolutional Neural Network
	- Parameters:
	    - `filters`: List of integers, number of filters for each conv layer
	    - `kernel_sizes`: List of integers, kernel size for each conv layer
	    - `paddings`: List of integers, padding for each conv layer
	    - `strides`: List of integers, stride for each conv layer
	    - `pool_sizes`: List of integers, pooling size after each conv layer (0 for no pooling)
	    - `fc_units`: List of integers, units in fully connected layers
	    - `batch_norm`: Boolean, whether to use batch normalization
	    - `dropouts`: Float or list of floats, dropout rates
	    - `prepool`: Integer, pre-pooling factor
	    - `postpool`: Integer, post-pooling factor
	    - `gsp`: Boolean, whether to use Global Sum Pooling
	    - `dims`: Integer (1 or 2), dimensionality of input

- `"MLP"`: Multi-Layer Perceptron
    - Parameters:
        - [Need to document parameters]

- `"ResNet"`: Residual Network
	- Parameters:
		- `filters`: List of integers specifying number of filters. First element applies to initial layer, remaining elements apply to residual blocks
		- `kernel_sizes`: List of integers specifying kernel sizes
		- `num_blocks`: List of integers where each element specifies how many times to repeat a block configuration using the corresponding parameters from filters/kernel_sizes/pool_sizes/paddings lists
		- `pool_sizes`: List of integers specifying pooling between blocks
		- `strides`: List of integers specifying strides for each layer
		- `paddings`: List of integers specifying paddings for each layer
		- `prepool`: Integer specifying pre-pooling factor (default: 1)
		- `postpool`: String ('max' or 'avg') specifying type of final pooling
		- `batch_norm`: Boolean specifying use of batch normalization (default: False)
		- `bn_momentum`: Float specifying batch norm momentum (default: 0.1)
		- `dims`: Integer (1 or 2) specifying dimensionality of input

Note: In the standard ResNet, pool_sizes controls downsampling between blocks. This behavior is corrected in the ResNetStride variant which separates stride and pooling controls.

- `"ResNetSampleNorm"`: ResNet with Sample Normalization
    - Parameters:
        - Same as ResNet, plus:
        - `samplenorm`: String, normalization type ('minmax')

- `"ResNetStride"`: ResNet with Strided Convolutions
    - Parameters:
        - Same as ResNet, plus:
		- `pool_sizes`: List of integers specifying pooling sizes for each layer
		- `strides`: List of integers specifying actual stride values

- `"TorchVisionModel"`: Models from torchvision
	- Parameters:
	    - `model`: String, name of torchvision model
	    - `replace_classifier`: Boolean, whether to replace the classifier layer (default: True)
	    - `fm_output_layer`: String, name of feature map output layer (default: 'flatten')
	    - `freeze_feature_extractor`: Boolean, whether to freeze feature extractor (default: True)
	    - Additional arguments passed to torchvision model


Supported optimizers: 
- PyTorch: [https://pytorch.org/docs/stable/optim.html](https://pytorch.org/docs/stable/optim.html)
- Keras: [https://keras.io/api/optimizers/](https://keras.io/api/optimizers/)

Supported schedulers: 
- PyTorch: [https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate](https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)
- Keras: [https://keras.io/api/optimizers/learning_rate_schedules/](https://keras.io/api/optimizers/learning_rate_schedules/)

## Optional Sections

### 1. Preprocessing
They are executed sequentially in the order they appear in the configuration file.

```toml
[[preprocessing]]
kind = "DatamodelConverter"

[[preprocessing]]
kind = "Normalize"
```

Supported preprocessing:
- `"BandPassFilter"`
- `"Class2BinMatrix"`
- `"CopySet"`
- `"DatamodelConverter"`
- `"DatasetSplitter"`
- `"DatasetSplitterBySubjects"`
- `"MFCC"`
- `"Normalize"`
- `"Reshape2DTo1D"`
- `"RemoveActivity"`
- `"RemoveSensor"`
- `"VisualizeActivities"`
- `"VisualizeWindows"`
- `"Window"`

### 2. Data Augmentation
Data augmentations are executed sequentially in the order they appear in the configuration file, with one important distinction: all augmentations with `params.before = true` are executed first, followed by all augmentations with `params.after = true`.

```toml
[[data_augmentation]]
kind = "RandomRotation"
params.before = true    # Apply before GPU transfer
params.after = false    # Apply after GPU transfer
params.evaluate = false # Use during inference
```

Signal Processing :

- `"Amplitude"`: Amplitude modification
- `"CMSISMFCC"`: MFCC transformation using ARM CMSIS implementation
- `"GaussianNoise"`: Add Gaussian noise
- `"MFCC"`: MFCC transformation using torchaudio implementation
- `"Normalize"`: Normalize data using torchvision transforms
- `"TimeShifting"`: Time-based shifting
- `"TimeWarping"`: Time warping transformation

Image Processing :

- `"AutoAugment"`: Automatic augmentation (using torchvision module)
- `"Crop"`: Cropping transformation
- `"Cutout1D"`: Cutout augmentation
- `"HorizontalFlip"`: Horizontal flip
- `"ResizedCrop"`: Resize and crop
- `"Rotation"`: 3D rotation transformation
- `"Rotation2D"`: 2D rotation
- `"TorchVisionModelTransforms"`: torchvision model transforms

Data Type Conversion :

- `"IntToFloat32"`: Convert integers to float32

Something else :
- `"Mixup"`: Mixup augmentation

Parameters for each augmentation:

- `before`: Boolean, apply before GPU transfer (default: False)
- `after`: Boolean, apply after GPU transfer (default: True)
- `evaluate`: Boolean, use during inference (default: False)

### 3. Post-processing
They are executed sequentially in the order they appear in the configuration file.
```toml
[[postprocessing]]
kind = "FuseBatchNorm"
export = true  # Save modified weights
```

Each postprocessing module can include:
- `export`: Boolean, whether to save model weights after processing (default: False)
 
**Model Analysis**
`"Distribution"`: Parameter Distribution Analysis
- Analyzes distribution of model parameters
- Parameters:
	- `method`: Analysis method:
		- `"layer_wise"`: Analyze per layer (default)
		- `"network_wise"`: Analyze whole network
  - `bins`: Number of histogram bins (default: 10)
  - `min`: Minimum value for histogram (default: -5.0)
  - `max`: Maximum value for histogram (default: 5.0)
  - `output_layer`: Save layer information in pickle files (default: True)
  - `output_pdf`: Generate PDF with distributions (default: False)
- Output Files:
	- Distribution files: `out/distribution/<network_name>/`
- Export Support: ❌ (Analysis only, no model weight modification)

`"VisualizeFeatureMaps"`: Feature Map Visualization 
- Visualizes feature maps of model layers
- Parameters:
	- `create_pdf`: Generate PDF visualization (default: True)
	- `save_feature_maps`: Save feature maps (default: True)
	- `compress_feature_maps`: Use compression (default: True)
	- `data_range`: Optional list of [start, end] indices for selecting test dataset samples to generate average feature maps
- Output Files:
	- Feature maps and PDFs: `out/feature_maps/`
- Export Support: ❌ (Visualization only, no model weight modification)

**Model Optimization**
`"FuseBatchNorm"`: BatchNorm Fusion
- Fuses BatchNorm layers into preceding convolutions
- Parameters:
	- `evaluate`: Evaluate model after fusion (default: True)
- Output Files when `export=true`:
	- Model weights: `out/learningmodel/<model_name>_fused`
- Export Support: ✅ (Saves modified model with fused layers)
- Notes: Only for PyTorch models in eval mode

`"QuantizationAwareTraining"`: QAT Training
- Performs quantization-aware training or post-training quantization
- Parameters:
    - `epochs`: Training epochs (default: 1)
    - Note: If epochs=0, performs Post-Training Quantization instead of Quantization-Aware Training
    - `batch_size`: Batch size (default: 32)
    - `model`: Model configuration containing:
    - `params.quant_params`:
        - `bits`: Quantization bit width
        - `quantype`: Quantization type, `'fxp'` for fixed-point or `'fake'`
        - `roundtype`: Rounding type, `'nearest'`, `'floor'` or `'ceil'`
        - `range_setting`: Tensor range analysis, `'minmax'`, `'MSE_simulation'` or `'MSE_analysis'`
        - `force_q`: Optionally force Qx coding for all layers (number of bits for fractional part)
        - `LSQ`: Use LSQ quantization-aware training (default: False)
    - `optimizer`: Optional optimizer configuration
    - `evaluate_before`: Evaluate before QAT (default: True)
- Output Files when `export=true`:
    - Model weights: `out/learningmodel/<model_name>_q<bits>_force_q<value>_e<epochs>_LSQ<bool>`
    - Activation ranges: `out/learningmodel/<model_name>_activations_range.txt`
- Export Support: ✅ (Saves quantized model and ranges)

 `"QuantizationAwareTrainingFX"`: FX-based QAT
- Extension of QuantizationAwareTraining using torch.fx
- Same parameters as QuantizationAwareTraining
- Same output files and export behavior
- Export Support: ✅ (Saves quantized model and ranges)

**Model Conversion**
`"RemoveKerasSoftmax"`: Softmax Removal
- Removes final Softmax layer from Keras models
- Output Files when `export=true`:
	- Model weights: `out/learningmodel/<model_name>_no_softmax`
- Export Support: ✅ (Saves model without Softmax)
- Notes: Only works if last layer is Activation(softmax)

`"Torch2Keras"`: PyTorch to Keras Conversion
- Converts PyTorch models to Keras format
- Parameters:
	- `mapping`: Path to TOML file defining layer mapping
- Output Files when `export=true`:
	- Keras model: `out/learningmodel/<model_name>_keras`
	- Activation ranges: `out/learningmodel/<model_name>_activations_range.h5.txt`
- Export Support: ✅ (Saves Keras model)

**Example Configuration:**

```toml
# Fuse batch normalization and save weights
[[postprocessing]]
kind = "FuseBatchNorm"
params.evaluate = true  # Evaluate model after fusion
export = true    # Save fused model weights

# Quantization-aware training
[[postprocessing]]
kind = "QuantizationAwareTraining"
params.epochs = 5       # Number of QAT epochs
params.model.params.quant_params.bits           = 8 # 8-bit quantization
params.model.params.quant_params.quantype       = "fxp" # Fixed-point
params.model.params.quant_params.roundtype      = "floor" # Floor rounding mode
params.model.params.quant_params.range_setting  = "minmax" # Min-max range analysis
params.model.params.quant_params.LSQ            = false # LSQ QAT disabled
params.evaluate_before = true  # Evaluate model before QAT
export = true    # Save quantized model
```

### 4. Deployment

```toml
[deploy]
target = "Linux"              # Target platform
converter.kind = "QualiaCodeGen" # Use Qualia-CodeGen converter 
quantize = ["int8"] # Quantization format
```

 **`"QualiaCodeGen"`**
Converts models to C code using Qualia-CodeGen.
Supported Targets:
- `"NucleoH7S3L8"` (STMicroelectronics Nucleo-H7S3L8 board)
- `"NucleoL452REP"` (STMicroelectronics Nucleo-L452RE-P board)
- `"NucleoU575ZIQ"` (STMicroelectronics Nucleo-U575ZI-Q board)
- `"SparkFunEdge"` (SparkFun Edge board)
- `"LonganNano"` (Sipeed Longan Nano board)
- `"Linux"` (for desktop/server deployment)


**`"Keras2TFLite"`**
Converts Keras models to TFLite format.
Supported Targets:
- `"Linux"` (TFLite runtime or STM32Cube.AI runtime, not usable implicitly)
- `"NucleoL452REP"` (STM32Cube.AI runtime, Nucleo-L452RE-P board)
- `"SparkFunEdge"` (TFLite Micro runtime, SparkFun Edge board)

**Example Configurations**
```toml
# Using QualiaCodeGen for STM32
[deploy]
target = "NucleoH7S3L8"
converter.kind = "QualiaCodeGen"
quantize = ["int8"]

# Using Keras2TFLite
[deploy]
target = "Linux"
converter.kind = "Keras2TFLite"
quantize = ["int8"]
```

**Quantize Parameter**
In the deployment configuration, `quantize` specifies what data types to use:

```toml
[deploy]
quantize = ["float32"]  # Use 32-bit floating point
# or
quantize = ["int8"]     # Use 8-bit integers
# or
quantize = ["int16"]    # Use 16-bit integers
```

Important notes about quantization:
- The `quantize` parameter must be provided as a single-element list
- When using integer quantization (int8/int16), you must configure Quantization-Aware Training in the postprocessing section
- Different quantization formats require separate configuration files

Available quantization types:
- `"float32"`: 32-bit floating point
- `"float16"`: 16-bit floating point (TFLite only)
- `"float8"`: 8-bit floating point (TFLite only)
- `"int16"`: 16-bit integer
- `"int8"`: 8-bit integer

Notes:
- Must be provided as a list, even for single option
- Order matters for some converters
- Some options may not be supported by all converters (e.g., float16 and float8 are TFLite-specific)

### 5. Experiment Tracking

```toml
[experimenttracking]
kind = "ClearML"              # Tracking system to use
params.project = "MyProject"  # Project name
```

**PyTorch Tracking**
- `"ClearML"`: Integration with ClearML tracking system
- `"Neptune"`: Integration with Neptune.ai platform

**Keras Tracking**
- `"Neptune"`: Integration with Neptune.ai platform

**Example Configurations**
```toml
# Using ClearML with PyTorch
[experimenttracking]
kind = "ClearML"
params.project = "MyProject"
params.task = "Training"

# Using Neptune with Keras or PyTorch
[experimenttracking]
kind = "Neptune"
params.project = "MyProject"
params.experiment = "Training"
```

### 6. Model Definition
Models in Qualia are defined through two components:
1. A template (`[model_template]`) containing common settings
2. Specific variations (`[[model]]`) that can override template settings

#### Model Template
The template defines default settings for all models:

```toml
[model_template]
kind = "CNN"                # Model architecture type
epochs = 10                 # Training epochs
batch_size = 32            # Batch size

# Model-specific parameters
params.batch_norm = true
params.filters = [32, 64]
params.kernel_sizes = [3, 3]

# Optimizer settings
[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

# Optional scheduler
[model_template.optimizer.scheduler]
kind = "StepLR"
params.step_size = 30
```

Common settings:
- `kind`: Model architecture (see "Supported Model Architectures")
- `epochs`: Number of training epochs
- `batch_size`: Training and inference batch size
- `params`: Architecture-specific parameters
- `optimizer`: Training optimizer configuration
- `scheduler`: Learning rate scheduler (optional)

#### Model Variants
Each model variant is defined in its own `[[model]]` section:

```toml
[[model]]
name = "cnn_small"            # Unique model name
params.filters = [32, 64]     # Override specific params
disabled = false              # Optional, skip this model

[[model]]
name = "cnn_large"
params.filters = [64, 128]
params.fc_units = [256]       # Add new params

[[model]]
name = "cnn_custom"
kind = "ResNet"              # Override architecture
params = { ... }             # Complete param override
```

Settings:
- `name`: Unique identifier (required)
- `disabled`: Skip this model (default: false)
- Any template setting can be overridden:
	- `kind`: Different architecture
	- `epochs`, `batch_size`: Different training settings
	- `params`: Partial or complete parameter override 
	- `optimizer`, `scheduler`: Different training config

### Common Model Settings

#### Training Control
```toml
[model_template]
load = false          # Load existing weights
train = true         # Perform training
evaluate = true      # Run evaluation
```

#### Data Parameters
```toml
[model_template]
input_shape = [28, 28, 1]   # Input dimensions
output_shape = [10]         # Output dimensions
```

#### Optimizer Options
```toml
[model_template.optimizer]
kind = "SGD"
params.lr = 0.01
params.momentum = 0.9
params.weight_decay = 0.0001
```

#### Scheduler Options
```toml
[model_template.optimizer.scheduler]
kind = "StepLR"
params.step_size = 30
params.gamma = 0.1
```

### Example Complete Configuration

```toml
# Template for all models
[model_template]
kind = "CNN"
epochs = 100
batch_size = 32
params.batch_norm = true
params.filters = [32, 64]
params.kernel_sizes = [3, 3]
params.pool_sizes = [2, 2]

[model_template.optimizer]
kind = "Adam"
params.lr = 0.001

# Small model variant
[[model]]
name = "cnn_small"
# Uses template settings

# Medium model with custom filters
[[model]]
name = "cnn_medium"
params.filters = [64, 128]

# Large model with different architecture
[[model]]
name = "cnn_large"
params.filters = [128, 256]
params.fc_units = [512]
epochs = 150  # More epochs

# Disabled variant
[[model]]
name = "experimental"
params.filters = [256, 512]
disabled = true
```

## Best Practices

1. Always specify unique model names
2. Use comments to document parameter choices
3. Start with example configurations
4. Test configurations with small datasets first
