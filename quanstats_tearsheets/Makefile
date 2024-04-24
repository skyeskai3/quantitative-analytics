run:
	docker-compose up
build:
	docker-compose up --build
stop:
	docker-compose stop
down:
	docker-compose down
test:
	curl -X PUT -H 'aum:10000' -H 'id:1' -H 'active:active' --data-binary @test.csv http://0.0.0.0:3778/week
helm-install:
	helm install tearsheets ./helm
