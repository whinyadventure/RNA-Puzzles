#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $DIR
REGISTRY_NAME=kube-registry

kind delete cluster
kind create cluster --config $DIR/kind-cluster.yaml

until [ -z "$(docker ps -a | grep $REGISTRY_NAME)" ]; do
        docker stop $REGISTRY_NAME || true
        docker rm $REGISTRY_NAME || true
        sleep 5
done
docker run -d -p 5000:5000 --restart=always --name $REGISTRY_NAME registry:2

export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"

while [ -n "$(kubectl get pods --all-namespaces --no-headers | grep -v Running)" ]; do
        sleep 10
done

for node in $(kubectl get nodes --no-headers | awk '{print $1}'); do
        docker exec -it -d $node bash -c "sed -i '/\[plugins.cri.registry.mirrors\]/a\        [plugins.cri.registry.mirrors.\"registry:5000\"]\n\          endpoint = [\"http://registry:5000\"]' /etc/containerd/config.toml"
        docker exec -it -d $node bash -c "systemctl restart containerd"
        echo $node
        echo $(docker inspect --format '{{.NetworkSettings.IPAddress }}' $REGISTRY_NAME)
        docker exec -it -d $node sh -c "echo $(docker inspect --format '{{.NetworkSettings.IPAddress }}' $REGISTRY_NAME)'\t'registry >> /etc/hosts"
done


