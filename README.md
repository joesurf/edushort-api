# ToolFinder: AI-Powered Toolbox for Entrepreneurs

![Continuous Integration](https://github.com/joesurf/toolfinder/workflows/Continuous%20Integration/badge.svg)
![Continuous Deployment](https://github.com/joesurf/toolfinder/workflows/Continuous%20Deployment/badge.svg)


## Overview
For entrepreneurs to find the best tools to solve their problems on a daily basis so that they can focus on business progress, rather than operational or technical work.

Focus on scaling and automation tools, at least the angle.

### Features
- [] Users are able to input their problem or challenges
- [] Users have the option to structure their input for better results
- [] Users receive a structured response on possible tools, with description, ranked and with comparisons (users, costs, pros and cons) and guides
- [] Users have to view advertisements or subscribe to use the tool
- [] Users can view content on how people used a combination of tools to build businesses


### Common Commands
Build the images:
- docker-compose build

Run the containers:
- docker-compose up -d

Apply the migrations: 
- docker-compose exec web aerich migrate
- docker-compose exec web aerich upgrade


Run the tests:
- docker-compose exec web python -m pytest

Run the tests with coverage:
- docker-compose exec web python -m pytest --cov="."

Lint:
- docker-compose exec web flake8 .

Run Black and isort with check options:
- docker-compose exec web black . --check
- docker-compose exec web isort . --check-only

Make code changes with Black and isort:
- docker-compose exec web black .
- docker-compose exec web isort .

### Other Commands

To stop the containers:
- docker-compose stop

To bring down the containers:
- docker-compose down

Want to force a build?
- docker-compose build --no-cache

Remove images:
- docker rmi -(docker images -q)

### Postgres
Want to access the database via psql?
- docker-compose exec web-db psql -U postgres

Then, you can connect to the database and run SQL queries. For example:
- \c web_dev
- select * from textsummary;


### Tests
Test API Route
http --json POST <API Route> <key=value> ...
