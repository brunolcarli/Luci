install:
	pip3 install -r luci/requirements/development.txt

run:
	python3 main.py run


repl_runner:
	pip3 install -r luci/requirements/common.txt
	python3 -m spacy download pt
	make run

train:
	python3 main.py train


no_free_lunch:
	python3 main.py no_free_lunch
