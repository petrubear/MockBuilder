#!/usr/bin/env bash

# Importante: Configurar esta ruta!
IN_PATH=/opt/fbp/mocks_baninter/in/
FILE_EXTENSION=log

function parse_directory_files {
    for f in ${IN_PATH}*.${FILE_EXTENSION}; do
        if [ -f ${f} ]; then
            echo "********************************************************************************"
            # si prepare_log falla, detengo la ejecucion en el archivo que fallo
            sh prepare_log.sh ${f} || exit 0

            mv -f ${f} ${f}.done
            # pauso para evitar que se pisen los archivos
            # que pasa si no hago esto? T.T
            sleep 1
            echo "********************************************************************************"
         fi
    done
}

parse_directory_files