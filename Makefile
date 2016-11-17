init:
	pip install -r requirements.txt

install:
	python setup.py install

publish: test
	python setup.py sdist upload

test:
	clear
	rm -rf data
	git clone --depth=1 https://github.com/w4k2/data.git data
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=ece --nocapture
	rm -rf data

.PHONY: publish test
