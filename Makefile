.PHONY: integration-test
integration-test:
	docker-compose -f integration-test/docker-compose.yaml up  -d --no-deps --build
	docker-compose -f integration-test/docker-compose.yaml up  --abort-on-container-exit