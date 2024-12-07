import os
import gzip
import shutil
from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartTemplateOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

# Python function to compress files
def compress_files(source_dir, output_file):
    """Compress multiple files into a single gzip archive."""
    with open(output_file, 'wb') as f_out:
        for file_name in os.listdir(source_dir):
            full_path = os.path.join(source_dir, file_name)
            if os.path.isfile(full_path):  # Skip directories
                with open(full_path, 'rb') as f_in:
                    shutil.copyfileobj(f_in, f_out)
    print(f"Compressed files saved at {output_file}")

with DAG(
    dag_id='dataflow_bulk_file_compression',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Compress the files locally
    compress_task = PythonOperator(
        task_id='compress_files',
        python_callable=compress_files,
        op_kwargs={
            'source_dir': '/path/to/source/files',  # Local directory with bulk files
            'output_file': '/path/to/output/compressed_files.gz',  # Output compressed file
        },
    )

    # Task 2: Upload the compressed file to GCS
    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_compressed_to_gcs',
        src='/path/to/output/compressed_files.gz',  # Local compressed file
        dst='compressed_files/compressed_files.gz',  # GCS destination path
        bucket_name='your-gcs-bucket-name',  # Your GCS bucket name
    )

    # Task 3: Start the Dataflow job
    start_dataflow_job = DataflowStartTemplateOperator(
        task_id='start_dataflow_job',
        project_id='your-project-id',
        location='us-central1',
        template_name='your-template-name',  # Predefined Dataflow template
        parameters={
            'input': 'gs://your-gcs-bucket-name/compressed_files/compressed_files.gz',  # Input file
            'output_table': 'your-project-id:your_dataset.your_table',  # BigQuery output
            'write_disposition': 'WRITE_APPEND',
        },
        gcp_conn_id='google_cloud_default',
    )

    # Define task dependencies
    compress_task >> upload_to_gcs >> start_dataflow_job
