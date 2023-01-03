
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
from datetime import datetime, timedelta
import requests
from get_zipcodes import zipcode_get
from dotenv import load_dotenv

load_dotenv('../.devcontainer/')  # take environment variables from .env.

YELP_API_KEY = os.environ.get("YELP_API_KEY")

# Connection to the database

'''
with airflow download a zip file from a url, unzip the file and place it in a tmp folder.
The unzipped file is a csv containing state and zip codes,
read the csv and insert the states and zip codes to a database.
'''
database_connection = 'postgres_local'
dbname = 'yelpDB'

# Define default_args dictionary to specify default parameters of the DAG, such as the start date and the frequency at which to run
default_args = {
    'owner': 'me',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False
}

# Create a DAG instance and pass it the default_args dictionary
dag = DAG(
    'yelp_data_collection',
    default_args=default_args,
    description='Collect data from Yelp API',
    # Set the frequency at which to run the DAG
    schedule_interval=timedelta(hours=24)
)

# Define a function that retrieves all categories from the Yelp API


def retrieve_yelp_categories():

    # Set the base URL for the Yelp API endpoint
    base_url = "https://api.yelp.com/v3/categories"

    # Set the API key and other parameters for the request
    api_key = YELP_API_KEY
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Make the request to the Yelp API
    response = requests.get(base_url, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # If the request was successful, get the JSON data from the response
        data = response.json()

        # Return the list of categories
        return data["categories"]
    else:
        # If the request was unsuccessful, print an error message
        print(f"An error occurred: {response.status_code}")


# Define a function that retrieves data from the Yelp API for a specific category
def retrieve_yelp_data_for_category(categories):

    # Iterate through the list of categories
    for category in categories:
        # Set the base URL for the Yelp API endpoint
        base_url = "https://api.yelp.com/v3/businesses/search"

        # Set the API key and other parameters for the request
        api_key = YELP_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "term": "coffee shop",
            "location": "San Francisco, CA",
            "categories": category["alias"]
        }

        # Make the request to the Yelp API
        response = requests.get(base_url, headers=headers, params=params)

        # Check the status code of the response
        if response.status_code == 200:
            # If the request was successful, get the JSON data from the response
            data = response.json()

            # Iterate through the list of businesses and print their names
            for business in data["businesses"]:
                print(business["name"])
        else:
            # If the request was unsuccessful, print an error message
            print(f"An error occurred: {response.status_code}")


def get_zip_codes():
    # Code to get a list of all zip codes in the United States
    pass


def get_businesses_by_zip_code(zip_code, **kwargs):
    # Code to use the Yelp API to get all business data for businesses
    # in the specified zip code
    pass


def insert_business_data_into_postgres(**kwargs):
    # Code to insert the business data into the Postgres database
    # using the PostgresOperator
    business_data = kwargs['business_data']

    # for data in business_data:
    #     sql = f"INSERT INTO yelp_businesses (name, address, zip_code) VALUES ('{data['name']}', '{data['address']}', '{data['zip_code']}')"
    #     task = PostgresOperator(
    #         task_id=f'insert_business_{data['id']}',
    #         postgres_conn_id=database_connection,
    #         sql=sql,
    #         dag=dag,
    #     )
    #     task.execute(context=kwargs['context'])


# Define a task that retrieves all categories from the Yelp API
retrieve_yelp_categories_task = PythonOperator(
    task_id='retrieve_yelp_categories',
    python_callable=retrieve_yelp_categories,
    provide_context=True,  # enable passing context to downstream tasks
    dag=dag
)

# Define a task that retrieves data from the Yelp API for a specific category
retrieve_yelp_data_task = PythonOperator(
    task_id='retrieve_yelp_data_for_category',
    python_callable=retrieve_yelp_data_for_category,
    # pass the returned values from the retrieve_yelp_categories_task as an argument to the function
    op_args=[
        "{{ task_instance.xcom_pull(task_ids='retrieve_yelp_categories') }}"],
    provide_context=True,  # enable passing context from upstream tasks
    dag=dag
)


create_tables = PostgresOperator(
    task_id='create_tables',
    sql='sql/yelp_full_stack.sql',
    postgres_conn_id=database_connection,
    dag=dag,
)

get_zip_codes_task = PythonOperator(
    task_id='get_zip_codes',
    python_callable=get_zip_codes,
    provide_context=True,
    dag=dag,
)

get_businesses_by_zip_code_task = PythonOperator(
    task_id='get_businesses_by_zip_code',
    python_callable=get_businesses_by_zip_code,
    provide_context=True,
    dag=dag,
)

insert_business_data_task = PythonOperator(
    task_id='insert_business_data_into_postgres',
    python_callable=insert_business_data_into_postgres,
    provide_context=True,
    dag=dag,
)


# Set the dependencies for the tasks
retrieve_yelp_categories_task >> retrieve_yelp_data_task >> create_tables


# create_database >> get_zip_codes_task >> get_businesses_by_zip_code_task >> insert_business_data_task
