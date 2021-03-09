FROM python:3.7

#RUN mkdir /app \
#&& pip install kafka-python
WORKDIR /app
ADD . /app/

#EXPOSE 9092
CMD ["python","-u", "/app/new_consumer.py"]
