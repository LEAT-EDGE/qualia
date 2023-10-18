# Update

```{contents} Table of Contents
---
depth: 3
---
```

## User setup

### Existing Python environment with Pip

Pip will not handle the update of all your Python packages. It will only allow updating the specified Qualia's component and installing new dependencies when required.

Run, specifying all the Qualia's components your are using and their optional depencency groups in brackets:
```
pip install -U qualia-core[pytorch] --extra-index-url=https://naixtech.unice.fr/devpi/penovac/qualia-nightly/+simple --trusted-host naixtech.unice.fr 
```

#### Dedicated in-project environment with PDM

Move into the base Qualia directory:
```
cd qualia-master
```

Activate the environment with:
```
$(pdm venv activate)
```

Then run:
```
pdm update
```

## Developer setup

### Update Qualia's components

Updating Qualia's components in the developer setup is done by fetching and merging the new changes from the git repositories.

If working off of the `master` branch, a `git pull` in the component's repository should be enough.

Repeat this step for any additional Qualia component you are using.

### Update third-party dependencies

You may need to update third-party dependencies in case a breaking change happened.

#### Dedicated in-project environment with PDM

Move into the base qualia directory:
```
cd qualia
```

Activate the environment with:
```
$(pdm venv activate)
```

Then run:
```
pdm update
```

#### Existing environment with Pip

Pip will not handle the update of all your Python packages. It will only allow installing new dependencies when required.

Move into the Qualia's component directory, e.g., for Qualia-Core:
```
cd qualia-core
```

Then run, specifying optional depencency groups in brackets:
```
pip install -e .[pytorch]
```

Repeat this step for any additional Qualia component you are using, in order from the root of the dependency graph (see <project:User/Components.md>).
