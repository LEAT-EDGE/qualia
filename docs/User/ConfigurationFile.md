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
- `"DatamodelConverter"`
  - [Parameters need to be documented]
- `"Normalize"`
  - `mean`: Float
  - `std`: Float
- `"Class2BinMatrix"`
  - [Parameters need to be documented]

[Additional preprocessing types need to be documented]

### 2. Data Augmentation

```toml
[[data_augmentation]]
kind = "RandomRotation"
params.before = true    # Apply before GPU transfer
params.after = false    # Apply after GPU transfer
params.evaluate = false # Use during inference
```

Supported augmentations:
- `"RandomRotation"`
  - [Parameters need to be documented]

[Additional augmentation types need to be documented]

Common parameters for all augmentations:
- `before`: Boolean, default false
- `after`: Boolean, default true
- `evaluate`: Boolean, default false

### 3. Post-processing

```toml
[[postprocessing]]
kind = "FuseBatchNorm"
export = true  # Save modified weights
```

Supported post-processing:
- `"FuseBatchNorm"`
  - `export`: Boolean, save weights after processing
  - [Additional parameters need to be documented]

[Additional post-processing types need to be documented]

### 4. Deployment

```toml
[deploy]
target = "Linux"
converter.kind = "QualiaCodeGen"
converter.params = { optimize = true }
deployer.params = { port = "/dev/ttyUSB0" }
evaluator.params = { batch_size = 32 }
quantize = ["float32"]
```

Supported targets:
- `"Linux"`
  - [Parameters need to be documented]
- `"SparkFunEdge"`
  - [Parameters need to be documented]
Only QualiaCodeGen
[Additional targets need to be documented]

Supported converters:
- `"QualiaCodeGen"`
  - [Parameters need to be documented]

[Additional converters need to be documented]

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