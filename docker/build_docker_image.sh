#!/bin/sh

cd ../src/dist
python create_dist.py latest-docker

cd ../../docker
cp -f ../bin/azure-apim-deployment-utils-latest-docker.zip azure-apim.zip

if [ ! -z "$docker_https_proxy" ]; then
    docker build -t donmartin76/azure-apim-deployment-utils --build-arg http_proxy=$docker_http_proxy --build-arg https_proxy=$docker_https_proxy .
else
    docker build -t donmartin76/azure-apim-deployment-utils .
fi

rm -f azure-apim.zip
