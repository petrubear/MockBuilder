#!/bin/sh
# request parser
OUTPUT_PATH=/Users/edison/Tmp/mock_test/out/
TIMESTAMP=$(date +"%Y%m%d_%I%M%S")

mkdir -p ${OUTPUT_PATH}
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
fi

echo ''
echo '[INFO] Processing mocks...'
python3 MockBuilder.py ${req_output_file} ${res_output_file}
