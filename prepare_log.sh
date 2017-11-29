#!/bin/sh

# Importante: Configurar esta ruta!
# En linux cambiar sed -i '' por sed -i
OUTPUT_PATH=/opt/fbp/tmp/out/

TIMESTAMP=$(date +"%Y%m%d_%I%M%S")

function process_request {
    echo '[INFO] Input: '$1
    echo ''
    echo '[INFO] Processing request...'
    req_output_file=${OUTPUT_PATH}'request-'${TIMESTAMP}'.txt'

    if [ -f ${req_output_file} ] ; then
        rm ${req_output_file}
    fi

    awk '$0 ~ ".*REQ_OUT" {p=1}; p; $0 ~ "Payload:" {p=0}' $1 |  \
        sed -e 's/    //g' | \
        awk '{while(match($0, /.*REQ_OUT.*/) > 0){sub(/.*REQ_OUT.*/, "ID: " ++c)}};1' | \
        tr '\n' '#' | \
        sed -e 's/ID:/\'$'\nID:/g' > ${req_output_file}
    echo '[INFO] Output: '${req_output_file}

}

function process_response {
    echo ''
    echo '[INFO] Processing response...'
    res_output_file=${OUTPUT_PATH}'response-'${TIMESTAMP}'.txt'

    if [ -f ${res_output_file} ] ; then
        rm ${res_output_file}
    fi

    awk '$0 ~ ".*RESP_IN" {p=1}; p; $0 ~ "Payload:" {p=0}' $1 |  \
        sed -e 's/    //g' | \
        awk '{while(match($0, /.*RESP_IN.*/) > 0){sub(/.*RESP_IN.*/, "ID: " ++c)}};1' | \
        tr '\n' '#' | \
        sed -e 's/ID:/\'$'\nID:/g' > ${res_output_file}
    echo '[INFO] Output: '${res_output_file}
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