
install:
	@pip3 install -r requirements.txt

clean:
	@rm -rf src/__pycache__
	@rm -rf src/.mypy_cache
	@rm -rf src/models/__pycache__
	@rm -rf src/.ipynb_checkpoints
	@rm -rf .mypy_cache

check:
	@echo --------------------------
	@echo FLAKE8 is checking ....
	@flake8 src/main.py  --config .config/.flake8 || true
	@echo --------------------------
	@echo PYLINT is checking ....
	@pylint --rcfile .config/.pylintrc  src/*.py || true
	@echo --------------------------
	@echo MYPY is checking ....
	@mypy . --config-file .config/mypy.ini || true
	@echo --------------------------


lint:
	@isort src/*.py
	@yapf --style .config/.style.yapf -i src/*.py
#@black src/*.py --line-length 100 -t py36