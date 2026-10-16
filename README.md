# LakeHouse System

# Descripcion

El documento proporciona una visión detallada de la arquitectura y los servicios utilizados en Google Cloud Platform para un sistema de análisis de datos de mediciones de vibraciones en puentes. Se incluye un diagrama arquitectónico que ilustra la configuración general del sistema, destacando los servicios clave como Cloud Storage para el almacenamiento de datos crudos y procesados, Dataproc para el procesamiento y transformación de datos, y BigQuery para consultas analíticas ad-hoc. La tabla asociada describe específicamente cada servicio utilizado, su componente correspondiente y el rol que desempeña en la arquitectura.

# Servicios usados y arquitectura general en Google Cloud Platform

A continuacion, la figura uno (1) muestra los servicios usados y como se ve plasmada la arquitectura general del sistema en Google Cloud Platform; la tabla uno (1) ahonda en la explicacion de los diferentes servicios y su proposito dentro de la arquitectura mostrada.

**Figura 1**

*Diagrama de la arquitectura del sistema en Google Cloud Platform.*

![dpLakeHouseWorkflow-architectural-diagram.png](https://dev.azure.com/kbenjumeao/5098febc-21d6-4123-8ec2-4eb6bc270093/_apis/git/repositories/451c328b-a54d-4381-a890-9d33463552ce/items?path=/docs/img/dpLakeHouseWorkflow-architectural-diagram.png&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=feat/spuertaf&resolveLfs=true&%24format=octetStream&api-version=5.0)

**Tabla 1**

*Servicios de Google Cloud Platform usados y proposito de los mismos.*

| Nombre del servicio | Nombre del componente | Rol que desempeña |
| --- | --- | --- |
| Cloud Storage | sif-med-lakehouse-raw-data-dev | Bucket que se encarga de almacenar los datos crudos que provienen de los archivos CSV resultantes de las mediciones de las vibraciones en los puente. |
| Cloud Storage | sif-med-lakehouse-trusted-data-dev | Bucket que se encarga de almacenar la tabla de delta y los datos procesados y transformados.  |
| Dataproc | dp_lakehouse_workflow_dev | Servicio encargado de consumir la data cruda presente en el Bucket “sif-med-lakehouse-raw-data-dev”, procesarla, hallar la transformada inversa de fourier para los registros y almacenarla en el Bucket “sif-med-lakehouse-trusted-data-dev”. |
| BigQuery | trusted_mobile_app_external_tables | Servicio usado para las consultas analiticas ad-hoc de la informacion previamente procesada almacenada en el bucket “sif-med-lakehouse-trusted-data-dev”. |

# Contrato de datos

El contrato de datos presente dentro de la carpeta **`docs/contracts`** del presente repositorio, contiene el detalle de los datos almacenados en cada uno de los buckets y BigQuery, los procesos de transformacion por los cuales pasan los datos, reglas de calidad evaluadas a los mismos e informacion adicional acerca del servicio de Dataproc usado para el procesamiento de los datos.

# Despliegue de la aplicacion

Dado el caso de que se desee realizar un nuevo de despliegue de la aplicacion se deberan de seguir los siguiente pasos.

1. Clonar el repositorio donde se encuentra disponible el codigo.
    
    ```bash
    git clone https://kbenjumeao@dev.azure.com/kbenjumeao/Proyecto%20integrador%202/_git/mobileApplicationBack
    ```
    
2. Posicionarse en la carpeta `/deploy` del proyecto.
    
    ```bash
    cd mobileApplicationBack/ && cd deploy/
    ```
    
3. Instalar y ejecutar el comando make.
    
    ```bash
    sudo apt update && sudo apt install build-essential && make
    ```
    

El comando make se encargara de crear todas los buckets e incializar los servicios expuestos, ademas de empaquetar y subir el codigo a Google Cloud Platform.