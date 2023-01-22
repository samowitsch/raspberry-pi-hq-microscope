.PHONY: show-cron-processes
show-cron-processes: ## Show cron processes
	@echo "Show cron processes"
	ps -o pid,sess,cmd afx | egrep -A20 "( |/)cron( -f)?"

	@echo ""
	@echo "Search for python script. Stop process with 'pkill -s [pid]'"

# Self-Documenting Makefiles utilizing comments starting with
# double hash appended in same line where the rule is defined
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## prints this help information
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help