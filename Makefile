# Minimal Makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = docs

.PHONY: help html clean

# Show help message
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build HTML into docs/ and add .nojekyll
html:
	@echo "Building HTML into $(BUILDDIR)/ ..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@echo "Creating .nojekyll in $(BUILDDIR)/ ..."
	@touch "$(BUILDDIR)/.nojekyll"

# Remove generated files
clean:
	@echo "Removing $(BUILDDIR)/ ..."
	@rm -rf "$(BUILDDIR)/"
