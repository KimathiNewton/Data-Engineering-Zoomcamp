import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
  
# The reason we save it in AIRFLOW_HOME is because if we save in default location, all these files will be deleted after the task finishes
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# The interval of how we want to run the job, which is all the data accumulated for the last month
local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *",  # every 2nd of the month at 6 AM
    start_date=datetime(2021, 1, 1),
)

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"


URL_PREFIX ="https://d37ci6vzurychx.cloudfront.net/trip-data"
URL_TEMPLATE= URL_PREFIX + "/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
OUTPUT_FILE_TEMPLATE= path_to_local_home + 'output_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"'
with local_workflow:
    # The first task is downloading the file using curl
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
        
    )

    # The second task is to list the contents of the directory
    ingest_task = BashOperator(
        task_id="ingest",
        bash_command=f"ls {path_to_local_home}"  
    )

    # We specify the task dependencies
    wget_task >> ingest_task
