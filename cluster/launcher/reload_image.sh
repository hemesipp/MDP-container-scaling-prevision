# Reload job-consumer, producer and pacman images
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
