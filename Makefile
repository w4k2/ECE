init: getData
	pip install -r requirements.txt

install:
	python setup.py install

publish: test
	python setup.py sdist upload

getData:
	if [ ! -d "data" ]; then git clone https://github.com/w4k2/data.git; rm -rf data/.git; fi

test: getData
	clear
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=ece --nocapture

.PHONY: publish test
