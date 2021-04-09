# delete all deployments, services, statefulsets and pods created
kubectl delete deployment pacman
kubectl delete service pacman
kubectl delete deployment producer
kubectl delete statefulset broker
kubectl delete deployment zookeeper
kubectl delete service broker
kubectl delete service zookeeper-service
kubectl delete pods --all