# Launch all the simulation -- prerequisites: launch minikube
cd ..
eval $(minikube docker-env)
cd src/images/prod/producer
docker build -t producer:latest .
cd ..
cd pod_job_consumer
docker build -t job-consumer:latest .
cd ..
cd pacman
docker build -t pacman:latest .

cd ..
cd ..
cd ..
cd deployments/prod
kubectl create -f deployment-zookeeper.yml
kubectl create -f service-kafka.yml
kubectl create -f deployment-kafka.yml
kubectl create -f role.yaml
kubectl create -f role-binding.yaml
kubectl create -f deployment-pacman.yml
kubectl create -f deployment-producer.yml
cd ..
cd ..
cd ..
cd launcher
python3 create_first_job_consumer.py


