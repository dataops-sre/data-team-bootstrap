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

- Minikube
- Make
- Helm + Tillerless plugin

Install upon packages with your prefer package manager, to install helm Tillerless plugin:
```bash
helm init --client-only \
helm plugin install https://github.com/rimusz/helm-tiller \
helm plugin update tiller
```

## Quick starts
Simple run :
``` make deploy ```
```bash
zhaolong@Odyssus ~/workspace/data-team-bootstrap % make deploy
Switched to context "minikube".
Makefile:12: avertissement : variable « NAMESPACE » indéfinie
for service in data-team-bootstrap; do \
        helm tiller run  -- helm upgrade --install --wait "$service" data-team-bootstrap-helm --values ./helm-values/$service-helm-values/values-local.yaml
done
Installed Helm version v2.12.3
Installed Tiller version v2.12.3
Helm and Tiller are the same version!
Starting Tiller...
Tiller namespace: kube-system
Running: helm upgrade --install --wait data-team-bootstrap data-team-bootstrap-helm --values ./helm-values/data-team-bootstrap-helm-values/values-local.yaml

Release "data-team-bootstrap" has been upgraded. Happy Helming!
LAST DEPLOYED: Thu Feb 28 13:31:18 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1beta1/Deployment
NAME                   DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
broker                 1        1        1           1          4m53s
kafka-schema-registry  1        1        1           1          4m53s
zookeeper              1        1        1           1          4m53s

==> v1/Pod(related)
NAME                                    READY  STATUS   RESTARTS  AGE
datadog-agent-bgs2v                     1/1    Running  0         4m53s
jupyter-notebook-7d9bd49b87-8rjzd       1/1    Running  0         98s
broker-6679944c58-p2vv2                 1/1    Running  0         4m53s
kafka-schema-registry-6659797cc5-f9ntr  1/1    Running  0         4m53s
zookeeper-5d5cb47745-jcwgz              1/1    Running  0         4m53s

==> v1/ConfigMap
NAME            DATA  AGE
datadog-config  2     4m53s

==> v1/Service
NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)                        AGE
datadogstatsd          ClusterIP  10.107.69.107   <none>       8125/UDP                       4m53s
jupyter-notebook       NodePort   10.109.171.163  <none>       8888:30040/TCP                 98s
broker                 NodePort   10.110.233.63   <none>       9092:30537/TCP,9999:30727/TCP  4m53s
kafka-schema-registry  ClusterIP  10.111.130.26   <none>       8081/TCP                       4m53s
zookeeper              ClusterIP  10.103.7.91     <none>       2181/TCP                       4m53s

==> v1beta1/DaemonSet
NAME           DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR  AGE
datadog-agent  1        1        1      1           1          <none>         4m53s

==> v1/Deployment
NAME              DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
jupyter-notebook  1        1        1           1          98s


Stopping Tiller...
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