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
- `first_run`: Integer, starting iteration (allow in case of crash to not start from the beginning)
- `last_run`: Integer, ending iteration
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

# CIFAR-10 example
[dataset]
kind = "CIFAR10"
params.path = "data/cifar10/"
params.dtype = "float32"

# CORe50 example
[dataset]
kind = "CORe50"
params.path = "data/core50/"
params.variant = "category"

# GSC example
[dataset]
kind = "GSC"
params.path = "data/speech_commands/"
params.variant = "v2"
params.subset = "digits"
params.train_valid_split = true

# WSMNIST example
[dataset]
kind = "WSMNIST"
params.path = "data/wsmnist/"
params.variant = "spoken"

# BrainMIX example
[dataset]
kind = "BrainMIX"
params.path = "data/brainmix/"
```

Supported dataset:

- `"BrainMIX"`: Brain dataset
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

- `"ElicieHAR"`: Elicie Human Activity Recognition dataset
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

- `"QuantizedCNN"`: Quantized Convolutional Neural Network
    - Notes: Supports GSP (Gradual Sparseness Promotion)

- `"QuantizedMLP"`: Quantized Multi-Layer Perceptron
    - Parameters:
        - [Need to document parameters]

- `"QuantizedResNet"`: Quantized Residual Network
    - Parameters:
        - [Need to document parameters]
    - Notes: PyTorch 2.x compatible

- `"ResNet"`: Residual Network
	- Parameters:
	    - `filters`: List of integers, number of filters for each layer
	    - `kernel_sizes`: List of integers, kernel sizes
	    - `num_blocks`: List of integers, number of residual blocks in each layer
	    - `strides`: List of integers, strides for each layer
	    - `paddings`: List of integers, paddings for each layer
	    - `prepool`: Integer, pre-pooling factor (default: 1)
	    - `postpool`: String ('max' or 'avg'), type of final pooling
	    - `batch_norm`: Boolean, use batch normalization (default: False)
	    - `bn_momentum`: Float, batch norm momentum (default: 0.1)
	    - `dims`: Integer (1 or 2), dimensionality of input

- `"ResNetSampleNorm"`: ResNet with Sample Normalization
    - Parameters:
        - Same as ResNet, plus:
        - `samplenorm`: String, normalization type ('minmax')

- `"ResNetStride"`: ResNet with Strided Convolutions
    - Parameters:
        - Same as ResNet, plus:
        - `pool_sizes`: List of integers, pooling sizes for each layer

- `"TorchVisionModel"`: Models from torchvision
	- Parameters:
	    - `model`: String, name of torchvision model
	    - `replace_classifier`: Boolean, whether to replace the classifier layer (default: True)
	    - `fm_output_layer`: String, name of feature map output layer (default: 'flatten')
	    - `freeze_feature_extractor`: Boolean, whether to freeze feature extractor (default: True)
	    - Additional arguments passed to torchvision model


Supported optimizers:
- `"Adam"`
  - `lr`: Learning rate (float)
- `"SGD"`
- Most of the optimizers in Pytorch

Supported schedulers:
- `"StepLR"`
  - `step_size`: Integer, epochs between LR updates
  - [Additional parameters need to be documented]
- `"ReduceLROnPlateau"`
  - [Parameters need to be documented]

## Optional Sections

### 1. Preprocessing

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

```toml
[[data_augmentation]]
kind = "RandomRotation"
params.before = true    # Apply before GPU transfer
params.after = false    # Apply after GPU transfer
params.evaluate = false # Use during inference
```

Signal Processing :

- `"Amplitude"`: Amplitude modification
- `"CMSISMFCC"`: MFCC transformation
- `"GaussianNoise"`: Add Gaussian noise
- `"MFCC"`: Mel-frequency cepstral coefficients
- `"Normalize"`: Normalize data using torchvision transforms
- `"TimeShifting"`: Time-based shifting
- `"TimeWarping"`: Time warping transformation

Image Processing :

- `"AutoAugment"`: Automatic augmentation
- `"Crop"`: Cropping transformation
- `"CutoutID"`: Cutout augmentation
- `"HorizontalFlip"`: Horizontal flip
- `"ResizedCrop"`: Resize and crop
- `"Rotation"`: Rotation transformation
- `"Rotation2D"`: 2D rotation
- `"TorchVisionModelTransforms"`: torchvision model transforms

Data Type Conversion :

- `"IntToFloat32"`: Convert integers to float32
- `"Mixup"`: Mixup augmentation

Parameters for each augmentation:

- `before`: Boolean, apply before GPU transfer (default: False)
- `after`: Boolean, apply after GPU transfer (default: True)
- `evaluate`: Boolean, use during inference (default: False)

### 3. Post-processing

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
	- `data_range`: Optional list of [start, end] indices
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
- Performs quantization-aware training
- Parameters:
	- `epochs`: Training epochs (default: 1)
	- `batch_size`: Batch size (default: 32)
	- `model`: Model configuration containing:
	- `params.quant_params`:
		- `bits`: Quantization bit width
		- `force_q`: Optional forced quantization
		- `LSQ`: Use LSQ quantization (default: False)
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
`"Keras2TFLite"`: Keras to TFLite Conversion
- Converts Keras models to TFLite format
- Parameters:
	- `quantize`: Target format:
		- `"float32"`: No quantization
		- `"int8"`: 8-bit integer quantization
		- `"int16"`: 16-bit integer quantization
  - `new_converter`: Use new TFLite converter (default: False)
- Output Files when `export=true`:
	- TFLite model: `out/<target>/<model_name>.tflite`
- Export Support: ✅ (Saves TFLite model)

 `"QualiaCodeGen"`: C Code Generation
- Generates optimized C code implementation
- Parameters:
	- `quantize`: Target format:
		- `"float32"`: 32-bit floating point
		- `"int8"`: 8-bit integer
		- `"int16"`: 16-bit integer
	- `long_width`: Width for long integers
	- `outdir`: Output directory (default: "out/qualia_codegen")
	- `metrics`: List of metrics to convert
- Output Files when `export=true`:
	- C code: `out/qualia_codegen/<model_name>_q<type>/`
- Export Support: ✅ (Saves C code implementation)

### `"RemoveKerasSoftmax"`: Softmax Removal
- Removes final Softmax layer from Keras models
- Output Files when `export=true`:
	- Model weights: `out/learningmodel/<model_name>_no_softmax`
- Export Support: ✅ (Saves model without Softmax)
- Notes: Only works if last layer is Activation(softmax)

### `"Torch2Keras"`: PyTorch to Keras Conversion
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
evaluate = true
export = true  # Saves fused model

# Quantization-aware training
[[postprocessing]]
kind = "QuantizationAwareTraining"
epochs = 5
model.params.quant_params = { bits = 8 }
evaluate_before = true
export = true  # Saves quantized model

# Generate and save C code
[[postprocessing]]
kind = "QualiaCodeGen"
quantize = "int8"
metrics = ["accuracy"]
export = true  # Saves generated code
```

### 4. Deployment

```toml
[deploy]
target = "Linux"              # Target platform
converter.kind = "QualiaCodeGen"  # Converter to use
quantize = ["float32"]       # Quantization options
```

 **`"QualiaCodeGen"`**
Converts models to C code.
Supported Targets:
- `"NucleoH7S3L8"` (STM32H7 board, up to 740MHz)
- `"NucleoL452REP"` (STM32L4 board)
- `"NucleoU575ZIQ"` (STM32U5 board)
- `"SparkFunEdge"` (SparkFun Edge board)
- `"LonganNano"` (Sipeed Longan Nano board)
- `"Linux"`


**`"Keras2TFLite"`**
Converts Keras models to TFLite format.
Supported Targets:
- `"Linux"` only


**`"TFLite"`**
For pre-converted TFLite models.
Supported Targets:
- `"Linux"` only


**`"stm32cubeai"`**
Uses STM32Cube.AI to deploy models on STM32 boards.
Supported Targets:
- `"NucleoH7S3L8"` (STM32H7 board)
- `"NucleoL452REP"` (STM32L4 board)
- `"STM32CubeAI"` (Generic STM32 with Cube.AI)


**`"tflitemicro"`**
TensorFlow Lite for Microcontrollers deployment.
Supported Targets:
- `"SparkFunEdge"` (SparkFun Edge board)

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
quantize = ["float32"]     # Single option
# or
quantize = ["int8", "int16"]  # Multiple options
```

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
kind = "ClearML"
params.project = "MyProject"
params.task = "MyTask"
```

Supported tracking systems:
- `"ClearML"`
  - `project`: String
  - `task`: String
  - [Additional parameters need to be documented]

[Additional tracking systems need to be documented]

## Model Definition
Define specific model variations using the `[[model]]` section:

```toml
[[model]]
name = "cnn_small"            # Unique name required
params.filters = [32, 64]     # Override template params
params.kernel_sizes = [3, 3]
disabled = false              # Optional, default false
```

Each `[[model]]` inherits from `[model_template]` and can override any setting.

## Best Practices

1. Always specify unique model names
2. Use comments to document parameter choices
3. Group related models in the same configuration file
4. Start with example configurations
5. Test configurations with small datasets first

## Common Issues

1. Missing required fields
2. Incorrect parameter types
3. Invalid paths or filenames
4. Mismatched array lengths in model parameters

## Getting Help

1. Check error messages carefully
2. Use example configurations as templates
3. Verify all paths and filenames
4. Ensure virtual environment is activated