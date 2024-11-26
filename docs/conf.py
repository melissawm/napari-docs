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
import logging

from jinja2.filters import FILTERS
from sphinx_gallery import scrapers
from sphinx_gallery.sorting import ExampleTitleSortKey
from sphinx.highlighting import lexers
from sphinx.util import logging as sphinx_logging
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

project = 'napari'
copyright = f'{datetime.now().year}, The napari team'
author = 'The napari team'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
autosummary_generate = True
autosummary_imported_members = True
comments_config = {'hypothesis': False, 'utterances': False}

# execution_allow_errors = False
# execution_excludepatterns = []
# execution_in_temp = False
# execution_timeout = 30

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
    "sphinx_gallery.gen_gallery",
    "sphinx_tags",
]

external_toc_path = "_toc.yml"
external_toc_exclude_missing = False

tags_create_tags = True
tags_output_dir = "_tags"
tags_overview_title = "Tags"
tags_extension = ["md", "rst"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'napari_sphinx_theme'

# Define the json_url for our version switcher.
json_url = "https://napari.org/dev/_static/version_switcher.json"

if version == "dev":
    version_match = "dev"
else:
    version_match = release

html_theme_options = {
    "external_links": [
        {"name": "napari hub", "url": "https://napari-hub.org"},
        {"name": "Island Dispatch", "url": "https://napari.org/island-dispatch"},
        {"name": "Community chat", "url": "https://napari.zulipchat.com"},
        {"name": "workshop template", "url": "https://napari.org/napari-workshop-template"},
    ],
    "github_url": "https://github.com/napari/napari",
    "navbar_start": ["navbar-logo", "navbar-project"],
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
    "navbar_persistent": [],
    "header_links_before_dropdown": 6,
    "secondary_sidebar_items": ["page-toc"],
    "pygment_light_style": "napari",
    "pygment_dark_style": "napari",
    "announcement": "https://napari.org/dev/_static/announcement.html",
    "back_to_top_button": False,
    "analytics": {
        # The domain you'd like to use for this analytics instance
        "plausible_analytics_domain": "napari.org",
        # The analytics script that is served by Plausible
        "plausible_analytics_url": "https://plausible.io/js/plausible.js",
    },
    "footer_start": ["napari-footer-links"],
    "footer_end": ["napari-copyright"],
}

html_sidebars = {
    "**": ["search-field.html", "sidebar-nav-bs"],
    "index": ["search-field.html" , "calendar-template"],
}

html_context = {
   # use Light theme only, don't auto switch (default)
   "default_mode": "light"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = "_static/images/logo.png"
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
    'app-model': [
        'http://app-model.readthedocs.io/en/latest/',
        'http://app-model.readthedocs.io/en/latest/objects.inv',
    ],
}

myst_enable_extensions = [
    'colon_fence',
    'dollarmath',
    'substitution',
    'tasklist',
    'attrs_inline',
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
nb_execution_mode = "off"

panels_add_bootstrap_css = False
pygments_style = 'solarized-dark'
suppress_warnings = ['myst.header', 'etoc.toctree', 'config.cache']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

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
    'plugins/building_a_plugin/_layer_data_guide.md',
    'gallery/index.rst',
]

napoleon_custom_sections = [('Events', 'params_style')]
lexers['toml'] = TOMLLexer(startinline=True)


def reset_napari(gallery_conf, fname):
    from napari.settings import get_settings
    from qtpy.QtWidgets import QApplication

    settings = get_settings()
    settings.appearance.theme = 'dark'

    # Disabling `QApplication.exec_` means example scripts can call `exec_`
    # (scripts work when run normally) without blocking example execution by
    # sphinx-gallery. (from qtgallery)
    QApplication.exec_ = lambda _: None


def napari_scraper(block, block_vars, gallery_conf):
    """Basic napari window scraper.

    Looks for any QtMainWindow instances and takes a screenshot of them.

    `app.processEvents()` allows Qt events to propagateo and prevents hanging.
    """
    imgpath_iter = block_vars['image_path_iterator']

    if app := napari.qt.get_qapp():
        app.processEvents()
    else:
        return ""

    img_paths = []
    for win, img_path in zip(
        reversed(napari._qt.qt_main_window._QtMainWindow._instances),
        imgpath_iter,
    ):
        img_paths.append(img_path)
        win._window.screenshot(img_path, canvas_only=False)

    napari.Viewer.close_all()
    app.processEvents()

    return scrapers.figure_rst(img_paths, gallery_conf['src_dir'])

from sphinx_gallery import gen_rst

gen_rst.EXAMPLE_HEADER = """
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "{0}"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        :ref:`Go to the end <sphx_glr_download_{1}>`
        to download the full example anbs a Python script or as a
        Jupyter notebook.{2}

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_{1}:

"""

sphinx_gallery_conf = {
    # path to your example scripts (this value is set in the Makefile)
    # 'examples_dirs': '../../napari/examples',
    'gallery_dirs': 'gallery',  # path to where to save gallery generated output
    'filename_pattern': '/*.py',
    'ignore_pattern': 'README.rst|/*_.py',
    'default_thumb_file': Path(__file__).parent / '_static' / 'images' / 'logo.png',
    'plot_gallery': "'True'",  # https://github.com/sphinx-gallery/sphinx-gallery/pull/304/files
    'download_all_examples': False,
    'min_reported_time': 10,
    'only_warn_on_example_error': False,
    'abort_on_example_error': True,
    'image_scrapers': ("matplotlib", napari_scraper,),
    'reset_modules': (reset_napari,),
    'reference_url': {'napari': None},
    'within_subsection_order': ExampleTitleSortKey,
}

GOOGLE_CALENDAR_API_KEY = os.environ.get('GOOGLE_CALENDAR_API_KEY', '')


def add_google_calendar_secrets(app, docname, source):
    """Add google calendar api key to meeting schedule page.

    The source argument is a list whose single element is the contents of the
    source file. You can process the contents and replace this item to implement
    source-level transformations.
    """
    if docname == 'community/meeting_schedule':
        source[0] = source[0].replace('{API_KEY}', GOOGLE_CALENDAR_API_KEY)


class FilterSphinxWarnings(logging.Filter):
    """Filter 'duplicate object description' warnings.

    These warnings are a result of autosummary limitations when we have
    Attributes and Properties in a class sharing the same name.

    The warnings are not useful - they don't result in any missing documentation
    or rendering issues, so we can safely ignore them.

    """
    def __init__(self, app):
        self.app = app
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()

        filter_out = (
            "duplicate object description",
        )

        if msg.strip().startswith(filter_out):
            return False
        return True


def qt_docstrings(app, what, name, obj, options, lines):
    """Only show first line of Qt threading docstrings.

    Avoids syntax errors since the Qt threading docstrings are written in
    Markdown, and injected into rst docstring automatically.
    """
    ignore_list = ["WorkerBase", "FunctionWorker", "GeneratorWorker"]
    if any([f in name for f in ignore_list]):
        if len(lines) > 0:
            del lines[1:]


def setup(app):
    """Set up docs build.

    * Ignores .ipynb files to prevent sphinx from complaining about multiple
      files found for document when generating the gallery
    * Rewrites github anchors to be comparable
    * Adds google calendar api key to meetings schedule page
    * Filters out 'duplicate object description' Sphinx warnings
    * Cleans out Qt threading docstrings

    """
    app.registry.source_suffix.pop(".ipynb", None)
    app.connect('source-read', add_google_calendar_secrets)
    app.connect('linkcheck-process-uri', rewrite_github_anchor)
    app.connect('autodoc-process-docstring', qt_docstrings)
    logger = logging.getLogger("sphinx")

    warning_handler, *_ = [
        h for h in logger.handlers
        if isinstance(h, sphinx_logging.WarningStreamHandler)
    ]
    warning_handler.filters.insert(0, FilterSphinxWarnings(app))


def get_attributes(item, obj, modulename):
    """Filters attributes to be used in autosummary.

    Fixes import errors when documenting inherited attributes with autosummary.

    """
    module = import_module(modulename)
    if hasattr(module, "__all__") and obj not in module.__all__:
        return ""

    if hasattr(getattr(module, obj), item):
        return f"~{obj}.{item}"
    else:
        return ""


FILTERS["get_attributes"] = get_attributes

autosummary_ignore_module_all = False

linkcheck_anchors_ignore = [r'^!', r'L\d+-L\d+', r'r\d+', r'issuecomment-\d+']
linkcheck_ignore = [
    "https://napari.zulipchat.com/",
    "../_tags",
    "https://en.wikipedia.org/wiki/Napari#/media/File:Tabuaeran_Kiribati.jpg",
    "http://localhost:8000",
    "https://datadryad.org/stash/downloads/file_stream/182482",
    "https://github.com/napari/docs/issues/new/choose",
    "https://github.com/napari/napari/issues/new/choose",
    "https://github.com/napari/napari/issues/new",
    "https://napari-hub.org",
    "https://github.com/napari/napari/releases/latest",
    "https://onlinelibrary.wiley.com/doi/10.1002/col.20327",
]
linkcheck_allowed_redirects = {
    r"https://youtu\.be/.*": r"https://www\.youtube\.com/.*",
    r"https://github\.com/napari/napari/releases/download/.*": r"https://objects\.githubusercontent\.com/.*",
}


def rewrite_github_anchor(app, uri: str):
    """Rewrite anchor name of the hyperlink to github.com

    The hyperlink anchors in github.com are dynamically generated.  This rewrites
    them before checking and makes them comparable.
    """
    parsed = urlparse(uri)
    if parsed.hostname == "github.com" and parsed.fragment:
        for text in [
            "L",
            "readme",
            "pullrequestreview",
            "issuecomment",
            "issue",
        ]:
            if parsed.fragment.startswith(text):
                return None
        if re.match(r'r\d+', parsed.fragment):
            return None
        prefixed = parsed.fragment.startswith('user-content-')
        if not prefixed:
            fragment = f'user-content-{parsed.fragment}'
            return urlunparse(parsed._replace(fragment=fragment))
    return None
