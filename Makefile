# Makefile for pyPAHdb

TESTS  = pytest
SPHINX = sphinx-apidoc

all: wheel tests alldocs changelog

alldocs: htmldocs pdfdocs

sphinx:
	${SPHINX} -f -o docs/source/ pypahdb

htmldocs: sphinx
	make -C docs html

pdfdocs: sphinx
	make -C docs latexpdf

tests:
	${TESTS}

clean: docsclean

docsclean:
	make -C docs clean
	/bin/rm -rf docs/build
