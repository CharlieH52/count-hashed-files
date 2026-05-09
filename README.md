# Certificador de archivos
Analiza recursivamente los archivos en la ruta especificada para generar una huella hash mediante el algoritmo **SHA256** y crea un registro completo de los archivos detectados con su respectiva marca de tiempo de lectura.

Esta aplicación pretende garantizar la integridad de los archivos analizados para su posterior revisión por el órgano auditor que solicite este proceso mediante el mismo procedimiento.

> [!IMPORTANT]  
> Normalmente se realizan estos análisis en ***dispositivos extraíbles***, memorias USB, unidades de CD y DVD, etc. Pueden existir **discrepancias** en las referencias de **espacio utilizado** y **disponible**, pues depende de que **Windows** considere correctamente el espacio ocupado por los clústeres de la unidad, particiones, archivos ocultos de la unidad, etc.
>  
> También se han encontrado discrepancias en el conteo cuando los nombres de los archivos tienen problemas de longitud o caracteres fuera de la codificación **UTF-8**.

> [!NOTE]  
> Esto ***NO*** significa que el análisis de la aplicación sea incorrecto, simplemente puede variar según los criterios tomados por las ***Propiedades de la carpeta*** en **Windows** y este software...