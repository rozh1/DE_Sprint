from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
from airflow.decorators import task
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.exceptions import AirflowSensorTimeout
from airflow.sensors.python import PythonSensor
import os
import shutil
import pandas as pd

POSTGRES_CONN_ID = "pgdb"


@task(task_id="pg_prepare")
def pg_prepare(file_path: str, pg_dir: str):
    query = """CREATE TABLE if not exists practice (game_number integer PRIMARY KEY, game_length integer NOT NULL); 
        TRUNCATE practice;"""
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.commit()

    file = os.path.join(pg_dir, os.path.basename(file_path))
    shutil.copy(file_path, file)

    copy_query = f"""COPY practice(game_number, game_length)
FROM '{file}'
DELIMITER ','
CSV HEADER;"""
    cursor = connection.cursor()
    cursor.execute(copy_query)
    cursor.close()
    connection.commit()

    connection.close()

@task(task_id="processing")
def process_data(ti=None):
    query = """select * from practice_etl;"""
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)

    df = pd.DataFrame(cursor.fetchall(), columns=['game_number', 'game_length', 'game_lenght_ratio'])
    stats = df['game_length'].describe().to_json()
    ti.xcom_push(key="stats", value=stats)

    cursor.close()
    connection.close()

def pg_check_data():
    query = "select game_number from practice limit 1;"
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    records_exist = len(cursor.fetchall()) > 0
    cursor.close()
    connection.close()

    return records_exist


def download_file(url: str, file_path: str) -> BashOperator:
    cmd = f"curl {url} --output {file_path}"
    return BashOperator(task_id="download_file", bash_command=cmd)


def _failure_callback(context):
    if isinstance(context['exception'], AirflowSensorTimeout):
        print(context)
        print("Sensor timed out")


with DAG(dag_id="pratice_pg", start_date=datetime(2022, 11, 30), schedule="0 6 * * *") as dag:
    file_path = Variable.get("practice_file_path")
    pg_dir = Variable.get("pg_dir")

    download_task = download_file(
        "https://people.sc.fsu.edu/~jburkardt/data/csv/snakes_count_100.csv", file_path)
    db_prepare_task = pg_prepare(file_path, pg_dir)
    waiting_for_data = PythonSensor(task_id="waiting_for_data", poke_interval=60,
                                    timeout=60 * 30, mode="reschedule", soft_fail=True, 
                                    on_failure_callback=_failure_callback, python_callable=pg_check_data)
    etl_task = PostgresOperator(
        task_id="etl_task",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""CREATE TABLE if not exists practice_etl (game_number integer PRIMARY KEY, game_length integer NOT NULL, game_length_ratio numeric NOT NULL);
        TRUNCATE practice_etl;
        INSERT INTO practice_etl SELECT game_number, game_length, game_length/(SELECT MAX(game_length)::numeric from practice) from practice;""",
        autocommit=True,
    )

    processing_task = process_data()

    send_email = EmailOperator(
        task_id='send_email',
        to='abduevsultanmurad@yandex.ru',
        subject='Практика 3.6',
        html_content="""<p>Классен Роман Константинович</p>
        <a href="https://people.sc.fsu.edu/~jburkardt/data/csv/snakes_count_100.csv">snakes_count_100.csv</a>
        <p>Статистика по длине игры</p>
        <pre>{{ task_instance.xcom_pull(task_ids='processing', key='stats') }}</pre> 
        <p>GIT: <a href="https://github.com/rozh1/DE_Sprint/tree/main/3/3.6">https://github.com/rozh1/DE_Sprint/tree/main/3/3.6</a></p>
        """)
        
    download_task >> db_prepare_task >> waiting_for_data >> etl_task >> processing_task >> send_email
