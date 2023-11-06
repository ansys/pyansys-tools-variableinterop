# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j auto
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
# TODO: these lines of code should be removed once the feature branch is merged
	for /f %%i in ('pip freeze ^| findstr /c:"sphinx-autoapi @ git+https://github.com/ansys/sphinx-autoapi"') do set is_custom_sphinx_autoapi_installed=%%i
	if NOT "%is_custom_sphinx_autoapi_installed%" == "sphinx-autoapi" (
		pip uninstall --yes sphinx-autoapi
		pip install "sphinx-autoapi @ git+https://github.com/ansys/sphinx-autoapi@feat/single-page-stable")
# TODO: these lines of code should be removed once the feature branch is merged
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*
	find . -type d -name "_autosummary" -exec rm -rf {} +

pdf:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(BUILDDIR)/latex/pyansys-tools-variableinterop-Documentation-*.pdf && echo pdf exists) || exit 1
