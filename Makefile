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
	rm -rf __pycache__ build *.egg-info dist test
	rm -f *.py[oc] MANIFEST with_.py

test:
	python2.5 test.py
	python2.7 test.py
	python3 test.py
	# This is less painful than the node_bridge.js approach,
	# since Brython's import machinery doesn't work in Node.
	rm -rf test
	mkdir test
	cp test.py with_3_3.py with_brython.py with_skulpt_3.py test/
	cd test && brython-cli make_package test
	cd test && brython-cli install
	cp test_brython.html test/index.html
	cd test && brython-cli start_server
