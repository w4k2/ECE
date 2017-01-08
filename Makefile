init: getData
	pip install -r requirements.txt

install:
	python setup.py install

publish: test
	python setup.py sdist upload

getData:
	rm -rf data
	git clone --depth=1 https://github.com/w4k2/data.git data

test:
	clear
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=ece --nocapture

.PHONY: publish test
