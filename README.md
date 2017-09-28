# MockBuilder

Configurar la variable **output_dir** en el archivo **prepare_log.sh**

```bash
output_dir=/Users/edison/Tmp/mock_test/out/
```

Configurar la variable **OUTPUTPATH** en el archivo **mockbuilder.db**

```bash
OUTPUTPATH=/Users/edison/Tmp/mock_test/out
```

Ejecutar el script prepare_log.sh con el log de salida de cxf como parámetro, este genera los request y response para wiremock

```bash
./prepare_log.sh cxf_log.log
```

Los archivos de salida de request deben copiarse en el directorio **mappings** y los archivos de salida de response en el directorio **__files**

Alternativamente, se puede invocar el programa MockBuilder.py con los archivos de salida de request y response que genera **prepare_log.sh**

```bash
python3 MockBuilder.py request-20170928_101035.txt response-20170928_101035.txt
```


