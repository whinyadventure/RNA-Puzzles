export KUBECONFIG="$(kind get kubeconfig-path --name="kind")" 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta4/aio/deploy/recommended.yaml
kubectl apply -f $DIR/dashboard-adminuser.yaml
kubectl apply -f $DIR/admin-role-binding.yaml 
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}') | grep token:
echo "

Kubernetes dashboard:
 
#export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
#kubectl proxy

Next go to http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
and enter token
"