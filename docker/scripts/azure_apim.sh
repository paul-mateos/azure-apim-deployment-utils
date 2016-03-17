#!/bin/sh

#echo "Command: $1"
#echo "Argument: $2"

cd /azure-apim-deployment-utils

if [ "$1" = 'update' ] || [ "$1" = 'update_extract' ]; then
    echo "========================"
    echo " UPDATING APIM INSTANCE"
    echo "========================"
    python apim_update.py /apim
fi

if [ "$1" = 'extract' ] || [ "$1" = 'update_extract' ]; then
    echo "=========================="
    echo " EXTRACTING APIM INSTANCE"
    echo "=========================="
    if [ ! -z "$2" ]; then
        python apim_extract.py /apim /apim/$2
    else
        python apim_extract.py /apim /apim/apim_extract.zip
    fi
fi

if [ "$1" = 'deploy' ]; then
    echo "============================"
    echo " DEPLOYING TO APIM INSTANCE"
    echo "============================"
    if [ ! -z "$2" ]; then
        python apim_deploy.py /apim/$2
    else
        echo "Missing mandatory argument: <source zip>"
    fi
fi

if [ "$1" = 'extract_properties' ]; then
    echo "=========================================="
    echo " EXTRACTING PROPERTIES FROM APIM INSTANCE"
    echo "=========================================="
    python apim_extract_properties.py /apim
fi

if [ "$1" = 'pkcs12_fingerprint' ]; then
    if [ ! -z "$2" ]; then
        python apim_openssl.py $2 $3 /apim
    else
        echo "Usage:"
        echo "  <docker> pkcs12_fingerprint <pfx_file> <password>"
    fi
fi
