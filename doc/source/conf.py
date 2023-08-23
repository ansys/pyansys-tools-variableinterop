"""Sphinx documentation configuration file."""
from datetime import datetime
import os

from ansys_sphinx_theme import ansys_favicon, get_version_match, pyansys_logo_black

from ansys.tools.variableinterop import __version__

# Project information
project = "pyansys-tools-variableinterop"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "Ansys Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "<DEFAULT_CNAME>")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_logo = pyansys_logo_black
html_favicon = ansys_favicon
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyAnsys Tools Variable Interop"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pyansys-tools-variableinterop",
    "check_switcher": False,
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/ansys/pyansys-tools-variableinterop/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "ansys",
    "github_repo": "pyansys-tools-variableinterop",
    "github_version": "main",
    "doc_path": "doc/source",
}

# Sphinx extensions
extensions = [
    "notfound.extension",  # for the not found page.
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "anyio": ("https://anyio.readthedocs.io/en/stable/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_xref_param_type = True
autosectionlabel_prefix_document = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned
}

var_value_regex_prefix = "ansys\.tools\.variableinterop\..*Value\."
numpydoc_validation_exclude = {
    # Ignore methods inherited from numpy with doc errors
    var_value_regex_prefix + "astype",
    var_value_regex_prefix + "copy",
    var_value_regex_prefix + "dot",
    var_value_regex_prefix + "tobytes",
    var_value_regex_prefix + "tostring",
    var_value_regex_prefix + "T",
    var_value_regex_prefix + "nbytes",
    var_value_regex_prefix + "real",
    var_value_regex_prefix + "shape",
    var_value_regex_prefix + "strides",
    var_value_regex_prefix + "conj",
    var_value_regex_prefix + "denominator",
    var_value_regex_prefix + "numerator",
    "numpy\._typing\._array_like\.SupportsArray",
    "numpy\._typing\._nested_sequence\._NestedSequence",
    # Ignore importlib missing docstrings
    "ansys\.tools\.variableinterop\.importlib_metadata\..*",
}

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "links.rst",
]

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()
