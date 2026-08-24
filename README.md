# Certificador de archivos
Analiza la ruta especificada e itera sobre los archivos contenidos para generar un registro de los archivos con su respectiva huella hash hecha con SHA256. Integra opciones como conteo total de archivos analizados, espacio total utilizado por estos, listado de extensiones y conteo por extensión, además de proveer datos sobre la unidad analizada (capacidad total, espacio ocupado por los archivos y espacio libre en la unidad).

## Detrás del proyecto
### Contexto
Anteriormente un **órgano auditor** solía solicitar archivos expedidos por la organización para la que he trabajado, archivos que se envían aún en unidades extraíbles como USB, CD o DVD.

Estos archivos se solían enviar sin más. En la actualidad, este y otros órganos encargados de realizar auditorías han comenzado a solicitar respaldos digitales sobre el contenido de las unidades entregadas. Es por ello que se han comenzado a utilizar las certificaciones mediante huella hash; en nuestro caso particular se solicitan mediante el algoritmo `SHA256` junto con los datos mencionados en el primer párrafo. Esto con la finalidad de asegurar y mantener la integridad de la información que se entrega desde la organización.

### Justificación
El proceso planteado por el órgano en turno consistía en una serie de pasos sistemáticos y varias aplicaciones libres de por medio muy sencillas. Decidí crear una herramienta centralizada que realizara exactamente lo que se solicita con una interfaz sencilla y muy directa, para así eficientar todo el proceso, el cual cada día es más solicitado en mi área de Sistemas.

### ¿Por qué SHA256?
Actualmente es el requisito principal solicitado por el organo auditor respecto a la generación de la huella hash.

### Motivación
Realicé una investigación respecto al método utilizado para esta actividad dentro de los documentos proporcionados por el órgano auditor y me di cuenta de que, en general, era una actividad sistemática muy sencilla respecto a los requisitos solicitados, por lo que consideré que era un reto muy sencillo de trabajar con Python. Además, considerando la demanda creciente de estas solicitudes, encontré óptimo crearla no solo para mi uso en el área, sino para el uso común de las áreas que también lo requieran.

Es posible implementarla para otras organizaciones que tengan esta misma necesidad e incluso implementar otros algoritmos para la generación de la huella hash.

## Información técnica
Este proyecto consiste en una aplicación de escritorio con interfaz gráfica para centralizar los datos solicitados con un flujo de trabajo sencillo.

<div align="center" style="width:100%">
    <picture>
        <source srcset="./docs/screenshot-main_view.png" media="(max-width: 600px)"/>
        <img style="max-width: 600px;" src="./docs/screenshot-main_view.png" alt="Captura de pantalla de la vista previa de la interfaz al iniciar el programa."/>
    </picture>
</div>

<br/>

### Tecnologías utilizadas
- Python, lenguaje utilizado.
- Flet, librería de interfaces modernas.
- WMI, librería utilizada para obtener objetos específicos de Windows.
- PyInstaller, librería para crear el ejecutable empaquetado.

### Características
- Generación de hashes `SHA256`.
- Conteo total de archivos.
- Estadísticas por extensión.
- Cálculo de espacio utilizado.
- Cálculo del espacio disponible.
- Interfaz gráfica sencilla.
- Generación automatizada de reportes.

#### Justificación técnica
Decidí utilizar Python, pues para la primera versión rápida de prueba de concepto realicé varias certificaciones con algunas líneas de código y una interfaz CLI.

Una vez terminadas las funciones principales implementé Flet para centralizar la información y volver más accesible la aplicación.

Para la entrega de reportes utilicé un formato de salida en JSON, pues esto puede ser extendible para otro tipo de lectores automatizados, implementación de APIs y facilita su importación en programas compatibles con este formato.

Por último, PyInstaller es esencial para portabilizar el programa, pues es necesario que sea más sencillo de implementar para el personal externo al área de Sistemas.

<div align="center" style="width:100%">
    <picture>
        <source srcset="./docs/screenshot-output-example.png" media="(max-width: 600px)"/>
        <img style="max-width: 600px;" src="./docs/screenshot-output-example.png" alt="Captura de pantalla de la salida resultante de una certificacion."/>
    </picture>
</div>

<br/>

Por ultimo Pyinstaller es esencial para portabilizar el programa, pues es necesario que sea más sencillo de implementar para el personal externo al área de Sistemas.

## Flujo de trabajo

### Instalación
Preparar entorno virtual:
> `python -m venv venv`

Instalación de dependencias:
> `pip install -r requirements.txt`

Ejecución:
> `python .\main.py`

Compilar programa:
> `python .\build.py`

> [!NOTE]  
> Es posible cambiar algunos parametros dentro de `build.py` para ajustar la compilación a las necesidades que requieras.

### Resultado obtenido
El siguiente es un ejemplo del resultado esperado:

<div align="center" style="width:100%">
    <source srcset="./docs/screenshot-output-view-example.png" media="(max-width: 600px)"/>
    <img style="max-width: 600px;" src="./docs/screenshot-output-view-example.png" alt="Captura de pantalla del resultado obtenido en la interfaz de la aplicación."/>
</div>

<br/>

> [!NOTE]  
> Puede existir el caso de que el dispositivo analizado no provea información respecto a su capacidad o propiedades fisicas, como en el siguiente caso.  

<div align="center" style="width:100%">
    <picture>
        <source srcset="./docs/screenshot-cd_case.png" media="(max-width: 600px)"/>
        <img style="max-width: 600px;" src="./docs/screenshot-cd_case.png" alt="Captura de pantalla del resultado obtenido de un CD antiguo de Windows NT Original."/>
    </picture>
</div>

<br/>

> Eso sucede principalmente en unidades de CD o DVD, pues dependiendo del fabricante, la antigüedad, entre otros factores como codificación de los archivos y formato de la unidad.

### Limitaciones conocidas
- El tiempo que demora el análisis depende principalmente del tamaño de la muestra y la velocidad de lectura de la unidad.
- Los archivos bloqueados por el sistema podrían omitirse.
- Archivos y rutas con caracteres especiales o longitudes anormales en los nombres podrían omitirse.
- Actualmente solo está disponible el algoritmo `SHA256`.

<table style="width:100%; border:none;">
  <tr>
    <td align="center">
        <picture>
            <source srcset="./docs/screenshot-output-view-test.png" media="(max-width: 400px)"/>
            <img style="max-width: 400px;" src="./docs/screenshot-output-view-test.png" alt="Captura de pantalla que contrasta el resultado de la aplicación con el mostrado por Windows."/>
        </picture>
    </td>
    <td align="center">
        <picture>
            <source srcset="./docs/windows-info.png" media="(max-width: 240px)"/>
            <img style="max-width: 240px;" src="./docs/screenshot-windows-info.png" alt="Captura de pantalla del las propiedades mostradas por Windows."/>
        </picture>
    </td>
  </tr>
</table>

> [!CAUTION]  
> Puede haber una ligera discrepancia en el espacio ocupado mostrado por la aplicación y el marcado por las propiedades de Windows, ya que influyen factores como los mencionados en las limitaciones conocidas.