from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def hello():
    print("Hello!")


with DAG(dag_id="first_dag", start_date=datetime(2022, 1, 1), schedule="0 0 * * *") as dag:
    bash_task = BashOperator(task_id="hello", bash_command="echo hello")
    python_task = PythonOperator(task_id="world", python_callable=hello)
    bash_task >> python_task
