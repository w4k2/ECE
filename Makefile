init:
	pip install -r requirements.txt

publish:
	pycco eec/*.py
	python setup.py sdist upload
	git subtree push --prefix docs origin gh-pages

.PHONY: publish