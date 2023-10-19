# Python package structure

```{contents} Table of Contents
---
depth: 3
---
```

Sub-packages are required to contain a `__init__.py` file because namespace packages are not always supported properly
(in particular, it will not work with the `importlib.resources` module of Python 3.9).

## Qualia

Qualia-Core and Qualia-Plugin top-level package should follow this sub-packages and modules organization.

A plugin may contain any of these sub-packages or modules, depending on the features it provides.

For more information, see <inv:#qualia_core>

### `assets/`

Any non-Python files that should be included when installing the package.

Note that `assets/` is a Python subpackage itself so it needs to contain a `__init__.py` file as well (even empty).

### `dataaugmentation/`

Contains the data augmentation modules, referenced in the `[[data_augmentation]]` sections of the <project:/User/ConfigurationFile.md>.

### `datamodel/`

Contains the data structures used to store the dataset after loading.

### `dataset/`

Contains the dataset loader modules, referenced in the `[dataset]` section of the <project:/User/ConfigurationFile.md>.

### `deployment/`

Contains the target deployment modules used during `prepare_deploy` and `deploy_and_evaluate` actions, configured
in the `[deploy]` sections of the <project:/User/ConfigurationFile.md>
and suggested by the model converter module.

### `evaluation/`

Contains the on-target evaluation modules used during `deploy_and_evaluate` action, configured
in the `[deploy]` sections of the <project:/User/ConfigurationFile.md>
and suggested by the target deployment module.

### `experimenttracking/`

Contains the dataset loader modules, referenced in the `[experimenttracking]` section of the <project:/User/ConfigurationFile.md>.

### `learningframework/`

Contains the learning framework modules, referenced in the `[learningframework]` section of the <project:/User/ConfigurationFile.md>.

### `learningmodel/`

Contains the learning model modules, under a subdirectory for each learning framework,
referenced in the `[model_template]` and/or `[[model]]` sections of the <project:/User/ConfigurationFile.md>.

### `postprocessing/`

Contains the model postprocessing modules, referenced in the `[[postprocessing]]` sections of the <project:/User/ConfigurationFile.md>.

Also contains the model converter modules, referenced in the `[deploy]` sections of the <project:/User/ConfigurationFile.md>.

### `preprocessing/`

Contains the data preprocessing modules, referenced in the `[[preprocessing]]` sections of the <project:/User/ConfigurationFile.md>
and used during the `preprocess_data` action.

### `utils/`

Any extra utility modules that do not fit in another sub-package.

### `main.py`

Mandatory if a command-line interface is provided.

The entry point for the command-line interface that is referenced in `pyproject.toml`.

### `py.typed`

Mandatory except if type hints are not available yet.

An empty file to signify that this package provides type hints when imported by other packages.

For more information, see <project:TypeChecking.md>

### `typing.py`

Contains any common type hint definitions, e.g., the custom `TYPE_CHECKING` constant.

For more information, see <project:TypeChecking.md>

## Qualia-CodeGen

Qualia-CodeGen-Core and Qualia-CodeGen-Plugin top-level package should follow this sub-packages and modules organization.

A plugin may contain any of these sub-packages or modules, depending on the features it provides.

For more information, see <inv:#qualia_codegen_core>

### `assets/`

Non-Python files that should be included when installing the package, in particular contains the template files for code generation.

Note that `assets` is a Python subpackage itself so it needs to contain a `__init__.py` file (even empty).

### `examples/`

Contains the project files for deployment on a specific target.

Note that `examples` is a Python subpackage itself so it needs to contain a `__init__.py` file (even empty).

### `graph/`

Contains the internal graph representation data structures as well as the graph conversion modules (PyTorch, Keras…).

### `graph/layers/`

Contains the internal graph representation layers definitions.

### `main.py`

Mandatory if a command-line interface is provided.

The entry point for the command-line interface that is referenced in `pyproject.toml`.

### `py.typed`

Mandatory except if type hints are not available yet.

An empty file to signify that this package provides type hints when imported by other packages.

For more information, see <project:TypeChecking.md>

### `typing.py`

Contains any common type hint definitions, e.g., the custom `TYPE_CHECKING` constant.

For more information, see <project:TypeChecking.md>
