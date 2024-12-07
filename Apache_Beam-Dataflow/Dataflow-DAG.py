pip install apache-airflow-providers-google # type: ignore

#starting the Airflow web server
airflow webserver # type: ignore
airflow scheduler # type: ignore

#trigger airflow from web
airflow dags trigger dataflow_job_example # type: ignore




from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartTemplateOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='dataflow_job_example',
    default_args=default_args,
    schedule_interval=None,  # Set to your desired schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Run a Dataflow job from a template
    start_dataflow_job = DataflowStartTemplateOperator(
        task_id='start_dataflow_job',
        project_id='your-project-id',  # Replace with your GCP Project ID
        location='us-central1',  # Replace with your Dataflow region
        template_name='your-template-name',  # Replace with your Dataflow template
        parameters={
            'input': 'gs://your-bucket-name/input-data',
            'output': 'gs://your-bucket-name/output-data',
        },
        gcp_conn_id='google_cloud_default',  # GCP connection ID
    )

    start_dataflow_job




    #Custom airflow dag

from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator

run_custom_dataflow_job = DataflowCreatePythonJobOperator(
    task_id='run_custom_dataflow_job',
    py_file='gs://your-bucket-name/your-dataflow-script.py',
    project_id='your-project-id',
    location='us-central1',
    job_name='custom-dataflow-job',
    py_options=['-m'],
    options={
        'input': 'gs://your-bucket-name/input-data',
        'output': 'gs://your-bucket-name/output-data',
    },
    gcp_conn_id='google_cloud_default',
)

#BigQuery output 

from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartTemplateOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='dataflow_job_to_bigquery',
    default_args=default_args,
    schedule_interval=None,  # Set to your desired schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Run a Dataflow job from a template and write output to BigQuery
    start_dataflow_job = DataflowStartTemplateOperator(
        task_id='start_dataflow_job_to_bigquery',
        project_id='your-project-id',  # Replace with your GCP Project ID
        location='us-central1',  # Replace with your Dataflow region
        template_name='your-template-name',  # Replace with your Dataflow template
        parameters={
            'input': 'gs://your-bucket-name/input-data',  # Input data
            'output_table': 'your-project-id:your_dataset.your_table',  # BigQuery table
            'write_disposition': 'WRITE_APPEND',  # Options: WRITE_TRUNCATE, WRITE_APPEND
        },
        gcp_conn_id='google_cloud_default',  # GCP connection ID
    )

    start_dataflow_job

#custom python dataflow job

from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='custom_dataflow_to_bigquery',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    run_dataflow_job = DataflowCreatePythonJobOperator(
        task_id='run_custom_dataflow_job',
        py_file='gs://your-bucket-name/your-dataflow-script.py',  # Your Python script for Dataflow
        project_id='your-project-id',  # Replace with your GCP Project ID
        location='us-central1',  # Replace with your Dataflow region
        job_name='dataflow-to-bigquery',
        options={
            'input': 'gs://your-bucket-name/input-data',  # Input data
            'output_table': 'your-project-id:your_dataset.your_table',  # BigQuery table
            'temp_location': 'gs://your-bucket-name/temp/',  # Temporary location
        },
        gcp_conn_id='google_cloud_default',  # GCP connection ID
    )

    run_dataflow_job


