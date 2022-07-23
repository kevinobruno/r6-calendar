.PHONY: build
build:
	docker run --rm --volume=$(shell pwd):/lambda-build -w=/lambda-build lambci/lambda:build-python3.8 pip install -r requirements.txt --target ./python
	zip -r r6-calendar-layer.zip python/

	zip -r r6-calendar-package.zip app
	zip -g r6-calendar-package.zip lambda_function.py
