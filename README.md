# MockBuilder

Configurar la variable **output_dir** en el archivo **prepare_log.sh**

```bash
output_dir=/Users/edison/Tmp/mock_test/out/
```

Configurar la variable **OUTPUTPATH** en el archivo **mockbuilder.db**

```bash
OUTPUTPATH=/Users/edison/Tmp/mock_test/out
```

Ejecutar el script prepare_log.sh con el log de salida de cxf como parámetro

```bash
./prepare_log.sh cxf_log.log
```

Invocar el programa MockBuilder.py con los archivos de salida del comando anterior como parámetro

```bash
python MockBuilder.py request-20170928_101035.txt response-20170928_101035.txt
```


