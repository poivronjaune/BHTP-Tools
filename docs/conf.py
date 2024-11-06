# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# For Markdown source files
#import recommonmark.parser
#source_parsers = {
#    '.md': 'recommonmark.parser.CommonMarkParser',
#}
#
#source_suffix = ['.rst', '.md']

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BHTP'
copyright = '2024, PoivronJaune'
author = 'PoivronJaune'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Disable the "View source" link
html_show_sourcelink = False

autodoc_default_options = {
    'private-members': False,
    'special-members': False,
    'show-inheritance': True,
    'show-sourcelink': False,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
