from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from airflow.decorators import task
from airflow.models.xcom import XCom
import os

def download_file(url:str, file_path:str) -> BashOperator:
    cmd = f"curl {url} --output {file_path}"
    return BashOperator(task_id="download_file", bash_command=cmd)

@task(task_id="lines_counter")
def lines_counter(file_path:str, ti=None):
    counter = -1 # first line is header
    with open(file_path, "r") as f:
        for _ in f:
            counter+=1
    ti.xcom_push(key="lines_count", value=counter)


@task(task_id="add_column")
def add_column(file_path:str, ti=None):
    counter = ti.xcom_pull(task_ids="lines_counter", key="lines_count")
    new_file_path = file_path + ".tmp"
    with open(file_path, "r") as input:
        with open(new_file_path, "w") as output:
            is_first_line = True
            for line in input:
                if (is_first_line):
                    output.write(line[:-1] + ", \"Reverse order\"\n")
                    is_first_line = False
                else:
                    output.write(line[:-1] + f", {counter}\n")
                    counter-=1
    os.remove(file_path)
    os.rename(new_file_path, file_path)

with DAG(dag_id="_prcatice", start_date=datetime(2022, 11, 30), schedule="0 6 * * *") as dag:
    file_path = Variable.get("practice_file_path")

    download_task = download_file("https://people.sc.fsu.edu/~jburkardt/data/csv/snakes_count_100.csv", file_path)
    count_task = lines_counter(file_path)
    numerate_task = add_column(file_path)
    move_file_task = BashOperator(task_id="move_file", bash_command=f"mv {file_path} /opt/airflow/dags/result.csv")
    success_task = BashOperator(task_id="success", bash_command="echo \"Success\"")
    download_task >> count_task >> numerate_task >> move_file_task >> success_task
