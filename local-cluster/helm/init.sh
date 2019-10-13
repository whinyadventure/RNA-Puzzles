#!/bin/bash

export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
kubectl create namespace tiller-helm
kubectl create serviceaccount tiller --namespace tiller-helm

kubectl create -f $DIR/role-helm.yaml
kubectl create -f $DIR/binding.yaml

helm init --service-account tiller --tiller-namespace tiller-helm --wait --upgrade
