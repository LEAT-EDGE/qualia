# Migration from previous versions

## Migration from 1.0 (known as MicroAI)

Qualia was previously known as MicroAI in its 1.0 version. For users of MicroAI 1.0, Qualia 2.0 mainly brings 3 major breaking changes:

1. Plugin system
2. Renaming MicroAI to Qualia
3. Renaming KerasCNN2C to Qualia-CodeGen

The codebase structure stays mostly the same, except for the split in plugins.

### Plugin system

The plugin system is only relevant for users of the post-1.0 private development version
using self-organizing maps, spiking neural networks and/or SPLEAT deployment.
The public 1.0 version does not contain these features.

In order to migrate to Qualia 2.0 when these features are in use, the appropriate plugin must be installed and enable in the configuration file.

For example, to use the spiking neural networks and SPLEAT deployment features, add to the configuration:
```toml
[bench]
plugins = ['qualia_plugin_snn', 'qualia_plugin_spleat']
```

For more information about the available plugins, see: <project:Components.md>. For more information about the configuration file, see: <project:ConfigurationFile.md>.

### Renaming MicroAI to Qualia

The name `microai` (capitalized as MicroAI) was dropped from the entire code base and the name `qualia` (capitalized as Qualia) should be used instead.

Note that due to the changes related to plugin system, the root Python packages are named as follow:
- `qualia_core` (capitalized as Qualia-Core): derived from the public 1.0 version and some additional features,
- `qualia_plugin_snn` (capitalized as Qualia-Plugin-SNN): the spiking neural network-related features,
- `qualia_plugin_spleat` (capitalized as Qualia-Plugin-SPLEAT): the SPLEAT deployer.

### Renaming KerasCNN2C to Qualia-CodeGen

KerasCNN2C was the name of the code generation tool available as part of MicroAI 1.0.
Originally intended to convert Keras models to a C inference library, it since gained support for PyTorch and other targets (SPLEAT),
therefore it is now named Qualia-CodeGen.

The name `kerascnn2c` (capitalized as KerasCNN2C) was dropped from the entire code base and
the name `qualia_codegen` (capitalized as Qualia-CodeGen, or QualiaCodeGen only if hyphens are no allowed) should be used instead.


Note that due to the changes related to plugin system, the root Python packages are named as follow:
- `qualia_codegen_core` (capitalized as Qualia-CodeGen-Core): derived from the public 1.0 version and some additional features,
- `qualia_codegen_plugin_snn` (capitalized as Qualia-CodeGen-Plugin-SNN): the spiking neural network-related features,
- `qualia_codegen_plugin_spleat` (capitalized as Qualia-CodeGen-Plugin-SPLEAT): the SPLEAT configuration generator.
