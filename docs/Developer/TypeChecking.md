# Type checking

```{contents} Table of Contents
---
depth: 3
---
```

Python is originally a dynamic and implicitely typed language.
However, dynamic typing can be the source of many bugs, so in an attempt to make Python code more robust, static type checking with type hints was introduced.

It is important to understand that type hints have absolutely **no effect** on the execution of the code.
Good type hints, no type hints, wrong type hints will always produce the same result at runtime.
Type hints are only useful when combined to the use of a static type checker.

The static type checker will analyse the variable and functions to make sure their usage correspond to the type they were declared with.
As an example, with proper type hints, ``None`` types should always be handled so ``NoneType`` related errors should be eliminated.
This is similar to using ``Optional`` in Java to avoid ``NullPointerException``.

## Caveats

Some notable peculiarities of static type checking:
- A variable cannot change type once it has been declared.
- Containers cannot contain objects of types that are unknown at the time of the container's declaration. By extension, this also greatly limits the usage of `*args` and `**kwargs` which should now be avoided, as it is not possible to pass or forward arbitrary arguments anymore.
- Duck typing should be forgotten and proper polymorphism used instead.
- Conforming to strict type checking can sometimes be difficult, but this may reveal that the code or architecture is too complex to begin with, so it can be a good opportunity to simplify and write the code in a more straightforward manner.
- As the name implies, static means that behaviours that are too "dynamic" will not be compatible with static type checking.

## Type checking in Qualia

In Qualia, "strict" type checking is used as much as possible.
There's no universal definition of "strict" type checking as it depends on the type checker and its rule set.
However, it generally means that you cannot have partially type-hinted code or uknown types.
Type parameter for generics, e.g., containers like `list[]` are important.
At the time of writing, not all modules have been fully typed. Some external libraries are not typed either.

In Qualia, the default type checker is [mypy](https://github.com/python/mypy) as it is slightly more flexible than other type checkers and is smarter at infering some complicated types.
However, it has extremely poor performances and it is completely unreasonable to use during development as a result.

For development, it is highly recommended to use [pyright](https://github.com/microsoft/pyright).

In the future, a complete switch to pyright might be considered.

### Postponed evaluation of annotations

Generally, modules should have `from __future__ import annotations` at the top of the file in order
to enable postponed evaluation of annotations.

Among other perks, this allows using some newer annotations syntax like `|` on older versions of Python, provided the type checker understands them.
This also allows forward references.

### Union type with `|`

Postponed evaluation of annotations enables the use of newer features that may not be compatible with Python 3.9
(currently the oldest supported version for Qualia).

Therefore, it is recommended to write Union annotations as ``X | Y`` and Optional annotations as ``X | None``
as recommended by [PEP 604](https://peps.python.org/pep-0604/)

### Custom TYPE_CHECKING constant

With [PEP 563](https://peps.python.org/pep-0563/), modules that are only used for type checking should be enclosed
in a `if typing.TYPE_CHECKING` block.
However, this currently prevents Sphinx Autodoc from generating correct types for these modules.

Therefore, Qualia introduces `qualia_core.typing.TYPE_CHECKING` and `qualia_codegen_core.typing.TYPE_CHECKING` constants
that always evaluate to `True` when Sphinx Autodoc is running, to use in place of `typing.TYPE_CHECKING`.

However, Ruff will still trigger a warning for import statements that should be in a `TYPE_CHECKING` block
when Qualia's `TYPE_CHECKING` constant is used. The Ruff rule stays enabled by default as a hint for the developer to put
imports in the `TYPE_CHECKING` block, but if they are already in Qualia's `TYPE_CHECKING` block, the corresponding rule (TCH001-TCH003)
may be ignored for each of them by adding for example `  # noqa: TCH002` at the end of the line.

Additionally, some imports for type checking may still trigger a circular import situation which would cause Sphinx Autodoc
to fail. In that case, a standard `typing.TYPE_CHECKING` block should be used for the problematic import instead of Qualia's `TYPE_CHECKING`.

See <Developer/Documentation> for more information about Sphinx Autodoc, and <Developer/CodeStyleLinter> for more information about the Ruff linter.

### Override decorator

`@override` is not a type annotation but a decorator
However it is used for typing to signify a derived class is overriding a base classe method,
and to check the signature of an overriden method in a derived class compared to the base class' method signature.

`@override` was introduced with [PEP 698](https://peps.python.org/pep-0698/) as part of Python 3.12,
therefore it is not available in older Python version, and being a decorator, postponed evaluation of annotations does not help.

Usage of override in derived classes is highly recommended, and it should be imported with the following piece of code
until support for the last version that does not include it is dropped:

```python
import sys
if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override
```


## Run mypy

Make sure the `typecheck` dependency group is installed, e.g.:
```
pdm install -G typecheck
```

Then run:
```
mypy
```

This will take several minutes to complete the first time using 100% of the CPU. This is expected.
Subsequent runs will complete faster, but still much slower than required for real-time analysis.

## Run pyright

Make sure the `typecheck` dependency group is installed, e.g.:
```
pdm install -G typecheck
```

Then run:
```
pyright
```

## IDE Integration

### VS Code

Use the [ms-pyright extension](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright).

### LunarVim

Install `pyright`  on your system, e.g., on ArchLinux:
```
sudo pacman -S pyright 
```

Edit your LunarVim configuration (`~/.config/lvim/config.lua`) to disable the built-in LSP servers and enable `pyright`:
```
vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "pylyzer", "pylsp", "ruff_lsp", "pyright" })

local opts = {}
require("lspconfig")["pyright"].setup(opts)
```

## CI/CD

After pushing new commits, the Gitlab CI/CD script (`.gitlab-ci.yml`) will automatically run the `mypy` as part of the `check` stage,
after running tests and before uploading the Python package and updating the documentation (depending on the component).

## References

- <https://docs.python.org/3/library/typing.html>
- <https://peps.python.org/pep-0484/>
- <https://peps.python.org/pep-0526/>
- <https://peps.python.org/pep-0563/>
- <https://peps.python.org/pep-0604/>
- <https://peps.python.org/pep-0698/>
