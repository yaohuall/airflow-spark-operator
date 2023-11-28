import datetime as dt
from datetime import timedelta, datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.utils.dates import days_ago
from utils import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['example@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 3
}

dag = DAG(
    dag_id='example',
    start_date=dt.datetime(2023, 11, 24),
    default_args=default_args,
    schedule_interval='0 11 * * *',
    tags=['example']
)
start = DummyOperator(task_id="start", dag=dag)

check_existing_spark_app = PythonOperator(
    task_id="check_existing_spark_app",
    python_callable=check_existing_spark_app,
    dag=dag,
    op_kwargs={
         "SPARK_APPLICATION_NAME": "pyspark-example",
     },
)

submit = SparkKubernetesOperator(
    task_id='pyspark_example',
    namespace='spark-operator',
    application_file='/scripts/pyspark-example.yaml',
    kubernetes_conn_id='kubernetes_default',
    do_xcom_push=True,
    dag=dag,
    api_group="sparkoperator.k8s.io",
    api_version="v1beta2",
    # env_vars=env_vars,
)

start >> check_existing_spark_app >> submit