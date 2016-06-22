init:
	pip install -r requirements.txt

install:
	python setup.py install

publish:
	pycco eec/*.py
	python setup.py sdist upload
	git subtree push --prefix docs origin gh-pages

.PHONY: publish