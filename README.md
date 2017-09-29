# MockBuilder
### Idea Original de @bluewake

Configurar la variable **OUTPUT_PATH** en el archivo **prepare_log.sh**

```bash
output_dir=/Users/edison/Tmp/mock_test/out/
```

Configurar la variable **OUTPUT_PATH** en el archivo **mockbuilder.ini**

```bash
OUTPUTPATH=/Users/edison/Tmp/mock_test/out
```

Ejecutar el script prepare_log.sh con el log de salida de cxf como parámetro, este genera los request y response para wiremock

```bash
./prepare_log.sh cxf_log.log
```

Los archivos de salida de request deben copiarse en el directorio **mappings** y los archivos de salida de response en el directorio **__files** en wiremock



