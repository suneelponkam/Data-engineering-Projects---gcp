from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

# Default args for the DAG
default_args = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'example_gcp_workflow',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Example Task: Create a BigQuery Table
    create_bq_table = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table',
        dataset_id='my_dataset',
        table_id='my_table',
        schema_fields=[
            {'name': 'id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
        ],
        project_id='bright-antonym-436213-v2',
    )

    # # Example Task: Transform a File in GCS
    # transform_file = GCSFileTransformOperator(
    #     task_id='transform_file',
    #     source_bucket='gfcp-bucket/my-source-bucket',
    #     source_object='sample.csv',
    #     destination_bucket='gfcp-bucket/my-destination-bucket',
    #     destination_object='transformed_file.csv',
    #     transform_script='/home/airflow/gcs/data/transform_script.py',
    # )

    # Example Task: Trigger a Dataflow Job
    # trigger_dataflow = DataflowTemplateOperator(
    #     task_id='trigger_dataflow',
    #     template='gs://dataflow-templates/latest/Word_Count',
    #     job_name='dataflow-job-example',
    #     location='us-central1',
    #     parameters={
    #         'inputFile': 'gs://my-source-bucket/source_file.txt',
    #         'output': 'gs://my-destination-bucket/output/',
    #     },
    # )

    # Example Task: Load Data from GCS to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq',
        bucket='gfcp-bucket',
        source_objects=['my-source-bucket/sample.csv'],
        destination_project_dataset_table='bright-antonym-436213-v2.my_dataset.my_table',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )

    # Task dependencies
    create_bq_table >> load_gcs_to_bq
  