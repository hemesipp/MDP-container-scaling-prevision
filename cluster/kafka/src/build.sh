cd ./producer
sudo docker build --rm -t producer:v0 . -f Dockerfile

cd ../consumer
sudo docker build --rm -t consumer:v0 . -f Dockerfile