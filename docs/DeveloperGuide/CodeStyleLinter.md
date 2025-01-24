# Code style and linter

## Code style

Code style should try to be homogeneous across the entire project as much as possible.
It is recommended to read exisiting code to get familiar with the current style.

### Python

Python source code should always try to follow the [PEP 8](https://peps.python.org/pep-0008/) guide.

However, there are 2 major exceptions to these rules in the Qualia codebase:

**Line length:** line length is limited to 131 columns instead of the 79 limit or the 99 tolerance,
however this should not justify abusing complex one-liners or indented blocks.
And function arguments can still be wrapped before reaching the limit, and developers are free to stick to a tighter limit if preferred.
It is recommended to use an [EditorConfig](https://editorconfig.org/)-aware editor so that the 131 columns
limit is applied to Python source files.

**Module name case:** modules that contain a single public class can take the name of the class in CamelCase rather than lowercase.
Other modules should still follow the lowercase rule.

The second exception is accompanied by a recommendation to avoid packing multiple independent public classes in the same module
in order to avoid excissively long files and keep the codebase more flexible.

### C/C++

C and C++ do not have an official recommendation on the code style. There are many code styles in use in different projects.
However, a project should stick to a single code style across the board.

Qualia does not have a well-defined C/C++ code style (yet).
It is recommended to get inspiration from existing source code.
However, here are some general rules currently used in the codebase:
- K&R style
- Opening brace of blocks on same line as control structure statement (if, for…)
- Content of block indented by one level
- Closing brace at the same level as the control structure statement
- Single space before opening brace
- Single space after closing brace when followed by a `else`
- Single space between keyword and opening parenthesis
- No space between function name and opening parenthesis
- Space around operators
- One statement per line
- C++ code generally uses single tab indentation rendered as 4-wide indent (e.g., Qualia-Server)
- C code generally uses 2 spaces indentation (e.g., Qualia-CodeGen)

It is higly recommended to use an [EditorConfig](https://editorconfig.org/)-aware editor so that space or tab indentations are applied to the appropriate files.
The different indentations may be consolidated in the future.

## Linter
A linter is a kind of static analysis tool that helps following a given code style and attempts to detect common bad practices.

In Qualia, there is currently no linter used for the C/C++ source code.
In particular, static analysis of templace C code would prove to be difficult.
Therefore this section only covers the Python source code.

[Ruff](https://github.com/astral-sh/ruff) with most rules enabled is used for Python source code.


### Run Ruff linter standalone

Make sure the `lint` dependency group is installed, e.g.:
```
pdm install -G lint
```

Then run:
```
ruff src
```

### IDE Integration

#### VS Code

Use the [ruff-vscode extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).

#### LunarVim

Install `ruff` and `ruff-lsp` on your system, e.g., on ArchLinux:
```
sudo pacman -S ruff ruff-lsp
```

Edit your LunarVim configuration (`~/.config/lvim/config.lua`) to disable the built-in LSP servers and enable `ruff_lsp`:
```
vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "pylyzer", "pylsp", "ruff_lsp", "pyright" })

local opts = {}
require("lspconfig")["ruff_lsp"].setup(opts)
```

### CI/CD

After pushing new commits, the Gitlab CI/CD script (`.gitlab-ci.yml`) will automatically run the linter as part of the `check` stage,
after running tests and before uploading the Python package and updating the documentation (depending on the component).

### Currently disabled Ruff rules

- ANN101: Ignore missing type annotation for self in methods, keep it implicit for now
- ANN102: Ignore missing type annotation for self in class methods, keep it implicit for now
- N999: Ignore invalid module name, our module have the same name as the contained class in PascalCase
- D203: Conflicting rule, prefer D211
- D213: Conflicting rule, prefer D212 which is also ruff's preference
