default:
	python setup.py sdist
	python setup.py bdist_wheel --python-tag py20
	rm build/lib/with_.py
	python setup.py bdist_wheel --python-tag py25
	rm build/lib/with_.py
	python setup.py bdist_wheel --python-tag py26.py3

clean:
	rm -rf __pycache__ build *.egg-info dist
	rm -f *.py[oc] MANIFEST with_.py
