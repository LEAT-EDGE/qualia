# Qualia Plugins Guide

```{contents} Table of Contents
---
depth: 3
---
```

## Introduction

Qualia's plugin system allows extending core functionality through modular packages. Plugins can add new features, override existing ones, or provide experimental implementations while maintaining clean separation from core components.

## Plugin Structure

A typical Qualia plugin follows this structure:

```
qualia-plugin-name/
├── conf/                    # Configuration examples
│   └── dataset_name/       
│       └── model_conf.toml
├── docs/                    
│   ├── conf.py
│   ├── index.rst
│   └── Makefile
├── src/
│   └── qualia_plugin_name/  # Must follow qualia_plugin_* naming
│       ├── deployment/      # Target-specific deployment
│       │   └── qualia_codegen/
│       │       ├── __init__.py
│       │       └── target_name.py
│       ├── learningframework/  # Framework implementations
│       │   ├── __init__.py
│       │   └── custom_framework.py
│       ├── learningmodel/     # Model architectures
│       │   └── pytorch/      # Organized by framework
│       │       ├── __init__.py
│       │       ├── layers/   # Custom layer implementations
│       │       │   ├── __init__.py
│       │       │   └── custom_layers.py
│       │       └── models.py
│       ├── postprocessing/   # Conversion & post-processing
│       │   ├── __init__.py
│       │   └── custom_converter.py
│       ├── preprocessing/    # Data preprocessing
│       │   ├── __init__.py
│       │   └── custom_preprocessor.py
│       ├── __init__.py
│       └── py.typed
├── tests/
│   └── functional/
├── LICENSE
├── pyproject.toml          # Project metadata & dependencies
└── README.md
```

## Using Plugins

### Configuration

To use a plugin, add it to your configuration file under the `[bench]` section:

```toml
[bench]
plugins = ['qualia_plugin_snn', 'qualia_plugin_spleat']
```

### Plugin Loading Process

1. Qualia-Core scans the `plugins` list in order
2. For each plugin, it imports and merges these packages:
   - `preprocessing`
   - `learningframework`
   - `postprocessing`
3. Plugins listed later can override earlier plugins
4. Other packages are loaded on-demand by the plugin's modules

## Creating a Plugin

### 1. Setup Project Structure

Use the Qualia Plugin Template to create a new plugin:

```bash
# Clone the template
git clone https://your-gitlab-server/qualia-plugin-template.git qualia-plugin-name
cd qualia-plugin-name

# Initialize project structure
mkdir -p src/qualia_plugin_name/{learningframework,learningmodel,postprocessing,preprocessing}
touch src/qualia_plugin_name/{__init__.py,py.typed}
```

### 2. Configure Project Metadata

Edit `pyproject.toml`:

```toml
[project]
name = "qualia-plugin-name"
version = "0.1.0"
description = "Your plugin description"
dependencies = [
    "qualia-core>=2.0.0",
    # Add your dependencies
]

[project.optional-dependencies]
dev = ["pytest", "pylint", "mypy"]
```

### 3. Implement Plugin Features

#### Adding New Features

Create new modules in appropriate directories:

```python
# src/qualia_plugin_name/learningframework/custom_framework.py
from qualia_core.learningframework import BaseLearningFramework

class CustomFramework(BaseLearningFramework):
    def __init__(self, config):
        super().__init__(config)
        # Your implementation

    def train(self, model, train_loader, val_loader):
        # Training implementation
        pass
```

#### Overriding Existing Features

Inherit and extend existing classes:

```python
# src/qualia_plugin_name/postprocessing/custom_converter.py
from qualia_core.postprocessing import BaseConverter

class CustomConverter(BaseConverter):
    def __init__(self, config):
        super().__init__(config)
        # Additional initialization

    def convert(self, model):
        # Custom conversion logic
        pass
```

### 4. Plugin Integration Points

Plugins can integrate with Qualia in several ways:

1. **Learning Frameworks**
   - Add new frameworks via `learningframework/`
   - Override existing framework behaviors
   - Example: Adding SNN support

```python
# Example: Adding a new learning framework
from qualia_core.learningframework import register_framework

@register_framework
class SNNFramework(BaseLearningFramework):
    name = "snn"  # Used in config files
    
    def __init__(self, config):
        super().__init__(config)
```

2. **Model Architectures**
   - Implement new models in `learningmodel/`
   - Organize by framework (pytorch/, keras/)
   - Example: Custom neural architectures

3. **Processing Pipelines**
   - Add preprocessing steps
   - Implement custom data augmentation
   - Create post-processing transformations

4. **Deployment**
   - Add new target platforms
   - Customize deployment processes
   - Implement evaluation methods

## Plugin Categories

Plugins typically fall into three categories:

1. **External Dependency Plugins**
   - Handle non-AGPL-3.0 compatible dependencies
   - Example: `qualia-plugin-snn` (SpikingJelly integration)

2. **Proprietary Features**
   - Closed-source implementations
   - Example: `qualia-plugin-spleat`

3. **Experimental Features**
   - Research and development
   - Example: `qualia-plugin-som`

## Best Practices

1. **Naming Conventions**
   - Package name: `qualia-plugin-*`
   - Python package: `qualia_plugin_*`
   - Class names: CamelCase, descriptive

2. **Documentation**
   - Include clear README
   - Document configuration options
   - Provide usage examples

3. **Testing**
   - Write unit tests
   - Include functional tests
   - Test with different configurations

4. **Type Hints**
   - Use type annotations
   - Include `py.typed` file
   - Support mypy checking

## Common Issues and Solutions

1. **Plugin Not Loading**
   - Check package name in `plugins` list
   - Verify installation in environment
   - Check import paths

2. **Version Conflicts**
   - Specify compatible versions in `pyproject.toml`
   - Use appropriate version constraints
   - Test with target Qualia version

3. **Integration Problems**
   - Follow base class interfaces
   - Use proper registration decorators
   - Check configuration format

## Example Configurations

```toml
# Example configuration using plugin features
[bench]
plugins = ['qualia_plugin_snn']

[learningframework]
name = "snn"  # Provided by plugin
timesteps = 100

[model_template]
name = "SCNN"  # Custom model from plugin
layers = [64, 128, 10]
```

Would you like me to expand on any particular section or add more specific examples?