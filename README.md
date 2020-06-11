# Data team bootstrap

This project contains local dev setup for Data team.
it contains following components:

- Kafka broker
- Kafka zookeeper
- Kafka schema registry
- Kafka control center(Optional)
- Datadog daemon set(Optional)
- Jupyter notebook(Optional)

## Pré-requis
You need following components:

- Taskfile
- Helm3

## Quick starts
Simple run :
``` task run.local ```
```bash
zhaolong@Odyssus ~/workspace/data-team-bootstrap (git)-[master] % task run.local             
task start.minikube; eval $(minikube docker-env); task deploy;

if minikube status | grep Running; then echo "minikube running..."; else echo "starting minikube"; minikube start; fi
host: Running
kubelet: Running
apiserver: Running
minikube running...
kubectl config set-context minikube --namespace=$NAMESPACE
Context "minikube" modified.
kubectl config use-context minikube --namespace=$NAMESPACE
Switched to context "minikube".
helm upgrade $PROJECT_NAME $PROJECT_NAME-helm \
  --namespace $NAMESPACE \
  --install \
  --atomic \
  --cleanup-on-fail \
  --force \
  --wait \
  --timeout 600s \
  --values helm-values/$PROJECT_NAME-helm-values/values-$ENV.yaml

Release "data-team-bootstrap" does not exist. Installing it now.
NAME: data-team-bootstrap
LAST DEPLOYED: Thu Jun 11 09:32:16 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
Here is a table to list how to access to bootstrapped services:

|Service name           |Minikube internal endpoint |Localhost endpoint                 |
|-----------------------|---------------------------|-----------------------------------|
|broker                 |broker:9092                | `minikube service broker `        |
|kafka-schema-registry  |kafka-schema-registry:8081 |None                               |
|zookeeper              |zookeeper:2181             |None                               |
|control-center         |control-center:9021        |`minikube service control-center`  |
|jupyter-notebook       |jupyter-notebook:8888      |`minikube service jupyter-notebook`|
|datadog-agent          |datadogstatsd:8125         |None                               |

## User configurations
As the bootstrap project is configured by a helm you have some flexibility to configure it, Especially the components docker images, find the default helm value configurations in `data-team-bootstrap-helm/values.yaml`, you can overwrite them in the file : `./helm-values/$service-helm-values/values-local.yaml`

|Service name           |Image name                                       |Default enabled |
|-----------------------|-------------------------------------------------|----------------|
|broker                 |confluentinc/cp-enterprise-kafka:4.1.0-1         |True            |
|kafka-schema-registry  |confluentinc/cp-schema-registry:4.1.0-1          |True            |
|zookeeper              |confluentinc/cp-schema-registry:4.1.0-1          |True            |
|control-center         |confluentinc/cp-enterprise-control-center:4.1.0-1|False           |
|jupyter-notebook       |jupyter/minimal-notebook:latest                  |False           |
|datadog-agent          |datadog/agent:latest-jmx                         |True            |

As a Data Analyst you may want to change the default `jupyter-notebook` image to be some of the more data specific images.

## Change your minikube default container memory limit
You should set a default container memory limit for your minikube if you don't have a big amount of RAM
``` yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 256Mi
    defaultRequest:
      memory: 128Mi
    type: Container
```