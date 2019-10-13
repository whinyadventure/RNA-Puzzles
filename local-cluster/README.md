# Goal
Goal of this folder is to provide local development enviroment that is already configured and ready to use.
## Kubernetes Cluster
We are use [kind](https://github.com/kubernetes-sigs/kind) to start local Kubernetes Cluster.
### Installation
- Install [go](https://golang.org/doc/install)
- Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)(Ubuntu)
- Run `GO111MODULE="on" go get sigs.k8s.io/kind@v0.5.1`

### Usage
`kind-cluster/start.sh` will start Kubernetes cluster with configuration in kind-cluster/kind-cluster.yaml. For example configuration that will create cluster with one control plane and two workers is presented below:
```
kind: Cluster
apiVersion: kind.sigs.k8s.io/v1alpha3
nodes:
- role: control-plane
- role: worker
- role: worker
```
### Kubernetes Dashboard
```
kind-cluster/kub-dashbord.sh
export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
kubectl proxy
```

Next you can go to http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
and enter token.
Token should be printed at the end of executing kube-dashbord.sh eg.
```
...
serviceaccount/admin-user created
clusterrolebinding.rbac.authorization.k8s.io/admin-user created
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTVzbjdyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3YWQ5NjBmNi1jZGFmLTQ5OTUtYTU5NC00ZDExN2Q0Y2MzMjAiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.MXxkKxMtqOS_gUODFhbGKZgX42E7oqYjsVK6aZPugAcMXJEfkMv69NprzwU5LqRLd5a8FWUfEmPhJsY_iU9DaLta98_AImlZMqtpVd1m4Vh4GxM3i5GjWPLJNwipT_5sLkH2AMqYtZyEwBoYRPGljzO0aqhVVnV8ckHLkDkZgrGowG2JnEOJwAxNW280Gl1wOGXgu9JQyBRfWxCIAV7e9CFBaQOIqkCkpfxqxFeKeBh151eL_Aex_mTb9m9tP4teDa-IXCSW8YAeC89SEFc3Be-JGnORY-FYsJVEnngkHhCzQrK4taouiHHTi7Yy20q6E-eiKJZgf4K-0hDzfTWyDQ


Kubernetes dashboard:
 ...
```
## Postgresql and RabbitMq
Postgresql and RabbitMq are installed on cluster using [helm](https://helm.sh/docs/). To install helm go to [this](https://github.com/helm/helm/releases/tag/v2.14.3) site and download version that suit your system.
### Installing helm on cluster
Run `helm/init.sh`.
### Deploying Postgresql on cluster
Run `helm/postgresql/start.sh`
### Deploying Rabbitmq on cluster
Run `helm/rabbitmq/start.sh`
