from airflow.providers.cncf.kubernetes.hooks.kubernetes import KubernetesHook

def check_existing_spark_app(SPARK_APPLICATION_NAME):
    k8s_hook = KubernetesHook(conn_id='k8s')
    print('k8s connected!')
    try:
        existing = k8s_hook.get_custom_object(group="sparkoperator.k8s.io",
                                              version="v1beta2",
                                              namespace="spark-operator",
                                              plural="sparkapplications",
                                              name=SPARK_APPLICATION_NAME)

        if existing:
            print("SparkApplication already exists, delete first")
            k8s_hook.delete_custom_object(group="sparkoperator.k8s.io",
                                       version="v1beta2",
                                       namespace="spark-operator",
                                       plural="sparkapplications",
                                       name=SPARK_APPLICATION_NAME)
    except:
        print("Creating SparkApplication...")