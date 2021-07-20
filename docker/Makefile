.PHONY: backup build clean run

build: Makefile
	# build vue.js app via npm and make
	# currently working with node v14.15.0 with npm v6.14.8 
	# make sure to use correct package.json
	rm -rf ../client/build
	cd ../client && npm install
	cd ../client && $(MAKE)
	# copy all source folders to this folder to build docker image
	rm -rf client scripts server ntg_common
	mkdir client
	mkdir scripts	
	cp -a ../server ../ntg_common .
	cp -a ../client/build/* ./client
	cp -a ../scripts/cceh/* ./scripts
	# we need two dockerfiles, one for the db and one for the server
	docker build -f Dockerfile.db --tag=intf/ntg-db-server  .
	docker build -f Dockerfile    --tag=intf/ntg-app-server .

# this command only works on a production server with a fully functional database
backup:
	mkdir -p /tmp/backup
	pg_dump --format custom mark_ph31 -n ntg -T "ntg.original_*" -T "ntg.tmp_*" \
			--exclude-table-data="ntg.notes*" > /tmp/backup/mark_ph31.dump

run: 
	sudo docker-compose up

stop: 
	sudo docker-compose stop

cbgm: build
	docker-compose run ntg-app-server cbgm

dbshell:
	sudo docker exec -i -t docker_ntg-db-server_1 /bin/bash

ntvmrimport:
	python ../scripts/python/ntvmrimport.py


# TODO integrate in gitlab registry of wwu.it
# push:
# 	cat ~/.dockerhubpass | docker login --username marcelloperathoner --password-stdin
# 	docker push cceh/ntg-app-server:latest
# 	docker push cceh/ntg-db-server:latest
# 	docker logout

clean:
	docker container stop $$(docker container ls -a -q) || true
	docker container rm   $$(docker container ls -a -q) || true
	docker network prune -f || true
	docker rmi -f $$(docker images --filter dangling=true -qa) || true
	docker volume rm $$(docker volume ls --filter dangling=true -q) || true
	docker rmi -f $$(docker images -qa) || true

clean-volume:
	sudo docker-compose down --volumes
