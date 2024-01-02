# EduShort: AI-Powered Whiteboard Animation for Storytelling

![Continuous Integration](https://github.com/joesurf/edushort-api/workflows/Continuous%20Integration/badge.svg)
![Continuous Deployment](https://github.com/joesurf/edushort-api/workflows/Continuous%20Deployment/badge.svg)


## Overview
For content creators to automatically generate beautiful whiteboard animation for storytelling without the hassle of manually copy and pasting illustrations and recording voiceovers

### Features
[ ] For users to generate animations from script
[ ] For users to pay for tokens


### Common Commands
Build the images:
- docker-compose build

Run the containers:
- docker-compose up -d

Apply the migrations: 
- docker-compose exec web aerich migrate
- docker-compose exec web aerich upgrade
- heroku run aerich migrate --app edushort
- heroku run aerich upgrade --app edushort

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
