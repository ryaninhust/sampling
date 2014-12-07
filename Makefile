all:
	rm -rf result
	mkdir result
	python algorithms.py
clean_pyc:
	find . -name "*.pyc" -exec rm -rf {} \; 



