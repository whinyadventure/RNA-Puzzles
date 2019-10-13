export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

kubectl create namespace rabbitmq

kubectl create -f $DIR/role.yaml
kubectl create -f $DIR/binding.yaml

helm install stable/rabbitmq-ha --namespace rabbitmq --tiller-namespace tiller-helm --set replicaCount=1