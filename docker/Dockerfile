FROM alpine:3.3

RUN apk --update add build-base libffi-dev openssl-dev python-dev py-pip git \ 
    && pip install pyopenssl \
    && pip install gitpython \
    && pip install requests \
    && apk del build-base libffi-dev openssl-dev \
    && apk add openssl

RUN cd /root \
    && wget https://github.com/Haufe-Lexware/azure-apim-deployment-utils/releases/download/v0.1/azure-apim-deployment-utils-v0.1.zip \
    && unzip azure-apim-deployment-utils-v0.1.zip

