# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

project = 'whot'
copyright = '2025, Eteims'
author = 'Eteims'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_copybutton"
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#306998",  # blue from logo
        "color-brand-content": "#0b487a",  # blue more saturated and less dark
    },
    "dark_css_variables": {
        "color-brand-primary": "#ffd43bcc",  # yellow from logo, more muted than content
        "color-brand-content": "#ffd43bd9",  # yellow from logo, transparent like text
    },
    "sidebar_hide_name": True,
}

html_logo = "_static/PyWhot.svg"

html_favicon = "_static/pywhot_transparent.png"


html_static_path = ['_static']
