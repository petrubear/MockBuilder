#!/bin/sh

# Importante: Configurar esta ruta!
# En linux cambiar sed -i '' por sed -i
OUTPUT_PATH=/opt/fbp/mocks_baninter/out/

TIMESTAMP=$(date +"%Y%m%d_%I%M%S")

function process_request {
    echo '[INFO] Input: '$1
    echo ''
    echo '[INFO] Processing request...'
    req_output_file=${OUTPUT_PATH}'request-'${TIMESTAMP}'.txt'

    if [ -f ${req_output_file} ] ; then
        rm ${req_output_file}
    fi

    awk '$0=="---------------------------" {p=1}; p; $0=="--------------------------------------" {p=0}' $1 | tr '\n' '#'  > ${req_output_file}
    if [ -f ${req_output_file} ] ; then
        sed -i '' 's/--------------------------------------#---------------------------#/\'$'\n/g' ${req_output_file}
        sed -i '' 's/---------------------------#//g' ${req_output_file}
        echo '[INFO] Output: '${req_output_file}
    else
       echo '[ERROR] File not Found: '${req_output_file}
       exit 1
    fi
}

function process_response {
    echo ''
    echo '[INFO] Processing response...'
    res_output_file=${OUTPUT_PATH}'response-'${TIMESTAMP}'.txt'

    if [ -f ${res_output_file} ] ; then
        rm ${res_output_file}
    fi

    awk '$0=="----------------------------" {p=1}; p; $0=="--------------------------------------" {p=0}' $1 | tr '\n' '#' > ${res_output_file}
    if [ -f ${res_output_file} ] ; then
        sed -i '' 's/--------------------------------------#----------------------------#/\'$'\n/g' ${res_output_file}
        sed -i '' 's/----------------------------#//g' ${res_output_file}
        echo '[INFO] Output: '${res_output_file}
    else
       echo '[ERROR] File not Found: '${res_output_file}
       exit 1
    fi
}

function execute_builder {
    echo ''
    echo '[INFO] Processing mocks...'
    python3 MockBuilder.py ${req_output_file} ${res_output_file}
}

function main {
    if [ -f $1 ]; then
        mkdir -p ${OUTPUT_PATH}
        process_request $1 || exit 0
        process_response $1 || exit 0
        execute_builder
    else
        echo 'Cannot Open File:' ${1}
        exit 0
    fi
}

# main entry point
main $1