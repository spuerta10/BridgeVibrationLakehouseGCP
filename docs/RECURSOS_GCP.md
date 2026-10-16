# Nomenclatura recursos GCP

## Nomenclatura de los servicios

| Recurso | Nomenclatura                               |                                                                                                    |
| --- |--------------------------------------------|----------------------------------------------------------------------------------------------------|
| Nombre de proyecto | sif-med-bridges-vibrations-[ambiente]      |                                                                                                    |
| GCS raw | sif-med-lakehouse-raw-data-[ambiente]      | gs://sif-med-lakehouse-raw-data-[ambiente]                                                         |
| Directorio raw data | sif-med-raw-data                           | gs://sif-med-lakehouse-raw-data-[ambiente]/sif-med-raw-data/MOBILE_APP/[NOMBRE_ARCHIVO]            |
| Directorio error data | sif-med-error-data                         | gs://sif-med-lakehouse-raw-data-[ambiente]/sif-med-error-data/MOBILE_APP/[NOMBRE_ARCHIVO]          |
| GCS trusted | sif-med-lakehouse-trusted-data-[ambiente]  | gs://sif-med-lakehouse-trusted-data-[ambiente]/MOBILE_APP/                                         |
| Dataproc Workflow | dp_lakehouse_workflow_[ambiente]           |                                                                                                    |
| Dataproc Cluster | dp-carga-lakehouse-pipeline-[ambiente]     |                                                                                                    |
| Dataproc Job | dp-carga-lakehouse-job-[ambiente]          |                                                                                                    |
| BigQuery dataset tablas externas | trusted_mobile_app_external_tables         |                                                                                                    |
| BigQuery dataset vistas | trusted_mobile_app_views                   |                                                                                                    |
| Cloud Scheduler Job | cs-lakehouse-mobileapp-scheduler-[ambiente] |                                                                                                    |

## Nomenclatura de las cuentas de servicio

| Cuenta de servicio | Nomenclatura |
| --- | --- |
| Cuenta de servicio Mobile App escritura GCS raw | sa-[ambiente]-mobile-app-ingest@co-alcaldia-med-bridges-vibrations-[ambiente]_gcp.iam.gserviceaccount.com |
| Cuenta de servicio Cloud Scheduler programacion | sa-[ambiente]-scheduler-orchestration@co-alcaldia-med-bridges-vibrations-[ambiente]_gcp.iam.gserviceaccount.com |