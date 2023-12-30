# Test-Driven Development with FastAPI and Docker

![Continuous Integration and Delivery](https://github.com/joesurf/toolfinder/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)


warm-springs-90557-4a73d66a2571

heroku addons:create heroku-postgresql:mini --app warm-springs-90557

registry.heroku.com/warm-springs-90557/web:latest

postgresql-rigid-45752

docker build -f project/Dockerfile.prod -t registry.heroku.com/warm-springs-90557/web ./project


docker run --name fastapi-tdd -e PORT=8765 -e DATABASE_URL=sqlite://sqlite.db -p 5003:8765 registry.heroku.com/warm-springs-90557/web:latest

docker push registry.heroku.com/warm-springs-90557/web:latest


heroku container:release web --app warm-springs-90557

https://warm-springs-90557.herokuapp.com/ping/



docker buildx build --platform linux/amd64 -f project/Dockerfile.prod -t registry.heroku.com/warm-springs-90557/web ./project


heroku run aerich upgrade --app warm-springs-90557


http --json POST https://warm-springs-90557-4a73d66a2571.herokuapp.com/summaries/ url=https://testdriven.io



--------------------


docker build -f project/Dockerfile.prod -t ghcr.io/joesurf/toolfinder/summarizer:latest ./project


docker login ghcr.io -u joesurf -p <token>


docker push ghcr.io/joesurf/toolfinder/summarizer:latest
 

git remote set-url origin https://joesurf:<token>@github.com/joesurf/toolfinder.git