# Clean and reload job_consumer, producer and pacman
kubectl delete deployment pacman
kubectl delete service pacman
kubectl delete deployment producer
kubectl delete pods --all
cd ..
cd src/deployments/prod
kubectl create -f deployment-pacman.yml
kubectl create -f deployment-producer.yml
cd ..
cd ..
cd ..
cd launcher
python3 create_first_job_consumer.py


