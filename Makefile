init:
	pip install -r requirements.txt

install:
	python setup.py install

publish: test docset
	python setup.py sdist upload
	git subtree push --prefix docs origin gh-pages
	git add .
	git commit -m "Publication"
	git push

test:
	nosetests
	
docset:
	pycco eec/*.py

.PHONY: publish docset test