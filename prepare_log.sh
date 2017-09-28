#!/bin/sh
# request parser
output_dir=/Users/edison/Tmp/mock_test/out/
timestamp=$(date +"%Y%m%d_%I%M%S")
req_output_file=${output_dir}'request-'${timestamp}'.txt'

mkdir -p ${output_dir}
echo 'Input: '$1

echo 'Processing request...'
if [ -f ${req_output_file} ] ; then
    rm ${req_output_file}
fi

awk '$0=="---------------------------" {p=1}; p; $0=="--------------------------------------" {p=0}' $1 | tr '\n' '#'  > ${req_output_file}
if [ -f ${req_output_file} ] ; then
    sed -i '' 's/--------------------------------------#---------------------------#/\'$'\n/g' ${req_output_file}
    sed -i '' 's/---------------------------#//g' ${req_output_file}
    echo 'Output: '${req_output_file}
else
   echo 'File not Found: '${req_output_file}
   exit 1
fi

echo 'Processing response...'
res_output_file=${output_dir}'response-'${timestamp}'.txt'
echo 'Input: '$1

if [ -f ${res_output_file} ] ; then
    rm ${res_output_file}
fi

awk '$0=="----------------------------" {p=1}; p; $0=="--------------------------------------" {p=0}' $1 | tr '\n' '#' > ${res_output_file}
if [ -f ${res_output_file} ] ; then
    sed -i '' 's/--------------------------------------#----------------------------#/\'$'\n/g' ${res_output_file}
    sed -i '' 's/----------------------------#//g' ${res_output_file}
    echo 'Output: '${res_output_file}
else
   echo 'File not Found: '${res_output_file}
fi

