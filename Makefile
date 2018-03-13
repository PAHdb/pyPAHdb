# Makefile for pyPAHdb

TESTS  = green
SPHINX = sphinx-apidoc

all: wheel tests alldocs changelog

alldocs: htmldocs pdfdocs

sphinx:
	${SPHINX} -f -o docs/source/ pypahdb

htmldocs: sphinx
	make -C docs html
	/bin/rm -rf docs/html
	/bin/mv -f docs/build/html docs/

pdfdocs: sphinx
	make -C docs latexpdf
	/bin/mv -f docs/build/latex/pyPAHdb.pdf docs/pyPAHdb_`/bin/cat VERSION`.pdf

tests:
	${TESTS} pypahdb

wheel:
	python setup.py bdist_wheel

changelog:
	git log --decorate --color >> CHANGELOG.md

clean: docsclean

docsclean:
	make -C docs clean
	/bin/rm -rf docs/build
	/bin/rm -rf docs/html
	/bin/rm -f docs/manual.pdf
