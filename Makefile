install:
	pip3 install --no-binary :all -r luci/requirements/development.txt
	python3 -m spacy download pt

run:
	python3 main.py


repl_runner:
	pip3 install -r luci/requirements/common.txt
	python3 -m spacy download pt
	make run

train:
	python3 manage.py train


no_free_lunch:
	python3 manage.py no_free_lunch


test:
	python3 -m unittest discover

help:
	python3 manage.py help
