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

A Qualia configuration file is divided in multiple sections

### `[bench]`

name
seed
first_run
last_run
plugins

### `[learningframework]`

### `[deploy]`

### `[dataset]`

### `[[preprocessing]]`

### `[[data_augmentation]]`

### `[[postprocessing]]`

### `[model_template]`

#### `[model_template.optimizer]`

#### `[model_template.optimizer.scheduler]`

### `[[model]]`

## Example configuration file
