# Usage

## Overview

Qualia uses configuration files in order to describe an experiment, which consists of 
a dataset, dataset preprocessing steps, learning model, training configuration, learning model postprocessing steps and a deployment configuration.

For more information about the configuration file, see <project:ConfigurationFile.md>.

## Run Qualia

Do not forget to activate your Python virtual environment first, e.g., when using PDM:

```bash
$(pdm venv activate)
```

Qualia is launched from the command line with the `qualia` command:

```bash
qualia <config.toml> <action> [config_params]
```

`config.toml` is the path to the configuration file for this experiment.

`action` is one of the action described below.

`config_params` are optional arguments to override settings from the configuration file.
They are specified with the format `--<key1>.<key...>.<keyn>=<value>`.
`key` can be a string to index a dictionary or an integer to index a list. `value` is evaluated as a Python expression.
For example, to override the `name` setting in the `[bench]` section: `--bench.name="Test"`;
and to override the `disabled` parameter of the first `[[model]]`: `--model.0.disabled=True`.

It it recommended to avoid adding any `config_params` as the configuration file itself should reflect all the settings for an experiment.

Currently, Qualia offers 4 actions that are designed to be run in sequence and described thereafter.

### `preprocess_data`

`preprocess_data` will load the dataset specified in the `[dataset]` section of the configuration file,
then apply the preprocessing steps specified in the `[[preprocessing]]` sections of the configuration file, from first to last.

The processed dataset is then exported as [Zstandard](https://github.com/facebook/zstd)-compressed NumPy arrays for better interoperability.

The exported data can be found in the `out/data/<dataset_name>` folder.

Note that the data is assumed to be in `channels_last` format, with `[N, H, W, C]` order for 2D data or `[N, S, C]` order for 1D data.

### `train`

`train` starts the training process for each model specified in `[[model]]` sections of the configuration file, from first to last.
Note that each `[[model]]` section inherits the settings from the `[model_template]` section but they can be overriden.

The training is performed with the learning framework specified in the `[learningframework]` section

The trained model weights are saved in the `out/learningmodel` folder with the model name in the file name.
The format of the file depends on the chosen learning framework.
The results are saved in the `log/<bench_name>/learningmodel` folder.

After each model training is done, the model postprocessing steps specified in `[[postprocessing]]` sections of the configuration file are applied.

Postprocessing steps may change the model name and re-export the weights if their `export` setting is set to `true`.

### `prepare_deploy`

`prepare_deploy` prepares the files to be deployed on the target configured in the `[deploy]` section of the configuration file,
for each model specified in `[[model]]` sections, from first to last.

First, a converter module is called in order to convert the trained learning model to a format suitable for the target.
For example, this may perform code generation using Qualia-CodeGen.
The conversion will export files in the `out/<converter>` folder.

Then, this converted model is prepared for deployment.
For example, this may perform compilation of the generated source code to produce a firmware image.
The prepared files are saved in the `out/<deploy>` folder.

### `deploy_and_evaluate`

`deploy_and_evaluate` deploys the files prepared with `prepare_deploy` onto the target configured in the `[deploy]` section of the configuration,
then runs the on-target evaluation. This is performed for each model specified in `[[model]]` sections, from first to last.

The results are saved in the `log/<bench_name>/evaluate` folder.
