init:
	pip install -r requirements.txt

install:
	python setup.py install

publish:
	python setup.py sdist upload
	
docset:
	pycco eec/*.py
#	git subtree push --prefix docs origin gh-pages

.PHONY: publish docset