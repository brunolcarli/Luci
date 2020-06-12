install:
	pip3 install -r luci/requirements/development.txt

run:
	python3 main.py


repl_runner:
	pip3 install -r luci/requirements/common.txt
	make run
