from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.gcs import GCSDeleteObjectsOperator  # Corrected import
from airflow.contrib.operators.dataflow_operator import DataflowPythonOperator

#from airflow.providers.google.cloud.operators.dataflow import DataflowTemplateOperator

# Default args for the DAG
default_args = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'gcp_workflow',
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

    # Example Task: Load Data from GCS to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq',
        bucket='gfcp-bucket',
        source_objects=['my-source-bucket/sample_data.csv'],
        destination_project_dataset_table='bright-antonym-436213-v2.my_dataset.my_table',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
    )

    # # Example Task: Trigger a Dataflow Job
    # trigger_dataflow = DataflowTemplateOperator(
    #     task_id='trigger_dataflow',
    #     template='gs://gfcp-bucket/dataflow-templates/Dataflow_M_code',
    #     job_name='dataflow-job-example',
    #     location='us-central1',
    #     parameters={
    #         'inputFile': 'gs://gfcp-bucket/my-source-bucket/sample_data.csv',
    #         'output': 'gs://gfcp-bucket/my-destination-bucket/',
    #     },
    # )
  #Python templates for your Dataflow job
    trigger_dataflow = DataflowPythonOperator(
    task_id='trigger_dataflow',
    job_name='dataflow-job-example',
    template='gs://gfcp-bucket/dataflow-templates/Dataflow_M_code.py',  # Python template path
    location='us-central1',
    parameters={
        'inputFile': 'gs://gfcp-bucket/my-source-bucket/sample_data.csv',
        'output': 'gs://gfcp-bucket/my-destination-bucket/',
    },
    project_id='bright-antonym-436213-v2',  # Add project_id here
)

    # Task to delete the file from GCS
    delete_source_file = GCSDeleteObjectsOperator(  # Using the correct operator
        task_id='delete_file',
        bucket='gfcp-bucket',  # Replace with your GCS bucket name
        object_names=['my-source-bucket/sample_data.csv'],  # Use a list to delete objects
    )

    # Task dependencies
    create_bq_table >> load_gcs_to_bq >> trigger_dataflow >> delete_source_file
