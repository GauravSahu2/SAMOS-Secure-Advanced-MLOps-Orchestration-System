
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('samos_enterprise_pipeline', start_date=datetime(2024, 1, 1), schedule_interval='@daily') as dag:
    data_ops = BashOperator(task_id='data_ops', bash_command='samos --group dataops')
    ml_ops = BashOperator(task_id='ml_ops', bash_command='samos --group mlops')
    model_sec = BashOperator(task_id='model_sec', bash_command='samos --group modelsecops')
    
    data_ops >> ml_ops >> model_sec
