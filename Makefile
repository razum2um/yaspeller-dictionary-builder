test:
		nosetests

lintfix:
		find {src,tests} -iname '*.py' -exec autopep8 -i {} \;