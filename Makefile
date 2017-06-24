init: getData
	pip install -r requirements.txt

install:
	python setup.py install

publish: test
	python setup.py sdist upload

test:
	clear
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=ece --nocapture

.PHONY: publish test
