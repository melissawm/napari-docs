# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import re
import os
from datetime import datetime
from importlib import import_module
from importlib.metadata import distribution
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from jinja2.filters import FILTERS
from sphinx.highlighting import lexers
from packaging.version import parse as parse_version
from pygments.lexers import TOMLLexer

import napari
from napari._version import __version_tuple__

release = napari.__version__
if "dev" in release:
    version = "dev"
else:
    version = release

# -- Project information -----------------------------------------------------

project = 'napari contributing guide'
copyright = f'{datetime.now().year}, The napari team'
author = 'The napari team'

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_external_toc",
    "sphinx_design",
    'myst_nb',
    #    "sphinx_comments",
    "sphinx.ext.viewcode",
    "sphinx_favicon",
    "sphinx_copybutton",
    "sphinx_tags",
]

external_toc_path = "_toc.yml"
external_toc_exclude_missing = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'napari_sphinx_theme'

html_theme_options = {
    "external_links": [
        {"name": "napari hub", "url": "https://napari-hub.org"}
    ],
    "github_url": "https://github.com/napari/napari",
    "navbar_start": ["navbar-logo", "navbar-project"],
    "navbar_end": ["navbar-icon-links"],
    "navbar_center": ["navbar-nav"],
    "navbar_persistent": [],
    "header_links_before_dropdown": 6,
    "secondary_sidebar_items": ["page-toc"],
    "pygments_light_style": "napari",
    "pygments_dark_style": "napari",
    "announcement": "https://napari.org/dev/_static/announcement.html",
}

html_sidebars = {"**": ["sidebar-nav-bs"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_static']
html_logo = "../_static/images/logo.png"
html_sourcelink_suffix = ''
html_title = 'napari'

favicons = [
    {
        # the SVG is the "best" and contains code to detect OS light/dark mode
        "static-file": "favicon/logo-silhouette-dark-light.svg",
        "type": "image/svg+xml",
    },
    {
        # Safari in Oct. 2022 does not support SVG
        # an ICO would work as well, but PNG should be just as good
        # setting sizes="any" is needed for Chrome to prefer the SVG
        "sizes": "any",
        "static-file": "favicon/logo-silhouette-192.png",
    },
    {
        # this is used on iPad/iPhone for "Save to Home Screen"
        # apparently some other apps use it as well
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "static-file": "favicon/logo-noborder-180.png",
    },
]

html_css_files = [
    'custom.css',
]

intersphinx_mapping = {
    'python': ['https://docs.python.org/3', None],
    'numpy': ['https://numpy.org/doc/stable/', None],
    'napari_plugin_engine': [
        'https://napari-plugin-engine.readthedocs.io/en/latest/',
        'https://napari-plugin-engine.readthedocs.io/en/latest/objects.inv',
    ],
    'magicgui': [
        'https://pyapp-kit.github.io/magicgui/',
        'https://pyapp-kit.github.io/magicgui/objects.inv',
    ],
    'napari': (
        'https://melissawm.github.io',
        (None, '../_build/napari_objects.inv')
    ),
}

myst_enable_extensions = [
    'colon_fence',
    'dollarmath',
    'substitution',
    'tasklist',
]

myst_heading_anchors = 4


def get_supported_python_versions(project_name):
    """
    Get the supported Python versions for a given project
    based on the classifiers in its distribution metadata.
    """
    dist = distribution(project_name)
    classifiers = [value for key, value in dist.metadata.items() if key == 'Classifier' and value.startswith('Programming Language :: Python ::')]
    return [parse_version(c.split(' :: ')[-1]) for c in classifiers if not c.endswith('Only')]


napari_supported_python_versions = get_supported_python_versions('napari')

min_python_version = min(napari_supported_python_versions)
max_python_version = max(napari_supported_python_versions)

version_string = '.'.join(str(x) for x in __version_tuple__[:3])
python_version = '3.10'
python_version_range = f"{min_python_version}-{max_python_version}"

myst_substitutions = {
    "napari_conda_version": f"`napari={version_string}`",
    "napari_version": version_string,
    "python_version": python_version,
    "python_version_range": python_version_range,
    "python_version_code": f"`python={python_version}`",
    "conda_create_env": f"```sh\nconda create -y -n napari-env -c conda-forge python={python_version}\nconda activate napari-env\n```",
}

myst_footnote_transition = False

nb_output_stderr = 'show'

panels_add_bootstrap_css = False
pygments_style = 'solarized-dark'
suppress_warnings = ['myst.header', 'etoc.toctree']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '.jupyter_cache',
    'jupyter_execute',
    'plugins/_*.md',
    'gallery/index.rst',
]

lexers['toml'] = TOMLLexer(startinline=True)
