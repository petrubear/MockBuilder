#!/usr/bin/env bash
IN_PATH=/opt/fbp/mocks_baninter/in/
FILE_EXTENSION=log

for f in ${IN_PATH}*.${FILE_EXTENSION}; do
    sh prepare_log.sh ${f} || exit 0
    mv -f ${f} ${f}.done
#    pauso para evitar que se pisen los archivos?? deberia hacer esto??
    sleep 1
    echo "********************************************************************************"
done