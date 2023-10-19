# Configuration file

```{contents} Table of Contents
---
depth: 3
---
```

The configuration file describes an experiment, which consists of 
a dataset, dataset preprocessing steps, learning model, training configuration, learning model postprocessing steps and a deployment configuration.

## TOML format

The configuration file format is [TOML](https://toml.io/), an [INI](https://en.wikipedia.org/wiki/INI_file)-like format.

The configuration is fundamentally a key-value mapping, i.e., a dictionary, where
the value can be a container such as another dictionary (called a Table in TOML) or a list (called an Array in TOML),
allowing hierarchical settings, or a literal such as a string, a number or a boolean.
These values are parsed in Python and converted to nested `dict`, `list`, `str`, `int`, `float`, and `bool` types.

### Tables

Tables (i.e., dictionaries) can be expressed with 3 possibles syntaxes:

1. Block-style
```toml
[mydict]
mykey = "myvalue"
```

2. Key-style
```toml
mydict.mykey = "myvalue"
```

3. Inline-style
```
mydict = { mykey = "myvalue" }
```

They can be nested with the `.` separator, e.g., `[mydict1.mydict2]` or `mydict1.mydict2.mykey = "myvalue"`

In Qualia's configuration files, syntax 1. is generally used
for top-level sections, syntax 3. is discouraged, and syntax 2. is generally used for hierarchical settings inside a section.

### Arrays

Arrays (i.e. list) can be expressed with 2 possible syntaxes:

1. Block-style, array of tables only
```toml
[[mylist]]
mykey = "myvalue1"

[[mylist]]
mykey = "myvalue2"
```
This creates a list containing 2 elements, each of them being a dictionary with a single "mykey" key,
the first one with value `"value1"` and the second one with `"value2"`.
The blocks are read in the order they are written in the file to build the list.

2. Inline-style
```toml
mylist = ["myvalue1", "myvalue2"]
```
This creates a simple list with 2 elements of different values.

In Qualia's configuration files, syntax 1. is generally used for top-level sections and syntax 2. is used for settings inside a section.

### Booleans

Booleans are written as `true` or `false`, without a capital letter, and translate directly to Python's `True` or `False`.

### Int, Float, Str

These types are written the same as in Python and translate directly to the Python type.

### Null-type

TOML does not have any null type (or an equivalent of Python's `None`), see [this issue](https://github.com/toml-lang/toml/issues/30).
If absolutely required, a `false` literal might be used instead, and manually converted to `None` in Python.

### Comments

Comments start with a `#` at the end of a line (empty or not).

## Qualia configuration structure

A Qualia configuration file is divided in multiple sections described below.

Each section contains a list of settings.
The TOML type is provided in the description whenever possible.
Settings are mandatory unless described as optional.

**Warning**: unrecognized sections are silently ignored. Unrecognized settings may be silently ignored depending on their location.

Example configuration files are available in the `conf` folder of the Qualia-Core and Qualia-Plugins source code repositories.

### `[bench]`

The `[bench]` section contains some general settings for the experiment described in the configuration file.

List of settings:
- **`name` (string)**: name of the experiment, used for the logs output folder among other things.
- **`seed` (integer)**: global seed to set for various random generators (Python, NumPy, PyTorch, Tensorflow…) at the beginning of the experiment.
- **`first_run` (integer)**: first iteration to run for model training, deployment and evaluation.
- **`last_run` (integer)**: last iteration to run for model training, deployment and evaluation, experiment will iterate `last_run - first_run + 1` times.
- **`plugins` (array of string, optional)**: list of plugin package names to load in order of appearance, e.g., `['qualia_plugin_snn', 'qualia_plugin_spleat]`.

### `[learningframework]`

The learning framework to load for this experiment.

For more information about available learning frameworks and their parameters, see <inv:#qualia_core.learningframework>.
Plugins may also load their own learning frameworks.

List of settings:
- **`kind` (string)**: name of the learningframework class to load, e.g., `PyTorch` or `Keras`.
- **`params` (table, optional)**: keyword parameters to pass to the constructor of the loaded learningframework class.

### `[deploy]` (optional)

Configuration for the deployment onto a target. Only required for the `prepare_deploy` and `deploy_and_evaluate` actions.

For more information about available converters and their parameters, see <inv:#qualia_core.postprocessing>.
The suggested deployers are available as the `deployers` attribute of the converter class.
The suggested evaluator is available as the `evaluator` attribute of the deployer class.
Plugins may also load their own converters which can suggest their own deployers and evaluators.


List of settings:
- **`target` (string)**: name of the target to deploy onto, this must match a class in the deployers suggested by the converter.
- **`converter.kind` (string)**: the converter class to use for deployment, e.g. C code generation with `QualiaCodeGen`.
- **`converter.params` (table, optional)**: keyword parameters to pass to the constructor of the converter class.
- **`deployer.params` (table, optional)**: keyword parameters to pass to the deployer class constructor (which is determined from the suggested deployers and the target name).
- **`evaluator.params` (table, optional)**: keyword parameters to pass to the evaluator class constructor (which is suggested by the deployer class)
- **`quantize` (array of string)**: base data type to use for quantization, passed to the converter class construtor.

### `[dataset]`

The dataset to load.

For more information about available datasets, see <inv:#qualia_core.dataset>.

List of settings:
- **`kind` (string)**: name of the dataset class.
- **`params` (array of string, optional)**: keyword parameters to pass to the dataset class constructor.

### `[experimenttracking]`

The experiment tracking module to use during the `train` action.

For more information about available datasets, see <inv:#qualia_core.experimenttracking>.

List of settings:
- **`kind` (string)**: name of the experiment tracking class.
- **`params` (array of string, optional)**: keyword parameters to pass to the experiment tracking class constructor.

### `[[preprocessing]]` (optional)

Zero, one or more `[[preprocessing]]` sections can be present in the configuration.
They correspond to preprocessing modules to apply successively after loading the dataset in the `preprocess_data` action and before exporting the data.

For more information about available preprocessing modules and their parameters, see <inv:#qualia_core.preprocessing>.
Plugins may also load their own preprocessing modules or override existing ones.

List of settings:
- **`kind` (string)**: name of the preprocessing class to apply.
- **`params` (array of string, optional)**: keyword parameters to pass to the preprocessing class constructor.

### `[[data_augmentation]]` (optional)

Zero, one or more `[[data_augmentation]]` sections can be present in the configuration.
They correspond to dataaugmentation modules to apply successively during training to the data before injecting it into the model in the `training` action.

Dataaugmentation modules with their `before` attribute will all be applied before sending the data to the device (e.g., GPU).
Dataaugmentation modules with their `after` attribute will all be applied after sending the data to the device (e.g., GPU).
In order words, the ordering of dataaugmentation modules only affect the `before` and the `after` independently,
as modules marked `before` will always be applied before the modules marked `after`.
A dataugmentation module cannot have both `before` and `after` set to `true`.

Dataaugmentation modules with their `evaluate` attribute set to `true` will also affect inference, both in the  `training` and the `deploy_and_evaluate` actions.

For more information about available preprocessing modules and their parameters, see <inv:#qualia_core.dataaugmentation>.

List of settings:
- **`kind` (string)**: name of the preprocessing class to apply.
- **`params` (array of string, optional)**: keyword parameters to pass to the preprocessing class constructor.
- **`params.before` (boolean, optional)**: if `true`, apply before transfering the data to the device (e.g., GPU), default to `false`.
- **`params.after` (boolean, optional)**: if `true`, apply after transfering the data to the device (e.g., GPU), default to `true`.
- **`params.evaluate` (boolean, optional)**: if `true`, apply during inference as well, default to `false`.

### `[[postprocessing]]` (optional)

Zero, one or more `[[postprocessing]]` sections can be present in the configuration.
They correspond to postprocessing modules to apply successively on the model after performing the initial training in the `train` action.
Postprocessing modules are also applied after loading the model in the `prepare_deploy` and `deploy_and_evaluate` actions.

Postprocessing module can change the name of a model the learning framework currently in use.
These transformations are applied during the application of the module in the `training` action,
but before instantiating the model in the `prepare_deploy` and `deploy_and_evaluate actions`.

For more information about available postprocessing modules and their parameters, see <inv:#qualia_core.postprocessing>.
Plugins may also load their own postprocessing modules or override existing ones.

List of settings:
- **`kind` (string)**: name of the preprocessing class to apply.
- **`params` (array of string, optional)**: keyword parameters to pass to the preprocessing class constructor.
- **`export` (boolean, optional)**: if `true`, save the weights of the model afterwards, default to `false`.
  This may or may not erase the existing model weights depening on whether the postprocessing module changes the name of the model.

### `[model_template]`

Common training and model settings that are inherited by each of the `[[model]]` section.

For more information about available learning models for each learning framework and their parameters, see <inv:#qualia_core.learningmodel>.
Plugins may also load their own learning framework and bring their own learning models alongside.

List of settings:
- **`load` (boolean, optional)**: if `true`, load existing model weights, default to `false`.
- **`train` (boolean, optional)**: if `false`, do not perform training, default to `true`.
- **`evaluate` (boolean, optional)**: if `false`, do not perform evaluation of the model, default to `true`.
- **`epochs` (integer)**: number of training epochs.
- **`batch_size` (integer)**: training and inference batch size.
- **`kind` (string)**: name of the learning model class.
- **`params` (table)**: keyword parameters to pass to the learning model class constructor.

#### `[model_template.optimizer]`

Optimizer settings passed to the learning framework.

For more information about available optimizer and their parameters, see the appropriate learningframework in <inv:#qualia_core.learningframework>.

List of settings:
- **`kind` (string)**: name of optimizer class to use.
- **`params` (string)**: keyword parameters to pass to the optimizer class constructor.

#### `[model_template.optimizer.scheduler]` (optional)

Learning rate scheduler settings passed to the learning framework.

For more information about available learning rate scheduler and their parameters, see the appropriate learningframework in <inv:#qualia_core.learningframework>.

List of settings:
- **`kind` (string)**: name of learning rate scheduler class to use.
- **`params` (string)**: keyword parameters to pass to the learning rate scheduler class constructor.

### `[[model]]`

One or more learning model configuration to process successively in the `train`, `prepare_deploy` and `deploy_and_evaluate` actions.

Each `[[model]]` section inherits from the common `[model_template]`, but can override any setting, including optimizer.

For more information about available learning models for each learning framework and their parameters, see <inv:#qualia_core.learningmodel>.
Plugins may also load their own learning framework and bring their own learning models alongside.

List of settings:
- **`name` (string)**: model name used to save weights and log results, must be unique.
- **`load` (boolean, optional)**: if `true`, load existing model weights, overrides `[model_template]`.
- **`train` (boolean, optional)**: if `false`, do not perform training, overrides `[model_template]`.
- **`evaluate` (boolean, optional)**: if `false`, do not perform evaluation of the model, overrides `[model_template]`.
- **`epochs` (integer, optional)**: number of training epochs, overrides `[model_template]`.
- **`batch_size` (integer, optional)**: training and inference batch size, overrides `[model_template]`.
- **`kind` (string, optional)**: name of the learning model class, overrides `[model_template]`.
- **`params` (table, optional)**: keyword parameters to pass to the learning model class constructor, merged with `[model_template]` and overrides conflicting settings.
- **`disabled` (boolean, optional)**: if `true`, skip this model, default to `false`.
