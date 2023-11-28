# airflow-spark-operator
Running Apache Airflow SparkKubernetesOperator on K8s
### Prerequisite
- **Docker**: docker engine community, v23.0.1
- **Apache Airflow**: v2.7.2 
### Need to update

### Framework version
- Apache Spark image: v3.3.3

### File tree
```bash

├── README.md
├── example_dag.py #Airflow dag
├── scripts
│   ├── pyspark-example.yaml #Spark operator pod yaml
└── <other_modules>
└── utils.py #helper function
```

### How to use this repo?
- Wrap up your Pyspark code in image and upload to docker hub.
- Specify your image, Apache Spark version and Pyspark file location of your image in your deploy yaml file.
- Change Spark application name in dag file.
    ```
    check_existing_spark_app = PythonOperator(
        task_id="check_existing_spark_app",
        python_callable=check_existing_spark_app,
        dag=dag,
        op_kwargs={
             "SPARK_APPLICATION_NAME": "pyspark-example", #change this line
         },
    )
    ```
