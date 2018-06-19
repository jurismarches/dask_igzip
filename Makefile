tests:
	pytest --cov=dask_igzip --cov-config .coveragerc
quality:
	flake8 --max-line-length=100 **/*.py
distribute:
	[ -z $(ls dist/)  ] || rm dist/*
	python3 setup.py bdist
	python3 setup.py bdist_wheel
	twine upload -u jurismarches -s dist/*
