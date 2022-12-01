import airflow
import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from Airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from app.get_categories import extract_categories
# create_businesses_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# instantiating the Postgres Operator

# Postgres connection id from airflow configuration
POSTGRES_CONN_ID="postgres_db"

## Airflow default arguments for postgres

args={'owner': 'airflow'}

default_args = {
    'owner': 'airflow',    
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    #'email': ['airflow@example.com'],
    #'email_on_failure': False,
    # 'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id="postgres_operator_dag",
    start_date=datetime.datetime(year=2022, month=11, day=26),
    schedule_interval="@once",
    catchup=False,
) as dag:
    create_database_tables = PostgresOperator(
        task_id="create_database_tables",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="sql/businesses_schema.sql",
        ),
    get_categories = PythonOperator(
        task_id="get_categories"
        python_callable=
    )
    

create_database_tables