docker_build:
	docker build -t vespapp/vespapp-web .
docker_push:
	docker push vespapp/vespapp-web
devel:
	docker-compose run --rm --service-ports dev
