# Python Package Structure

## Basic Structure

A typical Qualia package (core or plugin) has the following structure:

```
qualia-package/
├── conf/                    # Configuration files
│   ├── dataset1/           # Organized by dataset
│   │   └── model_conf.toml
│   └── dataset2/
│       └── model_conf.toml
├── docs/                    # Documentation
│   ├── conf.py
│   ├── index.rst
│   └── Makefile
├── src/
│   └── qualia_package_name/
│       ├── assets/         # Non-Python files
│       ├── dataaugmentation/  # Data augmentation modules
│       │   └── pytorch/
│       ├── datamodel/      # Dataset structures
│       ├── dataset/        # Dataset loaders
│       ├── deployment/     # Target deployment modules
│       │   ├── keras/
│       │   ├── qualia_codegen/
│       │   └── tflite/
│       ├── evaluation/     # On-target evaluation
│       │   ├── host/
│       │   └── target/
│       ├── experimenttracking/ # Experiment tracking modules
│       ├── learningframework/  # Learning framework modules
│       ├── learningmodel/     # Model definitions
│       │   ├── keras/
│       │   └── pytorch/
│       │       └── layers/
│       ├── postprocessing/    # Model post-processing
│       ├── preprocessing/     # Data preprocessing
│       ├── utils/            # Utility functions
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       ├── py.typed         # Type hints marker
│       └── typing.py        # Type definitions
├── tests/                   # Test files
│   └── functional/
│       ├── end_to_end/
│       └── training/
├── LICENSE
├── pyproject.toml          # Project metadata and dependencies
└── README.md
```

## Directory Descriptions

### Top-level Directories

- `conf/`: Contains TOML configuration files organized by dataset and experiment
- `docs/`: Documentation files and build configuration
- `src/`: Source code directory containing the main package
- `tests/`: Test files organized by type (functional, unit, etc.)

### Source Package Structure (`src/qualia_package_name/`)

#### Core Modules

1. **`assets/`**
   - Non-Python files needed for package installation
   - Must contain `__init__.py` (can be empty)
   - Template files, project files, etc.

2. **`datamodel/`**
   - Data structures for storing dataset information
   - Common data representations
   - Dataset-specific models

3. **`dataset/`**
   - Dataset loader modules
   - Referenced in `[dataset]` configuration sections
   - Handles data import and initial formatting

4. **`learningframework/`**
   - Framework-specific implementations (PyTorch, Keras, etc.)
   - Referenced in `[learningframework]` configuration
   - Handles training loop and model interaction

5. **`learningmodel/`**
   - Model architecture definitions
   - Organized by framework (pytorch/, keras/)
   - Custom layers and components
   - Referenced in `[model_template]` and `[[model]]` sections

#### Processing Modules

6. **`preprocessing/`**
   - Data preprocessing modules
   - Used during `preprocess_data` action
   - Referenced in `[[preprocessing]]` sections

7. **`dataaugmentation/`**
   - Data augmentation implementations
   - Referenced in `[[data_augmentation]]` sections
   - Framework-specific augmentation methods

8. **`postprocessing/`**
   - Model postprocessing modules
   - Model converter modules
   - Referenced in `[[postprocessing]]` and `[deploy]` sections

#### Deployment Modules

9. **`deployment/`**
   - Target deployment modules
   - Used during `prepare_deploy` and `deploy_and_evaluate`
   - Framework-specific deployment handlers
   - Referenced in `[deploy]` sections

10. **`evaluation/`**
    - On-target evaluation modules
    - Used during `deploy_and_evaluate`
    - Host and target-specific evaluations
    - Referenced in `[deploy]` sections

11. **`experimenttracking/`**
    - Experiment logging and tracking
    - Referenced in `[experimenttracking]` section
    - Framework-specific tracking implementations

#### Utility Files

12. **`utils/`**
    - Common utility functions
    - File handling, logging, process management
    - Helper functions used across modules

13. **Required Files**
    - `main.py`: CLI entry point (if CLI is provided)
    - `py.typed`: Empty file marking package as type-hinted
    - `typing.py`: Common type definitions
    - `__init__.py`: Required in all directories for proper importing

## Notes

- All directories must contain `__init__.py` files (Python 3.9 compatibility)
- Plugins may implement any subset of these directories based on features
- Directory structure matches configuration file sections
- Type hints are mandatory unless explicitly marked as unavailable