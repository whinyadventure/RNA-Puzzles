export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#kubectl create namespace postgresql
#kubectl create serviceaccount tiller --namespace postgresql
kubectl create namespace rnapuzzles
kubectl create -f $DIR/role.yaml
kubectl create -f $DIR/binding.yaml

helm install stable/postgresql --namespace rnapuzzles --tiller-namespace tiller-helm --set postgresqlPassword=password --name postgres

kubectl -n rnapuzzles \
             wait --for=condition=running --timeout=1m svc/postgres-postgresql
kubectl port-forward --namespace rnapuzzles  svc/postgres-postgresql 5432:5432

echo "
To export port to local host use:
kubectl port-forward --namespace postgresql  svc/postgres-postgresql 5432:5432

Postgres port: 5432
user: postgres
password: password
"