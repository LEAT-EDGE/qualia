# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

import sphinx.application

root_path = Path('..').resolve()

sys.path.insert(0, str(root_path/'src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Qualia'
copyright = '2023, Pierre-Emmanuel Novac'
author = 'Pierre-Emmanuel Novac'

qualia_doc_base_url = 'https://leat-edge.github.io' if os.getenv('GITHUB_ACTIONS') else 'http://naixtech.unice.fr/~gitlab/docs'

myst_substitutions = {
        'qualia_git_ssh_base_url': 'git@github.com:LEAT-EDGE' if os.getenv('GITHUB_ACTIONS') else 'ssh://git@naixtech.unice.fr:2204/qualia',
        'qualia_git_https_base_url': 'https://github.com/LEAT-EDGE' if os.getenv('GITHUB_ACTIONS') else 'https://naixtech.unice.fr/gitlab/qualia',
        'qualia_archive_url': ('https://github.com/LEAT-EDGE/qualia/archive/refs/heads/master.tar.gz'
                        if os.getenv('GITHUB_ACTIONS') else 'https://naixtech.unice.fr/gitlab/qualia/qualia/-/archive/master/qualia-master.tar.gz'),
        'qualia_extra_index': ('' if os.getenv('GITHUB_ACTIONS')
                               else ' --extra-index-url=https://naixtech.unice.fr/devpi/penovac/qualia-nightly/+simple --trusted-host naixtech.unice.fr'),
        'qualia_doc_base_url': qualia_doc_base_url,
}

# The full version, including alpha/beta/rc tags
def pdm_get_version(root_path: Path) -> str:
    import pdm.core
    import pdm.models.project_info

    core = pdm.core.Core()
    project = core.create_project(root_path=root_path)
    metadata = project.make_self_candidate(False).prepare(project.environment).prepare_metadata(True)
    project_info = pdm.models.project_info.ProjectInfo.from_distribution(metadata)

    return project_info.version

release = pdm_get_version(root_path=root_path)
version = release

# -- General configuration ---------------------------------------------------


extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
]

# Only include supported extensions
myst_enable_extensions = [
    'substitution',
    'linkify',
    'colon_fence',
    'deflist',
    'tasklist'
]

# Enable anchor generation for headers
myst_heading_anchors = 3


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx.
language = 'en'

html_title = f"{project} Documentation"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "furo"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#336790",
        "color-brand-primary-dark": "#1c3951",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fb",
        "color-foreground-primary": "#000000",
        "color-foreground-secondary": "#555555",
    },
    "dark_css_variables": {
        "color-brand-primary": "#84B2DC",
        "color-brand-primary-dark": "#C4E1FF",
        "color-background-primary": "#1a1a1a",
        "color-background-secondary": "#25282f",
        "color-foreground-primary": "#ffffff",
        "color-foreground-secondary": "#aaaaaa",
    },
}

html_static_path = ['_static']

html_search_options = {
    'type': 'default',
    'dict': None,
    'languages': ['en'],
}

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'PyTorch': ('https://pytorch.org/docs/stable/', None),
    'qualia_core': (f'{qualia_doc_base_url}/qualia-core', None),
    'qualia_plugin_snn': (f'{qualia_doc_base_url}/qualia-plugin-snn', None),
    'qualia_plugin_spleat': (f'{qualia_doc_base_url}/qualia-plugin-spleat', None),
    'qualia_plugin_som': (f'{qualia_doc_base_url}/qualia-plugin-som', None),
    'qualia_plugin_template': (f'{qualia_doc_base_url}/qualia-plugin-template', None),
    'qualia_codegen_core': (f'{qualia_doc_base_url}/qualia-codegen-core', None),
    'qualia_codegen_plugin_snn': (f'{qualia_doc_base_url}/qualia-codegen-plugin-snn', None),
    'qualia_codegen_plugin_spleat': (f'{qualia_doc_base_url}/qualia-codegen-plugin-spleat', None),
    'qualia_codegen_plugin_som': (f'{qualia_doc_base_url}/qualia-codegen-plugin-som', None),
}

show_authors = True

napoleon_use_ivar = True

# Autodoc configuration
autodoc_mock_imports = []
autoclass_content = 'class'
autodoc_class_signature = 'separated'
autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = False
autodoc_typehints = 'both'
autodoc_default_options = {'special-members': '__init__, __call__'}

master_doc = 'index'

# Enable TYPE_CHECKING blocks for autodoc
os.environ['SPHINX_AUTODOC'] = '1'

# Call sphinx-apidoc
def run_apidoc(_: sphinx.application.Sphinx) -> int:
    from sphinx.ext.apidoc import main
    return main(['-e',
          '-o',
          str(Path().resolve()/'source'),
          str(root_path/'src'/'qualia'),
          '--force'])

def setup(app: sphinx.application.Sphinx) -> None:
    if True:
        return
    _ = app.connect('builder-inited', run_apidoc)