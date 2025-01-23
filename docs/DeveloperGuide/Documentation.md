# Writing documentation

## API documentation

API documentation is the documentation associated to the source code.
It describes each part of the code base in its hierarchical structure: packages, modules, classes, attributes and methods.

In Python, this documentation is part of each of these item and written as a [docstring](https://peps.python.org/pep-0257/).
Other programming languages have similar facilities, often written as comment blocks.

In Qualia, the docstrings are collected using Sphinx' [Autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) module.
They are then parsed by Sphinx as [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html).
Therefore, the written docstrings must conform both to the reStructuredText syntax and the Autodoc syntax.
Autodoc is automatically called when the documentation is re-generated.

It is recommended to get familiar with the writing rules by taking a look at existing Qualia's APIs documentation.

Here is an example of a docstring-annotated module containing a class with an attribute and a method:

```python
"""Contains an example Counter class to illustrate docstrings."""

class Counter:
    """Example Counter class to illustrate the usage of docstrings."""

    x: int = 0 #: Current counter value

    def add(self, y: int) -> int:
        """Add a positive ``y`` value to the counter then return the new counter value.

        This is a very simple operation that add the current counter value :attr:`x` to the provided ``y`` value,
        store it back into :attr:`x` then return the result of the operation.

        Only positive values for ``y`` are supported.

        :param y: Value to add to the counter
        :return: New value of the counter
        :raise ValueError: If ``y`` is negative
        """
        if y < 0:
            raise ValueError
        x += y
        return x
```

In this example, `` :attr:`x` `` references the attribute `x` of the current class.
Any Python object can be referenced, such as packages and modules with `:mod:`, classes with `:class:`, attributes with `:attr:` and methods with `:meth:`.
The fully-qualified name of the object must be provided if it is outside the current scope, e.g., `` :attr:`package.module.Class.attribute` ``.

External projects can also be referenced, provided their documentation is compatible
with [InterSphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) and referenced in the `intersphinx_mapping` dict of
the `docs/conf.py` Sphinx configuration file.

## High-level documentation

High-level documentation is independent from the source code structure.
Obviously, it cannot be generated automatically (please don't tell me about whatever generative large language model is popular right now).
However, it is still part of the Sphinx process to include it into the documentation website.

This documentation is mostly split into two parts:
- User's manual: mostly focuses on installation, configuration, usage and examples
- Developer's manual: mostly focuses on contributing to Qualia and developing new modules and plugins

Therefore, additional documentation pages should be put under the correct directory, and the correct index in `docs/index.rst`.

Documentation pages can either be redacted in reStructuredText or in MarkDown using [MyST parser](https://myst-parser.readthedocs.io/en/latest/).
ReStructuredText pages should have the `.rst` extension and Markdown pages should have the `.md` extension.

## Build the documentation

The documentation is built by [Sphinx](https://www.sphinx-doc.org/) as an HTML website.

Make sure the `docs` dependency group is installed, e.g.:
```
pdm install -G docs
```

Then run:
```
cd docs
make clean && make html
```

The documentation will be built as HTML under the `docs/_build/html/` directory, from which the `index.html` file can be opened in any browser.

## CI/CD

After pushing new commits, the Gitlab CI/CD script (`.gitlab-ci.yml`) or the GitHub Actions script (`.github/workflows/doc.yml`) will automatically update the online documentation
(currently hosted at {{ '<{}/qualia>'.format(qualia_doc_base_url) }}) as the last stage of the process, after running tests,
linter and typing checks, and uploading the Python package (depending on the component).
