default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	
.PHONY: setup
setup: # Install dependencies, setup pre-commit hooks
	./setup.sh

.PHONY: test
test: # Run unit tests and code coverage test
	./test.sh

.PHONY: lint
lint: # Check style error and static type
	./lint.sh