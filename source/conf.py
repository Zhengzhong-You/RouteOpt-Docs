from __future__ import annotations

import datetime
import os
import sys

# -- Project information -----------------------------------------------------
sys.path.insert(0, os.path.abspath("../../"))

now = datetime.date.today()

project = "RouteOpt"
copyright = "2025, Zhengzhong (Ricky) You"
author = "Zhengzhong (Ricky) You"
repo_url = "https://github.com/Zhengzhong-You/RouteOpt/"

# -- API documentation -------------------------------------------------------
autoclass_content = "class"
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autodoc_preserve_defaults = True

# -- numpydoc ----------------------------------------------------------------
numpydoc_xref_param_type = True
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = False
napoleon_include_special_with_doc = True

# -- nbsphinx ----------------------------------------------------------------
skip_notebooks = os.getenv("SKIP_NOTEBOOKS", False)
nbsphinx_execute = "never" if skip_notebooks else "always"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_immaterial",
    "nbsphinx",
    "numpydoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinxcontrib.bibtex",
]

exclude_patterns = ["_build", "**.ipynb_checkpoints"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

add_module_names = False
python_use_unqualified_type_names = True

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_immaterial"
html_static_path = ["_static"]
html_baseurl = "https://zhengzhong-you.github.io/RouteOpt-Docs/"

html_theme_options = {
    "site_url": "https://zhengzhong-you.github.io/RouteOpt-Docs/",
    "repo_url": "https://github.com/Zhengzhong-You/RouteOpt",
    "repo_name": "RouteOpt",
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "features": [
        "navigation.expand",
        "navigation.top",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "primary": "green",
            "accent": "blue",
            "scheme": "default",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "primary": "green",
            "accent": "blue",
            "scheme": "slate",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "version_dropdown": False,
}

python_resolve_unqualified_typing = True
python_transform_type_annotations_pep585 = True
python_transform_type_annotations_pep604 = True
object_description_options = [
    ("py:.*", dict(include_fields_in_toc=False, include_rubrics_in_toc=False)),
    ("py:attribute", dict(include_in_toc=False)),
    ("py:parameter", dict(include_in_toc=False)),
]

# -- Options for EPUB output -------------------------------------------------
epub_show_urls = "footnote"

bibtex_bibfiles = ["all.bib"]
bibtex_reference_style = "author_year"


# -- Custom CSS for Logo Size -------------------------------------------------
def setup(app):
    app.add_css_file("custom.css")
