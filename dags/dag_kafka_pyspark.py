from airflow import DAG
from airflow.providers.apache.kafka.sensors.consume import KafkaConsumeSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

# Define the DAG
dag = DAG(
    "fraud_detection_dag",
    default_args=default_args,
    description="A DAG for fraud detection pipeline",
    schedule_interval=None,  
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Kafka Sensor Task
kafka_sensor_task = KafkaConsumeSensor(
    task_id="kafka_sensor",
    kafka_conn_id="kafka_default", 
    topic="fraud-detection",  
    timeout=600,  
    dag=dag,
)

# Task to run the pyspark_consumer.py script
def run_pyspark_script():
    os.system("python dags/scripts/pyspark_consumer.py")

pyspark_task = PythonOperator(
    task_id="run_pyspark_consumer",
    python_callable=run_pyspark_script,
    dag=dag,
)

# Define task dependencies
kafka_sensor_task >> pyspark_task 