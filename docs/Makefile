# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = nornir
SOURCEDIR     = .
BUILDDIR      = _build

OC_PYANG_PLUGINS_DIR="/src/oc-pyang/openconfig_pyang/plugins"

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

yang-docs:
	pyang \
		--plugindir $(OC_PYANG_PLUGINS_DIR) \
		-f docs \
		--path models \
		--doc-format rst \
		--strip-ns \
		../ntc_rosetta_conf/yang/ietf-yang-library.yang > yang/ietf-yang-library.rst
	pyang \
		--plugindir $(OC_PYANG_PLUGINS_DIR) \
		-f docs \
		--path models \
		--doc-format rst \
		--strip-ns \
		../ntc_rosetta_conf/yang/ntc-rosetta-conf.yang > yang/ntc-rosetta-conf.rst

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	cp ../CHANGELOG.rst .
	cp ../CONTRIBUTING.rst .
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
