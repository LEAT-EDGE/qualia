# Using Qualia

## Overview

Qualia uses TOML configuration files to define machine learning experiments. Each experiment can include:
- Dataset selection and preprocessing
- Model architecture and training parameters
- Post-processing steps
- Deployment configuration
If you want more information about how to create your configuration file you can find it here [[ConfigurationFile]].
## Quick Start

1. Activate your virtual environment:
```bash
# If using uv:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# If using PDM:
$(pdm venv activate qualia_env)
```

2. Basic command structure:
```bash
qualia <config.toml> <action> [config_params]
```

## Workflow Steps

Qualia's workflow consists of four main actions that are typically run in sequence:

### 1. Preprocess Data
```bash
qualia config.toml preprocess_data
```
- Loads dataset specified in `[dataset]` section
- Applies preprocessing steps from `[[preprocessing]]` sections
- Exports processed data to `out/data/<dataset_name>` as compressed NumPy arrays
- Handles both 2D data (`[N, H, W, C]`) and 1D data (`[N, S, C]`)

Example output structure:
```
out/
└── data/
    └── UCI_HAR/
        ├── train_data.npz
        └── test_data.npz
```

### 2. Train Models
```bash
qualia config.toml train
```
- Trains models defined in `[[model]]` sections
- Uses settings from `[model_template]` (can be overridden)
- Saves:
  - Model weights in `out/learningmodel/`
  - Training results in `log/<bench_name>/learningmodel/`
- Applies post-processing steps if specified

Example output structure:
```
out/
└── learningmodel/
    └── uci-har_cnn_simple.pth

log/
└── UCI-HAR_CNN_example/
    └── learningmodel/
        ├── metrics.json
        └── training_log.txt
```

### 3. Prepare for Deployment
```bash
qualia config.toml prepare_deploy
```
- Converts models for target platform
- Uses settings from `[deploy]` section
- Creates deployment files in:
  - `out/<converter>/`: Converted model files
  - `out/<deploy>/`: Platform-specific files

Example output structure:
```
out/
├── codegen/
│   └── uci-har_cnn_simple/
│       ├── model.c
│       └── model.h
└── deploy/
    └── uci-har_cnn_simple/
        └── firmware.bin
```

### 4. Deploy and Evaluate
```bash
qualia config.toml deploy_and_evaluate
```
- Deploys prepared files to target system
- Runs evaluation
- Saves results in `log/<bench_name>/evaluate/`

Example output structure:
```
log/
└── UCI-HAR_CNN_example/
    └── evaluate/
        ├── accuracy.json
        └── inference_times.csv
```

## Configuration Parameters

You can override configuration settings via command line arguments:

```bash
qualia config.toml train --bench.name="Test" --model.0.disabled=True
```

Parameter format:
- `--<section>.<key>=<value>`
- For nested settings: `--<section>.<subsection>.<key>=<value>`
- For array elements: `--<section>.<index>.<key>=<value>`

Examples:
```bash
# Change experiment name
--bench.name="MyExperiment"

# Modify learning rate
--model_template.optimizer.params.lr=0.001

# Disable specific model
--model.0.disabled=True

# Change batch size for second model
--model.1.batch_size=64
```

Note: It's recommended to make changes in the configuration file rather than using command-line overrides to maintain reproducibility.

## Best Practices

1. **Configuration Files**
   - Keep one configuration file per experiment
   - Use descriptive names for experiments and models
   - Comment important parameter choices

2. **Directory Structure**
   - Organize datasets in `data/`
   - Keep configuration files in a dedicated directory
   - Use version control for configurations

3. **Workflow**
   - Run actions in sequence
   - Verify outputs after each step
   - Monitor training progress in logs

4. **Deployment**
   - Test deployment on small datasets first
   - Keep track of model versions
   - Document target-specific requirements

## Common Issues

1. **Data Format**
   - Ensure correct channel order (`channels_last`)
   - Verify data dimensions match model expectations
   - Check preprocessing output shapes

2. **Training**
   - Monitor GPU memory usage
   - Watch for learning rate issues
   - Verify model convergence

3. **Deployment**
   - Check target compatibility
   - Verify memory constraints
   - Test deployment environment

## Getting Help

If you encounter issues:
1. Check the logs in `log/<bench_name>/`
2. Verify configuration file syntax
3. Ensure all dependencies are installed
4. Review target platform requirements

For more detailed information about configuration options, see the Configuration File documentation.