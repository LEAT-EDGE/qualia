# Installation

```{contents} Table of Contents
---
depth: 3
---
```


Two setups are possible and described below: developer and user.

## Common requirements

- Python >= 3.9, < 3.12 ; recommended: 3.11
- Pip
- (Optional) Conda if the system's Python version is not suitable

## User setup

Use this setup if you do not plan on making modifications to one of Qualia's component source code. You can still develop your own, independent plugin with this setup.

You can either install Qualia in an existing virtual environment with Pip, or create a new environment managed by PDM.

### Existing Python environment with Pip

Any component of Qualia can be installed with `pip` in an existing environment by specifying our dedicated PyPI server URL [https://naixtech.unice.fr/devpi/penovac/qualia-nightly/+simple](https://naixtech.unice.fr/devpi/penovac/qualia-nightly/+simple)

You can also create a virtual environment for Qualia yourself.

Optional dependency groups must be specified in brackets after the package name, e.g., `qualia-core[pytorch]`.

For example, to install Qualia-Core with PyTorch support:
```
pip install -U qualia-core[pytorch] --extra-index-url=https://naixtech.unice.fr/devpi/penovac/qualia-nightly/+simple --trusted-host naixtech.unice.fr 
```

A Qualia component will automatically pull any other required Qualia components.

### Dedicated environment with PDM

#### Additional requirements
- PDM
    - On Ubuntu >= 22.10: `sudo apt install python3-pdm`
    - Or with Pip: `pip install pdm`

#### Dowload and extract the base Qualia project
Download: [https://naixtech.unice.fr/gitlab/qualia/qualia/-/archive/master/qualia-master.tar.gz](https://naixtech.unice.fr/gitlab/qualia/qualia/-/archive/master/qualia-master.tar.gz)

Extract it:
```
tar -xvf qualia-master.tar.gz
cd qualia-master
```

#### Create a new dedicated in-project virtual environment

If host's Python version is not 3.11, it is recommended to create a Conda environment with Python 3.11:
```
pdm venv create -w conda 3.11
pdm use .venv/bin/python
```

Otherwise you can use a simple virtualenv:
```
pdm venv create -w virtualenv
pdm use .venv/bin/python
```

#### Activate the virtual environment

You will need to perform this step for every new shell you open:
```
$(pdm venv activate)
```

#### Add a Qualia component to the environment

Add Qualia component, you can specify additional dependency groups in brackets, e.g., for Qualia-Core with Pytorch:
```
pdm add qualia-core[pytorch]
```

Repeat this step for any additional Qualia component you want to use, in order from the root of the dependency graph (see [Qualia Components](Components)).

## Developer setup

Use this setup if you want to make modifications to one of Qualia's component source code.

It is recommended to create a new Python environment for Qualia managed by PDM, but you can also install Qualia in an existing virtual environment with Pip.

### Additional requirements
- Git

### Recommended: Dedicated in-project environment with PDM

#### Additional requirements
- PDM
    - On Ubuntu >= 22.10: `sudo apt install python3-pdm`
    - Or with Pip: `pip install pdm`

#### Clone the base Qualia repository
```
git clone ssh://git@naixtech.unice.fr:2204/qualia/qualia.git
cd qualia
```

#### Create a new dedicated in-project virtual environment

If host's Python version is not 3.11, it is recommended to create a Conda environment with Python 3.11:
```
pdm venv create -w conda 3.11
pdm use .venv/bin/python
```

Otherwise you can use a simple virtualenv:
```
pdm venv create -w virtualenv
pdm use .venv/bin/python
```

#### Activate the virtual environment

You will need to perform this step for every new shell you open:
```
$(pdm venv activate)
```

#### Add a Qualia component to the environment

To add a Qualia component, e.g., Qualia-Core, first clone the repository:
```
git clone ssh://git@naixtech.unice.fr:2204/qualia/qualia-core.git
```
Then install it, you can specify additional dependency groups in brackets, e.g., for Qualia-Core with Pytorch:
```
pdm add -e ./qualia-core[pytorch] --dev
```

Repeat this step for any additional Qualia component you want to use, in order from the root of the dependency graph (see [Qualia Components](Components)).

You can then edit the source code in each of the cloned component repository and commit as usual.

### Existing Python environment with Pip

If you have an existing Python environment with a compatible version of Python, use `pip` to install Qualia components inside of it.

Clone the repository:
```
git clone ssh://git@naixtech.unice.fr:2204/qualia/qualia-core.git
```

Install it, specifying additional dependency groups in brakckets, e.g., for Qualia-Core with PyTorch:
```
cd qualia-core
pip install -e .[pytorch]
```

Repeat this step for any additional Qualia component you want to use, in order from the root of the dependency graph (see [Qualia Components](Components)).
