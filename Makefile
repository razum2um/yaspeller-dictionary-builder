test:
		nosetests
autofix:
		find {src,tests} -iname '*.py' -exec autopep8 -i {} \;
lint:
		flake8 --max-line-length 120 --exclude .git,__pycache__,env
