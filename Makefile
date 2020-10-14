default:
	python setup.py sdist
	python setup.py bdist_wheel --python-tag py22
	rm build/lib/with_.py
	python setup.py bdist_wheel --python-tag py25
	rm build/lib/with_.py
	python setup.py bdist_wheel --python-tag py26.py30
	rm build/lib/with_.py
	python setup.py bdist_wheel --python-tag py33

clean:
	rm -rf __pycache__ build *.egg-info dist
	rm -f *.py[oc] MANIFEST with_.py

test:
	python2.5 test.py
	python2.7 test.py
	python3 test.py
