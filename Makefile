init:
	pip install -r requirements.txt

install:
	python setup.py install

publish: test
	python setup.py sdist upload

test:
	nosetests
	
docset:
	pycco eec/*.py
	git subtree push --prefix docs origin gh-pages

.PHONY: publish docset test