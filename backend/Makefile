help:
		@printf "Available targets:\n\n"
		@awk '/^[a-zA-Z\-\_0-9%:\\]+/ { \
          helpMessage = match(lastLine, /^## (.*)/); \
          if (helpMessage) { \
            helpCommand = $$1; \
            helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
      gsub("\\\\", "", helpCommand); \
      gsub(":+$$", "", helpCommand); \
            printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
          } \
        } \
        { lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
		@printf "\n"



## create, migrate, & seed dev database
db-build: db-create db-migrate db-seed

## create dev database
db-create:
	createdb method_dev -O method_interview

## delete dev database
db-drop:
	dropdb method_dev

## migrate dev database
db-migrate:
	cd db/ && \
		alembic upgrade head


## setup clean dev database
db-setup: db-drop db-create db-migrate

run-dev:
	honcho -f Procfile.local start

