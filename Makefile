install:
	pip3 install -r luci/requirements/development.txt

run:
	python3 main.py run


repl_runner:
	pip3 install -r luci/requirements/common.txt
	make run

train:
	python3 main.py train


no_free_lunch:
	python3 main.py no_free_lunch
