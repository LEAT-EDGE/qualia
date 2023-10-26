# Plugin architecture

Qualia 2.0 introduces a plugin system in order to split optional modules from the core.

Basically, a plugin is a collection of package and modules organized in a way similar to the core it extends (Qualia-Core or Qualia-CodeGen-Core).

For more information about the package structure, see <project:PackageStructure.md>.


## Purpose

The plugin system enables the isolation of the feature development that fall into one of these categories:
1. Features using external dependencies with licensing problems (not AGPL-3.0 compatible)
2. Proprietary features not intended to be published under open-source license
3. Experimental features not (yet) intended for the main development branch

For example, these plugins fall into one of the category:
- Qualia-Plugin-SNN falls into category 1. due to the dependency on SpikingJelly ("Disclosure of Commercial Use" license requirement).
- Qualia-Plugin-SPLEAT falls into category 2. as SPLEAT is not indended for open-source release.
- Qualia-Plugin-SOM (not available yet) falls into category 3. due to its experimental nature.

## Use a plugin

A plugin is loaded by Qualia-Core when the top-level package name is specified in the `plugins` setting of the `[bench]` section in the configuration file.

For example, in order to load Qualia-Plugin-SNN and Qualia-Plugin-SPLEAT for SPLEAT deployment:
```toml
[bench]
plugins = ['qualia_plugin_snn', 'qualia_plugin_spleat']
```

Qualia-Core will then merge and override any conflict with the content of the following packages from the plugins (in the order they are liste in the configuration):
- `preprocessing`
- `learningframework`
- `postprocessing`

Other subpackages are not imported directly. It is up to the plugin to load them from one of the imported module.

For example, Qualia-Core loads the `learningframework` package from the plugins.
The plugin can add a new learningframework with its own set of learningmodels to be used in the configuration,
or override an existing learningframework by inheriting from it and using the same name to extend the learningmodels.

Similarly, the plugin can add new model converters in `postprocessing` or override an existing one for use in the `[deploy]` section of the configuration.
This way, the new or overriden model converter can suggest different or overriden deployers which themselves can be suggest different or overiddend evaluator modules.


## Create a plugin

It is recommend to take inspiration from the existing plugins (e.g., Qualia-Plugin-SNN or Qualia-Plugin-SPLEAT) to write a new one.

A plugin is a Python project that should follow the usual packaging processes and use the common <project:RepositoryStructure.md>.
Make sure to fill the correct project metadata in the `pyproject.toml` file as well as the dependencies.

Then, you can add new Python modules in one of the subpackage listed in <project:PackageStructure.md>.
In Qualia, each Python module generally contains one class for its implementation.
If the Python module is suppposed to override an existing one, it should inherit from the class it overrides then only implement the required changes.


Qualia Plugin Template provides a template project that should be used to create a new plugin.
Follow the documentation at [Qualia Plugin Template](inv:qualia_plugin_template:std:doc#index).
